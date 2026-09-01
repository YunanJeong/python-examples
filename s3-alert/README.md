# s3-alert

S3 특정 경로에 파일이 올라오면 그 내용을 메일로 보내는 크론 스크립트.
알림이 늘어나도 스크립트는 하나이고 `pipelines.yaml` 항목만 추가한다.

```
s3-alert/
├── s3_mail_alert.py        공용 러너
├── pipelines.yaml          설정 전부 (SMTP / 대상 경로 / 수신자 / 문구)
└── test_s3_mail_alert.py   순수함수 유닛테스트
```

알림 발생 앱들이 클라우드·폐쇄망·온프렘·로컬에 흩어져 있어 직통 경로를 뚫기 어렵다.
S3는 조직 데이터레이크라 이미 전 환경에서 접근되므로 그 길에 얹었다 — **파일 업로드가 곧 알림이다.**

## 실행

```bash
uv run s3_mail_alert.py kr-r2o-newlog-live      # 인자는 pipelines.yaml 의 키
```

크론 한 줄 = 파이프라인 하나. **크론 주기와 파티션 단위를 1:1로 맞춘다.(default hourly 기준으로 작업한다.)**

```sh
# 크론은 PATH가 최소라 uv 를 못 찾는다
PATH=/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin:/bin

# 매시 15분 + hour 파티션 + offset_hours: 1 → 14:15 회차가 hour=13 을 읽는다
15 * * * * uv run /home/ubuntu/works/wai-monitor/s3-alert/s3_mail_alert.py kr-r2o-newlog-live >> /var/log/s3_alert.log
```

## 알림 추가

`pipelines.yaml` 에 항목 하나. 스크립트는 건드리지 않는다.

```yaml
  kr-xxx-error-live:
    bucket: "<버킷>"
    prefix: "alert/error.beat.xxx.live"
    partition_format: "year=%Y/month=%m/day=%d/hour=%H"   # S3 sink 의 path.format 과 같은 단위
    partition_tz: "Asia/Seoul"                            # S3 sink 의 timezone 과 같아야 함
    offset_hours: 1                                       # 직전 파티션을 본다
    subject: "[kr-xxx-live] 에러 레코드 발생"
    message: "kr-xxx-live 에서 처리할 수 없는 레코드가 발생했습니다."
    to: "<수신주소>"
```

실제 값이 담긴 `pipelines.yaml` 은 배포 호스트에만 둔다.

## 테스트

```bash
uv run test_s3_mail_alert.py
```
