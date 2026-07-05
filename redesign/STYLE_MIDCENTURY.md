# Los décimos de Ildefonso — Style Direction v2 (LOCKED)
### "El Cartel de Ildefonso" · `Anuncio · Décimo · Legible`

> v1 was a 19th-century engraved jeweller's cabinet (Cinzel/Playfair, brass-on-bottle-green, security-print hush).
> **v2 is the beloved mid-century *Sorteo de Navidad* poster** pasted in the administración window — the loud, warm,
> optimistic offset-litho announcement of *the years Ildefonso actually lived through* (born 1955; living memory c. 1960–1990).
> Same heirloom soul, new voice: it now **shouts the good news** the way a 1955–1985 cartel did, while staying calm and
> huge for a 70-year-old's eyes.

This is the canonical art direction for the **v2 reskin**. Like v1 it ships as a **pure CSS overlay** (`theme.css`) on the
existing Flask + Bootstrap 4.6 markup. **No markup contract changes** — every Bootstrap class, every WTForms `id`/`name`,
every JS hook in `redesign/FUNCTIONAL_CONTRACT.md` is preserved and merely re-skinned. Where heritage and legibility
conflict, **legibility wins in the function; the cartel wins in the finish.**

---

## 1. Concept narrative & heritage rationale

### 1.1 The move, in one line
v1 imitated the **décimo** (the engraved ticket: fine lithography, guilloche, carmín rule, brass). v2 imitates the
**cartel** (the *promotional poster*: offset-litho flats, halftone, destellos, the GORDO-scale number, the bombo, the
niños). Per the carteles brief, *décimo ≠ cartel* — the ticket stayed conservative for four decades while the
**graphic-design evolution happened on the poster**. v2 finally lets the site *be the poster*.

### 1.2 The three layers (the governing idea)
Every screen is composed from three honest print registers — never blended into mush:

1. **The loud announcement layer** — *destellos/starburst, the GORDO-scale número, the bombo, coins, the banderola.*
   Reserved for **announcement moments**: the masthead, the home hero, the número héroe, a winning tile. Loud = meaningful.
2. **The always-on period substrate** — *warm cream press-stock, halftone dot screen, the billete double-rule frame,
   a hair of misregistration.* This is the paper everything is printed on. Quiet, ambient, **always beneath text**.
3. **The calm reading body** — *Lora ≥19px on cream, generous leading, warm near-black ink.* The poster shouts; the
   body never does. This is the non-negotiable floor for the 70-year-old.

> If a thing is loud it must be an announcement; if it is texture it must sit under the text; if it is read it must be calm and big.

### 1.3 What carries over from v1 (continuity, not reset)
- **Green stays year-round and structural.** Verde-botella is the administración fascia + the map/photo baize mat — *not*
  a Christmas-only skin. (Solves "green is only Navidad," exactly as v1 argued.)
- **Cream stock, warm ink, never pure #000/#fff.** The aged-paper soul is intact — just a **warmer, more saturated press
  cream** (`#F3E9D2` vs v1 `#F7F1E3`) and a hotter red.
- **The collection is the hero.** One piece, beautifully framed; the número is the largest type on the page.
- **The functional contract is untouched.** Same overlay discipline.

### 1.4 What changes from v1 (the three biggest visual moves)
1. **Carmín jewel → bermellón shout.** The cool oxblood/carmín ceremony of v1 becomes the **warmer red-orange
   *bermellón* (`#CE3526`)** of period offset ink — the signature of the billete rule and the headline. Gold goes from
   *brass fitting* to *flat ochre litho-gold*.
2. **Engraved guilloche → halftone + destellos + misregistration.** The security-print substrate (feTurbulence guilloche,
   double-rule brass) is replaced by the **cartel substrate**: a halftone dot screen, a starburst masthead, and a 1–2px
   registration ghost — *the loupe view of a 1960s poster*.
3. **Quiet engraver's serifs → bold poster gothic + slab.** Cinzel/Playfair/Spectral give way to **Anton** (the
   condensed cartel shout), **Alfa Slab One** (the Clarendon "money" number), **Oswald** (the Alternate-Gothic ticket
   workhorse with tabular figures), **Yellowtail** (the signpainter flourish) over **Lora** (the calm body).

### 1.5 The kitsch line (read twice — it MOVED, it did not disappear)
The whole point of v2 is to walk *toward* the line v1 stayed far from — the joyful announcement — **without falling over it.**
- **Period-true announcement** = flat offset inks knocked back into cream, a real halftone dot, a *destello* haloing the
  número, the word **"Desde 1955"** on a banderola, the bombo as a clean line-badge, **"Que la suerte te acompañe"** typeset
  with dignity.
- **Kitsch (still banned)** = gradients-on-everything, neon, glitter/confetti, casino sirens, cartoon four-leaf clovers,
  slot machines, glossy 3D coins, "¡¡FELICIDADES!!", drop-shadowed WordArt, tiki/diner brush (no Pacifico, no Lobster),
  Western-saloon slab (no Rye as body). **Souvenir-mug test still applies.** Saturated-but-muted, never hot-neon. One
  destello per view, not ambient sparkle.

### 1.6 The North-Star user (unchanged)
A ~70-year-old Spanish lifelong *player and collector* with a bespoke walnut cabinet and aging eyes/hands. Two co-equal
laws: **(1) it must feel like a treasured heirloom; (2) it must be effortless for older eyes and hands.**
**Litmus test:** *"Would this hang framed beside his cabinet as a poster he bought tickets under in 1972 — and can he read
and use it without his glasses straining?"* If either answer is no, redesign it.

---

## 2. Color palette (LOCKED) — period offset-litho inks on warm stock

Muted-but-saturated press inks; **warm near-black ink, never pure black; warm cream, never pure white.** Values are final.

```css
:root{
  /* --- Reading surfaces: warm press stock, never #fff --- */
  --crema:        #F3E9D2;  /* page + card ground (offset cream) */
  --papel-prensa: #E7D8B6;  /* deeper newsprint panel / foxing / "Faltan datos" tile */
  --marfil:       #F6F0E2;  /* reversed text on red/green/blue/walnut */

  /* --- Ink: warm near-black --- */
  --tinta:        #241E16;  /* body ink on cream (~13:1, AAA) */
  --tinta-sepia:  #4A3A28;  /* captions / microtext, use >=17px */

  /* --- The signature: bermellón (warm red-orange) --- */
  --bermellon:      #CE3526;  /* hero red, billete rule, banner, primary action — large only */
  --bermellon-hondo:#9A2419;  /* pressed/hover red, deep engraving, AAA-on-marfil action fill */

  /* --- Litho gold (flat ochre, NOT a metal) --- */
  --ocre-oro:     #C2912C;  /* fascia/banner gold, hairlines, frames (decorative; not body text) */
  --mostaza:      #D9A93B;  /* lighter ochre — halftone-tint base, "Defectuoso" tile fill */

  /* --- Structure: deep green (year-round) + walnut --- */
  --verde-botella:#1A5538;  /* fascia, map/photo baize mat, "Perfecto" tile */
  --verde-claro:  #236B47;  /* green hover / "owned" accent / guilloche-line */
  --nogal:        #3A2A1A;  /* footer/counter, frames, cabinet chrome */

  /* --- Officialdom: royal blue (coolest, sparest) --- */
  --azul-real:    #1C3E7C;  /* SELAE/legal, map plate-mark, not-owned clusters */

  /* --- Decorative only (never text) --- */
  --tinta-registro:#1E9FB0; /* cyan "misregistration ghost" behind a heading */
}
```

### 2.1 Contrast table — what is allowed to touch what (WCAG 2.x, sRGB)

| Foreground | Background | Ratio | WCAG | Allowed use |
|---|---|---|---|---|
| `--tinta` `#241E16` | `--crema` `#F3E9D2` | **≈13:1** | AAA | **All body text, labels, form text — the default** |
| `--tinta-sepia` `#4A3A28` | `--crema` `#F3E9D2` | **≈8.5:1** | AAA | Captions, microtext, metadata (keep ≥17px) |
| `--tinta` `#241E16` | `--papel-prensa` `#E7D8B6` | **≈11:1** | AAA | Text on panels / "Faltan datos" tile |
| `--marfil` `#F6F0E2` | `--verde-botella` `#1A5538` | **≈8.5:1** | AAA | Reversed nav text, baize labels, "Perfecto" numeral |
| `--marfil` `#F6F0E2` | `--bermellon-hondo` `#9A2419` | **≈7.0:1** | AAA | **Primary button text (resting)**, banderola text |
| `--marfil` `#F6F0E2` | `--bermellon` `#CE3526` | **≈4.4:1** | AA (large only) | Loud red button/banner text — **bold ≥19px only** |
| `--marfil` `#F6F0E2` | `--azul-real` `#1C3E7C` | **≈9.5:1** | AAA | Legal/SELAE chrome, map plate-mark labels |
| `--marfil` `#F6F0E2` | `--nogal` `#3A2A1A` | **≈12:1** | AAA | Footer / cabinet-chrome text |
| `--tinta` `#241E16` | `--mostaza` `#D9A93B` | **≈7.6:1** | AAA | "Defectuoso" tile numeral (dark on light gold) |
| `--marfil` `#F6F0E2` | `--verde-claro` `#236B47` | **≈6.5:1** | AA | Hover-on-green, "owned" accent |
| `--bermellon` `#CE3526` | `--crema` `#F3E9D2` | **≈4.6:1** | AA (AAA large) | **Hero número, billete-rule** — large/bold & scarce only |
| `--ocre-oro` `#C2912C` on green | — | **≈3.0:1** | AA large only | Fascia **gold-on-green** display lettering only |
| `--ocre-oro` / `--mostaza` | `--crema` | **<3:1** | **FAILS text** | **Decorative only** — frames, rules, tints — never text on cream |
| `--tinta-registro` `#1E9FB0` | any | — | **n/a** | **Decorative ghost only — never text** |

### 2.2 Colour discipline (non-negotiable)
- **Bermellón is the signature but scarce and large.** It is **4.6:1 on cream → never body text, never small text.**
  Use it for the número, the billete rule, the banner, the primary CTA — and at **≥19px bold** so it always clears AA large.
- **Litho gold (`--ocre-oro`/`--mostaza`) is decorative-only on cream.** It lives as **gold-on-green** fascia lettering,
  frames, hairlines, and halftone tint — **never as text on the cream page.**
- **Green is structural and year-round** (fascia, baize, "Perfecto"). **Blue is officialdom, coolest and sparest.**
- **Meaning is never carried by hue alone** — every status pairs colour with **shape + icon + a visible word** (see §5.6).
- **No pure black on pure white, no faint placeholders, no gold/gray body text.** If it's faint, it fails.

---

## 3. Typography (LOCKED) — the poster voice over a calm body

### 3.1 Google Fonts load (final `@import`)
```css
@import url('https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Anton&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Oswald:wght@400;500;600;700&family=Yellowtail&display=swap');
```
HTML alternative (preconnect for speed):
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Anton&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Oswald:wght@400;500;600;700&family=Yellowtail&display=swap">
```

### 3.2 Type tokens
```css
:root{
  --font-banner:    "Anton", "Oswald", sans-serif;          /* the cartel shout */
  --font-slab:      "Alfa Slab One", "Rockwell", serif;     /* the Clarendon "money" number */
  --font-condensed: "Oswald", "Archivo Narrow", sans-serif; /* Alternate-Gothic ticket workhorse */
  --font-script:    "Yellowtail", "Kaushan Script", cursive;/* signpainter flourish — ornament only */
  --font-body:      "Lora", Georgia, serif;                 /* the calm reading face */
}
body{
  font-family: var(--font-body);
  font-size: 19px;          /* base — never below 18px for read text; 17px floor for microtext */
  line-height: 1.6;
  color: var(--tinta);
  background: var(--crema);
}
```

### 3.3 Role / size table — **body ≥18px everywhere readable**

| Role | Font (weight) | Size / leading | Treatment |
|---|---|---|---|
| **Masthead brand + H1 cartel shout** (`.navbar-brand`, H1) | **Anton** 400 | brand ~30px; H1 `clamp(34px, 6vw, 60px)` / 1.05 | Tracked caps, **short strings only**; gold-on-green or bermellón; halftone + optional registration ghost |
| **Section / ledger titles** (H2, H3) | **Oswald** 600/700 | H2 ~28px · H3 / lead ~22px / 1.25 | Condensed period subhead; tinta/nogal on cream, or marfil on green band |
| **Hero número** (`#current_number`, prize figure) | **Alfa Slab One** 400, `"tnum"` | plaque `clamp(34px, 5.2vw, 58px)`; standalone hero `clamp(56px, 12vw, 104px)` / 0.95 | The Clarendon "value" slab — bermellón on a cream décimo plaque + billete rule. **Scarce, ceremonial.** |
| **Número grid tiles + figures + rail labels** | **Oswald** 500/600/700, `"tnum"` | tile numeral ≥20px / 1.0; rail/label **18px** / 1.4 | Tabular figures so columns of números align like a ticket |
| **Body & UI reading** (the workhorse) | **Lora** 400/500 (+italic) | **19px / 1.6** (UI labels 500) | Default reading face everywhere; ≥18px floor |
| **One brush flourish** (subtitle, footer name) | **Yellowtail** 400 | ornament only, ≥1 short line | The administración "¡suerte!" cursive — **never a sentence, never functional text** |
| **Legal / microtext** | **Oswald** 500 small-caps *or* Lora 400 | **17px min** | Real text only; non-informative microprint as SVG only |

### 3.4 Type rules (hard)
- **Nothing readable below 18px** (microtext/legal floor 17px). Base body 19px.
- **No all-caps on long strings.** Anton caps are for short shouts only (brand, H1, "GORDO", "DESDE 1955").
- **Alfa Slab One is scarce** — a number plus maybe one ceremonial word ("Premio"), never a paragraph, never a row of 100 tiles (use Oswald for the grid — it has real `tnum`).
- **Yellowtail and any script are ornament only** — never an instruction, label, or value.
- **Tabular figures (`"tnum"`) are sacred** on every numeral the collector cares about; render them large and aligned.
- **Measure 60–75 chars; line-height 1.5–1.7.** **200% zoom / OS scaling must never clip or trigger horizontal scroll.**

```css
h1,.h1{ font-family:var(--font-banner); font-weight:400; letter-spacing:.01em;
        font-size:clamp(34px,6vw,60px); line-height:1.05; color:var(--nogal); }
h2,.h2{ font-family:var(--font-condensed); font-weight:700; font-size:28px; color:var(--nogal); letter-spacing:.01em; }
h3,.h3{ font-family:var(--font-condensed); font-weight:600; font-size:22px; color:var(--nogal); }
.lead{ font-family:var(--font-body); font-size:21px; color:var(--tinta-sepia); }
```

---

## 4. Motif kit (LOCKED) — buildable in CSS/SVG, no raster assets

Eleven motifs. All textures sit **beneath** text and **never** drop contrast below AA. All animation is killable by
`prefers-reduced-motion`. (SVG-in-CSS URL-encodes `#` as `%23`.)

### 4.1 Destellos / starburst — the announcement halo (loud layer)
Two flavours; reserve for announcement moments (masthead, hero, número, a winning tile). One per view.
```css
/* (a) conic sunburst behind a headline — cheap, optionally slow-turning */
.destello{ position:relative; isolation:isolate; }
.destello::before{
  content:""; position:absolute; inset:-28%; z-index:-1; pointer-events:none;
  background:repeating-conic-gradient(from 0deg,
    var(--ocre-oro) 0deg 5deg, transparent 5deg 11deg);
  -webkit-mask:radial-gradient(circle, #000 58%, transparent 72%);
          mask:radial-gradient(circle, #000 58%, transparent 72%);
  opacity:.5;
  animation:lot-turn 60s linear infinite;
}
@keyframes lot-turn{ to{ transform:rotate(360deg); } }
@media (prefers-reduced-motion:reduce){ .destello::before{ animation:none; } }
```
```css
/* (b) SVG "explosion" star (alternating rays) as a one-off badge ground */
.anuncio{ background:var(--bermellon)
  url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23D9A93B' d='M50 0 56 30 78 8 62 36 96 30 64 46 100 60 62 56 84 86 54 62 50 100 46 62 16 86 38 56 0 60 36 46 4 30 38 36 22 8 44 30Z'/%3E%3C/svg%3E")
  center/120% no-repeat; }
```

### 4.2 Halftone dot screen — the always-on substrate
```css
.semitono{ position:relative; }
.semitono::after{
  content:""; position:absolute; inset:0; pointer-events:none; z-index:0;
  mix-blend-mode:multiply; opacity:.14;
  background:radial-gradient(var(--tinta) 1px, transparent 1.6px);
  background-size:5px 5px;            /* rotate the host box ~15deg for a true screen angle */
}
/* tint variants for section grounds */
.semitono--rojo::after{ background:radial-gradient(var(--bermellon) 1px, transparent 1.6px); opacity:.10; }
.semitono--oro::after { background:radial-gradient(var(--mostaza)   1px, transparent 1.6px); opacity:.12; }
```
Apply over hero/masthead/section grounds only; **keep map tiles and dense data tables clean.**

### 4.3 Registration ghost — the "slipped plate" (one or two display headings only)
```css
.ghost-registro{ position:relative; }
.ghost-registro::before{
  content:attr(data-ghost); position:absolute; left:2px; top:1px; z-index:-1;
  color:var(--tinta-registro); pointer-events:none; user-select:none;
}
@media (prefers-reduced-motion:reduce){ .ghost-registro::before{ display:none; } }
```
Static, subtle, decorative; the real ink heading sits on top at full contrast.

### 4.4 Dot-gain cream paper (kept from v1, retuned)
```css
body::before{
  content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
  opacity:.9; background-color:var(--crema);
  background-image:
    radial-gradient(140% 120% at 50% -10%, rgba(231,216,182,0) 55%, rgba(231,216,182,.5) 100%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-blend-mode:normal, multiply; background-size:cover, 180px 180px;
}
```

### 4.5 El bombo (wire-cage drum) — line-badge for *sorteo / estadísticas*
```html
<svg viewBox="0 0 64 64" fill="none" stroke="#1A5538" stroke-width="2.2"
     stroke-linecap="round" role="img" aria-label="Bombo de lotería">
  <circle cx="32" cy="30" r="18"/>
  <ellipse cx="32" cy="30" rx="7" ry="18"/><ellipse cx="32" cy="30" rx="14" ry="18"/>
  <line x1="14" y1="30" x2="50" y2="30"/>
  <path d="M14 30 L4 38 M50 30 L60 38"/>
  <g stroke="none" fill="#C2912C">
    <circle cx="30" cy="34" r="3"/><circle cx="37" cy="31" r="3"/>
    <circle cx="28" cy="28" r="3"/><circle cx="34" cy="26" r="2.5"/>
  </g>
</svg>
```
Pure geometry → crisp at 16px; the cage `<g>` may spin on hover (`@keyframes`, off under reduced-motion). Always with a word.

### 4.6 Niños de San Ildefonso (singing the número) — section glyph for "Números cantados / mi colección"
```html
<svg viewBox="0 0 64 64" role="img" aria-label="Niño cantando el número">
  <path fill="#241E16" d="M26 8a8 8 0 1 1 0 16 8 8 0 0 1 0-16Z M16 52c0-10 6-18 16-18s16 8 16 18Z"/>
  <circle cx="29" cy="18" r="2.4" fill="#F3E9D2"/>                <!-- open singing mouth -->
  <g fill="#CE3526"><circle cx="46" cy="22" r="3.2"/><rect x="48.4" y="9" width="2" height="13"/></g>
  <line x1="12" y1="60" x2="52" y2="60" stroke="#C2912C" stroke-width="2"/>  <!-- alambre -->
  <g fill="#1A5538"><circle cx="20" cy="60" r="3"/><circle cx="30" cy="60" r="3"/><circle cx="40" cy="60" r="3"/></g>
</svg>
```

### 4.7 GORDO / número on a destello (loud layer)
```css
.gordo{ font-family:var(--font-banner); font-size:1.4rem; letter-spacing:.05em;
  text-transform:uppercase; color:var(--marfil); background:var(--bermellon);
  padding:.22em .8em; transform:skewX(-6deg); box-shadow:.16em .16em 0 var(--nogal); }
.numero-gordo{ font-family:var(--font-slab); font-size:clamp(56px,12vw,104px); line-height:.95;
  font-feature-settings:"tnum"; font-variant-numeric:tabular-nums; color:var(--bermellon);
  text-shadow:1px 1px 0 var(--mostaza), 3px 3px 0 var(--nogal); }   /* mock litho relief */
```
The número is always a real selectable `<span>`/`<label>`, never an image. Layer over §4.1 for "number-in-a-burst."

### 4.8 Banderola (notched ribbon) — "DESDE 1955", "Sorteo de Navidad", "Que la suerte te acompañe"
```css
.banderola{ display:inline-block; background:var(--bermellon); color:var(--marfil);
  font-family:var(--font-condensed); font-weight:700; font-size:18px; letter-spacing:.06em;
  padding:.35em 1.5em; clip-path:polygon(0 0,100% 0,92% 50%,100% 100%,0 100%,8% 50%); }
.banderola--verde{ background:var(--verde-botella); }
.banderola--oro{ background:var(--ocre-oro); color:var(--nogal); }
```

### 4.9 Billete double-rule frame (the orla) — around cards, the map, the hero panel
```css
.orla{ position:relative; padding:1.2rem; background:var(--crema);
  border:3px solid var(--bermellon); outline:1px solid var(--ocre-oro); outline-offset:4px; }
.orla--verde{ border-color:var(--verde-botella); outline-color:var(--ocre-oro); }
```
For a true poster orla, four absolutely-positioned corner SVG filigrees in `--ocre-oro`.

### 4.10 Coins / duros (sparingly — value/prize only)
```html
<svg viewBox="0 0 48 48" role="img" aria-label="Cinco pesetas">
  <circle cx="24" cy="24" r="22" fill="#C2912C" stroke="#8c6f12" stroke-width="2"/>
  <circle cx="24" cy="24" r="17" fill="none" stroke="#8c6f12" stroke-width="1.5"/>
  <text x="24" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="#5c4a0d"
        font-family="Oswald,sans-serif">5</text>
  <text x="24" y="33" text-anchor="middle" font-size="6.5" letter-spacing=".5" fill="#5c4a0d"
        font-family="Oswald,sans-serif">PTAS</text>
  <circle cx="17" cy="15" r="2" fill="#fff8e1" opacity=".8"/>
</svg>
```
Flat, two-tone, no glossy 3D. Use only where money is the subject (footer flourish, a "premio" badge) — never ambient.

### 4.11 Navidad set (date-gated `.modo-navidad` toggle) — estrella de Belén · campana · acebo
Flat two-colour SVGs (green + gold/bermellón). Toggle a body class by date to swap the §4.1 destello centre for a Belén
star and drop holly into corner orlas. (Same approach as motifs brief §6.)

---

## 5. Component mapping (overlay on existing Bootstrap markup)

Ship one `theme.css` after Bootstrap. Every selector targets **existing classes/ids from the live templates** — nothing in
the functional contract is renamed. (Selectors below are the v2-specific ones; the v1 `theme.css` structure is the
scaffold to evolve.)

### 5.1 Navbar / rótulo — the starburst announcement masthead (`base.html`, every page)
The single biggest move. The lit administración fascia becomes a **Sorteo poster header**: verde-botella ground, an
ocre-oro **destello** behind the brand, a **bermellón billete-rule** at the bottom edge, a halftone tint, the brand in
**Anton**, and a **"DESDE 1955" banderola**.
```css
.navbar.bg-light{
  position:relative; isolation:isolate; overflow:hidden;
  background:var(--verde-botella) !important;
  border-bottom:3px solid var(--ocre-oro);
  box-shadow:0 3px 0 var(--bermellon), 0 8px 20px rgba(0,0,0,.28);   /* the billete rule + lift */
  padding:.55rem 1rem;
}
/* destello behind the masthead, masked + faint, slow (off under reduced-motion) */
body > .navbar.bg-light::before{
  content:""; position:absolute; inset:-40% -10%; z-index:-1; pointer-events:none;
  background:repeating-conic-gradient(from 0deg, rgba(194,145,44,.5) 0deg 5deg, transparent 5deg 11deg);
  -webkit-mask:radial-gradient(60% 140% at 22% 50%, #000 40%, transparent 75%);
          mask:radial-gradient(60% 140% at 22% 50%, #000 40%, transparent 75%);
  animation:lot-turn 90s linear infinite;
}
/* halftone over the green */
body > .navbar.bg-light::after{
  content:""; position:absolute; inset:0; z-index:-1; pointer-events:none;
  mix-blend-mode:multiply; opacity:.10;
  background:radial-gradient(#0c2c1d 1px, transparent 1.6px); background-size:5px 5px;
}
/* brand: the cartel shout in litho-gold-on-green (AA large) */
.navbar-brand{
  font-family:var(--font-banner); font-weight:400; letter-spacing:.05em; font-size:30px; line-height:1.1;
  color:var(--mostaza) !important;
  background:linear-gradient(180deg, var(--mostaza), var(--ocre-oro));
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  text-shadow:0 1px 0 rgba(0,0,0,.35);
}
.navbar .nav-link{ color:var(--marfil) !important; font-family:var(--font-condensed); font-weight:600;
  font-size:19px; letter-spacing:.03em; }
.navbar .nav-link:hover,.navbar .nav-link:focus,.navbar .nav-link.active{
  color:var(--mostaza) !important; text-decoration:underline; text-underline-offset:5px; text-decoration-thickness:2px; }
.navbar #edit_mode_password{ background:var(--crema); border:1px solid var(--ocre-oro); color:var(--tinta); min-height:48px; }
.navbar #edit_mode_password::placeholder{ color:var(--tinta-sepia); opacity:1; }
```
- A **"DESDE 1955" `.banderola`** span is added to the brand cluster (decorative, no JS role). On the **home hero** the
  masthead theme expands to a full cartel: giant Anton H1 over a §4.1 destello, the **bombo + niños** glyphs, the billete
  `.orla`, and the `.banderola` line *"Que la suerte te acompañe"*.
- Keep `navbar-expand-lg navbar-light`, `#navbarNav`, the toggler, `#edit_mode_password`, `login()/logout()` intact.

### 5.2 Buttons (Bootstrap classes kept; re-skinned)
The primary is the **GORDO ribbon button**: bermellón fill, marfil bold ≥19px, a thin gold inner rule, a hard offset
shadow (printed look). Outlines are **billete buttons** (cream + ruled rim).
```css
.btn{ font-family:var(--font-condensed); font-weight:600; font-size:19px; letter-spacing:.03em;
  min-height:48px; padding:.5rem 1.15rem; border-radius:4px; border-width:2px; }

/* PRIMARY save/submit — #submit / #submit_save get .btn-info via JS. Scoped off the grid chip. */
.btn-info:not(.btn_number){
  background:var(--bermellon) !important; border-color:var(--bermellon-hondo) !important;
  color:var(--marfil) !important; box-shadow:inset 0 0 0 1px var(--mostaza), .12em .12em 0 var(--nogal); }
.btn-info:not(.btn_number):hover,.btn-info:not(.btn_number):focus,.btn-info:not(.btn_number):active{
  background:var(--bermellon-hondo) !important; color:var(--marfil) !important; }   /* deepens to AAA 7:1 */

.btn-outline-secondary{ background:var(--crema); color:var(--tinta) !important; border:2px solid var(--ocre-oro); }   /* section nav */
.btn-outline-secondary:hover{ background:var(--papel-prensa) !important; color:var(--tinta) !important; }
.btn-outline-info{ background:var(--crema); color:var(--verde-claro) !important; border:2px solid var(--ocre-oro); }   /* "Mostrar todas" + bombo glyph */
.btn-outline-info:hover{ background:var(--papel-prensa) !important; color:var(--verde-botella) !important; }
.btn-outline-dark,.btn-outline-primary{ background:var(--crema); color:var(--nogal) !important; border:2px solid var(--nogal); }  /* "Buscar" */
.btn-outline-success{ background:var(--crema); color:var(--verde-botella) !important; border:2px solid var(--verde-claro); }      /* capture/photo + camera glyph */
.btn-outline-success:hover{ background:var(--verde-botella) !important; color:var(--marfil) !important; }
.btn-success:not(.btn_number){ background:var(--crema) !important; color:var(--tinta) !important; border:2px solid var(--ocre-oro) !important; }   /* navbar "Identifícate" */
.btn-danger:not(.btn_number){ background:transparent !important; color:var(--bermellon-hondo) !important; border:2px solid var(--bermellon-hondo) !important; } /* navbar "Salir de modo edición" */
.btn-danger:not(.btn_number):hover{ background:var(--bermellon-hondo) !important; color:var(--marfil) !important; }
```
All buttons: **≥48px target, ≥8px apart, text label always present** (icons only ever accompany a word). Focus ring §6.

### 5.3 Forms (`.form-control`, labels, `quick_form` output)
A **billete form**: cream fields, warm ruled borders, bermellón focus, **Oswald labels always visible**, Lora input text.
Overrides the per-page inline **14px** in `retailers_collection.html` up to ≥18px.
```css
.form-control{ font-family:var(--font-body); color:var(--tinta); background:var(--crema);
  border:1px solid var(--nogal); border-radius:4px; min-height:48px; padding:.5rem .75rem; }
.form-control::placeholder{ color:var(--tinta-sepia); opacity:1; }     /* never faint */
.form-control:focus{ border-color:var(--bermellon); box-shadow:0 0 0 3px rgba(206,53,38,.28); }
.col-form-label,label{ font-family:var(--font-condensed); font-weight:600; color:var(--tinta); letter-spacing:.02em; }
form .form-control,.form-horizontal .form-control{ font-size:18px; }   /* raise inline 14px via descendant specificity */
form label,form .col-form-label,.form-horizontal label,.form-horizontal .col-form-label{ font-size:18px; }
.radio label,.checkbox label{ font-size:18px; font-weight:500; }
.help-block,.error,p.error,.invalid-feedback{ color:var(--bermellon-hondo); font-size:17px; font-family:var(--font-body); }
.alert-info{ background:var(--crema); border:1px solid var(--papel-prensa); border-left:4px solid var(--bermellon); color:var(--tinta); }
```
Labels above/aside, **never placeholder-as-label**; inputs ≥48px; errors in plain Castilian beside the field with the fix.

### 5.4 Comment leaves — the "Tablón" (`index.html` `.media` rows)
Each comment is a **participación / shop receipt**: cream leaf, a **bermellón→ocre billete top-rule**, an ocre-oro left
border, the Gravatar reframed as a **sello/stamp** in an ocre ring; a faint halftone on the leaf.
```css
.media{ position:relative; overflow:hidden; background:var(--crema);
  border:1px solid var(--papel-prensa); border-left:3px solid var(--ocre-oro); border-radius:4px;
  padding:1rem 1.25rem; box-shadow:0 1px 0 var(--papel-prensa), 0 6px 14px rgba(58,42,26,.08); }
.media::before{ content:""; position:absolute; left:0; right:0; top:0; height:4px;
  background:linear-gradient(90deg, var(--bermellon) 0 60%, var(--ocre-oro) 60% 100%); }   /* billete rule */
.media .avatar,.media img.rounded-circle{ border:2px solid var(--ocre-oro); background:var(--crema); padding:2px; }
.media-body{ font-family:var(--font-body); font-size:19px; color:var(--tinta); }
.media-body h5{ font-family:var(--font-condensed); font-weight:700; color:var(--nogal); }
```
Section head "Últimos comentarios" uses an Oswald title (optionally a `.banderola--verde`). The `index.html` resize JS
(`#container`, `#number_info_posts/_form`, `.border-right`) is untouched; `.border-right` → warm hairline.

### 5.5 Número héroe (`#current_number`) — a décimo pinned to the poster
The load-bearing label (read via `.text()`) is mounted as a **cream décimo plaque** on the green sub-nav, so the bermellón
**Alfa Slab One** numeral keeps its proper ground (~4.6:1, AA large) even over the fascia, with a billete rule beneath.
```css
#current_number{
  display:inline-block; font-family:var(--font-slab) !important; font-weight:400;
  font-feature-settings:"tnum"; font-variant-numeric:tabular-nums;
  font-size:clamp(34px,5.2vw,58px) !important; line-height:1; letter-spacing:.02em;
  color:var(--bermellon) !important; -webkit-text-fill-color:var(--bermellon);
  background:var(--crema); border:2px solid var(--nogal); border-bottom:5px solid var(--bermellon);   /* billete rule */
  border-radius:4px; padding:.04em .38em .0em; margin:0;
  box-shadow:0 2px 6px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.5); }
```
On a dedicated "winning number" reveal, use `.numero-gordo` (§4.7) over a `.destello` (§4.1) — the classic
number-in-a-burst — with the `.gordo` ribbon label.

### 5.6 Numbers grid — bolas del bombo (`numbers_collection.html`, `numbers_filters.html`)
The heart of the site. The four rails + filter results are `.btn_number.btn`; the 00–99 grid buttons also carry
`id="button_number_NN"` (read by `update_colors`); `resize_buttons()` swaps `btn-lg/md/sm`. **All preserved.** Each chip
reads as a **boj ball / numbered ticket tile** — Oswald tabular numeral, tactile, on a strict grid.
```css
.btn_number{ font-family:var(--font-condensed); font-weight:700; font-feature-settings:"tnum";
  font-variant-numeric:tabular-nums; min-width:48px; min-height:48px; border-radius:6px;
  color:var(--tinta); background:var(--crema); border:1px solid var(--nogal);
  box-shadow:0 1px 0 rgba(0,0,0,.15); position:relative; overflow:visible; }
.btn_number:hover{ background:var(--papel-prensa); }
.btn_number.btn-lg{ font-size:22px; min-height:52px; }
.btn_number.btn-md{ font-size:20px; min-height:48px; }
.btn_number.btn-sm{ font-size:18px; min-height:44px; min-width:44px; }
.btn-group>.btn_number,.btn-group-vertical>.btn_number{ margin:0 8px 8px 0; }     /* ≥8px apart */
.group_label{ font-family:var(--font-condensed); font-weight:600; font-size:18px; color:var(--nogal); letter-spacing:.05em; }
```

#### 5.6.1 Status colours — load-bearing: hue **+ shape + icon + label** (never hue alone)
`update_colors` recolours tiles by these **exact four Bootstrap classes** (names kept). Because four muted earth-tones blur
for older eyes, **each state carries a distinct shape/icon + a visible word.** Bermellón is deliberately **kept out** of the
status set (it stays the scarce hero red).

| Class (kept) | Meaning | Fill | Numeral | Shape / icon signal | Label |
|---|---|---|---|---|---|
| `.btn-success` | **Perfecto** (owned, perfect) | `--verde-botella` (8.5:1) | `--marfil` | filled bola + ocre corner-mark + a tiny **destello spark** ("sung & won") | "Perfecto" |
| `.btn-warning` | **Defectuoso** (owned, defective) | `--mostaza` (7.6:1) | `--tinta` | filled tile + **notched/cut top-right corner** (defect) | "Defectuoso" |
| `.btn-secondary` | **Falta** (missing) | bare `--crema` | `--tinta-sepia` | **dashed outline**, empty slot — no fill, no mark | "Falta" |
| `.btn-info` | **Faltan datos** (owned, data missing) | `--papel-prensa` (11:1) | `--tinta-sepia` | **dotted border** + a small **"?"** glyph | "Faltan datos" |

```css
.btn_number.btn-success{ background:var(--verde-botella) !important; color:var(--marfil) !important; border-color:var(--nogal) !important; }
.btn_number.btn-success::before{ content:""; position:absolute; top:3px; left:3px; width:12px; height:12px;
  border-top:2px solid var(--mostaza); border-left:2px solid var(--mostaza); }                 /* corner-mark */
.btn_number.btn-success::after{ content:""; position:absolute; right:3px; bottom:3px; width:10px; height:10px;
  background:radial-gradient(circle, var(--mostaza) 1px, transparent 1.6px) 0 0/4px 4px; opacity:.9; }  /* destello spark */

.btn_number.btn-warning{ background:var(--mostaza) !important; color:var(--tinta) !important; border-color:var(--nogal) !important; }
.btn_number.btn-warning::after{ content:""; position:absolute; top:-1px; right:-1px;                       /* the defect notch */
  border-style:solid; border-width:0 14px 14px 0; border-color:transparent var(--crema) transparent transparent; }
.btn_number.btn-warning::before{ content:""; position:absolute; top:0; right:0; width:20px; border-top:1px solid var(--nogal);
  transform-origin:top right; transform:rotate(45deg); }

.btn_number.btn-secondary{ background:var(--crema) !important; color:var(--tinta-sepia) !important; border:1px dashed var(--nogal) !important; }
.btn_number.btn-secondary::before,.btn_number.btn-secondary::after{ content:none; }

.btn_number.btn-info{ background:var(--papel-prensa) !important; color:var(--tinta-sepia) !important; border:2px dotted var(--nogal) !important; }
.btn_number.btn-info::after{ content:"?"; position:absolute; top:1px; right:4px; font-family:var(--font-condensed);
  font-size:12px; font-weight:700; color:var(--nogal); line-height:1; }
```
A `.semitono`/`.orla--verde` may wrap the centena panel; the panel title can use the **niños** glyph (§4.6): *"la centena
del número que cantan los niños de San Ildefonso."* Filters (`numbers_filters.html`): ledger rows with an ocre-on-walnut
slider thumb, Oswald labels ≥18px, disabled (slider==0) shown at .55 opacity **with an "off" text cue** (not colour alone).
Result buttons keep `class="btn_number btn btn-lg btn-secondary"`.

### 5.7 Leaflet map frame (`map.html`, `retailers_collection.html`)
The map is **matted as a framed cartel**: verde-botella baize mat, an **ocre-oro poster frame**, a **bermellón hairline**,
and an `--azul-real` plate-mark (officialdom register). All ids, the `insert_map` macro, the `<br>`-joined popup order, and
**all marker-cluster class names** are kept.
```css
#map_container{ padding:10px; background:var(--verde-botella);          /* baize mat */
  border:4px solid var(--ocre-oro); box-shadow:inset 0 0 0 1px var(--bermellon);
  outline:1px solid var(--azul-real); outline-offset:4px; border-radius:4px; position:relative; }
#map{ border:1px solid var(--nogal); border-radius:2px; }
/* popups as a small cream "billete" ficha */
.leaflet-popup-content-wrapper{ background:var(--crema); color:var(--tinta); border:1px solid var(--ocre-oro); border-radius:4px; }
.leaflet-popup-content{ font-family:var(--font-condensed); font-size:18px; line-height:1.45; color:var(--tinta); }
.leaflet-popup-tip{ background:var(--crema); border:1px solid var(--ocre-oro); }
/* clusters: owned = ocre→green ("in the collection"); not-owned = officialdom blue. Two-class selectors outrank inline. */
.marker-cluster.marker-cluster-owned-small  { background:rgba(194,145,44,.35)!important; }
.marker-cluster.marker-cluster-owned-small  div{ background:rgba(26,85,56,.85)!important; color:var(--marfil)!important; }
.marker-cluster.marker-cluster-owned-medium { background:rgba(194,145,44,.45)!important; }
.marker-cluster.marker-cluster-owned-medium div{ background:rgba(26,85,56,.9)!important;  color:var(--marfil)!important; }
.marker-cluster.marker-cluster-owned-large  { background:rgba(194,145,44,.55)!important; }
.marker-cluster.marker-cluster-owned-large  div{ background:rgba(26,85,56,.95)!important; color:var(--marfil)!important; }
.marker-cluster.marker-cluster-small  { background:rgba(28,62,124,.30)!important; }
.marker-cluster.marker-cluster-small  div{ background:rgba(28,62,124,.78)!important; color:var(--marfil)!important; }
.marker-cluster.marker-cluster-medium { background:rgba(28,62,124,.40)!important; }
.marker-cluster.marker-cluster-medium div{ background:rgba(28,62,124,.88)!important; color:var(--marfil)!important; }
.marker-cluster.marker-cluster-large  { background:rgba(28,62,124,.50)!important; }
.marker-cluster.marker-cluster-large  div{ background:rgba(28,62,124,.95)!important; color:var(--marfil)!important; }
.marker-cluster div{ font-family:var(--font-condensed); font-weight:700; font-feature-settings:"tnum"; }
```
`my_marker_own.png` / `my_marker_not.png` are kept (a shape distinction beyond hue). The photo/screenshot panel
(`#screenshot`/`#image`) is the same baize tray, framed in ocre-oro with optional `.photo-corner` spans.

### 5.8 Statistics charts (`numbers_statistics.html`, `retailers_statistics.html`)
Canvas ids and `create_pie_chart`/`create_bar_chart` signatures untouched. Pass the **offset-litho palette** as the
`colors` argument (the functions already accept it). Titles in Oswald, legend ≥18px, datalabels in tinta/marfil, single
≤200ms draw, reduced-motion respected.
```js
const LOT_CHART = ['#1A5538','#C2912C','#CE3526','#1C3E7C','#236B47','#D9A93B','#4A3A28','#9A2419'];
```

### 5.9 Footer / cabinet chrome
Walnut counter kept (`--nogal` ground, `--marfil` text, 12:1), now topped by a **bermellón billete-rule**, a **Yellowtail**
"Los décimos de Ildefonso" flourish (ornament only), a small **duro** coin glyph (§4.10), and an `--azul-real` SELAE-style
legal microline (real text ≥17px).

---

## 6. Accessibility commitments (override aesthetics on conflict)

**P0 — must ship:**
1. **Body ≥18px (base 19px), microtext floor 17px.** Line-height 1.5–1.7, measure 60–75 chars. Real resizable text;
   **200% zoom / OS scaling never clips or scrolls horizontally.**
2. **Contrast:** body ink-on-cream **AAA (~13:1)**; all meaningful text/UI **AA (≥4.5:1 normal, ≥3:1 large & components).**
   **Bermellón and litho-gold are large/decorative only** (bermellón text ≥19px bold; gold never text on cream). No faint
   placeholders, no gold/gray body text.
3. **Targets ≥48px, ≥8px apart; text-labelled buttons** (icon-only banned for actions); whole chip/card clickable.
4. **Visible focus on every interactive element** — a 3px ocre ring with offset + a 1px dark inset (guarantees ≥3:1 on
   cream/green/walnut/red). Never removed or faded; focus order follows visual order.
   ```css
   :focus-visible{ outline:3px solid var(--ocre-oro); outline-offset:2px; box-shadow:0 0 0 1px var(--tinta); }
   ```
5. **Meaning never by colour alone** — status/links/errors pair colour with **text + icon/shape/underline** (§5.6).
6. **Minimal motion** (≤200ms). The destello turn is ≥60s, faint, decorative; the registration ghost is static. A **full
   `prefers-reduced-motion` off-switch** stops all spin/ghost/transition. **Zero autoplay, flashing, parallax, confetti.**
   ```css
   @media (prefers-reduced-motion:reduce){ *,*::before,*::after{ animation:none!important; transition:none!important; } }
   ```
7. **The collection is the visual hero** — one piece framed; `#current_number` is the largest type on its page.

**Forms/errors:** labels always visible (never placeholder-as-label); inputs ≥48px; errors in plain Castilian beside the
field with how to fix; never silently log out mid-task. **Optional P2:** a "modo lectura grande" type/spacing bump; a
print-friendly "cartel de exposición" sheet per ticket.

---

## 7. Spanish UI copy tone
Dignified, plain Castilian, **to a peer collector** — warm, concrete, never down to an elder, never hype. Heritage strings
kept (Tablón, Colección de números, Colección de administraciones, Estadísticas, Identifícate para hacer cambios, etc.).
v2 may add **period-true announcement copy as ornament**: *"Desde 1955"*, *"Que la suerte te acompañe"*, *"Sorteo de
Navidad"* — typeset on banderolas, **never as exclamation spam.** Status labels *Perfecto · Defectuoso · Falta · Faltan
datos* always rendered as text beside the visual state. The kitsch ban applies to copy too: no jackpot/"suerte"-siren
shouting, no "¡¡FELICIDADES!!" banners.

---

## 8. Build notes (how it ships) — LOCKED
- One stylesheet `theme.css`, loaded **after** `bootstrap.load_css()` (in the `styles`/`head` block of
  `bootstrap_base.html`), plus the §3.1 fonts `<link>`/`@import`. Evolve the existing v1 `theme.css` in place.
- **No template markup changes** beyond optional decorative spans (`.banderola`, `.orla`, `.photo-corner`, `.destello`
  wrappers, inline bombo/niños/coin SVGs) that carry **no JS/contract role**.
- Override the per-page inline 14px blocks (notably `retailers_collection.html`) by loading `theme.css` last and raising
  those rules to ≥18px via descendant specificity (§5.3) — no `!important` needed on `#current_number`.
- **Everything in `redesign/FUNCTIONAL_CONTRACT.md` is preserved and only re-skinned:** WTForms `id`/`name`s,
  `#submit`/`#submit_save`, the `owned` radio values, `button_number_*` + `#button_number_NN`, status classes
  `btn-success/btn-warning/btn-secondary/btn-info`, `btn_number`/`group_label`/`btn-lg|md|sm`, marker-cluster classes,
  `#map`/`#map_container`, the canvas ids, the spinner/image fallbacks, and all global JS function names.

---

### Summary card
**Palette:** crema `#F3E9D2` · papel-prensa `#E7D8B6` · marfil `#F6F0E2` · tinta `#241E16` · tinta-sepia `#4A3A28` ·
**bermellón `#CE3526`** · bermellón-hondo `#9A2419` · ocre-oro `#C2912C` · mostaza `#D9A93B` · verde-botella `#1A5538` ·
verde-claro `#236B47` · azul-real `#1C3E7C` · nogal `#3A2A1A` · tinta-registro `#1E9FB0` (decorative cyan).
**Fonts:** **Anton** (masthead/H1 shout) · **Alfa Slab One** (hero número / "premio") · **Oswald** tabular (subheads,
tiles, rails, figures) · **Yellowtail** (one flourish) · **Lora** 19px/1.6 (body).
**Feel:** `Anuncio · Décimo · Legible` — a beloved 1955–1985 *Sorteo de Navidad* cartel you can read without your glasses.
