# /// script
# requires-python = ">=3.11"
# dependencies = ["boto3", "pyyaml"]
# ///
#
# S3 알림 파일 메일 발송 (알림 파이프라인 공용 러너)
#
# 대상 프리픽스에 파일이 "존재하면" 그 파일들을 읽어 합본을 sort -u 해서 메일 본문에 싣는다.
# 세부 파싱은 하지 않는다. 줄 단위 중복만 접고 나머지는 올라온 그대로 보낸다.
# 상태를 기억하지 않고, S3에 쓰지도 지우지도 않는다.
#
# 크론 등록 예시 (crontab -e). 파티션 단위와 크론 주기를 1:1로 맞춘다.
#
#   # uv 는 절대경로로 부른다
#   # 매시 15분 + hour 파티션 + offset_hours: 1 -> 14:15 회차가 hour=13 을 읽는다
#   15 * * * * <uv설치경로>/uv run <스크립트경로>/s3_mail_alert.py kr-r2o-newlog-live >> /var/log/s3_alert.log

import gzip
import os
import smtplib
import sys
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path
from zoneinfo import ZoneInfo

import boto3
import yaml

CONFIG_PATH = Path(os.environ.get("S3_ALERT_CONFIG", Path(__file__).with_name("pipelines.yaml")))


# 소규모 SMTP 서버의 경우 인증절차 없이 smtp 서버, 포트로만 하는 경우도 있는데 그럴 땐 서버, 포트 주소 자체가 보안사항
class SmtpMailer:
    """ 일반적으로 가져와서 사용할 수 있도록 SMTP 메일 보내기 기능 구현"""
    def __init__(self, host, port, from_name, from_addr, to_addrs, cc_addrs=None, password=None):
        self.host = host
        self.port = int(port)
        self.from_name = from_name
        self.from_addr = from_addr
        self.to_addrs = to_addrs      # e.g. "a@x.com,b@y.com" 콤마로 구분되는 단일 문자열
        self.cc_addrs = cc_addrs      # e.g. "a@x.com,b@y.com" 콤마로 구분되는 단일 문자열
        self.password = password      # 필요시 사용 (로그인)

    def send(self, subject, body):
        """메일 함수"""
        msg = MIMEMultipart()
        msg["From"] = formataddr((self.from_name, self.from_addr))
        msg["To"] = self.to_addrs

        receiver_list = self.to_addrs.split(",")
        if self.cc_addrs:
            msg["Cc"] = self.cc_addrs
            receiver_list = receiver_list + self.cc_addrs.split(",")
        receiver_list = list(set(receiver_list))

        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(self.host, self.port) as server:
            server.ehlo()
            # server.starttls()                              # 필요시 사용 (TLS 사용시)
            # server.login(self.from_addr, self.password)     # 필요시 사용 (로그인)
            server.sendmail(self.from_addr, receiver_list, msg.as_string())


def target_time(offset_hours, tz_name, now=None):
    """이번 회차가 볼 시각. 파티션 경로를 만드는 기준이다.

    tz_name 은 S3 sink connector 의 timezone 설정과 같아야 한다.
    커넥터가 UTC로 경로를 쓰는데 여기서 KST로 계산하면 9시간 어긋난 경로를 본다.
    """
    at = now or datetime.now(timezone.utc)
    return at.astimezone(ZoneInfo(tz_name)) - timedelta(hours=offset_hours)


def target_prefix(prefix, partition_format, at):
    """읽을 프리픽스. 이 경로가 곧 '이번 회차 대상'의 정의라서 스크립트가 기억할 상태가 없다."""
    return f"{prefix.rstrip('/')}/{at.strftime(partition_format)}/"


def decode(raw):
    """gzip 이면 풀고, 아니면 그대로 읽는다 (zcat 과 같은 동작).

    커넥터의 압축 설정에 상관없이 동작하도록 키 확장자가 아니라 매직바이트로 판별한다.
    """
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8")


def list_keys(s3, bucket, prefix):
    """목록조회가 트리거다. 여기가 비면 GET 을 한 번도 하지 않고 끝난다.

    알림 주기가 짧아져도 빈 회차의 비용은 목록조회 한 번뿐이다.
    """
    keys = []

    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            # 콘솔에서 만든 디렉터리 표시용 0바이트 키는 제외한다
            if obj["Key"].endswith("/"):
                continue
            keys.append(obj["Key"])

    return keys


def read_objects(s3, bucket, keys):
    """파일이 있다고 확인된 다음에만 불린다.

    로컬에 파일을 만들지 않는다. 받아서 풀고 합치는 걸 전부 메모리에서 하므로 치울 것이 없다.
    알림 볼륨이 극소라 가능한 방식이다.
    """
    return [decode(s3.get_object(Bucket=bucket, Key=key)["Body"].read()) for key in keys]


def sort_unique(texts):
    """합본을 sort -u 한다. 줄 단위 중복만 접고 세부 파싱은 하지 않는다."""
    return sorted({line for line in "\n".join(texts).splitlines() if line.strip()})


def build_body(message, at, tz_name, files, lines, command):
    return (
        f"{message}\n"
        f"\n"
        f"대상 시간대: {at:%Y-%m-%d %H}시 ({tz_name})\n"
        f"알림 파일: {files}건 / sort -u 후 {len(lines)}줄\n"
        f"\n"
        f"## 내용\n"
        f"\n"
        + "\n".join(lines)
        + f"\n\n"
        f"원본 그대로 받아보려면:\n"
        f"  {command}\n"
        f"\n"
        f"Powered by crontab / uv\n"
    )


def download_command(bucket, prefix, name, at):
    """복붙해서 바로 되는 한 줄이어야 값어치가 있다"""
    return f"aws s3 cp --recursive s3://{bucket}/{prefix} ./{name}-{at:%Y%m%d-%H%M}/"


def main():
    if len(sys.argv) != 2:
        sys.exit(f"usage: {Path(sys.argv[0]).name} <파이프라인명>   ({CONFIG_PATH} 의 pipelines 키)")

    name = sys.argv[1]
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    pipelines = config["pipelines"]
    if name not in pipelines:
        sys.exit(f"'{name}' 은 {CONFIG_PATH} 에 없다. 사용 가능: {', '.join(sorted(pipelines))}")

    smtp = config["smtp"]
    conf = pipelines[name]
    bucket = conf["bucket"]
    tz_name = conf["partition_tz"]

    at = target_time(conf.get("offset_hours", 1), tz_name)
    prefix = target_prefix(conf["prefix"], conf["partition_format"], at)

    s3 = boto3.client("s3")
    keys = list_keys(s3, bucket, prefix)
    if not keys:
        print(f"s3_mail_alert.py {name} nothing at s3://{bucket}/{prefix}")
        return

    lines = sort_unique(read_objects(s3, bucket, keys))

    SmtpMailer(
        host      = smtp["server"],
        port      = smtp["port"],
        from_name = smtp["from_name"],
        from_addr = smtp["from_addr"],
        to_addrs  = conf["to"],
        cc_addrs  = conf.get("cc"),
    ).send(
        f"{conf['subject']} ({len(lines)}건)",
        build_body(conf["message"], at, tz_name, len(keys), lines,
                   download_command(bucket, prefix, name, at)),
    )

    print(f"s3_mail_alert.py {name} sent files={len(keys)} lines={len(lines)} prefix=s3://{bucket}/{prefix}")


if __name__ == "__main__":
    main()
