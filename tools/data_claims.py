# -*- coding: utf-8 -*-
"""主張帳本：報告裡每一則可檢驗的主張，逐段拆解。

欄位
  id      L5 之類。K＝重點發現、I＝導論、L＝勞動需求、P＝生產力、B＝瓶頸與流程、H＝招募、E＝雇主
  sec,key 段落座標（對應 source/paras.json；key 是 ¶n、KF1–KF4、fig1–fig8、fn1）
  p       PDF 頁次
  type    desc／cause／meas／anec／extrap／norm（見 data_meta.TYPES）
  src     資料來源（見 data_meta.SOURCES）
  zh      報告說了什麼——我的轉述，不是翻譯
  note    我的評析
  grade   A／B／C／D／-（見 data_meta.GRADES）
  self    報告自己點出了這個限制
  refs    連到圖（fig1）、核算（N1）、缺口（G1）、文獻（lit:x）、法條（law:x）、其他主張

核對用欄位（verify.py 會逐一比對；不在網頁上顯示原文）
  nums    zh／note 裡引用的報告數字。字串＝必須出現在本段；[字串, "S4:fig2"]＝必須出現在指定段落
  fig     [圖內標示, "figN"]：只印在點陣圖上的終點標示，比對圖框 OCR
  read    讀圖數值（目視估計，標「讀圖」，不進機械核對）
  calc    我算出來的數字（公式見 data_checks.CALCS）
  ext     [數字, "lit:x"]：取自外部文獻的數字（已對原頁逐字核對，見 data_lit）
  anchors 本段必須出現的英文關鍵詞（核對座標用）
  web     「原文定位」用的 Text Fragment 片語：必須同時出現在本段與官方網頁版
"""

CLAIMS = [
    # ------------------------------------------------------------------ §1 開場與重點發現
    dict(id="K0", sec="S1", key="¶1", p=[2], type="extrap", src=[], grade="D",
         zh="報告的自我定位：Anthropic 位在 AI 採用前沿，可能是 AI 如何改變整體經濟的工作組織、招募與勞動需求的「領先指標」。",
         note="這是全篇外推的前提，不是發現。要成立，其他企業得在模型取得、人才組成、成長速度、持股文化上逐步趨近 Anthropic；"
              "作者自己在 §6¶7 也說許多做法無法複製到整體經濟。",
         refs=["E6", "G15"], anchors=["leading indicator"], web="could be a leading indicator"),
    dict(id="K1", sec="S1", key="KF1", p=[2], type="desc", src=["hr", "tele"], grade="B",
         zh="初階技術職在招募中的占比變小；同一期間，AI agent 的工時相對員工快速擴大，到 8 月，互動式 agent 的工時是員工的 6 倍。",
         note="兩件事是並列（原文用「同時發生」的句型），沒有主張因果。6 倍的口徑只含員工自己發動的互動式 session，"
              "人類工時以人數乘每週 40 小時計（圖 2 註）。",
         refs=["fig2", "N7"], nums=["6 to 1", ["40 hours", "S4:fig2"]],
         anchors=["smaller share of junior technical positions"], web="interactive AI agent hours outnumbered"),
    dict(id="K2", sec="S1", key="KF2", p=[2], type="cause", src=["out"], grade="B",
         zh="agent 擴散後，人均程式碼、每位業務的成交、合約處理量都上升；追蹤同一位員工，採用新 AI 工具後產出上升。",
         note="同一人前後比較（圖 4）只做了工程師與業務兩種職能；「合約處理量」只有描述性的時間序列（圖 3），沒有同一人比較。"
              "重點發現把兩種強度不同的證據放在同一句。",
         refs=["fig3", "fig4", "P6"], anchors=["processing more contracts", "same employee over time"],
         web="processing more contracts"),
    dict(id="K3", sec="S1", key="KF3", p=[2], type="meas", src=["tele"], grade="B",
         zh="加速讓人的注意力成為 agent 產出的瓶頸：即使是非技術員工，讀完自己 Claude agent 的全部輸出也要花掉半個工作週；"
            "員工因此轉向打造可視化工具、監控 agent 流程這類「後設工作」。",
         note="「半個工作週」是把輸出 token 換算成閱讀時數的示意指標（圖 6）。以圖 6 最後一個月計，5 個非技術群組中有 4 組超過 20 小時，"
              "行銷與公關只有 12 小時；改用前一個月，只剩 2 組超過（讀圖）。",
         refs=["fig6", "N6"], fig=[["12 h", "fig6"]], calc=["5", "4", "20", "2"],
         anchors=["half their work week", "meta-work"], web="half their work week"),
    dict(id="K4", sec="S1", key="KF4", p=[2], type="desc", src=["hire"], grade="C",
         zh="工作組織的改變也反映在招募主管的優先順序：愈來愈重視自主性與判斷力，相對降低技術領域專長與執行能力的比重。",
         note="來源是以自動編碼器處理的面試評分卡（§5¶15–16）。報告沒有給各類評語的占比，也沒說編碼器怎麼驗證。",
         refs=["H1", "H2", "G4"], anchors=["autonomy and judgment"], web="emphasize autonomy and judgment"),

    # ------------------------------------------------------------------ §2 導論
    dict(id="I1", sec="S2", key="¶1", p=[2], type="desc", src=["tele"], grade="B",
         zh="Anthropic 已把工作流程全面圍繞 AI 重塑：agent 穿梭在 Slack 對話裡、排會議、自主修 bug、協作大型工程；agent 的工時是人類的 6 倍。",
         note="這一句沒有標明口徑。對照重點發現與圖 2，6 倍指的是互動式 session（不含自主式）；加上自主式只會更高，所以不算誇大，"
              "但讀者在這裡無從得知口徑。",
         refs=["K1", "fig2"], nums=["6 to 1"], anchors=["thoroughly molded its workflows"],
         web="outnumber human hours"),
    dict(id="I2", sec="S2", key="¶2", p=[2], type="meas", src=["hr", "tele", "out", "survey", "comm", "cal", "hire", "intv"],
         grade="A",
         zh="資料來源：Anthropic 內部的就業、AI 使用、產出指標、員工調查、內部通訊型態、員工行事曆與招募決策紀錄七類，外加 17 場員工訪談。",
         note="七類資料都只在 Anthropic 內部，外界無法重製；訪談對象怎麼選、涵蓋哪些職能，報告沒有說明。",
         refs=["G15", "G16"], nums=["17"], anchors=["hiring decision records"], web="17 employee interviews"),
    dict(id="I3", sec="S2", key="¶3", p=[2, 3], type="cause", src=["hr", "out", "hire"], grade="B",
         zh="即使公司在成長，初階技術職的「相對」招募仍放緩；工程與非技術員工的生產力都在採用 coding agent 時急升；"
            "招募主管更重視自主與判斷，而不是特定技術專長。",
         note="作者在這裡用了「相對」——這個限定詞很關鍵：占比下降不等於人數減少（N1）。",
         refs=["N1"], anchors=["relative hiring"], web="relative hiring in junior technical positions"),
    dict(id="I4", sec="S2", key="¶3", p=[3], type="anec", src=["intv"], grade="D",
         zh="AI 密集組織的一個特徵，是不斷有壓力要把自己從瓶頸位置移開；一位工程師形容自己面對一整支 Claude 大軍，每一個都在爭取自己的注意力。"
            "作者的結論：員工仍然關鍵，但貢獻的性質變了。",
         note="全站唯一的逐字引文就是這一句（見頁首）。",
         refs=[], anchors=["an army of Claudes"], web="an army of Claudes"),
    dict(id="I5", sec="S2", key="¶4", p=[3], type="norm", src=[], grade="D",
         zh="Anthropic 的回應：建立追蹤「可能受衝擊職務」的預警系統，並在職務演變時優先內部轉調。作者也承認，這些承諾究竟該長什麼樣子，仍是難題。",
         note="預警系統的指標、門檻與治理方式都沒有揭露（§6¶9 只多說了一句：以職務層級的需求與生產力指標對照 AI 能力與使用），外界無法評估它是否有效。",
         refs=["E9", "G7"], anchors=["early warning system", "internal redeployments"],
         web="early warning system to track jobs"),

    # ------------------------------------------------------------------ §3 前沿的勞動需求
    dict(id="L1", sec="S3", key="¶1", p=[3, 18], type="extrap", src=["fin", "hr", "ext"], grade="C",
         zh="Anthropic 擴張很快，但每一元營收雇用的人比上一代大型科技公司少：成立五年時，每名員工營收是 Meta、Google 同齡時的 2–4 倍。"
            "依註 1，Anthropic 的數字取自截至 2026 年 4 月十二個月的內部財務與人事紀錄，Google（2003）與 Meta（2009）依 10-K，全部平減到 2025 年幣值。",
         note="三個問題。第一，只給倍數，沒給 Anthropic 的營收與人數，無法重算。第二，營收不等於附加價值：AI 實驗室的營收裡含大量算力成本，"
              "拿來跟 2003 年的 Google、2009 年的 Meta 比每人營收，口徑不同。第三，註 1 說 Google、Meta 的數字來自「成立 5 年時的 10-K」，"
              "但兩家當年都還沒上市（Google 2004 年、Facebook 2012 年才上市），那兩年沒有 10-K；數字應是取自日後 10-K 的歷年比較或 S-1。"
              "不影響方向，但出處寫得不精確。",
         refs=["G11", "G14"], nums=["2–4", ["5 years", "S6:fn1"], ["twelve months", "S6:fn1"]],
         anchors=["revenue per employee"], web="revenue per employee as Meta and Google"),
    dict(id="L2", sec="S3", key="¶2", p=[3], type="anec", src=["intv"], grade="D",
         zh="內部對「初階技術人力需求下降」的討論，2026 年 1 月始於核心技術部門：最倚重 Claude 的團隊發現寫程式與找 bug 可以愈來愈多交給 Claude；"
            "新模型加速了這個認知——一位受訪者說，效能工程師的能力提升幾乎一夜之間改變了他們要找的人。",
         note="時間點和圖 1 職缺占比自 2025 年 12 月起下滑大致吻合，但「討論出現」本身是組織敘事，不是量測。",
         refs=["fig1"], nums=["January 2026"], anchors=["performance engineers"], web="uplift for performance engineers"),
    dict(id="L3", sec="S3", key="¶3", p=[3], type="desc", src=[], grade="C",
         zh="到 4 月，工程與研究團隊已調低較低職等技術職的招募比重。",
         note="「較低職等」（lower band）沒有定義，也沒說這句的資料來源是招募計畫、職缺系統還是主管說法。",
         refs=["G17"], anchors=["lower band technical positions"], web="deemphasized hiring for lower band"),
    dict(id="L4", sec="S3", key="¶3", p=[3], type="cause", src=["survey"], grade="C",
         zh="同月的主管調查：多數主管表示因為 AI 而改找不同的技能組合；約三分之一的 ML 主管、五分之一的軟體工程主管表示因為 AI 而少招人。",
         note="主管自己判斷的因果。樣本數、回應率、題目措辭都沒有揭露；「多數」也沒給百分比。",
         refs=["G2", "G3"], anchors=["a third of ML", "a fifth of SWE"], web="Around a third of ML"),
    dict(id="L5", sec="S3", key="¶4", p=[3, 4], type="desc", src=["hr"], grade="A",
         zh="技術部門的初階員工占比，從 2025 年初的 21% 降到 14%。",
         note="這是「占比」。同一時期公司規模約成長為三倍，占比下降和初階人數增加可以同時成立：用報告自己的三個數字試算，"
              "初階技術員工的絕對人數約為原來的 1.84 倍（N1）。",
         refs=["N1", "fig1"], nums=["21%", "14%"], fig=[["14%", "fig1"]], calc=["1.84"],
         anchors=["junior-level employees in technical departments"], web="from 21% to 14%"),
    dict(id="L6", sec="S3", key="¶4", p=[3, 4], type="desc", src=["hr"], grade="A",
         zh="初階技術職的「新進」占比降得更快：從 27% 降到 9%。",
         note="要讓初階新進的「人數」不減，技術職新進總數得成長到 3 倍；報告沒給新進總數，所以無法判斷初階新進人數是增是減（N2）。"
              "圖 1 的新進線從 2025 年 5 月才開始，起點約 27.6%（讀圖）。",
         refs=["N2", "fig1"], nums=["27%", "9%"], fig=[["9%", "fig1"]], calc=["3"], read=["27.6"],
         anchors=["junior technical hires"], web="from 27% to 9%"),
    dict(id="L7", sec="S3", key="¶4", p=[3, 4], type="desc", src=["hr"], grade="A",
         zh="初階職缺自 2025 年 12 月起下降得特別急。",
         note="圖 1 技術部門的初階職缺占比在 2025 年 11 月達到約 21.4% 的高點，到 2026 年 6 月只剩 6%。"
              "非技術部門的初階職缺占比也從約 31.5% 降到 13%，而且主要降在 2025 年——本文完全沒有討論（N13、G9）。",
         refs=["fig1", "N13", "G9"], nums=["December 2025"], fig=[["6%", "fig1"], ["13%", "fig1"]], read=["21.4", "31.5"],
         anchors=["Postings for juniors"], web="particularly sharply since December 2025"),
    dict(id="L8", sec="S3", key="¶5", p=[4], type="desc", src=["hr"], grade="A",
         zh="技術部門占全公司就業的比重，一年內從 61% 降到 56%。",
         note="這是 N1 試算需要的第二個數字。",
         refs=["N1"], nums=["61%", "56%"], anchors=["employment share of technical departments"], web="from 61% to 56%"),
    dict(id="L9", sec="S3", key="¶5", p=[4], type="desc", src=["hr"], grade="B",
         zh="技術招募的絕對數仍在成長，只是業務、財務、招募部門的密集招募成長得更快。",
         note="報告自己承認技術招募的絕對數在成長——這是理解「占比下降」的關鍵，但沒有給數字。",
         refs=["N1", "G1"], anchors=["absolute terms"], web="continued growing in absolute terms"),
    dict(id="L10", sec="S3", key="¶5", p=[4], type="anec", src=["intv"], grade="D",
         zh="作者的解讀：一部分是公司規模擴大後業務功能的自然擴張；一部分可能是 coding 工具讓非技術員工自己做軟體——例如一位業務代表花三到四小時，"
            "自己做出量身訂做的儀表板與資料流程。",
         note="兩個解釋各占多少，沒有拆開。",
         refs=[], anchors=["three to four hours"], web="three to four hours"),
    dict(id="L11", sec="S3", key="¶5", p=[4], type="desc", src=["tele"], grade="B",
         zh="非技術員工（基準期沒有任何 commit、排除新進者）的 coding 類 agent session：2025 年 8 月每月 2 次，2026 年 5 月 90 次。",
         note="單位不明：是每人每月，還是整個群體每月？兩種讀法的意義差很多（N17）。",
         refs=["N17", "G17"], nums=["2 per month", "90"], anchors=["no code commits at baseline"],
         web="2 per month in August 2025"),
    dict(id="L12", sec="S3", key="¶6", p=[4], type="desc", src=["out", "hr"], grade="B",
         zh="技術部門裡「沒在寫程式」（前 30 天沒有 commit）的員工占比，在截至 2026 年 4 月的一年內幾乎減半。",
         note="沒給起點與終點的水準。",
         refs=["G2"], nums=["30 days"], anchors=["almost half"], web="fell by almost half"),
    dict(id="L13", sec="S3", key="¶6", p=[5], type="desc", src=["hr"], grade="A",
         zh="一部分原因是非工程師的比重變薄：例如工程師對產品經理約 17 比 1，且自 2025 年起持續上升。",
         note="", refs=[], nums=["17 to 1"], anchors=["product managers"], web="17 to 1"),
    dict(id="L14", sec="S3", key="¶6", p=[5], type="desc", src=["out"], grade="B",
         zh="主管的 commit 數也翻倍；技術團隊裡的督導與協調角色，愈來愈多是親自寫碼、出貨。",
         note="commit 數是程式碼活動量，不是產出價值。外部研究（Demirer 等人）發現 commit 的增幅傳到實際發布時大幅縮水。",
         refs=["lit:demirer"], anchors=["commits from managers has also doubled"], web="commits from managers has also doubled"),
    dict(id="L15", sec="S3", key="¶7", p=[5], type="desc", src=["hr", "intv"], grade="C",
         zh="通常隨公司規模擴張的行政職沒有加速招募：agent 助理、自動化審核，加上客服工單外包，讓公司在快速成長中仍維持「行政輕量」；"
            "一位財務經理自己做了採購申請審查 agent。",
         note="作者列出的三個原因裡，有一個是「外包」——那不是 AI 的效果。三者各占多少沒有拆開。",
         refs=[], anchors=["clerical-light", "ticket service outsourcing"], web="clerical-light"),
    dict(id="L16", sec="S3", key="¶8", p=[5], type="anec", src=["intv"], grade="D",
         zh="即使與面對面互動緊密相關的文書工作也成長緩慢：一位行政助理自建排程與 email 分流 agent，認為最入門的行政角色已被 Claude 取代，"
            "自己轉做較高階的「幕僚長」型工作。",
         note="", refs=[], anchors=["executive assistant"], web="chief of staff"),
    dict(id="L17", sec="S3", key="¶9", p=[5], type="desc", src=["hr"], grade="B",
         zh="再配置已經發生：在職滿一年的員工，2026 年每月跨部門移動的機率比 2025 年高 50%。",
         note="相對增幅，沒給基準率。舉例：若原本每月 1% 的人換部門，提高 50% 也只是 1.5%（N10，示意）。",
         refs=["N10", "G2"], nums=["50%"], calc=["1", "1.5"], anchors=["move across departments"],
         web="50% more likely to move across departments"),
    dict(id="L18", sec="S3", key="¶9", p=[5], type="anec", src=["intv"], grade="D",
         zh="整個團隊也可能因為把工作交給 agent 而被重新配置：一個撰寫 Claude.ai 問候語等產品文案的設計團隊，2026 年春建立了能引導 agent 寫出好文案的 context graph，"
            "之後轉做 agent prompting、撰寫模型評測與 prompt。",
         note="一個團隊的案例，說明「再配置」長什麼樣子，不能推論為普遍模式。",
         refs=[], anchors=["context graph"], web="context graph"),

    # ------------------------------------------------------------------ §4 AI 是否推升生產力
    dict(id="P1", sec="S4", key="¶1", p=[5], type="desc", src=["tele"], grade="B",
         zh="依 agent session 遙測，2026 年 3 月，自主式加互動式 agent 的工時總和首度超過人類工時。",
         note="自主式 session 的工時怎麼算，報告沒說明（圖 2 註只定義了互動式）。圖 2 只看互動式，全體員工那條線約在 5 月初才越過平價線（讀圖），"
              "兩者並不矛盾。",
         refs=["fig2", "N11"], nums=["March 2026"], anchors=["autonomous and interactive agent work hours"],
         web="leapt past human work hours"),
    dict(id="P2", sec="S4", key="¶1", p=[5, 6], type="desc", src=["tele"], grade="C",
         zh="其中一部分來自大批 agent 從事工業規模的軟體工程：補例行測試與檢查、維護不斷膨脹的基礎設施程式碼、大規模轉譯 codebase。",
         note="", refs=[], anchors=["translate massive codebases"], web="translate massive codebases"),
    dict(id="P3", sec="S4", key="¶1", p=[6], type="meas", src=["tele", "hr"], grade="B",
         zh="只看員工個人部署的 agent（圖 2），到 8 月，agent 的工時是人類的 6 倍；圖中研究組織是 19 倍。",
         note="口徑（圖 2 註）：只含員工發動的互動式 session，子 agent 合併計算；agent 工時是推論與工具執行的時間，但排除超過 30 分鐘的等待；"
              "人類工時是人數乘每週 40 小時（假設值）。三個地方會把比值推高：平行子 agent 的時間是相加的；一個 agent 小時不等於一個人類小時的工作量；"
              "人類若實際每週工作超過 40 小時，分母就被低估（每週 50 小時時，6 倍變 4.8 倍，N7）。",
         refs=["fig2", "N7", "N11"], nums=["6 times", ["30 minutes", "S4:fig2"], ["40 hours", "S4:fig2"]],
         fig=[["19×", "fig2"], ["6×", "fig2"]], calc=["50", "4.8"],
         anchors=["human handlers"], web="6 times as many hours"),
    dict(id="P4", sec="S4", key="¶2", p=[6], type="desc", src=["tele"], grade="C",
         zh="Anthropic 是軟體公司，流經 agent 的 token 絕大部分用來產出程式碼；但個人助理 agent 也監看行事曆與訊息、排程、彙整待辦，並在會前自動簡報與會者與會議目的。",
         note="", refs=[], anchors=["personal assistant agents"], web="vast bulk of tokens"),
    dict(id="P5", sec="S4", key="¶3", p=[6, 7], type="desc", src=["out"], grade="B",
         zh="每位工程師的 commit 數成長最快，是 6 個月前的 5 倍（圖 3 標示 5.1 倍）。",
         note="commit 是活動量指標。報告引用的同公司文章（Favaro & Clark）自己就說，以程式碼行數衡量的 8 倍幾乎確定高估了真實生產力；"
              "外部的 Demirer 等人發現 commit 增幅傳到實際發布時大幅縮水（240% 到 30%）。另外，圖 3 以 2025 年 12 月為 100，"
              "commit 線在基期前已從約 59 漲到 100（讀圖），倍數對基期的選擇很敏感（N12）。",
         refs=["fig3", "N12", "lit:rsi", "lit:demirer"], nums=["5x", "6 months"], fig=[["5.1×", "fig3"], ["100", "fig3"]],
         read=["59"], ext=[["8", "lit:rsi"], ["240", "lit:demirer"], ["30", "lit:demirer"]],
         anchors=["commits per engineer have risen the fastest"], web="commits per engineer have risen the fastest"),
    dict(id="P6", sec="S4", key="fig3", p=[7], type="desc", src=["out"], grade="B",
         zh="圖 3 其他職能（以 2025 年 12 月為 100）：資料科學家的查詢 3.1 倍、法務人員處理的合約 3.1 倍、業務成交 1.7 倍、招募人員錄用 1.4 倍、應付帳款處理的發票 1.4 倍。",
         note="這是描述性時間序列，經 loess 平滑。業務、招募與法務的量都和公司業務爆炸成長高度相關（作者在 §4¶4 自己承認）。"
              "招募人員的指數在 2025 年 7 月已約 128（讀圖），相對當時只多約 9%。法務「合約 3.1 倍」沒有任何同一人比較或品質指標。",
         refs=["fig3", "N12", "G12"], fig=[["3.1×", "fig3"], ["1.7×", "fig3"], ["1.4×", "fig3"], ["100", "fig3"]],
         read=["128"], calc=["9"], anchors=["Loess"], web="Productivity boom across functions"),
    dict(id="P7", sec="S4", key="¶3", p=[7], type="desc", src=["out"], grade="C",
         zh="資料科學家要 Claude agent 即時把指標送上儀表板；非技術員工的產出也隨 coding agent 擴散而上升：律師處理更多合約、應付帳款處理更多發票、業務成交更多。",
         note="", refs=["P6"], anchors=["lawyers processed more contracts"], web="lawyers processed more contracts"),
    dict(id="P8", sec="S4", key="¶4", p=[7], type="meas", src=[], grade="-", self=True,
         zh="作者自承：同期公司業務爆炸成長（好模型好賣），所以改用「已採用 vs 尚未採用 agent 工具」的同月員工比較來估 AI 的獨立效果；"
            "並承認採用時點不是隨機的——例如即將啟動大專案的人先把工具備齊，就會讓估計偏誤。",
         note="這是全篇方法上最誠實的一段：點名了最主要的替代解釋（業務成長）與最主要的偏誤來源（自選採用時點）。",
         refs=["fig4"], anchors=["explosive business growth", "tool adoption is not random"],
         web="tool adoption is not random"),
    dict(id="P9", sec="S4", key="¶5", p=[8], type="cause", src=["out", "tele"], grade="B",
         zh="追蹤 192 名採用 coding agent 的工程師，對照 74 名在研究期間都沒採用的工程師；採用後幾個月，工程師新增的程式碼量急升。",
         note="讀圖：採用當月約 +0.98、第一個月 +1.31、第二個月 +1.85、第三個月 +1.01 對數點；若是自然對數差，約等於 2.7、3.7、6.4、2.7 倍（N3）。"
              "採用前四個月接近 0，前趨勢平坦——這是這個面板可信的地方。限制有三：結果變數是「新增程式碼」，不是價值；"
              "對照組只有 74 人、約占樣本的 28%（N15），而且是「到最後都沒採用」的人，本身可能就不同；"
              "交錯採用搭配雙向固定效果，在處理效果因人因時而異時有已知偏誤，報告沒說用的是哪種估計式。",
         refs=["fig4", "N3", "N15", "G3"], nums=["192", "74"], read=["0.98", "1.31", "1.85", "1.01"],
         calc=["2.7", "3.7", "6.4", "28"], anchors=["192 engineers"], web="We follow 192 engineers"),
    dict(id="P10", sec="S4", key="¶5", p=[8, 9], type="cause", src=["out"], grade="B",
         zh="為檢驗「AI 垃圾碼」，比較同一人、同一個月、同一個目錄裡，由 coding agent 寫的與本人直接寫的程式碼——後續被刪除或回退的比率沒有差異。",
         note="設計很聰明：同人、同月、同目錄，排除了人與專案的差異。但「沒有顯著差異」不等於「證明一樣好」：6 個指標的信賴區間寬窄不一，"
              "例如新增 lint 抑制約 −2 到 +1.9 個百分點、被 bug-fix 刪除約 −0.6 到 +2.1（讀圖），而報告沒給各指標的基準率，無從判斷區間算寬還是窄。"
              "「明確回退」那一列的區間下緣在讀圖上與 0 重疊，屬臨界。90 天的觀察窗也看不到長期維護成本。",
         refs=["fig4", "G2"], nums=[["90 days", "S4:fig4"]], read=["2", "1.9", "0.6", "2.1"], calc=["6"],
         anchors=["AI code slop", "same coding directory"], web="To test for AI code slop"),
    dict(id="P11", sec="S4", key="¶6", p=[9], type="cause", src=["out", "tele"], grade="A", self=True,
         zh="改看工程師採用第一個「全自主」agent 的前後：採用者在採用前就已處於陡升軌跡——轉向全自主 agent 的人，本來就在加速產出。",
         note="讀圖：採用前第四個月約 −0.43、第三個月 −0.37、第二個月 −0.22 對數點，信賴區間都不含 0。從採用前第四個月到採用當月總共升了約 0.72，"
              "其中約 0.43（六成）發生在採用之前（N3）。所以這個面板不能當成 AI 效果的證據——報告自己也這麼說。",
         refs=["fig4", "N3"], read=["0.43", "0.37", "0.22"], calc=["0.72", "0.43"],
         anchors=["steeply upward trajectory"], web="already on a steeply upward trajectory"),
    dict(id="P12", sec="S4", key="¶7", p=[9], type="cause", src=["out"], grade="C", self=True,
         zh="業務代表自「去年 9 月」（應指 2025 年 9 月）起陸續採用 agent；採用後成交的客戶數增加。作者承認，這可能是「機會多的業務比較會去自動化」的自選效果，"
            "也可能是記錄與例行溝通被自動化的結果。",
         note="讀圖：採用後第一、二、三個月，每月成交客戶比採用前一個月多約 3.0、5.6、6.6 位，但報告沒給業務原本每月成交幾位客戶，無法換算成百分比。"
              "採用前的係數在 0 附近（前第四個月約 −1.2，信賴區間含 0），前趨勢大致平坦；自選問題作者自己點了名，但無法排除。",
         refs=["fig4", "G2"], read=["3.0", "5.6", "6.6", "1.2"], anchors=["starting last September", "selecting into automation"],
         web="selecting into automation"),
    dict(id="P13", sec="S4", key="¶7", p=[9], type="anec", src=["intv"], grade="D",
         zh="一位客戶經理說，Claude 自動化處理 email 草擬與客戶管理軟體整合，取代了約 20% 原本的工作任務；另一位說省下的時間拿去面對面，接觸的客戶多了 30%。",
         note="受訪者自估，不是量測。", refs=[], nums=["20%", "30%"], anchors=["account executive"],
         web="replacing around 20% of their prior"),
    dict(id="P14", sec="S4", key="¶8", p=[9], type="anec", src=["intv"], grade="D",
         zh="一位 Anthropic 律師用 Claude 建了一系列自動化：掃描風險與機會、分流法律問題、對外文案的法務初審。一位招募人員用 Claude 做人選搜尋、申請追蹤，"
            "以及一份原本要「大概幾週」的分析，騰出時間重寫過時的面試題目、見更多應徵者。",
         note="對法務讀者最相關的一段，但只是個案描述（見「法務意涵」）。",
         refs=[], anchors=["triage legal questions"], web="triage legal questions"),
    dict(id="P15", sec="S4", key="¶9", p=[9, 10], type="desc", src=["hr", "tele"], grade="B",
         zh="描述性地看，把 Claude 用在最複雜任務的職務，初階就業放緩（圖 5）。圖 5 以職務為單位：橫軸是該職務 Claude 任務的複雜度百分位"
            "（以 2025 年 10 月到 12 月的 agent 紀錄自動編碼），縱軸是 2026 年 1 月到 7 月初階在職人數的成長（對數點），迴歸線依人數加權。",
         note="讀圖：共 32 個職務，21 個的初階人數在半年內增加、2 個持平、9 個減少；加權迴歸線約在第 77 百分位才穿過 0。"
              "換句話說，多數職務的初階人數還在長，只是複雜度愈高的職務長得愈慢——依迴歸線，位在第 25 百分位的職務半年內初階人數約翻倍，"
              "第 75 百分位約持平（N14）。複雜度在結果期之前量測，避開了反向因果，這是設計上的優點；但沒有其他控制變數，"
              "複雜度高的職務可能本來就偏好資深人力。",
         refs=["fig5", "N14", "G3"], read=["32", "21", "2", "9", "77"], anchors=["Descriptively"],
         web="Descriptively, we see junior employment slowing"),

    # ------------------------------------------------------------------ §5 瓶頸與流程
    dict(id="B1", sec="S5", key="¶1", p=[9, 10], type="anec", src=["intv"], grade="D",
         zh="大量採用 AI 不只改變就業與生產力，也持續改變工作流程：員工形容公司有一股要盡可能快、凡事用 Claude 的「永恆壓力」，"
            "也有人說，這裡一週要完成的事，在別處要三個月。",
         note="壓力有被引述，卻沒有任何福祉或倦怠的量化指標（G13）。", refs=["G13"], anchors=["eternal pressure"],
         web="eternal pressure at Anthropic"),
    dict(id="B2", sec="S5", key="¶1", p=[10], type="desc", src=["survey"], grade="B", self=True,
         zh="內部調查問「公司的工作流程是否讓你盡可能有生產力」：同意者 2024 年底 44%、2025 年 11 月 58%；2026 年 4 月是 75%，但題目拿掉了「盡可能」，變得比較好答。",
         note="可比的只有 44% 到 58%（同一題，多了 14 個百分點，N8）。75% 換了題目，作者自己標註了，但仍放在同一句，讀者很容易把三個數字連成一條線。",
         refs=["N8"], nums=["44%", "58%", "75%"], calc=["14"], anchors=["as possible"], web="44% of employees agreed in late 2024"),
    dict(id="B3", sec="S5", key="¶1", p=[10], type="extrap", src=["survey", "ext"], grade="C",
         zh="截至 8 月，Anthropic 員工預期到 2030 年 AI 能做他們 75% 的工作，其他美國人則是 28%。",
         note="這句的連結指向同日發表的〈The AI expectations gap〉，但那篇沒有列進 Works cited。依該頁：員工端是 2026 年 8 月 9 日至 12 日的內部問卷，"
              "1,334 人、未加權、用滑桿作答；美國成人端是 Morning Consult 在 8 月 11 日至 23 日做的線上自選樣本，10,980 人、加權，作答是選區間再取中點；"
              "兩邊都是平均數。作答格式不同、樣本性質不同，該頁自己列了這些限制，本報告轉述時一個都沒帶。",
         refs=["lit:gap", "G14"], nums=["75%", "28%", "2030"], ext=[["1,334", "lit:gap"], ["10,980", "lit:gap"]],
         anchors=["other Americans"], web="compared to 28% for other Americans"),
    dict(id="B4", sec="S5", key="¶2", p=[10, 11], type="meas", src=["tele"], grade="C",
         zh="每次內部發布新模型，員工就在互動式 coding session 裡挑戰更難的問題。以 Claude 評分器，依深度、範圍、牽涉的系統數評估去識別化 session 的任務難度："
            "超過舊模型第 90 百分位難度的任務占比上升約 30%（從 10% 到 13%），並在發布後數週維持高檔；簡單端幾乎沒變。",
         note="「急升約 30%」是相對增幅，絕對增幅是 3 個百分點（N5）。評分器是 Claude，報告沒說是哪個模型版本、有沒有人工驗證；"
              "若評分器就是新模型，「新模型讓任務變難」這個量測就可能有自己評自己的循環性（G4）。",
         refs=["N5", "G4"], nums=["90th", "30%", "10%", "13%"], calc=["3"], anchors=["automated Claude grader"],
         web="from 10% to 13% of all tasks"),
    dict(id="B5", sec="S5", key="¶3", p=[11], type="anec", src=["intv"], grade="D",
         zh="一位工程師把同時應付好幾個 Claude 比作當保母：每個 agent 不分事情輕重，都用同樣急迫的方式要人處理。",
         note="", refs=[], anchors=["babysitting"], web="One engineer compared this to babysitting"),
    dict(id="B6", sec="S5", key="¶5", p=[11], type="desc", src=["survey"], grade="C",
         zh="2026 年 4 月調查的開放題（AI 怎麼影響日常工作）：27% 描述 Claude 工具帶來的生產力提升，20% 描述自己的角色從實際做事轉為管理 Claude。",
         note="開放題的答案怎麼歸類（人工或 LLM）、多少人作答，報告沒說。", refs=["G3", "G4"], nums=["27%", "20%"],
         anchors=["open-ended question"], web="27% described productivity gains"),
    dict(id="B7", sec="S5", key="¶6", p=[11], type="meas", src=["tele"], grade="B",
         zh="在互動式的多輪 session 裡，agent 大部分時間不是在工作，而是在等：以 session 的牆鐘時間減去 agent 實際工作時間計算閒置，Claude session 約 80% 的時間在等人類輸入。",
         note="這是「session 層級」的閒置率，不是「人」的閒置率。一個人同時開好幾個 session 時，每個 session 依定義大多在等——80% 反映的是人的注意力被切成好幾份，"
              "正好支持作者的瓶頸論點，但不代表人慢。報告也沒說超過多久的等待會被截掉（圖 2 的工時口徑排除超過 30 分鐘的等待，這裡沒說是否同樣處理）。",
         refs=["fig2"], nums=["80%", ["30 minutes", "S4:fig2"]], anchors=["wall-clock time"],
         web="around 80% idly waiting for human input"),
    dict(id="B8", sec="S5", key="¶7", p=[11, 12], type="meas", src=["tele"], grade="B",
         zh="把互動式 session 的 agent 輸出 token 換算成閱讀時數（每個 token 0.75 個英文字、每分鐘讀 250 字）：技術職能的輸出量過去 6 個月暴增；"
            "即使是非技術群組，輸出量也足以占掉半個以上工作週。圖 6 的終點：工程與研究每人每週 424 小時、財會 43、業務 35、其他非工程 27、法務政策與信任 26、行銷與公關 12。",
         note="這是把「量」換成直覺單位的示意指標，不是真的有人要讀：工程與研究的 424 小時是一週 40 小時的 10.6 倍。三個讀法上的提醒："
              "六張小圖的縱軸刻度各不相同（工程到 400、行銷只到 12），斜率看起來差不多，量其實差了幾十倍；"
              "多數小圖最後一個月急升，例如法務從約 8.4 跳到 26 小時（讀圖），用前一個月計，只有財會與業務超過 20 小時；"
              "程式碼與工具呼叫的 token 也被當成英文散文來換算。",
         refs=["fig6", "N6"], nums=["6 months", ["0.75", "S5:fig6"], ["250", "S5:fig6"], ["40 hours", "S4:fig2"]],
         fig=[["424 h", "fig6"], ["43 h", "fig6"], ["35 h", "fig6"], ["27 h", "fig6"], ["26 h", "fig6"], ["12 h", "fig6"],
              ["400", "fig6"]],
         read=["8.4"], calc=["10.6", "20"], anchors=["average human reading speed"],
         web="over half of the work week"),
    dict(id="B9", sec="S5", key="¶8", p=[11], type="desc", src=["tele"], grade="B",
         zh="於是出現另一種工作：寫給 agent 的常設指示，從 2025 年 7 月的「數百份」增加到一年後的 8,500 份。",
         note="「常設指示」沒有定義（是 CLAUDE.md 一類的設定檔？skills？）；「數百份」也不精確，若指 200 到 500 份，增幅約 17 到 43 倍（N16）。",
         refs=["N16", "G17"], nums=["8,500"], calc=["200", "500", "17", "43"], anchors=["standing instructions"],
         web="8,500 a year later"),
    dict(id="B10", sec="S5", key="¶8", p=[11, 12], type="anec", src=["intv"], grade="D",
         zh="例子：一位工程師設了「agent 幕僚長」來分流 agent 的請求；有人替自己的 Claude 團隊寫績效檢討；招募人員建了整合儀表板，讓 agent 主動揭露問題並啟動行動；"
            "一位律師把重心從審閱法律問題，轉為替法律建議做「SEO」——寫出能被（內部客戶的）agent 找到的框架。",
         note="律師的例子對法務工作的意涵最大：法務的產出從「答案」變成「可以被 agent 檢索與套用的規則」（見「法務意涵」）。",
         refs=[], anchors=["SEO for legal advice"], web="SEO for legal advice"),
    dict(id="B11", sec="S5", key="¶9", p=[12], type="meas", src=["tele"], grade="C",
         zh="這類後設工作占一般員工互動式 session 的比重，從 2025 年秋的 10% 升到 2026 年春的 22%；增幅主要來自 agent 管理：替多 agent 執行寫規格、讓一個 agent 審另一個的輸出、監控流程。",
         note="以自動編碼器評 2,000 則一行對話摘要。2,000 則若平均分到 12 列乘 2 期，每格只有約 83 則，比例 20% 的 95% 信賴區間約正負 8.6 個百分點（N9，假設值），"
              "所以職能之間差幾個百分點不宜過度解讀。圖 7：基礎設施從約 4.7% 升到 29%、開發工具約 4.5% 到 26%，業務幾乎不動（約 14.5% 到 15%）；"
              "財務、法務與行銷合併成一組，約 6.4% 到 12%，是最低的一組（起點為讀圖）。",
         refs=["fig7", "N9", "N18", "G4"], nums=["10%", "22%", ["2,000", "S5:fig7"]],
         fig=[["29%", "fig7"], ["26%", "fig7"], ["15%", "fig7"], ["12%", "fig7"]],
         read=["4.7", "4.5", "14.5", "6.4"], calc=["12", "2", "83", "20", "95", "8.6"],
         anchors=["agent management"], web="leapt from 10% of the average employee"),
    dict(id="B12", sec="S5", key="¶10", p=[12, 13], type="anec", src=["intv"], grade="C",
         zh="儘管 agent 更可靠、監督工具投資很大，人類的信任與問責仍然關鍵：追 bug 愈來愈常挖出需要人類開會、決策、治理才能解的組織性、系統性或技術債問題；"
            "一場又一場訪談裡，員工都說面對面協調不可或缺。",
         note="", refs=[], anchors=["human trust and accountability"], web="human trust and accountability remains critical"),
    dict(id="B13", sec="S5", key="¶10", p=[13], type="desc", src=["cal"], grade="B",
         zh="依行事曆資料，中位數員工的開會時間比一年前多 20%；部分反映公司成長與轉向會議密集的非技術職，但即使是技術職的個人貢獻者，開會時間也多了 16%。",
         note="給了相對增幅，沒給基準時數。技術職個人貢獻者的 16% 排除了職務組成的變化，比全體的 20% 更有說服力。",
         refs=["G2"], nums=["20%", "16%"], anchors=["calendar data"], web="spends 20% more time in meetings"),
    dict(id="B14", sec="S5", key="¶11", p=[13], type="anec", src=["intv"], grade="D",
         zh="技術與非技術角色的「執行」部分都被自動化了（寫程式、找 bug、記錄進度、草擬 email）。工程師說自己成了 agent 的領導者與管理者；"
            "非技術員工說自己做愈來愈多策略性工作——一位受訪者說，原本占 20% 的策略工作變成占 90%。但許多非技術角色的核心執行本身就是人際的："
            "一通業務電話、一場面試、一次跨部門對齊，這些仍屬於人。",
         note="", refs=[], nums=["20%", "90%"], anchors=["remains human"], web="becomes 90% of the job"),
    dict(id="B15", sec="S5", key="¶12", p=[14], type="desc", src=["comm"], grade="B",
         zh="agent 擴散到 Slack，最終出現在近一半的活躍公開頻道。",
         note="只看公開頻道；agent「出現」的門檻（一則訊息？持續參與？）沒有定義。",
         refs=["G17"], anchors=["nearly half of active, public channels"], web="nearly half of active, public channels"),
    dict(id="B16", sec="S5", key="¶12", p=[14], type="desc", src=["comm"], grade="C",
         zh="圖 8 以某個大型部門為例，把所有公開頻道裡的人與 agent 依是否在同一討論串互動連成網路：代表 agent 討論串的橘點大量冒出、主導了網路。",
         note="A、B 兩張圖沒有標時間點或期間，也沒有任何網路指標的數值（密度、中心性）；而且只有一個部門。視覺印象強，資訊量少（G5）。",
         refs=["fig8", "G5"], anchors=["single large department"], web="orange dots blossom and dominate the network"),
    dict(id="B17", sec="S5", key="¶13", p=[14], type="desc", src=["comm"], grade="C",
         zh="agent 多半出現在專門的 Claude–人類互動頻道，而不是在既有的人類頻道裡大量發言；人類溝通的結構與密度變化不大：該部門人類討論串的人類回覆數維持不變，"
            "只是額外疊上 agent 的回覆。agent 是某一位員工的「團隊」，而不是同時連結很多人的樞紐。",
         note="結論合理，但沒有給任何數字（回覆數、密度），讀者只能相信。", refs=["G3"],
         anchors=["did not replace human interaction"], web="Agents did not replace human interaction"),
    dict(id="B18", sec="S5", key="¶14", p=[14, 15], type="anec", src=["intv"], grade="C",
         zh="人被迫把工作搬到 agent 看得見的地方：面對面做的決定如果沒留紀錄，agent 就缺少更新目標的關鍵脈絡——例如有人的名字掛在幾個月前一份周邊商品文件上，"
            "agent 就一直把 T 恤和馬克杯的請求轉給那個人，即使職責早就變了。在 AI 密集的職場，私下的工作（不留紀錄的會議與私訊）是看不見、令人困惑、而且被勸阻的；"
            "一位研究員說，多數組織不是這樣運作，這要求領導者得公開為回饋辯護。",
         note="這是報告裡法律意涵最大的一段：「預設公開」與律師－當事人特權的保密前提、營業秘密的「合理保密措施」要件（聯邦 DTSA 與加州法都有）、"
              "員工個資的目的限制都有張力（見「法律對照」）。",
         refs=["G8", "law:ustrade", "law:ccpa"], anchors=["agent-visible channels", "Claude swag"], web="agent-visible channels"),

    # ------------------------------------------------------------------ §5 招募（§5¶15–16）
    dict(id="H1", sec="S5", key="¶15", p=[15], type="desc", src=["hire"], grade="C",
         zh="招募評分卡：用自動編碼器處理 2024 年以來數千名新進人員的面試評語。最明顯的變化，是愈來愈看重候選人是否展現有創意地使用 AI 工具："
            "2024 年，技術職約 5%、非技術職 7% 的評估提到 AI 工具紀錄；到 2026 年，技術職變成三倍、非技術職變成四倍。",
         note="報告只給倍數。換算回去約是技術職 15%、非技術職 28%（N4）——即使變成四倍，多數評估仍然沒有提到 AI 工具。編碼器的定義與驗證都沒有揭露。",
         refs=["N4", "G4"], nums=["5%", "7%"], calc=["15", "28"], anchors=["tripled", "quadrupled"],
         web="around 5% of assessments for technical roles"),
    dict(id="H2", sec="S5", key="¶16", p=[15], type="desc", src=["hire"], grade="C",
         zh="更深一層的變化：技術職候選人的評語裡，增幅最大的是對自主性與判斷力的評論；領域專長的討論占比縮小。一位主管說，預期模型會持續「參差不齊」，"
            "所以希望團隊成員能跨領域互換。非技術職則是客戶導向與使命認同的評論增加、執行能力的討論減少。",
         note="沒有任何占比數字。值得對照的是 Anthropic 自己 6 月的研究（Hitzig 等人）：用 agent 寫程式時，從新手到中等程度的落差最大，"
              "再往上的深度專精只多一點點——這和「降低領域專長權重」「少收新手」兩個招募現象方向一致。但那篇的「新手」指的是任務領域的能力，不等於職級上的初階員工；這是兩份文件之間的推論，不是本報告的發現。",
         refs=["lit:hitzig"], anchors=["fungible across domains", "domain expertise shrank"], web="fungible across domains"),

    # ------------------------------------------------------------------ §6 雇主能做什麼
    dict(id="E1", sec="S6", key="¶1", p=[15, 16], type="extrap", src=[], grade="D",
         zh="歷史類比：鐵路帶來經理人企業、蒸汽動力帶來工廠、個人電腦帶來新創。LLM 會需要什麼新組織？一種想像是一人新創指揮成群 agent 賺進數十億；"
            "另一種是由 AI 天才當執行長、只雇人類去拿移液管做實驗、到國會作證的公司。",
         note="", refs=[], anchors=["managerial corporation"], web="personal computers delivered the startup"),
    dict(id="E2", sec="S6", key="¶2", p=[16], type="desc", src=["hr"], grade="C",
         zh="Anthropic 兩者皆非：一年內規模成長為三倍，不再是小新創；也沒有把經營控制權交給模型——從公司策略到團隊決策，都由書面的 Slack 辯論與面對面會議主導，"
            "AI agent 參與很少。保持人類工作可見，讓自主 agent 能從最新脈絡推理；指揮 agent 團隊的個人貢獻者，在所需知識與工作相互依賴上更像經理人。",
         note="「三倍」是理解全篇占比數字的關鍵分母，卻只在結論段出現一次，而且沒有附數字基礎（G1）。",
         refs=["N1", "G1"], anchors=["tripled in size"], web="It has tripled in size"),
    dict(id="E3", sec="S6", key="¶3", p=[16], type="extrap", src=[], grade="C",
         zh="員工愈來愈把工作看成管理一群 Claude，花更多時間打造自己領域需要的工具；這種實驗意味著員工持續把自己的任務自動化掉。"
            "在某些角色，人愈來愈遠離當初養成其技能的第一線工作。agent 跑得很快，人的注意力與判斷成為系統的瓶頸；從業務到法務，員工被期待做更多、不同的事。",
         note="這一句點出了「養成斷層」，卻沒有往下談：如果第一線工作是技能的來源，而人不再做第一線工作，下一代的判斷力從哪裡來？"
              "Anthropic 2025 年 12 月的內部研究（Huang 等人）已經記錄過工程師對技能萎縮的擔憂。",
         refs=["lit:huang"], anchors=["object-level work"], web="originally built their skills"),
    dict(id="E4", sec="S6", key="¶4", p=[16], type="desc", src=["hr", "fin"], grade="C",
         zh="總結：組織與工作內容的改變，與初階技術職在人數、新進、職缺三個口徑的占比下降同時出現；招募重自主與判斷，不重執行與狹窄專長；"
            "整體而言，Anthropic 營收成長相對於就業成長的速度，已超越前一代科技公司早期的高速生產力成長。",
         note="「同時出現」是準確的措辭（相關，不是因果）。營收對就業的比較，同樣受 L1 的口徑問題影響。",
         refs=["L1"], anchors=["appeared alongside"], web="revenue growth relative to its employment growth"),
    dict(id="E5", sec="S6", key="¶5", p=[16], type="extrap", src=["ext"], grade="C",
         zh="把這些模式往前、往外推到整體經濟，意味著 AI 擴散可能帶來勞工被取代的風險；既有研究也發現，AI 原生新創與 AI 採用者的組織更扁平、雇用更少初階員工。",
         note="引用核對：Kim & Koning（AI 原生新創規模小 25%、初階與經理人占比各低約 15%、層級約扁平半級）、Ewens & Giroud（採用 AI 後階層變扁平）、"
              "Hosseini & Lichtinger（採用生成式 AI 的公司，初階就業相對下降，主因是招募放緩）——三篇都支持報告的轉述（見「文獻」）。",
         refs=["lit:kim", "lit:ewens", "lit:hosseini"], ext=[["25", "lit:kim"], ["15", "lit:kim"]],
         anchors=["worker displacement"], web="could risk worker displacement"),
    dict(id="E6", sec="S6", key="¶7", p=[17], type="meas", src=[], grade="-", self=True,
         zh="能從 Anthropic 學到什麼？作者先自我設限：Anthropic 有許多雇用實務無法複製到整體經濟。",
         note="", refs=["K0"], anchors=["cannot be replicated"], web="cannot be replicated across the economy"),
    dict(id="E7", sec="S6", key="¶8", p=[17], type="norm", src=[], grade="D",
         zh="第一，廣泛的員工持股讓員工和公司的成功利害一致。作者承認，對估值大漲的公司這是容易擺出的姿態，對很多公司而言共同持股可能不夠、或不可取；"
            "但很難想像一種「親勞工的 AI 導入」裡，勞工對成功導入沒有財務上的利益。",
         note="報告沒有提出任何持股效果的證據；持股也把員工的薪資與財富集中押在同一家公司。對多數雇主——非上市、估值平平或成長停滯的公司——"
              "這個工具根本不存在，作者自己也承認這一點。",
         refs=[], anchors=["widespread stock ownership"], web="widespread stock ownership gives employees"),
    dict(id="E8", sec="S6", key="¶8", p=[17], type="norm", src=[], grade="D",
         zh="歷史類比：二戰後 1950 年代的勞資協議——汽車工人與鋼鐵工人的工會讓資方保有重組（甚至加重）工作的權力，換取與生產力連動的加薪和完整的福利。"
            "作者主張，不論 AI 時代的新協議長什麼樣子，分享導入利益的機制都不可或缺；Anthropic 的員工把自己的專業寫給機器、工作常規不斷被打亂、"
            "大量工作變成速讀 AI 的輸出——這些都不是無償的。",
         note="類比的機制不一樣：當年的協議靠高組織率的工會「集體」協商取得；報告提出的是「個別」持股。兩者分享利益的方式、談判力量與適用範圍都不同。",
         refs=[], nums=["1950s"], anchors=["United Auto Workers"], web="United Auto Workers"),
    dict(id="E9", sec="S6", key="¶9", p=[17], type="norm", src=[], grade="D",
         zh="第二，Anthropic 正在建立持續運作的預警系統，監測面臨 AI 轉型的職務：用一組職務層級的需求與生產力指標對照 AI 能力與使用，標出工作在哪裡移動，"
            "讓公司及早把受影響的員工轉到技能相近、較不立即受衝擊的職務。作者認為，AI 進步愈快，事事都到外部勞動市場找人就愈會成為瓶頸；內部彈性再配置的系統會很關鍵。",
         note="支持證據是報告自己的發現（部門間流動增加、工作內容改變）。預警系統的設計、準確度、員工能否得知與申訴，都沒有揭露（G7）。",
         refs=["G7", "L17"], anchors=["role-level metrics"], web="ongoing early warning system"),
    dict(id="E10", sec="S6", key="¶10", p=[18], type="norm", src=[], grade="-", self=True,
         zh="內部再配置承諾有取捨：運作良好的勞動市場應該把人移到最有生產力的位置，不論在現職公司或別家；承諾再配置現有員工，可能讓雇主不敢冒險雇用新人；"
            "在正常、尤其是競爭激烈的經濟環境下，這類承諾可能很昂貴。",
         note="這一段和報告的核心發現直接衝突：最受影響的正是新人（初階）。作者自己點出了「保護在職者，雇主就更不敢雇新人」的機制，卻仍把它列為建議（見「政策評析」）。",
         refs=[], anchors=["hesitant to take a risk"], web="hesitant to take a risk on hiring"),
    dict(id="E11", sec="S6", key="¶11", p=[18], type="norm", src=["ext"], grade="D",
         zh="但優先再配置會迫使採用 AI 的公司思考 AI 如何為新產品、新市場創造新任務，而不是只拿 AI 替代人力省成本；這有助抗拒「平庸」或「無效率」的自動化——"
            "AI 只勉強勝過人，雇主就把人換掉，被取代者承受龐大的所得損失，生產力卻只多一點點。",
         note="理論依據是 Acemoglu & Restrepo 的取代效果與恢復效果：自動化把任務從人移給資本（取代），新任務把工作帶回給人（恢復）。"
              "報告把「再配置承諾」當成推動恢復效果的組織機制——這是有意思的連結，但報告沒有證據顯示它在 Anthropic 確實催生了新任務。",
         refs=["lit:acemoglu", "lit:beraja"], anchors=["so-so", "inefficient"], web="create new tasks for new products"),
    dict(id="E12", sec="S6", key="¶12", p=[18], type="norm", src=["intv"], grade="D",
         zh="從 Anthropic 的經驗看，新穎的任務與持續屬於人的任務，都與密集的 AI 使用並存；未來的任務組合不確定，應該保留有彈性的人力。"
            "一位 Anthropic 高階主管說，焦慮擔憂的員工不會拿出最好的表現。",
         note="報告宣告「三項特徵」，卻只編號到「第二」，網頁版也一樣；依上下文，第三項最可能是這裡的「保留彈性人力／內部再配置承諾」（G6）。",
         refs=["G6"], anchors=["flexible workforce"], web="preserving a flexible workforce"),
    dict(id="E13", sec="S6", key="¶13", p=[18], type="norm", src=[], grade="-", self=True,
         zh="這些作為都擋不住強大的 AI 衝擊工作，也都沒有直接處理本報告記錄的初階招募放緩——對在職者的就業保障，幫不到一開始就沒被雇用的人。"
            "雇主的私人行動必須搭配有遠見的政府政策（再訓練與所得支持），並以清楚的職場轉型規模為依據。",
         note="「再訓練」的連結指向 Roodman & Massenkoff 的證據回顧：56 個美國隨機試驗的結論是效果「正向但有限」——每提供一個訓練名額，就業率約提高二到三個百分點、"
              "年收入約多 1,000 美元，成本約 13,000 美元；若 AI 大規模取代勞工，現有的再訓練計畫很可能不夠。報告只放了一個連結字，沒有把這個保守的結論帶進來（見「文獻」）。",
         refs=["lit:roodman"], ext=[["56", "lit:roodman"], ["1,000", "lit:roodman"], ["13,000", "lit:roodman"]],
         anchors=["not hired to begin with"], web="not benefit those not hired"),
]
