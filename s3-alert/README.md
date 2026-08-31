# s3-alert

S3 특정 경로에 파일이 올라오면 내용을 메일로 보내주는 크론 스크립트.
알림 파이프라인이 늘어나도 스크립트는 하나이고, 늘어나는 건 `pipelines.yaml` 항목뿐이다.

```
s3_mail_alert.py        공용 러너
pipelines.yaml          경로 / 수신자 / 문구
test_s3_mail_alert.py   순수함수 유닛테스트
```

## 왜 S3 파일을 알림 전송로로 쓰냐

알림을 발생시키는 앱들이 클라우드·폐쇄망·온프렘·로컬에 흩어져 있다. 모니터링 서버로 직통 경로(웹훅,
메시지큐, 에이전트)를 새로 뚫으려면 환경마다 방화벽·인증을 협의해야 하고 폐쇄망은 아예 못 뚫는다.

**그런데 S3는 조직 데이터레이크라서 이미 모든 환경에서 접근된다.** 경로도 자격증명도 이미 있으니
알림 전용 채널을 새로 깔지 않고 이미 뚫린 길에 얹었다. 앱이 조건 걸리면 파일을 올리고,
**파일이 올라온 것 자체가 알림이다.** 알림이 파일로 남아 나중에 다시 볼 수 있는 것도 덤이다.

받는 쪽은 모니터링 호스트(EC2) 한 대이고 크론으로 S3만 본다.

## 동작

1. 시간 파티셔닝 경로로 이번 회차 대상 프리픽스를 만든다
2. 그 밑 모든 파일을 읽는다 (gzip이면 매직바이트로 판별해서 푼다 = zcat)
3. 합본을 `sort -u` 한다 — 줄 단위 중복만 접고 **세부 파싱은 안 한다**
4. 메일로 보낸다. 원본을 통째로 받아볼 `aws s3 cp` 한 줄도 같이 넣는다

메일 본문은 이렇게 나온다.

```
kr-r2o-live 에서 여태 들어온 적 없는 로그타입이 감지되었습니다.

대상 시간대: 2026-08-31 13시 (Asia/Seoul)
알림 파일: 6건 / sort -u 후 4줄

## 내용

{"log_type": "chat", ...}
...

원본 그대로 받아보려면:
  aws s3 cp --recursive s3://<버킷>/alert/... ./kr-r2o-newlog-live-20260831-1300/
```

## 세 가지만 지킨다

- **상태를 기억하지 않는다.** 시간 파티셔닝 경로가 "이번 회차 대상"의 정의다. 어디까지 알렸는지
  기억할 필요가 없다. 목록조회량도 안 늘고, 재발송은 `offset_hours` 만 바꿔 수동 실행하면 된다.
  대신 **크론 주기와 파티션 단위를 1:1로 맞춰야 한다** (hour 파티션 → 시간별 크론).
- **S3에 쓰지도 지우지도 않는다.** 읽은 파일을 `sent/` 로 옮기는 방식은 모니터에 쓰기·삭제 권한을
  요구한다. 보기만 하는 프로세스가 데이터레이크를 지울 수 있게 되는 건 교환비가 안 맞는다.
- **로컬 파일을 안 만든다.** 받아서 풀고 합치는 걸 전부 메모리에서 하니 치울 임시파일이 없다.
  알림 볼륨이 극소라 가능한 방식이다.

## 실행

```bash
export SMTP_SERVER=<smtp주소> SMTP_PORT=25
uv run s3_mail_alert.py kr-r2o-newlog-live
```

인자는 `pipelines.yaml` 의 파이프라인 키다. 크론 한 줄 = 파이프라인 하나.

```
# cron은 PATH가 최소라 uv 경로를 넣어줘야 한다
PATH=/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin:/bin
SMTP_SERVER=<smtp주소>
SMTP_PORT=25
MAILTO=<장애수신주소>

15 * * * * uv run /home/ubuntu/works/wai-monitor/s3-alert/s3_mail_alert.py kr-r2o-newlog-live >> /var/log/s3_alert.log
```

- 파티션이 다 채워진 뒤 읽도록 정시가 아니라 `:15` 에 걸고, `offset_hours: 1` 로 직전 파티션을 본다
- `MAILTO` 를 두고 **stdout만** 리다이렉션하면 스크립트가 죽었을 때 stderr가 크론을 통해 메일로 온다.
  스크립트 자체의 장애 알림을 따로 만들 필요가 없다

## 알림 추가

`pipelines.yaml` 에 항목 하나. 스크립트는 건드리지 않는다.

```yaml
  kr-xxx-error-live:
    bucket: "<버킷>"
    prefix: "alert/error.beat.xxx.live"
    partition_format: "year=%Y/month=%m/day=%d/hour=%H"   # S3 sink 의 path.format 과 같은 단위
    partition_tz: "Asia/Seoul"                            # S3 sink 의 timezone 과 같아야 함
    offset_hours: 1
    subject: "[kr-xxx-live] 에러 레코드 발생"
    message: "kr-xxx-live 에서 처리할 수 없는 레코드가 발생했습니다."
    to: "<수신주소>"
```

`partition_tz` 를 커넥터와 다르게 적으면 어긋난 경로를 보고 "파일 없음"으로 조용히 끝난다.
SMTP 서버·포트는 보안사항이라 yaml에 두지 않고 환경변수로 넘긴다.

## 테스트

```bash
uv run test_s3_mail_alert.py
```

S3·SMTP를 건드리지 않는 순수함수만 검증한다. 파티션 경로 계산, 타임존, gzip 판별, `sort -u`,
본문 조립, 그리고 `pipelines.yaml` 에 모르는 항목이 섞이지 않았는지.
