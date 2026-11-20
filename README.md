# 《新概念丹麦语 1–5》（Ny Koncept Dansk, NCD）

[![Build and Release PDFs](https://github.com/JaehaerysRL/new-concept-danish/actions/workflows/build-and-release.yml/badge.svg)](https://github.com/JaehaerysRL/new-concept-danish/actions/workflows/build-and-release.yml)
[![Latest Release PDF](https://img.shields.io/github/v/release/JaehaerysRL/new-concept-danish?label=Release%20PDF&color=C8102E)](https://github.com/JaehaerysRL/new-concept-danish/releases/latest)
![DU3 Alignment](https://img.shields.io/badge/DU3-Modul%201--5%20%7C%20CEFR%20A1--C1-1B365D)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-006D77.svg)](./LICENSE)

效仿《新概念英语》（*New Concept English*）**「螺旋式递进语法大纲 + 高复现率短文 + 固定句型操练」**的自学体系，面向中文母语者，并深度对标丹麦官方语言教育 **DU3（Danskuddannelse 3）Modul 1–5 / PD3 → Studieprøven** 考核标准。

---

## 📥 免配环境 · PDF 电子书直接下载（GitHub Releases）

> [!TIP]
> **没有安装 LaTeX？无需配置任何编译环境！**
> 每次代码更新都会通过 GitHub Actions 自动编译并上传最新带书签的成品 PDF 到 **[GitHub Releases（点击进入发布页）](https://github.com/JaehaerysRL/new-concept-danish/releases/latest)**，下方表格也可一键直链下载：

| 电子书分册 | 对应水平 | 核心内容概要 | 页数 | 📦 Release 一键下载 | 📄 仓库 `dist/` |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **总目录与螺旋式语法大纲**<br>*00 NCD Syllabus* | 全 5 册 104 课<br>(A1 → C1) | 五册螺旋语法总矩阵、104 课分课语法靶点、30 天 DU3 Modul 2 速通路线 | 13 页 | [下载 `00_NCD_Syllabus.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/00_NCD_Syllabus.pdf) | [`dist/` 版](./dist/00_%E6%96%B0%E6%A6%82%E5%BF%B5%E4%B8%B9%E9%BA%A6%E8%AF%AD_%E6%80%BB%E7%9B%AE%E5%BD%95%E4%B8%8E%E8%AF%AD%E6%B3%95%E5%A4%A7%E7%BA%B2.pdf) |
| **NCD 1 · 起步篇**<br>*Første Skridt* | DU3 Modul 1<br>(A1 → A2-) | 全 6 单元 24 课：软 `d`/吞音/重音 IPA、情景对话、V2 倒装、基础时态与独白模板 | 156 页 | [下载 `NCD1_Foerste_Skridt.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/NCD1_Foerste_Skridt.pdf) | [`dist/` 版](./dist/NCD1_Foerste_Skridt.pdf) |
| **NCD 2 · 进阶篇**<br>*Fra Sætning til Tekst* | DU3 Modul 2<br>(A2) | 全 4 单元 24 课：从句语序、完成时 vs 过去时、核心连词、70+ 词邮件写作与阅读题型训练 | 181 页 | [下载 `NCD2_Fra_Saetning_til_Tekst.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/NCD2_Fra_Saetning_til_Tekst.pdf) | [`dist/` 版](./dist/NCD2_Fra_Saetning_til_Tekst.pdf) |
| **DU3 Modul 2 全真模考四套卷**<br>*4 Komplette Modultests* | SIRI / Modultest<br>2024–2025 (A2) | `Modultest 1–4` 完整试卷（阅读 24 分 + 邮件 + 口语 Mindmap/信息差）+ 评分卡 + 逐题精析 + A2/A2+ 范文 | 76 页 | [下载 `NCD2_DU3_Modul2_Modultest_1_4.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/NCD2_DU3_Modul2_Modultest_1_4.pdf) | [`dist/` 版](./dist/NCD2_DU3_Modul2_Modultest_1_4.pdf) |
| **NCD 3 · 社会篇**<br>*Hverdag og Samfund* | DU3 Modul 3<br>(B1) | 全 4 单元 20 课：`-s`/`blive` 被动、介词 + 形式宾语 `det` + 从句、无 `hvis` 条件倒装、投诉/推荐信与长语篇 | 152 页 | [下载 `NCD3_Hverdag_og_Samfund.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/NCD3_Hverdag_og_Samfund.pdf) | [`dist/` 版](./dist/NCD3_Hverdag_og_Samfund.pdf) |
| **DU3 Modul 3 全真模考四套卷**<br>*4 Komplette Modultests til Modul 3* | SIRI / Modultest<br>2025–2026 (B1) | `Modultest 1–4` 完整试卷（50 min/24 分制阅读五题型 + 投诉/推荐与 90+ 词邮件 + Mindmap/四图互动）+ 双档 B1/B1+ 范文 | 94 页 | [下载 `NCD3_DU3_Modul3_Modultest_1_4.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/NCD3_DU3_Modul3_Modultest_1_4.pdf) | [`dist/` 版](./dist/NCD3_DU3_Modul3_Modultest_1_4.pdf) |
| **NCD 4 · 思辨篇**<br>*Holdning og Debat* | DU3 Modul 4<br>(B1+ → B2-) | 全 4 单元 20 课：情态小品词、口语转书面、让步反驳、因果条件长句与 `Debatindlæg` 观点辩论写作 | 172 页 | [下载 `NCD4_Holdning_og_Debat.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/NCD4_Holdning_og_Debat.pdf) | [`dist/` 版](./dist/NCD4_Holdning_og_Debat.pdf) |
| **DU3 Modul 4 全真模考四套卷**<br>*4 Komplette Modultests til Modul 4* | SIRI / Modultest<br>2026 (B1+ → B2-) | `Modultest 1–4` 完整试卷（50 min/29 分制阅读四部分 8+5+10+6 + 125+ 词回信 & 100+ 词 `Blogindlæg` + `Emneopgave` & `Individuel → Paropgave`）+ B1+/B2- 双档范文 | 109 页 | [下载 `NCD4_DU3_Modul4_Modultest_1_4.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/NCD4_DU3_Modul4_Modultest_1_4.pdf) | [`dist/` 版](./dist/NCD4_DU3_Modul4_Modultest_1_4.pdf) |
| **NCD 5 · 精研篇**<br>*Tanke og Perspektiv* | PD3 (Modul 5) →<br>Studieprøven (B2 → C1) | 全 4 单元 16 课：统计图表三步分析法、低调反讽（*Underdrivelse/Litote*）、引述立场光谱、文化不可译词、多源综述（*Syntese*）与双语散文 | 153 页 | [下载 `NCD5_Tanke_og_Perspektiv.pdf`](https://github.com/JaehaerysRL/new-concept-danish/releases/latest/download/NCD5_Tanke_og_Perspektiv.pdf) | [`dist/` 版](./dist/NCD5_Tanke_og_Perspektiv.pdf) |

---

## 🎯 教材体系与编写进度

本系列坚持**每册可独立编译、自动生成 PDF 书签与可断页表格/框体**（避免大段留白，适合 iPad / 平板 / 电脑跨平台阅读与打印）。

### 1. 五册规划总览

| 分册 | 书名 | 对标《新概念英语》 | DU3 / CEFR | 篇幅与课数 | 状态 |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **总大纲** | 《总目录与螺旋式语法大纲》 | 体系总图 | 全阶段 | 104 课总规划 | ✅ 已完成 |
| **NCD 1** | *Første Skridt*（起步篇） | NCE 1 | Modul 1 (`A1 → A2-`) | 6 单元 · 24 课 | ✅ 已完成 |
| **NCD 2** | *Fra Sætning til Tekst*（进阶篇） | NCE 2 前半 | Modul 2 (`A2`) | 4 单元 · 24 课 | ✅ 已完成 |
| **M2 模考卷** | *DU3 Modul 2 全真模考四套卷* | 剑桥雅思真题集体例 | Modultest.dk (2024/2025) | 4 套零重复真题卷 | ✅ 已完成 |
| **NCD 3** | *Hverdag og Samfund*（社会篇） | NCE 2 后半 → NCE 3 前半 | Modul 3 (`B1`) | 4 单元 · 20 课 | ✅ 已完成 |
| **M3 模考卷** | *DU3 Modul 3 全真模考四套卷* | 剑桥雅思真题集体例 | Modultest.dk (2025/2026) | 4 套零重复真题卷 | ✅ 已完成 |
| **NCD 4** | *Holdning og Debat*（思辨篇） | NCE 3 | Modul 4 (`B1+ → B2-`) | 4 单元 · 20 课 | ✅ 已完成 |
| **M4 模考卷** | *DU3 Modul 4 全真模考四套卷* | 剑桥雅思真题集体例 | Modultest.dk (2026) | 4 套零重复真题卷 | ✅ 已完成 |
| **NCD 5** | *Tanke og Perspektiv*（精研篇） | NCE 4 | PD3 (Modul 5) → Modul 6 (`B2 → C1`) | 4 单元 · 16 课 | ✅ 已完成 |

### 2. 编写特色

- **精准 IPA 丹麦语标音**：采用 `Charis SIL` 字体完整渲染声门喉塞音 `[ˀ]` 与软 `d` `[ð]`，辅以连读与吞音感知提示。
- **完整屈折生词表**：名词标注完整四态（不定/定指/复数/定指复数），动词标注完成时助动词 `[har]` / `[er]` 与不规则变化。
- **中文语法对比拆解**：直击英语思维惯性易错点（V2 倒装、从句 `ikke/altid` 前置、`sin/sit/sine` 反身物主代词、完成时 vs 过去时切换）。
- **全真 DU3 Modul 2 模考卷**：`Modultest 1–4` 严格还原 40 分钟 24 分制阅读四题型（16 分及格）、70+ 词私人与半正式邮件双任务、Mindmap 独白与 6 格 `Informationskløft` 信息差题卡，并附同义转述解析与高分示范。
- **全真 DU3 Modul 3 模考卷**：`Modultest 1–4` 严格对标 2025/2026 官方考纲——50 分钟 24 分制阅读五部分（15 分及格，含气泡聊天补全 `Opg 2A/2B`、段内插句 `Opg 3`、三人匹配 `Opg 4`）、投诉/推荐信 + 90+ 词邮件双任务、`Mindmap` 禁选提醒与四图 `Paropgave` 互动卡，并配 B1/B1+ 双档范文与 IPA 口语逐字稿。
- **全真 DU3 Modul 4 模考卷**：`Modultest 1–4` 严格对标 2026 官方考纲——50 分钟 29 分制阅读四部分（`8 + 5 + 10 + 6`，含无词库开放完形 `Opg 3` 10 题）、125+ 词朋友邮件 + 100+ 词 `Blogindlæg` 观点辩论帖双任务、纯 `stikord` `Emneopgave` 陈述卡与先单人（`ca. 3 min./人`）后双人（`ca. 4 min.`）`Paropgave` 社会利弊互动卡，并配 B1+/B2- 双档范文与 IPA 口语辩论逐字稿。
- **NCD 5 高阶精研体系**：紧扣 PD3 与 Studieprøven 考核要求——覆盖统计图表黄金三步分析法、丹麦语低调反讽与曲言（*Underdrivelse/Litote*）、报刊社论与引述立场光谱、丹麦文化核心不可译词（*dannelse/tryghed/fællesskab*）以及双背景材料多源综述（*Syntese*）。

---

## 📂 仓库结构

```text
new-concept-danish/
├── .github/
│   └── workflows/
│       └── build-and-release.yml      # GitHub Actions 自动编译 PDF 并更新 Release 流水线
├── common/
│   └── ncd-style.sty                  # 统一教材 LaTeX 样式宏包（中丹混排 + 跨平台字体回退 + Charis SIL IPA）
├── syllabus/
│   └── 00_NCD_Syllabus.tex            # 《总目录与螺旋式语法大纲》（1–5 册，104 课）
├── ncd1/
│   ├── NCD1_Book.tex                  # 第一册主入口（Første Skridt，对标 Modul 1）
│   └── lessons/L01.tex ... L24.tex    # 单课独立模块
├── ncd2/
│   ├── NCD2_Book.tex                  # 第二册主入口（Fra Sætning til Tekst，对标 Modul 2）
│   └── lessons/L01.tex ... L24.tex    # 单课独立模块
├── modul2_tests/
│   ├── NCD2_Modultest_Book.tex        # DU3 Modul 2 全真模考四套卷主入口
│   └── tests/Test01.tex ... Test04.tex# 4 套全真模考试卷（阅读/写作/口语/详解）
├── ncd3/
│   ├── NCD3_Book.tex                  # 第三册主入口（Hverdag og Samfund，对标 Modul 3）
│   └── lessons/L01.tex ... L20.tex    # 单课独立模块
├── modul3_tests/
│   ├── NCD3_Modultest_Book.tex        # DU3 Modul 3 全真模考四套卷主入口
│   └── tests/Test01.tex ... Test04.tex# 4 套全真模考试卷（阅读/写作/口语/详解）
├── ncd4/
│   ├── NCD4_Book.tex                  # 第四册主入口（Holdning og Debat，对标 Modul 4）
│   └── lessons/L01.tex ... L20.tex    # 单课独立模块
├── modul4_tests/
│   ├── NCD4_Modultest_Book.tex        # DU3 Modul 4 全真模考四套卷主入口
│   └── tests/Test01.tex ... Test04.tex# 4 套全真模考试卷（阅读/写作/口语/详解）
├── ncd5/
│   ├── NCD5_Book.tex                  # 第五册主入口（Tanke og Perspektiv，对标 PD3 → Studieprøven）
│   └── lessons/L01.tex ... L16.tex    # 单课独立模块（全系列 104 课收官）
├── interactive/                       # 交互练习：题库抽取、YAML 题库、网页模板与构建脚本
├── audio/                             # 课文朗读稿、角色配音表与 TTS 合成脚本（录音输出到 dist/practice/audio/）
├── dist/                              # 编译生成的带书签完整分册 PDF + practice/index.html 练习页
├── publish.ps1                        # 一键多轮 XeLaTeX 编译与可选 Google Drive 同步脚本
├── CLAUDE.md                          # 给 Claude Code 的项目维护说明
└── LICENSE                            # GPL-3.0
```

---

## 🛠️ 本地编译与环境配置教程

如果你只需要**阅读或打印 PDF**，请直接前往上方的 [GitHub Releases](https://github.com/JaehaerysRL/new-concept-danish/releases/latest) 下载，跳过本节即可。
如果你想**修改源码、定制笔记或本地重新编译 PDF**，请按下列步骤配置环境：

### 第一步：安装 TeX Live（需含 `xelatex` 与 `ctex`）

<details>
<summary><b>Windows / macOS / Ubuntu Linux 安装命令与说明（点击展开）</b></summary>

- **Windows（推荐 TeX Live 完整版或基础版 + 中文/表格宏包）**
  1. 下载并安装 [TeX Live](https://tug.org/texlive/windows.html)（需包含 `xelatex`、`ctex`、`xecjk`、`tcolorbox`、`longtable`、`xltabular`、`pifont`、`booktabs`）。
  2. 打开 PowerShell 验证：`xelatex --version`。
- **macOS**
  1. 安装 [MacTeX](https://tug.org/mactex/)（或 `brew install --cask mactex`）及 PowerShell（`brew install --cask powershell`）。
- **Ubuntu / Debian Linux（与 GitHub CI 环境完全一致）**
  ```bash
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends \
    texlive-xetex texlive-latex-recommended texlive-latex-extra \
    texlive-fonts-recommended texlive-pictures texlive-lang-chinese \
    fonts-sil-charis fonts-noto-core fonts-noto-cjk fonts-dejavu-core fontconfig
  sudo fc-cache -fv
  ```

</details>

### 第二步：安装所需字体

1. **必须安装：`Charis SIL`**（正文、丹麦语特殊字母 `æ/ø/å` 及全部国际音标 IPA `[ˀ]`/`[ð]` 依赖此字体）：
   - 下载地址：[SIL Charis SIL 官网](https://software.sil.org/charis/download/)（或 Ubuntu 包 `fonts-sil-charis` / macOS `brew install --cask font-charis-sil`）。
   - 解压后选中 `.ttf` 字体文件，右键 **“为所有用户安装”**（Windows）或双击安装到“字体册”（macOS）。
2. **推荐安装（已有自动回退，未装也可正常编译）**：
   - 无衬线字体：`Noto Sans`（未安装时在 [ncd-style.sty](./common/ncd-style.sty) 中自动回退至 `Arial` 或 `Charis SIL`）
   - 等宽字体：`DejaVu Sans Mono`（未安装时自动回退至 `Consolas` 或 `Charis SIL`）
   - 中文字体：Windows 使用系统自带宋体/黑体，macOS 使用系统自带苹方，Linux CI 自动使用 `Noto Serif CJK SC` / `Noto Sans CJK SC`。

### 第三步：克隆仓库并一键编译

```powershell
# 1. 克隆仓库
git clone https://github.com/JaehaerysRL/new-concept-danish.git
cd new-concept-danish

# 2. 一键编译全套 9 本 PDF 到 dist/（脚本会自动运行多遍 XeLaTeX 直到目录/书签/表格宽度收敛）
.\publish.ps1          # Windows PowerShell
# pwsh ./publish.ps1   # macOS / Linux PowerShell
```

> [!NOTE]
> 如果你只修改了某一本教材，也可进入对应目录单独用 `xelatex` 编译两至三遍：
> ```powershell
> cd modul3_tests
> xelatex -interaction=nonstopmode -halt-on-error NCD3_Modultest_Book.tex
> xelatex -interaction=nonstopmode -halt-on-error NCD3_Modultest_Book.tex
> ```
> 脚本中的 `.\publish.ps1 -SyncDrive` 参数依赖个人环境已认证的 `gdrive` CLI 与目标云盘文件夹 ID，仅供作者本人同步 Google Drive 使用；普通本地编译不加 `-SyncDrive` 即可。

---

## 🧩 交互练习（NCD 1–5 全五册 104 课）

- **在线版**：<https://jaehaerysrl.github.io/new-concept-danish/practice/>（手机、平板可直接打开）
- **离线版**：克隆仓库后直接双击 [`dist/practice/index.html`](./dist/practice/index.html)，无需联网（录音在同目录的 `audio/` 里）；Release 中的单文件 `NCD_Practice.html` 不带录音，朗读会退回浏览器自带的语音

每课开头是**课文点读**：NCD 1 对话/独白、NCD 2–4 的 Tekst A/B 及生词表全部配有预录制的 Gemini TTS 录音（旁白 Charon，男声 Iapetus，女声 Leda/Kore），可以点句播放、全部连播、0.75×/1×/1.25× 变速、开关中文翻译，以及“跟读停顿”（每句后留出与原句等长的跟读时间）；NCD 5 全部 16 课同样已生成 `Tekst A/B` 与 `Gloser` 点读板块（当前由浏览器自带 `speechSynthesis` 语音引擎朗读，待后续补充独立录音）。考试格式课文里只剩空格的句子照常显示，但不朗读。

之后是生词闪卡、语序拼句，以及与 PDF 同步的练习 A/B/C（句中填空、改写、纠错、中译丹），带自动判分、错词高亮、书中解析和丹麦语朗读；开放式改写题可以自评“我的答案也对”。学习进度只保存在本机浏览器里。

题库每课一个 YAML 文件，由脚本从 `.tex` 课文中抽取：

```text
interactive/
├── data/ncd1/L01.yaml … data/ncd5/L16.yaml   # 题库：flashcards / order / drill（cloze、write）
├── extract.py           # 从 ncd*/lessons/*.tex 生成题库（生词表 + 练习 A/B/C 及答案）
├── template.html        # 单文件网页模板（内联 CSS/JS）
└── build.py             # 校验题库并生成 dist/practice/index.html
```

需要 Python 3 与 `pip install pyyaml`：

```powershell
python interactive/extract.py --force   # 课文 .tex 改动后重新抽取题库
python interactive/build.py             # 生成练习页
```

> [!NOTE]
> 首行带 `# hand-made` 标记的题库（如 `data/ncd2/L05.yaml`）是人工精编版，`extract.py --force` 不会覆盖。手工修改过某课题库后，加上这一行即可保护你的改动。

> [!TIP]
> 朗读功能使用系统自带的语音引擎。Windows 用户如果听到的不是丹麦语口音，可以在「设置 → 时间和语言 → 语音」里添加 **Dansk** 语音包。

---

## ⚙️ CI/CD 自动化流水线与发布机制

本项目配置了 [`.github/workflows/build-and-release.yml`](./.github/workflows/build-and-release.yml) 自动化流水线：

1. **自动编译校验（CI）**：每次向 `main` 分支推送代码、提交 Pull Request 或发布 `v*` 标签时，GitHub Actions 会在 `ubuntu-latest` 中自动安装 `XeLaTeX` + `Charis SIL` + `Noto CJK` 并执行 `pwsh ./publish.ps1`。
2. **工作流产物归档**：每次构建都会将最新 9 本 PDF 上传为 Workflow Artifact（`ncd-books-pdf`）。
3. **GitHub Release 自动发布/刷新（CD）**：
   - 推送版本标签（例如 `git tag -a v1.6.0 -m "..." && git push origin v1.6.0`）时，自动创建对应的版本 Release 并附上 9 本 PDF；
   - 平时直接向 `main` 推送更新或修错时，自动将最新编译的 PDF 覆盖更新（`--clobber`）到当前最新 Release 中，确保 [Releases 页面](https://github.com/JaehaerysRL/new-concept-danish/releases/latest) 始终提供最新可下载版本。
4. **交互练习部署**：同一流水线会运行 `interactive/build.py`，把练习页作为 `NCD_Practice.html` 附到 Release，并部署到 [GitHub Pages](https://jaehaerysrl.github.io/new-concept-danish/practice/)。

---

## 📜 许可证

本项目（LaTeX 源码、编译出的 PDF、交互练习的代码与题库）以 [GNU General Public License v3.0](./LICENSE) 发布。
你可以自由使用、修改和再分发；分发修改版时，需要同样以 GPL-3.0 公开源码并保留版权与许可声明。
