#!/usr/bin/env python3
"""One-time backfill: parse dashboard.md into tasks.jsonl + days.jsonl + priorities.md + backlog.md."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DASHBOARD = ROOT / "dashboard.md.bak"
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

EMOJI_TO_CATEGORY = {
    "📦": "FULFILLMENT",
    "🎬": "MARKETING",
    "💵": "SALES",
    "🏦": "FINANCE",
    "⚙️": "BUILD",
    "❌": "TRAP",
    "👤": "PERSONAL",
}

MONTH_TO_NUM = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

YEAR = 2026

def main():
    text = DASHBOARD.read_text()

    # Extract sections by header markers
    priorities = extract_section(text, "## **🔥 Top Priorities**", "## **📥 Backlog**")
    backlog = extract_section(text, "## **📥 Backlog**", "## **⚡ Activity")
    log_section = text[text.find("## **📋 Daily Log**"):]

    (DATA / "priorities.md").write_text(priorities.strip() + "\n")
    (DATA / "backlog.md").write_text(backlog.strip() + "\n")

    tasks, days = parse_log(log_section)
    tasks.sort(key=lambda t: t["date"])
    days.sort(key=lambda d: d["date"])

    (DATA / "tasks.jsonl").write_text(
        "\n".join(json.dumps(t, ensure_ascii=False) for t in tasks) + "\n"
    )
    (DATA / "days.jsonl").write_text(
        "\n".join(json.dumps(d, ensure_ascii=False) for d in days) + "\n"
    )
    print(f"Wrote {len(tasks)} tasks and {len(days)} days")
    print(f"priorities.md: {len(priorities)} chars")
    print(f"backlog.md: {len(backlog)} chars")


def extract_section(text, start_marker, end_marker):
    s = text.find(start_marker)
    e = text.find(end_marker, s)
    if s == -1 or e == -1:
        return ""
    section = text[s:e]
    # Strip trailing horizontal rule + whitespace
    section = re.sub(r"\n---\s*$", "", section)
    return section


def parse_log(log_text):
    day_re = re.compile(r"^### (\w+) (\d+) \((\w+)\)(?: — (.+))?$", re.MULTILINE)
    tasks = []
    days = []
    matches = list(day_re.finditer(log_text))
    for i, m in enumerate(matches):
        month_str, day_str, dow, suffix = m.groups()
        month = MONTH_TO_NUM.get(month_str)
        if not month:
            continue
        date_iso = f"{YEAR:04d}-{month:02d}-{int(day_str):02d}"

        gsd = None
        gsd_pct = None
        day_type = None
        if suffix:
            m_score = re.search(r"GSD:\s*(\d+)/10", suffix)
            m_pct = re.search(r"GSD:\s*(\d+)%", suffix)
            if m_score:
                gsd = int(m_score.group(1))
            elif m_pct:
                gsd_pct = int(m_pct.group(1))
            if "REST DAY" in suffix.upper():
                day_type = "REST"

        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(log_text)
        body = log_text[body_start:body_end]

        for line in body.splitlines():
            line = line.strip()
            if not line.startswith("- "):
                continue
            content = line[2:].strip()
            category = None
            for emoji, cat in EMOJI_TO_CATEGORY.items():
                if content.startswith(emoji):
                    category = cat
                    content = content[len(emoji):].strip()
                    break
            if not category:
                continue

            note = None
            note_match = re.search(r"\s*\(([^)]+)\)\s*$", content)
            if note_match:
                note = note_match.group(1)
                content = content[:note_match.start()].strip()

            emphasis = "**" in content
            title = re.sub(r"\*\*", "", content).strip()

            task = {"date": date_iso, "category": category, "title": title}
            if note:
                task["note"] = note
            if emphasis:
                task["emphasis"] = True
            tasks.append(task)

        day_record = {"date": date_iso, "dow": dow}
        if gsd is not None:
            day_record["gsd"] = gsd
        if gsd_pct is not None:
            day_record["gsd_pct"] = gsd_pct
        if day_type:
            day_record["day_type"] = day_type
        days.append(day_record)

    return tasks, days


if __name__ == "__main__":
    main()
