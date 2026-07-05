# EL ARTE DEL DÉCIMO — v3 (LOCKED)

> **Status:** LOCKED direction for the visual redesign of *Los décimos de Ildefonso*.
> **Replaces:** v2 "EL CARTEL DE ILDEFONSO" (`STYLE_MIDCENTURY.md`, the cartel `theme.css`)
> — **REJECTED** for reading like a lottery *advertisement* (poster shout, starbursts,
> banderola ribbons, "GORDO" hype, halftone, slow-turning destello, royal-blue officialdom,
> litho-gold-on-green masthead). v3 keeps the same **CSS-overlay-on-Bootstrap-4.6** structure
> and every load-bearing class/id/JS hook from `FUNCTIONAL_CONTRACT.md`. Nothing in the markup
> contract changes; this is a re-skin.
> **Keeps intact:** the warm aged-paper ground, and the 1970s–80s décimo NUMERAL treatment for
> the chip grid + hero número (`STYLE_DECIMO_NUMERALS.md`) — the real numbering-machine serial,
> not an ad. WCAG AA, body ≥18px, ≥44–48px targets, visible focus.

---

## 1. Concept narrative

The site is the private album of a **retired professor (b. 1955)** who collects *décimos* not for
luck but for their **engraving craft** — the burin work the FNMT *grabadores* cut into security
paper: the *orla* (engraved border), the *volutas* (scrollwork) at its corners, the *guilloché*
lathe-line drawn by a *torno geométrico*, the fine *filigrana*, the *cartelas* (cartouches) that
quiet an inscription, the small monochrome allegorical vignette held inside a roundel.

We are reproducing **the frame and the line, never the picture and never the advertisement.** The
page behaves like *an engraved leaf under a reading lamp*: a warm cream sheet, one or two muted
engraving inks, symmetry and repetition, ornament that **rewards close reading and never calls
across a room.** The eye lands on the **number** — the warm-black numbering-machine serial, the one
strong note — then reads outward into the quiet ornament.

**The signature is the engraved décimo frame**, not a masthead. We spend our single measure of
boldness on **one beautifully engraved orla** (graded rules → voluta corners → faint guilloche
ground) around the principal plate, and keep everything else whisper-quiet. No motion. No prize,
luck, betting or winning framing. No state / SELAE / ministry wording or seal.

---

## 2. Palette — aged paper + engraving ink + ONE accent

A deliberately **collapsed, quiet** palette: warm paper, a warm-black/umber engraving ink, and a
**single restrained accent — deep bottle-green (`--verde-botella`)**, the period FNMT
security/design ink. Green is chosen over carmine precisely *because* it reads scholarly, not
"lotto", and because it unifies with the green guilloche ground the numeral treatment already uses.
**There is no second chromatic accent** — no gold, no red, no blue. Status, hierarchy and meaning
come from **value + engraved ornament + label**, not from a spread of hues.

Token names are kept identical to the current `theme.css` so the implementation is mostly a
**value swap + section rewrite**; re-valued tokens are noted.

```css
:root{
  /* — Paper: warm aged security stock, never pure white — */
  --crema:        #F4ECD8;  /* page + card + chip ground (cream security paper) */
  --crema-alta:   #FBF5E6;  /* raised/reserved highlight panel, navbar field, incise highlight */
  --papel-prensa: #E6D8B8;  /* deeper panel / foxing / "Faltan datos" tile / paper edge   (re-valued) */
  --marfil:       #F8F2E2;  /* reversed text/numerals on the green accent */

  /* — Ink: the engraving (warm near-black + umber line) — */
  --tinta:        #1C1812;  /* body ink, masthead titling, the numeral overprint  (re-valued)  ~15:1 AAA */
  --tinta-sepia:  #574231;  /* engraving LINE + captions + frame rules (umber)     (re-valued)  ~8:1 AAA */
  --nogal:        #3A2A1A;  /* deepest umber — outer frame rule, footer, cabinet chrome */
  --nogal-claro:  #5A3E2B;  /* dividers, soft hairlines, divider ornament */
  --sepia-tenue:  #8A745C;  /* faintest engraved hairline / guilloche-in-sepia — DECORATIVE only, never text */

  /* — The ONE accent: deep bottle-green FNMT design ink — */
  --verde-botella:#1E4D34;  /* accent fills (owned/Perfecto tile, map mat), reversed text ground  (re-valued) ~8.2:1 */
  --verde-claro:  #2E5E3A;  /* the décimo guilloche ink + owned accent line/border  (re-valued) ~6.4:1 */

  /* (REMOVED from v2 — do not reintroduce: --bermellon, --bermellon-hondo, --ocre-oro,
     --mostaza, --azul-real, --tinta-registro, --billete-rule, --semitono*) */
}
```

### WCAG notes (computed on `--crema` #F4ECD8, L≈0.842)

| Pair | Ratio | Verdict |
|---|---|---|
| `--tinta` #1C1812 on cream | **15.0:1** | AAA — body, numerals, titling |
| `--tinta-sepia` #574231 on cream | **8.0:1** | AAA — captions/labels ≥17px, ornament line, frame rules |
| `--nogal` #3A2A1A on cream | ~11:1 | AAA — outer rules, footer text |
| `--verde-botella` #1E4D34 on cream | **8.2:1** | AAA as line/text; used as accent line + fill |
| `--marfil` #F8F2E2 on `--verde-botella` | **8.2:1** | AAA — reversed numeral on the green tile |
| `--verde-claro` #2E5E3A on cream | **6.4:1** | AA normal / AAA large — owned border, success line |
| `--sepia-tenue` #8A745C on cream | ~3.2:1 | **decorative only** (guilloche/hairline), never text |

Rule: the engraving inks (`--tinta` / `--tinta-sepia` / `--nogal` / `--verde-botella`) are all
**AA+ for text**; `--sepia-tenue` and any guilloche/filigree are **texture below text** at low
opacity and must never carry meaning or contrast. Contrast hierarchy (darkest → faintest):
**numerals → masthead titling → border rules → vignette → guilloche/filigree ground.**

---

## 3. Type system

A refined engraver's roman for display, a sober small-caps inscription voice for captions/labels,
a genuinely legible serif for reading, and the numbering-machine faces for numbers.

```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=EB+Garamond:ital,wght@0,400;0,500;0,600&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Oswald:wght@500;600;700&family=Martian+Mono:wght@600;800&display=swap');

:root{
  --font-display:   "Cormorant Garamond", "Playfair Display", Georgia, serif; /* high-contrast engraver's roman — masthead + H1/H2, all-caps, tracked */
  --font-caps:      "EB Garamond", Georgia, serif;     /* true small-caps (smcp) — captions, labels, nav, button text */
  --font-body:      "Lora", Georgia, serif;            /* the calm reading face — robust x-height for older eyes */
  /* — décimo numbering faces (KEPT verbatim from STYLE_DECIMO_NUMERALS.md) — */
  --font-numerador: "Martian Mono", "Oswald", monospace;  /* hero número — literal numbering-machine */
  --font-chip:      "Oswald", system-ui, sans-serif;      /* two-digit chips — tall, tabular, legible small */
  --num-features:   "tnum" 1, "lnum" 1, "calt" 0, "liga" 0;

  /* (REMOVED from v2: --font-banner Anton, --font-slab Alfa Slab One, --font-script Yellowtail,
     --font-condensed Oswald-as-UI. Oswald survives ONLY as the chip numeral face.) */
}
```

**Roles & sizes**

- **Body** — `--font-body` (Lora), **19px** base / **1.6** line-height, `--tinta`. Never below 18px
  for read text; 17px microtype floor for captions.
- **Display H1 / masthead** — `--font-display`, **all-caps, `letter-spacing:.08em`**, `--tinta`,
  high stroke contrast. `clamp(34px, 5vw, 56px)`. This is *engraved titling*, set centered, quiet —
  it does **not** advertise. No fill-gold, no destello, no skew, no drop-shadow stack.
- **H2–H6** — `--font-display` 600 (H2 30px, H3 25px, H4 22px, H5 20px, H6 18px), `--nogal`.
- **Captions / labels / nav / button text** — `--font-caps` (EB Garamond) **small-caps**, tracked
  `.06–.08em`, `--tinta-sepia` — the sober "document inscription" voice. Use `.engrave-caps` (§5.8).
- **Lead** — `--font-body` italic, 21px, `--tinta-sepia`.
- **Numbers** — chips `--font-chip` 600; hero `--font-numerador` 800; always
  `font-variant-numeric: tabular-nums lining-nums; font-feature-settings: var(--num-features);`.

---

## 4. The décimo numeral treatment (KEPT — the only strong note)

Unchanged in spirit from `STYLE_DECIMO_NUMERALS.md`; the green guilloche ground and warm-black
overprint already match the v3 accent, so this carries straight over. Re-stated tokens:

```css
:root{
  --perf-r: 2px;  --perf-s: 9px;   /* perforation radius + pitch (the torn fracción edge) */
  /* faint verde guilloche security ground for the ticket tiles (opacity baked into the SVG) */
  --guilloche-decimo: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='40'%3E%3Cg fill='none' stroke='%232E5E3A' stroke-width='0.6' opacity='0.16'%3E%3Cpath d='M0 20 C15 4 45 4 60 20 S105 36 120 20'/%3E%3Cpath d='M0 20 C15 36 45 36 60 20 S105 4 120 20'/%3E%3Cpath d='M0 12 C15 0 45 24 60 12 S105 0 120 12'/%3E%3Cpath d='M0 28 C15 40 45 16 60 28 S105 40 120 28'/%3E%3C/g%3E%3C/svg%3E");
}
```

- **`#current_number` (hero número)** — `--font-numerador` 800, `--tinta` overprint, tabular,
  `letter-spacing:.07em`, on a cream plaque with the four-sided perforation + faint guilloche
  ground. The v2 **bermellón billete bottom-rule is REPLACED** by a graded **sepia engraved
  base-rule** and a single **voluta cresting** above (`.cartouche`, §5.2). The `Nº` caption
  (`::before`, cosmetic, not read by JS) becomes `--font-caps` small-caps `--tinta-sepia`.
- **`.btn_number` (chips)** — `--font-chip` 600, `--tinta`, tabular; perforated edges + guilloche
  ground over a reserved (lighter) `--crema-alta` panel; outer hairline `inset 0 0 0 1px
  var(--papel-prensa)`. No ruled box. (§6 status states recolor *only* `background-color`/`color`,
  preserving the perforation + guilloche image layers.)

---

## 5. ENGRAVING ORNAMENT KIT (CSS / SVG)

Every technique is **static** (no `@keyframes`, no movement transition — hover may change *color*
only), **subtle** (stroke 0.6–1px, opacity 0.12–0.25), and **subordinate to text** (ornament at
`z-index:0` beneath content at `z-index:1`, never dropping contrast below AA).
**Data-URI rule:** encode every `#` as `%23`; size `<rect>` in absolute px (never `100%`) to avoid
`%`. All SVG attributes in single quotes.

### 5.1 Aged-paper texture (fine grain + low-freq foxing, NO halftone)
Replaces v2's `--paper-grain`/`.semitono` poster screens. `fractalNoise` mapped luminance→alpha so
it only darkens the cream; large-scale layer (2) adds uneven aging.

```css
body{ background-color: var(--crema); }
body::before{
  content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
  opacity:.12; mix-blend-mode:multiply;
  background-repeat:repeat, repeat; background-size:180px 180px, 360px 360px;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch' result='n'/%3E%3CfeColorMatrix in='n' type='matrix' values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.33 0.33 0.33 0 0'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23g)'/%3E%3C/svg%3E"),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='360' height='360'%3E%3Cfilter id='m'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.012' numOctaves='2' stitchTiles='stitch' result='n'/%3E%3CfeColorMatrix in='n' type='matrix' values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.18 0.18 0.18 0 0'/%3E%3C/filter%3E%3Crect width='360' height='360' filter='url(%23m)'/%3E%3C/svg%3E");
}
```

### 5.2 Voluta corner ornaments (the corner pair, mirrored to 4)
One inline S-scroll, flipped to four corners via CSS transforms; `currentColor` themes it.
Deploy on `.cartouche`: the **hero plate corners**, the **map orla corners**, a section masthead.
Keep the reading field free of scrollwork.

```html
<div class="cartouche">  <!-- e.g. wraps #current_number, or a heading -->
  <svg class="voluta voluta--tl" viewBox="0 0 64 64" aria-hidden="true">
    <path fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round"
      d="M2 62 C2 34 14 8 40 4 C26 10 22 24 26 34 C29 41 38 42 42 36 C45 31 41 26 36 28 C40 27 43 31 41 35"/>
  </svg>
  <!-- duplicate as voluta--tr / voluta--bl / voluta--br -->
</div>
```
```css
.cartouche{ position:relative; }
.voluta{ position:absolute; width:56px; height:56px; color:var(--tinta-sepia); opacity:.6; pointer-events:none; }
.voluta--tl{ top:6px; left:6px; }
.voluta--tr{ top:6px;  right:6px;  transform:scaleX(-1); }
.voluta--bl{ bottom:6px; left:6px; transform:scaleY(-1); }
.voluta--br{ bottom:6px; right:6px; transform:scale(-1,-1); }
/* a single top-center cresting (masthead): one voluta pair, no body scrollwork */
.cartouche--crest .voluta--tl{ left:50%; transform:translateX(-100%); }
.cartouche--crest .voluta--tr{ left:50%; transform:translateX(0) scaleX(-1); }
```

### 5.3 Filigree / acanthus divider (the *cul-de-lampe* section break)
A centered scroll knot flanked by tapering hairlines — the engraver's section rule. Static; the
single `<circle>` "eye" + two acanthus hooks read as cut scrollwork, **not** a sales rule.
Replaces the v2 `h1::after` billete bar and any `.banderola`.

```html
<svg class="divider" viewBox="0 0 240 16" width="240" height="16" role="presentation">
  <g fill="none" stroke="currentColor" stroke-width="0.8">
    <line x1="0" y1="8" x2="96" y2="8"/><line x1="144" y1="8" x2="240" y2="8"/>
    <path d="M96 8 C104 8 108 3 114 5 C120 7 117 12 111 11
             M144 8 C136 8 132 3 126 5 C120 7 123 12 129 11"/>
  </g><circle cx="120" cy="8" r="1.6" fill="currentColor"/>
</svg>
```
```css
.divider{ display:block; margin:1.75rem auto; color:var(--nogal-claro); opacity:.7; }
.divider--verde{ color:var(--verde-claro); }   /* under a nameplate / between collection sections */
```

### 5.4 Guilloche band (the slim lathe rule)
The workhorse tiling ornament — two phase-mirrored sine paths braiding past a midline; one exact
integer number of periods (120 = two of 60) so it repeats seamlessly. Use as a thin rule under the
navbar, framing the numeral block, footer band, card header. Default **sepia**; ceremonial
**verde** variant. Knock back with container `opacity`.

```css
.guilloche{ position:relative; }
.guilloche > *{ position:relative; z-index:1; }
.guilloche::before{
  content:""; position:absolute; inset:0; z-index:0; pointer-events:none; opacity:.16;
  background-repeat:repeat;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='24'%3E%3Cg fill='none' stroke='%23574231' stroke-width='0.8'%3E%3Cpath d='M0 12 C20 2 40 22 60 12 S100 2 120 12'/%3E%3Cpath d='M0 12 C20 22 40 2 60 12 S100 22 120 12'/%3E%3C/g%3E%3C/svg%3E");
}
.guilloche--verde::before{
  opacity:.14;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='24'%3E%3Cg fill='none' stroke='%232E5E3A' stroke-width='0.8'%3E%3Cpath d='M0 12 C20 2 40 22 60 12 S100 2 120 12'/%3E%3Cpath d='M0 12 C20 22 40 2 60 12 S100 22 120 12'/%3E%3C/g%3E%3C/svg%3E");
}
```

### 5.5 Guilloche rosette (the ceremonial seal)
A radiating star-flower of overlapping ellipses — the lathe roseta. Use **once** as a quiet
medallion where a seal would sit (hero corner, footer center, the `.btn-success` corner-mark),
carrying a **neutral floret only — never an official emblem**. Swap the ellipse stack for a baked
hypotrochoid `<path>` (miniwebtool / Pattern Monster export) for a denser cut.

```html
<svg class="roseta" viewBox="0 0 100 100" aria-hidden="true">
  <g fill="none" stroke="currentColor" stroke-width="0.6">
    <ellipse cx="50" cy="50" rx="40" ry="15" transform="rotate(0 50 50)"/>
    <ellipse cx="50" cy="50" rx="40" ry="15" transform="rotate(30 50 50)"/>
    <ellipse cx="50" cy="50" rx="40" ry="15" transform="rotate(60 50 50)"/>
    <ellipse cx="50" cy="50" rx="40" ry="15" transform="rotate(90 50 50)"/>
    <ellipse cx="50" cy="50" rx="40" ry="15" transform="rotate(120 50 50)"/>
    <ellipse cx="50" cy="50" rx="40" ry="15" transform="rotate(150 50 50)"/>
    <circle cx="50" cy="50" r="6"/>
  </g>
</svg>
```
```css
.roseta{ width:64px; height:64px; color:var(--verde-claro); opacity:.5; pointer-events:none; }
```

### 5.6 Triple-rule cartouche frame (no extra markup)
The engraver's graded **thick–thin–thin** orla, stacked with `::before`/`::after` so the rules sit
*inside* the panel. Sub-pixel weights snap to 0 on standard screens → emulate a lighter line with
a low-alpha inset `box-shadow`. Use on `.orla` / cards / the hero plate / `.frame`.

```css
.orla{ position:relative; padding:1.4rem 1.6rem; background:var(--crema);
  box-shadow: inset 0 0 0 1.5px var(--nogal); }            /* outer umber filete */
.orla::before{ content:""; position:absolute; inset:7px; pointer-events:none;
  border:1px solid var(--tinta-sepia); }                   /* walnut hairline */
.orla::after{ content:""; position:absolute; inset:11px; pointer-events:none;
  box-shadow: inset 0 0 0 1px rgba(46,94,58,.45); }        /* faint ~0.6px verde rule */
.orla--verde{ box-shadow: inset 0 0 0 1.5px var(--verde-botella); }
```

### 5.7 Corner-flourish orla via `border-image` (slice-9)
For volutas baked into the four corners with a thin repeating edge tick — the full engraved
*orla*. Color is hard-coded (`%23574231` sepia). Combine with §5.6 for a debossed cartouche with
filigree corners. This is the **signature frame** around the principal plate.

```css
.frame-orla{
  border:24px solid transparent;
  border-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='72' height='72'%3E%3Cg fill='none' stroke='%23574231' stroke-width='0.9' stroke-linecap='round'%3E%3Cpath d='M4 24 V8 a4 4 0 0 1 4-4 H24'/%3E%3Cpath d='M10 22 C10 14 14 10 22 10'/%3E%3Cpath d='M68 24 V8 a4 4 0 0 0-4-4 H48'/%3E%3Cpath d='M62 22 C62 14 58 10 50 10'/%3E%3Cpath d='M4 48 V64 a4 4 0 0 0 4 4 H24'/%3E%3Cpath d='M10 50 C10 58 14 62 22 62'/%3E%3Cpath d='M68 48 V64 a4 4 0 0 1-4 4 H48'/%3E%3Cpath d='M62 50 C62 58 58 62 50 62'/%3E%3Cpath d='M28 4 H44 M28 68 H44 M4 28 V44 M68 28 V44' stroke-width='0.7'/%3E%3C/g%3E%3C/svg%3E")
    24 / 24px / 0 stretch;
}
```

### 5.8 Engraved small-caps heading (incised, static)
`font-variant-caps` survives tracking better than raw `"smcp"`. The 1px light highlight cuts the
glyph into the cream — the same incised language as the hero numeral. **Large headings / nameplates
on a *solid* ground only** (never body, never over texture/guilloche — it muddies). Hover = color
only.

```css
.engrave-caps{
  font-family: var(--font-caps);
  font-variant-caps: small-caps; font-feature-settings:"smcp" 1,"onum" 0;
  letter-spacing:.08em; word-spacing:.04em;
  color: var(--tinta-sepia);
  text-shadow: 0 1px 0 rgba(255,255,255,.55);          /* incised into cream */
}
.on-green .engrave-caps{ color: var(--marfil); text-shadow: 0 -1px 0 rgba(0,0,0,.45); }
```

---

## 6. Component overlay mapping (Bootstrap → v3)

> All selectors below already exist in v2's `theme.css`; v3 **re-skins** them. Every contract
> class/id/JS hook is preserved (see `FUNCTIONAL_CONTRACT.md` §7). No markup is added that the
> JS does not expect; the SVG ornaments above are injected only via the **existing template
> regions** (macros / static wrapper markup), never into JS-swapped innerHTML targets
> (`#map_container`, `#number_info`, `#hundred_container`, `#filtered_list`, `#image`).

**Navbar (`body > .navbar.bg-light`)** — *a quiet engraved nameplate, NOT a loud masthead.*
Ground `--crema-alta`; bottom edge = a graded **double rule** (1.5px `--nogal` over a 1px
`--tinta-sepia` hairline) with a slim **`.guilloche` band** behind it. Brand in `--font-display`
small-caps `--tinta`, tracked `.06em`, optional single **voluta cresting**; no gold clip, no rays,
no halftone. Nav links `--font-caps` small-caps `--tinta-sepia`; hover/active = `--verde-claro` +
2px underline (never hue alone). `#edit_mode_password` = cream field, `--tinta-sepia` 1px border,
min-height 48px.

**Headings** — `--font-display` (§3). `h1` centered, all-caps tracked; its underline becomes the
`.divider` filigree rule (§5.3), **not** the bermellón bar. `.lead` = Lora italic `--tinta-sepia`.

**Buttons (`.btn`)** — `--font-caps` small-caps, tracked, **min-height 48px**, square-ish (4px),
2px rule, **no offset/printed shadow, no skew, no transition movement** (color-only state change).
- Primary save/submit (`.btn-info:not(.btn_number)`, added by JS) → **solid `--verde-botella`**
  fill, `--marfil` text, 1px inset `--verde-claro` rule; hover deepens fill (stays AAA). The one
  "filled" button — quiet, not a GORDO ribbon.
- `.btn-outline-secondary` / `-info` / `-dark` / `-primary` → cream ground, **`--tinta-sepia`
  engraved 2px rule**, `--tinta` text; hover → `--papel-prensa` ground (rule unchanged).
- `.btn-outline-success` / `.btn-success:not(.btn_number)` (capture / login) → cream ground,
  `--verde-claro` rule, `--verde-botella` text; hover → `--verde-botella` fill + `--marfil`.
- Logout `.btn-danger:not(.btn_number)` → **`--nogal` outline**, walnut text; hover → `--nogal`
  fill + `--marfil`. (No red — danger is carried by an `×`/wording + value, not a loud hue.)

**Billete forms (`.form-control`, labels)** — cream fields, **1px `--nogal` engraved rule**, 4px,
min-height 48px, `--font-body` ≥18px (raised above any inline 14px via `form .form-control`).
Labels always visible, `--font-caps` small-caps `--tinta`. **Focus** = `--verde-claro` border +
`0 0 0 3px rgba(46,94,58,.25)` halo (replaces the bermellón focus). Errors: `--tinta-sepia` text +
plain Castilian beside the field, 17px. Flash `.alert-info` = cream, `--tinta-sepia` left rule 4px.
Wrap the principal retailer/number form in `.orla` (§5.6) for the engraved cartouche.

**Comment leaves (`.media`) + chart cards (`.card`)** — cream leaf, 1px `--papel-prensa` rule, a
**slim `.guilloche` header band** + a 1px `--tinta-sepia` top hairline (replaces the bermellón→ocre
`.media::before` billete rule). Gravatar reframed as a *sello*: 2px `--tinta-sepia` ring on cream.
`.media-body` Lora 19px `--tinta`; its `h5` `--font-display` `--nogal`. Optionally seat the card in
`.frame-orla` (§5.7) for the signature corner filigree.

**El número héroe (`#current_number`)** — §4. Cream plaque, perforation + verde guilloche ground,
`--tinta` numbering-machine serial; **graded sepia base-rule + single voluta crest** (wrap in
`.cartouche--crest`) instead of the bermellón rule. The page's strongest contrast — and the only
one.

**Perforated chip grid (`.btn_number`)** + status states — base chip §4 (perforation + guilloche +
reserved `--crema-alta` panel + 1px `--papel-prensa` hairline). Status recolors **only**
`background-color`/`color` so the décimo layers survive; meaning is reinforced by an **engraved
corner ornament + the template label**, not hue alone:
- **`.btn-success` — Perfecto / en la colección** → `--verde-botella` fill, `--marfil` numeral,
  `--nogal` border; top-left **engraved corner-mark** (a tiny voluta tick or `.roseta` seal in
  `--verde-claro`). *The complete, inked ticket.*
- **`.btn-warning` — Defectuoso** → `--papel-prensa`/sepia-toned fill, `--tinta` numeral, `--nogal`
  border; a **cut top-right corner** (page shows through) + a fine `--nogal` defect rule. *The
  foxed/flawed sheet.* (Distinct from success by warm-brown vs green **and** the cut corner.)
- **`.btn-secondary` — Falta** → bare `--crema`, **dashed `--nogal-claro` engraved hairline**,
  `--tinta-sepia` numeral, no ornament. *The empty album slot.*
- **`.btn-info` — Faltan datos** → `--papel-prensa` panel, **dotted `--nogal-claro` rule**,
  `--tinta-sepia` numeral + small `?`. *Recorded but incomplete.*
- Sizing `.btn-lg/.btn-md/.btn-sm` (set by `resize_buttons`) and `.group_label` keep their roles;
  chips stay ≥44–48px with ≥8px gaps.

**Filters (`.slider_filter`, `#filter_container`)** — ledger hairlines `rgba(90,62,43,.30)`; slider
track `--nogal-claro→--nogal`; **thumb = a small `--verde-claro` engraved disc** with a 1px
`--nogal` ring (replaces the ochre thumb). Disabled inputs → `--papel-prensa`, dimmed.

**Map frame (`#map_container`)** — *the second engraved orla.* Cream mat with a faint **verde
guilloche ground**, framed by the **triple sepia rule** (§5.6) + **voluta corners** (§5.2) —
replacing v2's ocre poster frame + bermellón hairline + royal-blue plate-mark. `#map` itself keeps
a 1px `--nogal` rule. Leaflet popups → cream *ficha*, 1px `--tinta-sepia` border, `--font-caps`/
`--font-body` text. **Marker-cluster classes (contract):** owned = `--verde-botella` discs on a
faint verde halo; not-owned = **`--tinta-sepia`/umber** discs (NOT royal blue) — quiet, monochrome,
distinguished by value + the marker icon, with `--marfil` tabular counts.

**Photo panel (`#screenshot`, `#image`)** — cream tray with the sepia triple-rule orla + voluta
corners (matches the map). `#image` keeps 1px `--nogal` rule on cream. `.loading` spinner unchanged.

---

## 7. Motion & accessibility (non-negotiable)

- **No motion.** Remove **all** `@keyframes` and the `animation`/movement transitions of v2
  (`lot-turn`, `.destello`, the conic-ray fascia, transition-driven button lifts). Permitted state
  change = a **color** shift on hover/focus only; nothing rotates, pulses, sweeps or draws on.
  Keep `@media (prefers-reduced-motion: reduce)` as a belt-and-braces no-op guard.
- **Focus** (two-tone, reads on cream / green / sepia): `outline:3px solid var(--verde-claro);
  outline-offset:2px; box-shadow:0 0 0 1px var(--crema-alta);` on every interactive element
  (`a, button, .btn, input, select, textarea, .btn_number, .slider_filter`). On the green tile the
  cream halo carries it (8:1); on cream the verde outline carries it (6.4:1).
- **Targets ≥44–48px**, body ≥18px, captions ≥17px, AA everywhere; labels never replaced by
  placeholders; links underlined (`--verde-botella` ink) — meaning never by hue alone.

---

## 8. The single signature move

**One beautifully engraved décimo *orla* around the principal plate** — graded **thick–thin–thin
sepia rules → mirrored voluta-and-acanthus corners → a faint verde guilloche ground** (the
hero número plate; echoed on the map mat and the form cartouche). Everything else stays quiet
paper. The number is the only strong note; the frame is the only flourish. That is the whole show.

---

## 9. What v3 REMOVES from v2 (rejection checklist)

- **Loud inks:** `--bermellon`/`--bermellon-hondo` (red as the dominant ink + primary action +
  focus), `--ocre-oro`/`--mostaza` (litho gold — masthead clip, frames, thumb, focus ring),
  `--azul-real` (royal-blue officialdom/plate-mark/not-owned clusters), `--tinta-registro` (cyan
  registration ghost). → collapsed to **paper + umber ink + one bottle-green accent**.
- **Poster type:** `--font-banner` (Anton masthead shout), `--font-slab` (Alfa Slab "money"
  number), `--font-script` (Yellowtail flourish), `--font-condensed` as the UI voice. → **Cormorant
  Garamond + EB Garamond small-caps + Lora**; Oswald survives only as the chip numeral face.
- **Advertisement devices:** the `.destello` slow-turning halo + `lot-turn` `@keyframes`, the
  navbar conic-ray fascia + halftone screen, `.banderola` notched sales ribbons, `.gordo` /
  `.numero-gordo` prize hype, `.semitono`/`--semitono*` halftone "comic" screens, the
  `.ghost-registro` slipped-plate gimmick, the bermellón `h1::after` / `.media::before` /
  `.card::before` billete bars, the gold `.nameplate` gradient, all printed offset/drop shadows
  and button skew.
- **Energy & wording:** all marketing / tombola / fairground feel; any "GORDO" / prize / luck /
  betting / winning framing ("Que la suerte te acompañe", "+18", "juega con responsabilidad");
  any official/state reference (SELAE, "Sorteos del Estado", Loterías y Apuestas del Estado,
  ministry, organism, official seal).
- **Kept (do not touch):** the warm aged-paper ground; the 70s–80s décimo numeral treatment
  (numbering-machine serial, perforation, verde guilloche ground, reserved panel) on the chip grid
  + hero; full WCAG-AA legibility (≥18px body, ≥44–48px targets, visible focus); and **every**
  load-bearing class/id/JS hook in `FUNCTIONAL_CONTRACT.md`.
```
