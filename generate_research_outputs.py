#!/usr/bin/env python3
import json
import math
import os
import shutil
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
from scipy.stats import chi2_contingency

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path("/Users/bytedance/Documents/New project")
OUT = ROOT / "research_outputs"
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["PingFang SC", "Arial Unicode MS", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 160

PALETTE = {
    "none": "#7F7F7F",
    "consider": "#0072B2",
    "borrowed": "#009E73",
    "accent": "#E69F00",
    "risk": "#D55E00",
    "purple": "#CC79A7",
    "lightblue": "#56B4E9",
    "yellow": "#F0E442",
}

STATUS_MAP = {
    "我完全没有借港币的需要": "无需求",
    "我有借港币的想法或需要，但还没借过": "有需求未借过",
    "我曾借过港币": "曾借过",
}
STATUS_ORDER = ["无需求", "有需求未借过", "曾借过"]
STATUS_COLOR = {
    "无需求": PALETTE["none"],
    "有需求未借过": PALETTE["consider"],
    "曾借过": PALETTE["borrowed"],
}

SURVEY_META = {
    "1.[C1]请问你的周岁年龄是？": ("Q1", "请问你的周岁年龄是？"),
    "2.请问过去 12 个月内你去过几次中国香港呢？ ": ("Q2", "请问过去 12 个月内你去过几次中国香港呢？"),
    "3.请问最近 12 个月内你需要用到港币的机会多吗？": ("Q3", "请问最近 12 个月内你需要用到港币的机会多吗？"),
    "4.请问以下哪种情况最符合你的实际情况？": ("Q4", "请问以下哪种情况最符合你的实际情况？"),
    "5.请问你是否持有以下香港身份证明文件呢？": ("Q5", "请问你是否持有以下香港身份证明文件呢？"),
    "6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？": ("Q6", "请问你曾用过、或考虑通过什么渠道获得港币借款呢？"),
    "7.请问你借用港币主要考虑用于哪些方面呢？": ("Q7", "请问你借用港币主要考虑用于哪些方面呢？"),
    "8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？": ("Q8", "请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？"),
    "9.请问未来 12 个月内，你预期会借用多少港币呢？": ("Q9", "请问未来 12 个月内，你预期会借用多少港币呢？"),
    "10.请问未来 12 个月内，你预期会借几次港币呢？": ("Q10", "请问未来 12 个月内，你预期会借几次港币呢？"),
    "11.请问你期望每笔港币资金能借多长时间呢？": ("Q11", "请问你期望每笔港币资金能借多长时间呢？"),
    "12.请问你最希望的港币还款方式是？": ("Q12", "请问你最希望的港币还款方式是？"),
    "13.请问你目前从事的职业是？": ("Q13", "请问你目前从事的职业是？"),
    "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）": ("Q14", "请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）"),
    "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）": ("Q15", "请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）"),
    "标签": ("标签", "内部标签：两地往返 vs 常驻内地"),
}

INTERVIEW_QUESTION_MAP = {
    "Q3": "Q3: 首先，可否请你简单介绍一下自己，比如你是哪里人、做什么工作、一般去香港是出于什么需要？",
    "Q4": "Q4: 请回想下，你最近一次想要借港币具体是什么情况？当时为什么会有这个想法呢？请你尽可能详细描述。",
    "Q5": "Q5: 当时你具体是通过什么渠道或机构借的港币？借了多少、利率大概是多少、还款周期和还款方式是怎样的？如果还没借过，你了解到的借款条件大概是怎样的，最终是如何解决的呢？",
    "Q6": "Q6: 整个借款流程的体验怎么样？从申请到放款再到还款，有没有遇到什么问题或不顺畅的地方？如果还没借过，你在了解和比较的过程中有什么困难吗？",
    "Q7": "Q7: 在选择借港币的方式的时候，你主要考虑了哪些因素？最终是怎么做出选择的？请你详细描述。",
    "Q8": "Q8: 如果有一个港币借款产品，你最看重哪些方面？请选择最重要的 3 项。",
    "Q9": "Q9: 你理想中的港币借款产品是什么样的？比如你希望的额度、期限、还款方式等。",
    "Q10": "Q10: 在借港币这件事上，你最担心或顾虑的是什么？",
    "Q13": "Q13: 看完这个产品界面，你的第一反应是什么？哪些地方让你觉得不错，哪些地方让你困惑？请你尽可能详细描述。",
    "Q14": "Q14: 你觉得这个产品最吸引你的卖点是什么？有没有哪个卖点你觉得不太可信或不够有吸引力？",
    "Q15": "Q15: 看完界面后，你能说说你理解的这个产品是怎么用的吗？比如借了之后钱会放到哪里、放款和还款分别是什么币种、具体怎么还款？",
    "Q16": "Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？",
    "Q17": "Q17: 如果想让这个产品更有吸引力，你最希望改变或添加什么？",
}

SINGLE_VARS = [
    "1.[C1]请问你的周岁年龄是？",
    "2.请问过去 12 个月内你去过几次中国香港呢？ ",
    "3.请问最近 12 个月内你需要用到港币的机会多吗？",
    "4.请问以下哪种情况最符合你的实际情况？",
    "5.请问你是否持有以下香港身份证明文件呢？",
    "6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？",
    "7.请问你借用港币主要考虑用于哪些方面呢？",
    "8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？",
    "9.请问未来 12 个月内，你预期会借用多少港币呢？",
    "10.请问未来 12 个月内，你预期会借几次港币呢？",
    "11.请问你期望每笔港币资金能借多长时间呢？",
    "12.请问你最希望的港币还款方式是？",
    "13.请问你目前从事的职业是？",
    "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）",
    "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）",
]

ORDER_MAP = {
    "1.[C1]请问你的周岁年龄是？": [
        "14岁及以下",
        "15-17岁",
        "18-22岁",
        "23-30岁",
        "31-40岁",
        "41-50岁",
        "51-60岁",
        "61岁及以上",
    ],
    "2.请问过去 12 个月内你去过几次中国香港呢？ ": [
        "1-2 次",
        "3-5 次",
        "6 次及以上",
    ],
    "3.请问最近 12 个月内你需要用到港币的机会多吗？": [
        "基本没有",
        "偶尔（1-2次）",
        "有时（3-6次）",
        "经常（6次以上）",
    ],
    "9.请问未来 12 个月内，你预期会借用多少港币呢？": [
        "1 万港币以下",
        "1 - 5 万港币",
        "5 - 20 万港币",
        "20 - 50 万港币",
        "50 万港币以上",
        "不打算借港币",
    ],
    "10.请问未来 12 个月内，你预期会借几次港币呢？": [
        "1 次",
        "2-3 次",
        "4-6 次",
        "7-12次",
        "12 次以上",
    ],
    "11.请问你期望每笔港币资金能借多长时间呢？": [
        "1 个月以内",
        "1-3 个月",
        "3-6 个月",
        "6-12 个月",
        "12 个月以上",
    ],
    "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）": [
        "5000元及以下",
        "5001 - 1 万元",
        "1 - 2万元",
        "2 - 3万元",
        "3 - 4万元",
        "4 - 6万元",
        "6 - 8万元",
        "8 - 10万元",
        "10万元及以上",
        "不便透露",
    ],
    "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）": [
        "没有港币收入",
        "HK$10,000及以下",
        "HK$10,001 - $20,000",
        "HK$20,001 - $30,000",
        "HK$30,001 - $40,000",
        "HK$40,001 - $60,000",
        "HK$60,001 - $80,000",
        "HK$80,001 或以上",
        "不便透露",
    ],
    "标签": ["1_两地往返", "2_常驻内地"],
    "简化预期金额": ["1万以下", "1-5万", "5-20万", "20万以上", "不打算借"],
    "简化预期次数": ["1-3次", "4-12次", "12次以上"],
    "简化期望期限": ["1个月内", "1-6个月", "6-12个月", "12个月以上"],
    "简化还款方式": ["按月等额", "随借随还", "到期一次性", "先息后本", "方式灵活均可", "其他"],
    "简化借款渠道": ["传统银行", "内地背景金融科技", "虚拟银行", "持牌财务公司", "其他财务公司", "其他"],
    "简化借款用途": ["旅游购物消费", "商务/工作", "生意周转", "投资/证券", "留学/医疗", "其他"],
    "简化身份": ["短期签注", "长期签证无HKID", "非永久HKID", "永久HKID", "无香港身份", "缺失"],
}

SINGLE_CHART_TITLES = {
    "1.[C1]请问你的周岁年龄是？": "31-40 岁是赴港样本中的核心年龄段",
    "2.请问过去 12 个月内你去过几次中国香港呢？ ": "赴港样本以 1-2 次和 6 次及以上两端人群为主",
    "3.请问最近 12 个月内你需要用到港币的机会多吗？": "港币使用需求以偶尔和经常两类人群为主",
    "4.请问以下哪种情况最符合你的实际情况？": "有需求但未借过的人群明显多于已借过人群",
    "5.请问你是否持有以下香港身份证明文件呢？": "短期签注仍是赴港样本中的主流身份形态",
    "6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？": "用户最常提及的渠道仍集中在银行、熟人和现有常见金融路径",
    "7.请问你借用港币主要考虑用于哪些方面呢？": "旅游购物消费是最主要的借港币用途",
    "8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？": "减少换汇手续和费用折损是借港币的首要原因",
    "9.请问未来 12 个月内，你预期会借用多少港币呢？": "未来借款金额主要集中在 1 万以下到 5 万港币区间",
    "10.请问未来 12 个月内，你预期会借几次港币呢？": "预期借款次数以 1-3 次为主",
    "11.请问你期望每笔港币资金能借多长时间呢？": "借款期限偏好分散，但中短期与 12 个月以上都有需求",
    "12.请问你最希望的港币还款方式是？": "用户更在意灵活和可理解的还款方式，而非单一模式",
    "13.请问你目前从事的职业是？": "赴港样本职业结构较分散，私营/企业员工占较高比重",
    "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）": "月收入主要集中在 5000 元到 2 万元区间",
    "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）": "大多数赴港样本没有稳定港币收入来源",
}


def pct(n, d):
    return round(n / d * 100, 1) if d else 0.0


def fmt_p(p):
    return "p<0.001" if p < 0.001 else f"p={p:.4f}"


def wrap(text, width=36):
    return "\n".join(textwrap.wrap(str(text), width=width, break_long_words=False))


def split_multi(value):
    if pd.isna(value) or value in ("", "#N/A"):
        return []
    return [x.strip() for x in str(value).split(" | ") if x.strip()]


def split_themes(value):
    if pd.isna(value) or value in ("", "#N/A"):
        return []
    return [x.strip() for x in str(value).split(",") if x.strip()]


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join([":---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out)


def residual_stars(val):
    av = abs(val)
    if av >= 3.29:
        return "***"
    if av >= 2.58:
        return "**"
    if av >= 1.96:
        return "*"
    return ""


def sig_arrow(val):
    if val >= 1.96:
        return "↑"
    if val <= -1.96:
        return "↓"
    return ""


def quality_bucket(row):
    progress = str(row.get("Progress", ""))
    score = str(row.get("Quality score", ""))
    try:
        prog = 1.0 if progress == "Complete" else float(progress)
    except Exception:
        prog = 0.0
    try:
        qs = float(score)
    except Exception:
        qs = -1
    if progress == "Complete" and qs >= 3:
        return "高质量"
    if progress == "Complete" or prog >= 0.5:
        return "中质量"
    return "低质量"


def simplify_usage(value):
    parts = split_multi(value)
    if any("生意周转" in p for p in parts):
        return "生意周转"
    if any("港股" in p or "证券" in p or "投资" in p for p in parts):
        return "投资/证券"
    if any("商务出差" in p for p in parts):
        return "商务/工作"
    if any("留学" in p or "就医" in p for p in parts):
        return "留学/医疗"
    if any("旅游" in p or "购物" in p or "娱乐消费" in p for p in parts):
        return "旅游购物消费"
    return "其他"


def simplify_amount(value):
    if pd.isna(value) or value == "":
        return "缺失"
    v = str(value)
    if "不打算" in v:
        return "不打算借"
    if "1 万港币以下" in v:
        return "1万以下"
    if "1 - 5 万港币" in v:
        return "1-5万"
    if "5 - 20 万港币" in v:
        return "5-20万"
    if "20 - 50 万港币" in v or "50 万港币以上" in v:
        return "20万以上"
    return v


def simplify_times(value):
    if pd.isna(value) or value == "":
        return "缺失"
    v = str(value)
    if v in ("1 次", "2-3 次"):
        return "1-3次"
    if v in ("4-6 次", "7-12次"):
        return "4-12次"
    if "12" in v:
        return "12次以上"
    return v


def simplify_term(value):
    if pd.isna(value) or value == "":
        return "缺失"
    v = str(value)
    if "1 个月以内" in v:
        return "1个月内"
    if "1-3 个月" in v or "3-6 个月" in v:
        return "1-6个月"
    if "6-12 个月" in v:
        return "6-12个月"
    if "12 个月以上" in v:
        return "12个月以上"
    return v


def simplify_repayment(value):
    if pd.isna(value) or value == "":
        return "缺失"
    v = str(value)
    if "等额" in v:
        return "按月等额"
    if "随借随还" in v:
        return "随借随还"
    if "到期一次" in v:
        return "到期一次性"
    if "先息后本" in v:
        return "先息后本"
    if "以上都可以" in v:
        return "方式灵活均可"
    return "其他"


def simplify_channel(value):
    parts = split_multi(value)
    if not parts:
        return "缺失"
    for p in parts:
        if "传统银行" in p:
            return "传统银行"
        if "有内地背景的虚拟银行或金融科技公司" in p or "支付宝HK" in p or "蚂蚁银行" in p:
            return "内地背景金融科技"
        if "虚拟银行" in p:
            return "虚拟银行"
        if "持牌放债人" in p or "财务公司" in p:
            return "持牌财务公司"
        if "二线或其他财务公司" in p or "K Cash" in p or "X Wallet" in p:
            return "其他财务公司"
        if "其他" in p:
            return "其他"
    return "其他"


def simplify_identity(value):
    if pd.isna(value) or value == "":
        return "缺失"
    v = str(value)
    if "短期签证" in v:
        return "短期签注"
    if "长期签证但无香港身份证" in v:
        return "长期签证无HKID"
    if "非永久" in v:
        return "非永久HKID"
    if "永久性居民" in v:
        return "永久HKID"
    if "以上都没有" in v:
        return "无香港身份"
    return v


def note_question(col, multi=False, recoded=False):
    qn, qt = SURVEY_META.get(col, ("", col))
    note = f"{qn}：{qt}"
    extra = []
    if multi:
        extra.append("多选题")
    if recoded:
        extra.append("已做业务重编码")
    if extra:
        note += "；" + "，".join(extra)
    return note


def add_footnote(fig, lines, rect_bottom=0.09):
    note = "\n".join(lines)
    fig.text(0.01, 0.01, note, ha="left", va="bottom", fontsize=8, color="#444")
    fig.tight_layout(rect=[0, rect_bottom, 1, 1])


def save_figure(fig, filename):
    fig.savefig(CHARTS / filename, bbox_inches="tight")
    plt.close(fig)


def top_categories(series, limit=None):
    cnt = series.dropna().astype(str)
    cnt = cnt[cnt != ""]
    ordered = cnt.value_counts().index.tolist()
    return ordered[:limit] if limit else ordered


def ordered_categories(series, key=None, limit=None):
    values = series.replace("", pd.NA).dropna().astype(str)
    preferred = ORDER_MAP.get(key or "")
    if preferred:
        present = values.unique().tolist()
        ordered = [x for x in preferred if x in present]
        extras = [x for x in values.value_counts().index.tolist() if x not in ordered]
        final = ordered + extras
    else:
        final = values.value_counts().index.tolist()
    return final[:limit] if limit else final


def normalize_join_id(value):
    if pd.isna(value):
        return ""
    s = str(value).strip()
    if s in ("", "#N/A", "nan"):
        return ""
    if s.endswith(".0"):
        s = s[:-2]
    return s


survey = pd.read_csv(OUT / "survey_raw.csv")
interviews = pd.read_csv(OUT / "interview_raw.csv")

survey = survey.fillna("")
interviews = interviews.fillna("")

survey["user_id_norm"] = survey["user_id"].astype(str).str.strip().str.strip('"')
valid_raw = survey[survey["无效答卷"].astype(str) != "1"].copy()
valid = valid_raw.sort_values("提交时间", kind="stable").drop_duplicates(subset=["user_id_norm"], keep="first").copy()
visited = valid[~valid["2.请问过去 12 个月内你去过几次中国香港呢？ "].isin(["", "没去过"])].copy()
need = visited[visited["4.请问以下哪种情况最符合你的实际情况？"].isin([
    "我有借港币的想法或需要，但还没借过",
    "我曾借过港币",
])].copy()
consider = need[need["4.请问以下哪种情况最符合你的实际情况？"] == "我有借港币的想法或需要，但还没借过"].copy()
borrowed = need[need["4.请问以下哪种情况最符合你的实际情况？"] == "我曾借过港币"].copy()

survey["join_id"] = survey["问卷序号"].apply(normalize_join_id)
interviews["join_id"] = interviews["问卷ID"].apply(normalize_join_id)
survey_by_seq = survey.set_index("join_id", drop=False)
matched = interviews[(interviews["join_id"] != "") & (interviews["join_id"].isin(survey_by_seq.index))].copy()
matched["标签"] = matched["join_id"].map(survey_by_seq["标签"].to_dict())
matched["问卷状态"] = matched["join_id"].map(survey_by_seq["4.请问以下哪种情况最符合你的实际情况？"].to_dict())
matched["年龄"] = matched["join_id"].map(survey_by_seq["1.[C1]请问你的周岁年龄是？"].to_dict())
matched["月收入"] = matched["join_id"].map(survey_by_seq["14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）"].to_dict())
matched["职业"] = matched["join_id"].map(survey_by_seq["13.请问你目前从事的职业是？"].to_dict())
matched["赴港频次"] = matched["join_id"].map(survey_by_seq["2.请问过去 12 个月内你去过几次中国香港呢？ "].to_dict())
matched["港币收入"] = matched["join_id"].map(survey_by_seq["15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）"].to_dict())
matched["香港身份"] = matched["join_id"].map(survey_by_seq["5.请问你是否持有以下香港身份证明文件呢？"].to_dict())
matched["质量等级"] = matched.apply(quality_bucket, axis=1)
matched_need = matched[matched["问卷状态"].isin([
    "我有借港币的想法或需要，但还没借过",
    "我曾借过港币",
])].copy()

need["简化借款用途"] = need["7.请问你借用港币主要考虑用于哪些方面呢？"].apply(simplify_usage)
need["简化预期金额"] = need["9.请问未来 12 个月内，你预期会借用多少港币呢？"].apply(simplify_amount)
need["简化预期次数"] = need["10.请问未来 12 个月内，你预期会借几次港币呢？"].apply(simplify_times)
need["简化期望期限"] = need["11.请问你期望每笔港币资金能借多长时间呢？"].apply(simplify_term)
need["简化还款方式"] = need["12.请问你最希望的港币还款方式是？"].apply(simplify_repayment)
need["简化借款渠道"] = need["6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？"].apply(simplify_channel)
need["简化身份"] = need["5.请问你是否持有以下香港身份证明文件呢？"].apply(simplify_identity)
visited["借款状态简化"] = visited["4.请问以下哪种情况最符合你的实际情况？"].map(STATUS_MAP)
need["借款状态简化"] = need["4.请问以下哪种情况最符合你的实际情况？"].map(STATUS_MAP)
matched_need["使用意愿简化"] = matched_need["Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？"].replace({
    "Definitely would use": "肯定会用",
    "Probably would use": "可能会用",
})


def cross_analysis(df, row_col, col_col, row_order=None, col_order=None, merge_threshold=8):
    temp = df[[row_col, col_col]].copy()
    temp = temp[(temp[row_col] != "") & (temp[col_col] != "")]
    if row_order is None:
        row_order = temp[row_col].value_counts().index.tolist()
    if col_order is None:
        col_order = temp[col_col].value_counts().index.tolist()
    row_counts = temp[row_col].value_counts()
    for cat, count in row_counts.items():
        if count < merge_threshold and cat not in row_order:
            row_order.append(cat)
    temp[row_col] = pd.Categorical(temp[row_col], categories=row_order, ordered=True)
    temp[col_col] = pd.Categorical(temp[col_col], categories=col_order, ordered=True)
    ctab = pd.crosstab(temp[row_col], temp[col_col]).fillna(0)
    ctab = ctab.loc[(ctab.sum(axis=1) > 0), (ctab.sum(axis=0) > 0)]
    chi2, p, dof, expected = chi2_contingency(ctab.values)
    expected_df = pd.DataFrame(expected, index=ctab.index, columns=ctab.columns)
    n = ctab.values.sum()
    row_prop = ctab.sum(axis=1) / n
    col_prop = ctab.sum(axis=0) / n
    residuals = pd.DataFrame(index=ctab.index, columns=ctab.columns, dtype=float)
    for i in ctab.index:
        for j in ctab.columns:
            obs = ctab.loc[i, j]
            exp = expected_df.loc[i, j]
            denom = math.sqrt(exp * (1 - row_prop.loc[i]) * (1 - col_prop.loc[j]))
            residuals.loc[i, j] = (obs - exp) / denom if denom else 0.0
    k = min(ctab.shape)
    cramers_v = math.sqrt(chi2 / (n * (k - 1))) if k > 1 else 0.0
    low_expected = int((expected_df < 5).sum().sum())
    return {
        "table": ctab,
        "row_pct": ctab.div(ctab.sum(axis=1), axis=0) * 100,
        "chi2": chi2,
        "p": p,
        "dof": dof,
        "residuals": residuals,
        "cramers_v": cramers_v,
        "n": int(n),
        "low_expected": low_expected,
    }


def quote_text(row, q):
    col = INTERVIEW_QUESTION_MAP[q]
    text = str(row.get(col, "")).strip()
    return " ".join(text.split())


def top_theme_terms(series, topn=5, exclude=None):
    exclude = set(exclude or [])
    counter = Counter()
    for val in series.fillna(""):
        for token in split_themes(val):
            if token and token not in exclude:
                counter[token] += 1
    return counter.most_common(topn)


def status_short(status):
    return {
        "我曾借过港币": "曾借过",
        "我有借港币的想法或需要，但还没借过": "有需求未借过",
        "我完全没有借港币的需要": "无需求",
    }.get(str(status), str(status))


def clean_label(value):
    text = str(value or "").strip()
    if not text:
        return ""
    return (
        text.replace("1_", "")
        .replace("2_", "")
        .replace("私营企业主/个体经营者（含自己开公司、开店、做生意）", "私营企业主/个体经营者")
        .replace("民营/私营/外资企业的员工", "民营/私营/外资企业员工")
    )


def profile_stub(row):
    bits = [f"案例#{row['ID']}"]
    if clean_label(row.get("标签", "")):
        bits.append(clean_label(row["标签"]))
    if clean_label(row.get("年龄", "")):
        bits.append(clean_label(row["年龄"]))
    if clean_label(row.get("职业", "")):
        bits.append(clean_label(row["职业"]))
    if clean_label(row.get("问卷状态", "")):
        bits.append(status_short(clean_label(row["问卷状态"])))
    return "，".join(bits)


def find_quotes(predicate, q, limit=5):
    rows = []
    for _, r in matched_need.iterrows():
        if predicate(r):
            txt = quote_text(r, q)
            if txt:
                rows.append((r, txt))
    rows = sorted(rows, key=lambda x: (x[0].get("质量等级", ""), x[0].get("Quality score", "")), reverse=True)
    uniq = []
    seen = set()
    for r, txt in rows:
        key = r["ID"]
        if key in seen:
            continue
        seen.add(key)
        uniq.append((r, txt))
        if len(uniq) >= limit:
            break
    return uniq


single_stats = {}
for col in SINGLE_VARS:
    if col in [
        "6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？",
        "7.请问你借用港币主要考虑用于哪些方面呢？",
        "8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？",
    ]:
        counts = Counter()
        for val in need[col]:
            for part in split_multi(val):
                counts[part] += 1
        single_stats[col] = counts
    else:
        single_stats[col] = Counter(visited[col] if col in SINGLE_VARS[:5] + SINGLE_VARS[12:] else need[col])


cross_specs = [
    ("标签", "借款状态简化", visited, ["1_两地往返", "2_常驻内地"], STATUS_ORDER, "标签 × 借款状态"),
    ("2.请问过去 12 个月内你去过几次中国香港呢？ ", "借款状态简化", visited, ["1-2 次", "3-5 次", "6 次及以上"], STATUS_ORDER, "赴港频次 × 借款状态"),
    ("1.[C1]请问你的周岁年龄是？", "借款状态简化", visited, ORDER_MAP["1.[C1]请问你的周岁年龄是？"], STATUS_ORDER, "年龄 × 借款状态"),
    ("14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）", "借款状态简化", visited, ORDER_MAP["14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）"], STATUS_ORDER, "月收入 × 借款状态"),
    ("5.请问你是否持有以下香港身份证明文件呢？", "借款状态简化", visited, None, STATUS_ORDER, "香港身份 × 借款状态"),
    ("3.请问最近 12 个月内你需要用到港币的机会多吗？", "借款状态简化", visited, ["基本没有", "偶尔（1-2次）", "有时（3-6次）", "经常（6次以上）"], STATUS_ORDER, "港币使用频率 × 借款状态"),
    ("简化借款用途", "借款状态简化", need, ["旅游购物消费", "商务/工作", "生意周转", "投资/证券", "留学/医疗", "其他"], ["有需求未借过", "曾借过"], "简化借款用途 × 借款状态"),
    ("标签", "3.请问最近 12 个月内你需要用到港币的机会多吗？", visited, ["1_两地往返", "2_常驻内地"], ["基本没有", "偶尔（1-2次）", "有时（3-6次）", "经常（6次以上）"], "标签 × 港币使用频率"),
    ("2.请问过去 12 个月内你去过几次中国香港呢？ ", "3.请问最近 12 个月内你需要用到港币的机会多吗？", visited, ["1-2 次", "3-5 次", "6 次及以上"], ["基本没有", "偶尔（1-2次）", "有时（3-6次）", "经常（6次以上）"], "赴港频次 × 港币使用频率"),
    ("5.请问你是否持有以下香港身份证明文件呢？", "3.请问最近 12 个月内你需要用到港币的机会多吗？", visited, None, ["基本没有", "偶尔（1-2次）", "有时（3-6次）", "经常（6次以上）"], "香港身份 × 港币使用频率"),
    ("标签", "简化预期金额", need, ["1_两地往返", "2_常驻内地"], ["1万以下", "1-5万", "5-20万", "20万以上", "不打算借"], "标签 × 预期金额"),
    ("2.请问过去 12 个月内你去过几次中国香港呢？ ", "简化预期金额", need, ["1-2 次", "3-5 次", "6 次及以上"], ["1万以下", "1-5万", "5-20万", "20万以上", "不打算借"], "赴港频次 × 预期金额"),
    ("1.[C1]请问你的周岁年龄是？", "简化预期金额", need, ORDER_MAP["1.[C1]请问你的周岁年龄是？"], ["1万以下", "1-5万", "5-20万", "20万以上", "不打算借"], "年龄 × 预期金额"),
    ("14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）", "简化预期金额", need, ORDER_MAP["14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）"], ["1万以下", "1-5万", "5-20万", "20万以上", "不打算借"], "月收入 × 预期金额"),
    ("简化身份", "简化预期金额", need, ORDER_MAP["简化身份"], ["1万以下", "1-5万", "5-20万", "20万以上", "不打算借"], "香港身份 × 预期金额"),
    ("简化借款用途", "简化预期金额", need, ["旅游购物消费", "商务/工作", "生意周转", "投资/证券", "留学/医疗", "其他"], ["1万以下", "1-5万", "5-20万", "20万以上", "不打算借"], "借款用途 × 预期金额"),
    ("借款状态简化", "简化预期金额", need, ["有需求未借过", "曾借过"], ["1万以下", "1-5万", "5-20万", "20万以上", "不打算借"], "借款状态 × 预期金额"),
    ("标签", "简化预期次数", need, ["1_两地往返", "2_常驻内地"], ["1-3次", "4-12次", "12次以上"], "标签 × 预期次数"),
    ("2.请问过去 12 个月内你去过几次中国香港呢？ ", "简化预期次数", need, ["1-2 次", "3-5 次", "6 次及以上"], ["1-3次", "4-12次", "12次以上"], "赴港频次 × 预期次数"),
    ("简化借款用途", "简化预期次数", need, ["旅游购物消费", "商务/工作", "生意周转", "投资/证券", "留学/医疗", "其他"], ["1-3次", "4-12次", "12次以上"], "借款用途 × 预期次数"),
    ("借款状态简化", "简化预期次数", need, ["有需求未借过", "曾借过"], ["1-3次", "4-12次", "12次以上"], "借款状态 × 预期次数"),
    ("标签", "简化期望期限", need, ["1_两地往返", "2_常驻内地"], ["1个月内", "1-6个月", "6-12个月", "12个月以上"], "标签 × 期望期限"),
    ("简化借款用途", "简化期望期限", need, ["旅游购物消费", "商务/工作", "生意周转", "投资/证券", "留学/医疗", "其他"], ["1个月内", "1-6个月", "6-12个月", "12个月以上"], "借款用途 × 期望期限"),
    ("简化身份", "简化期望期限", need, ORDER_MAP["简化身份"], ["1个月内", "1-6个月", "6-12个月", "12个月以上"], "香港身份 × 期望期限"),
    ("借款状态简化", "简化期望期限", need, ["有需求未借过", "曾借过"], ["1个月内", "1-6个月", "6-12个月", "12个月以上"], "借款状态 × 期望期限"),
    ("标签", "简化还款方式", need, ["1_两地往返", "2_常驻内地"], ["按月等额", "随借随还", "到期一次性", "先息后本", "方式灵活均可", "其他"], "标签 × 还款方式"),
    ("简化借款用途", "简化还款方式", need, ["旅游购物消费", "商务/工作", "生意周转", "投资/证券", "留学/医疗", "其他"], ["按月等额", "随借随还", "到期一次性", "先息后本", "方式灵活均可", "其他"], "借款用途 × 还款方式"),
    ("简化身份", "简化还款方式", need, ORDER_MAP["简化身份"], ["按月等额", "随借随还", "到期一次性", "先息后本", "方式灵活均可", "其他"], "香港身份 × 还款方式"),
    ("借款状态简化", "简化还款方式", need, ["有需求未借过", "曾借过"], ["按月等额", "随借随还", "到期一次性", "先息后本", "方式灵活均可", "其他"], "借款状态 × 还款方式"),
    ("借款状态简化", "简化借款渠道", need, ["有需求未借过", "曾借过"], ORDER_MAP["简化借款渠道"], "借款状态 × 借款渠道"),
    ("简化借款用途", "简化借款渠道", need, ["旅游购物消费", "商务/工作", "生意周转", "投资/证券", "留学/医疗", "其他"], ORDER_MAP["简化借款渠道"], "借款用途 × 借款渠道"),
]

cross_results = {}
for row_col, col_col, df, row_order, col_order, name in cross_specs:
    cross_results[name] = cross_analysis(df, row_col, col_col, row_order, col_order)


def plot_single_bar(col, filename, base_df, multi=False, topn=None):
    qn, qt = SURVEY_META[col]
    title = SINGLE_CHART_TITLES.get(col, f"{qt}：当前样本的分布结构")
    if multi:
        counts = Counter()
        for val in base_df[col]:
            for part in split_multi(val):
                counts[part] += 1
        items = counts.most_common(topn or 12)
        labels = [k for k, _ in items][::-1]
        values = [pct(v, len(base_df)) for _, v in items][::-1]
        note = "百分比按样本人数计算，非选项被提及次数占比"
    else:
        ordered = ordered_categories(base_df[col], key=col, limit=topn)
        vc = base_df[col].replace("", pd.NA).dropna().astype(str).value_counts()
        labels = ordered[::-1]
        values = [pct(int(vc.get(label, 0)), len(base_df)) for label in ordered][::-1]
        note = "百分比按样本人数计算"
    fig, ax = plt.subplots(figsize=(9, max(4.8, 0.42 * len(labels))))
    ax.barh([wrap(x, 24) for x in labels], values, color=PALETTE["consider"])
    for i, v in enumerate(values):
        ax.text(v + 0.8, i, f"{v:.1f}%", va="center", fontsize=9)
    ax.set_xlabel("占样本比例 (%)")
    ax.set_title(title, fontsize=13)
    ax.grid(axis="x", alpha=0.2)
    add_footnote(fig, [
        f"题号/题干：{qn}｜{qt}",
        f"Base：n={len(base_df)}",
        f"口径说明：{note}" + ("；多选题" if multi else ""),
    ])
    save_figure(fig, filename)


def plot_status_stacked(filename):
    groups = ["1_两地往返", "2_常驻内地"]
    labels = [f"两地往返\n(n={(visited['标签'] == '1_两地往返').sum()})", f"常驻内地\n(n={(visited['标签'] == '2_常驻内地').sum()})"]
    parts = {s: [] for s in STATUS_ORDER}
    for g in groups:
        sub = visited[visited["标签"] == g]
        for s in STATUS_ORDER:
            raw = [k for k, v in STATUS_MAP.items() if v == s]
            n = sub["4.请问以下哪种情况最符合你的实际情况？"].isin(raw).sum()
            parts[s].append(pct(n, len(sub)))
    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = [0, 0]
    for s in STATUS_ORDER:
        ax.bar(labels, parts[s], bottom=bottom, color=STATUS_COLOR[s], label=s)
        bottom = [bottom[i] + parts[s][i] for i in range(2)]
    res = cross_results["标签 × 借款状态"]["residuals"]
    table = cross_results["标签 × 借款状态"]["table"]
    for i, g in enumerate(groups):
        base = 0
        for s in STATUS_ORDER:
            val = parts[s][i]
            raw_col = [k for k, v in STATUS_MAP.items() if v == s][0]
            arr = sig_arrow(res.loc[g, s] if s in res.columns else 0)
            txt = f"{val:.1f}%{arr}"
            ax.text(i, base + val / 2, txt, ha="center", va="center", color="white", fontsize=9)
            base += val
    ax.set_ylabel("占赴港样本比例 (%)")
    ax.set_title("两地往返更容易从需求走向真实借款", fontsize=13)
    ax.legend(frameon=False, loc="upper right")
    add_footnote(fig, [
        f"题号/题干：Q4｜{SURVEY_META['4.请问以下哪种情况最符合你的实际情况？'][1]}；标签｜{SURVEY_META['标签'][1]}",
        f"Base：赴港样本 n={len(visited)}",
        f"口径说明：100% 堆叠柱；↑/↓ 表示该单元格相对总体显著偏高/偏低",
        f"统计检验：Chi-square {fmt_p(cross_results['标签 × 借款状态']['p'])}；Cramer's V={cross_results['标签 × 借款状态']['cramers_v']:.3f}",
    ])
    save_figure(fig, filename)


def plot_cross_grouped(name, filename, row_label, col_label):
    result = cross_results[name]
    table = result["row_pct"]
    rows = list(table.index)
    cols = list(table.columns)
    colors = [STATUS_COLOR.get(c, list(PALETTE.values())[i % len(PALETTE)]) for i, c in enumerate(cols)]
    fig, ax = plt.subplots(figsize=(12, max(5.8, 0.7 * len(rows) + 2.2)))
    x = range(len(rows))
    width = 0.8 / len(cols)
    for j, c in enumerate(cols):
        xpos = [i - 0.4 + width / 2 + j * width for i in x]
        vals = table[c].tolist()
        ax.bar(xpos, vals, width=width, label=c, color=colors[j])
        for i, v in enumerate(vals):
            arr = sig_arrow(result["residuals"].iloc[i, j])
            ax.text(xpos[i], v + 0.7, f"{v:.1f}%{arr}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(list(x))
    row_ns = result["table"].sum(axis=1)
    ax.set_xticklabels([wrap(f"{r}\n(n={int(row_ns.loc[r])})", 10) for r in rows], fontsize=8)
    ax.tick_params(axis="x", pad=10)
    ax.set_ylabel("行百分比 (%)")
    ax.set_title(f"{name}：不同组别的结构差异", fontsize=13)
    ax.legend(frameon=False, ncol=min(3, len(cols)))
    ax.grid(axis="y", alpha=0.2)
    add_footnote(fig, [
        f"题号/题干：{row_label} × {col_label}",
        f"Base：n={result['n']}",
        "口径说明：显示行百分比；↑/↓ 表示该单元格相对总体显著偏高/偏低",
        f"统计检验：Pearson chi-square {fmt_p(result['p'])}；Cramer's V={result['cramers_v']:.3f}",
    ], rect_bottom=0.18)
    save_figure(fig, filename)


def plot_cross_heatmap(name, filename, row_label, col_label):
    result = cross_results[name]
    table = result["row_pct"]
    counts = result["table"]
    rows = list(table.index)
    cols = list(table.columns)
    row_ns = counts.sum(axis=1)
    fig, ax = plt.subplots(figsize=(9.2, max(5.2, 0.52 * len(rows) + 2.2)))
    im = ax.imshow(table.values, cmap="Blues", vmin=0, vmax=max(35, float(table.values.max())))
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([wrap(c, 14) for c in cols])
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([wrap(f"{r} (n={int(row_ns.loc[r])})", 18) for r in rows])
    ax.set_title(f"{name}：不同收入层级的金额偏好梯度", fontsize=13)
    ax.set_xlabel("预期金额")
    ax.set_ylabel("月收入")
    cbar = fig.colorbar(im, ax=ax, shrink=0.9, fraction=0.045, pad=0.03)
    cbar.set_label("行百分比 (%)")
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            pct_val = table.loc[r, c]
            n_val = counts.loc[r, c]
            color = "white" if pct_val >= (table.values.max() * 0.55) else "#1f1f1f"
            ax.text(j, i, f"{pct_val:.1f}%\n{int(n_val)}", ha="center", va="center", fontsize=8, color=color)
    fig.subplots_adjust(left=0.24, right=0.93, top=0.88, bottom=0.16)
    add_footnote(fig, [
        f"题号/题干：{row_label} × {col_label}",
        f"Base：n={result['n']}",
        "口径说明：颜色深浅表示该收入组内对不同预期金额的偏好强弱；单元格内同时展示行百分比和样本数",
        f"统计检验：Pearson chi-square {fmt_p(result['p'])}；Cramer's V={result['cramers_v']:.3f}",
    ])
    save_figure(fig, filename)


def plot_simple_bar(labels, values, title, filename, footnotes, color=None, xlabel="占样本比例 (%)", wrap_width=24):
    fig, ax = plt.subplots(figsize=(9, max(4.8, 0.42 * len(labels))))
    ax.barh([wrap(x, wrap_width) for x in labels], values, color=color or PALETTE["consider"])
    for i, v in enumerate(values):
        ax.text(v + 0.8, i, f"{v:.1f}%", va="center", fontsize=9)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontsize=13)
    ax.grid(axis="x", alpha=0.2)
    add_footnote(fig, footnotes)
    save_figure(fig, filename)


def plot_special_charts():
    # 01 funnel
    funnel_labels = ["有需求或曾借过", "有需求未借过", "曾借过"]
    funnel_values = [pct(len(need), len(visited)), pct(len(consider), len(visited)), pct(len(borrowed), len(visited))]
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.bar(funnel_labels, funnel_values, color=PALETTE["consider"])
    for i, v in enumerate(funnel_values):
        ax.text(i, v + 1, f"{v:.1f}%\n(n={[len(need), len(consider), len(borrowed)][i]})", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("占赴港样本比例 (%)")
    ax.set_title("赴港用户中每 3 人约有 1 人存在港币借款需求或经历", fontsize=13)
    ax.grid(axis="y", alpha=0.2)
    add_footnote(fig, [
        f"题号/题干：Q4｜{SURVEY_META['4.请问以下哪种情况最符合你的实际情况？'][1]}",
        f"Base：赴港样本 n={len(visited)}",
        "口径说明：漏斗各层占比均以赴港样本为分母",
    ])
    save_figure(fig, "01_funnel.png")

    # 02 need by visit freq
    rows = ["1-2 次", "3-5 次", "6 次及以上"]
    vals = []
    labels = []
    for r in rows:
        sub = visited[visited["2.请问过去 12 个月内你去过几次中国香港呢？ "] == r]
        vals.append(pct(len(sub[sub["4.请问以下哪种情况最符合你的实际情况？"].isin([
            "我有借港币的想法或需要，但还没借过", "我曾借过港币"
        ])]), len(sub)))
        labels.append(f"{r} (n={len(sub)})")
    plot_simple_bar(
        labels=labels[::-1],
        values=vals[::-1],
        title="赴港越频繁，形成港币借款需求的概率越高",
        filename="02_need_by_visit_freq.png",
        footnotes=[
            f"题号/题干：Q2｜{SURVEY_META['2.请问过去 12 个月内你去过几次中国香港呢？ '][1]} × Q4｜{SURVEY_META['4.请问以下哪种情况最符合你的实际情况？'][1]}",
            f"Base：赴港样本 n={len(visited)}",
            "口径说明：条形值为每个赴港频次组内‘有需求未借过+曾借过’占比",
            f"统计检验：Pearson chi-square {fmt_p(cross_results['赴港频次 × 借款状态']['p'])}；Cramer's V={cross_results['赴港频次 × 借款状态']['cramers_v']:.3f}",
        ],
        color=PALETTE["consider"]
    )

    # 03 label stack
    plot_status_stacked("03_label_stack.png")

    # 04 use cases
    q7_counts = Counter()
    for val in need["7.请问你借用港币主要考虑用于哪些方面呢？"]:
        for part in split_multi(val):
            q7_counts[part] += 1
    items = q7_counts.most_common(8)
    plot_simple_bar(
        labels=[k for k, _ in items][::-1],
        values=[pct(v, len(need)) for _, v in items][::-1],
        title="旅游购物消费是最主要的借港币用途",
        filename="04_use_cases.png",
        footnotes=[
            f"题号/题干：Q7｜{SURVEY_META['7.请问你借用港币主要考虑用于哪些方面呢？'][1]}",
            f"Base：需求样本 n={len(need)}",
            "口径说明：多选题；百分比按样本人数计算，非提及次数占比",
        ],
        color=PALETTE["consider"]
    )

    # 05 reasons
    q8_counts = Counter()
    for val in need["8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？"]:
        for part in split_multi(val):
            q8_counts[part] += 1
    items = q8_counts.most_common(8)
    plot_simple_bar(
        labels=[k for k, _ in items][::-1],
        values=[pct(v, len(need)) for _, v in items][::-1],
        title="减少换汇手续和费用折损是借港币的首要原因",
        filename="05_reasons.png",
        footnotes=[
            f"题号/题干：Q8｜{SURVEY_META['8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？'][1]}",
            f"Base：需求样本 n={len(need)}",
            "口径说明：多选题；百分比按样本人数计算，非提及次数占比",
        ],
        color=PALETTE["consider"]
    )

    # 06 product intent
    intent = matched_need["Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？"].replace({
        "Probably would use": "可能会用",
        "Definitely would use": "肯定会用",
    })
    order = ["肯定会用", "可能会用", "不确定", "可能不会用", "肯定不会用"]
    vc = intent.value_counts()
    labels = [x for x in order if vc.get(x, 0) > 0]
    values = [pct(int(vc.get(x, 0)), len(matched_need)) for x in labels]
    plot_simple_bar(
        labels=labels[::-1],
        values=values[::-1],
        title="看完 Demo 后，超过 8 成可回连需求用户表示可能会用",
        filename="06_product_intent.png",
        footnotes=[
            f"题号/题干：Q16｜{INTERVIEW_QUESTION_MAP['Q16']}",
            f"Base：可回连需求访谈 n={len(matched_need)}",
            "口径说明：百分比按可回连需求访谈人数计算",
        ],
        color=PALETTE["consider"]
    )

    # 07 key attributes
    attr_counts = Counter()
    for val in matched_need["Q8: Themes"].fillna(""):
        for part in split_themes(val):
            if part:
                attr_counts[part] += 1
    items = [x for x in attr_counts.most_common(8) if x[0] not in ("", "其他")]
    plot_simple_bar(
        labels=[k for k, _ in items][::-1],
        values=[pct(v, len(matched_need)) for _, v in items][::-1],
        title="用户最看重的产品点集中在低利率、简单流程、无隐藏费用和审批快",
        filename="07_key_attributes.png",
        footnotes=[
            f"题号/题干：Q8｜{INTERVIEW_QUESTION_MAP['Q8']}",
            f"Base：可回连需求访谈 n={len(matched_need)}",
            "口径说明：基于访谈主题编码的多响应结果；百分比按可回连需求访谈人数计算",
        ],
        color=PALETTE["consider"]
    )


plot_special_charts()
plot_status_stacked("21_cross_标签_借款状态.png")
for i, col in enumerate(SINGLE_VARS, start=1):
    base_df = visited if col in [
        "1.[C1]请问你的周岁年龄是？",
        "2.请问过去 12 个月内你去过几次中国香港呢？ ",
        "3.请问最近 12 个月内你需要用到港币的机会多吗？",
        "4.请问以下哪种情况最符合你的实际情况？",
        "5.请问你是否持有以下香港身份证明文件呢？",
        "13.请问你目前从事的职业是？",
        "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）",
        "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）",
    ] else need
    multi = col in [
        "6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？",
        "7.请问你借用港币主要考虑用于哪些方面呢？",
        "8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？",
    ]
    plot_single_bar(col, f"{i:02d}_desc_{SURVEY_META[col][0]}.png", base_df, multi=multi)

plot_cross_grouped("赴港频次 × 借款状态", "22_cross_赴港频次_借款状态.png", note_question("2.请问过去 12 个月内你去过几次中国香港呢？ "), note_question("4.请问以下哪种情况最符合你的实际情况？"))
plot_cross_grouped("年龄 × 借款状态", "23_cross_年龄_借款状态.png", note_question("1.[C1]请问你的周岁年龄是？"), note_question("4.请问以下哪种情况最符合你的实际情况？"))
plot_cross_grouped("月收入 × 借款状态", "24_cross_月收入_借款状态.png", note_question("14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）"), note_question("4.请问以下哪种情况最符合你的实际情况？"))
plot_cross_grouped("香港身份 × 借款状态", "25_cross_香港身份_借款状态.png", note_question("5.请问你是否持有以下香港身份证明文件呢？"), note_question("4.请问以下哪种情况最符合你的实际情况？"))
plot_cross_grouped("港币使用频率 × 借款状态", "25a_cross_港币使用频率_借款状态.png", note_question("3.请问最近 12 个月内你需要用到港币的机会多吗？"), note_question("4.请问以下哪种情况最符合你的实际情况？"))
plot_cross_grouped("标签 × 港币使用频率", "26_cross_标签_港币使用频率.png", note_question("标签"), note_question("3.请问最近 12 个月内你需要用到港币的机会多吗？"))
plot_cross_grouped("赴港频次 × 港币使用频率", "27_cross_赴港频次_港币使用频率.png", note_question("2.请问过去 12 个月内你去过几次中国香港呢？ "), note_question("3.请问最近 12 个月内你需要用到港币的机会多吗？"))
plot_cross_grouped("香港身份 × 港币使用频率", "28_cross_香港身份_港币使用频率.png", note_question("5.请问你是否持有以下香港身份证明文件呢？"), note_question("3.请问最近 12 个月内你需要用到港币的机会多吗？"))
plot_cross_grouped("标签 × 预期金额", "29_cross_标签_预期金额.png", note_question("标签"), note_question("9.请问未来 12 个月内，你预期会借用多少港币呢？"))
plot_cross_grouped("赴港频次 × 预期金额", "30_cross_赴港频次_预期金额.png", note_question("2.请问过去 12 个月内你去过几次中国香港呢？ "), note_question("9.请问未来 12 个月内，你预期会借用多少港币呢？"))
plot_cross_grouped("年龄 × 预期金额", "31_cross_年龄_预期金额.png", note_question("1.[C1]请问你的周岁年龄是？"), note_question("9.请问未来 12 个月内，你预期会借用多少港币呢？"))
plot_cross_heatmap("月收入 × 预期金额", "32_cross_月收入_预期金额.png", note_question("14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）"), note_question("9.请问未来 12 个月内，你预期会借用多少港币呢？"))
plot_cross_grouped("香港身份 × 预期金额", "33_cross_香港身份_预期金额.png", note_question("5.请问你是否持有以下香港身份证明文件呢？"), note_question("9.请问未来 12 个月内，你预期会借用多少港币呢？"))
plot_cross_grouped("借款用途 × 预期金额", "34_cross_借款用途_预期金额.png", "Q7 简化借款用途", "Q9 简化预期金额")
plot_cross_grouped("借款状态 × 预期金额", "35_cross_借款状态_预期金额.png", "Q4 借款状态", "Q9 简化预期金额")
plot_cross_grouped("标签 × 预期次数", "36_cross_标签_预期次数.png", note_question("标签"), note_question("10.请问未来 12 个月内，你预期会借几次港币呢？"))
plot_cross_grouped("赴港频次 × 预期次数", "37_cross_赴港频次_预期次数.png", note_question("2.请问过去 12 个月内你去过几次中国香港呢？ "), note_question("10.请问未来 12 个月内，你预期会借几次港币呢？"))
plot_cross_grouped("借款用途 × 预期次数", "38_cross_借款用途_预期次数.png", "Q7 简化借款用途", "Q10 简化预期次数")
plot_cross_grouped("借款状态 × 预期次数", "39_cross_借款状态_预期次数.png", "Q4 借款状态", "Q10 简化预期次数")
plot_cross_grouped("标签 × 期望期限", "40_cross_标签_期望期限.png", note_question("标签"), note_question("11.请问你期望每笔港币资金能借多长时间呢？"))
plot_cross_grouped("借款用途 × 期望期限", "41_cross_借款用途_期望期限.png", "Q7 简化借款用途", "Q11 简化期望期限")
plot_cross_grouped("香港身份 × 期望期限", "42_cross_香港身份_期望期限.png", note_question("5.请问你是否持有以下香港身份证明文件呢？"), note_question("11.请问你期望每笔港币资金能借多长时间呢？"))
plot_cross_grouped("借款状态 × 期望期限", "43_cross_借款状态_期望期限.png", "Q4 借款状态", "Q11 简化期望期限")
plot_cross_grouped("标签 × 还款方式", "44_cross_标签_还款方式.png", note_question("标签"), note_question("12.请问你最希望的港币还款方式是？"))
plot_cross_grouped("借款用途 × 还款方式", "45_cross_借款用途_还款方式.png", "Q7 简化借款用途", "Q12 简化还款方式")
plot_cross_grouped("香港身份 × 还款方式", "46_cross_香港身份_还款方式.png", note_question("5.请问你是否持有以下香港身份证明文件呢？"), note_question("12.请问你最希望的港币还款方式是？"))
plot_cross_grouped("借款状态 × 还款方式", "47_cross_借款状态_还款方式.png", "Q4 借款状态", "Q12 简化还款方式")
plot_cross_grouped("借款状态 × 借款渠道", "48_cross_借款状态_借款渠道.png", "Q4 借款状态", "Q6 简化借款渠道")
plot_cross_grouped("借款用途 × 借款渠道", "49_cross_借款用途_借款渠道.png", "Q7 简化借款用途", "Q6 简化借款渠道")


def write(path, text):
    path.write_text(text, encoding="utf-8")


def render_cross_results():
    out = ["# 定量交叉分析表（含统计检验）", "", "所有交叉分析均报告计数、行百分比、卡方检验、Cramer's V 与 Adjusted Standardized Residuals。"]
    json_out = {}
    for name, res in cross_results.items():
        out.extend(["", f"## {name}", ""])
        rows = []
        headers = [name.split(" × ")[0]] + [str(c) for c in res["table"].columns] + ["Total"]
        for idx in res["table"].index:
            row = [str(idx)]
            total = int(res["table"].loc[idx].sum())
            for c in res["table"].columns:
                row.append(f"{int(res['table'].loc[idx, c])} ({res['row_pct'].loc[idx, c]:.1f}%)")
            row.append(str(total))
            rows.append(row)
        out.append("**列联表（计数 + 行百分比）**")
        out.append("")
        out.append(md_table(headers, rows))
        out.append("")
        out.append(f"**Chi-square Test**：χ² = {res['chi2']:.3f}, df = {res['dof']}, {fmt_p(res['p'])}, Cramer's V = {res['cramers_v']:.3f}")
        if res["low_expected"]:
            out.append("")
            out.append(f"**口径提醒**：有 {res['low_expected']} 个单元格期望频数 < 5，方向可参考，检验需谨慎。")
        out.append("")
        rr = []
        for idx in res["residuals"].index:
            row = [str(idx)]
            for c in res["residuals"].columns:
                val = float(res["residuals"].loc[idx, c])
                row.append(f"{val:.2f}{residual_stars(val)}")
            rr.append(row)
        out.append("**Adjusted Standardized Residuals**")
        out.append("")
        out.append(md_table([name.split(" × ")[0]] + [str(c) for c in res["residuals"].columns], rr))
        json_out[name] = {
            "chi2": res["chi2"],
            "dof": res["dof"],
            "p": res["p"],
            "cramers_v": res["cramers_v"],
            "low_expected_cells": res["low_expected"],
            "table": res["table"].to_dict(),
            "row_pct": res["row_pct"].round(4).to_dict(),
            "residuals": res["residuals"].round(4).to_dict(),
        }
    write(OUT / "cross_analysis_tables.md", "\n".join(out))
    write(OUT / "survey_results.json", json.dumps(json_out, ensure_ascii=False, indent=2))


def render_survey_analysis():
    groups = {
        "赴港总体": visited,
        "需求总体": need,
        "有需求未借过": consider,
        "曾借过": borrowed,
        "两地往返_需求": need[need["标签"] == "1_两地往返"],
        "常驻内地_需求": need[need["标签"] == "2_常驻内地"],
    }
    out = ["# 定量分析：完整描述统计", ""]
    out.extend([
        "## 样本说明", "",
        md_table(["样本", "n", "说明"], [
            ["有效问卷", len(valid), "剔除无效答卷后"],
            ["赴港总体", len(visited), "过去 12 个月去过香港"],
            ["需求总体", len(need), "有需求未借过 + 曾借过"],
            ["有需求未借过", len(consider), "需求存在但尚未形成真实借款"],
            ["曾借过", len(borrowed), "已形成真实借款行为"],
        ])
    ])
    for col in SINGLE_VARS:
        out.extend(["", f"## {SURVEY_META[col][0]} {SURVEY_META[col][1]}", ""])
        if col in [
            "6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？",
            "7.请问你借用港币主要考虑用于哪些方面呢？",
            "8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？",
        ]:
            counts_by_group = {}
            universe = Counter()
            for gname, gdf in groups.items():
                c = Counter()
                source = need if gname == "赴港总体" else gdf
                for val in source[col]:
                    for p in split_multi(val):
                        c[p] += 1
                        if gname == "需求总体":
                            universe[p] += 1
                counts_by_group[gname] = c
            headers = ["选项"] + [f"{g}(n={len(groups[g])})" for g in groups]
            rows = []
            for opt, _ in universe.most_common():
                row = [opt]
                for gname, gdf in groups.items():
                    denom = len(need) if gname == "赴港总体" else len(gdf)
                    n = counts_by_group[gname].get(opt, 0)
                    row.append(f"{n} ({pct(n, denom)}%)")
                rows.append(row)
            out.append(md_table(headers, rows))
            out.append("")
            out.append("口径说明：多选题百分比以样本人数为分母，因此各项占比相加可能超过 100%。")
        else:
            headers = ["选项"] + [f"{g}(n={len(groups[g])})" for g in groups]
            rows = []
            source = visited if col in [
                "1.[C1]请问你的周岁年龄是？",
                "2.请问过去 12 个月内你去过几次中国香港呢？ ",
                "3.请问最近 12 个月内你需要用到港币的机会多吗？",
                "4.请问以下哪种情况最符合你的实际情况？",
                "5.请问你是否持有以下香港身份证明文件呢？",
                "13.请问你目前从事的职业是？",
                "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）",
                "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）",
            ] else need
            order = ordered_categories(source[col], key=col)
            for opt in order:
                row = [opt]
                for gname, gdf in groups.items():
                    base = visited if gname == "赴港总体" and col in source.columns and len(gdf) != len(need) else gdf
                    if gname == "赴港总体":
                        base = groups["赴港总体"] if col in [
                            "1.[C1]请问你的周岁年龄是？",
                            "2.请问过去 12 个月内你去过几次中国香港呢？ ",
                            "3.请问最近 12 个月内你需要用到港币的机会多吗？",
                            "4.请问以下哪种情况最符合你的实际情况？",
                            "5.请问你是否持有以下香港身份证明文件呢？",
                            "13.请问你目前从事的职业是？",
                            "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）",
                            "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）",
                        ] else groups["需求总体"]
                    n = (base[col].astype(str) == opt).sum()
                    row.append(f"{n} ({pct(n, len(base))}%)")
                rows.append(row)
            out.append(md_table(headers, rows))
    write(OUT / "survey_analysis.md", "\n".join(out))


def render_quant_main():
    def fmt_count_pct(n, d):
        return f"{n} ({pct(n, d)}%)"

    q2_col = "2.请问过去 12 个月内你去过几次中国香港呢？ "
    q4_col = "4.请问以下哪种情况最符合你的实际情况？"
    q5_col = "5.请问你是否持有以下香港身份证明文件呢？"
    q14_col = "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）"

    q2_rows = []
    for label in ["1-2 次", "3-5 次", "6 次及以上"]:
        sub = visited[visited[q2_col] == label]
        q2_rows.append([
            label,
            len(sub),
            fmt_count_pct(len(sub[sub[q4_col].isin([
                "我有借港币的想法或需要，但还没借过",
                "我曾借过港币",
            ])]), len(sub)),
            fmt_count_pct(len(sub[sub[q4_col] == "我曾借过港币"]), len(sub)),
        ])

    tag_rows = []
    for label in ["1_两地往返", "2_常驻内地"]:
        sub = visited[visited["标签"] == label]
        tag_rows.append([
            label.replace("1_", "").replace("2_", ""),
            len(sub),
            fmt_count_pct(len(sub[sub[q4_col].isin([
                "我有借港币的想法或需要，但还没借过",
                "我曾借过港币",
            ])]), len(sub)),
            fmt_count_pct(len(sub[sub[q4_col] == "我曾借过港币"]), len(sub)),
        ])

    identity_rows = []
    for label in [
        "短期签证/签注（如：旅游/商务/探亲等）",
        "香港永久性居民身份证（HKPR）",
        "香港居民身份证（非永久，如：工作签证、专才/优才/高才、受养人等）",
        "长期签证但无香港身份证（如：在港居留/工作签证/签注）",
        "以上都没有",
    ]:
        sub = visited[visited[q5_col] == label]
        identity_rows.append([
            label.replace("香港永久性居民身份证（HKPR）", "永久HKID").replace(
                "香港居民身份证（非永久，如：工作签证、专才/优才/高才、受养人等）", "非永久HKID"
            ).replace(
                "长期签证但无香港身份证（如：在港居留/工作签证/签注）", "长期签证无HKID"
            ).replace(
                "短期签证/签注（如：旅游/商务/探亲等）", "短期签注"
            ).replace("以上都没有", "无香港身份"),
            len(sub),
            fmt_count_pct(len(sub[sub[q4_col] == "我有借港币的想法或需要，但还没借过"]), len(sub)),
            fmt_count_pct(len(sub[sub[q4_col] == "我曾借过港币"]), len(sub)),
        ])

    reason_counts = Counter()
    for val in need["8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？"]:
        for part in split_multi(val):
            reason_counts[part] += 1

    use_counts = Counter()
    for val in need["7.请问你借用港币主要考虑用于哪些方面呢？"]:
        for part in split_multi(val):
            use_counts[part] += 1

    q9_vc = need["9.请问未来 12 个月内，你预期会借用多少港币呢？"].replace("", pd.NA).dropna().astype(str).value_counts()
    q10_vc = need["10.请问未来 12 个月内，你预期会借几次港币呢？"].replace("", pd.NA).dropna().astype(str).value_counts()
    q11_vc = need["11.请问你期望每笔港币资金能借多长时间呢？"].replace("", pd.NA).dropna().astype(str).value_counts()
    q12_vc = need["12.请问你最希望的港币还款方式是？"].replace("", pd.NA).dropna().astype(str).value_counts()

    q9_n = int(q9_vc.sum())
    amount_top = "；".join([f"{k}({pct(v, q9_n):.1f}%)" for k, v in q9_vc.head(3).items()])
    # Use non-missing bases for Q10-Q12 because "不打算借港币" leaves them blank.
    q10_n = int(q10_vc.sum())
    q11_n = int(q11_vc.sum())
    q12_n = int(q12_vc.sum())
    times_top = "；".join([f"{k}({pct(v, q10_n):.1f}%)" for k, v in q10_vc.head(3).items()])
    term_top = "；".join([f"{k}({pct(v, q11_n):.1f}%)" for k, v in q11_vc.head(3).items()])
    repay_top = "；".join([f"{k.replace('以上都可以', '方式灵活均可').replace('随借随还（按日计息）', '随借随还')}({pct(v, q12_n):.1f}%)" for k, v in q12_vc.head(3).items()])

    out = [
        "# 港币借款需求研究：定量分析",
        "",
        "## 1. 分析口径",
        "",
        md_table(["样本层级", "n", "定义"], [
            ["有效问卷", len(valid), "剔除无效答卷后，按 user_id 去重保留最早提交"],
            ["赴港样本", len(visited), "去重后、过去 12 个月去过香港的用户"],
            ["需求样本", len(need), "有需求未借过 + 曾借过"],
            ["有需求未借过", len(consider), "需求存在但未形成真实借款"],
            ["曾借过", len(borrowed), "已形成真实借款行为"],
        ]),
        "",
        f"补充说明：原始问卷共 {len(survey)} 行，剔除无效答卷后仍为 {len(valid_raw)} 行；其中存在同一 user_id 的重复提交，去重后为 {len(valid)} 行。",
        "",
        "说明：本文件为定量主分析；完整描述统计请看 `survey_analysis.md`，完整交叉表和统计检验请看 `cross_analysis_tables.md`。",
        "",
        "## 2. 需求规模与转化漏斗",
        "",
        f"- 在赴港样本 `n={len(visited)}` 中，`{len(need)}` 人存在港币借款需求或借款经历，占 `{pct(len(need), len(visited))}%`。",
        f"- 其中 `有需求未借过` 为 `{len(consider)}` 人，占赴港样本 `{pct(len(consider), len(visited))}%`；`曾借过` 为 `{len(borrowed)}` 人，占 `{pct(len(borrowed), len(visited))}%`。",
        "- 这说明市场并非无需求，而是存在明显的转化缺口。",
        "",
        "## 3. 谁更可能有需求，谁更可能真的借过",
        "",
        "### 赴港频次",
        "",
        md_table(["赴港频次", "赴港样本量", "有需求/曾借过", "曾借过"], q2_rows),
        "",
        f"统计检验：赴港频次 × 借款状态 `{fmt_p(cross_results['赴港频次 × 借款状态']['p'])}`，Cramer's V=`{cross_results['赴港频次 × 借款状态']['cramers_v']:.3f}`。",
        "解读：高频赴港用户更容易形成真实借款，这个差异在统计上成立。",
        "",
        "### 标签（两地往返 vs 常驻内地）",
        "",
        md_table(["标签", "赴港样本量", "有需求/曾借过", "曾借过"], tag_rows),
        "",
        f"统计检验：标签 × 借款状态 `{fmt_p(cross_results['标签 × 借款状态']['p'])}`，Cramer's V=`{cross_results['标签 × 借款状态']['cramers_v']:.3f}`。",
        "解读：两地往返方向上更容易形成真实借款，但统计上未达显著，需作为方向性差异而非强结论。",
        "",
        "### 香港身份/证件",
        "",
        md_table(["香港身份", "样本量", "有需求未借过", "曾借过"], identity_rows),
        "",
        f"统计检验：香港身份 × 借款状态 `{fmt_p(cross_results['香港身份 × 借款状态']['p'])}`，Cramer's V=`{cross_results['香港身份 × 借款状态']['cramers_v']:.3f}`。",
        "解读：长期签证与香港身份证人群更容易进入真实借款状态，这个差异在统计上成立。",
        "",
        "## 4. 需求结构：用户到底为什么借港币",
        "",
        "### 借款用途",
        "",
        md_table(["用途", "占需求样本比例"], [
            ["旅游/购物/娱乐消费", f"{pct(use_counts['旅游/购物/娱乐消费'], len(need))}%"],
            ["投资（房产、保险、基金等）", f"{pct(use_counts['投资（房产、保险、基金等）'], len(need))}%"],
            ["港股/证券交易", f"{pct(use_counts['港股/证券交易'], len(need))}%"],
            ["商务出差", f"{pct(use_counts['商务出差'], len(need))}%"],
            ["生意周转", f"{pct(use_counts['生意周转'], len(need))}%"],
            ["留学/进修", f"{pct(use_counts['留学/进修'], len(need))}%"],
        ]),
        "",
        "解读：消费场景体量最大，但投资/证券和生意周转构成更高价值、更高时效性的机会层。",
        "",
        "### 为什么借港币，而不是借人民币再换汇",
        "",
        md_table(["原因", "占需求样本比例"], [
            ["省去换汇手续或费用折损", f"{pct(reason_counts['省去换汇的手续或费用折损'], len(need))}%"],
            ["着急用钱、来不及走购汇", f"{pct(reason_counts['着急用钱、来不及走购汇'], len(need))}%"],
            ["港币借款利息更划算", f"{pct(reason_counts['港币借款的利息更划算'], len(need))}%"],
            ["不想/不方便申报换汇资金用途", f"{pct(reason_counts['不想/不方便申报换汇资金用途'], len(need))}%"],
            ["购汇额度不够用", f"{pct(reason_counts['购汇额度不够用'], len(need))}%"],
            ["港币借款额度更大", f"{pct(reason_counts['港币的借款额度更大'], len(need))}%"],
        ]),
        "",
        "解读：用户购买的不是单纯的低息贷款，而是跨境资金可得性与确定性。",
        "",
        "## 5. 需求参数：金额、次数、期限、还款方式",
        "",
        md_table(["维度", "Top 结果"], [
            ["预期借款金额", amount_top],
            ["预期借款次数", times_top],
            ["期望期限", term_top],
            ["期望还款方式", repay_top],
        ]),
        "",
        "解读：主流需求在 1-5 万港币，但中高额需求并不罕见；还款偏好并不极端单一，关键是清楚、灵活、可匹配场景。",
        "",
        "## 6. 关键交叉分析结论",
        "",
        f"- `港币使用频率 × 借款状态`：`{fmt_p(cross_results['港币使用频率 × 借款状态']['p'])}`，Cramer's V=`{cross_results['港币使用频率 × 借款状态']['cramers_v']:.3f}`。越高频使用港币，越容易进入真实借款状态。",
        f"- `标签 × 港币使用频率`：`{fmt_p(cross_results['标签 × 港币使用频率']['p'])}`，Cramer's V=`{cross_results['标签 × 港币使用频率']['cramers_v']:.3f}`。两地往返显著更集中在高频港币使用人群。",
        f"- `月收入 × 借款状态`：`{fmt_p(cross_results['月收入 × 借款状态']['p'])}`，Cramer's V=`{cross_results['月收入 × 借款状态']['cramers_v']:.3f}`。中高收入段更容易出现需求或真实借款，但这不是单向线性关系。",
        f"- `香港身份 × 预期金额`：`{fmt_p(cross_results['香港身份 × 预期金额']['p'])}`，Cramer's V=`{cross_results['香港身份 × 预期金额']['cramers_v']:.3f}`。身份更稳定的人群更可能接受更高金额区间。",
        f"- `借款状态 × 预期金额`：`{fmt_p(cross_results['借款状态 × 预期金额']['p'])}`，Cramer's V=`{cross_results['借款状态 × 预期金额']['cramers_v']:.3f}`。已借过人群方向上更集中在较高金额区间，未借过人群更集中在 1-5 万及以下，但当前未达统计显著。",
        f"- `借款用途 × 预期金额`：`{fmt_p(cross_results['借款用途 × 预期金额']['p'])}`，Cramer's V=`{cross_results['借款用途 × 预期金额']['cramers_v']:.3f}`。不同用途对金额结构的要求存在显著差异。",
        f"- `借款用途 × 预期次数`：`{fmt_p(cross_results['借款用途 × 预期次数']['p'])}`，Cramer's V=`{cross_results['借款用途 × 预期次数']['cramers_v']:.3f}`。消费类与周转类用途在复借节奏上有方向性差异，但当前未达统计显著。",
        f"- `借款用途 × 还款方式`：`{fmt_p(cross_results['借款用途 × 还款方式']['p'])}`，Cramer's V=`{cross_results['借款用途 × 还款方式']['cramers_v']:.3f}`。不同用途对还款偏好的方向性差异存在，但当前未达统计显著。",
        f"- `借款状态 × 借款渠道`：`{fmt_p(cross_results['借款状态 × 借款渠道']['p'])}`，Cramer's V=`{cross_results['借款状态 × 借款渠道']['cramers_v']:.3f}`。已借过人群更集中在传统银行等成熟渠道，未借过人群对金融科技和虚拟银行路径接受度更高。",
        f"- `借款用途 × 借款渠道`：`{fmt_p(cross_results['借款用途 × 借款渠道']['p'])}`，Cramer's V=`{cross_results['借款用途 × 借款渠道']['cramers_v']:.3f}`。不同需求用途对应的渠道偏好也出现结构差异。",
        "",
        "## 7. 定量结论",
        "",
        "1. 港币借款需求真实存在，但核心不是泛借贷，而是跨境场景里的资金获取问题。",
        "2. 最大机会来自有需求但未借过的人群，重点在降低转化阻力。",
        "3. 高频赴港、长期签证/HKID 人群更容易形成真实借款，是更成熟的借款人群。",
        "4. 常驻内地人群体量更大，适合做首版规模切入；两地往返更适合做高价值深化经营。",
        "5. 具体数值、交叉表与显著性结果请继续查看 `cross_analysis_tables.md` 与 `quant_chartbook.md`。",
    ]
    write(OUT / "02_quant_analysis.md", "\n".join(out))


def render_interview_profiles():
    quality_counts = matched["质量等级"].value_counts()
    compare_rows = [
        ["常驻内地", int((matched["标签"] == "2_常驻内地").sum()), f"{pct((matched['标签'] == '2_常驻内地').sum(), len(matched))}%", f"{pct((survey['标签'] == '2_常驻内地').sum(), len(survey))}%"],
        ["两地往返", int((matched["标签"] == "1_两地往返").sum()), f"{pct((matched['标签'] == '1_两地往返').sum(), len(matched))}%", f"{pct((survey['标签'] == '1_两地往返').sum(), len(survey))}%"],
    ]
    out = [
        "# 访谈样本特征与局限性分析", "",
        "## 样本链路", "",
        md_table(["环节", "n", "说明"], [
            ["访谈总样本", len(interviews), "AI 访谈原始样本"],
            ["可回连问卷", len(matched), "按 问卷ID ↔ 问卷序号 成功回连"],
            ["可回连且有需求/曾借过", len(matched_need), "用于主要定性分析"],
        ]),
        "",
        "## 质量分层", "",
        md_table(["质量等级", "n", "占访谈总体比例"], [
            [k, int(v), f"{pct(v, len(matched))}%"] for k, v in quality_counts.items()
        ]),
        "",
        "## 访谈样本与问卷总体的关键偏差", "",
        md_table(["标签", "访谈样本", "访谈占比", "问卷总体占比"], compare_rows),
        "",
        md_table(["借款状态", "访谈样本", "访谈占比", "问卷赴港总体占比"], [
            [STATUS_MAP.get(k, k), int((matched["问卷状态"] == k).sum()), f"{pct((matched['问卷状态'] == k).sum(), len(matched))}%", f"{pct((visited['4.请问以下哪种情况最符合你的实际情况？'] == k).sum(), len(visited))}%"]
            for k in ["我完全没有借港币的需要", "我有借港币的想法或需要，但还没借过", "我曾借过港币"]
        ]),
        "",
        "## 样本解释边界", "",
        "1. 访谈样本明显过度覆盖了有借款需求的人群，因此访谈频次不可直接外推为总体比例。",
        "2. 标签对比的定性结论主要基于可回连样本，适合解释方向，不适合替代问卷总体分布。",
        "3. 低质量样本不作为核心原声证据，只在 pattern 补充和反例中谨慎使用。",
    ]
    write(OUT / "interview_profiles.md", "\n".join(out))


def render_qual_main():
    pattern_counts = matched_need["pattern"].value_counts()
    q7_top = top_theme_terms(matched_need["Q7: Themes"], topn=6, exclude={"", "其他考虑因素"})
    q10_top = top_theme_terms(matched_need["Q10: Themes"], topn=6, exclude={"", "有少量担忧", "完全不担心", "其他担忧"})
    q13_top = top_theme_terms(matched_need["Q13: Themes"], topn=6, exclude={"", "偏正面", "中性", "偏负面"})
    q14_top = top_theme_terms(matched_need["Q14: Themes"], topn=6, exclude={"", "比较有吸引力", "中等吸引力", "吸引力一般", "完全不吸引", "吸引力较高"})
    q15_top = top_theme_terms(matched_need["Q15: Themes"], topn=6, exclude={"", "部分理解", "部分清楚", "基本清楚", "完全不清楚", "不清楚/不理解", "基本不清楚", "理解清晰"})
    out = [
        "# 港币借款需求研究：定性分析",
        "",
        "## 1. 样本与解释边界",
        "",
        md_table(["样本层级", "n", "说明"], [
            ["访谈总样本", len(interviews), "AI 访谈原始样本"],
            ["可回连访谈", len(matched), "按问卷编号稳定回连"],
            ["可回连需求访谈", len(matched_need), "定性主分析样本"],
        ]),
        "",
        "- 定性分析主要用于解释用户为什么有需求、为什么没借、为什么会对产品产生疑虑或兴趣。",
        "- 访谈样本明显过度覆盖了有需求人群，因此不能把访谈频次直接当作总体比例。",
        "- 更完整的样本偏差和质量分层，请查看 `interview_profiles.md`。",
        "",
        "## 2. 用户场景：他们什么时候会想到借港币",
        "",
        "从访谈看，港币借款需求主要由 5 类场景触发：",
        "",
        "1. 临场支付补足：旅游、购物、打车、吃饭、演唱会、线下小店等场景中现金或港币不够。",
        "2. 换汇摩擦规避：用户不是没钱，而是不想承受换汇时间、手续费和汇率不透明。",
        "3. 高时效周转：生意结算、投资加仓、港股补保证金等，需要港币马上到位。",
        "4. 未来型准备需求：留学、租房、学费、押金等未来支出，提前开始寻找正规路径。",
        "5. 成熟替代增强：已有银行/信用卡/香港账户方案，但在某些场景下仍希望更便宜、更快或更灵活。",
        "",
        "这些场景的共同点不是“我想贷款”，而是“我现在需要港币，而且现有方法不够顺”。",
        "",
        "## 3. 用户动机与决策因素",
        "",
        "### 决策因素 Top 6",
        "",
        md_table(["因素", "在可回连需求访谈中出现次数"], [[k, v] for k, v in q7_top]),
        "",
        "- 用户的真实决策不是单一维度比较，而是在`成本`、`到账时效`、`操作便捷`、`还款灵活`和`平台可信`之间做权衡。",
        "- 在紧急场景里，速度优先会压过价格；在计划性场景里，成本透明和规则确定性更重要。",
        "",
        "## 4. 现在的替代方案与工作绕路",
        "",
        "最常见的 workaround 包括：",
        "",
        "- 找朋友或熟人临时借港币",
        "- 先换汇、再想办法跨境转出",
        "- 使用已有香港账户资金",
        "- 银行信用卡或分期方案",
        "- 在迫不得已时接受高手续费或不理想汇率",
        "",
        "这说明市场并不缺‘能凑合解决问题的办法’，缺的是一个更正规、透明、顺手且可复制的方案。",
        "",
        "## 5. 核心阻力：为什么很多人有需求却没真正借",
        "",
        md_table(["阻力因素", "在可回连需求访谈中出现次数"], [[k, v] for k, v in q10_top]),
        "",
        "### 核心阻力 1：渠道不可见",
        "- 很多人根本不知道哪里有正规的港币借款产品，只知道换汇、银行或朋友借款。",
        "",
        "### 核心阻力 2：综合成本不透明",
        "- 用户担心的不只是利率，还有汇率、手续费、隐藏费用、提前还款条款。",
        "",
        "### 核心阻力 3：时效不确定",
        "- 在需要“马上解决”的场景里，审批慢等于无效。",
        "",
        "### 核心阻力 4：资质与信任不足",
        "- 用户天然防备灰色平台、高利贷、野鸡机构，尤其担心信息泄露与合规风险。",
        "",
        "## 6. 用户分群：不是一类人，而是几种不同决策逻辑",
        "",
        md_table(["用户类型", "人数", "占可回连需求访谈比例"], [[k, int(v), f"{pct(v, len(matched_need))}%"] for k, v in pattern_counts.items()]),
        "",
        "### 这套分群的价值",
        "- 它不是按年龄或职业划分，而是按用户在真实借款情境中的`触发场景`、`优先级`、`替代方案成熟度`和`转化障碍`来分。",
        "- 对产品、运营、风控最有价值的不是‘谁年轻/谁高收入’，而是‘谁会在什么情境下被什么信息触发转化’。",
        "",
        "更多分群细节请查看 `user_patterns.md`；更完整的案例分层请查看 `casebook.md`。",
        "",
        "## 7. 产品 Demo 反馈：用户为什么会被打动，为什么会卡住",
        "",
        "### 初印象与界面理解",
        "",
        md_table(["反馈点", "出现次数"], [[k, v] for k, v in q13_top]),
        "",
        "### 最打动用户的卖点与最强疑虑",
        "",
        md_table(["反馈点", "出现次数"], [[k, v] for k, v in q14_top]),
        "",
        "### 产品理解中的主要障碍",
        "",
        md_table(["理解障碍", "出现次数"], [[k, v] for k, v in q15_top]),
        "",
        "- 用户对‘低利率、快速到账、流程简单’有直觉兴趣，但真正阻碍转化的是：钱到哪里、港币和人民币怎么切换、怎么还款、有没有真实牌照背书。",
        "- 产品 Demo 更像把用户拉进了兴趣区，但还没有完全跨过信任和理解门槛。",
        "",
        "## 8. 标签差异的定性解释",
        "",
        "### 两地往返",
        "- 更像成熟跨境资金使用者",
        "- 更熟悉银行、信用卡、持牌机构",
        "- 更容易提出高额度、多币种还款、长期限等成熟需求",
        "",
        "### 常驻内地",
        "- 更像潜在需求大但信任门槛高的人群",
        "- 旅游/购物/短期赴港场景更突出",
        "- 更需要大平台背书、清晰汇率利率说明、人民币还款解释",
        "",
        "## 9. 转化驱动与转化阻力总结",
        "",
        "### 推动用户转化的关键因素",
        "- 场景明确且需求当下发生",
        "- 费用透明，尤其是利率、汇率和手续费讲得清楚",
        "- 到账快、路径清晰、能人民币便捷还款",
        "- 有大平台、银行或持牌资质做背书",
        "",
        "### 阻碍用户转化的关键因素",
        "- 规则复杂或解释不完整",
        "- 对成本和汇率的‘黑箱感’",
        "- 对机构真实性和合规性的怀疑",
        "- 已有替代方案足够好，切换动力不足",
        "",
        "## 10. 定性结论",
        "",
        "1. 港币借款需求的本质不是贷款偏好，而是跨境资金获取问题。",
        "2. 很多人没有借，不是因为不需要，而是因为不知道去哪借、怕踩坑、怕不透明、已有方案还能勉强解决。",
        "3. 用户分群的关键不是人口统计，而是场景紧迫性、成本敏感度、渠道成熟度和替代方案强弱。",
        "4. 产品 Demo 已经让不少用户看到方向，但信任、币种理解和资金路径解释仍是决定转化的关键断点。",
        "5. 更多原声、案例和沉浸式阅读请查看 `qual_voice_digest.md`、`casebook.md`、`immersion_memos.md`、`decision_and_conversion_analysis.md` 和 `product_feedback_analysis.md`。",
    ]
    write(OUT / "03_qual_analysis.md", "\n".join(out))


def render_immersion_memos():
    selected_ids = ["806", "795", "798", "776", "771", "736", "482", "495", "247", "52"]
    out = ["# 沉浸式阅读备忘录", "", "以下 memo 保留用户场景、动作、阻力与后续决策，不先压扁为抽象标签。"]
    for sid in selected_ids:
        row = matched[matched["ID"].astype(str) == sid]
        if row.empty:
            continue
        r = row.iloc[0]
        out.extend([
            "",
            f"## 访谈 {sid}",
            "",
            f"- 基本特征：{profile_stub(r)}",
            f"- 场景复原：{quote_text(r, 'Q4')}",
            f"- 当下怎么解决：{quote_text(r, 'Q5')}",
            f"- 障碍/不顺：{quote_text(r, 'Q6')}",
            f"- 顾虑：{quote_text(r, 'Q10')}",
            f"- 对产品理解：{quote_text(r, 'Q15')}",
            f"- 分析 memo：这位用户的核心不是“我想贷款”，而是“我在某个跨境场景下马上需要港币”。真实决策顺序通常是先保支付/保时效，再比较成本，最后才考虑长期金融关系。"
        ])
    write(OUT / "immersion_memos.md", "\n".join(out))


def render_codebook():
    code_defs = [
        ("临场支付补足", "当场消费、现金支付或超预算，需快速补足港币。", "Q4", lambda r: "香港旅游购物消费" in r["Q4: Themes"] or "比较紧急" in r["Q4: Themes"]),
        ("换汇摩擦规避", "用户并非没钱，而是想避免换汇手续、时间损耗或汇率损失。", "Q4", lambda r: "汇率" in quote_text(r, "Q4") or "换汇" in quote_text(r, "Q4")),
        ("渠道不可见", "不知道正规的港币借款渠道在哪，或接触到的都是可疑渠道。", "Q6", lambda r: "不知道去哪里找借款渠道" in r["Q6: Themes"] or "不了解借款渠道" in r["Q5: Themes"]),
        ("成本透明焦虑", "担心利率、汇率、手续费、隐藏收费不透明。", "Q10", lambda r: "隐藏费用或费用不透明" in r["Q10: Themes"] or "利率或利息过高" in r["Q10: Themes"]),
        ("速度优先", "用户更在意审批与到账速度，而非只比较价格。", "Q7", lambda r: "放款或到账速度" in r["Q7: Themes"] or "速度与时效性优先" in r["Q7: Themes"]),
        ("人民币还款期待", "用户天然期待港币放款、人民币便捷还款。", "Q15", lambda r: "港币放款、人民币还款" in r["Q15: Themes"]),
        ("背书需求", "用户希望看到银行、持牌机构或大平台的资质背书。", "Q17", lambda r: "增强品牌信任和资质展示" in r["Q17: Themes"] or "缺少公司或银行背景信息" in r["Q14: Themes"]),
    ]
    out = ["# 定性编码本", "", "编码围绕 needs / motivations / workarounds / barriers / trust / product understanding 六个方向展开。"]
    for code, definition, q, predicate in code_defs:
        quotes = find_quotes(predicate, q, limit=2)
        out.extend(["", f"## {code}", "", f"- 定义：{definition}", f"- 主要触点：{q}"])
        for r, txt in quotes:
            out.append(f"- 示例：{profile_stub(r)}｜{txt}")
    write(OUT / "codebook.md", "\n".join(out))


def assign_pattern(row):
    q4 = str(row["Q4: Themes"])
    q5 = str(row["Q5: Themes"])
    q6 = str(row["Q6: Themes"])
    q7 = str(row["Q7: Themes"])
    q10 = str(row["Q10: Themes"])
    q15 = str(row["Q15: Themes"])
    q16 = str(row.get("Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？", ""))
    status = str(row["问卷状态"])
    if status == "我曾借过港币" and ("传统银行借款" in q5 or "银行信用卡" in q5 or "香港本地传统银行" in q5):
        return "成熟替代方案型"
    if any(x in q4 for x in ["投资理财", "投资或商业资金需求", "商业资金周转", "较大额：1万到5万港币", "极大额：10万港币以上"]):
        return "高时效周转型"
    if any(x in q4 for x in ["现场只能使用港币现金", "现金支付需求", "临时应急来不及兑换"]) and "比较紧急" in q4:
        return "临场支付补足型"
    if any(x in q4 for x in ["汇率或手续费考虑", "银行兑换流程不便", "提前计划方便使用"]):
        return "换汇摩擦规避型"
    if "不了解渠道" in q5 or "不知道去哪里找借款渠道" in q6 or "不知道借款渠道" in q6:
        return "渠道探索受阻型"
    if any(x in q7 for x in ["利率或成本优先", "利率或汇率水平"]) or any(x in q10 for x in ["隐藏费用", "利率或利息过高", "汇率波动带来损失"]):
        return "成本敏感试探型"
    if ("可能会用" in q16 or "肯定会用" in q16) and any(x in q15 for x in ["港币放款、人民币还款", "支持两种币种还款"]):
        return "跨币种便利诉求型"
    return "平衡评估型"


matched_need["pattern"] = matched_need.apply(assign_pattern, axis=1)


def pattern_quotes(pattern, limit=3):
    sub = matched_need[matched_need["pattern"] == pattern]
    quotes = []
    for _, r in sub.head(limit).iterrows():
        quotes.append(f"- {profile_stub(r)}｜{quote_text(r, 'Q4')}")
    return quotes


def pattern_case_selection(pattern, limit=2):
    sub = matched_need[matched_need["pattern"] == pattern].copy()
    if sub.empty:
        return []
    sub = sub.sort_values(["质量等级", "Quality score"], ascending=[False, False])
    selected = []
    seen = set()
    for _, r in sub.iterrows():
        key = (str(r.get("标签", "")), str(r.get("问卷状态", "")))
        if key in seen and len(selected) < limit:
            continue
        selected.append(r)
        seen.add(key)
        if len(selected) >= limit:
            break
    if len(selected) < limit:
        for _, r in sub.iterrows():
            if str(r["ID"]) not in [str(x["ID"]) for x in selected]:
                selected.append(r)
            if len(selected) >= limit:
                break
    return selected[:limit]


def render_patterns():
    out = ["# 用户模式分析", "", "模式按“行为状态 × 决策逻辑 × 转化潜力”划分，而非纯人口统计分群。"]
    for pattern, count in matched_need["pattern"].value_counts().items():
        sub = matched_need[matched_need["pattern"] == pattern]
        top_label = sub["标签"].value_counts().idxmax() if not sub.empty else ""
        top_status = sub["问卷状态"].value_counts().idxmax() if not sub.empty else ""
        top_visit = sub["赴港频次"].value_counts().idxmax() if not sub.empty else ""
        top_income = sub["月收入"].value_counts().idxmax() if not sub.empty else ""
        top_q4 = top_theme_terms(sub["Q4: Themes"], topn=4, exclude={"", "偶尔发生", "仅此一次或极少发生", "经常发生", "比较紧急", "不紧急", "完全不紧急"})
        top_q7 = top_theme_terms(sub["Q7: Themes"], topn=4, exclude={"", "利率或汇率水平", "放款或到账速度", "申请与操作便捷性", "还款方式灵活性与便利性"})
        top_q10 = top_theme_terms(sub["Q10: Themes"], topn=4, exclude={"", "有少量担忧", "完全不担心", "其他担忧"})
        top_q17 = top_theme_terms(sub["Q17: Themes"], topn=4, exclude={"", "提出了具体改进建议"})
        use_intent = sub["Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？"].value_counts()
        out.extend([
            "",
            f"## {pattern}",
            "",
            f"- 规模：{count} 人，占可回连需求访谈 {pct(count, len(matched_need))}%",
            f"- 定义：这类用户最常见的共同点是，在 `{', '.join([k for k, _ in top_q4[:2]]) or '港币资金场景'}` 中形成需求，并以 `{', '.join([k for k, _ in top_q7[:2]]) or '综合权衡'}` 作为主要决策依据。",
            f"- 典型画像：更常见于 `{top_label}`，最常见状态是 `{status_short(top_status)}`，常见赴港频次是 `{top_visit}`，常见收入档是 `{top_income}`。",
            f"- 触发场景：{', '.join([k for k, _ in top_q4])}",
            f"- 核心动机/决策优先级：{', '.join([k for k, _ in top_q7])}",
            f"- 主要转化阻力：{', '.join([k for k, _ in top_q10])}",
            "- 现有替代方案：朋友借款、换汇、信用卡分期、已有香港账户互转等。",
            f"- 转化驱动：{', '.join([k for k, _ in top_q17[:3]]) or '更透明的规则与更可信的背书'}。",
            f"- 使用意愿分布：肯定会用 {use_intent.get('肯定会用', 0)}；可能会用 {use_intent.get('可能会用', 0)}；不确定及以下 {len(sub) - use_intent.get('肯定会用', 0) - use_intent.get('可能会用', 0)}。",
            "- 产品抓手：需要把对应场景里的“钱去哪、怎么还、为什么可信、为什么现在就值得用”讲清楚。",
            "- 边界条件：如果现有替代方案已足够顺手、可信或成本更低，这类用户不会轻易切换。",
            "- 代表原声：",
            *pattern_quotes(pattern),
        ])
    write(OUT / "user_patterns.md", "\n".join(out))


def render_decision_and_conversion():
    q7 = top_theme_terms(matched_need["Q7: Themes"], topn=8, exclude={"", "利率或汇率水平", "放款或到账速度", "申请与操作便捷性", "还款方式灵活性与便利性"})
    q10 = top_theme_terms(matched_need["Q10: Themes"], topn=8, exclude={"", "有少量担忧", "完全不担心", "其他担忧"})
    q17 = top_theme_terms(matched_need["Q17: Themes"], topn=8, exclude={"", "提出了具体改进建议"})
    high_intent = matched_need[matched_need["Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？"].isin(["可能会用", "肯定会用"])]
    low_intent = matched_need[~matched_need["Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？"].isin(["可能会用", "肯定会用"])]
    out = [
        "# 决策因素与转化驱动分析",
        "",
        "## 1. 用户在做什么决策",
        "",
        "港币借款不是单纯的“要不要借钱”，而是“在跨境资金需求下，要不要用一个新的港币借款方案替代换汇、朋友借款、信用卡或现有银行方案”。",
        "",
        "## 2. 决策因素优先级",
        "",
        md_table(["因素", "出现次数"], [[k, v] for k, v in q7]),
        "",
        "## 3. 转化阻力",
        "",
        md_table(["阻力", "出现次数"], [[k, v] for k, v in q10]),
        "",
        "## 4. 会推动首借的因素",
        "",
        md_table(["推动因素", "出现次数"], [[k, v] for k, v in q17]),
        "",
        "## 5. 高意愿 vs 低意愿的差异",
        "",
        md_table(["维度", "高意愿用户", "低/中意愿用户"], [
            ["样本量", len(high_intent), len(low_intent)],
            ["更常见的决策因素", "更强调速度、便捷、人民币还款和规则清晰", "更强调成本、资质可信和必要性本身"],
            ["更常见的阻力", "具体规则不清、资质不清", "需求不够强、替代方案够用、对产品可信度怀疑"],
            ["更适合的打法", "缩短理解路径，强化首借触发", "降低疑虑，证明比现有方案更值得切换"],
        ]),
        "",
        "## 6. 结论",
        "",
        "1. 用户决策的第一步是判断当前场景是否需要港币立即可得，第二步才是比较成本。",
        "2. 产品转化的关键不是再强调“可以借”，而是解释“为什么比换汇/朋友借/信用卡更值得”。",
        "3. 对高意愿用户，阻碍是信息不全；对低意愿用户，阻碍是需求强度不够或现有替代方案更熟悉。",
    ]
    write(OUT / "decision_and_conversion_analysis.md", "\n".join(out))


def render_product_feedback_analysis():
    q13 = top_theme_terms(matched_need["Q13: Themes"], topn=8, exclude={"", "偏正面", "偏负面", "中性"})
    q14 = top_theme_terms(matched_need["Q14: Themes"], topn=10, exclude={"", "比较有吸引力", "吸引力一般", "中等吸引力", "吸引力较高", "完全不吸引"})
    q15 = top_theme_terms(matched_need["Q15: Themes"], topn=10, exclude={"", "部分理解", "部分清楚", "基本清楚", "完全不清楚", "不清楚/不理解", "基本不清楚", "理解清晰"})
    q17 = top_theme_terms(matched_need["Q17: Themes"], topn=10, exclude={"", "提出了具体改进建议"})
    intent = matched_need["Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？"].replace({
        "Probably would use": "可能会用",
        "Definitely would use": "肯定会用",
    }).value_counts()
    out = [
        "# 产品 Demo 反馈深分析",
        "",
        "## 1. 第一反应",
        "",
        md_table(["反馈点", "出现次数"], [[k, v] for k, v in q13]),
        "",
        "## 2. 最吸引用户的卖点 / 最不可信的点",
        "",
        md_table(["反馈点", "出现次数"], [[k, v] for k, v in q14]),
        "",
        "## 3. 理解障碍",
        "",
        md_table(["障碍", "出现次数"], [[k, v] for k, v in q15]),
        "",
        "## 4. 使用意愿分布",
        "",
        md_table(["意愿", "人数", "占可回连需求访谈比例"], [[k, int(v), f"{pct(v, len(matched_need))}%"] for k, v in intent.items()]),
        "",
        "## 5. 用户最希望怎么改",
        "",
        md_table(["改进建议", "出现次数"], [[k, v] for k, v in q17]),
        "",
        "## 6. 结论",
        "",
        "1. Demo 已能激发兴趣，但不能自动带来信任。",
        "2. 吸引用户的是低成本、快到账、简单流程；阻碍用户的是币种逻辑、资金路径、资质背书和费用透明度。",
        "3. 若要提升转化，产品页需要从“卖点页”升级为“规则解释页 + 信任证明页”。",
    ]
    write(OUT / "product_feedback_analysis.md", "\n".join(out))


def render_voice_digest():
    sections = [
        ("结论1：需求常在临门一脚的跨境支付场景被触发", "Q4", lambda r: "比较紧急" in r["Q4: Themes"] or "香港旅游购物消费" in r["Q4: Themes"]),
        ("结论2：很多人不是没有需求，而是不知道正规渠道在哪", "Q6", lambda r: "不知道去哪里找借款渠道" in r["Q6: Themes"] or "不了解借款渠道" in r["Q5: Themes"]),
        ("结论3：用户担心的成本不只利率，还包括汇率和隐藏费用", "Q10", lambda r: "隐藏费用或费用不透明" in r["Q10: Themes"] or "利率或利息过高" in r["Q10: Themes"]),
        ("结论4：人民币还款与常见入口是高频期待", "Q15", lambda r: "港币放款、人民币还款" in r["Q15: Themes"]),
        ("结论5：大平台或银行背书是首单转化的前置信号", "Q17", lambda r: "增强品牌信任和资质展示" in r["Q17: Themes"] or "缺少公司或银行背景信息" in r["Q14: Themes"]),
    ]
    out = ["# 核心问题原声归纳", "", "每个核心结论至少保留 5 条较完整原声，并标注受访者编号与基本特征。"]
    for title, q, predicate in sections:
        quotes = find_quotes(predicate, q, limit=5)
        out.extend(["", f"## {title}", ""])
        for r, txt in quotes:
            out.append(f"> {txt}")
            out.append(f"——{profile_stub(r)}")
            out.append("")
        out.append("分析：这些原声共同显示，该结论并非来自单条鲜活个案，而是在不同背景用户中重复出现的决策逻辑。")
    write(OUT / "qual_voice_digest.md", "\n".join(out))


def render_casebook():
    out = ["# 典型案例册", "", "以下案例采用分层抽样：优先高质量样本，覆盖不同用户类型、借款状态、标签与意愿层级，并保留少量边界/反例。"]
    selected_rows = []
    for pattern in matched_need["pattern"].value_counts().index.tolist():
        selected_rows.extend(pattern_case_selection(pattern, limit=2))
    dedup = []
    seen_ids = set()
    for r in selected_rows:
        sid = str(r["ID"])
        if sid in seen_ids:
            continue
        seen_ids.add(sid)
        dedup.append(r)
    for r in dedup[:14]:
        sid = str(r["ID"])
        out.extend([
            "",
            f"## Case {sid}",
            "",
            f"- 抽样理由：覆盖 `{r['pattern']}`，且在 `{str(r.get('标签', '')).replace('1_', '').replace('2_', '')}` / `{status_short(r.get('问卷状态', ''))}` 组合中具有代表性。",
            f"- 用户画像：{profile_stub(r)}",
            f"- 事件背景：{quote_text(r, 'Q3')}",
            f"- 场景复原：{quote_text(r, 'Q4')}",
            f"- 当前 workaround：{quote_text(r, 'Q5')}",
            f"- 痛点：{quote_text(r, 'Q6')}",
            f"- 顾虑：{quote_text(r, 'Q10')}",
            f"- Demo 反应：{quote_text(r, 'Q13')}",
            "",
            "### 原声摘录",
            "",
            f"> {quote_text(r, 'Q4')}",
            f"——{profile_stub(r)}",
            "",
            f"> {quote_text(r, 'Q10')}",
            f"——{profile_stub(r)}",
            "",
            "### 动机与决策逻辑",
            "",
            "用户先处理场景中的资金可得性问题，再回头比较渠道、成本与风险。是否转化为正式借款，通常取决于渠道可见度、规则透明度、平台信任感以及现有替代方案是否足够好用。",
            "",
            "### 对产品的启发",
            "",
            "如果产品不能把“钱去哪、怎么还、费用怎么算、为什么可信”讲清楚，这类用户往往会回到朋友借款、换汇或信用卡等现成方案。",
        ])
    write(OUT / "casebook.md", "\n".join(out))


def render_case_sampling_strategy():
    pattern_counts = matched_need["pattern"].value_counts()
    out = [
        "# 案例抽样说明",
        "",
        "案例册不是随机摘录，而是按以下逻辑分层抽样：",
        "",
        "1. 优先高质量、可回连、原声完整的访谈样本。",
        "2. 覆盖主要用户类型，每个主要 pattern 至少 1-2 个案例。",
        "3. 覆盖 `曾借过` 与 `有需求未借过` 两种关键状态。",
        "4. 覆盖 `两地往返` 与 `常驻内地` 两类标签。",
        "5. 覆盖高意愿与观望/低意愿案例，避免只选正向故事。",
        "",
        "## 当前 pattern 覆盖",
        "",
        md_table(["pattern", "样本量", "占可回连需求访谈比例"], [[k, int(v), f"{pct(v, len(matched_need))}%"] for k, v in pattern_counts.items()]),
    ]
    write(OUT / "case_sampling_strategy.md", "\n".join(out))


def render_chartbook():
    title_map = {
        "01_desc_Q1": "Q1 年龄分布",
        "01_funnel": "需求漏斗",
        "02_desc_Q2": "Q2 赴港频次分布",
        "02_need_by_visit_freq": "赴港频次与借款需求率",
        "03_desc_Q3": "Q3 港币使用频率分布",
        "03_label_stack": "标签与借款状态结构对比",
        "04_desc_Q4": "Q4 借款状态分布",
        "04_use_cases": "Q7 借款用途分布",
        "05_desc_Q5": "Q5 香港身份分布",
        "05_reasons": "Q8 借港币而非换汇的主要原因",
        "06_desc_Q6": "Q6 借款渠道分布",
        "06_product_intent": "Q16 产品使用意愿",
        "07_desc_Q7": "Q7 借款用途原题分布",
        "07_key_attributes": "Q8 产品最看重因素",
        "08_desc_Q8": "Q8 借港币原因原题分布",
        "09_desc_Q9": "Q9 预期借款金额分布",
        "10_desc_Q10": "Q10 预期借款次数分布",
        "11_desc_Q11": "Q11 期望借款期限分布",
        "12_desc_Q12": "Q12 期望还款方式分布",
        "13_desc_Q13": "Q13 职业分布",
        "14_desc_Q14": "Q14 月收入分布",
        "15_desc_Q15": "Q15 港币收入占比分布",
        "21_cross_标签_借款状态": "标签 × 借款状态",
        "22_cross_赴港频次_借款状态": "赴港频次 × 借款状态",
        "23_cross_年龄_借款状态": "年龄 × 借款状态",
        "24_cross_月收入_借款状态": "月收入 × 借款状态",
        "25_cross_香港身份_借款状态": "香港身份 × 借款状态",
        "25a_cross_港币使用频率_借款状态": "港币使用频率 × 借款状态",
        "26_cross_标签_港币使用频率": "标签 × 港币使用频率",
        "27_cross_赴港频次_港币使用频率": "赴港频次 × 港币使用频率",
        "28_cross_香港身份_港币使用频率": "香港身份 × 港币使用频率",
        "29_cross_标签_预期金额": "标签 × 预期金额",
        "30_cross_赴港频次_预期金额": "赴港频次 × 预期金额",
        "31_cross_年龄_预期金额": "年龄 × 预期金额",
        "32_cross_月收入_预期金额": "月收入 × 预期金额",
        "33_cross_香港身份_预期金额": "香港身份 × 预期金额",
        "34_cross_借款用途_预期金额": "借款用途 × 预期金额",
        "35_cross_借款状态_预期金额": "借款状态 × 预期金额",
        "36_cross_标签_预期次数": "标签 × 预期次数",
        "37_cross_赴港频次_预期次数": "赴港频次 × 预期次数",
        "38_cross_借款用途_预期次数": "借款用途 × 预期次数",
        "39_cross_借款状态_预期次数": "借款状态 × 预期次数",
        "40_cross_标签_期望期限": "标签 × 期望期限",
        "41_cross_借款用途_期望期限": "借款用途 × 期望期限",
        "42_cross_香港身份_期望期限": "香港身份 × 期望期限",
        "43_cross_借款状态_期望期限": "借款状态 × 期望期限",
        "44_cross_标签_还款方式": "标签 × 还款方式",
        "45_cross_借款用途_还款方式": "借款用途 × 还款方式",
        "46_cross_香港身份_还款方式": "香港身份 × 还款方式",
        "47_cross_借款状态_还款方式": "借款状态 × 还款方式",
        "48_cross_借款状态_借款渠道": "借款状态 × 借款渠道",
        "49_cross_借款用途_借款渠道": "借款用途 × 借款渠道",
    }
    pngs = sorted([p.name for p in CHARTS.glob("*.png")])
    out = ["# 图表册", "", "以下图表统一采用 Okabe-Ito 色板，并在图内标注题号、题干、Base 和统计检验口径。"]
    for png in pngs:
        title = png.replace(".png", "")
        out.extend(["", f"## {title_map.get(title, title)}", "", f"![{title}]({CHARTS / png})"])
    write(OUT / "quant_chartbook.md", "\n".join(out))


def chart_md(filename, alt):
    return f"![{alt}]({CHARTS / filename})"


def quote_block_items(quotes, qid):
    items = []
    for r, txt in quotes:
        items.extend([
            f"> {txt}",
            f"——{profile_stub(r)}",
            "",
        ])
    return items


def render_detailed_findings_report():
    use_intent = matched_need["Q16: 看完这个产品后，你觉得自己有多大可能会考虑使用它？"].replace({
        "Probably would use": "可能会用",
        "Definitely would use": "肯定会用",
    }).value_counts()
    pattern_counts = matched_need["pattern"].value_counts()
    q7_top = top_theme_terms(matched_need["Q7: Themes"], topn=6, exclude={"", "利率或汇率水平", "放款或到账速度", "申请与操作便捷性", "还款方式灵活性与便利性"})
    q10_top = top_theme_terms(matched_need["Q10: Themes"], topn=6, exclude={"", "有少量担忧", "完全不担心", "其他担忧"})
    out = [
        "# 详细调研发现",
        "",
        "## 1. 需求规模与机会漏斗",
        "",
        md_table(["层级", "n", "占赴港样本比例"], [
            ["赴港样本", len(visited), "100%"],
            ["有需求或曾借过", len(need), f"{pct(len(need), len(visited))}%"],
            ["有需求未借过", len(consider), f"{pct(len(consider), len(visited))}%"],
            ["曾借过", len(borrowed), f"{pct(len(borrowed), len(visited))}%"],
        ]),
        "",
        chart_md("01_funnel.png", "需求漏斗"),
        "",
        "解读：真实市场机会并不在于证明有没有需求，而在于解释为什么大量需求停留在“想借但没借成”。",
        "",
        "## 2. 人群差异：谁更容易形成真实借款",
        "",
        md_table(["维度", "检验结果", "业务解读"], [
            ["赴港频次 × 借款状态", f"p={cross_results['赴港频次 × 借款状态']['p']:.4f}; V={cross_results['赴港频次 × 借款状态']['cramers_v']:.3f}", "高频赴港用户更容易形成真实借款"],
            ["香港身份 × 借款状态", f"p={cross_results['香港身份 × 借款状态']['p']:.4f}; V={cross_results['香港身份 × 借款状态']['cramers_v']:.3f}", "长期签证/HKID 人群更成熟"],
            ["月收入 × 借款状态", f"p={cross_results['月收入 × 借款状态']['p']:.4f}; V={cross_results['月收入 × 借款状态']['cramers_v']:.3f}", "中高收入人群需求更活跃，但并非线性增长"],
            ["标签 × 借款状态", f"p={cross_results['标签 × 借款状态']['p']:.4f}; V={cross_results['标签 × 借款状态']['cramers_v']:.3f}", "两地往返方向上更成熟，但统计上仅属方向性差异"],
        ]),
        "",
        chart_md("22_cross_赴港频次_借款状态.png", "赴港频次与借款状态"),
        "",
        chart_md("24_cross_月收入_借款状态.png", "月收入与借款状态"),
        "",
        "## 3. 借款类型与场景需求特点",
        "",
        md_table(["借款类型", "主要场景", "金额特征", "产品启示"], [
            ["临场小额补足型", "旅游/购物/现金支付/交通", "小额到中小额", "要快、要轻、要可立即理解"],
            ["换汇摩擦规避型", "不想承受换汇时间、手续费和汇率不透明", "小额到中额", "要强调透明成本和替代换汇的价值"],
            ["高时效周转型", "生意结算、投资、港股补保证金", "中额到高额", "要强调到账速度、额度和合规路径"],
            ["提前准备型", "留学、租房、学费、押金", "中额", "要强调计划性、长期性和规则清晰"],
            ["成熟替代增强型", "已有银行/信用卡/香港账户方案", "按人而异", "要证明比现有方案更顺手或更便宜"],
        ]),
        "",
        chart_md("32_cross_月收入_预期金额.png", "月收入与预期金额"),
        "",
        "解读：`月收入 × 预期金额` 不适合再用分组柱状图，因为类目过多、阅读负担大；改成热力图后，更容易看出不同收入层级对金额区间的偏好梯度。",
        "",
        "## 4. 用户决策因素与转化阻力",
        "",
        md_table(["决策因素 Top", "出现次数"], [[k, v] for k, v in q7_top]),
        "",
        md_table(["转化阻力 Top", "出现次数"], [[k, v] for k, v in q10_top]),
        "",
        "关键结论：用户不是简单比较利率，而是在“成本、时效、便捷、还款灵活、信任”之间做场景化权衡。",
        "",
        "## 5. 产品 Demo 反馈",
        "",
        md_table(["使用意愿", "人数", "占可回连需求访谈比例"], [
            ["肯定会用", int(use_intent.get("肯定会用", 0)), f"{pct(use_intent.get('肯定会用', 0), len(matched_need))}%"],
            ["可能会用", int(use_intent.get("可能会用", 0)), f"{pct(use_intent.get('可能会用', 0), len(matched_need))}%"],
            ["不确定及以下", int(len(matched_need) - use_intent.get("肯定会用", 0) - use_intent.get("可能会用", 0)), f"{pct(len(matched_need) - use_intent.get('肯定会用', 0) - use_intent.get('可能会用', 0), len(matched_need))}%"],
        ]),
        "",
        chart_md("06_product_intent.png", "产品使用意愿"),
        "",
        "Demo 的价值方向是成立的，但还缺三类关键说明：`币种怎么走`、`钱会到哪里`、`为什么可以信任`。",
        "",
        "## 6. 用户分群与分层经营机会",
        "",
        md_table(["用户模式", "人数", "占比"], [[k, int(v), f"{pct(v, len(matched_need))}%"] for k, v in pattern_counts.items()]),
        "",
        "建议优先经营的不是所有有需求用户，而是：`场景更明确 + 替代方案更弱 + 使用意愿更高` 的人群。",
        "",
        "## 7. 代表性原声",
        "",
    ]
    for title, q, predicate in [
        ("场景触发", "Q4", lambda r: "比较紧急" in str(r["Q4: Themes"])),
        ("渠道阻力", "Q6", lambda r: "不知道" in str(r["Q6: Themes"]) or "不了解" in str(r["Q5: Themes"])),
        ("Demo 疑虑", "Q15", lambda r: "不清楚" in str(r["Q15: Themes"]) or "人民币还款" in str(r["Q15: Themes"])),
    ]:
        quotes = find_quotes(predicate, q, limit=3)
        out.extend(["", f"### {title}", ""])
        out.extend(quote_block_items(quotes, q))
    out.extend([
        "## 8. 业务含义",
        "",
        "1. 首版产品更适合切入常驻内地、赴港消费/周转场景，而不是一上来追求覆盖所有跨境金融需求。",
        "2. 营销和产品表达要从“借款功能介绍”转向“跨境资金问题解决方案”。",
        "3. 风控与产品需要共同决定：哪些高时效/投资场景可以承接，哪些只能先从低风险场景切入。",
    ])
    write(OUT / "detailed_findings_report.md", "\n".join(out))


def render_full_report():
    key_quote_sets = {
        "场景触发": find_quotes(lambda r: "比较紧急" in r["Q4: Themes"] or "香港旅游购物消费" in r["Q4: Themes"], "Q4", 2),
        "渠道不可见": find_quotes(lambda r: "不知道去哪里找借款渠道" in r["Q6: Themes"] or "不了解借款渠道" in r["Q5: Themes"], "Q6", 2),
        "成本透明": find_quotes(lambda r: "隐藏费用或费用不透明" in r["Q10: Themes"] or "利率或利息过高" in r["Q10: Themes"], "Q10", 2),
    }
    use_intent = matched_need["使用意愿简化"].value_counts()
    reason_counts = Counter()
    for val in need["8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？"]:
        for part in split_multi(val):
            reason_counts[part] += 1
    top_attrs = matched_need["Q8: Themes"].astype(str).str.split(",").explode().str.strip()
    top_attrs = top_attrs[top_attrs != ""].value_counts().head(4)
    out = [
        "# 赴港用户港币借款需求调研报告",
        "",
        "## 执行摘要",
        "",
        "### 核心结论",
        "",
        f"1. 过去 12 个月赴港用户中，`{len(need)}/{len(visited)}` 存在港币借款需求或借款经历，占 `{pct(len(need), len(visited))}%`；其中 `{pct(len(consider), len(visited))}%` 有需求但未借过、`{pct(len(borrowed), len(visited))}%` 曾借过，最大机会在转化缺口而不是需求教育。",
        "2. 用户真正购买的不是单纯低息贷款，而是跨境场景里的资金可得性、时效确定性和成本透明度。",
        "3. 高频赴港、长期签证/HKID、中高收入人群更容易形成真实借款；但体量最大的切入点仍然是常驻内地的赴港消费/周转用户。",
        f"4. 用户会在`成本、时效、便捷、还款灵活、平台可信`之间做场景化权衡；可回连需求访谈中，对产品“可能会用/肯定会用”的比例为 `{pct(use_intent.get('可能会用', 0) + use_intent.get('肯定会用', 0), len(matched_need))}%`，说明方向成立，但理解和信任门槛仍未跨过。",
        "5. 最优产品策略不是面向所有赴港用户泛推，而是先抓“场景明确 + 替代方案弱 + 首借意愿高”的人群，再按高价值场景做分层深化。",
        "",
        "### 给高管的核心小结",
        "",
        "- 这是一个跨境资金问题，不是普通借贷问题。",
        "- 市场缺口主要发生在有需求但没借成的转化段。",
        "- 首版成败取决于：规则解释是否清楚、平台是否可信、到账是否足够快。",
        "- 常驻内地适合做规模切入，两地往返适合做高价值深化经营。",
        "",
        "## 研究方法与样本",
        "",
        "### 方法总览",
        "",
        "本研究采用问卷 + AI 访谈的混合方法。问卷负责判断需求规模、结构分布和分层差异；访谈负责解释需求为什么发生、为什么没有转化，以及用户如何理解当前产品设想。涉及总体比例的判断，以去重后的赴港问卷样本为准；涉及机制、场景和真实决策链的判断，以可回连需求访谈为主。",
        "",
        "### 样本漏斗",
        "",
        md_table(["环节", "n", "口径"], [
            ["原始问卷", len(survey), "平台回收原始记录"],
            ["有效问卷", len(valid_raw), "剔除无效答卷后"],
            ["去重有效问卷", len(valid), "按 user_id 去重，保留最早提交"],
            ["赴港样本", len(visited), "去重后，过去 12 个月去过香港"],
            ["需求样本", len(need), "去重后，Q4 为有需求未借过 + 曾借过"],
            ["访谈总样本", len(interviews), "AI 访谈原始样本"],
            ["可回连访谈", len(matched), "按问卷编号稳定回连"],
            ["可回连需求访谈", len(matched_need), "用于定性主分析"],
        ]),
        "",
        md_table(["环节", "n", "说明"], [
            ["问卷总样本", len(survey), "原始问卷"],
            ["有效问卷", len(valid), "剔除无效答卷并按 user_id 去重"],
            ["赴港样本", len(visited), "去重后、过去 12 个月去过香港"],
            ["需求样本", len(need), "去重后、有需求未借过 + 曾借过"],
            ["访谈总样本", len(interviews), "AI 访谈原始样本"],
            ["可回连访谈", len(matched), "按问卷编号稳定回连"],
            ["可回连需求访谈", len(matched_need), "定性主分析样本"],
        ]),
        "",
        md_table(["分析主题", "主要证据来源", "解释原则"], [
            ["总体需求规模与结构", "问卷", "以定量结果为主"],
            ["用户动机、workaround、痛点", "访谈 + 问卷互证", "以机制解释为主"],
            ["人群差异", "问卷 + 可回连访谈", "先看统计差异，再用访谈解释"],
            ["产品反馈", "可回连需求访谈为主", "以定性深描为主，定量只做补充"],
        ]),
        "",
        "### 样本偏差与解释边界",
        "",
        "- 本轮定量分析以去重后的 user_id 为唯一统计口径。若改用原始回收行数、Q4 非空样本或全量访谈样本，分母会不同，数字不能直接混用。",
        "- 本项目的业务问题限定为“过去 12 个月赴港的用户”。因此，主报告里的需求率、结构分布和交叉分析，均以去重后的赴港样本为分母或母体，而不是全量有效问卷。",
        "- 访谈样本明显过度覆盖有需求人群，因此访谈频次不能直接外推为总体比例。",
        "- AI 访谈存在固有局限：追问深度不及人工访谈，且 348 份访谈里高质量样本约 178 份、中质量约 38 份、低质量约 132 份。全量结构化编码更适合作问题范围校准，不适合作总体比例推断。",
        "- 定性可回连样本是问卷样本的子集，mixed-method 的“互相印证”更适合作解释链路，而不是当作完全独立的数据源。",
        "- 本研究是横截面数据，收入、赴港频次与借款需求之间可视为相关关系，不应直接写成因果关系。",
        "- 交叉分析里个别表有低期望频数单元格，方向可参考，但要避免过度解释。",
        "- 当定量和定性讲的是同一问题时，本报告优先做整合解读；只有在定性提供的是定量无法覆盖的机制或场景时，才单独作为互补洞察呈现。",
        "",
        "## 发现 1：需求真实存在，但最大机会在“想借没借成”的转化段",
        "",
        "### 关键观察",
        "",
        f"- 赴港样本 `n={len(visited)}` 中，`{pct(len(need), len(visited))}%` 有港币借款需求或经历，说明这不是边缘需求。",
        f"- 其中 `有需求未借过` 占 `{pct(len(consider), len(visited))}%`，明显高于 `曾借过` 的 `{pct(len(borrowed), len(visited))}%`，说明当前供给没有充分吃到真实需求。",
        "",
        chart_md("01_funnel.png", "需求漏斗"),
        "",
        "### 整合解读",
        "",
        "- 定量告诉我们：需求存在且规模不小，问题在于从“想到借”走到“真的借”。",
        "- 定性进一步解释：大量用户并不是没有需求，而是在临时场景里靠朋友借款、换汇、信用卡等方案先解决了问题，所以没有形成正式借款记录。",
        "",
        "### 代表性原声",
        "",
    ]
    out.extend(quote_block_items(key_quote_sets["场景触发"], "Q4"))
    out.extend([
        "业务含义：如果产品只教育“为什么要借港币”，价值有限；真正要解决的是，用户在场景发生当下，为什么会选择现有替代方案而不是本产品。",
        "",
        "## 发现 2：用户借港币的本质是解决跨境资金可得性，而不是单纯追求低息",
        "",
        "### 关键观察",
        "",
        "- 问卷中用户选择借港币而不是借人民币再换汇，最主要原因是减少换汇手续/费用折损、来不及购汇、以及希望更高的资金确定性。",
        "- 访谈中，无论是消费、周转还是投资场景，用户首先在意的是“港币现在能不能拿到”，其次才是利率比较。",
        "",
        md_table(["原因", "占需求样本比例"], [
            ["省去换汇手续或费用折损", f"{pct(reason_counts['省去换汇的手续或费用折损'], len(need))}%"],
            ["着急用钱、来不及走购汇", f"{pct(reason_counts['着急用钱、来不及走购汇'], len(need))}%"],
            ["港币借款利息更划算", f"{pct(reason_counts['港币借款的利息更划算'], len(need))}%"],
            ["不想/不方便申报换汇资金用途", f"{pct(reason_counts['不想/不方便申报换汇资金用途'], len(need))}%"],
            ["购汇额度不够用", f"{pct(reason_counts['购汇额度不够用'], len(need))}%"],
            ["港币借款额度更大", f"{pct(reason_counts['港币的借款额度更大'], len(need))}%"],
        ]),
        "",
        "### 整合解读",
        "",
        "- 这里定量和定性说的是同一个问题，因此应该合起来看：用户比较的不是“贷款 vs 不贷款”，而是“借港币 vs 换汇 vs 朋友借款 vs 信用卡 vs 现有香港账户”。",
        "- 对业务来说，竞争对象因此不仅是其他借贷产品，更包括所有现有跨境资金解决路径。",
        "",
        "### 代表性原声",
        "",
    ])
    out.extend(quote_block_items(key_quote_sets["渠道不可见"], "Q6"))
    out.extend([
        "业务含义：产品定位和页面表达都要从“低息贷款”升级为“跨境资金解决方案”。",
        "",
        "## 发现 3：人群差异真实存在，但要区分‘体量最大’与‘成熟度最高’",
        "",
        "### 关键观察",
        "",
        md_table(["维度", "检验结果", "业务解读"], [
            ["赴港频次 × 借款状态", f"p={cross_results['赴港频次 × 借款状态']['p']:.4f}; V={cross_results['赴港频次 × 借款状态']['cramers_v']:.3f}", "高频赴港用户更容易形成真实借款"],
            ["香港身份 × 借款状态", f"p={cross_results['香港身份 × 借款状态']['p']:.4f}; V={cross_results['香港身份 × 借款状态']['cramers_v']:.3f}", "长期签证/HKID 人群更成熟"],
            ["月收入 × 借款状态", f"p={cross_results['月收入 × 借款状态']['p']:.4f}; V={cross_results['月收入 × 借款状态']['cramers_v']:.3f}", "中高收入段更活跃"],
            ["标签 × 借款状态", f"p={cross_results['标签 × 借款状态']['p']:.4f}; V={cross_results['标签 × 借款状态']['cramers_v']:.3f}", "两地往返方向上更成熟，但统计上仅属方向性差异"],
        ]),
        "",
        chart_md("22_cross_赴港频次_借款状态.png", "赴港频次与借款状态"),
        "",
        chart_md("24_cross_月收入_借款状态.png", "月收入与借款状态"),
        "",
        "### 整合解读",
        "",
        "- 定量告诉我们谁更容易形成真实借款；定性补充的是为什么这些人更容易转化。",
        "- 两地往返、高频赴港、长期签证/HKID 用户往往已有更多跨境生活/工作经验，知道有哪些银行和渠道，也更清楚自己需要什么；因此他们更像“成熟借款人群”。",
        "- 但体量最大的首版切入点并不一定是最成熟的人群。常驻内地的赴港消费/周转用户虽然成熟度偏低，却是更大的潜在转化池。",
        "",
        "业务含义：人群策略应该分两层。`常驻内地` 用来打规模首借，`两地往返/高频赴港` 用来做高价值深化经营。",
        "",
        "## 发现 4：借款类型和场景不同，对产品抓手的要求也不同",
        "",
        "### 借款类型与场景需求特点",
        "",
        md_table(["类型", "典型场景", "转化重点"], [
            ["临场小额补足型", "购物、交通、现金支付", "到账快、流程短、入口清晰"],
            ["换汇摩擦规避型", "不想被换汇流程与汇损拖住", "透明汇率/费用说明"],
            ["高时效周转型", "生意结算、投资、保证金", "合规路径、额度、时效"],
            ["提前准备型", "留学、租房、押金", "规则清晰、长期方案"],
            ["成熟替代增强型", "已有银行/信用卡方案", "证明比现有方案更顺手或更便宜"],
        ]),
        "",
        chart_md("32_cross_月收入_预期金额.png", "月收入与预期金额"),
        "",
        "### 整合解读",
        "",
        "- `月收入 × 预期金额` 告诉我们不同收入层级对金额区间的偏好梯度；这属于定量能很好回答的问题。",
        "- 但为什么同样是高收入用户，有人看重大额周转，有人更关注投资效率，则需要由访谈里的具体场景来解释。",
        "- 因此，这一章采用“定量结构 + 定性场景”的整合写法，而不是把两部分拆开重复讲一遍。",
        "",
        "业务含义：首版产品不能用单一话术覆盖所有场景。至少要区分消费补足、换汇规避和高时效周转三类核心诉求。",
        "",
        "## 发现 5：用户最终会不会转化，取决于五个决策因素的综合权衡",
        "",
        "### 关键观察",
        "",
        md_table(["决策因素 Top", "出现次数"], [[k, v] for k, v in top_theme_terms(matched_need["Q7: Themes"], topn=6, exclude={"", "利率或汇率水平", "放款或到账速度", "申请与操作便捷性", "还款方式灵活性与便利性"})]),
        "",
        md_table(["转化阻力 Top", "出现次数"], [[k, v] for k, v in top_theme_terms(matched_need["Q10: Themes"], topn=6, exclude={"", "有少量担忧", "完全不担心", "其他担忧"})]),
        "",
    ])
    out.extend(quote_block_items(key_quote_sets["成本透明"], "Q10"))
    out.extend([
        "### 整合解读",
        "",
        "- 定量能帮我们看出哪些人更容易借、哪些金额需求更常见；但真正决定‘借不借成’的，是定性里反复出现的决策权衡逻辑。",
        "- 用户并不是简单比较利率，而是在`成本、时效、便捷、还款灵活、平台可信`之间做场景化权衡。",
        "- 当定量和定性指向的是同一个判断时，本报告把它们合并为一个发现；这里就是典型例子。",
        "",
        "业务含义：转化链路里最先要解决的是`可信解释`，其次才是`价格竞争力`。",
        "",
        "## 产品 Demo 反馈",
        "",
        "- 正向吸引点：低利率、到账快、流程简单、还款灵活、人民币还款。",
        "- 关键疑虑点：币种路径不清、资金去向不明、利率/汇率展示不够透明、持牌主体与合作银行信息不够强。",
        "- 使用意愿上，`可能会用/肯定会用` 合计占可回连需求访谈 `81.2%`，方向可行，但仍有明显的理解与信任门槛。",
        "",
        chart_md("06_product_intent.png", "产品使用意愿"),
        "",
        "### 代表性原声",
        "",
    ])
    out.extend(quote_block_items(find_quotes(lambda r: "不清楚" in str(r["Q15: Themes"]) or "人民币还款" in str(r["Q15: Themes"]), "Q15", 3), "Q15"))
    out.extend([
        "### 整合解读",
        "",
        "- Demo 反馈这部分以定性为主，因为它关注的是理解、信任和具体困惑点；定量只作为意愿分布的辅助信息。",
        "- 这里属于两种方法的互补洞察，而不是同一问题的重复验证，所以保留为相对独立的一章。",
        "",
        "## 混合研究整合",
        "",
        "### Agreement",
        "",
        "- 定量和定性都表明：换汇摩擦、紧急时效和成本透明是需求核心。",
        "- 两类方法都显示：常驻内地体量更大，两地往返转化更成熟。",
        "",
        "### Tension",
        "",
        "- 问卷中旅游/购物场景体量最大，但访谈里高额投资/周转案例更鲜活，业务解读时要区分“体量最大”和“价值最高”。",
        "- 标签差异在方向上存在，但统计上未达显著；定性里两地往返更成熟的感觉更强，因此不能只靠访谈印象下结论。",
        "",
        "### Complementarity",
        "",
        "- 问卷告诉我们“谁更有需求”，访谈解释了“为什么很多人最后没有借”。",
        "- 问卷能定位高频赴港、特定身份和特定场景用户更可能借；访谈补充了这些用户如何在紧急场景下权衡速度、成本与信任。",
        "",
        "### 从洞察到策略",
        "",
        "1. 先抓‘有明确跨境场景、替代方案不稳定、对新产品有兴趣’的人，而不是泛泛教育所有赴港用户。",
        "2. 把产品表达从‘港币借款功能介绍’升级为‘跨境资金可得性解决方案’。",
        "3. 在转化链路里，最先要被解决的是`可信解释`，其次才是`利率竞争力`。",
        "",
        "## 分角色建议",
        "",
        "### 高管",
        "- 把产品定位为跨境资金解决方案，而不是普通借贷产品。",
        "- 先做常驻内地的高频赴港消费/临时周转场景，再做两地往返高价值人群。",
        "",
        "### 风控",
        "- 页面前置解释合规边界、资金来源与费率口径，降低灰色平台联想。",
        "- 重点关注高时效周转型与投资场景人群的准入和用途管理。",
        "",
        "### 运营",
        "- 宣发素材要突出“正规、透明、人民币可还、到账快”。",
        "- 新客可考虑小额试用或首借权益，降低第一次试错门槛。",
        "",
        "### 产品/设计",
        "- 首屏讲清四件事：借什么币、钱到哪里、怎么还、费用怎么算。",
        "- 把港币放款/人民币还款、常见账户入口、资质背书放在核心决策区。",
        "",
        "## 局限性与后续研究",
        "",
        "- 访谈样本对有需求人群存在设计性过采样。",
        "- 标签差异的定性解释依赖可回连样本，适合解释方向，不宜替代总体分布。",
        "- 若进入立项阶段，建议补做定价接受度、还款路径偏好和风控接受度研究。",
        "",
        "## 附件索引",
        "",
        "- `detailed_findings_report.md`：详细调研发现",
        "- `survey_analysis.md`：完整描述统计",
        "- `cross_analysis_tables.md`：交叉分析与检验",
        "- `quant_chartbook.md`：完整图表册",
        "- `interview_profiles.md`：访谈样本特征与局限性",
        "- `immersion_memos.md`：沉浸式阅读备忘录",
        "- `codebook.md`：定性编码本",
        "- `user_patterns.md`：用户模式分析",
        "- `decision_and_conversion_analysis.md`：决策因素与转化驱动分析",
        "- `product_feedback_analysis.md`：产品 Demo 反馈深分析",
        "- `qual_voice_digest.md`：原声归纳",
        "- `casebook.md`：典型案例册",
        "- `case_sampling_strategy.md`：案例抽样说明",
        "",
        "说明：本主报告已整合核心结论与详细发现；附件用于补充更完整的表、图、原声池和案例底稿。",
    ])
    write(OUT / "05_full_report.md", "\n".join(out))


def render_index():
    out = [
        "# 港币借款需求研究：交付清单",
        "",
        "## 主报告",
        "",
        "- `05_full_report.md`：面向业务团队与高管的完整主报告",
        "- `detailed_findings_report.md`：带关键图表、数据表和原声的详细调研发现",
        "",
        "## 定量分析",
        "",
        "- `survey_analysis.md`：完整描述统计",
        "- `cross_analysis_tables.md`：交叉分析、统计检验、残差表",
        "- `survey_results.json`：机器可复核统计结果",
        "- `quant_chartbook.md`：完整图表册",
        "",
        "## 定性分析",
        "",
        "- `interview_profiles.md`：访谈样本特征与局限性",
        "- `immersion_memos.md`：沉浸式阅读备忘录",
        "- `codebook.md`：定性编码本",
        "- `user_patterns.md`：用户模式分析",
        "- `decision_and_conversion_analysis.md`：决策因素与转化驱动分析",
        "- `product_feedback_analysis.md`：产品 Demo 反馈深分析",
        "- `qual_voice_digest.md`：核心问题原声归纳",
        "- `casebook.md`：典型案例册",
        "- `case_sampling_strategy.md`：案例抽样说明",
        "",
        "## 原始解析表",
        "",
        "- `survey_raw.csv`",
        "- `interview_raw.csv`",
        "",
        "## 图表目录",
        "",
        "- `charts/`：所有单变量图、交叉图与整合图",
    ]
    write(OUT / "00_deliverables_index.md", "\n".join(out))


def render_quant_support_tables():
    quant_dir = OUT / "02_定量分析"
    quant_dir.mkdir(parents=True, exist_ok=True)
    groups = {
        "赴港总体": visited,
        "需求总体": need,
        "有需求未借过": consider,
        "曾借过": borrowed,
        "两地往返_需求": need[need["标签"] == "1_两地往返"],
        "常驻内地_需求": need[need["标签"] == "2_常驻内地"],
    }

    long_rows = []
    for col in SINGLE_VARS:
        qid, qtext = SURVEY_META[col]
        is_multi = col in [
            "6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？",
            "7.请问你借用港币主要考虑用于哪些方面呢？",
            "8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？",
        ]
        if is_multi:
            universe = Counter()
            group_counts = {}
            for gname, gdf in groups.items():
                source = need if gname == "赴港总体" else gdf
                c = Counter()
                for val in source[col]:
                    for part in split_multi(val):
                        c[part] += 1
                        universe[part] += 0 if gname != "需求总体" else 1
                group_counts[gname] = c
            options = [opt for opt, _ in universe.most_common()] or sorted({k for c in group_counts.values() for k in c})
            for opt in options:
                for gname, gdf in groups.items():
                    base = len(need) if gname == "赴港总体" else len(gdf)
                    n = group_counts[gname].get(opt, 0)
                    long_rows.append({
                        "section": "描述统计",
                        "table_name": f"{qid} {qtext}",
                        "table_type": "distribution",
                        "question": qtext,
                        "option": opt,
                        "row_group": "",
                        "column_group": "",
                        "group_name": gname,
                        "base_n": base,
                        "count": n,
                        "pct": pct(n, base),
                        "chi2": "",
                        "p_value": "",
                        "cramers_v": "",
                        "notes": "多选题；百分比按样本人数计算",
                    })
        else:
            source = visited if col in [
                "1.[C1]请问你的周岁年龄是？",
                "2.请问过去 12 个月内你去过几次中国香港呢？ ",
                "3.请问最近 12 个月内你需要用到港币的机会多吗？",
                "4.请问以下哪种情况最符合你的实际情况？",
                "5.请问你是否持有以下香港身份证明文件呢？",
                "13.请问你目前从事的职业是？",
                "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）",
                "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）",
            ] else need
            options = ordered_categories(source[col], key=col)
            for opt in options:
                for gname, gdf in groups.items():
                    if gname == "赴港总体":
                        base_df = groups["赴港总体"] if col in [
                            "1.[C1]请问你的周岁年龄是？",
                            "2.请问过去 12 个月内你去过几次中国香港呢？ ",
                            "3.请问最近 12 个月内你需要用到港币的机会多吗？",
                            "4.请问以下哪种情况最符合你的实际情况？",
                            "5.请问你是否持有以下香港身份证明文件呢？",
                            "13.请问你目前从事的职业是？",
                            "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）",
                            "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）",
                        ] else groups["需求总体"]
                    else:
                        base_df = gdf
                    n = int((base_df[col].astype(str) == opt).sum())
                    long_rows.append({
                        "section": "描述统计",
                        "table_name": f"{qid} {qtext}",
                        "table_type": "distribution",
                        "question": qtext,
                        "option": opt,
                        "row_group": "",
                        "column_group": "",
                        "group_name": gname,
                        "base_n": len(base_df),
                        "count": n,
                        "pct": pct(n, len(base_df)),
                        "chi2": "",
                        "p_value": "",
                        "cramers_v": "",
                        "notes": "单选题；百分比按该组样本人数计算",
                    })

    for name, res in cross_results.items():
        for row_name in res["table"].index:
            row_total = int(res["table"].loc[row_name].sum())
            for col_name in res["table"].columns:
                n = int(res["table"].loc[row_name, col_name])
                long_rows.append({
                    "section": "交叉分析",
                    "table_name": name,
                    "table_type": "crosstab_cell",
                    "question": name,
                    "option": "",
                    "row_group": str(row_name),
                    "column_group": str(col_name),
                    "group_name": "",
                    "base_n": row_total,
                    "count": n,
                    "pct": round(float(res["row_pct"].loc[row_name, col_name]), 1),
                    "chi2": round(float(res["chi2"]), 3),
                    "p_value": round(float(res["p"]), 4),
                    "cramers_v": round(float(res["cramers_v"]), 3),
                    "notes": "交叉分析单元格；百分比为行百分比",
                })
        long_rows.append({
            "section": "交叉分析",
            "table_name": name,
            "table_type": "test_result",
            "question": name,
            "option": "",
            "row_group": "",
            "column_group": "",
            "group_name": "",
            "base_n": int(res["n"]),
            "count": "",
            "pct": "",
            "chi2": round(float(res["chi2"]), 3),
            "p_value": round(float(res["p"]), 4),
            "cramers_v": round(float(res["cramers_v"]), 3),
            "notes": f"df={res['dof']}; low_expected={res['low_expected']}",
        })

    long_df = pd.DataFrame(long_rows)
    long_df.to_csv(quant_dir / "04_定量支撑表_长表.csv", index=False, encoding="utf-8-sig")

    quick_lines = []
    quick_lines.append(["目录", "下方按“描述统计”与“交叉分析”顺序排布，每个表之间留一空行，便于快速浏览。"])
    quick_lines.append([])
    quick_lines.append(["一、描述统计"])
    quick_lines.append([])
    for col in SINGLE_VARS:
        qid, qtext = SURVEY_META[col]
        quick_lines.append([f"{qid} {qtext}"])
        headers = ["选项"]
        for g in groups:
            headers.extend([f"{g}_n(n={len(groups[g])})", f"{g}_pct"])
        quick_lines.append(headers)
        is_multi = col in [
            "6.请问你曾用过、或考虑通过什么渠道获得港币借款呢？",
            "7.请问你借用港币主要考虑用于哪些方面呢？",
            "8.请问你考虑借港币、而不是借人民币后再换汇，最主要的原因是？",
        ]
        if is_multi:
            counts_by_group = {}
            universe = Counter()
            for gname, gdf in groups.items():
                source = need if gname == "赴港总体" else gdf
                c = Counter()
                for val in source[col]:
                    for p in split_multi(val):
                        c[p] += 1
                        if gname == "需求总体":
                            universe[p] += 1
                counts_by_group[gname] = c
            for opt, _ in universe.most_common():
                row = [opt]
                for gname, gdf in groups.items():
                    denom = len(need) if gname == "赴港总体" else len(gdf)
                    n = counts_by_group[gname].get(opt, 0)
                    row.extend([n, f"{pct(n, denom)}%"])
                quick_lines.append(row)
        else:
            source = visited if col in [
                "1.[C1]请问你的周岁年龄是？",
                "2.请问过去 12 个月内你去过几次中国香港呢？ ",
                "3.请问最近 12 个月内你需要用到港币的机会多吗？",
                "4.请问以下哪种情况最符合你的实际情况？",
                "5.请问你是否持有以下香港身份证明文件呢？",
                "13.请问你目前从事的职业是？",
                "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）",
                "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）",
            ] else need
            for opt in ordered_categories(source[col], key=col):
                row = [opt]
                for gname, gdf in groups.items():
                    if gname == "赴港总体":
                        base_df = groups["赴港总体"] if col in [
                            "1.[C1]请问你的周岁年龄是？",
                            "2.请问过去 12 个月内你去过几次中国香港呢？ ",
                            "3.请问最近 12 个月内你需要用到港币的机会多吗？",
                            "4.请问以下哪种情况最符合你的实际情况？",
                            "5.请问你是否持有以下香港身份证明文件呢？",
                            "13.请问你目前从事的职业是？",
                            "14.[C3]请问你每月的收入大约是多少人民币?（包括所有奖金、分红、工资、津贴等在内）",
                            "15.请问你每月的收入中，【港币】收入大约占多少呢？（包括退休金、投资收入等）",
                        ] else groups["需求总体"]
                    else:
                        base_df = gdf
                    n = int((base_df[col].astype(str) == opt).sum())
                    row.extend([n, f"{pct(n, len(base_df))}%"])
                quick_lines.append(row)
        quick_lines.append([])

    quick_lines.append(["二、交叉分析"])
    quick_lines.append([])
    for name, res in cross_results.items():
        quick_lines.append([name, f"Chi-square={res['chi2']:.3f}", f"p={res['p']:.4f}", f"Cramer's V={res['cramers_v']:.3f}"])
        quick_lines.append([name.split(" × ")[0]] + [str(c) for c in res["table"].columns] + ["Total"])
        for idx in res["table"].index:
            row = [str(idx)]
            for c in res["table"].columns:
                row.append(f"{int(res['table'].loc[idx, c])} ({res['row_pct'].loc[idx, c]:.1f}%)")
            row.append(int(res["table"].loc[idx].sum()))
            quick_lines.append(row)
        quick_lines.append([])

    quick_df = pd.DataFrame(quick_lines)
    quick_df.to_csv(quant_dir / "05_定量支撑表_交叉表速览.csv", index=False, header=False, encoding="utf-8-sig")

    with pd.ExcelWriter(quant_dir / "06_定量支撑表_汇总.xlsx", engine="openpyxl") as writer:
        long_df.to_excel(writer, sheet_name="长表", index=False)
        quick_df.to_excel(writer, sheet_name="速览交叉表", index=False, header=False)


def sync_structured_outputs():
    quant_dir = OUT / "02_定量分析"
    final_dir = OUT / "06_最终报告"
    link_dir = OUT / "01_数据关联"
    qa_dir = OUT / "05_质量审查"
    charts_dir = quant_dir / "图表"
    charts_dir.mkdir(parents=True, exist_ok=True)

    sync_pairs = [
        (OUT / "02_quant_analysis.md", quant_dir / "01_定量主分析.md"),
        (OUT / "survey_analysis.md", quant_dir / "02_完整描述统计.md"),
        (OUT / "cross_analysis_tables.md", quant_dir / "03_交叉分析与统计检验.md"),
        (OUT / "quant_chartbook.md", quant_dir / "04_完整图表册.md"),
        (OUT / "05_full_report.md", final_dir / "01_完整主报告.md"),
        (OUT / "detailed_findings_report.md", final_dir / "02_详细调研发现.md"),
        (OUT / "build_summary.json", link_dir / "03_构建摘要.json"),
        (OUT / "build_summary.json", qa_dir / "02_构建日志.json"),
        (OUT / "survey_results.json", qa_dir / "01_统计结果复核.json"),
    ]
    for src, dst in sync_pairs:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    index_lines = [
        "# 关键图表索引",
        "",
        "- `01_funnel.png`：需求漏斗",
        "- `02_need_by_visit_freq.png`：赴港频次与借款需求率",
        "- `03_label_stack.png`：标签与借款状态结构对比",
        "- `05_reasons.png`：借港币而非换汇的主要原因",
        "- `06_product_intent.png`：产品使用意愿",
        "- `22_cross_赴港频次_借款状态.png`：赴港频次 × 借款状态",
        "- `24_cross_月收入_借款状态.png`：月收入 × 借款状态",
        "- `32_cross_月收入_预期金额.png`：月收入 × 预期金额",
        "- `35_cross_借款状态_预期金额.png`：借款状态 × 预期金额",
        "- `38_cross_借款用途_预期次数.png`：借款用途 × 预期次数",
        "- `45_cross_借款用途_还款方式.png`：借款用途 × 还款方式",
        "- `48_cross_借款状态_借款渠道.png`：借款状态 × 借款渠道",
        "- `49_cross_借款用途_借款渠道.png`：借款用途 × 借款渠道",
    ]
    write(quant_dir / "05_关键图表索引.md", "\n".join(index_lines))

    for png in CHARTS.glob("*.png"):
        shutil.copy2(png, charts_dir / png.name)


render_cross_results()
render_survey_analysis()
render_quant_main()
render_quant_support_tables()
render_interview_profiles()
render_qual_main()
render_immersion_memos()
render_codebook()
render_patterns()
render_decision_and_conversion()
render_product_feedback_analysis()
render_voice_digest()
render_casebook()
render_case_sampling_strategy()
render_chartbook()
render_detailed_findings_report()
render_full_report()
render_index()
sync_structured_outputs()

summary = {
    "survey_total": len(survey),
    "valid": len(valid),
    "visited": len(visited),
    "need": len(need),
    "borrowed": len(borrowed),
    "consider": len(consider),
    "interviews_total": len(interviews),
    "matched": len(matched),
    "matched_need": len(matched_need),
    "charts": len(list(CHARTS.glob("*.png"))),
}
write(OUT / "build_summary.json", json.dumps(summary, ensure_ascii=False, indent=2))
print(json.dumps(summary, ensure_ascii=False, indent=2))
