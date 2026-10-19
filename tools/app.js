/* Anthropic 就業報告拆解——前端。資料在 window.DATA（build.py 注入）。改完先跑 node --check tools/app.js */
(function () {
  "use strict";
  var D = window.DATA;
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  var by = function (arr, k) { var m = {}; arr.forEach(function (x) { m[x[k || "id"]] = x; }); return m; };
  var CL = by(D.claims), FG = by(D.figs), NC = by(D.calcs), GP = by(D.gaps), LT = by(D.lit), LW = by(D.law);
  var TYPE = {}; D.types.forEach(function (t) { TYPE[t.k] = t.zh; });
  var SRC = {}; D.sources.forEach(function (s) { SRC[s.k] = s.zh; });
  var GRADE = {}; D.grades.forEach(function (g) { GRADE[g.k] = g; });
  var SEC = by(D.sections, "k");
  var gcls = function (g) { return "g" + (g === "-" ? "X" : g); };

  /* ---------------------------------------------------------------- 連結 */
  function tf(phrase) {
    return D.meta.url_web + "#:~:text=" + encodeURIComponent(phrase).replace(/-/g, "%2D");
  }
  function pdfUrl(p) { return D.meta.url_pdf + "#page=" + p; }
  function secUrl(k) { var s = SEC[k]; return s && s.web ? D.meta.url_web + "#" + s.web : D.meta.url_web; }
  function ext(href, text) { return '<a href="' + esc(href) + '" target="_blank" rel="noopener">' + text + "</a>"; }

  function refKind(r) {
    if (r.indexOf("lit:") === 0) return "lit";
    if (r.indexOf("law:") === 0) return "law";
    if (/^fig\d$/.test(r)) return "fig";
    if (/^N\d+$/.test(r)) return "calc";
    if (/^G\d+$/.test(r)) return "gap";
    return "claim";
  }
  function refLabel(r) {
    var k = refKind(r);
    if (k === "lit") { var l = LT[r.slice(4)]; return l ? l.short : r; }
    if (k === "law") { var w = LW[r.slice(4)]; return w ? (w.chip || w.short) : r; }
    if (k === "fig") return "圖 " + r.slice(3);
    return r;
  }
  function chip(r) {
    var k = refKind(r), cls;
    if (k === "claim") cls = CL[r] ? gcls(CL[r].grade) : "gX";
    else cls = { calc: "kcalc", gap: "kgap", fig: "kfig", lit: "klit", law: "klaw" }[k];
    var title = { claim: "主張", calc: "數字核算", gap: "報告沒說的", fig: "圖", lit: "文獻", law: "法條" }[k];
    return '<a class="chip ' + cls + '" href="#ref/' + esc(r) + '" data-ref="' + esc(r) + '" title="' + title + '">' + esc(refLabel(r)) + "</a>";
  }
  /* 行內標記：**粗體**、[[ref]]；轉述裡的代號（L5、N1、G3）自動變成可點的標籤 */
  function md(s, auto) {
    var out = esc(s);
    if (auto) {
      out = out.replace(/(^|[^A-Za-z0-9#\/\-\[])((?:[KILPBHE]\d{1,2}|N\d{1,2}|G\d{1,2}))(?![A-Za-z0-9\]])/g, function (m, pre, id) {
        return (CL[id] || NC[id] || GP[id]) ? pre + chip(id) : m;
      });
    }
    out = out.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
    out = out.replace(/\[\[([^\]]+)\]\]/g, function (_, r) { return chip(r); });
    return out;
  }
  function coordOf(c) {
    var k = c.key, loc;
    if (/^KF/.test(k)) loc = "§1 重點發現 " + k.slice(2);
    else if (/^fig/.test(k)) loc = "圖 " + k.slice(3) + " 圖說";
    else if (k === "fn1") loc = "註 1";
    else loc = "§" + c.sec.slice(1) + k;
    return loc + " · p." + c.p.join("–");
  }
  function gradeBadge(g) {
    var G = GRADE[g];
    return '<span class="badge g ' + gcls(g) + '" title="' + esc(G.d) + '">' + (g === "-" ? "聲明" : g + "　" + G.zh) + "</span>";
  }

  /* ---------------------------------------------------------------- 卡片 */
  function claimCard(c) {
    var src = c.src.map(function (s) { return SRC[s]; }).join("、");
    return '<article class="card claim" id="c-' + c.id + '">' +
      '<div class="row1"><span class="id">' + c.id + "</span>" + gradeBadge(c.grade) +
      '<span class="typ">' + TYPE[c.type] + (src ? "・" + esc(src) : "") + "</span>" +
      (c.self ? '<span class="badge self" title="報告自己點出了這個限制">報告自承</span>' : "") +
      '<span class="coord" title="段落座標：§節¶段 · PDF 頁次">' + esc(coordOf(c)) + "</span>" +
      '<span class="src-links">' + (c.web ? ext(tf(c.web), "原文定位") : "") + ext(pdfUrl(c.p[0]), "PDF 第 " + c.p[0] + " 頁") + "</span></div>" +
      '<p class="zh">' + md(c.zh, true) + "</p>" +
      (c.note ? '<p class="note">' + md(c.note, true) + "</p>" : "") +
      (c.refs.length ? '<div class="refs">相關　' + c.refs.map(chip).join(" ") + "</div>" : "") +
      "</article>";
  }
  function labelList(arr, badge) {
    if (!arr || !arr.length) return "";
    return '<div class="labels">' + arr.map(function (x) {
      return '<span class="lab"><b>' + esc(x[0]) + "</b>　" + esc(x[1]) + "</span>";
    }).join("") + (badge || "") + "</div>";
  }
  function figBody(f, withChart) {
    var s = '<p class="small muted"><span class="en">' + esc(f.title_en) + "</span>" +
      (f.title_img ? "　圖框大標題：<span class=\"en\">" + esc(f.title_img) + "</span>" : "") + "</p>" +
      "<p>" + md(f.what, true) + "</p>";
    if (f.printed.length) s += '<h4>圖內標示 <span class="badge ocr">OCR 核對</span></h4>' + labelList(f.printed);
    if (f.read.length) s += '<h4>讀圖估計 <span class="badge read">讀圖</span></h4>' + labelList(f.read);
    if (withChart && f.chart) s += chartSlot(f.chart, f.id);
    s += '<div class="two"><div><h4>撐得起</h4><ul>' + f.shows.map(function (x) { return "<li>" + md(x, true) + "</li>"; }).join("") +
      '</ul></div><div><h4>撐不起或要小心</h4><ul>' + f.limits.map(function (x) { return "<li>" + md(x, true) + "</li>"; }).join("") + "</ul></div></div>";
    s += '<div class="refs small" style="margin-top:8px">相關主張　' + f.claims.map(chip).join(" ") + "</div>";
    s += '<p class="src-links small" style="margin-top:8px">' + ext(pdfUrl(f.p), "PDF 第 " + f.p + " 頁看原圖") + ext(secUrl(f.sec), "網頁版所在章節") + "</p>";
    return s;
  }
  function calcBody(n, withChart) {
    var s = '<dl class="kv"><dt>輸入</dt><dd>' + md(n.inputs, true) + "</dd><dt>公式</dt><dd>" + md(n.formula) + "</dd>" +
      "<dt>結果</dt><dd><b>" + md(n.result, true) + "</b></dd><dt>怎麼讀</dt><dd>" + md(n.reading, true) + "</dd>" +
      (n.caveat ? "<dt>注意</dt><dd>" + md(n.caveat, true) + "</dd>" : "") + "</dl>";
    if (withChart && n.chart) s += chartSlot(n.chart, n.id);
    s += '<div class="refs small">相關　' + n.refs.map(chip).join(" ") + "</div>";
    return s;
  }
  function gapBody(g) {
    var cls = { "高": "h", "中": "m", "低": "l" }[g.sev];
    return '<p><span class="sev ' + cls + '">嚴重度：' + g.sev + "</span></p><p>" + md(g.body, true) + "</p>" +
      '<p class="muted">為什麼重要　' + md(g.why, true) + "</p>" +
      '<div class="refs small">相關　' + g.refs.map(chip).join(" ") + "</div>";
  }
  var VD = { ok: "忠實", omits: "省略了限定", unchecked: "未核對", missing: "未引用" };
  function litBody(l) {
    return '<p><span class="vd ' + l.verdict + '">' + VD[l.verdict] + "</span>　" + esc(l.kind) + "</p>" +
      '<p><span class="en">' + esc(l.title) + "</span>　<span class=\"small muted\">" + esc(l.venue) + "</span></p>" +
      '<dl class="kv"><dt>報告怎麼用</dt><dd>' + esc(l.used) + "</dd><dt>核對來源</dt><dd>" + esc(l.checked) + "</dd>" +
      "<dt>它說了什麼</dt><dd>" + md(l.facts) + "</dd><dt>轉述是否忠實</dt><dd>" + md(l.fidelity) + "</dd></dl>" +
      '<p class="small">' + ext(l.url, "原文連結") + "</p>";
  }
  function lawBody(l) {
    return '<blockquote lang="' + (l.id === "tw" ? "zh-Hant" : "en") + '">' + esc(l.text) + "</blockquote>" +
      (l.zh ? '<p class="zh">' + esc(l.zh) + "</p>" : "") +
      '<p class="note"><b>對應</b>　' + md(l.note) + "</p>" +
      '<div class="refs small">對應的主張　' + l.maps.map(chip).join(" ") + "　" + ext(l.url, "官方來源") + "</div>";
  }
  function lawCard(l) {
    return '<div class="card law' + (l.id === "tw" ? " tw" : "") + '" id="law-' + l.id + '"><div class="hd"><b>' + esc(l.name) + "</b>" +
      '<span class="badge">' + esc(l.juris) + '</span><span class="small muted">' + esc(l.short) + "</span></div>" + lawBody(l) + "</div>";
  }

  /* ---------------------------------------------------------------- 圖表 */
  var CHARTS = [], CHN = 0;
  function chartSlot(spec, key) {
    var id = "ch-" + key + "-" + (CHN++);
    CHARTS.push({ id: id, spec: spec });
    return '<div class="chart" id="' + id + '"></div>' + (spec.note ? '<p class="chart-note">' + esc(spec.note) + "</p>" : "") +
      '<p class="chart-note">本站依圖內標示與讀圖重畫，不是原圖；讀圖數值是估計。</p>';
  }
  function drawCharts() {
    CHARTS.forEach(function (c) {
      var el = $(c.id);
      if (!el || !el.offsetParent) return;
      var W = Math.max(300, Math.min(780, el.clientWidth || 700));
      if (el.dataset.w === String(W)) return;
      el.dataset.w = String(W);
      var fn = { dumbbell: chDumbbell, slope: chDumbbell, bars: chBars, event: chEvent, scatter: chScatter, pair: chPair, scenario: chScenario }[c.spec.kind];
      el.innerHTML = fn ? fn(W, c.spec) : "";
    });
  }
  function svg(W, H, inner, label) {
    return '<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + esc(label || "") + '">' + inner + "</svg>";
  }
  function T(x, y, s, cls, anchor, size, weight) {
    return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" class="' + (cls || "svg-t") + '" font-size="' + (size || 12.5) +
      '"' + (anchor ? ' text-anchor="' + anchor + '"' : "") + (weight ? ' font-weight="' + weight + '"' : "") + ">" + esc(s) + "</text>";
  }
  function L(x1, y1, x2, y2, cls, w, dash) {
    return '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" class="' + cls +
      '" stroke-width="' + (w || 1) + '"' + (dash ? ' stroke-dasharray="' + dash + '"' : "") + "/>";
  }
  function fmt(v) { return (Math.round(v * 10) / 10).toString(); }
  /* 估計文字寬度：中日韓全形字約等於字級，半形約 0.56 倍 */
  function textW(s, size) { var w = 0; for (var i = 0; i < s.length; i++) w += s.charCodeAt(i) > 0x2e80 ? size : size * 0.56; return w; }
  function labelW(rows, size, cap) { return Math.min(cap, Math.max.apply(null, rows.map(function (r) { return textW(r[0], size); })) + 14); }
  function tick(v) { return (Math.round(v * 100) / 100).toString(); }

  /* 啞鈴：起點空心、終點實心（圖 1 的六列、圖 7 的十二列） */
  function chDumbbell(W, sp) {
    var rows = sp.rows.slice();
    if (sp.kind === "dumbbell") rows.sort(function (a, b) { return (b[2] - b[1]) - (a[2] - a[1]); });
    var lw = labelW(rows, 12.5, W * 0.45), pr = 44, top = sp.kind === "slope" ? 50 : 34, rh = 26, H = top + rows.length * rh + 30;
    var lx = W < 520 ? 4 : lw;
    var max = Math.max.apply(null, rows.map(function (r) { return Math.max(r[1], r[2]); })) * 1.08;
    var x = function (v) { return lw + (W - lw - pr) * v / max; };
    var g = "", step = max > 25 ? 10 : 5;
    for (var t = 0; t <= max; t += step) {
      g += L(x(t), top - 8, x(t), H - 26, "svg-grid") + T(x(t), H - 10, t + (sp.unit || ""), "svg-m", "middle", 11.5);
    }
    rows.forEach(function (r, i) {
      var y = top + i * rh + rh / 2, c = r[3] === "non" ? "svg-c2" : (r[3] === "tech" ? "svg-c1" : "svg-c2");
      g += T(lw - 8, y + 4, r[0], "svg-t", "end", 12.5);
      g += L(x(r[1]), y, x(r[2]), y, "svg-axis", 2.2);
      g += '<circle cx="' + x(r[1]).toFixed(1) + '" cy="' + y + '" r="5" class="svg-bg" stroke-width="1.8" style="stroke:var(--muted)"/>';
      g += '<circle cx="' + x(r[2]).toFixed(1) + '" cy="' + y + '" r="5.5" class="' + c + '"/>';
      var up = r[2] >= r[1], u = sp.unit || "";
      /* 終點值放在實心圓外側；起點值（讀圖）放在空心圓外側，空間不夠就省略 */
      g += up ? T(x(r[2]) + 9, y + 4, fmt(r[2]) + u, "svg-t", null, 12, 600)
              : T(x(r[2]) - 9, y + 4, fmt(r[2]) + u, "svg-t", "end", 12, 600);
      if (up && x(r[1]) - lw > 46) g += T(x(r[1]) - 9, y + 4, fmt(r[1]), "svg-m", "end", 11);
      if (!up) g += T(x(r[1]) + 9, y + 4, fmt(r[1]), "svg-m", null, 11);
    });
    var lg = '<circle cx="' + (lx + 6) + '" cy="12" r="5" class="svg-bg" stroke-width="1.8" style="stroke:var(--muted)"/>' + T(lx + 16, 16, sp.a || sp.start, "svg-m", null, 11.5);
    if (sp.kind === "slope") {
      lg += '<circle cx="' + (lx + 6) + '" cy="28" r="5" class="svg-c1"/>' + T(lx + 16, 32, "技術部門的" + sp.end, "svg-m", null, 11.5) +
        '<circle cx="' + (lx + 6) + '" cy="44" r="5" class="svg-c2"/>' + T(lx + 16, 48, "非技術部門的" + sp.end, "svg-m", null, 11.5);
    } else {
      lg += '<circle cx="' + (lx + 6) + '" cy="28" r="5" class="svg-c2"/>' + T(lx + 16, 32, sp.b, "svg-m", null, 11.5);
    }
    return svg(W, H + 10, '<g transform="translate(0,6)">' + g + "</g>" + lg, "啞鈴圖");
  }
  /* 橫條：圖 3 的倍數 */
  function chBars(W, sp) {
    var lw = labelW(sp.rows, 12.5, W * 0.52), pr = 50, top = 10, rh = 30, H = top + sp.rows.length * rh + 30;
    var max = Math.max.apply(null, sp.rows.map(function (r) { return r[1]; })) * 1.1;
    var x = function (v) { return lw + (W - lw - pr) * v / max; };
    var g = "";
    for (var t = 0; t <= max; t += 1) g += L(x(t), top, x(t), H - 24, "svg-grid") + T(x(t), H - 8, t + "×", "svg-m", "middle", 11.5);
    sp.rows.forEach(function (r, i) {
      var y = top + i * rh;
      g += T(lw - 8, y + 19, r[0], "svg-t", "end", 12.5);
      g += '<rect x="' + lw + '" y="' + (y + 6) + '" width="' + (x(r[1]) - lw).toFixed(1) + '" height="18" rx="3" class="svg-c1"/>';
      g += T(x(r[1]) + 6, y + 19, fmt(r[1]) + "×", "svg-t", null, 12, 600);
    });
    g += L(x(sp.ref), top - 2, x(sp.ref), H - 24, "svg-axis", 1.4, "4 3") + T(x(sp.ref) + 4, top + 4, "基期", "svg-m", null, 11);
    return svg(W, H, g, "橫條圖");
  }
  /* 事件研究：讀圖重畫的兩個面板 */
  function chEvent(W, sp) {
    var cols = W >= 620 ? 2 : 1, gap = 28, pw = (W - (cols - 1) * gap) / cols, ph = 230, out = "";
    sp.panels.forEach(function (p, k) {
      var ox = (k % cols) * (pw + gap), oy = Math.floor(k / cols) * (ph + 26);
      var l = 40, r = 10, t = 28, b = 34, iw = pw - l - r, ih = ph - t - b;
      var lo = Math.min.apply(null, p.lo.concat([0])), hi = Math.max.apply(null, p.hi.concat([0]));
      var pad = (hi - lo) * 0.08; lo -= pad; hi += pad;
      var xs = p.x, xn = xs.length;
      var X = function (i) { return ox + l + iw * (i + 0.5) / xn; };
      var Y = function (v) { return oy + t + ih * (hi - v) / (hi - lo); };
      var s = T(ox + l, oy + 14, p.t, "svg-t", null, 12.5, 600);
      var preEnd = xs.indexOf(-1) + 0.5;
      s += '<rect x="' + (ox + l) + '" y="' + (oy + t) + '" width="' + (iw * preEnd / xn).toFixed(1) + '" height="' + ih + '" class="svg-shade"/>';
      s += T(ox + l + 6, oy + t + 14, "採用前", "svg-m", null, 11);
      var step = (hi - lo) > 1.5 ? 1 : 0.25;
      for (var v = Math.ceil(lo / step) * step; v <= hi; v += step) {
        s += L(ox + l, Y(v), ox + l + iw, Y(v), Math.abs(v) < 1e-9 ? "svg-axis" : "svg-grid", Math.abs(v) < 1e-9 ? 1.3 : 1) +
          T(ox + l - 6, Y(v) + 4, tick(v), "svg-m", "end", 11);
      }
      xs.forEach(function (xv, i) {
        s += T(X(i), oy + ph - b + 16, (xv > 0 ? "+" : "") + xv, "svg-m", "middle", 11);
        if (xv !== -1) s += L(X(i), Y(p.lo[i]), X(i), Y(p.hi[i]), "svg-line2", 1.6);
      });
      var path = xs.map(function (xv, i) { return (i ? "L" : "M") + X(i).toFixed(1) + " " + Y(p.y[i]).toFixed(1); }).join(" ");
      s += '<path d="' + path + '" fill="none" class="svg-line2" stroke-width="1.6"/>';
      xs.forEach(function (xv, i) {
        s += xv === -1 ? '<circle cx="' + X(i).toFixed(1) + '" cy="' + Y(0).toFixed(1) + '" r="4.5" class="svg-bg" stroke-width="1.8" style="stroke:var(--c2)"/>'
          : '<circle cx="' + X(i).toFixed(1) + '" cy="' + Y(p.y[i]).toFixed(1) + '" r="4.5" class="svg-c2"/>';
      });
      s += T(ox + l + iw / 2, oy + ph - 2, "相對採用的月份", "svg-m", "middle", 11);
      out += s;
    });
    var rowsN = Math.ceil(sp.panels.length / cols);
    return svg(W, rowsN * ph + (rowsN - 1) * 26, out, "事件研究圖");
  }
  /* 散布：圖 5 */
  function chScatter(W, sp) {
    var H = Math.max(260, Math.min(380, W * 0.56)), l = 44, r = 14, t = 14, b = 40, iw = W - l - r, ih = H - t - b;
    var lo = -0.8, hi = 1.5;
    var X = function (v) { return l + iw * v / 100; }, Y = function (v) { return t + ih * (hi - v) / (hi - lo); };
    var g = "";
    [-0.5, 0, 0.5, 1, 1.5].forEach(function (v) {
      g += L(l, Y(v), l + iw, Y(v), v === 0 ? "svg-axis" : "svg-grid", v === 0 ? 1.4 : 1) + T(l - 6, Y(v) + 4, fmt(v), "svg-m", "end", 11);
    });
    [0, 20, 40, 60, 80, 100].forEach(function (v) { g += T(X(v), H - 22, v, "svg-m", "middle", 11); });
    g += T(l + iw / 2, H - 4, "職務的 Claude 任務複雜度（百分位）", "svg-m", "middle", 11.5);
    g += T(l + 4, t + 10, "初階人數成長（對數點）", "svg-m", null, 11);
    sp.pts.forEach(function (p) {
      var rr = 3 + p[2] * 2.2, cls = p[1] > 0.005 ? "svg-c1" : (p[1] < -0.005 ? "svg-c2" : "svg-c3");
      g += '<circle cx="' + X(p[0]).toFixed(1) + '" cy="' + Y(p[1]).toFixed(1) + '" r="' + rr.toFixed(1) + '" class="' + cls + '" fill-opacity=".35" stroke-width="1.2"/>';
    });
    g += L(X(sp.line[0][0]), Y(sp.line[0][1]), X(sp.line[1][0]), Y(sp.line[1][1]), "svg-axis", 1.8, "6 4");
    var up = sp.pts.filter(function (p) { return p[1] > 0.005; }).length, dn = sp.pts.filter(function (p) { return p[1] < -0.005; }).length;
    g += T(l + iw - 4, t + 12, "增加 " + up + "　持平 " + (sp.pts.length - up - dn) + "　減少 " + dn, "svg-t", "end", 12, 600);
    return svg(W, H, g, "散布圖");
  }
  /* 成對橫條：圖 6 的前一個月與最後一個月 */
  function chPair(W, sp) {
    var lw = labelW(sp.rows, 12.5, W * 0.45), pr = 40, top = 56, rh = 40, H = top + sp.rows.length * rh + 28;
    var lx = W < 520 ? 4 : lw;
    var max = 48, x = function (v) { return lw + (W - lw - pr) * v / max; };
    var g = "";
    [0, 10, 20, 30, 40].forEach(function (v) { g += L(x(v), top - 6, x(v), H - 24, "svg-grid") + T(x(v), H - 8, v, "svg-m", "middle", 11); });
    sp.refs.forEach(function (v) {
      g += L(x(v), top - 10, x(v), H - 24, "svg-axis", 1.5, "4 3") + T(x(v) + 3, top - 14, v === 20 ? "半週" : "一週", "svg-m", null, 11);
    });
    sp.rows.forEach(function (r, i) {
      var y = top + i * rh;
      g += T(lw - 8, y + 21, r[0], "svg-t", "end", 12.5);
      g += '<rect x="' + lw + '" y="' + (y + 5) + '" width="' + (x(r[1]) - lw).toFixed(1) + '" height="13" rx="2" class="svg-c3" fill-opacity=".55"/>';
      g += '<rect x="' + lw + '" y="' + (y + 20) + '" width="' + (x(r[2]) - lw).toFixed(1) + '" height="13" rx="2" class="svg-c2"/>';
      g += T(x(r[1]) + 5, y + 16, fmt(r[1]), "svg-m", null, 11) + T(x(r[2]) + 5, y + 31, fmt(r[2]), "svg-t", null, 11.5, 600);
    });
    g += '<rect x="' + lx + '" y="2" width="11" height="11" class="svg-c3" fill-opacity=".55"/>' + T(lx + 16, 12, sp.a, "svg-m", null, 11.5) +
      '<rect x="' + lx + '" y="19" width="11" height="11" class="svg-c2"/>' + T(lx + 16, 29, sp.b, "svg-m", null, 11.5);
    return svg(W, H, g, "成對橫條圖");
  }
  /* 情境：N1 */
  function chScenario(W, sp) {
    var H = 240, l = 40, r = 10, t = 18, b = 46, iw = W - l - r, ih = H - t - b, n = sp.rows.length;
    var max = 2.1, Y = function (v) { return t + ih * (max - v) / max; };
    var g = "";
    [0, 0.5, 1, 1.5, 2].forEach(function (v) { g += L(l, Y(v), l + iw, Y(v), "svg-grid") + T(l - 6, Y(v) + 4, fmt(v), "svg-m", "end", 11); });
    sp.rows.forEach(function (rw, i) {
      var bw = Math.min(70, iw / n * 0.55), cx = l + iw * (i + 0.5) / n;
      g += '<rect x="' + (cx - bw / 2).toFixed(1) + '" y="' + Y(rw[2]).toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + (Y(0) - Y(rw[2])).toFixed(1) +
        '" rx="3" class="' + (rw[2] >= 1 ? "svg-c1" : "svg-c2") + '"/>';
      g += T(cx, Y(rw[2]) - 6, rw[2].toFixed(2) + " 倍", "svg-t", "middle", 12, 600);
      g += T(cx, H - 26, rw[0], "svg-t", "middle", 12) + T(cx, H - 10, "全公司 ×" + rw[1], "svg-m", "middle", 11);
    });
    g += L(l, Y(sp.ref), l + iw, Y(sp.ref), "svg-axis", 1.5, "5 4") + T(l + 4, Y(sp.ref) - 6, "原本的初階技術人數＝1", "svg-m", null, 11);
    return svg(W, H, g, "情境試算");
  }
  /* 論證鏈：寬螢幕畫圖、窄螢幕列清單 */
  function chainHtml() {
    return '<div class="chart" id="chain-box"></div><p class="chart-note">點節點看支撐它的主張。顏色是證據等級：' +
      D.grades.filter(function (g) { return g.k !== "-"; }).map(function (g) { return '<span class="chip ' + gcls(g.k) + '">' + g.k + "</span> " + esc(g.zh); }).join("　") + "</p>";
  }
  function drawChain() {
    var el = $("chain-box");
    if (!el || !el.offsetParent) return;
    var W = el.clientWidth || 700, C = D.chain;
    var N = {}; C.nodes.forEach(function (n) { N[n.id] = n; });
    var edgeList = '<ol class="small chain-list" style="padding-left:1.6em;margin-top:6px">' + C.edges.map(function (e) {
      return "<li><b>" + esc(N[e.a].t) + "</b> → <b>" + esc(N[e.b].t) + "</b>：" + esc(e.t) + "　" +
        (e.conflict ? '<span class="chip gX" style="color:var(--bad)">反向作用</span>' : '<span class="chip ' + gcls(e.g) + '">' + e.g + "</span>") + "</li>";
    }).join("") + "</ol>";
    if (W < 560) {
      el.innerHTML = edgeList + C.nodes.map(function (n) {
        return '<p class="small"><span class="chip ' + gcls(n.g) + '">' + n.g + "</span> <b>" + esc(n.t) + "</b>　" + esc(n.s) + "　" + n.refs.map(chip).join(" ") + "</p>";
      }).join("");
      return;
    }
    var bw = 200, bh = 80, CW = 760, CH = 350, sc = Math.min(1, W / CW);
    var ctr = function (n) { return [n.x + bw / 2, n.y + bh / 2]; };
    var clip = function (p, q) {
      var dx = q[0] - p[0], dy = q[1] - p[1], tx = Math.abs(dx) > 1e-6 ? (bw / 2 + 2) / Math.abs(dx) : 1e9, ty = Math.abs(dy) > 1e-6 ? (bh / 2 + 2) / Math.abs(dy) : 1e9;
      var tt = Math.min(tx, ty); return [p[0] + dx * tt, p[1] + dy * tt];
    };
    var g = "<defs>" + ["A", "B", "C", "D", "X"].map(function (k) {
      return '<marker id="ar-' + k + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" class="f-' + k + '"/></marker>';
    }).join("") + "</defs>";
    var marks = "";
    C.edges.forEach(function (e, i) {
      var a = ctr(N[e.a]), b = ctr(N[e.b]);
      var pair = (e.a === "f" && e.b === "g") || (e.a === "g" && e.b === "f");
      var off = pair ? (e.a === "f" ? -11 : 11) : 0;
      a = [a[0], a[1] + off]; b = [b[0], b[1] + off];
      var p = clip(a, b), q = clip(b, a), k = e.conflict ? "X" : e.g;
      g += '<line x1="' + p[0].toFixed(1) + '" y1="' + p[1].toFixed(1) + '" x2="' + q[0].toFixed(1) + '" y2="' + q[1].toFixed(1) + '" class="e-' + k +
        '" stroke-width="2.2"' + (e.dash ? ' stroke-dasharray="6 5"' : "") + ' marker-end="url(#ar-' + k + ')"/>';
      var mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2;
      marks += '<circle cx="' + mx.toFixed(1) + '" cy="' + my.toFixed(1) + '" r="10" class="svg-bg" stroke-width="1.6" style="stroke:var(--' + (k === "X" ? "bad" : "g" + k) + ')"/>' +
        T(mx, my + 4.5, String(i + 1), k === "X" ? "f-X" : "svg-t", "middle", 12, 700);
    });
    C.nodes.forEach(function (n) {
      var lines = [], s = n.s; while (s.length) { lines.push(s.slice(0, 14)); s = s.slice(14); }
      g += '<g class="node" data-node="' + n.id + '" style="cursor:pointer" tabindex="0" role="button" aria-label="' + esc(n.t) + '">' +
        '<rect x="' + n.x + '" y="' + n.y + '" width="' + bw + '" height="' + bh + '" rx="9" stroke-width="1.2"/>' +
        '<rect x="' + n.x + '" y="' + n.y + '" width="6" height="' + bh + '" rx="3" class="f-' + n.g + '"/>' +
        T(n.x + 16, n.y + 23, n.t, "svg-t", null, 14.5, 700) + T(n.x + bw - 10, n.y + 21, n.g, "f-" + n.g, "end", 13, 700) +
        lines.slice(0, 3).map(function (ln, i) { return T(n.x + 16, n.y + 43 + i * 16, ln, "svg-m", null, 12); }).join("") + "</g>";
    });
    g += marks;
    g += T(560, 150, "數字＝下方清單的編號", "svg-m", null, 12);
    g += T(560, 170, "點方塊看支撐它的主張", "svg-m", null, 12);
    el.innerHTML = '<svg viewBox="0 0 ' + CW + " " + CH + '" width="' + (CW * sc).toFixed(0) + '" height="' + (CH * sc).toFixed(0) + '" role="img" aria-label="論證鏈">' + g + "</svg>" + edgeList;
    el.querySelectorAll("[data-node]").forEach(function (nd) {
      var open = function () { openNode(N[nd.getAttribute("data-node")]); };
      nd.addEventListener("click", open);
      nd.addEventListener("keydown", function (ev) { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(); } });
    });
  }

  /* ---------------------------------------------------------------- 抽屜 */
  var lastFocus = null;
  function openDrawer(title, html) {
    lastFocus = document.activeElement;
    var dr = $("drawer");
    dr.innerHTML = '<button class="x" type="button" id="dr-x" aria-label="關閉">關閉 ✕</button><h3 id="dr-title">' + title + "</h3>" + html;
    dr.hidden = false; $("scrim").hidden = false;
    drawCharts();
    $("dr-x").focus();
    $("dr-x").onclick = closeDrawer;
  }
  function closeDrawer() {
    $("drawer").hidden = true; $("scrim").hidden = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function openRef(r) {
    var k = refKind(r);
    if (k === "claim" && CL[r]) return openDrawer("主張 " + r, claimCard(CL[r]) + '<p class="small"><a href="#claims/' + r + '">在主張帳本裡看前後文 →</a></p>');
    if (k === "calc" && NC[r]) return openDrawer("數字核算 " + r + "　" + esc(NC[r].title), calcBody(NC[r], true));
    if (k === "gap" && GP[r]) return openDrawer("報告沒說的 " + r + "　" + esc(GP[r].title), gapBody(GP[r]));
    if (k === "fig" && FG[r]) return openDrawer("圖 " + FG[r].n + "　" + esc(FG[r].zh), figBody(FG[r], true));
    if (k === "lit" && LT[r.slice(4)]) return openDrawer(esc(LT[r.slice(4)].cite), litBody(LT[r.slice(4)]));
    if (k === "law" && LW[r.slice(4)]) { var l = LW[r.slice(4)]; return openDrawer(esc(l.name), '<p><span class="badge">' + esc(l.juris) + "</span></p>" + lawBody(l)); }
  }
  function openNode(n) {
    openDrawer("論證環節：" + esc(n.t), '<p><span class="chip ' + gcls(n.g) + '">' + n.g + "</span>　" + esc(n.s) + "</p>" +
      n.refs.map(function (r) { return CL[r] ? claimCard(CL[r]) : ""; }).join(""));
  }

  /* ---------------------------------------------------------------- 報告 */
  function statsHtml() {
    var s = D.stats, tot = s.claims;
    var seg = function (n, v) { return '<i style="width:' + (100 * n / tot).toFixed(2) + "%;background:var(--" + v + ')"></i>'; };
    return '<div class="stats">' +
      '<div class="stat"><b>' + s.claims + "</b><span>則主張，逐段拆解</span></div>" +
      '<div class="stat"><b>' + s.nums + "</b><span>個報告數字，機械核對</span></div>" +
      '<div class="stat"><b>' + s.calcs + "</b><span>項自己重算的數字</span></div>" +
      '<div class="stat"><b>' + s.gaps + "</b><span>項報告沒說的事（高 " + s.gaps_high + "）</span></div></div>" +
      '<div class="gbar" aria-hidden="true">' + seg(s.gA, "gA") + seg(s.gB, "gB") + seg(s.gC, "gC") + seg(s.gD, "gD") + seg(s.gX, "gX") + "</div>" +
      '<div class="gleg"><span style="--c:var(--gA)">A 直接量測 ' + s.gA + '</span><span style="--c:var(--gB)">B 量測有缺口 ' + s.gB +
      '</span><span style="--c:var(--gC)">C 間接或有替代解釋 ' + s.gC + '</span><span style="--c:var(--gD)">D 軼事或規範 ' + s.gD +
      '</span><span style="--c:var(--gX)">方法或限制聲明 ' + s.gX + "</span></div>";
  }
  function block(b) {
    switch (b.t) {
      case "p": return "<p>" + md(b.x) + "</p>";
      case "h3": return "<h3>" + md(b.x) + "</h3>";
      case "ul": return "<ul>" + b.items.map(function (x) { return "<li>" + md(x) + "</li>"; }).join("") + "</ul>";
      case "callout": return '<div class="callout ' + b.kind + '">' + md(b.x) + "</div>";
      case "coi": return '<div class="callout warn">' + esc(D.meta.coi) + "</div>";
      case "stats": return statsHtml();
      case "verdicts": return '<div class="grid2">' + D.verdicts.map(function (v) {
        var g = v.grade.charAt(0);
        return '<div class="card verdict"><div class="kf">' + esc(v.kf) + "　" + chip(v.claim) + "</div><h4>" + esc(v.head) + "</h4>" +
          '<div class="v"><span class="badge g ' + gcls(g) + '">' + esc(v.grade) + "</span><span>" + esc(v.verdict) + "</span></div>" +
          '<p class="b">' + md(v.body) + "</p></div>";
      }).join("") + "</div>";
      case "chain": return chainHtml();
      case "policy": return '<div class="tbl-wrap"><table class="tbl stack"><thead><tr><th>建議</th><th>報告的理由</th><th>證據</th><th>評析</th><th>美國法下的位置</th></tr></thead><tbody>' +
        D.policy.map(function (r) {
          return "<tr><td data-h=\"建議\"><b>" + md(r.item) + '</b></td><td data-h="報告的理由">' + md(r.why) + '</td><td data-h="證據">' + md(r.evidence) +
            '</td><td data-h="評析">' + md(r.assess) + '</td><td data-h="美國法下的位置">' + md(r.law) + "</td></tr>";
        }).join("") + "</tbody></table></div>";
      case "lawcards": return D.law.map(lawCard).join("");
      default: return "";
    }
  }
  function renderReport() {
    var m = D.meta;
    var toc = D.report.map(function (s) { return '<a href="#report/' + s.id + '" data-toc="' + s.id + '">' + esc(s.title.replace(/：.*$/, "")) + "</a>"; }).join("");
    var body = D.report.map(function (s) {
      return '<h2 id="r-' + s.id + '">' + esc(s.title) + "</h2>" + s.blocks.map(block).join("");
    }).join("");
    $("v-report").innerHTML =
      '<div class="hero"><div class="kicker">獨立分析筆記・非 Anthropic 出版品</div>' +
      "<h1>Anthropic 怎麼看自己的就業變化：逐項拆解<span class=\"en\">" + esc(m.title_en) + "</span></h1>" +
      '<div class="meta-line">' + esc(m.authors.join("、")) + "　·　" + esc(m.institution) + "　·　" + esc(m.date) + "　·　PDF " + m.pages + " 頁、" + m.figures + " 張圖</div>" +
      '<p class="lede">這份報告用 Anthropic 自己的內部資料，描述 AI agent 進入日常工作之後，就業、生產力與招募標準怎麼變。本站把它拆成 ' + D.stats.claims +
      " 則主張，逐一標出證據強度、回到原文核對，並把報告沒說的事整理出來。</p>" +
      '<div class="btns">' + '<a class="btn primary" href="#report/bottom">先看結論</a>' + ext(m.url_web, "讀原文網頁").replace("<a ", '<a class="btn" ') +
      ext(m.url_pdf, "開原文 PDF").replace("<a ", '<a class="btn" ') + '<a class="btn" href="report.md" download>下載 Markdown 版</a>' + "</div>" +
      '<div class="epi"><q lang="en">' + esc(m.epigraph.q) + '</q><span class="who">—— ' + esc(m.epigraph.who) + "（全站唯一的逐字引文）</span></div></div>" +
      '<div class="wrap" style="margin-top:22px"><nav class="toc" aria-label="報告目錄">' + toc + '</nav><article class="article">' + body + "</article></div>";
    drawChain();
    spy();
  }
  var spyObs = null;
  function spy() {
    if (!("IntersectionObserver" in window)) return;
    if (spyObs) spyObs.disconnect();
    var links = {}; document.querySelectorAll("[data-toc]").forEach(function (a) { links[a.getAttribute("data-toc")] = a; });
    spyObs = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (e.isIntersecting) {
          Object.keys(links).forEach(function (k) { links[k].classList.remove("on"); });
          var a = links[e.target.id.slice(2)]; if (a) a.classList.add("on");
        }
      });
    }, { rootMargin: "-70px 0px -70% 0px" });
    document.querySelectorAll("#v-report h2[id^=r-]").forEach(function (h) { spyObs.observe(h); });
  }

  /* ---------------------------------------------------------------- 主張帳本 */
  var F = { q: "", sec: "", grade: "", type: "", src: "", self: false };
  function renderClaims() {
    var opt = function (v, t, cur) { return '<option value="' + esc(v) + '"' + (v === cur ? " selected" : "") + ">" + esc(t) + "</option>"; };
    $("v-claims").innerHTML = "<h1>主張帳本</h1>" +
      '<p class="lede">報告裡每一則可檢驗的主張，依原文順序排列。「報告說了什麼」是本站的轉述，不是翻譯；「評析」是本站的判斷。每則都能一鍵回到原句：' +
      "「原文定位」會打開 Anthropic 官方網頁並標亮那一句（Chrome、Edge、Safari、Firefox 新版支援），「PDF」會開到該頁。</p>" +
      statsHtml() +
      '<div class="filters" role="search"><input type="search" id="f-q" placeholder="搜尋代號或內容，例如 L5、法務、初階" value="' + esc(F.q) + '" aria-label="搜尋">' +
      '<select id="f-sec" aria-label="章節">' + opt("", "全部章節", F.sec) + D.sections.filter(function (s) { return s.k !== "S0" && s.k !== "S7"; }).map(function (s) { return opt(s.k, "§" + s.k.slice(1) + " " + s.zh, F.sec); }).join("") + "</select>" +
      '<select id="f-grade" aria-label="證據等級">' + opt("", "全部等級", F.grade) + D.grades.map(function (g) { return opt(g.k, (g.k === "-" ? "聲明" : g.k) + " " + g.zh, F.grade); }).join("") + "</select>" +
      '<select id="f-type" aria-label="類型">' + opt("", "全部類型", F.type) + D.types.map(function (t) { return opt(t.k, t.zh, F.type); }).join("") + "</select>" +
      '<select id="f-src" aria-label="資料來源">' + opt("", "全部來源", F.src) + D.sources.map(function (s) { return opt(s.k, s.zh, F.src); }).join("") + "</select>" +
      '<label><input type="checkbox" id="f-self"' + (F.self ? " checked" : "") + ">報告自承</label>" +
      '<span class="count" id="f-count"></span></div><div id="claim-list"></div>';
    ["f-q", "f-sec", "f-grade", "f-type", "f-src", "f-self"].forEach(function (id) {
      $(id).addEventListener(id === "f-q" ? "input" : "change", function () {
        F.q = $("f-q").value.trim(); F.sec = $("f-sec").value; F.grade = $("f-grade").value; F.type = $("f-type").value; F.src = $("f-src").value; F.self = $("f-self").checked;
        listClaims();
      });
    });
    listClaims();
  }
  function listClaims() {
    var q = F.q.toLowerCase();
    var rows = D.claims.filter(function (c) {
      if (F.sec && c.sec !== F.sec) return false;
      if (F.grade && c.grade !== F.grade) return false;
      if (F.type && c.type !== F.type) return false;
      if (F.src && c.src.indexOf(F.src) < 0) return false;
      if (F.self && !c.self) return false;
      if (q && (c.id + " " + c.zh + " " + c.note).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    var cur = "", html = "";
    rows.forEach(function (c) {
      if (c.sec !== cur) { cur = c.sec; var s = SEC[c.sec]; html += '<h3 style="margin-top:26px">§' + c.sec.slice(1) + " " + esc(s.zh) + ' <span class="small muted en">' + esc(s.en) + "</span>" + ' <span class="small">' + ext(secUrl(c.sec), "原文章節") + "</span></h3>"; }
      html += claimCard(c);
    });
    $("claim-list").innerHTML = html || '<div class="empty">沒有符合條件的主張。</div>';
    $("f-count").textContent = "顯示 " + rows.length + " ／ " + D.claims.length + " 則";
  }

  /* ---------------------------------------------------------------- 其他檢視 */
  function renderFigs() {
    $("v-figs").innerHTML = "<h1>八張圖重讀</h1>" +
      '<p class="lede">報告的八張圖都是點陣圖。本站不轉載原圖，改成記錄每張圖量了什麼、圖上印了什麼（以 OCR 核對）、讀圖估計的數值（標「讀圖」），以及它撐得起與撐不起的結論；' +
      "有六張依標示與讀圖重畫，方便看出原圖不容易看出的東西。</p>" +
      D.figs.map(function (f) {
        return '<article class="card item" id="f-' + f.id + '"><div class="hd"><h3>圖 ' + f.n + "　" + esc(f.zh) + '</h3><span class="coord">p.' + f.p + "・§" + f.sec.slice(1) + "</span></div>" + figBody(f, true) + "</article>";
      }).join("");
  }
  function renderCalcs() {
    $("v-calcs").innerHTML = "<h1>數字核算</h1>" +
      '<p class="lede">報告給了很多占比、倍數與相對變化，卻很少給分母。這裡把關鍵數字重算一遍，每一項都寫出輸入、公式與假設。這些是本站算的，不是報告的數字。</p>' +
      D.calcs.map(function (n) {
        return '<article class="card item" id="n-' + n.id + '"><div class="hd"><span class="chip kcalc">' + n.id + "</span><h3>" + esc(n.title) + "</h3></div>" + calcBody(n, true) + "</article>";
      }).join("");
  }
  var GS = "";
  function renderGaps() {
    var b = function (v, t) { return '<button type="button" data-sev="' + v + '" aria-pressed="' + (GS === v) + '">' + t + "</button>"; };
    $("v-gaps").innerHTML = "<h1>報告沒說的事</h1>" +
      '<p class="lede">揭露缺口：報告沒有提供、但讀者需要才能判斷結論強度的東西。嚴重度是本站的判斷。沒說不等於沒做——這些是可查核性的缺口，不是指控。</p>' +
      '<div class="seg" role="group" aria-label="依嚴重度篩選">' + b("", "全部") + b("高", "高") + b("中", "中") + b("低", "低") + "</div>" +
      '<div id="gap-list"></div>';
    var list = function () {
      $("gap-list").innerHTML = D.gaps.filter(function (g) { return !GS || g.sev === GS; }).map(function (g) {
        return '<article class="card item" id="g-' + g.id + '"><div class="hd"><span class="chip kgap">' + g.id + "</span><h3>" + esc(g.title) + "</h3></div>" + gapBody(g) + "</article>";
      }).join("");
    };
    document.querySelectorAll("[data-sev]").forEach(function (btn) {
      btn.onclick = function () {
        GS = btn.getAttribute("data-sev");
        document.querySelectorAll("[data-sev]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === btn)); });
        list();
      };
    });
    list();
  }
  function renderLit() {
    var cnt = {}; D.lit.forEach(function (l) { cnt[l.verdict] = (cnt[l.verdict] || 0) + 1; });
    $("v-lit").innerHTML = "<h1>文獻：報告怎麼用每一筆引用</h1>" +
      '<p class="lede">報告列了 10 筆文獻，另有一筆只出現在連結、沒列進文獻表。本站逐一回到原頁核對報告的轉述是否忠實，並補上一篇高度相關、報告卻沒引用的外部研究。' +
      "其中 Anthropic 自家的文件占了一大半，三篇與本報告有共同作者。</p>" +
      '<p class="small">' + Object.keys(VD).map(function (k) { return '<span class="vd ' + k + '">' + VD[k] + "</span> " + (cnt[k] || 0); }).join("　") + "</p>" +
      D.lit.map(function (l) {
        return '<article class="card item" id="l-' + l.id + '"><div class="hd"><h3>' + esc(l.cite) + "</h3></div>" + litBody(l) + "</article>";
      }).join("");
  }
  function renderMethod() {
    var s = D.stats, m = D.meta;
    $("v-method").innerHTML = "<h1>方法與限制</h1>" +
      '<div class="callout warn">' + esc(m.coi) + "</div>" +
      '<div class="callout note">' + esc(m.disclaimer) + "</div>" +
      "<h2>為什麼不放原文</h2><p>" + esc(m.rights_note) + "</p>" +
      "<p>替代做法是「原文定位」：每一則主張附一個網址，打開 Anthropic 官方網頁時，瀏覽器會捲到並標亮那一句（Text Fragment）。網址裡只帶一小段定位片語（不超過 7 個英文字），" +
      "建置時逐一核對它同時出現在 PDF 該段與官方網頁版（" + s.web + " 個）。另附 PDF 頁碼連結。</p>" +
      "<h2>核對是機械化的</h2><ul>" +
      "<li>報告數字：每一則主張引用的數字，都核對它確實出現在所標的段落，前後不能黏著別的數字（" + s.nums + " 個）。</li>" +
      "<li>圖內標示：只印在圖上的終點數字，用 300 DPI 影像裁出圖框後以 OCR 核對（" + s.figlabels + " 次比對）。</li>" +
      "<li>讀圖數值：目測放大後依座標軸換算，一律標「讀圖」，不進機械核對（" + s.read + " 個）。</li>" +
      "<li>lint：站上中文裡出現的每一個數字，都必須在資料層宣告來處（報告原文、圖內標示、讀圖、自算或外部文獻），否則建置中止。</li>" +
      "<li>著作權：站上任何字串若與報告全文有連續 8 個英文字相同，除了標題、章節名、圖題、文獻題名與唯一一句引文之外，建置中止。</li>" +
      "<li>出處：本機 PDF 與官方 CDN 的檔案逐位元相同；" + esc(m.provenance.web_vs_pdf) + "</li></ul>" +
      '<div class="callout note">這些核對保證「數字確實印在那裡」，不保證我把它讀對了意思。轉述、評等與評析是判斷，可以不同意——所以每一則都附原文定位，讓你三秒內回到原句挑戰它。</div>' +
      "<h2>證據等級</h2><p>" + esc(D.grade_note) + "</p>" +
      '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>等級</th><th>意思</th><th>則數</th></tr></thead><tbody>' +
      D.grades.map(function (g) {
        var n = D.claims.filter(function (c) { return c.grade === g.k; }).length;
        return "<tr><td>" + gradeBadge(g.k) + "</td><td>" + esc(g.d) + "</td><td>" + n + "</td></tr>";
      }).join("") + "</tbody></table></div>" +
      "<h2>主張類型與資料來源</h2>" +
      '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>類型</th><th>意思</th></tr></thead><tbody>' +
      D.types.map(function (t) { return "<tr><td>" + esc(t.zh) + "</td><td>" + esc(t.d) + "</td></tr>"; }).join("") + "</tbody></table></div>" +
      '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>資料來源</th><th>內容</th><th>則數</th></tr></thead><tbody>' +
      D.sources.map(function (x) {
        var n = D.claims.filter(function (c) { return c.src.indexOf(x.k) >= 0; }).length;
        return "<tr><td>" + esc(x.zh) + "</td><td>" + esc(x.d) + "</td><td>" + n + "</td></tr>";
      }).join("") + "</tbody></table></div>" +
      "<h2>哪些是報告的、哪些是本站的</h2>" +
      '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>層</th><th>來源</th><th>怎麼看待</th></tr></thead><tbody>' +
      "<tr><td>數字、段落座標、圖內標示</td><td>報告</td><td>機械核對過出現位置</td></tr>" +
      "<tr><td>「報告說了什麼」</td><td>報告內容，本站轉述</td><td>AI 協助整理，可能有誤，以原文為準</td></tr>" +
      "<tr><td>評析、證據等級、論證鏈</td><td>本站的判斷</td><td>標準公開，可以不同意</td></tr>" +
      "<tr><td>讀圖數值、重畫的圖</td><td>本站目測</td><td>估計值，標「讀圖」</td></tr>" +
      "<tr><td>數字核算</td><td>本站計算</td><td>公式與假設都寫出來</td></tr>" +
      "<tr><td>文獻核對</td><td>回原頁讀取（2026-10-19）</td><td>只記錄核對到的內容；未取得的標「未核對」</td></tr>" +
      "<tr><td>法律對照</td><td>美國聯邦與加州官方來源、歐盟 AI 法、台灣全國法規資料庫</td><td>條文逐字；對應關係是本站的判斷，不是法律意見</td></tr>" +
      "</tbody></table></div>" +
      "<h2>已知限制</h2><ul>" +
      "<li><b>單一來源的報告。</b>報告的數字都來自 Anthropic 內部，本站只能核對「報告寫了什麼」，不能核對「事實是否如此」。</li>" +
      "<li><b>讀圖有誤差。</b>重畫的圖與讀圖數值是估計；對數刻度與小圖的誤差較大。</li>" +
      "<li><b>文獻核對只到摘要或公開頁面。</b>沒有逐頁讀完每一篇引用文獻。</li>" +
      "<li><b>法律對照不是法律意見。</b>只指出報告的做法在哪些規範下要注意，沒有就任何事實做結論。</li></ul>" +
      "<h2>重建方式</h2><p>資料層在 <code>tools/data_*.py</code>。原報告不在 repo 裡：先自行下載 PDF，然後依序執行 " +
      "<code>python tools/extract.py 報告.pdf</code>、<code>python tools/fetch_web.py</code>、<code>python tools/ocr_figs.py</code>（需要 poppler、PyMuPDF、Tesseract），" +
      "產物在 <code>source/</code>，已列入 .gitignore。最後 <code>python tools/build.py</code> 產出 <code>index.html</code> 與 <code>report.md</code>；任何一項核對不通過就不會產出。</p>" +
      "<h2>詞彙</h2><dl class=\"kv\" style=\"grid-template-columns:9em minmax(0,1fr)\">" +
      D.glossary.map(function (g) { return "<dt><b>" + esc(g.t) + '</b><br><span class="small en">' + esc(g.en) + "</span></dt><dd>" + md(g.d, true) + "</dd>"; }).join("") + "</dl>" +
      '<p class="small muted">建置日期 ' + esc(s.built) + "。</p>";
  }
  function renderAbout() {
    var m = D.meta;
    $("v-about").innerHTML = "<h1>關於</h1>" +
      '<p class="lede">這是一名台灣法律工作者替自己做的報告分析筆記。做它的理由：這份報告講的是 AI 怎麼改變一家公司的就業，其中有法務的資料點、有招募標準的轉向，' +
      "也有一段值得法律人細讀的政策建議；而它最重要的數字（占比、倍數、相對變化）線性讀一次很容易讀錯意思。</p>" +
      "<h2>報告</h2><p>" + esc(m.authors.join("、")) + "。<span class=\"en\">" + esc(m.title_en) + "</span>。" + esc(m.institution) + "，" + esc(m.doc_type) + "，" + esc(m.date) + "。</p>" +
      '<p class="src-links">' + ext(m.url_web, "原文網頁") + ext(m.url_pdf, "原文 PDF") + "</p>" +
      "<h2>作者</h2><p>蔡宗穎（Camus Tsai）。台灣 IP 法律人，專利訴訟／SEP-FRAND／AI 工作流。" + ext("https://cecefat.github.io/cv/", "線上履歷") + "。</p>" +
      "<p>這個站的做法：我訂定流程與驗證規則（逐段座標、數字機械核對、讀圖必須標示、不轉載原文），程式、資料整理與分析初稿由 Claude（AI）撰寫。" +
      "Claude 是 Anthropic 的模型，而這份報告是 Anthropic 的出版品——這是利益衝突，見「方法」頁的揭露。</p>" +
      "<h2>同一套做法的其他站</h2><ul>" +
      "<li>" + ext("https://cecefat.github.io/ai-misuse-lex/", "AI 濫用威脅圖譜") + "　Anthropic 威脅情報報告的中文索引。</li>" +
      "<li>" + ext("https://cecefat.github.io/claude-sysprompt-study/", "Claude 系統提示詞演變自學站") + "　公開 system prompt 的 changelog 與證據包。</li>" +
      "<li>" + ext("https://cecefat.github.io/rlhf-lex/", "RLHF 知識圖譜") + "　一本 RLHF 專書的概念、公式與檢核題。</li>" +
      "<li>" + ext("https://cecefat.github.io/ukipo-lex/", "英國 SEP／FRAND 因子知識圖譜") + "　英國判決的因子字典、矩陣與教義圖譜。</li></ul>" +
      "<h2>與 Anthropic 的關係</h2><p>沒有關係。本站不是 Anthropic 的出版品，未經其審閱或背書。" + esc(m.rights_note) + "</p>" +
      '<p class="small muted">' + esc(m.copyright) + "（原報告）。</p>" +
      '<p class="small muted">建置日期 ' + esc(D.stats.built) + "。原始碼：" + ext("https://github.com/CeceFat/ai-employment-lex", "github.com/CeceFat/ai-employment-lex") + "</p>";
  }

  /* ---------------------------------------------------------------- 路由 */
  var VIEWS = [["report", "報告"], ["claims", "主張帳本"], ["figs", "八張圖"], ["calcs", "數字核算"], ["gaps", "報告沒說的"], ["lit", "文獻"], ["method", "方法"], ["about", "關於"]];
  var RENDER = { report: renderReport, claims: renderClaims, figs: renderFigs, calcs: renderCalcs, gaps: renderGaps, lit: renderLit, method: renderMethod, about: renderAbout };
  var rendered = {}, current = null;
  $("nav").innerHTML = VIEWS.map(function (v) { return '<a href="#' + v[0] + '" data-v="' + v[0] + '">' + v[1] + "</a>"; }).join("");

  function show(view, item) {
    if (!RENDER[view]) { view = "report"; item = null; }
    if (current !== view) {
      VIEWS.forEach(function (v) { $("v-" + v[0]).classList.toggle("on", v[0] === view); });
      document.querySelectorAll("#nav a").forEach(function (a) {
        if (a.getAttribute("data-v") === view) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
      });
      if (!rendered[view]) { CHARTS = CHARTS.filter(function (c) { return $(c.id); }); RENDER[view](); rendered[view] = true; }
      current = view;
      if (!item) window.scrollTo(0, 0);
    }
    drawCharts(); if (view === "report") drawChain();
    if (item) {
      var target = view === "report" ? $("r-" + item) || $("law-" + item)
        : $({ claims: "c-", figs: "f-", calcs: "n-", gaps: "g-", lit: "l-" }[view] + item);
      if (view === "claims" && !target) { F = { q: "", sec: "", grade: "", type: "", src: "", self: false }; renderClaims(); target = $("c-" + item); }
      if (target) {
        target.scrollIntoView({ block: "start" });
        if (target.classList.contains("claim") || target.classList.contains("item")) {
          target.classList.add("flash"); setTimeout(function () { target.classList.remove("flash"); }, 1800);
        }
      }
    }
  }
  function route() {
    var h = decodeURIComponent(location.hash.replace(/^#/, ""));
    if (h.indexOf("ref/") === 0) { if (!current) show("report"); openRef(h.slice(4)); return; }
    var parts = h.split("/");
    show(parts[0] || "report", parts.slice(1).join("/") || null);
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("[data-ref]");
    if (a) { ev.preventDefault(); openRef(a.getAttribute("data-ref")); return; }
    var inDrawer = ev.target.closest && ev.target.closest("#drawer a[href^='#']");
    if (inDrawer) closeDrawer();
  });
  $("scrim").addEventListener("click", closeDrawer);
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && !$("drawer").hidden) closeDrawer(); });
  window.addEventListener("hashchange", route);
  var rt = null;
  window.addEventListener("resize", function () {
    clearTimeout(rt);
    rt = setTimeout(function () {
      document.querySelectorAll(".chart[data-w]").forEach(function (el) { el.removeAttribute("data-w"); });
      drawCharts(); drawChain();
    }, 160);
  });

  /* 深淺色：存在 localStorage（可能被擋，失敗就只在本頁有效） */
  function setTheme(t) {
    if (t) document.documentElement.setAttribute("data-theme", t); else document.documentElement.removeAttribute("data-theme");
  }
  try { setTheme(localStorage.getItem("aelex-theme")); } catch (e) { /* 無痕或封鎖時略過 */ }
  $("theme").addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme");
    var dark = cur ? cur === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
    var next = dark ? "light" : "dark";
    setTheme(next);
    try { localStorage.setItem("aelex-theme", next); } catch (e) { /* 略過 */ }
  });

  $("foot").innerHTML = "獨立分析筆記，與 Anthropic 無關；不含報告全文。原報告 " + esc(D.meta.copyright) + "。分析初稿由 AI 撰寫，可能有誤，請以原文為準。建置 " + esc(D.stats.built) + "。　" +
    '<a href="#method">方法與限制</a>　<a href="#about">關於</a>　' + ext("https://github.com/CeceFat/ai-employment-lex", "原始碼");
  route();
})();
