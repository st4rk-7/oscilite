# Oscilite — Image Shot List

Capture list for the README + LinkedIn / GitHub / portfolio publish.
Goal: show it **works**, show it's **real hardware**, and show the **engineering depth** (firmware → analog → PCB → fab).

Save everything into `assets/images/`. Suggested final filenames are in each item.
Existing files: `img1.jpg`, `img2.jpg` (re-slot or rename into the list below).

> **⚠️ No physical STM32 on hand right now.** Everything in **GROUP A** below is
> generated on your computer (KiCad, diagrams) and can be captured *today* — that
> covers all of TIER 1 except the live-screen photo, plus most depth shots.
> Everything in **GROUP B** needs the powered-up board and waits until you have it.
> You can publish a strong README/portfolio post with Group A alone; add Group B later.

---

## ✅ GROUP A — Capturable now (no hardware needed)

These are the high-value, "real engineering" shots and they're all free to produce:

- [ ] **PCB 3D render — top** — `pcb_3d_top.png`
  KiCad → open `pcb/fullScope/fullScope.kicad_pcb` → View → **3D Viewer** (Alt+3) → File → Export Current View → PNG. Use this as the **hero image** until you have a real photo.

- [ ] **PCB 3D render — bottom** — `pcb_3d_bottom.png`
  In the 3D viewer, drag to flip the board. Shows bottom-copper (blue) routing.

- [ ] **PCB 2D layout (routed)** — `pcb_layout.png`
  KiCad PCB editor, all copper layers on, traces visible. Screenshot or File → Export → SVG/PNG. Shows the routing work.

- [ ] **Schematic overview** — `schematic.png`
  From `fullScope.kicad_sch`: File → Plot → PDF (or screenshot the sheet). Signals "designed circuit, not a breadboard hack."

- [ ] **Analog frontend close-up** — `frontend.png`
  Crop just the frontend section of the schematic (±3.3V attenuator / op-amp / 1.65V bias). The cleverest electronics in the project. (Also see `docs/frontend.pdf`.)

- [ ] **Gerber / fab preview** — `gerber_preview.png`
  Upload `pcb/fullScope/fullScope_gerbers.zip` to an online viewer (JLCPCB preview, or use KiCad's Gerber Viewer) and screenshot. Proves it's manufacturing-ready.

- [ ] **Block diagram** — `block_diagram.png`
  Signal flow: `Input → Analog Frontend → ADC → DMA → Buffer → Display`. Make in draw.io / Excalidraw. The single most useful image for a reader skimming the README — and the README already has this as ASCII, so you're just prettifying it.

- [ ] **(Optional) DRC clean screenshot** — `drc_clean.png`
  KiCad → Inspect → Design Rules Checker → Run. Screenshot the "0 violations" result. Strong credibility for an embedded/hardware portfolio.

> With Group A you have: a hero (3D render), the layout, schematic, frontend, fab proof,
> and a diagram — enough for a complete README and LinkedIn carousel **today**.

---

## ⏳ GROUP B — Needs the physical board (capture later)

- [ ] **Hero shot (real)** — `hero.jpg` — assembled scope powered on showing a waveform. Swap in over the 3D render once you have it.
- [ ] **Live waveform close-up** — `waveform_screen.jpg` — display showing a trace + grid. Feed a 1 kHz square from a function gen or another MCU PWM pin.
- [ ] **Wiring / bring-up shot** — `bringup.jpg` — STM32F407 + display + frontend on jumper wires. `img1.jpg`/`img2.jpg` may already be this — check them.
- [ ] **UI / menu shot** — `ui_menu.jpg` — on-screen timebase/volt/trigger controls.
- [ ] **Splash screen** — `splash.jpg` — the boot splash (from your `splash.h` + `img2splash.py` pipeline).
- [ ] **Trigger demo (2 photos)** — `trigger_unstable.jpg` / `trigger_stable.jpg` — same signal, trigger off vs on. Great LinkedIn carousel.
- [ ] **Multiple waveforms grid** — `waveforms_montage.jpg` — sine/square/triangle/noise, 2x2.
- [ ] **Size/scale shot** — `scale.jpg` — board next to a coin/hand.

> **Check `assets/images/img1.jpg` and `img2.jpg` first** — if they're already bench/bring-up
> photos, you may already have part of Group B covered.

---

## (original tiers, for reference)

## TIER 1 — Must have (the README cannot land without these)

- [ ] **Hero shot** — `hero.jpg`
  The assembled scope powered on, displaying a clean waveform (sine or square). Slightly angled, good lighting, plain background. This is the LinkedIn thumbnail and the top of the README. Make it the best photo you take.

- [ ] **Live waveform close-up** — `waveform_screen.jpg`
  Tight shot of the display showing a recognizable trace with the grid/graticule visible. Proves the DSO actually samples and renders. Feed it a known signal (e.g. 1 kHz square from a function gen or another MCU PWM pin).

- [ ] **PCB 3D render — top** — `pcb_3d_top.png`
  KiCad → View → **3D Viewer** → export PNG. Top of `pcb/fullScope/fullScope.kicad_pcb`. Looks professional and costs nothing to produce.

- [ ] **PCB 2D layout (routed)** — `pcb_layout.png`
  KiCad PCB editor, all copper layers visible, traces routed. Export via File → Export → SVG/PNG, or screenshot. Shows the 179-trace routing work.

---

## TIER 2 — Strongly recommended (depth + credibility)

- [ ] **PCB 3D render — bottom** — `pcb_3d_bottom.png`
  Flip side in 3D viewer. Shows the bottom-copper (blue) routing.

- [ ] **Schematic overview** — `schematic.png`
  Export the full sheet from `fullScope.kicad_sch` (File → Plot → PDF, or screenshot). Even as a thumbnail it signals "this is a designed circuit, not a breadboard hack."

- [ ] **Analog frontend close-up** — `frontend.png`
  Crop of just the analog-frontend section of the schematic (the ±3.3V attenuator / op-amp / 1.65V bias). This is the cleverest electronics in the project — call it out. (Ref: `docs/frontend.pdf` mentioned in HowItWorks.md.)

- [ ] **Wiring / bring-up shot** — `bringup.jpg`
  STM32F407 + display + frontend wired on the bench (jumper wires / dev board stage). Tells the "before the PCB" story. `img1.jpg`/`img2.jpg` may already be this.

- [ ] **UI / menu shot** — `ui_menu.jpg`
  The on-screen UI: timebase / voltage / trigger controls or the menu. Shows it's a usable instrument, not just a trace renderer.

- [ ] **Splash screen** — `splash.jpg`
  The boot splash on the display. You built a `splash.h` + `img2splash.py` pipeline — worth a sentence and a photo.

---

## TIER 3 — Nice to have (storytelling / extra polish)

- [ ] **Trigger demo (2 photos)** — `trigger_stable.jpg`, `trigger_unstable.jpg`
  Same signal, trigger off vs on (jittery trace vs locked trace). Great for a LinkedIn carousel — visually demonstrates what triggering does.

- [ ] **Multiple waveforms grid** — `waveforms_montage.jpg`
  Sine / square / triangle / noise in a 2x2 montage. Shows range. Good portfolio filler.

- [ ] **Size/scale shot** — `scale.jpg`
  Scope next to a coin or hand for sense of scale. Humanizes the build.

- [ ] **Gerber / fab preview** — `gerber_preview.png`
  Screenshot of the gerbers in an online viewer (e.g. JLCPCB upload preview or KiCad gerber viewer). Proves it's manufacturing-ready.

- [ ] **Block diagram** — `block_diagram.png`
  Signal flow: `Input → Analog Frontend → ADC → DMA → Buffer → Display`. Make in draw.io / Excalidraw. The single most useful image for a reader skimming the README. (Optional but high value.)

---

## Capture tips
- **One consistent background + lighting** for all physical photos → looks like a deliberate project, not random snaps.
- Shoot landscape (16:9) — fits README and LinkedIn better than portrait.
- For screen photos: dim room, lower display brightness slightly, focus on the screen to avoid moire/glare.
- KiCad renders export at high res for free — lean on them; they carry the README even before you reshoot hardware photos.

## Where they go
- **README hero block:** `hero.jpg` + one-line tagline.
- **"It works" section:** `waveform_screen.jpg`, `ui_menu.jpg`, trigger demo.
- **"Hardware design" section:** `pcb_3d_top.png`, `pcb_layout.png`, `schematic.png`, `frontend.png`.
- **"How it works" section:** `block_diagram.png` (pairs with `docs/HowItWorks.md`).
- **LinkedIn post:** lead with `hero.jpg`, then a 3–5 image carousel (waveform, PCB 3D, schematic, trigger demo).
