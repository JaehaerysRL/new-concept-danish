# 《新概念丹麦语 1–5》（Ny Koncept Dansk, NCD）

[![Build and Release PDFs](https://github.com/JaehaerysRL/new-concept-danish/actions/workflows/build-and-release.yml/badge.svg)](https://github.com/JaehaerysRL/new-concept-danish/actions/workflows/build-and-release.yml)
[![Latest Release PDF](https://img.shields.io/github/v/release/JaehaerysRL/new-concept-danish?label=Release%20PDF&color=C8102E)](https://github.com/JaehaerysRL/new-concept-danish/releases/latest)
![DU3 Alignment](https://img.shields.io/badge/DU3-Modul%201--5%20%7C%20CEFR%20A1--C1-1B365D)

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

---

## 🎯 教材体系与编写进度

本系列坚持**每册可独立编译、自动生成 PDF 书签与可断页表格/框体**（避免大段留白，适合 iPad / 平板 / 电脑跨平台阅读与打印）。

### 1. 五册规划总览

| 分册 | 书名 | 对标《新概念英语》 | DU3 / CEFR | 篇幅与课数 | 状态 |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **总大纲** | 《总目录与螺旋式语法大纲》 | 体系总图 | 全阶段 | 104 课总规划 | ✅ 已完成 |
| **NCD 1** | *Første Skridt*（起步篇） | NCE 1 | Modul 1 (`A1 → A2-`) | 6 单元 · 24 课 | ✅ 已完成 |
| **NCD 2** | *Fra Sætning til Tekst*（进阶篇） | NCE 2 前半 | Modul 2 (`A2`) | 4 单元 · 24 课 | ✅ 已完成 |
| **模考卷** | *DU3 Modul 2 全真模考四套卷* | 剑桥雅思真题集体例 | Modultest.dk (2024/2025) | 4 套零重复真题卷 | ✅ 已完成 |
| **NCD 3** | *Hverdag og Samfund*（社会篇） | NCE 2 后半 → NCE 3 前半 | Modul 3 (`B1`) | 20 课 | ⏳ 规划中 |
| **NCD 4** | *Holdning og Debat*（思辨篇） | NCE 3 | Modul 4 (`B1+ → B2-`) | 20 课 | ⏳ 规划中 |
| **NCD 5** | *Tanke og Perspektiv*（精研篇） | NCE 4 | PD3 (Modul 5) → Modul 6 (`B2 → C1`) | 16 课 | ⏳ 规划中 |

### 2. 编写特色

- **精准 IPA 丹麦语标音**：采用 `Charis SIL` 字体完整渲染声门喉塞音 `[ˀ]` 与软 `d` `[ð]`，辅以连读与吞音感知提示。
- **完整屈折生词表**：名词标注完整四态（不定/定指/复数/定指复数），动词标注完成时助动词 `[har]` / `[er]` 与不规则变化。
- **中文语法对比拆解**：直击英语思维惯性易错点（V2 倒装、从句 `ikke/altid` 前置、`sin/sit/sine` 反身物主代词、完成时 vs 过去时切换）。
- **全真 DU3 Modul 2 模考卷**：`Modultest 1–4` 严格还原 40 分钟 24 分制阅读四题型（16 分及格）、70+ 词私人与半正式邮件双任务、Mindmap 独白与 6 格 `Informationskløft` 信息差题卡，并附同义转述解析与高分示范。

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
├── dist/                              # 编译生成的带书签完整分册 PDF
└── publish.ps1                        # 一键多轮 XeLaTeX 编译与可选 Google Drive 同步脚本
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

# 2. 一键编译全套 4 本 PDF 到 dist/（脚本会自动运行多遍 XeLaTeX 直到目录/书签/表格宽度收敛）
.\publish.ps1          # Windows PowerShell
# pwsh ./publish.ps1   # macOS / Linux PowerShell
```

> [!NOTE]
> 如果你只修改了某一本教材，也可进入对应目录单独用 `xelatex` 编译两至三遍：
> ```powershell
> cd modul2_tests
> xelatex -interaction=nonstopmode -halt-on-error NCD2_Modultest_Book.tex
> xelatex -interaction=nonstopmode -halt-on-error NCD2_Modultest_Book.tex
> ```
> 脚本中的 `.\publish.ps1 -SyncDrive` 参数依赖个人环境已认证的 `gdrive` CLI 与目标云盘文件夹 ID，仅供作者本人同步 Google Drive 使用；普通本地编译不加 `-SyncDrive` 即可。

---

## 🧩 交互练习（原型 · 目前收录 NCD 2 L05）

直接双击 [`dist/practice/index.html`](./dist/practice/index.html) 即可离线练习，无需联网或安装任何环境。题型包括生词闪卡、语序拼句、间接疑问句改写、纠错和中译丹，带自动判分、错词高亮和丹麦语朗读；学习进度只保存在本机浏览器里。

题库与 PDF 分开维护，每课一个 YAML 文件：

```text
interactive/
├── data/ncd2/L05.yaml   # 题库：flashcards / order / transform / correct / translate
├── template.html        # 单文件网页模板（内联 CSS/JS）
└── build.py             # 校验题库并生成 dist/practice/index.html
```

新增或修改题目后重新生成（需要 Python 3 与 `pip install pyyaml`）：

```powershell
python interactive/build.py
```

> [!TIP]
> 朗读功能使用系统自带的语音引擎。Windows 用户如果听到的不是丹麦语口音，可以在「设置 → 时间和语言 → 语音」里添加 **Dansk** 语音包。

---

## ⚙️ CI/CD 自动化流水线与发布机制

本项目配置了 [`.github/workflows/build-and-release.yml`](./.github/workflows/build-and-release.yml) 自动化流水线：

1. **自动编译校验（CI）**：每次向 `main` 分支推送代码、提交 Pull Request 或发布 `v*` 标签时，GitHub Actions 会在 `ubuntu-latest` 中自动安装 `XeLaTeX` + `Charis SIL` + `Noto CJK` 并执行 `pwsh ./publish.ps1`。
2. **工作流产物归档**：每次构建都会将最新 4 本 PDF 上传为 Workflow Artifact（`ncd-books-pdf`）。
3. **GitHub Release 自动发布/刷新（CD）**：
   - 推送版本标签（例如 `git tag v1.2.0 && git push origin v1.2.0`）时，自动创建对应的版本 Release 并附上 4 本 PDF；
   - 平时直接向 `main` 推送更新或修错时，自动将最新编译的 PDF 覆盖更新（`--clobber`）到当前最新 Release 中，确保 [Releases 页面](https://github.com/JaehaerysRL/new-concept-danish/releases/latest) 始终提供最新可下载版本。
