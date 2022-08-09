"""notifier.py."""
import os
import logging
import logging.handlers
import uuid
import pymsteams
from datetime import datetime
from dbextr.util import EDIT_HOME

WEBHOOK_URL = ""

def initialize_logger(log_info):
    """로거 설정.

    Note:
        초기화된 logger를 추후 call 할때는 logging.getLogger({동일한 이름})을 사용한다.

    Args:
        log_info (dic): service, path, bucket(로그 s3 업로드 기능 추가시 사용)

    Returns:
        logger: 로거 객체
    """
    service, path, bucket = log_info.values()
    logger = logging.getLogger("dbextr")

    # 로그 저장할 로컬 디렉토리 생성
    os.makedirs(f'{EDIT_HOME}/{path}', exist_ok=True)

    # 로그포맷
    format = "{"+"DateTime: %(asctime)s, level: %(levelname)s, module: %(module)s, message: %(message)s"+"}"  # NOQA
    formatter = logging.Formatter(format)

    # 콘솔출력 제어
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # 파일생성 제어
    hash = uuid.uuid4().hex[:8]
    date = datetime.now().strftime("%y%m%d_%H%M%S")  # 현시간 대신, targetdate로 해야하나?
    path = f'{EDIT_HOME}/{path}'
    file_handler = logging.FileHandler(f"{path}/{service}-{date}-{hash}.log")
    file_handler.setFormatter(formatter)

    # mail_handler = logging.handlers.SMTPHandler()

    # 로그레벨 제어
    # => logger 설정이 먼저 적용된 후, 그 범위 안에서 handler 설정이 적용됨
    # ex) logger level이 warning이면, handler level이 debug여도 debug로그 출력안됨.
    logger.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.DEBUG)  # INFO
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # MS 팀즈 경고메시지 전송용 핸들러 처리
    alert_handler = AlertHandler(log_info)
    alert_handler.setLevel(logging.WARNING)  # WARNING, ERROR, CRITICAL
    logger.addHandler(alert_handler)

    return logger


class AlertHandler(logging.StreamHandler):
    """커스텀 핸들러."""

    def __init__(self, log_info):
        logging.StreamHandler.__init__(self)
        self.log_info = log_info

    def emit(self, record):
        msg = self.format(record)
        self.alert_to_teams(self.log_info, msg)

    def alert_to_teams(self, log_info, msg):
        """팀즈에 알림보내기.

        Note:
            관리자: MS Teams에서 팀 및 채널 생성 후, "webhook" 커넥터 앱을 해당 채널에 연동해야 한다.
            사용자: 해당 채널에 등록된 멤버는 알림을 받아볼 수 있다.

        Args:
            log_info (dict): 대상 서비스명 등 알림시 필요 내용이 추가될 수 있다.
            msg (str): 보낼 알림 내용. 주로 에러 및 exception 내용이 입력된다.
        """
        # 서비스명 있어어 함 config, log_info, service
        service, path, bucket = log_info.values()
        today = datetime.now()

        conn = pymsteams.connectorcard(WEBHOOK_URL)
        conn.title(f'DBEXTR ALERT: {service}-{today}')
        conn.text(msg)
        conn.send()
