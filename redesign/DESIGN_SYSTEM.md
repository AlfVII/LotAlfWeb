# Los décimos de Ildefonso — Design System
### "La Administración de Ildefonso" · `Rótulo · Décimo · Legible`

> The storefront as chrome · the engraved décimo as content · the curator's discipline as law.

This is the canonical visual specification for the LotAlfWeb redesign. It is a **pure CSS skin** (`theme.css`) layered on the existing Flask + Bootstrap 4 (bootstrap-flask) markup. It introduces **no markup-contract changes**: every Bootstrap class name, every WTForms `id`/`name`, every JS hook listed in `redesign/FUNCTIONAL_CONTRACT.md` is preserved and merely re-skinned. Where heritage and legibility conflict, **legibility wins in the function; heritage wins in the finish.**

---

## 1. Concept narrative & heritage rationale

### 1.1 The verdict
A single concept could not carry the whole site, so this is a **merge anchored on Concept 2 (Administración)**.

- **Spine — the Administración (Concept 2):** the one gesture no generic vintage site could fake is the **gold-on-bottle-green illuminated rótulo** of a Spanish lottery shop (Doña Manolita, El Gato Negro, La Bruixa d'Or). It is the most authentically *lotería* mark available, and it solves the "green is only Christmas" problem: green becomes a **year-round structural color** — the lit fascia on top and the baize mat behind a single piece — not a seasonal skin.
- **Content — the engraved décimo (Concept 1):** the collection pieces are the heroes, rendered in the idiom of state security printing — the **número héroe**, the **orla + guilloche** frame, the **sello de lacre**, and the numbers grid framed as *the number the niños de San Ildefonso sing into the bombo*. This pays off the site's own name, "Ildefonso."
- **Governance — the curator's discipline (Concept 3):** one accent metal (**brass**), **oxblood** as the leather-ledger primary action, **baize used strictly as a mat** never a page background, the tightest possible type system, and a build that is a CSS overlay, never a markup rewrite.

### 1.2 The North-Star user
A ~70-year-old Spaniard, a lifelong lottery *player and collector*, who commissioned bespoke walnut cabinetry to house a vast collection and wants to *show it*. His taste is exacting; his eyes and hands are aging. Two co-equal, non-negotiable pillars govern every decision:

1. **It must feel like a treasured heirloom** (heritage, craft, pride).
2. **It must be effortless for older eyes and hands** (accessibility is the foundation, not a layer).

> **The litmus test:** *"Would this look at home as a drawer in his bespoke cabinet — and could he read it and use it without his glasses straining?"* If either answer is no, redesign it.

### 1.3 The kitsch line (read twice)
- **Nostalgia** = the texture of aged paper, the weight of a serif, the bottle-green of a lottery sign, the carmine of a real décimo's number-rule.
- **Kitsch** = cartoon clovers, slot machines, gold coins, glitter, jackpot sirens, "¡FELICIDADES!" banners, confetti.
- If an element would look at home on a souvenir mug, cut it. No casino, no fintech dashboard, no flea market.

### 1.4 The layout metaphor (a two-part heirloom shell)
- **Top — the lit administración fascia:** a bottle-green navbar with gold Cinzel lettering and a brass hairline — the storefront you walk toward.
- **Bottom — the walnut counter/cabinet footer:** deep nogal where Ildefonso keeps his décimos.
- **Between — an aged-cream album page:** engraved décimos on cream stock, centered, generous margins, the collection as heroine and the chrome as showcase.
- **Detail views** mat the single hero piece on **bottle-green baize**, jeweller-tray style, so it sings.

---

## 2. Color palette

All values are locked. Roles and WCAG contrast notes are given for every pairing the UI actually uses. **Body text is always `--tinta` on `--crema` (well past AAA).** Contrast figures are computed against the relevant ground (sRGB, WCAG 2.x relative luminance).

```css
:root{
  /* Reading surfaces — aged paper, never pure white */
  --crema:        #F7F1E3;  /* page + card ground */
  --crema-sombra: #E7D9B4;  /* panel/edge foxing, card shadow, "Faltan Datos" tile */
  --marfil:       #F4F1E6;  /* reversed text on green/walnut */

  /* Ink */
  --tinta:        #1E1A14;  /* body ink on crema */
  --tinta-sepia:  #4A3B2A;  /* captions/microtext, use >=17px */

  /* Structure — fascia + counter */
  --verde-rotulo: #16432C;  /* navbar fascia (lit sign) + hero/detail mat */
  --verde-claro:  #1E5631;  /* guilloche lines, hover-on-green, "owned" accent */
  --nogal:        #3B2A1A;  /* footer/counter, frames, cabinet chrome */
  --nogal-claro:  #5A3E2B;  /* grain, dividers */

  /* The one accent metal — brass */
  --laton:        #B08D2A;  /* hairlines, label-holders, photo-corners, FOCUS ring */
  --laton-claro:  #C9A24B;  /* brass highlight / plate gradient */
  --oro-relieve:  #E6C66B;  /* top-stop for the embossed gold sign lettering ONLY */

  /* Ceremony — carmin (scarce) + oxblood (action) */
  --carmin:       #B01E28;  /* hero numero, wax seal, ticket rule */
  --carmin-hondo: #7C1420;  /* hover/pressed, deep engraving */
  --oxido:        #6E2A22;  /* PRIMARY buttons / ledger tabs / save-confirm */

  /* Officialdom (tertiary, sparse) */
  --azul-estado:  #012169;  /* SELAE/legal footer, map plate-mark frame */
}
```

### 2.1 Contrast table (what is allowed to touch what)

| Foreground | Background | Ratio | WCAG | Allowed use |
|---|---|---|---|---|
| `--tinta` #1E1A14 | `--crema` #F7F1E3 | **≈15.4:1** | AAA | All body text, UI labels, form text — the default |
| `--tinta-sepia` #4A3B2A | `--crema` #F7F1E3 | **≈9.6:1** | AAA | Captions, microtext, metadata chips (keep ≥17px) |
| `--tinta` #1E1A14 | `--crema-sombra` #E7D9B4 | **≈12.4:1** | AAA | Text on panels / "Faltan Datos" tile |
| `--marfil` #F4F1E6 | `--verde-rotulo` #16432C | **≈9.9:1** | AAA | Reversed nav text, baize-mat labels, owned-tile numeral |
| `--oro-relieve` #E6C66B | `--verde-rotulo` #16432C | **≈6.8:1** | AA | Gold sign lettering & short nameplates ONLY (never body) |
| `--marfil` #F4F1E6 | `--nogal` #3B2A1A | **≈12.1:1** | AAA | Footer / cabinet-chrome text |
| `--marfil` #F4F1E6 | `--oxido` #6E2A22 | **≈9.2:1** | AAA | Primary button text (oxblood ledger action) |
| `--marfil` #F4F1E6 | `--verde-claro` #1E5631 | **≈7.6:1** | AAA | Hover-on-green text, owned accent |
| `--marfil` #F4F1E6 | `--azul-estado` #012169 | **≈13.0:1** | AAA | Legal footer / SELAE-style chrome |
| `--carmin` #B01E28 | `--crema` #F7F1E3 | **≈6.1:1** | AA (AAA large) | Hero número, ticket-rule, wax seal — scarce/ceremonial |
| `--laton` #B08D2A | `--crema` #F7F1E3 | **≈2.8:1** | **FAILS text** | Decorative hairlines/fittings ONLY — never text |

### 2.2 Discipline (non-negotiable)
- **Gold-on-green** lives only in the fascia, section nameplates, and short headings — **never body text, never paragraphs, never placeholders.**
- **Brass is accent only** (hairlines, photo-corners, label-holders, focus ring). It is **2.8:1 on cream → it must never carry text.** Brass focus rings are paired with a dark inset (see §6) to guarantee ≥3:1 against any ground.
- **Carmín is emotional and scarce** — the number, the seal, one rule. Not a status color, not a button.
- **Oxblood (`--oxido`) is the only filled primary action color.**
- No casino-red status, no neon, no pure black on pure white, no thin gray-on-gray, no "elegant" low-contrast placeholder text. If it's faint, it fails.
- Never signal meaning by hue alone — pair with text + icon/shape (see §5.6 and §6).

---

## 3. Typography

### 3.1 Google Fonts load
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Playfair+Display:wght@600;700&family=Oswald:wght@600;700&family=Spectral:ital,wght@0,400;0,500;1,400&family=Archivo+Narrow:wght@600&family=EB+Garamond:wght@400&family=Pinyon+Script&display=swap" rel="stylesheet">
```

### 3.2 Type roles, families, sizes

| Role | Font (weight) | Size / leading | Treatment |
|---|---|---|---|
| Illuminated sign + brand "Los décimos de Ildefonso" | **Cinzel** 700 | navbar brand ~28px; H1 `clamp(32px, 5vw, 44px)` | Tracked caps, gold-emboss on green, warm halo |
| Section / ledger titles (nameplates) | **Playfair Display** 600/700 | H2 ~30px · H3 / lead ~24px / 1.3 | Brass-plate or debossed-paper nameplate |
| **Hero número** + grid tile numerals | **Oswald** 600/700, `font-feature-settings:"tnum"` | `#current_number` **`clamp(56px, 9vw, 104px)`**; tile numeral ≥20px / 1.0 | Tabular figures; carmine hero on a ticket-rule |
| Body & UI (workhorse) | **Spectral** 400/500 | **19px / 1.6** (UI labels 500) | The default reading face everywhere |
| Spec rail (serie · fracción · sorteo · año), brass-plate captions | **Archivo Narrow** 600 small caps | **17px min / 1.4** | Condensed functional caps, secondary |
| Legal / condiciones | **EB Garamond** (`font-feature-settings:"smcp"`) | 17px | True small caps; real microprint only as non-informative SVG |
| One signature flourish (footer sello) | **Pinyon Script** | ornament only | Never functional or informative text |

```css
:root{
  --font-sign:   "Cinzel", "Marcellus SC", serif;
  --font-title:  "Playfair Display", "Lora", serif;
  --font-numero: "Oswald", "Saira Condensed", sans-serif;
  --font-body:   "Spectral", "Source Serif 4", Georgia, serif;
  --font-rail:   "Archivo Narrow", "Saira Condensed", sans-serif;
  --font-legal:  "EB Garamond", "Cormorant SC", serif;
  --font-flourish:"Pinyon Script", cursive;
}
body{
  font-family: var(--font-body);
  font-size: 19px;          /* base — never below 17px anywhere */
  line-height: 1.6;
  color: var(--tinta);
  background: var(--crema);
}
h1,h2,h3,.h1,.h2,.h3{ font-family: var(--font-title); color: var(--nogal); }
```

### 3.3 Rules (hard)
- **Nothing readable below 17px** — including captions, footers, legal, form help text. Base body 19px.
- **No all-caps on long strings.** Caps reserved for short labels (nameplates, rail, brand).
- **Minimum weight 400** for body; 500 for UI labels; headings heavier, never thinner.
- **Measure 60–75 characters.** Line-height 1.5–1.7 for body.
- **200% zoom and OS text scaling must not break, clip, or trigger horizontal scroll.**
- **Cinzel and Pinyon** appear only in short ornamental pieces; never set a sentence in them.
- **Tabular figures** (`"tnum"`) on every numeral the collector cares about — they are sacred; render them large and aligned.

---

## 4. Ornament & motif library (the kit)

Seven motifs. Each is buildable in CSS/SVG with no images required. All textures sit **beneath** text and never drop contrast below AA.

### 4.1 Rótulo iluminado (the masthead) — the signature, year-round
Bottle-green fascia, Cinzel gold lettering with a soft *warm halo* (diffuse glow, **not neon**), brass bottom hairline.
```css
.navbar.bg-light{                       /* the global navbar is re-skinned, class kept */
  background: var(--verde-rotulo) !important;
  border-bottom: 2px solid var(--laton);
  box-shadow: 0 2px 0 var(--nogal), 0 6px 18px rgba(0,0,0,.25);
}
.navbar-brand{
  font-family: var(--font-sign);
  font-weight: 700;
  letter-spacing: .06em;
  font-size: 28px;
  color: var(--oro-relieve) !important;
  background: linear-gradient(180deg, var(--oro-relieve), var(--laton));
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 14px rgba(230,198,107,.35);   /* warm halo, diffuse */
}
@media (prefers-reduced-motion: no-preference){
  /* halo is static; nothing pulses or animates */
}
```

### 4.2 Orla + guilloche (engraved frame) — around cards, the map, the tablilla
A **double/triple ruled** engraved frame plus a hypotrochoid guilloche band as an SVG `<pattern>`, single-stroke in `--verde-claro` (or `--carmin` for ceremony).
```css
.orla{
  border: 3px double var(--laton);
  outline: 1px solid var(--nogal-claro);
  outline-offset: 3px;
  background:
    var(--crema)
    /* guilloche band tiled along the top edge */
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='16'><path d='M0 8 C 15 0, 30 16, 45 8 S 75 0, 90 8 105 16 120 8' fill='none' stroke='%231E5631' stroke-width='1'/></svg>")
    top left repeat-x;
}
.orla__corner{ position:absolute; width:22px; height:22px; }   /* inline-SVG brass rosette per corner */
```
Guilloche path = a spirograph/hypotrochoid parametric curve, one stroke color, tiled with `<pattern>`. The same curve with rotational symmetry = a central rosette around a crest.

### 4.3 Número héroe on a carmín rule
Oswald tabular, large, carmine, sitting on a thin carmine ticket-rule — exactly like a real décimo.
```css
#current_number{                         /* the load-bearing label, class/id kept */
  font-family: var(--font-numero);
  font-weight: 700;
  font-feature-settings: "tnum";
  font-size: clamp(56px, 9vw, 104px);
  line-height: 1;
  color: var(--carmin);
  border-bottom: 3px solid var(--carmin);     /* the ticket-rule */
  padding-bottom: .08em;
  text-shadow: 0 1px 0 rgba(255,255,255,.5), 0 -1px 0 var(--carmin-hondo); /* incised */
}
```

### 4.4 Sello de lacre (wax seal) — a badge, never a button
A carmine SVG roundel for *verificado / edición especial / destacada*. Scarce.
```css
.sello{
  width:64px; height:64px; border-radius:50%;
  background: radial-gradient(circle at 38% 34%, var(--carmin) 0%, var(--carmin-hondo) 70%);
  box-shadow: inset 0 2px 6px rgba(0,0,0,.45), 0 2px 4px rgba(0,0,0,.3);
  color: var(--marfil); display:grid; place-items:center;
}
/* inner crest = inline SVG line-engraving; the seal is a status MARK, not interactive */
```

### 4.5 Brass fittings (single metal)
Hairlines, label-holders/nameplates, **photo-corners** on thumbnails, and the **focus ring**.
```css
.hairline{ border:0; border-top:1px solid var(--laton); opacity:.8; }
.nameplate{                              /* engraved brass-on-walnut section tab */
  font-family: var(--font-rail); font-size:17px; letter-spacing:.08em;
  color: var(--nogal); background: linear-gradient(180deg,var(--laton-claro),var(--laton));
  border-radius:3px; padding:.25em .8em; box-shadow: inset 0 1px 0 rgba(255,255,255,.4);
}
.photo-corner{                           /* mounting-corner on a thumbnail */
  position:absolute; width:18px; height:18px;
  border-top:2px solid var(--laton); border-left:2px solid var(--laton);
}
.photo-corner--tr{ transform:rotate(90deg);} .photo-corner--br{transform:rotate(180deg);} .photo-corner--bl{transform:rotate(270deg);}
```

### 4.6 Aged cream paper
`feTurbulence` grain + radial vignette, `mix-blend-mode:multiply`, always beneath text, never below AA.
```css
body::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  opacity:.05; mix-blend-mode:multiply;
  background:
    radial-gradient(120% 120% at 50% 0%, transparent 60%, var(--crema-sombra) 100%),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
}
/* All real content sits at z-index:1+ so texture never reduces text contrast. */
```

### 4.7 Bombo + bolas de boj
A single-color line icon for *sorteo / estadísticas*; the grid tiles read as boj balls / fichas — "the number the niños sing." Build as flat inline SVG line-engravings in `--tinta` with optional hatch-fill for shading. Always paired with a visible word (icon-only is banned for actions).

---

## 5. Component specs (overlay on Bootstrap 4)

Ship one `theme.css` after Bootstrap. Every selector below targets **existing classes/ids from the live templates** — nothing in the functional contract is renamed.

### 5.1 Navbar / brand (`base.html`, every page)
- `.navbar.bg-light` → green fascia (§4.1). Keep `navbar-expand-lg navbar-light` so the collapse toggler and `#navbarNav` behavior is unchanged.
- `.navbar-brand` → Cinzel gold-emboss (the rótulo).
- `.nav-link` → `--marfil` at AAA on green; active/hover → `--oro-relieve` underline (color + underline, never color alone).
- Login cluster: keep `#edit_mode_password` (250px), the `btn-success` "Identifícate" and `btn-danger` "Salir de modo edición" buttons, and `onclick="login()"/"logout()"`. Re-skin `btn-success` here as a **brass-rimmed cream** action and `btn-danger` as a **muted oxblood** outline (avoid casino-red), keeping class names.
```css
.navbar .nav-link{ color: var(--marfil) !important; font-family: var(--font-rail); font-size:18px; letter-spacing:.04em; }
.navbar .nav-link:hover,.navbar .nav-link.active{ color: var(--oro-relieve) !important; text-decoration: underline; text-underline-offset:4px; }
```

### 5.2 Buttons (`.btn`, `.btn-info`, `.btn-outline-*`)
| Bootstrap class (kept) | Role in app | Re-skin |
|---|---|---|
| `.btn-info` | **primary save/submit** (`#submit`, `#submit_save` get `btn-info` added by JS) | **Oxblood fill** `--oxido`, `--marfil` text (≈9.2:1), brass 1px inner rule. The leather-ledger action. |
| `.btn-outline-secondary` | section nav links (collection pages) | **Brass-rimmed cream**: cream ground, `--laton` 2px border, `--tinta` text; hover → `--crema-sombra`. |
| `.btn-outline-info` | "Mostrar todas…" (retailers) | Brass-rim cream, `--verde-claro` text + bombo icon. |
| `.btn-outline-dark` / `.btn-outline-primary` | search "Buscar" buttons | Walnut-rim cream, `--nogal` text. |
| `.btn-outline-success` | "Iniciar captura"/"Echar foto" | Baize-green rim, `--verde-rotulo` text + camera glyph. |
| `.btn-success` (navbar login) | "Identifícate" | Brass-rimmed cream (see §5.1). |
| `.btn-danger` (navbar logout) | "Salir de modo edición" | Muted oxblood outline, `--oxido` text. |
```css
.btn{ font-family: var(--font-rail); font-size:18px; letter-spacing:.03em;
  min-height:48px; padding:.5rem 1.1rem; border-radius:4px; }
.btn-info{ background: var(--oxido) !important; border-color: var(--carmin-hondo) !important;
  color: var(--marfil) !important; box-shadow: inset 0 0 0 1px var(--laton); }
.btn-info:hover{ background: var(--carmin-hondo) !important; }
.btn-outline-secondary{ background: var(--crema); color: var(--tinta) !important;
  border:2px solid var(--laton); }
.btn-outline-secondary:hover{ background: var(--crema-sombra); color: var(--tinta) !important; }
```
All buttons: **≥48px target, ≥8px apart, text label always present** (icons only ever accompany a word). Visible focus ring per §6.

### 5.3 Forms (`.form-control`, labels, `quick_form` output)
The `quick_form` macro renders `form.form-horizontal` with `.form-row > label.col-form-label + div > .form-control`. Re-skin without touching structure:
```css
.col-form-label, label{ font-family: var(--font-rail); font-size:17px; font-weight:600;
  color: var(--tinta); letter-spacing:.02em; }   /* labels above/aside, always visible — never placeholder-as-label */
.form-control{ font-family: var(--font-body); font-size:18px; min-height:48px;
  color: var(--tinta); background: var(--crema); border:1px solid var(--nogal-claro);
  border-radius:4px; }
.form-control::placeholder{ color: var(--tinta-sepia); opacity:1; }  /* never faint */
.form-control:focus{ border-color: var(--laton); box-shadow: 0 0 0 3px rgba(176,141,42,.45); }
.radio label, .checkbox label{ font-size:18px; }    /* owned radio (Owned/Not owned) kept */
.help-block, .error, p.error{ color: var(--carmin-hondo); font-size:17px; }  /* errors: text + color, plain Spanish */
```
> Note: the live `retailers_collection.html` hard-codes `label/.form-control/.col-form-label` to `14px`. The redesign **must override those inline styles up to ≥17px** (older eyes). Inputs ≥48px tall. Error messages sit next to the field, in plain Castilian, explaining the fix — not just a red border.

### 5.4 Cards / `.media` comment board — the "Tablón" (`index.html`)
The Tablón is a list of `.media` rows (`img.rounded-circle.avatar` + `.media-body > h5 + comment`). Render each as an **engraved cream album leaf** with a brass hairline and photo-corners; the Gravatar identicon becomes a "mounted" portrait.
```css
.media{ background: var(--crema); border:1px solid var(--crema-sombra);
  border-left:3px solid var(--laton); border-radius:4px; padding:1rem 1.25rem;
  box-shadow: 0 1px 0 var(--crema-sombra), 0 6px 14px rgba(59,42,26,.08); position:relative; }
.media .avatar{ border:2px solid var(--laton); }          /* brass-framed portrait */
.media-body h5{ font-family: var(--font-title); color: var(--nogal); font-weight:600; }
.media-body{ font-family: var(--font-body); font-size:19px; color: var(--tinta); }
```
Section heads ("Últimos comentarios") use the Playfair nameplate. The PostForm (`name/email/post/submit`) follows §5.3; `#submit` keeps its JS-added `btn-info` and right-alignment. The `index.html` resize JS (`#container`, `#number_info_posts`, `#number_info_form`, `.border-right`) is untouched — re-skin `.border-right`/`.border-secondary` as a hairline `--nogal-claro` rule.

### 5.5 The numbers grid — collectible décimo chips (`numbers_collection.html`, `numbers_filters.html`)
The heart of the site. The four rails (`Dec. millar`, `Millares`, `Centenas`, `Decenas y unidades`) and the filter results are `.btn_number.btn` buttons; the 00–99 grid buttons also carry `id="button_number_NN"` (read by `update_colors`). `resize_buttons()` swaps `btn-lg/btn-md/btn-sm`; `.group_label` font-size is JS-adjusted. **All of this is preserved.**

Render each chip as a **boj ball / drawer-front ficha** — Oswald tabular numeral, tactile, on a strict grid.
```css
.btn_number{ font-family: var(--font-numero); font-weight:700; font-feature-settings:"tnum";
  min-width:48px; min-height:48px; border-radius:6px; color: var(--tinta);
  background: var(--crema); border:1px solid var(--nogal-claro);
  box-shadow: 0 1px 0 rgba(0,0,0,.15); }
.btn_number.btn-lg{ font-size:22px; min-height:52px; }
.group_label{ font-family: var(--font-rail); font-size:17px; color: var(--nogal);
  letter-spacing:.06em; }
.btn-group > .btn_number, .btn-group-vertical > .btn_number{ margin:0 8px 8px 0; } /* ≥8px apart */
```

#### 5.5.1 Status colors — load-bearing, hue + shape + icon + label
`update_colors` recolors tiles by **exactly these four Bootstrap classes** (must keep names). Because four reskinned earth-tones blur for older eyes, **each state carries a shape/icon + accessible label, not hue alone:**

| Class (kept) | Meaning | Fill | Numeral | Shape / icon signal | `aria-label` |
|---|---|---|---|---|---|
| `.btn-success` | **Perfecto** (owned, perfect) | baize `--verde-rotulo` | `--marfil` (≈9.9:1) | filled tile + **brass photo-corners** + **wax-seal dot** | "Perfecto" |
| `.btn-warning` | **Defectuoso** (owned, defective) | brass `--laton` | `--tinta` (≈5.5:1) | filled tile + **notched/cut top-right corner** (defect mark) | "Defectuoso" |
| `.btn-secondary` | **Falta** (missing) | bare `--crema` | `--tinta-sepia` | **empty outline corners**, no seal | "Falta" |
| `.btn-info` | **Faltan Datos** (owned, data missing) | `--crema-sombra` | `--tinta-sepia` (≈7.7:1) | **dotted border** + small "?" glyph | "Faltan datos" |

```css
.btn_number.btn-success{ background: var(--verde-rotulo); color: var(--marfil); border-color: var(--nogal); }
.btn_number.btn-warning{ background: var(--laton);        color: var(--tinta);  border-color: var(--nogal-claro);
  clip-path: polygon(0 0, 85% 0, 100% 18%, 100% 100%, 0 100%); }   /* corner notch = defect */
.btn_number.btn-secondary{ background: var(--crema);      color: var(--tinta-sepia); border:1px dashed var(--nogal-claro); }
.btn_number.btn-info{ background: var(--crema-sombra);    color: var(--tinta-sepia); border:2px dotted var(--nogal-claro); }
```
> Note: in `update_colors` these classes are added/removed by `id` (`#button_number_NN`). The reskin is class-based, so it tracks the JS automatically. The owned states (success/warning) get photo-corners + seal injected via `::before/::after` so ownership reads at a glance even in grayscale.

`#hundred_container`, `#number_info`, `#filtered_list` innerHTML swaps to the `img.loading` spinner — re-skin `.loading` (keep the class + `./static/loading.gif`) centered, no change to size logic.

#### 5.5.2 Filters (`numbers_filters.html`)
`add_filter(name,label)` rows = a `.slider_filter` (`#slider_filter_<name>`) + `#filter_<name>` text input; `#filter_limit`; `name="filter_button"` button; results into `#filtered_list`. Re-skin the slider thumb/track in brass-on-walnut, the row as a ledger line (`--crema` with a `--nogal-claro` rule), label in Archivo Narrow ≥17px. Disabled state (slider==0) → reduce opacity to .55 with a "off" text cue, not color alone. Result buttons keep `class="btn_number btn btn-lg btn-secondary"`.

### 5.6 Leaflet map frame + marker-cluster palette (`map.html`, `retailers_collection.html`)
Keep `#map`, `#map_container`, the `insert_map` macro, the globals, the `<br>`-joined popup order, and **all marker-cluster class names**. Frame the map as a **baize mat in a brass plate-frame** (jeweller-tray); the `azul-estado` plate-mark echoes the official register.
```css
#map_container{ padding:10px; background: var(--verde-rotulo);   /* baize mat */
  border:3px solid var(--laton); outline:1px solid var(--azul-estado); outline-offset:4px; border-radius:4px; }
#map{ border:1px solid var(--nogal); }
```
**Marker-cluster recolor — owned = brass/green, not-owned = state-blue (kept class names, hue + still distinguishable by the owned/not marker PNGs):**
```css
/* owned clusters → warm brass→green, reads as "in the collection" */
.marker-cluster-owned-small  { background: rgba(176,141,42,.35) !important; }
.marker-cluster-owned-small  div{ background: rgba(30,86,49,.85) !important; color:var(--marfil); }
.marker-cluster-owned-medium { background: rgba(176,141,42,.45) !important; }
.marker-cluster-owned-medium div{ background: rgba(22,67,44,.88) !important; color:var(--marfil); }
.marker-cluster-owned-large  { background: rgba(176,141,42,.55) !important; }
.marker-cluster-owned-large  div{ background: rgba(22,67,44,.95) !important; color:var(--marfil); }
/* not-owned clusters → sober state-blue */
.marker-cluster-small  { background: rgba(1,33,105,.30) !important; }
.marker-cluster-small  div{ background: rgba(1,33,105,.75) !important; color:var(--marfil); }
.marker-cluster-medium { background: rgba(1,33,105,.40) !important; }
.marker-cluster-medium div{ background: rgba(1,33,105,.85) !important; color:var(--marfil); }
.marker-cluster-large  { background: rgba(1,33,105,.50) !important; }
.marker-cluster-large  div{ background: rgba(1,33,105,.95) !important; color:var(--marfil); }
```
Marker icons `my_marker_own.png` / `my_marker_not.png` are kept (a shape/icon distinction beyond hue). Popups (`<br>` positional order) re-skinned as a small cream "ficha" with Archivo Narrow rail labels.

### 5.7 Photo / screenshot panel (`retailers_collection.html`)
Keep `#screenshot`, `#visualization`, `#image`, `#screen_button`, `#start_video_button`, `.screenshot`, `.enable_video_button`, `.take_screenshot_button`, and the `change_mode/change_button_mode` innerHTML swaps and `alt_image.png` fallback. Present the photo as a **mounted plate on the baize tray** with brass photo-corners.
```css
#screenshot{ background: var(--verde-rotulo); padding:14px; border:3px solid var(--laton); border-radius:4px; }
#image, .screenshot{ border:1px solid var(--nogal); background: var(--crema); }
.enable_video_button, .take_screenshot_button{ /* inherit .btn-outline-success baize-rim skin */ }
```
Add four `.photo-corner` spans absolutely-positioned over `#visualization` (decorative; no markup contract impact).

### 5.8 Statistics (`numbers_statistics.html`, `retailers_statistics.html`)
Canvas ids and `create_pie_chart` / `create_bar_chart` signatures are untouched. Pass a **heritage chart palette** as the `colors` argument (the functions already accept it):
```js
// engraved palette for Chart.js datasets — order = collection-positive → neutral
const LOT_CHART = ['#16432C','#B08D2A','#6E2A22','#012169','#1E5631','#C9A24B','#4A3B2A','#B01E28'];
```
Datalabels in `--tinta`/`--marfil` per slice; titles in Playfair; legend text ≥17px. No animation beyond a single ≤200ms draw; respect reduced-motion.

### 5.9 Footer / cabinet chrome
The walnut counter. Any footer/legal band → `--nogal` ground, `--marfil` text (≈12:1), a Pinyon Script "Ildefonso" flourish (ornament only), and an `--azul-estado` legal/SELAE-style microline (real text ≥17px; decorative microprint only as non-informative SVG).

---

## 6. Accessibility commitments (these override aesthetics on conflict)

**P0 — foundational, must ship:**
1. **Body ≥19px** (never below 17px anywhere). Line-height 1.5–1.7, measure 60–75 chars. Real, resizable text; **200% zoom / OS scaling never breaks or clips.**
2. **Contrast:** body ink-on-cream **AAA (≥7:1; actual ≈15:1)**; all other meaningful text/UI **AA (≥4.5:1 text, ≥3:1 large text & components).** No brass/gold/gray body text, no faint placeholders.
3. **Targets ≥48px**, ≥8px apart; **text-labeled buttons** (icon-only banned for primary actions); the whole card/chip is clickable, not a tiny link.
4. **Visible focus on every interactive element** — a **3px brass ring with offset, plus a 1px dark inset** to guarantee ≥3:1 on any ground; **never removed or faded.** Focus order follows visual order.
5. **Meaning never by color alone** — status/links/errors pair color with **text + icon/shape/underline** (see the number-grid states §5.5.1).
6. **Minimal motion** (≤200ms drawer slide / fade); **full `prefers-reduced-motion` off-switch**; **zero autoplay, parallax, flashing, confetti.** The user sets the pace.
7. **The collection is the visual hero** — generous space, one piece beautifully framed; the 5-digit `#current_number` is the largest type on the page.

```css
:focus-visible{
  outline: 3px solid var(--laton);
  outline-offset: 2px;
  box-shadow: 0 0 0 1px var(--tinta);   /* dark inset guarantees >=3:1 on cream, green, or walnut */
}
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{ animation:none !important; transition:none !important; scroll-behavior:auto !important; }
}
```

**Forms & errors:** labels always visible above/aside fields (never placeholder-as-label); inputs ≥48px tall; errors in plain Castilian next to the field with how to fix it; generous timeouts; never silently log out mid-task.

**Navigation:** flat, persistent header/footer identical on every page (the contract's nav set: *Tablón · Colección de números · Colección de administraciones*, plus the in-page section buttons); always show "you are here" (active state = color + underline); prominent, accent-tolerant search ("decimo" finds "décimo"; partial number/year matches); one dominant primary action per screen.

**Optional craft touch (P2):** a "modo lectura grande" that bumps base type/spacing further on tired-eye days; a print-friendly "exhibition sheet" for any ticket.

---

## 7. Spanish UI copy tone

Dignified, plain-spoken **Castilian**, spoken **to a peer collector** — never down to an elder, never hype.

- **Voice:** warm, concrete, first-person where the site speaks as Ildefonso ("Colecciono décimos de lotería…"). No exclamation spam, no "¡Oops!", no infantilizing helper-text.
- **Exhibition language:** *Vitrina · Catálogo · En exposición · Colección · Décimo de 1957 · Añadir a la colección.*
- **Existing strings to keep in this register:** "Los décimos de Ildefonso", "Tablón", "Colección de números", "Colección de administraciones", "Estadísticas", "Búsqueda por filtros", "Identifícate para hacer cambios", "Salir de modo edición", "Buscar número", "Buscar localidad", "Mostrar todas en la colección", "Iniciar captura" / "Echar foto", "Últimos comentarios".
- **Status labels (number grid):** *Perfecto · Defectuoso · Falta · Faltan datos* — always rendered as text beside the visual state, never as a bare color.
- **Confirmations & errors:** plain Spanish, concrete, beside the field. Confirm destructive actions explicitly ("¿Quitar este décimo de la colección?") — never irreversible on a single mis-tap.
- **The kitsch ban applies to copy too:** no jackpot/"suerte"-siren language, no banners. Dignified, like a card in a cabinet drawer.

---

## 8. Build notes (how it ships)

- One stylesheet, `theme.css`, loaded **after** `bootstrap.load_css()` (in the `styles`/`head` block of `bootstrap_base.html`), plus the Google Fonts `<link>`.
- **No template markup changes** beyond optional decorative spans (`.photo-corner`, `.orla__corner`, `.sello`) that carry no JS/contract role.
- Override the per-page inline `<style>` blocks that hard-code 14px type (notably `retailers_collection.html`) by loading `theme.css` last and/or raising those rules to ≥17px.
- Everything in `redesign/FUNCTIONAL_CONTRACT.md` — WTForms `id`/`name`s, `#submit`/`#submit_save`, the `owned` radio values, `button_number_*` + `#button_number_NN`, status classes `btn-success/btn-warning/btn-secondary/btn-info`, `btn_number`/`group_label`/`btn-lg|md|sm`, marker-cluster classes, `#map`/`#map_container`, the canvas ids, the spinner/image fallbacks, and all global JS function names — **is preserved and only re-skinned.**

---

### Summary card
**Palette:** crema `#F7F1E3` · crema-sombra `#E7D9B4` · marfil `#F4F1E6` · tinta `#1E1A14` · tinta-sepia `#4A3B2A` · verde-rótulo `#16432C` · verde-claro `#1E5631` · nogal `#3B2A1A` · nogal-claro `#5A3E2B` · latón `#B08D2A` · latón-claro `#C9A24B` · oro-relieve `#E6C66B` · carmín `#B01E28` · carmín-hondo `#7C1420` · óxido `#6E2A22` · azul-estado `#012169`.
**Fonts:** Cinzel (sign/brand) · Playfair Display (titles) · Oswald tabular (número héroe + tiles) · Spectral 19px/1.6 (body) · Archivo Narrow (spec rail) · EB Garamond (legal) · Pinyon Script (one flourish).
**Feel:** `Rótulo · Décimo · Legible`.
