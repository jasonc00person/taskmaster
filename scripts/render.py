#!/usr/bin/env python3
"""Render dashboard.md from data/ (tasks.jsonl, days.jsonl, priorities.md, backlog.md).

This is the SOURCE OF TRUTH render. Run after every task append.
"""
import json
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
DASHBOARD = ROOT / "dashboard.md"

CATEGORY_EMOJI = {
    "FULFILLMENT": "📦",
    "MARKETING": "🎬",
    "SALES": "💰",
    "FINANCE": "🏦",
    "BUILD": "⚙️",
    "TRAP": "❌",
    "PERSONAL": "👤",
}
CATEGORY_LABEL = {
    "FULFILLMENT": "Fulfillment",
    "MARKETING": "Marketing",
    "SALES": "Sales",
    "FINANCE": "Finance",
    "BUILD": "Build",
    "TRAP": "Trap",
}
CATEGORY_COLOR = {
    "FULFILLMENT": "#FB923C",
    "MARKETING": "#A78BFA",
    "SALES": "#4ADE80",
    "FINANCE": "#FBBF24",
    "BUILD": "#60A5FA",
    "TRAP": "#EF4444",
}
CHART_CATEGORIES = ["FULFILLMENT", "MARKETING", "SALES", "FINANCE", "BUILD", "TRAP"]
BAR_WIDTH = 21
PRETRACK_BEFORE = "2026-03-23"
PRIOR_WEEKS_SHOWN = 3


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def fmt_md(d: date) -> str:
    return f"{d.strftime('%b')} {d.day}"


def render_bar(category: str, count: int) -> str:
    blocks = min(count, BAR_WIDTH)
    dots = BAR_WIDTH - blocks
    block_str = "█" * blocks
    dot_str = "░" * dots
    label = CATEGORY_LABEL[category]
    if blocks > 0:
        color = CATEGORY_COLOR[category]
        bar = f'<span style="color:{color}">{block_str}</span>{dot_str}'
    else:
        bar = dot_str
    return f"  {label:<11}  {bar}  {count:2d}"


def render_week_block(tasks_in_week):
    counts = Counter()
    for t in tasks_in_week:
        if t["category"] in CHART_CATEGORIES:
            counts[t["category"]] += 1
    cats_sorted = sorted(
        CHART_CATEGORIES,
        key=lambda c: (-counts[c], CHART_CATEGORIES.index(c)),
    )
    lines = ["<pre>"]
    for c in cats_sorted:
        lines.append(render_bar(c, counts[c]))
    lines.append("</pre>")
    return "\n".join(lines)


def render_activity(tasks, today: date) -> str:
    by_week = defaultdict(list)
    for t in tasks:
        td = date.fromisoformat(t["date"])
        by_week[week_start(td)].append(t)

    cw_start = week_start(today)
    cw_end = cw_start + timedelta(days=6)

    out = [f"## **⚡ Activity ({fmt_md(cw_start)} – {fmt_md(cw_end)})**", ""]
    out.append(render_week_block(by_week.get(cw_start, [])))
    out.append("")

    for i in range(1, PRIOR_WEEKS_SHOWN + 1):
        ws = cw_start - timedelta(weeks=i)
        we = ws + timedelta(days=6)
        out.append(f"<details><summary>Prior week ({fmt_md(ws)} – {fmt_md(we)})</summary>")
        out.append("")
        out.append(render_week_block(by_week.get(ws, [])))
        out.append("")
        out.append("</details>")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def render_task(task: dict) -> str:
    emoji = CATEGORY_EMOJI[task["category"]]
    title = task["title"]
    if task.get("emphasis"):
        title = f"**{title}**"
    line = f"- {emoji} {title}"
    if task.get("note"):
        line += f" ({task['note']})"
    return line


def render_day_header(date_str: str, day_record: dict) -> str:
    d = date.fromisoformat(date_str)
    dow = day_record.get("dow") or d.strftime("%a")
    header = f"{d.strftime('%b')} {d.day} ({dow})"
    suffixes = []
    if day_record.get("day_type") == "REST":
        suffixes.append("REST DAY")
    if "gsd" in day_record:
        suffixes.append(f"GSD: {day_record['gsd']}/10")
    elif "gsd_pct" in day_record:
        suffixes.append(f"GSD: {day_record['gsd_pct']}%")
    if suffixes:
        header += " — " + " — ".join(suffixes)
    return f"### {header}"


def render_log(tasks, days) -> str:
    by_date = defaultdict(list)
    for t in tasks:
        by_date[t["date"]].append(t)
    days_by_date = {d["date"]: d for d in days}

    all_dates = sorted(set(list(by_date.keys()) + list(days_by_date.keys())), reverse=True)
    regular = [d for d in all_dates if d >= PRETRACK_BEFORE]
    pretrack = [d for d in all_dates if d < PRETRACK_BEFORE]

    out = ["## **📋 Daily Log**", ""]

    def render_date(d):
        out.append(render_day_header(d, days_by_date.get(d, {})))
        for t in by_date.get(d, []):
            out.append(render_task(t))
        out.append("")

    for d in regular:
        render_date(d)

    if pretrack:
        out.append("---")
        out.append("")
        out.append("**— Pre-tracking (calls only) —**")
        out.append("")
        for d in pretrack:
            render_date(d)

    return "\n".join(out).rstrip() + "\n"


def render(today: date | None = None):
    tasks = load_jsonl(DATA / "tasks.jsonl")
    days = load_jsonl(DATA / "days.jsonl")
    priorities_path = DATA / "priorities.md"
    backlog_path = DATA / "backlog.md"
    priorities = priorities_path.read_text().strip() if priorities_path.exists() else ""
    backlog = backlog_path.read_text().strip() if backlog_path.exists() else ""

    if today is None:
        today = date.today()

    parts = [
        "# **TASKMASTER** ☑️",
        "",
        f"_Updated: {today.strftime('%A')}, {today.strftime('%B')} {today.day}, {today.year}_",
        "",
        "---",
        "",
        priorities,
        "",
        "---",
        "",
        backlog,
        "",
        "---",
        "",
        render_activity(tasks, today),
        "---",
        "",
        render_log(tasks, days),
    ]
    DASHBOARD.write_text("\n".join(parts))
    print(f"Rendered {DASHBOARD} ({len(tasks)} tasks, {len(days)} days)")


if __name__ == "__main__":
    # Optional: pass YYYY-MM-DD as argv[1] to render for a fixed "today"
    today = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    render(today)
