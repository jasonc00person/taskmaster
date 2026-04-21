from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Static
from rich.text import Text
from rich.align import Align

BAR_WIDTH = 21

CATEGORY_COLORS = {
    "Fulfillment": "#FB923C",
    "Marketing":   "#A78BFA",
    "Sales":       "#4ADE80",
    "Build":       "#60A5FA",
    "Finance":     "#FBBF24",
    "Trap":        "#EF4444",
}

PRIORITIES = [
    {
        "n": "01",
        "task": "Hire Blake — Setter + Closer + Part-time CSM",
        "cat": "🏦 FINANCE",
        "deadline": "🔴 ASAP",
        "note": "$1K base + 10% commissions. Break the $20K/mo solopreneur ceiling.",
    },
    {
        "n": "02",
        "task": "Alex Eubank — Build Fresh Creatives Workstation",
        "cat": "📦 FULFILLMENT",
        "deadline": "🟡 Apr 4",
        "note": "AI creative generation for Fresh supplement brand launch.",
    },
]

ACTIVITY_WEEK = "Apr 20 – Apr 26"
ACTIVITY = [
    ("Fulfillment", 3),
    ("Marketing",   0),
    ("Sales",       0),
    ("Build",       1),
    ("Finance",     1),
    ("Trap",        0),
]

LOG = [
    ("Apr 20 (Mon)", None, [
        ("⚙️",  "Transitioned all 1-1 clients to group call model"),
        ("📦", "Group call"),
        ("🏦", "Sold the car (finally done)"),
        ("📦", "Ayden 1-1"),
        ("📦", "Client looms + weekly content ideas — 4 clients in 2 hrs"),
    ]),
    ("Apr 19 (Sun)", "1/10", [("👤", "Off day, nothing logged")]),
    ("Apr 18 (Sat)", "4/10", [("📦", "Oliver app — full day of build work")]),
    ("Apr 17 (Fri)", "6/10", [
        ("📦", "Oliver — Student Dashboard SHIPPED"),
        ("🎬", "Edited + posted IG reel"),
        ("❌", "Sales call no-show"),
        ("📦", "Patrick 1-1"),
        ("💵", "Sales call — just wanted to chop it up (no close)"),
    ]),
    ("Apr 16 (Thu)", "7/10", [
        ("📦", "Tyler 1-1"),
        ("📦", "Group call"),
        ("🎬", "Filmed 2 IG reels"),
        ("💵", "DM outreach/setting — booked 2 sales calls"),
    ]),
    ("Apr 15 (Wed)", "6/10", [("🎬", "Filmed + posted IG reel")]),
    ("Apr 14 (Tue)", None, [
        ("🏦", "Filed 2025 taxes"),
        ("📦", "Oliver 1-1"),
        ("💵", "DM outreach blitz (28 leads worked)"),
        ("🎬", "Reposted Poppy viral video"),
        ("⚙️",  "Built Content OS Claude system"),
    ]),
    ("Apr 13 (Mon)", None, [
        ("💵", "Higgsfield — $2K collected"),
        ("📦", "Gobb 1-1 / Moises 1-1 / Albert 1-1 / Ayden 1-1 / Saharat 1-1"),
        ("📦", "Oliver — Built MVP automation"),
    ]),
]

MONTH_TARGET = 40000
MONTH_COLLECTED = 15400


def make_bar(count: int, color: str) -> Text:
    text = Text()
    filled = min(count, BAR_WIDTH)
    text.append("█" * filled, style=color)
    text.append("░" * (BAR_WIDTH - filled), style="#333333")
    return text


class BannerPanel(Static):
    def render(self):
        pct = int((MONTH_COLLECTED / MONTH_TARGET) * 100)
        bar_len = 40
        filled = int((MONTH_COLLECTED / MONTH_TARGET) * bar_len)

        t = Text()
        t.append("TASKMASTER", style="bold #FB923C")
        t.append("  ·  ", style="#888888")
        t.append("Tuesday, April 21, 2026", style="white")
        t.append("  ·  ", style="#888888")
        t.append("GSD: ON\n\n", style="bold #4ADE80")

        t.append("APRIL $40K TARGET   ", style="bold white")
        t.append("█" * filled, style="#4ADE80")
        t.append("░" * (bar_len - filled), style="#333333")
        t.append(f"  {pct}%\n", style="bold #4ADE80")

        t.append(f"${MONTH_COLLECTED:,} collected", style="#4ADE80")
        t.append(" / ", style="#888888")
        t.append(f"${MONTH_TARGET:,} goal", style="white")
        t.append("   Gap: ", style="#888888")
        t.append(f"${MONTH_TARGET - MONTH_COLLECTED:,}", style="bold #EF4444")
        return t


class PrioritiesPanel(Static):
    def render(self):
        t = Text()
        t.append("🔥 TOP PRIORITIES\n\n", style="bold #FBBF24")
        for p in PRIORITIES:
            t.append(f"  {p['n']}  ", style="bold #888888")
            t.append(f"{p['task']}\n", style="bold white")
            t.append(f"       {p['cat']}", style="#60A5FA")
            t.append("   ", style="white")
            t.append(f"{p['deadline']}\n", style="white")
            t.append(f"       {p['note']}\n\n", style="italic #888888")
        return t


class ActivityPanel(Static):
    def render(self):
        t = Text()
        t.append(f"⚡ ACTIVITY ", style="bold #FBBF24")
        t.append(f"({ACTIVITY_WEEK})\n\n", style="#888888")
        total = 0
        for name, count in ACTIVITY:
            color = CATEGORY_COLORS[name]
            t.append(f"  {name:<12}  ", style="white")
            t.append(make_bar(count, color))
            t.append(f"  {count:>2}\n", style="bold white")
            total += count
        t.append("\n  ", style="")
        t.append(f"Total this week: ", style="#888888")
        t.append(f"{total}", style="bold #FBBF24")
        t.append(f"  ·  ", style="#888888")
        growth = sum(c for n, c in ACTIVITY if n in ("Sales", "Marketing"))
        t.append(f"Growth: ", style="#888888")
        t.append(f"{growth}", style="bold #4ADE80" if growth > 0 else "bold #EF4444")
        return t


class LogPanel(VerticalScroll):
    def compose(self) -> ComposeResult:
        header = Text()
        header.append("📋 DAILY LOG\n", style="bold #FBBF24")
        yield Static(header)
        for date, gsd, entries in LOG:
            t = Text()
            t.append(f"\n  {date}", style="bold #60A5FA")
            if gsd:
                t.append(f"   GSD: ", style="#888888")
                score = int(gsd.split("/")[0])
                color = "#4ADE80" if score >= 7 else "#FBBF24" if score >= 4 else "#EF4444"
                t.append(gsd, style=f"bold {color}")
            t.append("\n")
            for emoji, text in entries:
                t.append(f"    {emoji}  ", style="")
                t.append(f"{text}\n", style="white")
            yield Static(t)


class DashboardApp(App):
    CSS = """
    Screen {
        background: #0a0a0a;
    }
    #banner {
        height: 7;
        border: round #FBBF24;
        padding: 0 2;
        background: #111111;
    }
    #middle {
        height: 18;
    }
    #priorities {
        width: 55%;
        border: round #FB923C;
        padding: 1 2;
        background: #111111;
    }
    #activity {
        width: 45%;
        border: round #60A5FA;
        padding: 1 2;
        background: #111111;
        margin-left: 1;
    }
    #log {
        border: round #A78BFA;
        padding: 1 2;
        background: #111111;
        margin-top: 1;
    }
    Footer {
        background: #FB923C;
        color: #0a0a0a;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("n", "noop", "New Task"),
        ("l", "noop", "Log Activity"),
        ("p", "noop", "Plan Day"),
    ]

    TITLE = "TASKMASTER"
    SUB_TITLE = "GSD — Get Shit Done"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield BannerPanel(id="banner")
        with Horizontal(id="middle"):
            yield PrioritiesPanel(id="priorities")
            yield ActivityPanel(id="activity")
        yield LogPanel(id="log")
        yield Footer()

    def action_refresh(self) -> None:
        self.refresh()

    def action_noop(self) -> None:
        self.bell()


if __name__ == "__main__":
    DashboardApp().run()
