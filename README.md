# 项目工作汇报 Skill

用 Codex 将 Git 提交、工作日报和微信群聊记录整理成中文周报、月报或阶段总结。按项目或子系统输出「项目 / 子系统｜核心工作清单｜主要成果」三列表格，合并重复事项，并根据记录区分已提交、已测试、已验收和已上线等状态。

## 安装到 Codex

将整个仓库克隆到用户级 Skill 目录。

**Windows（PowerShell）**

```powershell
git clone https://github.com/hjw-alt/project-work-report.git "$env:USERPROFILE\.agents\skills\project-work-report"
```

**macOS / Linux**

```bash
git clone https://github.com/hjw-alt/project-work-report.git "$HOME/.agents/skills/project-work-report"
```

也可以在仓库页面选择 **Code → Download ZIP**，解压后把含有 `SKILL.md` 的文件夹命名为 `project-work-report`，放到用户主目录下的 `.agents/skills/` 中。

## 使用示例

在 Codex 中打开要汇报的 Git 仓库，再输入下面的指令。

> 用 $project-work-report 整理当前仓库 2026 年 10 月的 Git 提交，按业务模块生成月报，列出核心工作和主要成果。

也可以上传日报和微信群聊导出，按项目合并多种材料。

> 用 $project-work-report 把这几份日报和群聊记录整理成项目周报。同一事项合并，标明已完成和待确认的成果。

仓库附有[虚构汇报示例](references/report-example.md)和[本地 Git 取数说明](references/git.md)。
