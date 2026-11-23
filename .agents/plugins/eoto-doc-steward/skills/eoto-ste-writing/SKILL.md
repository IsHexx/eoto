---
name: eoto-ste-writing
description: >-
  Use this skill when creating, ingesting, auditing, or rewriting any Markdown
  documentation in the eoto repository to enforce the canonical glossary and
  ASD-STE100 writing rules.
---

# eoto 受控文档编写与审查工作流

本技能指导 Agent 按照 `eoto` 统一术语表与 ASD-STE100 适配规范编写、收录与审查 Markdown 文档。

## 执行步骤

### 第一步：加载权威规范

读取以下两个文件，建立当前项目的术语与规则上下文：

- [统一术语表.md](../../../../../docs/standards/统一术语表.md)
- [文档写作规范.md](../../../../../docs/standards/文档写作规范.md)

### 第二步：统一术语与登记新词

1. 扫描目标文档中的品牌名、模块名、数据实体、角色名与技术动词。
2. 将所有非标准别名替换为 `docs/standards/统一术语表.md` 中的标准术语。
3. 如果文档引入了新的核心业务或架构名词，先在 `docs/standards/统一术语表.md` 中新增条目（含标准词、英文标识、词性、唯一释义与禁用别名），再在正文中使用。

### 第三步：逐项执行 ASD-STE100 改写

按以下清单改写目标文档：

1. **中文命名与客观措辞**：除 `README.md`、`AGENTS.md`、`SKILL.md` 等约定俗成的英文文件名外，文档文件使用中文命名。正文使用中文，专业术语正常保留英文。将比喻、拟人、黑话、情绪化修饰词、空泛修辞与冗余双引号全部改写为标准互联网产品与架构术语。
2. **用词选择**：消除多义词与名词化动词（规则 3.7），移除英文短语动词（规则 9.3）。
3. **动词形式**：英文仅保留六种批准形态，删除完成时与动词性 `-ing`。中文删除 `进行了`、`开展了` 等空泛动词。
4. **语态**：将所有操作步骤、规范说明与架构要求改为主动语态，明确主语。
5. **句法**：拆分包含多条指令的长句，控制英文 20/25 词、中文 30/40 字上限，压缩超过 3 词的名词串，删除所有正文分号（规则 8.1）。
6. **段落结构**：每段保留一个主题且不超过 6 句话。将步骤、条件和复杂枚举改为垂直列表。
7. **安全与高危须知**：将涉及资金、库存、权限、人工确认与源码红线的要求提前至句首，用明确命令或条件开头。

### 第四步：运行自动化校验脚本

执行以下命令验证文档合规性：

```bash
python3 .agents/plugins/eoto-doc-steward/skills/eoto-ste-writing/scripts/check_docs.py docs README.md AGENTS.md
```

修复所有 `ERROR` 级别问题。逐条核查 `WARN` 级别提示并优化超长句或潜在被动语态。
