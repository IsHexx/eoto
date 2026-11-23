# eoto 文档与术语治理规则

在 `eoto` 仓库中创建或修改任何 Markdown 文档时，所有 Agent 必须遵守以下规定：

1. **中文文件命名与客观措辞**：除 `README.md`、`AGENTS.md`、`SKILL.md` 等约定俗成的英文文件名外，所有业务与规范文档的文件名统一使用中文。正文默认使用中文，专业术语按习惯正常保留英文。统一使用标准的互联网产品与架构术语，严禁使用比喻、拟人表达、黑话、情绪化修饰词、空泛修辞与不必要的双引号（正反例见 `docs/standards/文档写作规范.md`）。
2. **先查术语表**：编写文档前，查阅 `docs/standards/统一术语表.md`，统一使用标准术语（如 `eoto Core`、`eoto Link`、`eoto Sales`、`eoto Flow`、`eoto Cash`、`eoto Studio`、`企业微信`、`人工确认`）。
3. **严守 ASD-STE100 规范**：遵守 `docs/standards/文档写作规范.md`。正文中绝对禁止分号（`;` 与 `；`），优先主动语态与短句，每段不超过 6 句话，高危约束必须前置命令或条件。
4. **委托审查与自动校验**：文档定稿前，优先调用 `eoto-doc-steward` 子 Agent 审查，并运行 `python3 .agents/plugins/eoto-doc-steward/skills/eoto-ste-writing/scripts/check_docs.py` 验证通过。
