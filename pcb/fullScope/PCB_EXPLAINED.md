# pillScopePlus PCB — Everything Explained (Beginner's Guide)

This document explains, in plain language, everything that happened to turn your
oscilloscope schematic into a finished, manufacturable circuit board — starting
from the moment you were hand-drawing red traces, all the way to the Gerber files
ready for the factory.

Read it top to bottom. Each section builds on the last. If anything is unclear,
ask and we'll expand it.

---

## 0. The big picture: what is a PCB and what were we doing?

A **PCB (Printed Circuit Board)** is the green (or any color) board inside every
electronic device. Instead of connecting parts with loose wires, a PCB has thin
lines of copper baked onto it that carry electricity between the components.

Designing one has a fixed workflow. We had already done the first parts before
today:

1. **Schematic** — a diagram of *what connects to what* (done earlier).
2. **Footprints** — telling the software the real physical size/shape of each part (done earlier).
3. **Placement** — arranging the parts physically on the board ← *we redid this today*.
4. **Routing** — drawing the copper lines that connect the parts ← *the big job today*.
5. **DRC** — an automatic check that the board has no mistakes ← *today*.
6. **Gerbers** — the final files you send to the factory ← *today*.

You were stuck partway through step 4 (routing). Today we finished steps 3–6.

---

## 1. The vocabulary you asked about

Before the story, here are the words. Keep coming back to this section.

### Layers: F.Cu, B.Cu, Edge.Cuts

A PCB is like a sandwich with multiple layers. Yours is a **2-layer board** — it
has copper on the **top** and on the **bottom**. The software draws each layer in
a different color:

| Name | Means | Color on screen | What it is |
|---|---|---|---|
| **F.Cu** | **F**ront **Cu** (copper) | **Red** | The copper wiring on the **top** of the board |
| **B.Cu** | **B**ack **Cu** (copper) | **Blue** | The copper wiring on the **bottom** of the board |
| **Edge.Cuts** | Edge / cuts | **Yellow** | The *outline* — where the factory physically cuts the board out |

> **"Cu"** is the chemical symbol for copper. That's why copper layers end in `.Cu`.

So when you asked **"why are some wires blue?"** — those blue lines are traces on
the **bottom** copper layer (B.Cu). The red ones are on the **top** (F.Cu). Having
two layers means wires can cross each other without touching: one goes over the
top, the other underneath, like a road bridge over another road.

### Trace (a.k.a. track)

A **trace** is one line of copper that carries electricity from one point to
another. It replaces a wire. "Routing" = drawing all the traces.

### Pad

A **pad** is the little metal spot where a component's leg gets soldered. Traces
connect pad to pad. On your board most pads are **through-hole** — they have a
drilled hole so a component leg pokes through and is soldered on the back.

### Ratsnest (the thin lines you saw before routing)

Before you route, the software draws thin straight "rubber-band" lines showing
*which pads need to be connected*. These are called the **ratsnest** (or airwires).
They are **not** real wires — just hints. Your whole routing job was to replace
each thin ratsnest line with a real copper trace. When you draw the trace, the
matching ratsnest line disappears.

### Net

A **net** is a group of pads that all need to be connected together (because the
schematic says so). For example, every pad that should connect to "+3.3V" is on
the `+3.3V` net. "GND" is the net for ground. Routing = connecting every pad on
each net with copper.

---

## 2. The story, step by step (from your red traces to the finish)

### Where you started: hand-drawing red traces

When you pressed **`X`** in KiCad and clicked pad-to-pad, you were **manually
routing** — drawing copper traces by hand, one at a time. The red line that
appeared was a real trace on the top copper layer (F.Cu). You successfully
connected a few (like the +3.3V trace) — that proved you understood the idea:
**trace over each ratsnest line, pad to pad.**

### The problem we hit: bad placement made routing impossible

You found that many traces were impossible to route cleanly. **This was not your
fault.** The components were arranged badly. Two specific problems:

- The **display header (J3)** was on the far *left* of the board, but every wire
  it needed went to **J4 on the right** — so 6 wires had to cross the *entire*
  board.
- Two **buttons (SW2, SW3)** were on the left, but their signals went to J4 on
  the right too.

When parts that connect to each other are far apart, their wires cross everything
and tangle. The professional rule is: **good placement makes routing easy; bad
placement makes it impossible.** So we fixed the placement first.

### What I did: re-organized the components (Step 3 redone)

I rearranged all 22 components into logical **clusters**, so parts that connect to
each other sit near each other:

- **Power section** (voltage regulator + capacitors) grouped in the top-left.
- **Analog frontend** (the BNC input → op-amp chain) flowing left-to-right across
  the top.
- **Display header (J3)** moved right next to **J4** — killing those 6 cross-board wires.
- **Buttons** moved next to the headers they connect to.

This is why the tangle calmed down dramatically after the re-placement.

### Then: auto-routing with Freerouting (Step 4 finished)

Instead of you hand-drawing all ~19 connections, we used a program called
**Freerouting** to draw all the copper traces automatically. (Explained in detail
in Section 5.) It routed the whole board in about 2 seconds — that's the **179
traces**, both red (top) and blue (bottom), now on your board.

### Why I asked you to make changes twice

You asked why I made you redo things twice. Here's the honest answer:

When I first re-placed the components, I **underestimated the physical size of the
buttons**. A push-button is about 12 mm wide with pads sticking out 14 mm from its
anchor point — bigger than my first estimate. So:

- **1st fix:** A button (SW1) ended up physically *overlapping* the J2 header —
  their holes literally landed on the same spot. The DRC check caught it. I moved
  the buttons away and we re-routed.
- **2nd fix:** After that, two buttons (SW2, SW3) were still only 10 mm apart, but
  they need ~15 mm so their bodies don't physically collide. DRC caught that too.
  I spaced them out and we re-routed one last time.

Each time we moved parts, the old traces no longer lined up, so we had to re-route
— that's why you exported/imported a few times. It wasn't wasted; it was the
normal "check → fix → re-check" loop that catches real manufacturing problems
*before* you spend money. The end result: a board with **zero errors**.

### Finally: DRC clean → Gerbers exported (Steps 5 & 6)

After the last fix, the automatic check (DRC) reported **0 errors and 0 missing
connections**. That was our agreed stopping point. Then I exported the **Gerber**
files (Section 8) — the package you send to a factory like JLCPCB.

---

## 3. What did you do with the grounds? (your question)

**Ground (GND)** is the common "0 volts" reference that almost every part connects
to — it's the single biggest net on any board (tons of pads need ground).

There are two ways to connect all the ground pads:

1. **Route them as traces** — draw a copper line to each ground pad like any other
   net.
2. **Copper pour** — flood a whole area of the board with copper and let every
   ground pad touch it (Section 7).

**What we actually did:** Freerouting connected all the ground pads using normal
**traces** (option 1). The DRC check confirmed every single ground pad is properly
connected (0 unconnected). So ground is *fully handled*.

Earlier in the process I had planned to use a copper pour for ground (option 2),
which is why you saw "ground pour" in our step list. But since the auto-router
already connected every ground pad with traces, **the pour became unnecessary** —
the board is complete and correct without it. A pour would be a nice-to-have for
noise reduction, not a requirement. We correctly skipped it.

---

## 4. Why are some wires blue? (your question)

Because your board has **two copper layers**, and the software color-codes them:

- **Red wires = top copper (F.Cu)**
- **Blue wires = bottom copper (B.Cu)**

When two wires need to cross without touching, the router puts one on top (red)
and one on the bottom (blue) so they pass over/under each other — like a highway
overpass. On your through-hole board, the component legs go through the whole
board, so a trace can connect on either the red or the blue layer at the same pad
without needing extra holes. That's why there are no "vias" (layer-change holes) —
the through-hole pads already bridge both layers.

---

## 5. What is Freerouting and what is it used for? (your question)

**Freerouting** is a free, open-source **auto-router** — a program that draws all
the copper traces on a PCB automatically, so you don't have to click each one by
hand.

### Why we used it

Hand-routing your board meant manually drawing ~19 connections, and you found it
slow and frustrating ("super clunky"). An auto-router does the same job in
seconds. With your now-clean placement, it did an excellent job.

### How it works (the DSN → SES dance)

Freerouting is a separate program from KiCad, so they hand files back and forth:

1. **KiCad exports a `.dsn` file** (`File → Export → Specctra DSN`). This `.dsn`
   describes your board to Freerouting: where every pad is, the board outline, and
   which pads need connecting (the nets). Think of it as "here's the puzzle."
2. **Freerouting reads the `.dsn`, solves the routing**, trying thousands of trace
   paths until everything is connected without crossings or rule violations. I ran
   this on the command line:
   `java -jar freerouting.jar -de fullScope.dsn -do fullScope.ses`
3. **Freerouting writes a `.ses` file** (a "session" file). This is its *answer* —
   the list of all the trace paths it figured out.
4. **KiCad imports the `.ses`** (`File → Import → Specctra Session`), which draws
   all those traces onto your real board.

That's the whole loop: **KiCad → .dsn → Freerouting → .ses → KiCad.** Every time
we moved components, we ran this loop again so the routing matched the new
positions.

> **"java -jar"**: Freerouting is written in the Java language, so it runs with the
> `java` command. You already had Java installed, which is why it worked.

---

## 6. How my "automation scripting" works (your question)

A KiCad PCB file (`fullScope.kicad_pcb`) is actually a **text file**. If you open
it in a text editor, it's a long list describing every component, its position,
every trace, etc., written in a format with lots of parentheses, like:

```
(footprint "Button"
    (at 78 104)        ← this line is the component's X,Y position
    ...
)
```

Because it's text, I can read and edit it with small **scripts** (tiny programs,
written in Python). Here's what I used scripting for:

- **Reading the board:** my scripts scanned the file to list every component, its
  position, its pads, and which net each pad belongs to. That's how I figured out
  the "J3 is far from J4" problem mathematically.
- **Re-placing components:** to move a part, my script found its `(at X Y)` line
  and changed the numbers. Moving 22 components by hand would be slow and
  error-prone; a script does it instantly and exactly.
- **Checking for overlaps:** before applying a new layout, my script calculated
  each component's real size and checked that none would physically collide — so
  we'd catch problems *before* opening KiCad.
- **Clearing old traces:** when we re-placed parts, the old traces were wrong, so a
  script deleted all the `(segment ...)` lines (each trace is a "segment") to give
  a clean slate for re-routing.

> **Important caution we respected:** editing the file directly is powerful but
> risky — one wrong character can corrupt the board. That's why I always made a
> **backup first** (you'll see `.bak_...` files in the folder), and why we did the
> *routing* with Freerouting + the KiCad GUI rather than hand-writing traces into
> the file. We even tested it: I tried writing one trace directly into the file,
> it didn't take (your KiCad version uses a new format), so we wisely switched to
> the GUI/Freerouting approach instead.

---

## 7. What does "pouring" / copper pour mean? (your question)

A **copper pour** (also called a "filled zone" or "ground plane") is when you
flood an entire region of the board with a solid sheet of copper, instead of thin
traces.

It's mainly used for **ground**. Instead of running a separate ground trace to
every part, you pour copper across the whole board and every ground pad just
touches it. Benefits:

- Every ground pad connects automatically.
- The big copper sheet reduces electrical noise (good for sensitive analog parts
  like your op-amp).

**We did not need it** on your board, because the auto-router already connected
every ground pad with traces (see Section 3). The board is complete without a
pour. You could add one later as a polish step, but it's optional.

---

## 8. What is DRC? What is a drill file? What are Gerbers? (your questions)

These are the final three concepts — the "is it correct?" check and the "send to
factory" files.

### DRC — Design Rule Check

**DRC** is an automatic inspector. You press a button and the software checks your
whole board against the manufacturing rules and reports every mistake, such as:

- Two traces too close together (could short circuit).
- A drilled hole too close to another hole.
- A connection that was never routed (a "missing wire").
- A part hanging off the edge of the board.

**This is what caught the button problems.** Each time, DRC told us exactly what
was wrong and where. When DRC finally reported **"0 violations, 0 unconnected
items,"** it meant the board is electrically correct and manufacturable. That was
our finish line.

### Drill file

The factory needs to know **where to drill holes** (for every through-hole part
leg) and **how big** each hole is. The **drill file** (`fullScope.drl`) is a list
of all those hole positions and sizes. The drilling machine reads it directly.

### Gerbers

**Gerber files** are the universal language of PCB factories. Each Gerber file
describes **one layer** of your board as precise shapes the factory machines can
reproduce. Your export produced one file per layer, including:

| File ending | What it describes |
|---|---|
| `.gtl` / `-F_Cu` | Top copper (the red traces) |
| `.gbl` / `-B_Cu` | Bottom copper (the blue traces) |
| `.gts` / `.gbs` | Solder mask (the green coating, with gaps at pads) |
| `.gto` / `.gbo` | Silkscreen (the white text/labels) |
| `.gm1` / `-Edge_Cuts` | The board outline (where to cut) |
| `.drl` | The drill holes |

Together, these files are a complete recipe for building your exact board. I
bundled them into **`fullScope_gerbers.zip`** — that single zip is what you upload
to a manufacturer like JLCPCB, and they ship you the physical board.

---

## 9. Where things stand & what's left

- ✅ Board is fully placed, routed, and **passes DRC with zero errors**.
- ✅ Gerbers + drill files are exported and zipped:
  `pcb/fullScope/fullScope_gerbers.zip`
- ⚠️ **Before ordering:** measure the real distance between the two pin-header rows
  on your physical Diymore STM32 board with calipers, and confirm the J2↔J4
  spacing matches (~35.6 mm was an estimate). This is the one thing we couldn't
  verify without the board in hand. See `FABRICATION_TODO.md`. If it's off, the
  board won't plug together.

That's the entire journey. You took a circuit from a schematic to a
factory-ready board — placement, routing, verification, and output files. That's
the full PCB design skill in miniature.

---

## 10. Quick glossary (one-line reminders)

- **PCB** — the physical circuit board.
- **Trace / track** — a copper line that connects parts (replaces a wire).
- **Pad** — metal spot where a part is soldered.
- **Net** — a group of pads that must be connected (e.g. GND, +3.3V).
- **Ratsnest** — thin hint-lines showing what still needs connecting.
- **F.Cu (red)** — top copper layer. **B.Cu (blue)** — bottom copper layer.
- **Edge.Cuts (yellow)** — the board outline.
- **Placement** — arranging components physically.
- **Routing** — drawing the traces.
- **Freerouting** — a program that routes automatically.
- **DSN / SES** — the files KiCad and Freerouting exchange.
- **Copper pour** — a solid sheet of copper, usually for ground.
- **DRC** — automatic error check of the whole board.
- **Drill file** — list of hole positions/sizes.
- **Gerbers** — the per-layer files you send to the factory.
- **Via** — a small plated hole that moves a trace between layers (your board
  didn't need any, because through-hole pads already bridge both layers).
