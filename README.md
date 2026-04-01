# user-research-skill (Claude branch)

`user-research` is a Claude skill for turning messy product questions, interview data, survey outputs, and draft reports into decision-ready user research deliverables.

It is built for teams that want research outputs to be evidence-based, methodologically honest, easy for leadership to scan, detailed enough for practitioners to act on, and resilient under skeptical review.

## What It Does

This skill covers the full user research workflow: research planning and study design, qualitative coding and synthesis, survey and crosstab analysis, mixed-method integration, research report writing, executive-ready summarization, and rigorous review and hardening of draft reports.

It is especially useful when you need to move from scattered interviews to a structured insight system, from fragmented quant and qual outputs to one coherent report, from "interesting observations" to decisions with explicit evidence and confidence, or from weak draft reports to stronger, more defensible versions.

## How It Works — Three-Zone Collaboration Model

This skill does not fully automate research. It follows a three-zone human-AI collaboration model inspired by the REFINE framework, Great Question 6-step pipeline, and the augmentation-not-replacement consensus.

**Zone 1 — Claude autonomous.** Data cleaning, descriptive statistics, transcript structuring, initial open coding, pattern extraction, quote selection, confidence labeling, report scaffolding, red-teaming, and iteration triage. Claude executes and moves on without confirmation.

**Zone 2 — Claude proposes, human approves (3 gates).** These are the only points where Claude pauses:

- Gate 1: Codebook confirmation — Claude proposes 10–15 codes; user reviews before full analysis begins.
- Gate 2: Finding classification — Claude presents each candidate finding with a proposed status (formal finding / directional signal / downgrade / add caveat / drop as noise). A default-strict rule prevents over-promotion: unless evidence strength, denominator stability, and counter-example explanation are all adequate, findings default downward.
- Gate 3: Report quality review — Claude presents the full draft with red-team issues severity-ordered. Includes a check on whether recommendations exceed evidence strength.

**Zone 3 — Human decision (2 points).** Scope confirmation at the start (if business decision, audience, or data files are unclear) and publication sign-off at the end.

## What Makes It Different

Compared with lightweight "summarize these notes" prompts, this skill emphasizes denominator discipline, evidence traceability, confidence labeling, sharp separation between observation / interpretation / recommendation, realistic handling of research limitations, and alignment between executive summaries, section titles, body evidence, and action recommendations.

It also includes guardrails for common report quality failures: overstating weak evidence, mixing incompatible bases, burying proof in appendices, duplicating recommendation layers, treating prototype feedback as product validation, and leaving drafting residue in a final report.

## Repository Structure

```
SKILL.md                      # Main skill entry point (~230 lines)
references/
  README.md                   # Reference file navigator
  workflow.md                 # 16-step operating procedure
  report-standard.md          # Report structure and writing rules
  review-rubric.md            # 5-dimension review rubric
  delivery-formatting.md      # Feishu/Notion/Docs delivery conventions
  analysis-standards.md       # Coding and analysis rules
  evidence-confidence-standard.md
  qualitative-deep-dive.md
  quant-reporting-standard.md
  mixed-method-integration.md
  mixed-method-report-skeleton.md
  qual-packaging-standard.md
  executive-report-template.md
  finding-ledger-template.md
  research-assets-template.md
  citation-style.md
  artifact-interface.md
  iteration-playbook.md
  rollback-rules.md
  single-report-multistakeholder.md
scripts/
  validate_report.py          # Automated report validation
```

## Installation

Copy the `user-research` folder into your Claude skills directory:

```bash
cp -r user-research ~/.claude/skills/
```

After restarting Claude Desktop, the skill will appear in the available skills list and trigger automatically when you mention user research, UX research, interview coding, survey analysis, research report, or related terms.

## Branches

- `claude`: Claude-optimized version with three-zone collaboration model and progressive disclosure architecture (this branch)
- `codex`: Codex-oriented version
- `main`: shared baseline with bilingual README

## Getting Started

1. Start with [`SKILL.md`](./SKILL.md) — it contains the collaboration model, core principles, and operating procedure.
2. Use [`references/README.md`](./references/README.md) to navigate the 19 supporting reference files.
3. For report review, go to the review workflow and rubric first.
4. For new reports, combine the workflow, analysis standards, and report template.

## Status

This skill is actively evolving through real research projects. The current version includes the Gate 2 default-strict rule (preventing over-promotion of findings), the Gate 3 evidence-strength check for recommendations, delivery formatting extracted into a dedicated reference, and genericized examples suitable for any product domain.

---

# 中文说明（Claude 分支）

`user-research` 是一个 Claude 技能，用来把零散的产品问题、访谈材料、问卷结果和草稿报告整理成可以支持业务决策的用户研究产出。

它适合那些希望研究结果同时满足以下要求的团队：证据扎实、方法上诚实克制、方便管理层快速扫读、对执行角色足够可用、能经得住挑刺和复审。

## 这个技能能做什么

覆盖较完整的用户研究工作流：研究规划与方案设计、定性编码与归纳、问卷与交叉分析、混合方法整合、研究报告撰写、面向管理层的摘要整理、对已有报告做审阅和加固。

它尤其适合这些场景：把零散访谈整理成结构化洞察、把分裂的定量定性材料整合成一份完整报告、把"有一些发现"推进到"可以支撑决策"、把表述过满的草稿改成更能自圆其说的版本。

## 工作方式——三区协作模型

这个技能不会完全自动化研究流程，而是采用三区人机协作模型，参考了 REFINE 框架、Great Question 六步流程和"增强而非替代"的共识。

**Zone 1 — Claude 自主执行。** 数据清洗、描述统计、转录整理、初始编码、模式提取、引用选取、置信度标注、报告框架搭建、红队审查、迭代分类。Claude 直接执行，不需确认。

**Zone 2 — Claude 提议，人类审批（3 个门控）。** 这是 Claude 唯一暂停等待的环节：

- Gate 1：编码本确认——Claude 提出 10–15 个编码；用户审查后才开始正式分析。
- Gate 2：发现分类——Claude 呈现每个候选发现及建议状态（正式发现 / 方向性信号 / 降置信度 / 补边界条件 / 作为噪声丢弃）。内置默认从严规则：只要证据强度、分母稳定性、反例解释有一项不足，就不升级为正式发现。
- Gate 3：报告质量审查——Claude 呈现完整草稿和按严重度排序的红队问题，包括检查建议是否超过证据强度。

**Zone 3 — 人类决策（2 个节点）。** 开始时的范围确认（如果业务决策、受众或数据文件不明确）和结束时的发布签字。

## 与普通总结型 Prompt 的区别

相较于轻量的"帮我总结一下"式 prompt，这个技能更强调：分母口径纪律、证据链可追溯、结论置信度标注、观察/解释/建议三层分开、对研究局限保持诚实、以及摘要/标题/正文/建议之间的表述强度一致。

它也内置了常见质量问题的防护：用弱证据说强结论、混用不同 base 或 ID 体系、把关键证明藏在附录里、行动建议写两层却内容重复、把 demo 反馈误写成产品验证通过、最终稿残留草稿痕迹。

## 仓库结构

```
SKILL.md                      # 技能主入口（约 230 行）
references/
  README.md                   # 参考文件导航
  workflow.md                 # 16 步操作流程
  report-standard.md          # 报告结构与写作规则
  review-rubric.md            # 5 维审查 rubric
  delivery-formatting.md      # 飞书/Notion/Docs 交付规范
  ...（共 19 个参考文件）
scripts/
  validate_report.py          # 自动报告校验
```

## 安装方式

把 `user-research` 文件夹复制到 Claude 技能目录：

```bash
cp -r user-research ~/.claude/skills/
```

重启 Claude Desktop 后，技能会出现在可用列表里，提到用户研究、UX 研究、访谈编码、问卷分析、研究报告等关键词时会自动触发。

## 分支说明

- `claude`：Claude 优化版，包含三区协作模型和渐进式信息架构（当前分支）
- `codex`：Codex 版本
- `main`：共享基线分支，含双语 README

## 如何开始

1. 先看 [`SKILL.md`](./SKILL.md)——包含协作模型、核心原则和操作流程。
2. 用 [`references/README.md`](./references/README.md) 导航 19 个支持文件。
3. 审报告：先看 review workflow 和 rubric。
4. 写新报告：结合 workflow、analysis standards 和 report template。

## 当前状态

这个技能随着真实研究项目持续迭代。当前版本包含 Gate 2 默认从严规则（防止过度升级发现）、Gate 3 建议是否超过证据强度检查、交付格式抽取为独立参考文件、以及适用于任何产品领域的通用化示例。
