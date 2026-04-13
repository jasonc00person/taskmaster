# Taskmaster — CLAUDE.md

## What This Is

Jason's task management system. The goal is **GSD — Get Shit Done** and **make money**. Every task gets measured against one question: *does this move the business forward or improve my life?*

## How It Works

This is a **conversational system**. Jason talks to Claude, Claude updates the files. No manual entry. The workflow:

1. Jason says what he needs to do, what he did, or asks what's on deck
2. Claude updates the relevant Markdown files
3. Files are the source of truth — viewable in VS Code anytime

## Core Files

| File | Purpose |
|------|---------|
| `dashboard.md` | Command center — priorities, activity breakdown, scoreboard, daily log. The main file. |
| `week-plan.md` | The weekly plan — day-by-day schedule with calls, tasks, and themes. |
| `daily-logs/` | Permanent archive. One file per day: `YYYY-MM-DD.md`. The long-term record. |
| `weekly-reports/` | Weekly summaries. One file per week: `YYYY-WXX.md`. |

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

1. **When Jason dumps tasks**: Add to `dashboard.md` priorities or backlog. Tag with the right category. **When a task is completed, remove it from the priority list entirely — don't strikethrough it.** The daily log is the record of what got done; the prio list should only show what's still open.
2. **When Jason says "plan my day"**: Talk through the plan using `dashboard.md` priorities and `week-plan.md`. Make sure there's at least 1 SALES or MARKETING task on deck.
3. **When Jason completes a task OR logs any activity**: Full dashboard sync. Every time. No exceptions. Hit ALL of these:
   - [ ] Add/update the entry in the daily log
   - [ ] Recount and update the activity chart numbers for the current week
   - [ ] Check if any top priority items should be updated/removed
   - [ ] Update the "Updated" date at the top
   - **If you only update the log without touching the chart and prios, the dashboard is broken. Do not do partial updates.**
4. **When Jason says "what did I get done"**: Summarize from `dashboard.md` daily log, show the category breakdown, give the daily score.
5. **End of day**: Make sure the day is logged in `dashboard.md` daily log with a GSD score. Archive to `daily-logs/YYYY-MM-DD.md`.
6. **Weekly review**: Every Sunday/Monday, update `dashboard.md` with the new week's priorities, scores, and pipeline. Write weekly summary to `weekly-reports/`.
7. **Call out TRAP tasks**: If Jason is about to spend time on something that looks like busywork, say so. Be direct.
8. **Call out fulfillment-heavy days**: If the whole day is fulfillment with no sales or marketing, flag it. Maintenance isn't growth.
9. **Keep it simple**: Don't over-organize. Don't add metadata nobody reads. Don't create files that won't get used.

## April 2026 — The $40K Month

**Target: $40,000 cash collected in April.**

Revenue baseline (auto-pilot):
- $8,900 Skool low-ticket MRR
- $1,500 Poppy affiliate payouts
- $2,350 payment plans (Saharat + Moises — Moises at risk, silent first week)
- $2,000 Patrick collection (Apr 8-9)
- $2,000 Higgsfield brand deal (overdue, filming Apr 5)
- **Total baseline: ~$16,750**

**Gap: ~$23,250 in new high-ticket sales needed.**
- At $4K PIF: 6 closes. But not everyone PIFs.
- Realistic: **8-10 new closes this month** (~2-3/week).
- Requires **5-6 sales calls/week** at 40-50% close rate.
- Content + outreach are the pipeline. No content = no calls = no $40K.

**Current clients (7):** Ayden, Gobb, Albert, Saharat, Patrick, Moises, Tyler
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
