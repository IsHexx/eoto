# eoto

**Enterprise Operations, To One.** — 一个大脑，跑通整家公司 / 万象业务，归一智控。

`eoto`（读作“伊奥托” / `ee-oh-toh`）是面向中小企业的 AI 协同平台。`eoto` 围绕订单生命周期构建产品，让经营者随时了解每笔订单的成交、履约、回款与盈利状态。

## 产品矩阵

- **`eoto Link`**：接入钉钉、飞书与企业微信，提供交互入口与审批流连接。
- **`eoto Core`**：平台中枢。主 Agent 理解自然语言指令并调度子 Agent。订单引擎管理订单生命周期。
- **`eoto Sales`**：接单能力。管理线索、客户跟进、报价、签约与回访提醒。
- **`eoto Flow`**：履约能力。支持实物履约与服务履约。
- **`eoto Cash`**：回款能力。管理应收应付、催款提醒、单笔订单毛利与现金流预测。
- **`eoto Studio`**：承载行业模板、Prompt、业务规则库、工作流与行业插件，不修改底层主干源码即可满足行业需求。

`eoto Sales`、`eoto Flow` 与 `eoto Cash` 共用 `eoto Core` 的订单引擎，读写同一份订单数据。

## 仓库结构

本仓库采用单仓库结构，存放全部文档、契约规范与产品代码：

- `docs/`：战略、产品与架构文档。
- `spec/`：主数据模型与契约规范，按契约版本存放。
- `packages/`：各产品的代码包。

目录职责与代码包协作规则见 [仓库结构与代码组织规范](./docs/仓库结构与代码组织规范.md)。

## 项目文档

- [项目立项与战略决策纪要](./docs/项目立项与战略决策纪要.md)
- [品牌定位、品牌故事与产品矩阵命名体系](./docs/品牌定位与产品矩阵命名体系.md)
- [用户画像](./docs/用户画像.md)
- [仓库结构与代码组织规范](./docs/仓库结构与代码组织规范.md)
- [统一术语表与经批准词汇库](./docs/standards/统一术语表.md)
- [文档写作规范（ASD-STE100 适配版）](./docs/standards/文档写作规范.md)
- [项目工作总规矩（AGENTS.md）](./AGENTS.md)

## 文档治理与规范校验

所有人类成员与 AI Agent 编写或修改 Markdown 文档时，必须遵守 `统一术语表.md` 与 `文档写作规范.md`。

文档定稿前，作者应调用文档规范守护者（`eoto-doc-steward`）审查术语与句法，并运行校验脚本：

```bash
python3 .agents/plugins/eoto-doc-steward/skills/eoto-ste-writing/scripts/check_docs.py docs README.md AGENTS.md .agents/plugins/eoto-doc-steward/rules/AGENTS.md
```
