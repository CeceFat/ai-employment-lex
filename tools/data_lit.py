# -*- coding: utf-8 -*-
"""文獻（報告怎麼用每一筆引用、我回原頁核對到什麼）與台灣法對照。

文獻的 facts 是我回原頁核對過的內容，用自己的話寫；數字列在 ext_nums，
claims 的 ext 欄位引用這些數字時，verify.py 會檢查數字確實列在這裡。
核對日期一律 2026-10-19（以 curl 取回原頁文字後逐字比對；SSRN 頁面拒絕存取，改用作者網站上的 PDF）。
"""

LIT = [
    dict(id="acemoglu", short="Acemoglu & Restrepo 2019", cite="Acemoglu & Restrepo (2019)",
         title="Automation and New Tasks: How Technology Displaces and Reinstates Labor",
         venue="Journal of Economic Perspectives 33(2): 3–30", kind="外部・期刊", inworks=True,
         used="p.18，「so-so」自動化", url="https://doi.org/10.1257/jep.33.2.3",
         checked="AEA 文章頁摘要",
         facts="以「任務」為單位的架構：自動化讓資本接手原本由人做的任務（取代效果），新任務把工作帶回給人（恢復效果）。",
         fidelity="忠實。報告「優先再配置會逼公司去找新任務」的論點，正是這個架構的恢復效果。「so-so」一詞不在摘要裡，本站未核對全文。",
         verdict="ok", ext_nums=[]),
    dict(id="beraja", short="Beraja & Zorzi 2025", cite="Beraja & Zorzi (2025)", title="Inefficient Automation",
         venue="Review of Economic Studies 92(1): 69–96", kind="外部・期刊", inworks=True,
         used="p.18，「inefficient」自動化", url="https://academic.oup.com/restud/article-abstract/92/1/69/7612958",
         checked="未核對（出版社頁面拒絕存取）",
         facts="本站只記錄報告怎麼用它：與「so-so」並列，指 AI 只勉強勝過人、被取代者承受重大所得損失、生產力卻只多一點點的自動化。",
         fidelity="未核對。", verdict="unchecked", ext_nums=[]),
    dict(id="demirer", short="Demirer 等 2026", cite="Demirer, Musolff & Yang (2026)",
         title="Writing Code vs. Shipping Code: Productivity Effects Across Generations of AI Coding Tools",
         venue="NBER Working Paper w35275（2026 年 5 月，9 月修訂）", kind="外部・工作論文", inworks=True,
         used="p.8，「business impact」", url="https://www.nber.org/papers/w35275",
         checked="NBER 論文頁摘要",
         facts="50 萬名以上 GitHub 開發者加上 AI 使用遙測：自動補完、互動式 coding agent、自主式 coding agent 讓 commit 分別累計增加 30%、180%、240%；"
               "但沿生產鏈大幅縮水，240% 的效果到「專案數」剩 80%、到「實際發布」剩 30%。",
         fidelity="報告引它提醒「程式碼多不等於商業影響」，忠實。但報告自己的產出指標（圖 3、圖 4）仍停在 commit 與新增程式碼這一層，沒有往發布或商業結果走。",
         verdict="ok", ext_nums=["50", "30", "180", "240", "80"]),
    dict(id="ewens", short="Ewens & Giroud 2025", cite="Ewens & Giroud (2025)", title="Corporate Hierarchy",
         venue="NBER Working Paper w34162（2025 年 8 月，2026 年 9 月修訂）", kind="外部・工作論文", inworks=True,
         used="p.16，「AI-adopters」更扁平", url="https://www.nber.org/papers/w34162",
         checked="NBER 論文頁摘要",
         facts="用 1,810 萬份線上履歷為 3,454 家美國上市公司建立階層量測；公司採用 AI 之後，階層變得更扁平。",
         fidelity="支持「更扁平」。摘要沒有談初階就業——報告那半句由 Hosseini & Lichtinger 支撐。",
         verdict="ok", ext_nums=["1,810", "3,454"]),
    dict(id="rsi", short="Favaro & Clark 2026", cite="Favaro & Clark (2026)", title="When AI Builds Itself",
         venue="The Anthropic Institute", kind="Anthropic 內部", inworks=True,
         used="p.6，「automation of model training and research」", url="https://www.anthropic.com/institute/recursive-self-improvement",
         checked="Anthropic 網頁",
         facts="截至 2026 年 5 月，合併進 Anthropic 程式碼庫的程式碼有超過 80% 由 Claude 撰寫；文中並說，2026 年第二季每位工程師每天約 8 倍的程式碼行數，"
               "幾乎確定高估了真實的生產力增幅。",
         fidelity="一致。但它對「程式碼行數高估生產力」的保留，本報告沒有帶進來。",
         verdict="omits", ext_nums=["80", "8"]),
    dict(id="hitzig", short="Hitzig 等 2026", cite="Hitzig, Massenkoff, Lyubich, Zhang, Heller & McCrory (2026-06-16)",
         title="Agentic Coding and Persistent Returns to Expertise", venue="Anthropic", kind="Anthropic 內部", inworks=True,
         used="p.4，「other domain experts」", url="https://www.anthropic.com/research/claude-code-expertise",
         checked="Anthropic 網頁",
         facts="約 23.5 萬人、約 40 萬個互動式 Claude Code session（2025 年 10 月到 2026 年 4 月）：會產出程式碼的 session，軟體相關職業的驗證成功率 34%、其他職業 29%；"
               "效益主要來自「具備基本能力」，深度專精只多一點；完全沒有相關專業的人從同一個工具得到的少得多。作者自稱結果是初步的。",
         fidelity="支持「寫程式擴散到其他領域專家」。它「效益來自基本能力、不是深度專精」的發現，和本報告的招募變化方向一致（本站推論，見 H2）。"
                  "Massenkoff、McCrory 同時是本報告的作者。",
         verdict="ok", ext_nums=["23.5", "40", "34", "29"]),
    dict(id="hosseini", short="Hosseini & Lichtinger 2025", cite="Hosseini Maasoum & Lichtinger (2025)",
         title="Generative AI as Seniority-Biased Technological Change: Evidence from U.S. Résumé and Job Posting Data",
         venue="SSRN 5425555（本站核對 2026-05-06 版）", kind="外部・工作論文", inworks=True,
         used="p.16，「fewer entry-level」", url="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5425555",
         checked="作者網站上的 2026-05-06 版 PDF 摘要（SSRN 頁面拒絕存取）",
         facts="涵蓋 6,500 萬名勞工、28 萬家以上公司（2015–2025）的履歷資料：公司開始採用生成式 AI 後，初階就業相對未採用者急降，資深就業大致不變；"
               "集中在最受生成式 AI 影響的職業，主因是招募放緩而不是離職增加。",
         fidelity="忠實。", verdict="ok", ext_nums=["6,500", "28"]),
    dict(id="huang", short="Huang 等 2025", cite="Huang, Seethor, Durmus, Handa, McCain, Stern & Ganguli (2025-12-02)",
         title="How AI Is Transforming Work at Anthropic", venue="Anthropic", kind="Anthropic 內部", inworks=True,
         used="p.6，「surveying Anthropic engineers」", url="https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic",
         checked="Anthropic 網頁",
         facts="2025 年 8 月調查 132 名工程師與研究員、53 場深度訪談、20 萬份內部 Claude Code 紀錄：員工自述在 60% 的工作中使用 Claude、生產力提升 50%；"
               "Claude 協助的工作有 27% 是原本不會做的事。也記錄了擔憂：深層技能萎縮，以及「比較資淺的人比較少來問我問題」這類指導機會減少的現象。",
         fidelity="一致。但它記錄的技能萎縮與指導減少，本報告只在 §6¶3 一句帶過，沒有連到初階的發現。",
         verdict="omits", ext_nums=["132", "53", "20", "60", "50", "27"]),
    dict(id="kim", short="Kim & Koning 2026", cite="Kim & Koning (2026-06-09)", title="AI-Native Firms",
         venue="Harvard Business School Working Paper 26-090", kind="外部・工作論文", inworks=True,
         used="p.16，「AI-native start-ups」", url="https://www.hbs.edu/ris/Publication%20Files/26-090_96f92aa0-37d9-4789-beaa-5c0cb87a4032.pdf",
         checked="論文 PDF 摘要",
         facts="以 Y Combinator 與美國創投支持的新創為樣本：AI 原生公司比同產業同期的非 AI 新創規模小 25%，工程師占比高 13%，初階與經理人占比各低約 15%，"
               "層級約扁平半個職級，估值卻相當。",
         fidelity="忠實。", verdict="ok", ext_nums=["25", "13", "15"]),
    dict(id="roodman", short="Roodman & Massenkoff 2026", cite="Roodman & Massenkoff (2026)", title="An Evidence Review of Subsidized Job Training",
         venue="The Anthropic Institute Working Paper 2026-01", kind="Anthropic 內部", inworks=True,
         used="p.18，「retraining」", url="https://www.anthropic.com/research/reviewing-the-evidence-on-worker-retraining-programs",
         checked="Anthropic 網頁",
         facts="56 個美國隨機試驗的統合分析：職訓的效果正向但有限——每提供一個訓練名額，就業率約提高二到三個百分點、年收入約多 1,000 美元，成本約 13,000 美元；"
               "算進稅收與福利支出的節省，大致損益兩平。結論：若 AI 大規模取代勞工，現有的再訓練計畫很可能不夠。",
         fidelity="省略了關鍵限定。報告只用一個連結字支持「再訓練」政策，沒有提到自家回顧的結論是現有計畫很可能不夠。Massenkoff 同時是本報告的作者。",
         verdict="omits", ext_nums=["56", "1,000", "13,000"]),
    dict(id="gap", short="Sacher 等 2026", cite="Sacher, Cotter, Jones, Korinek & McCrory (2026-10-16)", title="The AI Expectations Gap",
         venue="The Anthropic Institute", kind="Anthropic 內部（未列入 Works cited）", inworks=False,
         used="p.10，「75% 對 28%」", url="https://www.anthropic.com/research/ai-expectations-gap",
         checked="Anthropic 網頁",
         facts="員工端：2026 年 8 月 9 日至 12 日的內部問卷，1,334 人、未加權、用滑桿作答。美國成人端：Morning Consult 8 月 11 日至 23 日的線上自選樣本，10,980 人、加權；"
               "這一題只用有工作的受訪者，作答是選區間再取中點。兩邊都是平均數：員工預期 2030 年 AI 能做 75% 的工作，美國勞工 28%。",
         fidelity="未列入 Works cited；轉述時沒有帶任何可比性限制（作答格式、樣本性質都不同，來源頁自己列了這些限制）。McCrory 同時是本報告的作者。",
         verdict="omits", ext_nums=["1,334", "10,980", "75", "28"]),
    dict(id="canaries", short="Brynjolfsson 等 2026", cite="Brynjolfsson, Chandar & Chen（2026 年 8 月版）",
         title="Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence",
         venue="Stanford Digital Economy Lab 工作論文", kind="外部・工作論文（本報告未引用）", inworks=False,
         used="—（本報告沒有引用）", url="https://digitaleconomy.stanford.edu/publications/canaries-in-the-coal-mine",
         checked="Stanford 網站上的 PDF 摘要（2026 年 8 月版）",
         facts="ADP 薪資資料到 2026 年 6 月：沒有證據顯示全面性的就業流失；但 AI 高曝露職業裡 22 到 25 歲的年輕勞工，就業比照低曝露同儕的走勢少了 19%，"
               "資深勞工沒有類似落差；主要經由減少雇用年輕人，而不是增加離職。作者強調這是描述性的早期指標，不是因果估計。",
         fidelity="與本報告的初階發現高度相關、而且是外部的大樣本資料，本報告沒有引用。",
         verdict="missing", ext_nums=["22", "25", "19"]),
]

