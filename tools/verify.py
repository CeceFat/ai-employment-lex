# -*- coding: utf-8 -*-
"""建置前的核對。任何一項不通過就 raise，build.py 不產出網頁。

1. 座標：每則主張的段落（sec, key）存在於 source/paras.json，頁次落在該段的頁次內。
2. 數字：nums 裡的每個字串都出現在所標段落（數字前後不能黏著別的數字）。
3. 關鍵詞：anchors 出現在所標段落；web（原文定位片語）同時出現在所標段落與官方網頁版文字。
4. 圖內標示：fig 裡的標示出現在該圖圖框的 OCR 文字。
5. lint：每段中文裡出現的數字，都必須在本筆資料宣告過（報告原文、圖內標示、讀圖、自算、外部文獻），
   或屬於日期、條號、座標等例外——防止寫了數字卻沒有來處。
6. 交叉引用：[[L5]]、refs、maps 指到的東西都存在。
7. 逐字引文：全站唯一一句，必須逐字出現在所標段落，且少於 15 個英文字。

需要 source/ 下的 pages.txt、paras.json、web.txt、fig_ocr.json（tools/extract.py、fetch_web.py、ocr_figs.py 產生，不進 repo）。
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source"


def norm(s):
    s = unicodedata.normalize("NFKC", str(s))
    for a, b in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), (" ", " "), ("−", "-")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def load():
    need = ["paras.json", "web.txt", "fig_ocr.json"]
    for n in need:
        if not (SRC / n).exists():
            raise SystemExit("缺 source/%s——先跑 tools/extract.py、fetch_web.py、ocr_figs.py" % n)
    paras = json.loads((SRC / "paras.json").read_text(encoding="utf-8"))
    idx = {}
    for p in paras:
        idx[(p["sec"], p["key"])] = dict(p, n=norm(p["text"]))
    web = norm((SRC / "web.txt").read_text(encoding="utf-8"))
    ocr = {k: norm(v) for k, v in json.loads((SRC / "fig_ocr.json").read_text(encoding="utf-8")).items()}
    return idx, web, ocr


IDX, WEB, OCR = load()
WEB_L = WEB.lower()


def num_in(value, text):
    """value 必須出現在 text，且前後不黏著數字或小數點（避免 14% 被 214% 矇混）。"""
    v = re.escape(norm(value))
    return re.search(r"(?<![\d.,])" + v + r"(?![\d])", text) is not None


def para(loc, errors, label):
    sec, key = loc.split(":", 1)
    p = IDX.get((sec, key))
    if p is None:
        errors.append("%s：段落 %s 不存在" % (label, loc))
    return p


def check_nums(item, own, errors, label):
    n = 0
    for x in item.get("nums", []):
        if isinstance(x, (list, tuple)):
            val, loc = x
            p = para(loc, errors, label)
        else:
            val, p = x, own
        if p is None:
            continue
        if num_in(val, p["n"]):
            n += 1
        else:
            errors.append("%s：%s 段找不到「%s」" % (label, p["sec"] + p["key"], val))
    return n


def fig_label_re(label):
    lab = norm(label)
    m = re.match(r"^([\d.,]+)\s*(%|×|x|h)?$", lab)
    if not m:
        return re.compile(re.escape(lab), re.I)
    num, unit = m.group(1), m.group(2)
    tail = {"%": r"\s*%", "×": r"\s*[x×*]?", "x": r"\s*[x×*]?", "h": r"\s*h"}.get(unit, "")
    return re.compile(r"(?<![\d.])" + re.escape(num) + tail + (r"(?![\d])" if not unit else ""), re.I)


def check_fig_labels(item, errors, label):
    n = 0
    for lab, fid in item.get("fig", []) + [[pp[0], item["id"]] for pp in item.get("printed", [])]:
        text = OCR.get(fid)
        if text is None:
            errors.append("%s：沒有 %s 的 OCR" % (label, fid))
            continue
        if fig_label_re(lab).search(text):
            n += 1
        else:
            errors.append("%s：%s 的圖框 OCR 找不到「%s」" % (label, fid, lab))
    return n


# ------------------------------------------------------------------ lint
EXEMPT = [
    r"\{\{\w+\}\}",                                   # 統計值佔位
    r"\[\[[^\]]+\]\]",                                # 交叉引用
    r"§\s?\d+(?:[.\-–]\d+)*(?:\([a-z0-9]+\))*",      # 條號、章節
    r"¶\s?\d+(?:[–-]¶?\d+)?", r"p\.\s?\d+(?:[–-]\d+)?", r"pp\.\s?\d+(?:[–-]\d+)?",
    r"圖\s?\d+", r"註\s?\d+", r"附件\s?[IVX]+",
    r"第\s?\d[\d,]*(?:\.\d+)?(?:\s?[條款項點號年度])?", r"之\s?\d+", r"\d+\s?年度",
    r"(?:19|20)\d{2}(?:\s?年代)?",                     # 年份
    r"\d{1,2}\s?月", r"\d{1,2}\s?日",
    r"10-K", r"S-1", r"Q[1-4]",
    r"\b[A-Za-z]{1,6}\d+[a-z]?\b",                   # L5、N12、fig3、w35275 之類代號
    r"tit\.\s?\d+", r"\bU\.S\.C\.", r"\d+\s?U\.S\.C\.", r"Local Law \d+",
    r"MD5", r"#page=\d+",
]
EXEMPT_RE = re.compile("|".join("(?:%s)" % e for e in EXEMPT))
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def bare(s):
    out = set()
    for m in NUM_RE.findall(norm(s)):
        out.add(m.replace(",", ""))
    return out


def lint(text, allowed, errors, label):
    t = EXEMPT_RE.sub(" ", norm(text))
    for m in NUM_RE.findall(t):
        v = m.replace(",", "")
        if v in ("0",) or v in allowed:
            continue
        errors.append("lint %s：數字「%s」沒有宣告來處" % (label, m))


def declared(item, lit_nums):
    a = set()
    for x in item.get("nums", []):
        a |= bare(x[0] if isinstance(x, (list, tuple)) else x)
    for lab, _ in item.get("fig", []):
        a |= bare(lab)
    for pp in item.get("printed", []):
        a |= bare(pp[0])
    for x in item.get("read", []):
        a |= bare(x[0] if isinstance(x, (list, tuple)) else x)
    for x in item.get("calc", []):
        a |= bare(x)
    for val, lid in item.get("ext", []):
        a |= bare(val)
    return a


def chart_nums(chart):
    a = set()

    def walk(o):
        if isinstance(o, (int, float)) and not isinstance(o, bool):
            v = ("%g" % abs(o))
            a.add(v)
            if "." in v:
                a.add(v.rstrip("0").rstrip("."))
        elif isinstance(o, dict):
            for vv in o.values():
                walk(vv)
        elif isinstance(o, (list, tuple)):
            for vv in o:
                walk(vv)
        elif isinstance(o, str):
            a.update(bare(o))
    walk(chart or {})
    return a


REF_RE = re.compile(r"\[\[([^\]]+)\]\]")
FIGPAGE = {}


def run(D):
    errors = []
    ids = dict(claim={c["id"] for c in D["claims"]}, fig={f["id"] for f in D["figs"]},
               calc={c["id"] for c in D["calcs"]}, gap={g["id"] for g in D["gaps"]},
               lit={l["id"] for l in D["lit"]}, law={l["id"] for l in D["law"]})
    lit_nums = {l["id"]: {n.replace(",", "") for x in l["ext_nums"] for n in bare(x)} for l in D["lit"]}

    def ref_ok(r):
        if r.startswith("lit:"):
            return r[4:] in ids["lit"]
        if r.startswith("law:"):
            return r[4:] in ids["law"]
        return r in ids["claim"] or r in ids["fig"] or r in ids["calc"] or r in ids["gap"]

    for kind in ("claim", "fig", "calc", "gap", "lit", "law"):
        coll = {"claim": D["claims"], "fig": D["figs"], "calc": D["calcs"], "gap": D["gaps"],
                "lit": D["lit"], "law": D["law"]}[kind]
        if len(ids[kind]) != len(coll):
            errors.append("%s 的 id 有重複" % kind)

    global FIGPAGE
    FIGPAGE = {f["id"]: f["p"] for f in D["figs"]}
    grades = {g["k"] for g in D["grades"]}
    types = {t["k"] for t in D["types"]}
    srcs = {s["k"] for s in D["sources"]}
    stats = dict(nums=0, figlabels=0, anchors=0, web=0, read=0)

    # ---------------- 主張
    for c in D["claims"]:
        lab = c["id"]
        own = IDX.get((c["sec"], c["key"]))
        if own is None:
            errors.append("%s：段落 %s %s 不存在" % (lab, c["sec"], c["key"]))
            continue
        ok_pages = set(own["pages"])
        for fid in [x[1] for x in c.get("fig", [])] + [r for r in c["refs"] if r.startswith("fig")]:
            ok_pages |= {FIGPAGE.get(fid, -1)}   # 引用到的圖所在頁
        for x in c.get("nums", []):          # 跨段引用的數字（例如註 1）也算進可標的頁次
            if isinstance(x, (list, tuple)):
                q = IDX.get(tuple(x[1].split(":", 1)))
                if q:
                    ok_pages |= set(q["pages"])
        if not set(c["p"]) <= ok_pages:
            errors.append("%s：頁次 %s 不在段落頁次 %s 內" % (lab, c["p"], sorted(ok_pages)))
        if c["grade"] not in grades:
            errors.append("%s：等級 %s 不存在" % (lab, c["grade"]))
        if c["type"] not in types:
            errors.append("%s：類型 %s 不存在" % (lab, c["type"]))
        for s in c["src"]:
            if s not in srcs:
                errors.append("%s：資料來源 %s 不存在" % (lab, s))
        stats["nums"] += check_nums(c, own, errors, lab)
        stats["figlabels"] += check_fig_labels(dict(c, printed=[]), errors, lab)
        for a in c.get("anchors", []):
            if norm(a).lower() in own["n"].lower():
                stats["anchors"] += 1
            else:
                errors.append("%s：本段找不到關鍵詞「%s」" % (lab, a))
        w = c.get("web")
        if w:
            wl = norm(w).lower()
            if wl not in own["n"].lower():
                errors.append("%s：原文定位片語不在 PDF 本段：%s" % (lab, w))
            if wl not in WEB_L:
                errors.append("%s：原文定位片語不在官方網頁版：%s" % (lab, w))
            elif len(re.findall(r"[a-z0-9]+(?:'[a-z]+)?", norm(w).lower())) > 7:
                errors.append("%s：原文定位片語超過 7 個字：%s" % (lab, w))
            else:
                stats["web"] += 1
        for val, lid in c.get("ext", []):
            if lid[4:] not in lit_nums or not bare(val) <= lit_nums[lid[4:]]:
                errors.append("%s：外部數字 %s 沒有列在 %s 的 ext_nums" % (lab, val, lid))
        stats["read"] += len(c.get("read", []))
        for r in c["refs"]:
            if not ref_ok(r):
                errors.append("%s：refs 指到不存在的 %s" % (lab, r))
        allowed = declared(c, lit_nums)
        lint(c["zh"], allowed, errors, lab + ".zh")
        lint(c["note"], allowed, errors, lab + ".note")

    # ---------------- 圖
    for f in D["figs"]:
        lab = f["id"]
        stats["nums"] += check_nums(f, None, errors, lab)
        stats["figlabels"] += check_fig_labels(f, errors, lab)
        if f.get("title_img"):
            t = re.sub(r"[^a-z]", "", f["title_img"].lower())
            o = re.sub(r"[^a-z]", "", OCR.get(lab, "").lower())
            if t not in o:
                errors.append("%s：圖框大標題 OCR 對不上：%s" % (lab, f["title_img"]))
        if not IDX.get((f["sec"], lab)):
            errors.append("%s：找不到圖說段落" % lab)
        allowed = declared(f, lit_nums) | chart_nums(f.get("chart"))
        stats["read"] += len(f.get("read", []))
        for fld in ("what",):
            lint(f[fld], allowed, errors, lab + "." + fld)
        for fld in ("shows", "limits"):
            for i, x in enumerate(f[fld]):
                lint(x, allowed, errors, "%s.%s[%d]" % (lab, fld, i))
        for x in f.get("read", []) + f.get("printed", []):
            lint(x[1], allowed, errors, lab + ".label")
        for cid in f.get("claims", []):
            if cid not in ids["claim"]:
                errors.append("%s：claims 指到不存在的 %s" % (lab, cid))

    # ---------------- 核算
    for n in D["calcs"]:
        lab = n["id"]
        stats["nums"] += check_nums(n, None, errors, lab)
        stats["figlabels"] += check_fig_labels(dict(n, printed=[]), errors, lab)
        allowed = declared(n, lit_nums) | chart_nums(n.get("chart"))
        for fld in ("title", "inputs", "formula", "result", "reading", "caveat"):
            lint(n.get(fld, ""), allowed, errors, lab + "." + fld)
        for r in n["refs"]:
            if not ref_ok(r):
                errors.append("%s：refs 指到不存在的 %s" % (lab, r))

    # ---------------- 全域可用數字（給缺口、報告敘述用）
    GLOBAL = set(D["meta"]["nums_ok"])
    for coll in (D["claims"], D["figs"], D["calcs"]):
        for it in coll:
            GLOBAL |= declared(it, lit_nums) | chart_nums(it.get("chart"))
    for l in D["lit"]:
        GLOBAL |= lit_nums[l["id"]]

    for g in D["gaps"]:
        for fld in ("title", "body", "why"):
            lint(g[fld], GLOBAL, errors, g["id"] + "." + fld)
        for r in g["refs"]:
            if not ref_ok(r):
                errors.append("%s：refs 指到不存在的 %s" % (g["id"], r))

    for l in D["lit"]:
        allowed = lit_nums[l["id"]]
        for fld in ("facts", "fidelity"):
            lint(l[fld], allowed, errors, "lit:" + l["id"] + "." + fld)

    for l in D["law"]:
        allowed = bare(l["text"]) | bare(l["name"]) | GLOBAL
        for fld in ("zh", "note"):
            lint(l[fld], allowed, errors, "law:" + l["id"] + "." + fld)
        for r in l["maps"]:
            if not ref_ok(r):
                errors.append("law:%s：maps 指到不存在的 %s" % (l["id"], r))

    def walk_text(o, label):
        if isinstance(o, str):
            lint(o, GLOBAL, errors, label)
            for r in REF_RE.findall(o):
                if not ref_ok(r):
                    errors.append("%s：[[%s]] 指到不存在的東西" % (label, r))
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ("id", "t", "kind", "a", "b", "g", "x", "y"):
                    continue
                walk_text(v, label + "." + k)
        elif isinstance(o, (list, tuple)):
            for i, v in enumerate(o):
                walk_text(v, "%s[%d]" % (label, i))

    walk_text(D["report"], "report")
    walk_text(D["verdicts"], "verdicts")
    walk_text(D["policy"], "policy")
    walk_text([dict(t=n["t"], s=n["s"]) for n in D["chain"]["nodes"]], "chain")
    for n in D["chain"]["nodes"]:
        for r in n["refs"]:
            if not ref_ok(r):
                errors.append("chain：%s 指到不存在的 %s" % (n["id"], r))
    for v in D["verdicts"]:
        if v["claim"] not in ids["claim"]:
            errors.append("verdicts：%s 不存在" % v["claim"])

    # ---------------- 逐字引文
    ep = D["meta"]["epigraph"]
    p = IDX.get((ep["sec"], ep["key"]))
    if p is None or norm(ep["q"]) not in p["n"]:
        errors.append("epigraph：所標段落找不到逐字引文")
    if len(ep["q"].split()) >= 15:
        errors.append("epigraph：超過 14 個英文字")

    if errors:
        print("\n核對失敗 %d 項：" % len(errors), file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        raise AssertionError("%d 項未通過核對" % len(errors))
    print("核對通過：報告數字 %d 個、圖內標示 %d 個（OCR）、關鍵詞 %d 個、原文定位片語 %d 個（PDF 與網頁版雙邊）、讀圖數值 %d 個、逐字引文 1 句"
          % (stats["nums"], stats["figlabels"], stats["anchors"], stats["web"], stats["read"]))
    return stats


# ------------------------------------------------------------------ 著作權：連續 8 個英文字
def ngram_check(payload_strings, allow):
    """站上任何一個字串，若與報告全文有連續 8 個英文字相同，除了白名單（標題、章節名、圖題、文獻題名、逐字引文）都要中止。"""
    # 網址是定位資訊、不是表達，比對前先剝掉
    words = lambda s: re.findall(r"[a-z0-9]+(?:'[a-z]+)?", re.sub(r"https?://\S+", " ", norm(s)).lower())
    src = []
    for p in IDX.values():
        src.append(words(p["text"]))
    grams = set()
    for ws in src:
        for i in range(len(ws) - 7):
            grams.add(" ".join(ws[i:i + 8]))
    allow_grams = set()
    for a in allow:
        ws = words(a)
        for i in range(len(ws) - 7):
            allow_grams.add(" ".join(ws[i:i + 8]))
    hits = []
    for s in payload_strings:
        ws = words(s)
        for i in range(len(ws) - 7):
            g = " ".join(ws[i:i + 8])
            if g in grams and g not in allow_grams:
                hits.append(g)
    return sorted(set(hits))
