# How to Build a TUI (Retro Terminal Dashboard)

Quick reference for making terminal dashboards like the Taskmaster TUI. Framework of choice: **Textual** (Python).

---

## Why Textual

- Reactive — data updates live (perfect for bots, dashboards, monitors)
- CSS-style theming — colors, borders, layouts all in declarative CSS
- Claude writes it fluently, fast to iterate
- Hot-reload with `textual run --dev <file>.py`
- Built on `rich` for beautiful output

**Alternatives:** Bubble Tea (Go, most authentic retro vibe), Ink (Node, React-style), Ratatui (Rust).

---

## Setup (one-time per project)

```bash
mkdir tui && cd tui
python3 -m venv .venv
.venv/bin/pip install textual rich
```

---

## Minimum viable app

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class MyApp(App):
    CSS = """
    Screen { background: #0a0a0a; }
    #box {
        border: round #FB923C;
        padding: 1 2;
        background: #111111;
    }
    """
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("hello world", id="box")
        yield Footer()

if __name__ == "__main__":
    MyApp().run()
```

Run: `.venv/bin/python app.py`

---

## Core building blocks

| Thing | What it does |
|-------|--------------|
| `App` | The whole application |
| `compose()` | Returns the widgets that go on screen |
| `Static` | A renderable text widget (most common) |
| `Header` / `Footer` | Top title bar / bottom keybindings bar |
| `Horizontal` / `Vertical` | Lay out children side-by-side or stacked |
| `VerticalScroll` | Container whose contents are scrollable |
| `BINDINGS` | List of `(key, action_name, label)` tuples |
| CSS | Styling — border, padding, colors, width, height |

---

## Coloring text (use `rich.text.Text`)

```python
from rich.text import Text

t = Text()
t.append("bold orange", style="bold #FB923C")
t.append(" — ", style="#888888")
t.append("green", style="#4ADE80")
```

**⚠️ Gotcha:** Rich requires **full 6-char hex** (`#FB923C`), NOT 3-char shorthand (`#FBC`). Short hex crashes with `MissingStyle` error.

---

## Layout tips

- Use CSS `border: round <color>;` instead of manually drawing `╭─╮` ASCII boxes. Hand-drawn boxes break the moment content length changes.
- Widths as percentages (`width: 55%;`) auto-resize with terminal.
- Fixed heights (`height: 18;`) = row count, not pixels.
- For fluid resize, avoid hardcoding bar widths — compute from `self.size.width`.

---

## Launching a TUI from outside the terminal (Mac)

TUIs need a TTY, so you can't just run them from a background script. Spawn a new Terminal window:

```bash
osascript -e 'tell application "Terminal" to do script "/absolute/path/to/run.sh"' \
          -e 'tell application "Terminal" to activate'
```

**Always use absolute paths in `run.sh`** — the new Terminal opens in `$HOME`, not wherever the script lives:

```bash
#!/bin/bash
cd /absolute/path/to/tui
./.venv/bin/python app.py
```

Don't try to cram the `cd` into the osascript arg — quoting is a nightmare. Script file it.

---

## Useful patterns

**Live updating data** (e.g. trading bot prices):
```python
from textual.reactive import reactive

class PriceWidget(Static):
    price = reactive(0.0)
    def watch_price(self, value): self.update(f"${value:,.2f}")

# Elsewhere: self.query_one(PriceWidget).price = new_price
```

**Timer updates** (refresh every N seconds):
```python
def on_mount(self):
    self.set_interval(5, self.refresh_data)

def refresh_data(self):
    # fetch new data, update widgets
    pass
```

**Colored bar (the Taskmaster way):**
```python
def make_bar(count: int, total: int, color: str) -> Text:
    t = Text()
    t.append("█" * count, style=color)
    t.append("░" * (total - count), style="#333333")
    return t
```

---

## Template to steal

The Taskmaster dashboard at `/Users/jasoncooperson/Projects/taskmaster/tui/dashboard.py` is a working reference with:
- Bordered banner (top)
- Horizontal split for two side panels
- Scrollable log section
- Color-coded GSD scores
- Keybindings in footer

Clone it, rename, swap the data — that's 80% of any dashboard.

---

## Color palette (Taskmaster)

| Category | Hex | Vibe |
|----------|-----|------|
| Orange | `#FB923C` | Fulfillment / highlight |
| Purple | `#A78BFA` | Marketing / accent |
| Green | `#4ADE80` | Sales / success |
| Blue | `#60A5FA` | Build / info |
| Gold | `#FBBF24` | Finance / warning |
| Red | `#EF4444` | Trap / error |
| Dark bg | `#111111` | Panel bg |
| Darker bg | `#0a0a0a` | Screen bg |
| Dim text | `#888888` | Secondary |
| Empty bar | `#333333` | Dots |

---

## Docs

- Textual: https://textual.textualize.io
- Rich: https://rich.readthedocs.io
