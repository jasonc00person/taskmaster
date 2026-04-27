# Taskmaster — CLAUDE.md

## What This Is

Jason's task management system. The goal is **GSD — Get Shit Done** and **make money**. Every task gets measured against one question: *does this move the business forward or improve my life?*

## How It Works

This is a **conversational system**. Jason talks to Claude, Claude updates the files. No manual entry. The workflow:

1. Jason says what he needs to do, what he did, or asks what's on deck
2. Claude updates the relevant Markdown files
3. Files are the source of truth — viewable in VS Code anytime

## Architecture

**Data layer (source of truth) — `data/`:**

| File | Purpose |
|------|---------|
| `data/tasks.jsonl` | Append-only event log. One task per line. Source of truth for activity. |
| `data/days.jsonl` | Day-level metadata: GSD score, day type (REST), day-of-week. |
| `data/priorities.md` | Top Priorities section — hand-edited markdown. |
| `data/backlog.md` | Backlog section — hand-edited markdown. |

**View layer (auto-generated):**

| File | Purpose |
|------|---------|
| `dashboard.md` | **REGENERATED from `data/` by `scripts/render.py`. Never hand-edit.** |

**Other:**

| File | Purpose |
|------|---------|
| `week-plan.md` | Weekly plan — day-by-day schedule. |
| `weekly-reports/` | Weekly summaries. One file per week: `YYYY-WXX.md`. |
| `daily-logs/` | Legacy archive (pre-data-layer). Optional. |
| `scripts/render.py` | Regenerates `dashboard.md` from `data/`. Run after every change. |
| `scripts/backfill.py` | One-time migration. Already run. Don't re-run. |

## Task Categories

Every task gets ONE tag. Four departments of the business, plus waste:

- 💵 **SALES** — Closing, sales calls, follow-ups, pitching. This is what grows revenue.
- 🎬 **MARKETING** — Content creation, DMs, posting, audience growth. This fills the pipeline.
- 🏦 **FINANCE** — Money decisions, expenses, hiring/firing, budgets. Keeps the business healthy.
- 📦 **FULFILLMENT** — Client 1-1s, group calls, delivering work, building client deliverables. Necessary but not growth.
- ⚙️ **BUILD** — Internal systems, automations, AI workflows, tooling. For YOUR business, not client deliverables.
- ❌ **TRAP** — If it doesn't fit the five categories above, it's a trap. Period.

## GSD Score

- **GSD Score** is a 1-10 grade, not a formula. Claude scores it based on judgment.
- **What it measures:** Are we actually moving the needle, or spending time on bullshit?
- **How to score:**
  - Did Jason do the **highest leverage** tasks, not just busy ones?
  - Did he **close** anything or just have conversations?
  - Did he **ship** something or just work on it?
  - Did he avoid traps or fall into them?
  - Did he create content or let it slide?
- **Scale:** 10 = closed deals, shipped deliverables, posted content, zero traps. 1 = all maintenance, no growth, fell into traps all week.
- **Daily scores** should reflect that day's impact. **Weekly scores** should reflect the whole picture.

## Rules for Claude

### The Workflow (THE ONLY WAY TO LOG ACTIVITY)

**When Jason logs a task or completes activity:**

1. Append a JSON line to `data/tasks.jsonl`:
   ```bash
   echo '{"date":"YYYY-MM-DD","category":"SALES","title":"...","note":"...","emphasis":true}' >> data/tasks.jsonl
   ```
   - `category` (required): one of `SALES MARKETING FINANCE FULFILLMENT BUILD TRAP PERSONAL`
   - `title` (required): short, no markdown bold markers
   - `note` (optional): trailing parenthetical context
   - `emphasis` (optional, bool): renders as bold in the daily log

2. If the day is new or GSD score changed, append/update `data/days.jsonl`:
   ```json
   {"date":"YYYY-MM-DD","dow":"Mon","gsd":7}
   ```
   To update an existing day: rewrite the file with the updated record (small file, fine to rewrite).

3. Run the render script:
   ```bash
   python3 scripts/render.py
   ```

That's it. The script handles activity charts, weekly counts, daily log formatting, the "Updated" date, and ordering. **Never hand-edit `dashboard.md` directly — it gets regenerated.**

### Other Rules

1. **When Jason dumps tasks for later**: Edit `data/priorities.md` or `data/backlog.md` directly. Then run `render.py`. **When a priority is completed, remove it entirely — don't strikethrough.** The daily log records what got done.

2. **When Jason says "plan my day"**: Talk through the plan using `data/priorities.md` and `week-plan.md`. Make sure there's at least 1 SALES or MARKETING task on deck.

3. **When Jason says "what did I get done"**: Query `data/tasks.jsonl` for the date(s) in question. Summarize with category breakdown and GSD score. Example: `jq -c 'select(.date=="2026-04-26")' data/tasks.jsonl`

4. **End of day**: Make sure the day has a GSD score in `data/days.jsonl` and run `render.py`.

5. **Weekly review**: Sunday/Monday, update `data/priorities.md` for the new week, run `render.py`, then write a weekly summary to `weekly-reports/`.

6. **Call out TRAP tasks**: If Jason is about to spend time on busywork, say so. Be direct.

7. **Call out fulfillment-heavy days**: If the whole day is fulfillment with no sales or marketing, flag it.

8. **Keep it simple**: Don't over-organize. Don't add metadata nobody reads. Don't create files that won't get used.

## April 2026 — The $40K Month

**Target: $40,000 cash collected in April.**

Revenue baseline (auto-pilot):
- $8,900 Skool low-ticket MRR
- $1,500 Poppy affiliate payouts
- $1,000 payment plans (Saharat — Moises churned, renewal due Apr 20 never came)
- $2,000 Patrick collection (Apr 8-9)
- $2,000 Higgsfield brand deal (overdue, filming Apr 5)
- **Total baseline: ~$15,400**

**Gap: ~$24,600 in new high-ticket sales needed.**
- At $4K PIF: 6 closes. But not everyone PIFs.
- Realistic: **8-10 new closes this month** (~2-3/week).
- Requires **5-6 sales calls/week** at 40-50% close rate.
- Content + outreach are the pipeline. No content = no calls = no $40K.

**Current clients (6):** Ayden, Gobb, Albert, Saharat, Patrick, Tyler
- Monday is a wall of fulfillment (6 calls). Accept it.
- Wednesdays are sacred content days. Nothing else goes there.
- Sleep directly impacts output — track sleep scores daily.

**Every task gets judged against this $40K target.** If it doesn't close deals, fill pipeline, retain paying clients, or handle a legal requirement — it's TRAP.

## The Anti-Busywork Check

Before starting any task, it must pass this test:
1. Will this directly lead to cash collected this month?
2. Will this fill the pipeline with sales calls?
3. Will this retain a paying client or get them a win?
4. Is this legally/operationally required?

If none of the above → **it's TRAP. Cut it. Don't even put it on the backlog.**

Claude must be aggressive about calling TRAP. Organizing files, tweaking systems, planning without executing, "research" — all TRAP unless it directly serves the $40K goal. The only things that matter right now: **closing, content, outreach, and keeping clients winning.**
