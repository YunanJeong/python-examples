# s3-alert

S3 특정 경로에 파일이 올라오면 그 내용을 메일로 보내는 크론 스크립트.
알림이 늘어나도 스크립트는 하나이고 `pipelines.yaml` 항목만 추가한다.

```
s3-alert/
├── s3_mail_alert.py        공용 러너
├── pipelines.yaml          설정 전부 (기본값 + 알림별 항목). 크론 한 줄이 이 파일을 담당한다
└── test_s3_mail_alert.py   순수함수 유닛테스트
```

알림 발생 앱들이 클라우드·폐쇄망·온프렘·로컬에 흩어져 있어 직통 경로를 뚫기 어렵다.
S3는 조직 데이터레이크라 이미 전 환경에서 접근되므로 그 길에 얹었다 — **파일 업로드가 곧 알림이다.**

## 실행

```bash
uv run s3_mail_alert.py pipelines.yaml                        # 그 파일의 항목 전부 순회
uv run s3_mail_alert.py pipelines.yaml kr-r2o-live-newlog     # 하나만 (enabled: false 여도 돈다)
```

**설정파일 하나가 크론 한 줄의 담당범위다.** 알림이 수십 개로 늘어도 크론탭은 그대로고
`pipelines.yaml` 항목만 늘어난다. 주기가 다르면 설정파일을 따로 만들어 줄을 하나 더 등록한다.

```sh
# uv 와 설정파일은 절대경로로 부른다
# 매시 15분 + hour 파티션 + offset_hours: 1 → 14:15 회차가 hour=13 을 읽는다
15 * * * * <uv설치경로>/uv run <스크립트경로>/s3_mail_alert.py <설정경로>/pipelines.yaml >> /var/log/s3_alert.log
```

## 알림 추가

`pipelines.yaml` 에 항목 하나. 스크립트는 건드리지 않는다.

```yaml
  kr-xxx-live-error:
    # enabled: false        # 잠깐 재울 때. 항목을 주석처리하면 yaml 이 깨져 전부 멈춘다
    bucket: "<버킷>"
    prefix: "alert/error.beat.xxx.live"
    subject: "[kr-xxx-live] 에러 레코드 발생"
    message: "kr-xxx-live 에서 처리할 수 없는 레코드가 발생했습니다."
    to: "<수신주소>"          # 수신자는 항목마다 따로 적는다
```

발송 설정(SMTP·발신자)과 `enabled`·파티션 형식·타임존·`offset_hours` 는 `defaults:` 에 깔려 있어
다를 때만 항목에 적는다. 항목에 적은 값이 기본값을 덮는다. 코드에 숨은 기본값은 없다.
`partition_format` 의 단위는 그 파일을 부르는 크론 주기와 맞춘다.

경우에 따라 smtp 주소 및 메일주소 등이 보안사항일 수 있음 주의.

## 테스트

```bash
uv run test_s3_mail_alert.py
```
