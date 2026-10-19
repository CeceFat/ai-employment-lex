# -*- coding: utf-8 -*-
"""法律對照：以美國聯邦與加州法為主框架。

為什麼是美國法：報告本身是經濟研究，沒有適用任何法律；但要評估它描述的雇用實務、
以及它推薦給雇主的做法，準據法是 Anthropic 雇用關係所在地的法律。Anthropic 總部在舊金山，
官方職缺頁（2026-10-19 查）的職缺集中在舊金山、紐約、西雅圖；另有倫敦、都柏林、慕尼黑、巴黎、
東京、首爾、雪梨等據點——報告沒有分國別，境外據點各依當地法（歐盟據點見 euaia）。

條文一律回官方來源逐字核對（2026-10-19）：加州法典取自 leginfo.legislature.ca.gov（以瀏覽器讀取）、
聯邦法典取自 Cornell LII、加州隱私保護局規則取自 cppa.ca.gov 公告的核定條文、加州民權委員會規則取自其
官方新聞稿、紐約市法規取自 nyc.gov、TAA 狀態取自美國勞工部網站、歐盟 AI 法取自 artificialintelligenceact.eu。
美國的成文法與規則屬政府文件，可逐字引用。

台灣法另列一則「移植提醒」（tw），明確標示不是本案準據法，只供台灣讀者評估仿效時參考。
"""

LAW = [
    dict(id="atwill", juris="加州", name="California Labor Code §2922", short="at-will 雇用",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=LAB&sectionNum=2922",
         text="An employment, having no specified term, may be terminated at the will of either party on notice to the other.",
         zh="未定期限的雇用，任一方得通知對方後隨時終止。",
         maps=["E9", "E10", "E12", "I5"],
         note="這是讀懂報告政策段的前提。在 at-will 制度下，雇主沒有法定的轉調或安置義務；Anthropic「優先內部轉調」是自願承諾，"
              "隨時可以改變。報告擔心「再配置承諾會讓雇主不敢雇新人」，正是因為這種承諾在美國沒有法律強制、要靠雇主自己扛成本。"
              "反過來說，承諾的可信度也只能靠公司自己——除非承諾寫進契約或形成默示契約，員工通常沒有法律上的請求權。"),
    dict(id="warn", juris="聯邦／加州", name="29 U.S.C. §2102(a)；California Labor Code §1401(a)", short="大量資遣 60 天預告",
         url="https://www.law.cornell.edu/uscode/text/29/2102",
         text="An employer shall not order a plant closing or mass layoff until the end of a 60-day period after the employer serves written notice of such an order— "
              "（加州 §1401(a)：An employer may not order a mass layoff, relocation, or termination at a covered establishment unless, 60 days before the order takes effect, "
              "the employer gives written notice of the order …）",
         zh="雇主在送達書面通知滿 60 天前，不得下令關廠或大量資遣（聯邦 WARN）；加州版要求大量資遣、遷移或終止營運前 60 天書面通知受影響員工與主管機關。",
         maps=["E13", "E9"],
         note="美國法對 AI 導致的組織調整，管的是「程序」（大量資遣前要預告），不是「實體」（不要求先轉調）。所以報告推薦的內部再配置，"
              "是在法律最低要求之上的選擇；若沒有做到，法律能提供的只是 60 天的預告期。"),
    dict(id="ccpa", juris="加州", name="California Civil Code §1798.100(a)(1)、(c)；§1798.145(m)(4)", short="員工個資：告知、目的限制、比例原則",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100",
         text="(c) A business’ collection, use, retention, and sharing of a consumer’s personal information shall be reasonably necessary and proportionate to achieve "
              "the purposes for which the personal information was collected or processed, or for another disclosed purpose that is compatible with the context in which "
              "the personal information was collected …（§1798.145(m) 的員工資料豁免：This subdivision shall become inoperative on January 1, 2023.）",
         zh="企業蒐集、使用、保存與分享個資，必須為達成蒐集目的（或與蒐集脈絡相容的已揭露目的）所合理必要且合乎比例；並須在蒐集時或之前告知蒐集的類別與目的。"
            "原本對員工與求職者資料的豁免，已於 2023 年 1 月 1 日失效。",
         maps=["G8", "B13", "B16", "P9", "H1", "E9"],
         note="報告的研究方法對員工資料做了個人層級的分析：agent 遙測、行事曆、Slack 網路、面試評分卡、commit 紀錄。在加州，這些都是 CCPA 下的員工個資，"
              "要回答兩個問題：蒐集時告知的目的是否涵蓋「職務預警」「勞動經濟研究」這類用途；這樣的使用是否合理必要且合乎比例。報告沒有交代（G8），"
              "沒交代不等於沒做，但想仿效的雇主一定要先做這一步。"),
    dict(id="admt", juris="加州", name="Cal. Code Regs. tit. 11, §7001(e)、§7001(ddd)(4)、§7200（加州隱私保護局 ADMT 規則）", short="自動化決策用於工作分派",
         url="https://cppa.ca.gov/regulations/ccpa_updates.html",
         text="“Automated decisionmaking technology” or “ADMT” means any technology that processes personal information and uses computation to replace human "
              "decisionmaking or substantially replace human decisionmaking. … “Employment or independent contracting opportunities or compensation” means: (A) Hiring; "
              "(B) Allocation or assignment of work for employees … (C) Promotion; and (D) Demotion, suspension, and termination.",
         zh="ADMT 指處理個資、以運算取代或實質取代人類決策的技術；「實質取代」指沒有人類參與就依技術產出做決定（人類參與須能解讀產出、審查分析、並有權改變決定）。"
            "「重大決定」包括雇用：錄用、工作分派與報酬、升遷、降調停職與終止。規則自 2026 年 1 月 1 日生效；在 2027 年 1 月 1 日前已用 ADMT 做重大決定者，"
            "須於該日前合規（事前告知、選擇退出、查詢權等）。",
         maps=["E9", "I5", "H1", "G7"],
         note="報告描述的預警系統是「職務層級的指標，供公司決定把人轉到哪裡」。只要最後的轉調決定有實質的人類審查，就不屬於 ADMT；但若系統的產出被直接拿來分派個人的工作，"
              "就落入「工作分派」這個重大決定類別，要給員工事前告知（§7220），原則上也要提供選擇退出（§7221，有例外）。報告沒有揭露系統設計（G7），所以無法判斷落在哪一邊——"
              "這正是想仿效的雇主要先設計清楚的地方。"),
    dict(id="feha", juris="加州", name="加州民權委員會「自動化決策系統」雇用規則（FEHA，2025 年 10 月 1 日生效）", short="AI 用於雇用決定的歧視風險",
         url="https://calcivilrights.ca.gov/2025/06/30/civil-rights-council-secures-approval-for-regulations-to-protect-against-employment-discrimination-related-to-artificial-intelligence/",
         text="Make it clear that the use of an automated-decision system may violate California law if it harms applicants or employees based on protected characteristics, "
              "such as gender, race, or disability. Ensure employers and covered entities maintain employment records, including automated-decision data, for a minimum of four years.",
         zh="（官方新聞稿對規則重點的說明）使用自動化決策系統若因性別、種族、身心障礙等受保護特徵而損害求職者或員工，可能違反加州法；"
            "雇主須保存雇用紀錄（包括自動化決策資料）至少四年。規則於 2025 年 6 月 27 日核定、10 月 1 日生效。",
         maps=["H1", "H2", "K4"],
         note="報告用自動編碼器分析面試評分卡，是「研究」用途，不是拿來做錄取決定。但報告的訊息是「招募標準正在轉向自主、判斷與 AI 工具使用」；"
              "雇主若把這套編碼直接用在甄選上，就進入這套規則的範圍，要能說明它不會對受保護群體造成不利影響，並保存相關資料。"),
    dict(id="nyc144", juris="紐約市", name="New York City Local Law 144 of 2021（自動化雇用決策工具）", short="AEDT 的偏誤稽核與通知",
         url="https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page",
         text="Local Law 144 of 2021 regarding automated employment decision tools (“AEDT”) prohibits employers and employment agencies from using an automated employment "
              "decision tool unless the tool has been subject to a bias audit within one year of the use of the tool, information about the bias audit is publicly available, "
              "and certain notices have been provided to employees or job candidates.",
         zh="雇主使用自動化雇用決策工具，須在使用前一年內完成偏誤稽核、公開稽核資訊，並通知員工或求職者；主管機關自 2023 年 7 月 5 日起執法。",
         maps=["H1", "H2"],
         note="Anthropic 在紐約有大量職缺。同上：報告的評分卡編碼是研究用途；但若被用來實質協助錄取或升遷決定、而對象是紐約市的求職者或員工，就要先做偏誤稽核並通知。"),
    dict(id="ustrade", juris="聯邦／加州", name="18 U.S.C. §1839(3)(A)（DTSA）；California Civil Code §3426.1(d)(2)（CUTSA）", short="營業秘密的合理保密措施",
         url="https://www.law.cornell.edu/uscode/text/18/1839",
         text="(A) the owner thereof has taken reasonable measures to keep such information secret; …（加州：Is the subject of efforts that are reasonable under the "
              "circumstances to maintain its secrecy.）",
         zh="資訊要受營業秘密保護，所有人必須已採取合理措施保持其秘密性（聯邦）；加州的要件是「已就具體情況採取合理的保密努力」。",
         maps=["B18", "E2"],
         note="報告把「預設公開、讓 agent 看得見」描寫成 AI 密集組織運作的條件。資訊放在廣泛公開的內部頻道、被大量 agent 讀取，若沒有依「需要知悉」分級，"
              "日後主張營業秘密時，「合理保密措施」會比較難證明。同樣的邏輯也適用於律師與當事人間的特權：特權以保密為前提，法律意見在內部被廣泛散布、"
              "超出需要知悉的範圍，可能動搖特權主張（視具體事實而定）。這是本站的延伸觀察，報告沒有討論。"),
    dict(id="taa", juris="聯邦", name="Trade Act of 1974 §285(a)（Trade Adjustment Assistance）", short="聯邦轉業調整方案的現況",
         url="https://www.dol.gov/agencies/eta/tradeact",
         text="On July 1, 2022, the termination provision under Section 285(a) of the Trade Act of 1974, as amended, took effect. Until further notice, the Department may "
              "not issue any determinations and may not accept any new petitions or requests for reconsideration.",
         zh="（美國勞工部公告）自 2022 年 7 月 1 日起，貿易調整援助方案的終止條款生效；在另行通知前，勞工部不得作成認定，也不受理新的申請。",
         maps=["E13"],
         note="報告最後呼籲「有遠見的政府政策（再訓練與所得支持）」。美國過去針對特定原因失業者最完整的轉業方案是 TAA（因貿易失業），它從 2022 年起已停止受理新案；"
              "就本站查到的範圍，沒有一個針對「因 AI 或技術而失業」、現成運作中的專門調整方案。報告自己連結的證據回顧又指出，一般性職訓的效果有限（Roodman & Massenkoff）。"
              "所以報告呼籲的政策，在美國幾乎要從頭建構。"),
    dict(id="euaia", juris="歐盟", name="歐盟人工智慧法附件 III 第 4 點", short="雇用領域的高風險 AI（歐盟據點）",
         url="https://artificialintelligenceact.eu/annex/3/",
         text="(a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted job advertisements, to analyse and "
              "filter job applications, and to evaluate candidates; (b) AI systems intended to be used to make decisions affecting terms of work-related relationships, "
              "the promotion or termination of work-related contractual relationships, to allocate tasks based on individual behaviour or personal traits or characteristics "
              "or to monitor and evaluate the performance and behaviour of persons in such relationships.",
         zh="（a）用於招募或甄選自然人的 AI 系統；（b）用於作成影響勞動關係條件、升遷或終止之決定，依個人行為或特質分派任務，或監測評估人員表現與行為的 AI 系統。",
         maps=["E9", "H1", "G7"],
         note="Anthropic 在都柏林、慕尼黑、巴黎也有職缺，報告的資料沒有分國別。若預警系統或評分卡編碼用在歐盟據點員工的個人層級決定，就屬於高風險 AI 的類別，"
              "另有 GDPR 的資料保護要求。"),
    dict(id="tw", chip="台灣移植提醒", juris="台灣（移植提醒）", name="若台灣企業仿效：勞動基準法第 11 條第 4 款等", short="不是本案準據法",
         url="https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=N0030001&flno=11",
         text="勞動基準法第 11 條第 4 款：業務性質變更，有減少勞工之必要，又無適當工作可供安置時。（最高法院 114 年度台上字第 766 號民事判決："
              "雇主資遣勞工前必先盡「安置前置義務」，必無處可供安置時，最後不得已才可資遣。）",
         zh="",
         maps=["E9", "E10"],
         note="這一則不是用來評價 Anthropic——它的雇用關係不受台灣法規範。放在這裡，是因為報告把做法推薦給「整體經濟」的雇主，台灣讀者會想知道照搬時的差異。"
              "最大的差異在第三項建議：美國是 at-will，內部再配置是自願承諾；台灣的資遣門檻本身就要求雇主先在既有的適當職缺安置（但不必另創新職位），"
              "AI 帶來的技術變更可以構成「業務性質變更」（最高法院 98 年度台上字第 652 號）。其他差異：利益分享可以接《公司法》第 235 條之 1 的員工酬勞（連動獲利，不是生產力）；"
              "員工資料受《個人資料保護法》第 5 條、第 20 條的目的限制；《人工智慧基本法》第 15 條把弭平技能落差、輔導 AI 致失業者就業列為政府義務。"),
]
