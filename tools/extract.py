# -*- coding: utf-8 -*-
"""把報告 PDF 抽成本機核對用的三個檔（全部在 source/，不進 repo）：

  source/pages.txt   逐頁全文（===== PAGE N ===== 分隔，已去掉書眉頁碼）
  source/paras.json  段落座標：[{sec, key, pages, text}]，key 是 ¶ 編號、KF1–KF4、fig1–fig8、fn1
  source/fig/*.png   圖頁 300 DPI 影像，給 ocr_figs.py 讀圖內標示用

  python tools/extract.py "C:/path/to/Employment at Anthropic.pdf"

報告 © 2026 Anthropic PBC。抽出的全文只用來做本機核對，.gitignore 已排除 source/。
需要 poppler 的 pdftotext；圖頁影像用 PyMuPDF（fitz）。
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source"

FOOTER = "How Employment is Changing at Anthropic"

# 報告的章節標題（逐字，用來切段；不是展示用）
HEADINGS = [
    ("S1", "Key Findings:"),
    ("S2", "Introduction"),
    ("S3", "Labor demand at the frontier"),
    ("S4", "Is AI driving productivity increases at Anthropic?"),
    ("S5", "Bottlenecks and process: new and old tasks in an AI-intensive workplace"),
    ("S6", "What employers can do"),
    ("S7", "Suggested Citation"),
]
FIG_PAGES = {1: 4, 2: 6, 3: 7, 4: 8, 5: 10, 6: 12, 7: 13, 8: 14}


def run_pdftotext(pdf, page):
    out = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-enc", "UTF-8", pdf, "-"],
        capture_output=True, check=True).stdout.decode("utf-8")
    out = unicodedata.normalize("NFKC", out.replace("\r\n", "\n").replace("\f", ""))
    lines = [ln.strip() for ln in out.split("\n")]
    # 去書眉與頁碼（每頁最後兩個非空行）
    keep = [ln for ln in lines if ln and ln != FOOTER and ln != str(page)]
    return keep


def page_count(pdf):
    info = subprocess.run(["pdfinfo", pdf], capture_output=True).stdout.decode("latin-1")
    return int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))


def ends_paragraph(s):
    return bool(re.search(r"[.?!:”\"’)]$", s))


def segment(pages):
    """逐頁走訪，依標題切節、依行切段；上一頁最後一段沒有句末標點就和下一頁第一段接起來。"""
    paras, sec, counters = [], "S0", {}
    heading_map = {h: k for k, h in HEADINGS}
    pending = None  # 跨頁未完的段落

    def emit(p):
        if p["sec"] == "S1" and p["text"].startswith("•"):
            counters["KF"] = counters.get("KF", 0) + 1
            p["key"] = "KF%d" % counters["KF"]
            p["text"] = p["text"].lstrip("• ").strip()
        elif p["text"].startswith("Figure ") and re.match(r"Figure (\d):", p["text"]):
            p["key"] = "fig" + re.match(r"Figure (\d):", p["text"]).group(1)
        elif re.match(r"^1 Anthropic estimates", p["text"]):
            p["key"] = "fn1"
        else:
            counters[p["sec"]] = counters.get(p["sec"], 0) + 1
            p["key"] = "¶%d" % counters[p["sec"]]
        paras.append(p)

    for pg in sorted(pages):
        lines = pages[pg]
        if pg == 2 and sec == "S0":
            sec = "S1"          # 第 2 頁開場段落在 Key Findings 標題之前，歸入 §1
        for i, ln in enumerate(lines):
            if sec == "S7":
                # 書末（引用格式、致謝、文獻）：一行一段，不跨頁接續
                if ln not in ("Acknowledgements", "Works cited"):
                    emit(dict(sec=sec, pages=[pg], text=ln))
                continue
            if ln in heading_map:
                if pending:
                    emit(pending)
                    pending = None
                sec = heading_map[ln]
                continue
            if pg == 19 and ln in ("Acknowledgements", "Works cited"):
                if pending:
                    emit(pending)
                    pending = None
                continue
            if pending is not None and i == 0 and not ln.startswith("Figure "):
                pending["text"] += " " + ln
                pending["pages"].append(pg)
                if ends_paragraph(ln):
                    emit(pending)
                    pending = None
                continue
            if pending is not None and ln.startswith("Figure "):
                # 圖說插在跨頁段落中間：圖說自成一段，段落繼續等下一行
                emit(dict(sec=sec, pages=[pg], text=ln))
                continue
            if pending is not None:
                pending["text"] += " " + ln
                if pg not in pending["pages"]:
                    pending["pages"].append(pg)
                if ends_paragraph(ln):
                    emit(pending)
                    pending = None
                continue
            p = dict(sec=sec, pages=[pg], text=ln)
            last_on_page = (i == len(lines) - 1)
            if last_on_page and not ends_paragraph(ln) and pg < max(pages):
                pending = p
            else:
                emit(p)
    if pending:
        emit(pending)
    return paras


def render_fig_pages(pdf):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("沒有 PyMuPDF，略過圖頁影像")
        return
    (SRC / "fig").mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    for n, pg in FIG_PAGES.items():
        pix = doc[pg - 1].get_pixmap(dpi=300)
        pix.save(str(SRC / "fig" / ("fig%d_p%d.png" % (n, pg))))
    print("圖頁影像 %d 張 → source/fig/" % len(FIG_PAGES))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pdf = sys.argv[1]
    n = page_count(pdf)
    pages = {i: run_pdftotext(pdf, i) for i in range(1, n + 1)}
    SRC.mkdir(exist_ok=True)
    chunks = ["===== PAGE %d =====\n%s\n" % (i, "\n".join(pages[i])) for i in range(1, n + 1)]
    (SRC / "pages.txt").write_text("\n".join(chunks), encoding="utf-8", newline="\n")
    paras = segment(pages)
    (SRC / "paras.json").write_text(json.dumps(paras, ensure_ascii=False, indent=1),
                                    encoding="utf-8", newline="\n")
    render_fig_pages(pdf)
    print("寫出 source/pages.txt（%d 頁）、source/paras.json（%d 段）" % (n, len(paras)))


if __name__ == "__main__":
    main()
