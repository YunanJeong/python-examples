import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import date

# password 외에도 SMTP 서버,포트,메일주소 등 모두가 보안사항일 수 있음
# 지메일 등 상용 서비스 메일은 별도 패스워드를 발급받아 보안인증함
# 소규모 SMTP 서버에선 별도 인증없이 주소/포트로만 접근하기도 하는데, 그럴 땐 주소/포트가 보안사항
class SmtpMailer:
    """SMTP 메일 전송 클래스
    
    - 재사용 가능한 메일전송 공통로직만 제공
    - 발신/수신자,제목,본문 등은 호출부에서 커스텀(하드코딩 방지, 보안관리)
    """
    def __init__(self, host, port, from_name, from_addr, to_addrs, cc_addrs=None, password=None):
        self.host = host
        self.port = int(port)
        self.from_name = from_name
        self.from_addr = from_addr
        self.to_addrs = to_addrs      # e.g. "a@x.com,b@y.com" 콤마로 구분되는 단일 문자열
        self.cc_addrs = cc_addrs      # e.g. "a@x.com,b@y.com" 콤마로 구분되는 단일 문자열
        self.password = password      # 필요시 사용 (로그인) #  from_mail의 비번 # 지메일의 경우 앱 비밀번호 별도 발급

    def send(self, subject, body):
        """메일 함수"""
        msg = MIMEMultipart()

        # 발신인 표기
        msg["From"] = formataddr((self.from_name, self.from_addr))
        
        # 수신인 표기 (문자열)
        msg["To"]   = self.to_addrs

        # "실제" 수신인 (리스트)
        receiver_list = self.to_addrs.split(",")

        # 참조 추가
        if self.cc_addrs:
            msg["Cc"] = self.cc_addrs
            receiver_list = receiver_list + self.cc_addrs.split(",")
        
        # 실제 수신인 중복 제거
        receiver_list = list(set(receiver_list))

        # 메일 제목
        msg["Subject"] = subject
        
        # 메일 내용
        msg.attach(MIMEText(body, "plain", "utf-8")) 

        with smtplib.SMTP(self.host, self.port) as server:
            server.ehlo()
            # server.starttls()                              # 필요시 사용 (TLS 사용시)
            # server.login(self.from_addr, self.password)    # 필요시 사용 (로그인)
            server.sendmail(self.from_addr, receiver_list, msg.as_string())


def _send_custom_mail(target_date):
    """SmtpMailer 기반으로 커스텀 메일을 작성하는 예시(bussiness logic sample)"""

    smtp = SmtpMailer(
        host      = os.environ['SMTP_SERVER'],
        port      = os.environ['SMTP_PORT'],
        from_name = 'my-mail-alert',
        from_addr = 'no-reply@github.com',
        to_addrs  = os.environ['MY_MAIL'],
        cc_addrs  = os.environ['CC_MAIL'],
        # 'password'   : os.environ['SMTP_PASSWORD']
    )

    # 여기에 메일 구성 내용 로직 구현

    subject = f'여기에 메일 제목을 작성 {target_date}'
    body = f"""
    여기에 메일 내용을 작성 {target_date}
    """
    
    # 메일함수 호출
    smtp.send(subject, body)


if __name__ == '__main__':
    _send_custom_mail(date.today())