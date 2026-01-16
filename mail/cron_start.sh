# 크론 실행용 명령어
# alert 스크립트는 주기적 상태체크 후 실패조건 달성시 메일을 전송하는 방법이 가능함 


# mail_env.sh를 통해 별도 정의돤 메일정보 등 환경변수들을 불러옴
# 이 때 dot(.)을 쓰는데, source와 동일한 기능임(개별 세션이 아닌, 현재 세션(쉘)에 명령어를 적용하는 기능)
# 크론탭에서는 source가 없을 수 있으므로 POSIX 표준인 dot(.)을 써야 함

. /home/ubuntu/.crontab/mail_env.sh && /usr/bin/python /home/ubuntu/.crontab/mail.py >> /home/ubuntu/.crontab/$(/usr/bin/date +\%Y\%m)_crontab_daily.log 2>&1

# 크론 자체가 비정상동작할 수 있으므로 redirection 통해서 간단하게 로깅 파일도 만들어준다.