#!/usr/bin/env python3
"""对比成稿与例文的句子风格指标（仅供参考，不是评分）。

用法（在 skill 目录执行）：
    python scripts/style_stats.py 成稿/某篇.md

输出：连接词密度、平均句长、短句比例，以及例文的取值范围；
另外列出命中的“精致腔/犹豫腔”词语，便于定位修改。
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_DIR = ROOT / "例文"
# 口吻不同或与另一篇重复的例文，不参与范围计算
EXCLUDE = {"你的月薪达到城市中位数了吗.txt", "你的存款到什么等级了.txt"}

CONNECTIVES = r"并不是|并非|而是|但是|并且|之后|的时候|因此|所以|那会儿|才明白|才知道|其实|后来"
LITERARY = ["窗外", "灯光", "光线", "雨", "烟雾", "沉默", "愣了很久", "像一", "仿佛", "宛如", "褶皱",
            "松弛感", "底层逻辑", "自洽", "内耗", "清醒", "叙事", "被看见", "情绪价值"]
HEDGES = ["可能", "或许", "也许", "某种程度", "一定程度", "当然", "每个人情况不同", "因人而异"]


def clean(text: str) -> str:
    text = text.lstrip("﻿").replace("**", "")
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)
    return text


def sentences(text: str):
    parts = re.split(r"[。？！?!\n]+", text)
    return [p.strip() for p in parts if len(re.sub(r"\s", "", p)) > 0]


def metrics(text: str) -> dict:
    text = clean(text)
    chars = len(re.sub(r"\s", "", text)) or 1
    sents = sentences(text)
    lens = [len(re.sub(r"\s", "", s)) for s in sents]
    short = sum(1 for n in lens if n <= 8)
    return {
        "连接词/千字": round(len(re.findall(CONNECTIVES, text)) / chars * 1000, 1),
        "“并不是/而是”/千字": round(len(re.findall(r"并不是|并非|而是", text)) / chars * 1000, 1),
        "平均句长": round(sum(lens) / len(lens), 1) if lens else 0,
        "短句(≤8字)比例%": round(short / len(lens) * 100, 1) if lens else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="UTF-8 正文文件（.md 或 .txt）")
    args = parser.parse_args()
    draft = Path(args.path).read_text(encoding="utf-8-sig")
    m = metrics(draft)

    ref = [metrics(p.read_text(encoding="utf-8-sig"))
           for p in sorted(EXAMPLE_DIR.glob("*.txt")) if p.name not in EXCLUDE]
    print(f"{'指标':<16}{'本稿':>8}    例文范围")
    for k, v in m.items():
        vals = [r[k] for r in ref]
        lo, hi = min(vals), max(vals)
        flag = "" if lo <= v <= hi else "  <-- 超出范围"
        print(f"{k:<16}{v:>8}    {lo} – {hi}{flag}")

    text = clean(draft)
    lit = [w for w in LITERARY if w in text]
    hedge = [w for w in HEDGES if w in text.replace("不可能", "")]
    if lit:
        print("精致腔/流行词命中：" + "、".join(lit))
    if hedge:
        print("犹豫腔命中：" + "、".join(hedge))
    print("（仅供参考：超出范围时先对照语感样本找原因，不要硬塞词凑指标。）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
