# 《新概念丹麦语 1–5》（Ny Koncept Dansk, NCD）

效仿《新概念英语》（*New Concept English*）**“螺旋式递进语法大纲 + 高复现率短文 + 固定句型操练”**的自学体系，并深度对标丹麦官方语言教育 **DU3（Danskuddannelse 3）Modul 1–5 / PD3 → Studieprøven** 的考核标准。

## 仓库结构

```text
new-concept-danish/
├── common/
│   └── ncd-style.sty                  # 统一教材 LaTeX 样式宏包（中丹混排 + Charis SIL 国际音标）
├── syllabus/
│   └── 00_NCD_Syllabus.tex            # 《总目录与螺旋式语法大纲》（1–5 册，104 课）
├── ncd1/
│   ├── NCD1_Book.tex                  # 第一册主入口（Første Skridt，对标 Modul 1）
│   └── lessons/L01.tex ...            # 单课独立模块
├── ncd2/
│   ├── NCD2_Book.tex                  # 第二册主入口（Fra Sætning til Tekst，对标 Modul 2）
│   └── lessons/L01.tex ...            # 单课独立模块
├── dist/                              # 编译生成的带书签完整分册 PDF（同步至 Google Drive）
└── publish.ps1                        # 一键编译 PDF、同步 Google Drive 与 Git 校验脚本
```

## 编译与发布

环境要求：TeX Live（`xelatex`）+ `Charis SIL` 字体 + `gdrive` CLI（可选云端同步）。

```powershell
# 仅本地编译所有 PDF 到 dist/
.\publish.ps1

# 编译并同步上传/覆盖更新 Google Drive (Dansk/NCD/)
.\publish.ps1 -SyncDrive
```

## 当前编写进度

- [x] **总目录与语法大纲**：`00_新概念丹麦语_总目录与语法大纲.pdf`（全五册 104 课完整规划 + 30 天 Modul 2 速通路线）
- [x] **NCD 1（第 1 册 · 起步篇）**：全册 6 单元共 24 课已全部完成（`NCD1_Foerste_Skridt.pdf`）
- [x] **NCD 2（第 2 册 · 进阶篇）**：L1 样章已完成（`NCD2_Fra_Saetning_til_Tekst.pdf`）
- [ ] **NCD 3–5**：待后续按计划逐步展开
