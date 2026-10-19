# -*- coding: utf-8 -*-
"""把資料層組裝成單檔 index.html，並輸出同內容的 report.md。

  python tools/build.py

需要本機的 source/（tools/extract.py、fetch_web.py、ocr_figs.py 產生，不進 repo）。
不要接管線——verify 的 assert 失敗時 exit code 會被吃掉。
"""
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import data_meta as dm      # noqa: E402
import data_claims as dc    # noqa: E402
import data_figs as df      # noqa: E402
import data_checks as dk    # noqa: E402
import data_lit as dl       # noqa: E402
import data_law as dw       # noqa: E402
import data_report as dr    # noqa: E402
import verify               # noqa: E402


def payload():
    return dict(
        meta=dm.META, sections=dm.SECTIONS, sources=dm.SOURCES, types=dm.TYPES, grades=dm.GRADES,
        grade_note=dm.GRADE_NOTE,
        claims=dc.CLAIMS, figs=df.FIGS, calcs=dk.CALCS, gaps=dk.GAPS, lit=dl.LIT, law=dw.LAW,
        report=dr.REPORT, verdicts=dr.VERDICTS, chain=dr.CHAIN, policy=dr.POLICY, glossary=dr.GLOSSARY,
    )


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from strings(v)


def fill(o, stats):
    if isinstance(o, str):
        return re.sub(r"\{\{(\w+)\}\}", lambda m: str(stats[m.group(1)]), o)
    if isinstance(o, dict):
        return {k: fill(v, stats) for k, v in o.items()}
    if isinstance(o, list):
        return [fill(v, stats) for v in o]
    return o


# ------------------------------------------------------------------ Markdown 版
REFNAME = {}


def md_inline(s):
    """[[P9]] [[P12]] 這類相鄰引用合併成（P9、P12）；文獻與法條換成短名。"""
    def grp(m):
        refs = re.findall(r"\[\[([^\]]+)\]\]", m.group(0))
        return "（" + "、".join(REFNAME.get(r, r) for r in refs) + "）"
    return re.sub(r"\s*(?:\[\[[^\]]+\]\]\s*)+", grp, s)


def to_markdown(D):
    m, out = D["meta"], []
    REFNAME.update({"lit:" + l["id"]: l["short"] for l in D["lit"]})
    REFNAME.update({"law:" + l["id"]: l.get("chip") or l["short"] for l in D["law"]})
    out.append("# 《%s》逐項拆解\n" % m["title_en"])
    out.append("%s。%s，%s。PDF %d 頁、%d 張圖。原文：%s\n" % (
        "、".join(m["authors"]), m["institution"], m["date"], m["pages"], m["figures"], m["url_web"]))
    out.append("> " + m["disclaimer"] + "\n")
    out.append("> " + m["coi"] + "\n")
    for sec in D["report"]:
        out.append("\n## %s\n" % sec["title"])
        for b in sec["blocks"]:
            t = b["t"]
            if t == "p":
                out.append(md_inline(b["x"]) + "\n")
            elif t == "h3":
                out.append("### " + b["x"] + "\n")
            elif t == "ul":
                out.extend("- " + md_inline(x) for x in b["items"])
                out.append("")
            elif t == "callout":
                out.append("> " + md_inline(b["x"]) + "\n")
            elif t == "coi":
                out.append("> " + m["coi"] + "\n")
            elif t == "verdicts":
                for v in D["verdicts"]:
                    out.append("**%s：%s**（等級 %s）——%s。%s\n" % (v["kf"], v["head"], v["grade"], v["verdict"], md_inline(v["body"])))
            elif t == "chain":
                for e in D["chain"]["edges"]:
                    na = next(n for n in D["chain"]["nodes"] if n["id"] == e["a"])
                    nb = next(n for n in D["chain"]["nodes"] if n["id"] == e["b"])
                    out.append("- %s → %s：%s（%s）" % (na["t"], nb["t"], e["t"], "衝突" if e.get("conflict") else e["g"]))
                out.append("")
            elif t == "policy":
                out.append("| 建議 | 報告的理由 | 證據 | 評析 | 美國法下的位置 |\n|---|---|---|---|---|")
                for r in D["policy"]:
                    out.append("| %s | %s | %s | %s | %s |" % tuple(md_inline(r[k]) for k in ("item", "why", "evidence", "assess", "law")))
                out.append("")
            elif t == "lawcards":
                for l in D["law"]:
                    out.append("**%s（%s）** %s" % (l["name"], l["juris"], l["url"]))
                    out.append("> " + l["text"] + "\n")
                    if l["zh"]:
                        out.append(l["zh"] + "\n")
                    out.append("對應：" + l["note"] + "\n")
            elif t == "stats":
                s = D["stats"]
                out.append("主張 %d 則（A %d、B %d、C %d、D %d、方法或限制聲明 %d）；數字核算 %d 項；揭露缺口 %d 項；報告數字機械核對 %d 個。\n" % (
                    s["claims"], s["gA"], s["gB"], s["gC"], s["gD"], s["gX"], s["calcs"], s["gaps"], s["nums"]))
    out.append("\n## 附錄 A　主張帳本\n")
    out.append("| ID | 座標 | 類型 | 等級 | 報告說了什麼（轉述） | 評析 |\n|---|---|---|---|---|---|")
    tname = {t["k"]: t["zh"] for t in D["types"]}
    for c in D["claims"]:
        coord = "§%s%s p.%s" % (c["sec"][1:], c["key"] if c["key"].startswith("¶") else "·" + c["key"], "–".join(map(str, c["p"])))
        out.append("| %s | %s | %s | %s | %s | %s |" % (c["id"], coord, tname[c["type"]], c["grade"], md_inline(c["zh"]).replace("|", "／"),
                                                    md_inline(c["note"]).replace("|", "／")))
    out.append("\n## 附錄 B　數字核算\n")
    for n in D["calcs"]:
        out.append("**%s %s**\n" % (n["id"], n["title"]))
        out.append("- 輸入：" + md_inline(n["inputs"]))
        out.append("- 公式：" + n["formula"])
        out.append("- 結果：" + n["result"])
        out.append("- 讀法：" + n["reading"])
        if n["caveat"]:
            out.append("- 注意：" + n["caveat"])
        out.append("")
    out.append("\n## 附錄 C　報告沒說的事\n")
    for g in D["gaps"]:
        out.append("**%s（%s）%s**　%s　%s\n" % (g["id"], g["sev"], g["title"], g["body"], g["why"]))
    out.append("\n## 附錄 D　文獻核對\n")
    for l in D["lit"]:
        out.append("**%s**，〈%s〉，%s。%s\n- 核對：%s\n- 內容：%s\n- 報告的用法：%s\n" % (
            l["cite"], l["title"], l["venue"], l["url"], l["checked"], l["facts"], l["fidelity"]))
    out.append("\n## 附錄 E　八張圖\n")
    for f in D["figs"]:
        out.append("**圖 %d　%s**（p.%d）\n%s" % (f["n"], f["zh"], f["p"], f["what"]))
        for x in f["shows"]:
            out.append("- 撐得起：" + x)
        for x in f["limits"]:
            out.append("- 撐不起：" + x)
        out.append("")
    out.append("\n---\n" + m["rights_note"] + "\n\n" + m["copyright"] + "（原報告）。建置 " + D["stats"]["built"] + "。\n")
    return "\n".join(out)


def main():
    D = payload()
    v = verify.run(D)

    g = Counter(c["grade"] for c in D["claims"])
    stats = dict(
        claims=len(D["claims"]), calcs=len(D["calcs"]), gaps=len(D["gaps"]),
        gaps_high=sum(1 for x in D["gaps"] if x["sev"] == "高"), figs=len(D["figs"]), lit=len(D["lit"]), law=len(D["law"]),
        self=sum(1 for c in D["claims"] if c.get("self")),
        gA=g["A"], gB=g["B"], gC=g["C"], gD=g["D"], gX=g["-"],
        nums=v["nums"], figlabels=v["figlabels"], anchors=v["anchors"], web=v["web"], read=v["read"],
        built=date.today().isoformat(),
    )
    D = fill(D, stats)
    D["stats"] = stats

    # 著作權機械檢查：站上任何字串與報告全文連續 8 個英文字相同者，只能是白名單
    allow = [D["meta"]["title_en"], D["meta"]["epigraph"]["q"]] + [s["en"] for s in D["sections"]] + \
            [f["title_en"] for f in D["figs"]] + [f.get("title_img", "") for f in D["figs"]] + [l["title"] for l in D["lit"]] +             [l["venue"] for l in D["lit"]] + [" ".join(D["meta"]["authors"]), "、".join(D["meta"]["authors"])]
    hits = verify.ngram_check(list(strings(D)), allow)
    if hits:
        print("著作權檢查失敗：下列 8 字序列與報告原文相同", file=sys.stderr)
        for h in hits:
            print("  -", h, file=sys.stderr)
        raise AssertionError("連續 8 字相同 %d 處" % len(hits))
    print("著作權檢查通過：除白名單外，站上沒有與報告原文連續 8 個英文字相同的字串")

    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    app = (HERE / "app.js").read_text(encoding="utf-8")
    blob = json.dumps(D, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = tpl.replace("/*__DATA__*/", "window.DATA=" + blob + ";").replace("/*__APP__*/", app)
    (ROOT / "index.html").write_text(html, encoding="utf-8", newline="\n")
    (ROOT / "report.md").write_text(to_markdown(D), encoding="utf-8", newline="\n")
    print("index.html %.0f KB、report.md %.0f KB" % ((ROOT / "index.html").stat().st_size / 1024,
                                                   (ROOT / "report.md").stat().st_size / 1024))
    print("主張 %(claims)d（A %(gA)d／B %(gB)d／C %(gC)d／D %(gD)d／聲明 %(gX)d）、自承 %(self)d、核算 %(calcs)d、缺口 %(gaps)d（高 %(gaps_high)d）、"
          "文獻 %(lit)d、法條 %(law)d" % stats)


if __name__ == "__main__":
    main()
