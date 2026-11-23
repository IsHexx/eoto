# eoto

**Enterprise Operations, To One.** — 一个大脑，跑通整家公司 / 万象业务，归一智控。

`eoto`（读作“伊奥托” / `ee-oh-toh`）是面向企业的全业务 AI 协同平台。平台以 `eoto Core` 为核心中枢，统一调度各业务域的子 Agent 协同作业。

## 产品矩阵

- **`eoto Link`**：接入钉钉、飞书与企业微信，提供交互入口与审批流连接。
- **`eoto Core`**：理解自然语言指令，拆解跨部门任务并调度各子 Agent。
- **`eoto Sales`**：管理销售线索、客户跟进、报价单、合同与回访提醒。
- **`eoto Flow`**：承接签单，管理查库存、锁定库存、采购、发货与交付流转。
- **`eoto Cash`**：聚焦经营财务，管理应收应付、自动催款、单笔订单毛利核算与现金流预测。
- **`eoto Studio`**：承载客户专属 Prompt、业务规则库、工作流与行业插件，不修改底层主干源码即可交付定制需求。

## 仓库矩阵

本仓库是 `eoto` 的主仓库，存放规范、文档与契约。各产品的实现代码存放在独立的产品仓库中：

- `eoto-core`：实现 `eoto Core`。
- `eoto-link`：实现 `eoto Link`。
- `eoto-sales`：实现 `eoto Sales`。
- `eoto-flow`：实现 `eoto Flow`。
- `eoto-cash`：实现 `eoto Cash`。
- `eoto-studio-sdk`：实现 `eoto Studio SDK`。

仓库职责与跨仓库协作规则见 [仓库结构与代码组织规范](./docs/仓库结构与代码组织规范.md)。

## 项目文档

- [仓库结构与代码组织规范](./docs/仓库结构与代码组织规范.md)

- [项目立项与战略决策纪要](./docs/项目立项与战略决策纪要.md)
- [品牌定位、品牌故事与产品矩阵命名体系](./docs/品牌定位与产品矩阵命名体系.md)
- [统一术语表与经批准词汇库](./docs/standards/统一术语表.md)
- [文档写作规范（ASD-STE100 适配版）](./docs/standards/文档写作规范.md)
- [项目工作总规矩（AGENTS.md）](./AGENTS.md)

## 文档治理与规范校验

所有人类成员与 AI Agent 编写或修改 Markdown 文档时，必须遵守 `统一术语表.md` 与 `文档写作规范.md`。

文档定稿前，作者应调用文档规范守护者（`eoto-doc-steward`）审查术语与句法，并运行校验脚本：

```bash
python3 .agents/plugins/eoto-doc-steward/skills/eoto-ste-writing/scripts/check_docs.py docs README.md AGENTS.md .agents/plugins/eoto-doc-steward/rules/AGENTS.md
```
