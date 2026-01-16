# crontab에서는 ~/.bashrc에서 정의한 환경변수가 적용되지 않음
# crontab에 직접 기입하거나, 아래와같이 별도 파일로 작성 후 crontab에서 호출하여 사용

export SMTP_SERVER=my-stmp.server.com
export SMTP_PORT=252525

export CC_MAIL="member1@github.com,member2@github.com"
export MY_MAIL="my-mail@github.com"
export TEAM_MAIL="my-team@github.com"
