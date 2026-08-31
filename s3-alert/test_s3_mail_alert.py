# /// script
# requires-python = ">=3.11"
# dependencies = ["boto3", "pyyaml", "pytest"]
# ///
#
# 순수함수 로직 테스트. 실제 S3·SMTP 는 건드리지 않는다.
# 실행: uv run test_s3_mail_alert.py

import gzip
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent))
import s3_mail_alert as m

HOURLY = "year=%Y/month=%m/day=%d/hour=%H"
KST = ZoneInfo("Asia/Seoul")


# ---- 파티션 경로 ------------------------------------------------------

def test_직전_시간_파티션을_가리킨다():
    at = m.target_time(1, "Asia/Seoul", datetime(2026, 8, 31, 14, 15, tzinfo=KST))
    assert m.target_prefix("alert/newlog", HOURLY, at) == \
        "alert/newlog/year=2026/month=08/day=31/hour=13/"


def test_날짜_경계에서_전날_파티션으로_넘어간다():
    at = m.target_time(1, "Asia/Seoul", datetime(2026, 9, 1, 0, 15, tzinfo=KST))
    assert m.target_prefix("alert/newlog", HOURLY, at) == \
        "alert/newlog/year=2026/month=08/day=31/hour=23/"


def test_커넥터_타임존_기준으로_경로가_갈린다():
    # 같은 순간이라도 파티션 타임존이 다르면 봐야 할 경로가 다르다
    now = datetime(2026, 8, 31, 2, 30, tzinfo=timezone.utc)   # KST 11:30

    kst = m.target_time(1, "Asia/Seoul", now)
    utc = m.target_time(1, "UTC", now)

    assert m.target_prefix("alert/newlog", HOURLY, kst) == "alert/newlog/year=2026/month=08/day=31/hour=10/"
    assert m.target_prefix("alert/newlog", HOURLY, utc) == "alert/newlog/year=2026/month=08/day=31/hour=01/"


def test_offset_hours로_더_앞의_파티션을_볼_수_있다():
    at = m.target_time(3, "Asia/Seoul", datetime(2026, 8, 31, 14, 15, tzinfo=KST))
    assert m.target_prefix("alert/newlog", HOURLY, at) == \
        "alert/newlog/year=2026/month=08/day=31/hour=11/"


def test_기준_프리픽스의_슬래시는_중복되지_않는다():
    at = m.target_time(1, "Asia/Seoul", datetime(2026, 8, 31, 14, 15, tzinfo=KST))
    assert m.target_prefix("alert/newlog/", HOURLY, at) == \
        "alert/newlog/year=2026/month=08/day=31/hour=13/"


def test_일단위_파티션이면_경로도_일단위로_나온다():
    at = m.target_time(1, "Asia/Seoul", datetime(2026, 8, 31, 14, 15, tzinfo=KST))
    assert m.target_prefix("alert/newlog", "year=%Y/month=%m/day=%d", at) == \
        "alert/newlog/year=2026/month=08/day=31/"


# ---- 읽기 (zcat 상당) -------------------------------------------------

def test_gzip이면_풀어서_읽는다():
    assert m.decode(gzip.compress("한글 줄\n".encode("utf-8"))) == "한글 줄\n"


def test_압축이_아니면_그대로_읽는다():
    assert m.decode("한글 줄\n".encode("utf-8")) == "한글 줄\n"


class FakeS3:
    """list_objects_v2 + get_object 만 흉내내는 대역. GET 횟수를 센다."""
    def __init__(self, objects):
        self.objects = objects   # {key: bytes}
        self.gets = 0

    def get_paginator(self, name):
        assert name == "list_objects_v2"
        return self

    def paginate(self, **kwargs):
        return [{"Contents": [{"Key": key} for key in self.objects]}]

    def get_object(self, Bucket, Key):
        self.gets += 1
        return {"Body": _Body(self.objects[Key])}


class _Body:
    def __init__(self, raw):
        self.raw = raw

    def read(self):
        return self.raw


def test_프리픽스의_모든_객체를_읽는다():
    s3 = FakeS3({
        "p/a.json": b'{"log_type": "A"}\n',
        "p/b.json.gz": gzip.compress(b'{"log_type": "B"}\n'),
    })
    keys = m.list_keys(s3, "bucket", "p/")
    assert m.read_objects(s3, "bucket", keys) == ['{"log_type": "A"}\n', '{"log_type": "B"}\n']


def test_디렉터리_표시용_키는_목록에서_빠진다():
    s3 = FakeS3({"p/": b"", "p/a.json": b"line\n"})
    assert m.list_keys(s3, "bucket", "p/") == ["p/a.json"]


def test_파일이_없으면_다운로드하지_않는다():
    # 목록조회가 트리거다. 빈 회차에는 GET 이 한 번도 나가지 않아야 한다
    s3 = FakeS3({})
    keys = m.list_keys(s3, "bucket", "p/")

    assert keys == []
    assert m.read_objects(s3, "bucket", keys) == []
    assert s3.gets == 0


def test_읽은_객체_수만큼만_다운로드한다():
    s3 = FakeS3({"p/": b"", "p/a.json": b"line\n", "p/b.json": b"line2\n"})
    m.read_objects(s3, "bucket", m.list_keys(s3, "bucket", "p/"))
    assert s3.gets == 2


# ---- sort -u ---------------------------------------------------------

def test_합본을_정렬하고_같은_줄은_한_번만_남긴다():
    texts = ["B\nA\n", "A\nC\n"]
    assert m.sort_unique(texts) == ["A", "B", "C"]


def test_빈_줄은_버린다():
    assert m.sort_unique(["A\n\n   \nB\n"]) == ["A", "B"]


def test_파일_경계에서_줄이_붙지_않는다():
    # 마지막 개행이 없는 파일이 있어도 다음 파일 첫 줄과 이어지지 않아야 한다
    assert m.sort_unique(["A", "B"]) == ["A", "B"]


def test_읽을_내용이_없으면_빈_목록이다():
    assert m.sort_unique([]) == []


# ---- 본문 ------------------------------------------------------------

def test_확인_명령은_프리픽스_전체를_로컬로_받는_한_줄이다():
    at = datetime(2026, 8, 31, 13, 0, tzinfo=KST)
    assert m.download_command("mybucket", "alert/newlog/hour=13/", "kr-r2o-newlog-live", at) == \
        "aws s3 cp --recursive s3://mybucket/alert/newlog/hour=13/ ./kr-r2o-newlog-live-20260831-1300/"


def test_본문에_현상_건수_내용_확인명령이_담긴다():
    at = datetime(2026, 8, 31, 13, 0, tzinfo=KST)
    body = m.build_body("kr-r2o-live 에서 신규 로그타입이 감지되었습니다.",
                        at, "Asia/Seoul", 2, ["첫줄", "둘째줄"], "aws s3 cp ...")

    assert "kr-r2o-live 에서 신규 로그타입이 감지되었습니다." in body
    assert "2026-08-31 13시 (Asia/Seoul)" in body
    assert "2건 / sort -u 후 2줄" in body
    assert "첫줄" in body and "둘째줄" in body
    assert "aws s3 cp ..." in body


# ---- 설정 -------------------------------------------------------------

def test_발송_설정이_한_군데_모여있다():
    smtp = yaml.safe_load(m.CONFIG_PATH.read_text(encoding="utf-8"))["smtp"]
    assert set(smtp) == {"server", "port", "from_name", "from_addr"}


def test_모든_파이프라인이_필수_항목을_갖고_있다():
    pipelines = yaml.safe_load(m.CONFIG_PATH.read_text(encoding="utf-8"))["pipelines"]
    assert pipelines

    for name, conf in pipelines.items():
        for key in ("bucket", "prefix", "partition_format", "partition_tz", "subject", "message", "to"):
            assert key in conf, f"{name} 에 {key} 가 없다"


def test_설정에_모르는_항목이_없다():
    allowed = {"bucket", "prefix", "partition_format", "partition_tz",
               "offset_hours", "subject", "message", "to", "cc"}
    pipelines = yaml.safe_load(m.CONFIG_PATH.read_text(encoding="utf-8"))["pipelines"]

    for name, conf in pipelines.items():
        assert set(conf) <= allowed, f"{name} 에 모르는 항목: {set(conf) - allowed}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
