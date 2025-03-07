import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import date

# password 외에도 SMTP 서버,포트,메일주소 등 모두가 보안사항일 수 있음
# 지메일 등 상용 서비스 메일은 별도 패스워드를 발급받아 보안인증함
# 소규모 SMTP 서버의 경우 인증절차 없이 smtp 서버, 포트로만 하는 경우도 있는데 그럴 땐 서버, 포트 주소 자체가 보안사항
_SMTP_INFO = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port'  : 587,
    'from_name'  : 'my-mail-alert',
    'from_mail'  : 'no-reply@gmail.com',
    'to_mail'    : 'my-mail@gmail.com',
    # 'password'   : "",                                         # 필요시 사용 (로그인) #  from_mail의 비번 # 지메일의 경우 앱 비밀번호 별도 발급
}
def send_mail(subject, body, smtp=_SMTP_INFO):
    """메일 함수"""
    smtp_server = smtp['smtp_server']
    smtp_port   = smtp['smtp_port']
    from_name   = smtp['from_name']
    from_mail   = smtp['from_mail']
    to_mail     = smtp['to_mail']
    # password    = smtp['password']                             # 필요시 사용 (로그인)

    msg = MIMEMultipart()
    msg['From'] = formataddr( (from_name, from_mail) )
    msg['To'] = to_mail
    msg['Subject'] = subject            # 메일 제목
    msg.attach(MIMEText(body, 'plain')) # 메일 내용

    # 메일 전송
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        # server.starttls()                                    # 필요시 사용 (TLS 사용시)
        # server.login(smtp["from_mail"], smtp["password"])    # 필요시 사용 (로그인)
        server.sendmail(from_mail, to_mail, msg.as_string())


def _send_custom_mail(target_date):
    """메일함수 기반으로 커스텀 메일 함수를 정의하는 예시 템플릿
    
    # mail example에서 메일정보를 그대로 할당하는 경우가 많긴한데, 보안사항 및 커스텀 사항 별도 관리를 위해 이렇게 템플릿을 구성해 봄
    # send_mail() 메소드를 다른 모듈에서 호출 후 _send_custom_mail() 처럼 구현하면 될 듯 하다.
    """

    # 커스텀 사항을 모두 모으기 위해 여기 기술
    # 구현방식에 따라 SMTP_INFO는 커스터메일함수 밖으로 빼도 괜찮을 것 같다.
    SMTP_INFO = {
        'smtp_server': os.environ['SMTP_SERVER'],
        'smtp_port'  : os.environ['SMTP_PORT'],
        'from_name'  : 'my-mail-alert',
        'from_mail'  : 'no-reply@github.com',
        'to_mail'    : os.environ['MY_MAIL'],
        # 'password'   : os.environ['SMTP_PASSWORD']
    }

    # 여기에 메일 구성 내용 로직 구현

    subject = f'여기에 메일 제목을 작성 {target_date}'
    body = f"""
    여기에 메일 내용을 작성 {target_date}
    """
    
    # 메일함수 호출
    send_mail(subject, body, SMTP_INFO)


if __name__ == '__main__':
    _send_custom_mail(date.today())