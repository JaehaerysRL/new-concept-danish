# CLAUDE.md

《新概念丹麦语》（Ny Koncept Dansk, NCD）：面向中文母语者、对标 DU3 Modul 1–5 的丹麦语自学教材。
LaTeX 源码编译成 PDF，并从同一份课文抽取题库，生成可离线使用的交互练习网页。

## 仓库结构

| 路径 | 内容 |
| :--- | :--- |
| `common/ncd-style.sty` | 全套教材共用的样式宏包（配色、`\ncdlesson`、`\da`/`\dabold`、`\ipa`、各类 tcolorbox、`glosertable`） |
| `syllabus/` | 总目录与螺旋式语法大纲 |
| `ncd1/`, `ncd2/`, `ncd3/`, `ncd4/`, `ncd5/` | `NCDx_Book.tex` 主入口 + `lessons/L01.tex …`（NCD 1/2 各 24 课，NCD 3/4 各 20 课，NCD 5 共 16 课，总计 104 课，由主入口 `\input`） |
| `modul2_tests/`, `modul3_tests/`, `modul4_tests/` | DU3 Modul 2 / Modul 3 / Modul 4 模考四套卷（`tests/Test01–04.tex`） |
| `dist/` | **已提交**的成品：9 本 PDF + `practice/index.html`（交互练习单文件） |
| `interactive/` | 交互练习：`extract.py`（tex → YAML 题库）、`data/<book>/LNN.yaml`、`template.html`、`build.py`（YAML → `dist/practice/index.html`） |
| `audio/` | 课文与生词音频：`script.py`（tex → 朗读稿 `scripts/<book>/LNN.yaml`）、`cast.yaml`（角色 → 声音）、`tts.py`（Vertex AI Gemini TTS → `dist/practice/audio/*.m4a` + `manifest.json`）、`voices.py`（声音试听）、`common.py` |
| `publish.ps1` | 多轮 XeLaTeX 编译全部 PDF 到 `dist/`（`-SyncDrive` 仅作者本人使用，不要在 CI 或替用户运行） |
| `.github/workflows/build-and-release.yml` | CI：编译 PDF、生成练习页、更新 Release、部署 GitHub Pages |

## 常用命令

```powershell
.\publish.ps1                            # 编译全部 PDF（需要 TeX Live xelatex + Charis SIL + Noto CJK）
python interactive/extract.py --check    # 只检查 tex → 题库的抽取报告，不写文件
python interactive/extract.py --force    # 课文 .tex 改动后重新生成题库（跳过 hand-made 文件）
python interactive/build.py              # 校验题库并生成 dist/practice/index.html
```

本地预览练习页：直接双击 `dist/practice/index.html` 即可（数据内嵌，支持 `file://`）。
浏览器自动化工具打不开 `file://` 时，在 `dist/practice` 下临时运行 `python -m http.server 8765 --bind 127.0.0.1`，用完要关掉。

## 课文 LaTeX 约定（交互练习依赖这些格式）

`extract.py` 按固定结构解析每课，修改课文时请保持：

- 课首 `\ncdlesson{编号}{丹麦语标题}{中文标题}{对标说明}{语法要点}{导语}`，前 5 个参数会被读取。
- 生词表放在 `\begin{glosertable}`，每行四列：`词性 & 原形 & \textit{(变化形式)} & 中文释义 \\`。
- 练习放在 `\ncdsubsec{五、Mønsterøvelser…}` 下，标题写成行首的 `\textbf{练习 A：说明}`，题目用 `enumerate`（少数用 `tabularx` 两栏，形如 `1. … & 5. … \\`）。填空的横线一律写 `\underline{\hspace{..}}`。
- 答案放在 `answerbox` 里，标题写成行首的 `\textbf{练习 A 答案…}`，条目顺序和数量必须与题目一一对应。
- 答案里的丹麦语用 `\textit{}`、`\da{}` 或 `\dabold{}` 标出，中文解析放在全角括号 `（…）` 里；备选答案用 ` / ` 或“或”连接；表示“不填”的写 `$\times$`。
- 答案标题里含“参考”的题组会被视为开放式改写（网页允许学生自评）。

改完课文后运行 `extract.py --check`，确认报告为 `review items: 0`，再运行 `--force` 和 `build.py`。

## 交互练习

- 题库 YAML 是生成物，但可以手工修改；手工修改过的文件要在**第一行**加 `# hand-made`，否则下次 `--force` 会覆盖。目前 `data/ncd2/L05.yaml` 是人工精编版。
- 分节类型：`flashcards`、`order`、`drill`（条目分 `cloze`/`write`），以及 L05 专用的 `transform`、`correct`、`translate`。新增类型时要同时修改 `build.py` 的 `REQUIRED`/校验逻辑和 `template.html` 的渲染。
- 填空题中，空格用 `{{_}}` 表示，斜体丹麦语用 `⟦…⟧` 标出；`blanks` 的数量必须等于 `{{_}}` 的数量（`build.py` 会校验）。
- `template.html` 是单文件，CSS 和 JS 全部内联，不依赖外部资源；必须保证离线可用，并支持深色模式和手机宽度。
- 修改模板或题库后的验证方法：在页面里把每道题的标准答案代入 `grade` / `blankOk`，确认全部判为正确；再把每课每题各渲染一遍，确认没有报错，页面上也没有出现 `null`。

- 分节类型 `text`（课文/生词表点读）不在题库 YAML 里，由 `build.py` 从 `audio/scripts/` 朗读稿生成并插在每课最前面；`manifest.json` 里有录音的句子带 `a`（片段 key）和 `dur`，网页优先播放录音，没有时退回浏览器 `speechSynthesis`。

## 课文音频

流程：`.tex` → `audio/script.py` → 朗读稿 `audio/scripts/<book>/LNN.yaml` → `audio/tts.py` → `dist/practice/audio/<key>.m4a` + `audio/manifest.json` → `interactive/build.py`。

```powershell
python audio/script.py --all              # 课文改动后重新生成朗读稿（跳过 hand-made 文件）
python audio/tts.py ncd2/L05 --qa         # 只合成缺的片段；--qa 用 gemini-3.8-flash 盲听转写核对
python audio/tts.py --all --qa --prune    # 全部课；--prune 删除不再被引用的片段
python interactive/build.py               # 把朗读稿和录音写进练习页
```

- 凭据：服务账号 JSON 放在仓库**外**，用用户环境变量 `GOOGLE_APPLICATION_CREDENTIALS` 指向它；绝不提交密钥（`.gitignore` 已覆盖常见文件名）。项目 ID 默认取自密钥（`NCD_GCP_PROJECT` 可覆盖），`NCD_GCP_LOCATION` 可改区域（默认 `global`）。
- 模型 `gemini-3.8-flash-tts`（不要用 2.5-pro）。声音在 `audio/cast.yaml`：旁白/学习者 Charon，男声 Iapetus，女声 Leda，同一对话里需要第二个女声时用 Kore。新增人物要加进 `roles`，并确认同一段对话里没有两人同声。
- `common.STYLE` 必须保持为空：3.8-flash-tts 会把文字里的风格提示一起读出来，`system_instruction` 则直接 400。
- 片段按 `sha256(model␟voice␟style␟text)` 寻址：改文字或换声音只重新合成受影响的句子。原始 WAV 缓存在 `audio/cache/`（不提交）；编码后的 m4a 和 `manifest.json` **要提交**，Pages 部署时会把 `dist/practice/audio/` 一起发布。
- 缩写、邮箱等模型读错的写法，优先加到 `cast.yaml` 的 `lexicon`（只替换送去合成的文字，网页显示不变，朗读稿仍可重新生成）。
- 个别句子读错（时态、漏词）时，换一次“take”通常就好：把 `audio/cache/` 里对应的 WAV 移走再重跑 `tts.py`，会重新合成。
- 朗读稿可以手改：读法和显示不同时（数字、缩写、填空题空格、TTS 读错的词）在该句加 `say:`，并在文件**第一行**加 `# hand-made: 原因`，否则 `script.py --all` 会覆盖。现有：`scripts/ncd2/L14.yaml`。
- 考试格式课文里只剩空格的句子（`(1) ___`、`Sara (2): ___`）由 `script.py` 标成 `mute: true`：网页照常显示，但不合成、不播放。对话气泡里 `Name (n):` 和 `A. Name:` 会识别为说话人（人名需在 `cast.yaml` 的 `roles` 里）。
- QA 报告写在 `audio/qa/`（不提交）；低于 0.92 的句子要人工试听。转写模型对拼写变体（如 smilte/smilede）和极短单词常误报，不一定是 TTS 的错。
- 配额较低：`tts.py` 用 3 个并发，429/5xx 指数退避重试；中断后直接重跑即可，已有片段会跳过。

## 发布流程

- 一直直接在 `main` 上提交并推送；推送到 `main` 后，CI 会覆盖更新当前最新 Release 的附件，并重新部署 Pages。
- 发布新版本：`git tag -a vX.Y.Z -m "…" && git push origin vX.Y.Z`，CI 会新建该版本的 Release（附 9 本 PDF 和 `NCD_Practice.html`）。已有版本：v1.2.0、v1.3.0、v1.4.0、v1.5.0、v1.6.0、v1.7.0。
- Pages 地址：<https://jaehaerysrl.github.io/new-concept-danish/practice/>（Source = GitHub Actions，由 `deploy-practice` job 部署）。`github-pages` 环境只允许 main 部署，所以这个 job 只在 main 上运行，tag 运行时会跳过（属正常情况）。
- 新增一本书（如 NCD 3 / NCD 4）时需要同时修改：`publish.ps1` 的 `$Jobs`、workflow 里复制 Release 资产的步骤和 release notes、`extract.py` 的 `BOOKS`、`template.html` 的 `BOOK_NAMES`、README 的下载表格。

## 写作风格

- 教材正文：中文讲解，丹麦语例句；丹麦语用 `\textit`，需要强调的语序或词形用 `\dabold`，IPA 用 `\ipa`。
- README 和面向读者的文档用中文。

## 许可证

GPL-3.0（见 `LICENSE`）。新增文件不需要逐个加许可证头。
