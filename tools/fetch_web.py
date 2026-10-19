# -*- coding: utf-8 -*-
"""抓官方網頁版的純文字到 source/web.txt（本機核對用，不進 repo）。

站上每條主張的「原文定位」連結用的是 Text Fragment（#:~:text=…），
verify.py 會檢查每個定位片語都真的出現在網頁版文字裡——網頁版與 PDF 有少量排版差異
（例如重點發現寫 "six to one"、PDF 寫 "6 to 1"），所以兩邊都要比。

  python tools/fetch_web.py
"""
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://www.anthropic.com/research/employment-at-anthropic"
OUT = ROOT / "source" / "web.txt"


def main():
    raw = subprocess.run(["curl", "-s", "-L", "-A", "Mozilla/5.0", URL],
                         capture_output=True, check=True).stdout.decode("utf-8")
    raw = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    txt = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    txt = re.sub(r"\s+", " ", txt).strip()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(txt, encoding="utf-8", newline="\n")
    print("寫出 %s（%d 字元）" % (OUT, len(txt)))


if __name__ == "__main__":
    main()
