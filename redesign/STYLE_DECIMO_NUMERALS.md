# Décimo numeral style (1970s–80s) — tokens for the numbers grid & hero número

Research-backed reference for restyling `.btn_number` chips and `#current_number` to echo the
NUMBER as printed on real Lotería Nacional décimos of the 70s–80s. Apply on top of the v2 cartel theme.

## Key findings (observed from period décimos + documented sources)
- **Number = overprint by a *máquina numeradora*** → reads as a serial: **tabular/monospaced**, every digit equal width, the five digits a rigid block aligning across the ten fracciones. This is the single most period-correct trait.
- **Face:** bold, tall, lightly-condensed grotesque — the heaviest mark on the ticket.
- **Ink:** **warm near-black overprint (#1A1714)** is the norm; the *fixed* artwork carried one design ink per sorteo (green/sepia/indigo/ochre/vermilion). Red numbering existed but was the exception → **default the número to black**, not red.
- **No hard box:** number sits on the guilloche ground over a faintly *reserved (lighter) panel*, not a ruled box. Often repeated smaller at the corners.
- **Edges:** ten décimos separated along **perforations** → a detached décimo shows serrated/punched edges ("torn from a booklet").
- **Ground:** fine guilloche lathe-work in the design ink at low opacity; cream security paper (~#F4ECD8), single engraved thematic vignette (one motif per sorteo since 1960).
- **70s→80s:** format stable; the authenticity date-stamp is the organism wording — pre-1985 "Servicio Nacional de Loterías / Ministerio de Hacienda" → from 1985–86 "Organismo Nacional de Loterías y Apuestas del Estado (ONLAE)".

## Fonts (Google Fonts)
- **Chips (two-digit tiles): `Oswald` 600** — tall, lightly-condensed, tabular numerals, very legible small (protects the 70yo reader).
- **Hero número: `Martian Mono` 800** (fallback `Oswald` 700) — grotesque monospace = literal numbering-machine texture; only used where size guarantees legibility.
- Force `font-variant-numeric: tabular-nums lining-nums;` + `font-feature-settings:"tnum" 1,"lnum" 1,"calt" 0,"liga" 0;`. Avoid Major Mono Display (low legibility).
- `@import`: `https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Martian+Mono:wght@600;800&display=swap`

## Palette
- Paper cream `#F4ECD8` (hi `#F8F2E2`, edge `#E7DBBE`); overprint near-black `#1A1714`.
- Design ink (one per theme): green `#2E5E3A` · sepia `#6E4A2B` · indigo `#28406B` · ochre `#B8860B` · vermilion `#B23A2E`. Guilloche = design ink @ ~18%.

## CSS recipe (perforated décimo chip + guilloche + reserved panel)
```css
:root{
  --paper:#F4ECD8; --paper-hi:#F8F2E2; --paper-edge:#E7DBBE;
  --ink:#1A1714; --design-ink:#2E5E3A; --guilloche:rgba(46,94,58,.18);
  --font-chip:"Oswald",system-ui,sans-serif;
  --font-hero:"Martian Mono","Oswald",monospace;
  --num-features:"tnum" 1,"lnum" 1,"calt" 0,"liga" 0;
  --perf-r:2px; --perf-s:8px;
  --guilloche-img:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='40'%3E%3Cg fill='none' stroke='%232E5E3A' stroke-width='0.6' opacity='0.18'%3E%3Cpath d='M0 20 C15 4 45 4 60 20 S105 36 120 20'/%3E%3Cpath d='M0 20 C15 36 45 36 60 20 S105 4 120 20'/%3E%3Cpath d='M0 12 C15 0 45 24 60 12 S105 0 120 12'/%3E%3Cpath d='M0 28 C15 40 45 16 60 28 S105 40 120 28'/%3E%3C/g%3E%3C/svg%3E");
}
.num{ font-variant-numeric:tabular-nums lining-nums; font-feature-settings:var(--num-features); }
/* .btn_number chip: warm-black tabular digit on cream guilloche, reserved panel, perforated edge.
   Use --page = color of the surface BEHIND the chip so the radial-gradient notches punch cleanly. */
.btn_number{
  --page:var(--paper);
  font-family:var(--font-chip); font-weight:600; color:var(--ink);
  font-variant-numeric:tabular-nums lining-nums; font-feature-settings:var(--num-features);
  background:
    radial-gradient(var(--perf-r) at 50% 0,#0000 96%,var(--page) 0) 0 0/var(--perf-s) var(--perf-s) repeat-x,
    radial-gradient(var(--perf-r) at 50% 100%,#0000 96%,var(--page) 0) 0 100%/var(--perf-s) var(--perf-s) repeat-x,
    radial-gradient(var(--perf-r) at 0 50%,#0000 96%,var(--page) 0) 0 0/var(--perf-s) var(--perf-s) repeat-y,
    radial-gradient(var(--perf-r) at 100% 50%,#0000 96%,var(--page) 0) 100% 0/var(--perf-s) var(--perf-s) repeat-y,
    radial-gradient(circle at 50% 50%,var(--paper-hi) 0 42%,#0000 64%),
    var(--guilloche-img) center/60px 20px repeat,
    var(--paper);
  box-shadow:inset 0 0 0 1px var(--paper-edge);
}
#current_number{
  font-family:var(--font-hero); font-weight:800; letter-spacing:.04em; color:var(--ink);
  font-variant-numeric:tabular-nums lining-nums; font-feature-settings:var(--num-features);
  text-shadow:0 1px 0 var(--paper-hi);
}
```
NOTE: this must be reconciled with the v2 status states (Perfecto/Defectuoso/Falta/Faltan datos) — keep the status as a coloured cue layered over the décimo look, not replacing legibility. Sources: infobae, tulotero, loteriaanta, museodelprado, BOE RD 904/1985, loteriachus/todocoleccion/aeclot galleries.
