# Anthropic 就業報告拆解

Wilmers, Catipon, Massenkoff & McCrory (2026),
*How Employment is Changing at Anthropic*（The Anthropic Institute, Technical Report, 2026-10-16，20 頁）的中文逐項分析。

報告用 Anthropic 自己的內部資料，描述 AI agent 進入日常工作之後，就業、生產力與招募標準怎麼變。
本站把它拆成 76 則主張，逐一標出證據強度、回到原文核對，並把報告沒說的事整理出來。

- 網站：<https://cecefat.github.io/ai-employment-lex/>
- 單檔報告（Markdown）：[`report.md`](report.md)
- 原文：<https://www.anthropic.com/research/employment-at-anthropic>

## 結論先講

**描述可信，歸因偏弱，外推要打折。** 初階技術職在在職、新進、職缺三個口徑的占比同步下降，agent 用量與人均產出指標急升，
面試評語的重心從專長移向自主與判斷——這些在描述層次都站得住。弱的是因果與外推：同一人前後比較只做了工程師與業務兩種職能；
公司一年內規模成為三倍，依報告自己的數字試算，初階技術員工的絕對人數很可能不減反增；Anthropic 是極端個案。
政策段的內部張力最值得注意：作者推薦的內部再配置承諾，依其自己的說法可能讓雇主更不敢雇新人。

## 這一站不含報告全文

原報告 © 2026 Anthropic PBC，未附開放授權。所以：

- **不內嵌全文、不轉載圖表、不建逐字引文庫。** 全站只逐字引用一句 11 個英文字的訪談句。
- 「報告說了什麼」是用自己的話寫的轉述，不是翻譯；其餘是分析、核算與評論。
- 每一則主張附「原文定位」連結（Text Fragment）：打開 Anthropic 官方網頁時，瀏覽器會捲到並標亮那一句。另附 PDF 頁碼連結。
- `source/`（報告逐頁抽取的文字、官方網頁文字、圖頁影像與 OCR，只用於本機核對）已列入 `.gitignore`，**不在這個 repo 裡**。

## 利益衝突揭露

本站的分析初稿由 Claude（Anthropic 的模型）撰寫，分析對象是 Anthropic 自己的報告。對策是把判斷攤開：評等標準公開、
每一則主張都能一鍵回到原句、每一個重算都寫出公式與假設、所有讀圖數字都標「讀圖」。

## 證據紀律

`tools/verify.py` 在建置時逐項核對，任何一項不通過，`build.py` 就不產出網頁：

| 核對 | 做法 |
|---|---|
| 報告數字（95 個） | 必須出現在所標段落，前後不能黏著別的數字 |
| 圖內標示（81 次比對） | 圖都是點陣圖；300 DPI 裁出圖框後以 Tesseract OCR 比對 |
| 原文定位片語（76 個） | 必須同時出現在 PDF 該段與官方網頁版，且不超過 7 個英文字 |
| lint | 站上中文裡出現的每個數字，都要在資料層宣告來處（報告原文、圖內標示、讀圖、自算、外部文獻） |
| 著作權 | 站上任何字串若與報告全文有連續 8 個英文字相同，除標題、章節名、圖題、文獻題名與唯一引文外，建置中止 |
| 出處 | 本機 PDF 與官方 CDN 檔案的 MD5、大小相同（2026-10-19） |

讀圖數值（85 個）是放大到 300 DPI 後依座標軸換算的估計，標「讀圖」，不進機械核對。
這些核對保證「數字確實印在那裡」，不保證我把它讀對了意思；轉述、評等與評析是判斷。

## 法律對照以美國法為主

報告本身是經濟研究，沒有適用任何法律；但評估它描述的雇用實務與推薦的做法，準據法是 Anthropic 雇用關係所在地的法律——
美國聯邦法與加州法（at-will 雇用、WARN、CCPA／CPRA、加州隱私保護局 ADMT 規則、加州 FEHA 自動化決策規則、紐約市 AEDT 法、
營業秘密的合理保密措施、TAA 的現況），歐盟另列 AI 法附件 III 第 4 點。條文都回官方來源逐字核對。
台灣法只列一則「若台灣企業仿效」的移植提醒，明確標示不是本案的準據法。

## 重建

```
python tools/extract.py "path/to/Employment at Anthropic.pdf"   # pdftotext＋PyMuPDF；產出 source/pages.txt、paras.json、fig/*.png
python tools/fetch_web.py                                        # 官方網頁版文字 → source/web.txt
python tools/ocr_figs.py                                         # 需要 Tesseract；圖框 OCR → source/fig_ocr.json
python tools/build.py                                            # 核對通過才會產出 index.html 與 report.md
```

不要接管線（`| tail` 之類）——assert 失敗的 exit code 會被吃掉。改 `tools/app.js` 之後先 `node --check tools/app.js`。

| 檔 | 作用 |
|---|---|
| `tools/data_meta.py` | 書目、出處驗證、章節地圖、資料來源、主張類型、證據等級 |
| `tools/data_claims.py` | 76 則主張（座標、類型、來源、等級、轉述、評析、核對欄位） |
| `tools/data_figs.py` | 八張圖的重讀：圖內標示、讀圖、撐得起與撐不起、重畫資料 |
| `tools/data_checks.py` | 18 項數字核算、18 項揭露缺口 |
| `tools/data_lit.py` | 12 筆文獻：報告怎麼用、回原頁核對到什麼 |
| `tools/data_law.py` | 法律對照（美國為主、歐盟、台灣移植提醒） |
| `tools/data_report.py` | 主報告敘述、判定、論證鏈、政策評析、詞彙 |
| `tools/verify.py` | 核對與著作權檢查 |
| `tools/build.py` | 組裝單檔 `index.html` 與 `report.md` |
| `tools/template.html`、`tools/app.js` | 版面、樣式與前端 |

## 限制

- 報告的數字都來自 Anthropic 內部；本站只能核對「報告寫了什麼」，不能核對「事實是否如此」。
- 讀圖數值與重畫的圖是估計。
- 文獻核對只到摘要或公開頁面；出版社拒絕存取的一篇標「未核對」。
- 法律對照不是法律意見。
- 中文敘述與分類是 AI 協助整理的詮釋，可能有誤。最終檢閱是使用人自己的責任。

## 關係聲明

本站不是 Anthropic 的出版品，未經其審閱或背書，與 Anthropic 無關。
流程與驗證規則由我訂定；程式、資料整理與分析初稿由 Claude（AI）撰寫。

原報告 © 2026 Anthropic PBC。

同一套做法的其他站：[AI 濫用威脅圖譜](https://cecefat.github.io/ai-misuse-lex/)、
[Claude 系統提示詞演變自學站](https://cecefat.github.io/claude-sysprompt-study/)、
[RLHF 知識圖譜](https://cecefat.github.io/rlhf-lex/)、
[英國 SEP／FRAND 因子知識圖譜](https://cecefat.github.io/ukipo-lex/)。
