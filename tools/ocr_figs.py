# -*- coding: utf-8 -*-
"""圖內標示的 OCR（只在本機跑，結果寫進 source/fig_ocr.json，不進 repo）。

報告的 8 張圖是點陣圖，圖裡印的終點標示（5.1×、424 h、29%…）不在文字層。
這支把 extract.py 產生的 300 DPI 圖頁影像丟給 Tesseract（sparse text 模式），
verify.py 再拿「圖內標示」類的數字去比對這份 OCR 文字。

  python tools/ocr_figs.py

需要 Tesseract（預設 C:\\Program Files\\Tesseract-OCR\\tesseract.exe，可用環境變數 TESSERACT 覆寫）。
讀圖位置估的數值（標「讀圖」）不走 OCR，也不進機械核對。
"""
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "source" / "fig"
OUT = ROOT / "source" / "fig_ocr.json"
TESS = os.environ.get("TESSERACT", r"C:\Program Files\Tesseract-OCR\tesseract.exe")


# 只裁圖框（頁面上緣到圖說之前），避免把同頁內文的數字當成圖內標示
CROP = {1: 0.43, 2: 0.43, 3: 0.49, 4: 0.62, 5: 0.51, 6: 0.47, 7: 0.47, 8: 0.42}


def ocr(png, n):
    from PIL import Image
    img = Image.open(png)
    w, h = img.size
    crop = FIG / ("crop_fig%d.png" % n)
    img.crop((0, 0, w, int(h * CROP[n]))).save(crop)
    res = subprocess.run([TESS, str(crop), "-", "-l", "eng", "--psm", "11"],
                         capture_output=True)
    return res.stdout.decode("utf-8", "replace")


def main():
    out = {}
    for png in sorted(FIG.glob("fig*_p*.png")):
        n = int(re.match(r"fig(\d+)_p", png.name).group(1))
        out["fig%d" % n] = ocr(png, n)
        print("fig%d：%d 字元" % (n, len(out["fig%d" % n])))
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print("寫出", OUT)


if __name__ == "__main__":
    main()
