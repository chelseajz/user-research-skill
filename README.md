# user-research-skill

`user-research` is a reusable research skill for turning messy product questions, interview data, survey outputs, and draft reports into decision-ready user research deliverables.

It is built for teams that want research outputs to be:
- evidence-based
- methodologically honest
- easy for leadership to scan
- detailed enough for practitioners to act on
- resilient under skeptical review

## What It Does

This skill helps with the full user research workflow:
- research planning and study design
- qualitative coding and synthesis
- survey and crosstab analysis
- mixed-method integration
- research report writing
- executive-ready summarization
- rigorous review and hardening of draft reports

It is especially useful when a team needs to move from:
- scattered interviews to a structured insight system
- fragmented quant and qual outputs to one coherent report
- "interesting observations" to decisions with explicit evidence and confidence
- weak or overclaimed draft reports to stronger, more defensible versions

## What Makes It Different

Compared with lightweight "summarize these notes" prompts, this skill emphasizes:
- denominator discipline
- evidence traceability
- confidence labeling
- sharp separation between observation, interpretation, and recommendation
- realistic handling of research limitations
- better alignment between executive summaries, section titles, body evidence, and action recommendations

It also includes guardrails for common report quality failures such as:
- overstating weak evidence
- mixing incompatible bases or respondent IDs
- burying proof inside appendices or embedded tables
- duplicating recommendation layers
- treating prototype feedback as product validation
- leaving drafting residue in a "final" report

## Automation Model

This skill is intentionally designed for high automation with a small number of required human judgment gates.

The default model is:
- automate the mechanical work
- pause only at the decisions most likely to prevent downstream rework

Most operational steps can be automated:
- cleaning and structuring data
- first-pass coding
- pattern extraction
- quote and case selection
- draft confidence labels
- red-team issue collection
- report formatting and packaging

Human review is concentrated at five checkpoints:
- Opening confirmation: only if decision, audience, or data scope is unclear
- Gate 1: codebook review
- Gate 2: finding classification
- Gate 3: report quality review
- Final sign-off

The most important gate is Gate 2. Candidate findings are explicitly classified as:
- `promote`
- `directional`
- `degrade`
- `add caveat`
- `drop as noise`

The default bias is conservative: do not promote by default.

## Best Use Cases

This repository is a strong fit for:
- product researchers
- PMs and designers doing mixed-method synthesis
- strategy and operations teams writing internal user insight reports
- AI-assisted research workflows that need stronger structure and review discipline

Typical scenarios:
- "Review this report and tell me what is overclaimed."
- "Turn these interviews and crosstabs into one polished report."
- "Help me write an executive-ready user research document."
- "Audit this agency report before I send it upward."
- "Make this demo feedback section more actionable and less repetitive."

## Repository Structure

- [`SKILL.md`](./SKILL.md): main skill instructions and operating rules
- [`references/README.md`](./references/README.md): reference map
- [`references/`](./references): workflow, standards, templates, and review rubrics
- [`scripts/validate_report.py`](./scripts/validate_report.py): report validation helper
- [`generate_research_outputs.py`](./generate_research_outputs.py): generation helper used in this workflow

## Branches

- `codex`: Codex-oriented version of the skill
- `claude`: branch reserved for the Claude-oriented variant
- `main`: shared baseline / repository default

## Design Philosophy

The skill is opinionated about research quality:
- one report should usually be readable by leaders and usable by practitioners
- strong reports should survive format conversion, not just look good in markdown
- research recommendations should be decision-ready, not generic
- product feedback should be structured into concrete friction types
- qualitative quotes should preserve user voice instead of being flattened into abstractions

In short, this repository is meant to help produce research outputs that feel like they were written by a strong human researcher, not a generic AI summarizer.

## Getting Started

1. Start with [`SKILL.md`](./SKILL.md).
2. Use [`references/README.md`](./references/README.md) to navigate the supporting materials.
3. If you are reviewing a report, go first to the review workflow and rubric.
4. If you are creating a new report, use the workflow, standards, and report template together.

## Status

This repository is actively evolving through real report review and revision work. The current updates include stronger guidance on:
- keeping top-layer strategy language aligned with evidence strength
- separating recommendation layers cleanly
- restating key proof in the body instead of hiding it in embeds
- labeling supplementary examples when they are off-denominator
- keeping summary, title, and body caveats synchronized

---

# 中文说明

`user-research` 是一个可复用的研究技能，用来把零散的问题、访谈材料、问卷结果和草稿报告，整理成可以支持业务决策的用户研究产出。

它适合那些希望研究结果同时满足以下要求的团队：
- 证据扎实
- 方法上诚实克制
- 方便管理层快速扫读
- 对产品、设计、运营等执行角色足够可用
- 能经得住挑刺和复审

## 这个技能能做什么

这个技能覆盖了较完整的用户研究工作流：
- 研究规划与方案设计
- 定性编码与归纳
- 问卷分析与交叉分析
- 定量定性混合研究整合
- 研究报告撰写
- 面向管理层的高层摘要整理
- 对已有研究报告做审阅、纠偏和加固

它尤其适合下面这些场景：
- 把零散访谈整理成结构化洞察
- 把分裂的定量和定性材料整合成一份完整报告
- 把“有一些发现”推进到“可以支撑决策”
- 把表述过满、证据不稳的草稿改成更能自圆其说的版本

## 它和普通总结型 Prompt 的区别

相较于轻量的“帮我总结一下”式 prompt，这个技能更强调：
- 分母口径纪律
- 证据链可追溯
- 结论置信度标注
- 观察、解释、建议三层分开
- 对研究局限保持诚实
- 摘要、标题、正文和建议之间的表述强度一致

它也内置了一些常见质量问题的防护规则，例如：
- 用弱证据说强结论
- 混用不同题目 base 或不同 ID 体系
- 把关键证明藏在附录或嵌入表里
- 行动建议写两层却内容重复
- 把 demo 反馈误写成产品验证通过
- 最终稿里残留“待补”之类草稿痕迹

## 适合谁用

这个仓库比较适合：
- 用户研究员
- 需要自己做 mixed-method synthesis 的 PM / 设计师
- 写内部洞察报告的策略、运营团队
- 希望把 AI 研究辅助流程做得更严谨的团队

典型使用场景包括：
- “帮我审这份报告，看哪里说过头了。”
- “把这些访谈和 crosstab 整成一份完整报告。”
- “帮我写一份可以给管理层看的用研报告。”
- “先帮我把 agency 报告挑一遍再往上发。”
- “把 demo 反馈那一段改得更可执行、少重复。”

## 仓库结构

- [`SKILL.md`](./SKILL.md)：技能主说明
- [`references/README.md`](./references/README.md)：参考资料导航
- [`references/`](./references)：工作流、标准、模板和 review rubric
- [`scripts/validate_report.py`](./scripts/validate_report.py)：报告校验脚本
- [`generate_research_outputs.py`](./generate_research_outputs.py)：当前流程使用的生成辅助脚本

## 分支说明

- `codex`：Codex 版本
- `claude`：预留给 Claude 版本
- `main`：共享基线分支

## 设计取向

这个技能对研究质量有比较明确的偏好：
- 一份报告最好既能给领导看，也能给执行同学直接用
- 好报告不只是 markdown 里好看，转到飞书等文档系统里也要能站得住
- 建议应该能支持决策，而不是泛泛而谈
- 产品反馈最好拆成具体 friction 类型，而不是一团“信任问题”
- 原声要尽量保留用户语感，而不是全部压平为抽象概念

一句话说，这个仓库希望帮助产出“像强研究员写的”，而不是“像 AI 自动概括的”研究结果。

## 如何开始

1. 先看 [`SKILL.md`](./SKILL.md)。
2. 再用 [`references/README.md`](./references/README.md) 找到对应的支持材料。
3. 如果你要审报告，先看 review workflow 和 rubric。
4. 如果你要写新报告，就结合 workflow、analysis standards 和 report template 一起使用。

## 当前状态

这个仓库会随着真实的报告审阅和改稿工作持续迭代。当前这轮更新重点补强了：
- 顶层策略表述与正文证据强度保持一致
- 行动建议分层，避免重复
- 关键证明要回写到正文，不只藏在嵌入对象里
- 对 off-denominator 的补充例子做明确标注
- 摘要、标题、正文里的 caveat 要同步

## 自动化协作模式

这个技能的设计目标不是“让人全程盯着”，而是“尽量自动跑完，只在高杠杆判断点停下来”。

默认协作方式是：
- 机械性工作尽量自动化
- 只在最容易引发后续返工的地方保留人工闸门

大部分执行步骤都可以自动完成，例如：
- 数据清洗与结构化
- 初始编码应用
- 模式提取
- 原声与案例选择
- 置信度草标
- 红队问题收集
- 报告格式整理与打包

人工主要集中在 5 个检查点：
- 开头确认：仅当业务决策、受众或数据范围不清时触发
- Gate 1：编码簿审阅
- Gate 2：发现分级
- Gate 3：报告质量终审
- Final sign-off：最终签发

其中最关键的是 Gate 2。候选发现会被明确分成五类：
- `promote`
- `directional`
- `degrade`
- `add caveat`
- `drop as noise`

默认原则是从严处理，不默认升级为正式发现。
