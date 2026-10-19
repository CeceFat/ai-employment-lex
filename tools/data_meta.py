# -*- coding: utf-8 -*-
"""書目、出處驗證、章節地圖、分類表（資料來源、主張類型、證據等級）。"""

META = dict(
    title_en="How Employment is Changing at Anthropic",
    title_zh="Anthropic 的就業正在怎麼變",
    authors=["Nathan Wilmers", "Regina Catipon", "Maxim Massenkoff", "Peter McCrory"],
    date="2026-10-16",
    institution="The Anthropic Institute",
    doc_type="Technical Report",
    web_label="Economics",
    pages=20, figures=8, footnotes=1, works_cited=10, interviews=17, acknowledged=26,
    # 敘述裡可以直接用的書目數字（頁數、圖數、註腳、文獻數、訪談數、致謝人數、網頁比對段落數、
    # 逐字引文字數、WARN 預告天數、引文上限字數、原文定位片語上限字數）
    nums_ok=["20", "8", "1", "10", "17", "26", "69", "49", "11", "60", "15", "7"],
    url_web="https://www.anthropic.com/research/employment-at-anthropic",
    url_pdf="https://www-cdn.anthropic.com/72628f1863c53432195db83279252dfd2cb53158/Employment%20at%20Anthropic.pdf",
    copyright="© 2026 Anthropic PBC",
    # 出處驗證（2026-10-19）：本機 PDF 與官方 CDN 回傳的 x-sanity-md5、Content-Length 完全相同
    provenance=dict(
        checked="2026-10-19",
        md5="299e6b0a713f57f40e272dabbe646108",
        bytes=2042091,
        web_vs_pdf="以段落為單位比對網頁版與 PDF：69 個可比段落中 49 段逐字相同；其餘 20 段的差異都是排版或文字潤飾"
                   "（例如重點發現的「6 to 1」網頁寫作「six to one」、Spiralling／Spiraling、連字號、引用格式），"
                   "沒有數字或主張不同。「三項特徵只標到第二」這一點網頁版與 PDF 相同。",
    ),
    # 全站唯一一句逐字引文（11 個英文字），出自 §2¶3；verify.py 逐字核對
    epigraph=dict(
        q="an army of Claudes, with every one asking for my attention",
        sec="S2", key="¶3", p=3,
        who="一位 Anthropic 工程師，報告 §2¶3 引述",
    ),
    disclaimer=(
        "本站是一名讀者替自己做的分析筆記，不是 Anthropic 的出版品，與 Anthropic 無關。"
        "中文敘述、評等與評論是 AI 協助整理的詮釋，可能有誤；每一則主張都附原文座標與「原文定位」連結，"
        "站上引用的報告數字在建置時經機械核對。請以原文為準，最終檢閱是使用人自己的責任。"
    ),
    coi=(
        "利益衝突揭露：本站的分析初稿由 Claude（Anthropic 的模型）撰寫，分析對象是 Anthropic 自己的報告。"
        "讀者應把這一點當成和報告本身的利益衝突同等的警訊。對策是把判斷攤開：評等標準公開、每一則主張都能一鍵回到原句、"
        "每一個重算都寫出公式與假設、所有讀圖數字都標「讀圖」。"
    ),
    rights_note=(
        "原報告 © 2026 Anthropic PBC，未附開放授權。因此本站不內嵌報告全文、不轉載圖表、不建逐字引文庫；"
        "全站只逐字引用一句 11 個英文字的訪談句，其餘都是用自己的話寫的分析，外加座標與連結讓你回到原文。"
        "原文請至 Anthropic 網站閱讀。"
    ),
)

# 章節地圖。web = 官方網頁版的錨點 id（2026-10-19 以瀏覽器確認）
SECTIONS = [
    dict(k="S0", en="Front matter", zh="封面", pages="1", web=None),
    dict(k="S1", en="Key Findings", zh="開場與重點發現", pages="2", web="key-findings"),
    dict(k="S2", en="Introduction", zh="導論", pages="2–3", web="introduction"),
    dict(k="S3", en="Labor demand at the frontier", zh="前沿的勞動需求", pages="3–5",
         web="labor-demand-at-the-frontier"),
    dict(k="S4", en="Is AI driving productivity increases at Anthropic?", zh="AI 是否推升生產力",
         pages="5–9", web="is-ai-driving-productivity-increases-at-anthropic"),
    dict(k="S5", en="Bottlenecks and process: new and old tasks in an AI-intensive workplace",
         zh="瓶頸與流程：AI 密集職場的新舊任務", pages="9–15",
         web="bottlenecks-and-process-new-and-old-tasks-in-an-ai-intensive-workplace"),
    dict(k="S6", en="What employers can do", zh="雇主能做什麼", pages="15–18", web="what-employers-can-do"),
    dict(k="S7", en="Suggested citation, Acknowledgements, Works cited", zh="書末（引用格式、致謝、文獻）",
         pages="19–20", web="works-cited"),
]

# 報告自述的資料來源（§2¶2 列了七類＋訪談），外加財務紀錄（註 1）與外部資料
SOURCES = [
    dict(k="hr", zh="人事紀錄", d="在職人數、新進、職缺、跨部門移動、職務類別"),
    dict(k="fin", zh="財務紀錄", d="營收（註 1：截至 2026 年 4 月的十二個月）"),
    dict(k="tele", zh="agent 遙測", d="session 數、agent 工時、閒置時間、輸出 token、常設指示"),
    dict(k="out", zh="產出指標", d="commit、新增程式碼、查詢、合約、成交、錄用、發票"),
    dict(k="survey", zh="員工調查", d="主管調查、生產力調查、開放題、AI 預期"),
    dict(k="comm", zh="內部通訊", d="Slack 公開頻道與討論串"),
    dict(k="cal", zh="行事曆", d="開會時間"),
    dict(k="hire", zh="招募評分卡", d="2024 年以來的面試評語"),
    dict(k="intv", zh="訪談", d="17 場員工訪談"),
    dict(k="ext", zh="外部資料", d="Google、Meta 的公開財報；其他研究"),
]

TYPES = [
    dict(k="desc", zh="描述", d="報告說「發生了什麼」——量了什麼、量到多少。"),
    dict(k="cause", zh="歸因", d="報告說「是 AI 造成的」或用了因果設計。"),
    dict(k="meas", zh="測量／方法", d="報告說明怎麼量、或自己點出方法限制。"),
    dict(k="anec", zh="訪談／案例", d="受訪者的說法或單一團隊的例子。"),
    dict(k="extrap", zh="外推", d="從 Anthropic 推到其他公司或整體經濟。"),
    dict(k="norm", zh="規範主張", d="報告說雇主或政府「應該」怎麼做。"),
]

GRADES = [
    dict(k="A", zh="直接量測", d="口徑清楚，報告說的就是它量的；描述層次的事實。"),
    dict(k="B", zh="量測有缺口", d="量測可信，但基期、單位、分母或定義有缺口；或有部分識別設計的因果估計。"),
    dict(k="C", zh="間接或有替代解釋", d="依賴自評、未揭露驗證的 LLM 編碼，或有明顯沒排除的替代解釋。"),
    dict(k="D", zh="軼事或規範", d="單一訪談、單一案例、推測或價值主張。不等於錯，而是這種證據形式撐不起普遍結論。"),
    dict(k="-", zh="方法或限制聲明", d="報告在說明自己的方法或限制，不是對世界的主張，不評等。"),
]

# 評等是我（本站）的判斷，不是報告的；這段文字會出現在方法頁
GRADE_NOTE = (
    "評等對象是「報告這句話本身主張到哪裡」，不是對作者的評價。同一個數字可能在描述層是 A、在歸因層是 C："
    "例如「初階技術職占比從 21% 降到 14%」是 A，但「這是 AI 造成的」是 C。評等是本站的判斷，標準如上，可以不同意。"
)
