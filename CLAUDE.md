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

- 💰 **SALES** — Closing, sales calls, follow-ups, pitching. This is what grows revenue.
- 🎬 **MARKETING** — Content creation, DMs, posting, audience growth. This fills the pipeline.
- 🏦 **FINANCE** — Money decisions, expenses, hiring/firing, budgets. Keeps the business healthy.
- 📦 **FULFILLMENT** — Delivering for paying members. Skool group calls, office hours, community engagement, member wins. Also: 1-1 high-ticket client calls and deliverables (existing roster only). **For Skool, this IS the retention motion — directly serves the $20K MRR goal.**
- ⚙️ **BUILD** — Internal systems, automations, AI workflows, tooling. For YOUR business, not client deliverables.
- ❌ **TRAP** — If it doesn't fit the five categories above, it's a trap. Period.

## GSD Score

- **GSD Score** is a 1-10 grade, not a formula. Claude scores it based on judgment.
- **What it measures:** Are we actually moving the needle on **$20K Skool MRR**, or spending time on bullshit?
- **How to score:**
  - Did Jason **ship content** (the funnel input)?
  - Did he move a **funnel metric** — new signups, conversion rate, retention, ARPU?
  - Did he **deliver hard** for existing Skool members (retention work)?
  - Did he avoid traps — especially the high-ticket-mentor / low-quality-sales-call pull?
  - Did he hold the line on the low-ticket motion?
- **Scale:** 10 = shipped content, moved a funnel metric, members got real value, zero traps. 1 = traps + busywork + no funnel movement.
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

3. **If the completed task was on `data/priorities.md` (or `data/backlog.md`), remove it entirely.** Don't strikethrough, don't leave it. The daily log already records what got done — keeping it in priorities is just stale to-do clutter. Renumber the remaining rows so the table stays clean.

4. Run the render script:
   ```bash
   python3 scripts/render.py
   ```

That's it. The script handles activity charts, weekly counts, daily log formatting, the "Updated" date, and ordering. **Never hand-edit `dashboard.md` directly — it gets regenerated.**

**This is a 4-step workflow, not 3. If you only did steps 1+2+4 and the task was on the priority list, you didn't finish — go back and do step 3.**

### Other Rules

1. **When Jason dumps tasks for later**: Edit `data/priorities.md` or `data/backlog.md` directly, then run `render.py`. (Removal-on-completion is handled in the workflow above — step 3.)

2. **When Jason says "plan my day"**: Talk through the plan using `data/priorities.md` and `week-plan.md`. Make sure there's at least 1 SALES or MARKETING task on deck.

3. **When Jason says "what did I get done"**: Query `data/tasks.jsonl` for the date(s) in question. Summarize with category breakdown and GSD score. Example: `jq -c 'select(.date=="2026-04-26")' data/tasks.jsonl`

4. **End of day**: Make sure the day has a GSD score in `data/days.jsonl` and run `render.py`.

5. **Weekly review**: Sunday/Monday, update `data/priorities.md` for the new week, run `render.py`, then write a weekly summary to `weekly-reports/`.

6. **Call out TRAP tasks**: If Jason is about to spend time on busywork, say so. Be direct.

7. **Call out fulfillment-heavy days**: If the whole day is fulfillment with no sales or marketing, flag it.

8. **Keep it simple**: Don't over-organize. Don't add metadata nobody reads. Don't create files that won't get used.

## The Mission — $20K Skool MRR

**Mission-critical target: $20,000/month recurring revenue from Creator Accelerator (Skool).**

This replaces the prior "$40K high-ticket month" framing entirely. Jason walked away from high-ticket as the primary growth lever on 2026-05-03. The new motion is sustainable low-ticket scale.

### Current State (as of 2026-05-03)

- **MRR: $7,410** · **173 members**
- **Pricing:** Standard $75/mo or $500/yr · Premium $4,000/yr (group calls + program access) · VIP $8K/yr (off)
- **Engagement: 71% · Retention: 66%**
- **Last 30d:** 1,186 visitors → 18 signups (1.5% conv) → $1,275 new MRR (~$71/signup)
- **Signup channels (last 30d):** YouTube 50% · Direct 22% · Instagram 11% · Skool network 11% · Email 6%

### The Math

- **Gap: $12,590 MRR.** ~168 net new $75/mo subs (or ~315 net new at blended monthly+annual ARPU).
- **At current pace** ($1,275 new MRR/mo, ignoring churn): ~10 months. With realistic churn at 66% retention: longer.
- **To hit $20K within 6 months:** roughly **2x new-MRR pace AND hold/improve retention**.

### The Four Levers (everything important serves one of these)

1. **GROW MRR** — new signups via content (especially YouTube, the proven 50% channel), traffic, paid acquisition
2. **HOLD MRR** — retain existing members via delivery, engagement, community quality (the 66% retention is the leak)
3. **LIFT ARPU** — push Standard → Premium ($4K/yr tier), surgical upsells
4. **COMPOUND THE FUNNEL** — build/improve the systems that do 1-3 (YouTube engine, content pipeline, automations, conversion improvements on the Skool sales page)

### Other Revenue (supplemental, not the focus)

- Poppy affiliate payouts (~$1.5K/mo) — passive
- Brand deals (Higgsfield-style, sporadic) — passive opportunistic
- 6 existing high-ticket clients (Ayden, Gobb, Albert, Saharat, Patrick, Tyler) — finish out engagements; not actively replacing

### Open Questions (need decisions)

- **Blake** — hired as setter/closer for high-ticket. Re-point at Skool / affiliate work, or pause?
- **Inner Circle calls** — keep, modify, retire? They feed Premium tier value; possibly load-bearing.
- **6 high-ticket clients** — finish out and don't replace, or actively transition them into Skool tiers?
- **Wednesday content day** — still sacred? (Yes by default — content is the funnel input.)

## The Anti-Busywork Check

Before starting any task, it must pass at least one of:

1. **Grow MRR** — bring in new Skool signups
2. **Hold MRR** — retain existing members (delivery, engagement, community quality)
3. **Lift ARPU** — push Standard → Premium
4. **Compound the funnel** — build the system that does 1-3
5. Legally/operationally required (taxes, contracts, payouts)

If none of the above → **it's TRAP. Cut it. Don't even put it on the backlog.**

### Common Traps (call these out aggressively)

- **Low-quality sales calls** — the "should have known they'd never buy" pattern. The qualification filter has to be tight. If the call doesn't have a clear path to MRR (Skool signup, Premium upsell, or a real high-ticket fit from existing pipeline), it's TRAP.
- **Mentor-program churn** — joining the next high-ticket guru program. Jason already concluded the space is mostly overcharging. Stop buying programs.
- **High-ticket outreach for new prospects** — that motion is paused. Don't reflexively suggest it.
- **System-tweaking without funnel impact** — organizing files, polishing docs, tooling that doesn't compound.
- **"Research" without execution.**
- **Generic content not aimed at the funnel.**

**The only things that matter right now: content that grows YouTube/IG, conversion improvements on the Skool page, retention/delivery work inside the community, and surgical Premium upsells.**
