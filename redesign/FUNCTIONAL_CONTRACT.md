# LotAlfWeb — Functional Contract (Visual-Redesign Invariants)

This document captures the EXACT functional contract that a purely-visual redesign of
"Los décimos de Ildefonso" (LotAlfWeb Flask app) MUST preserve so that behavior is unchanged.
Anything listed here (element `id`s, `name` attributes, CSS classes referenced by JS, WTForms
fields and their rendered DOM ids, backend routes + the form params they expect, and JS event
hooks / global function names) is load-bearing. You may restyle, restructure layout, swap markup,
change colors/spacing, etc. — but you must NOT rename, remove, or change the contract items below
without also changing the JavaScript / backend that depends on them.

Sources analyzed: `app/routes.py`, `app/forms.py`, `app/static/retailers_utils.js`,
`app/static/statistics_utils.js`, and all of `app/templates/` (`base.html`, `bootstrap_base.html`,
`index.html`, `map.html`, `numbers_collection.html`, `numbers_filters.html`,
`numbers_statistics.html`, `retailers_statistics.html`, `province_select.html`, `wtf.html`).

---

## 0. WTForms → DOM id/name mapping (global rule)

WTForms renders each field with BOTH `id="<fieldname>"` and `name="<fieldname>"`. The
`wtf.quick_form` macro (`wtf.html`) wraps fields in `form method="post" action="" class="form form-horizontal" role="form"` and emits `form.hidden_tag()` (a `csrf_token` hidden input). All
`quick_form` forms are rendered with `form_type='horizontal'`, `horizontal_columns=('sm', 4, 8)`
(`province_select.html` uses `('sm', 3, 6)`). The `<form>` itself has NO `id`. Each form POSTs to
its own page URL (action="").

- `SelectField`/`StringField`/`IntegerField`/etc. → `id` == `name` == field name.
- `SubmitField submit` → `id="submit"`, `name="submit"`. `SubmitField submit_save` → `id="submit_save"`.
- `RadioField owned` → one `<input type="radio" name="owned">` per choice with
  `value="Owned"` and `value="Not owned"` (subfield ids `owned-0`, `owned-1`). JS selects by
  `name=owned` + `value`, NOT by id.

### NumberForm (used by /numbers_collection, /numbers_filters)
Rendered field ids/names: `status`, `origin`, `lot`, `year`, `coin`, `retailer_region`,
`retailer_province`, `retailer_town`, `retailer_number`, `copies`, `submit`, `csrf_token`.
- `status` choices: Perfecto / Defectuoso / Falta (required).
- `origin`, `lot`, `year`, `coin`, `retailer_region` each have a first option `value="Default"`
  ("Selecciona ..."). The JS treats `"Default"` as the empty/placeholder sentinel everywhere.
- `copies` default 1, required.

### PostForm (used by / and /index)
Rendered field ids/names: `name`, `email`, `post`, `submit`, `csrf_token`.

### RetailerForm (used by /retailers_collection)
Rendered field ids/names: `retailer_region`, `retailer_province`, `retailer_town`,
`retailer_number`, `retailer_name`, `retailer_street`, `retailer_street_number`,
`retailer_postal_code`, `retailer_telephone`, `retailer_email`, `retailer_latitude`,
`retailer_longitude`, `owned` (radio), `submit_save`, `csrf_token`.
- NOTE: `number` (the lottery number `IntegerField`) is COMMENTED OUT in `forms.py`, so there is
  no `#number` element in the rendered form. JS still references `$('#number')` (in `load_data`,
  `clear_data`, `set_value_or_default('number', ...)`) — these are currently no-ops. Preserving
  current behavior means it is fine for `#number` to be absent; do NOT add it unless intentional.

---

## 1. Global navbar / auth (base.html — present on every page)

Element ids / hooks:
- `#edit_mode_password` — password input; read by `login()` as `$("#edit_mode_password").val()`.
- `#navbarNav` — Bootstrap collapse target (the `data-target="#navbarNav"` toggler).
- Login button: `onclick="login()"`. Logout button: `onclick="logout()"`.
- Nav links via `url_for`: `index` (Tablón), `numbers_collection`, `retailers_collection`.
- Whether login/logout button shows is driven server-side by `session['logged_in']`.

JS functions (defined inline in base.html):
- `login()` → `$.post('/login', { password: <#edit_mode_password value> })`; on done sets
  `window.location.href = response` (response is the referrer's last path segment → reload page).
- `logout()` → `$.post('/logout', {})`; on done `window.location.href = response`.

Backend:
- `POST /login` — expects form param `password`. If `password == '2Galletas!'` sets
  `session['logged_in']=True`. Returns `request.referrer.split('/')[-1]`.
- `POST /logout` — deletes `session['logged_in']`. Returns referrer last segment.
- `POST /check_login` — returns the literal string `"logged in"` or `"not logged in"`.

base.html also renders flashed messages in `.alert.alert-info` inside `.container-fluid`.

---

## 2. Page: index / "Tablón" (home)

- Route: `GET,POST /` and `GET,POST /index` → `index()`; template `index.html` (extends base.html).
- Form: `PostForm` via `wtf.quick_form`. Submitting POSTs to `/index`; backend inserts a comment
  with `name=form.name.data`, `email=form.email.data`, `comment=form.post.data`, then redirects to
  `index`. Comments rendered server-side (newest first) with a Gravatar identicon per `name`.

Element ids referenced by JS:
- `#submit` — restyled on ready (`addClass('btn-info my-4')`, parent col-sm-12, right-aligned).
- `#container` — toggled `container`/`container-fluid` on window resize (>1200px).
- `#number_info_posts`, `#number_info_form` — reordered on resize (>575px swaps which comes first;
  toggles `.border-right` on `#number_info_posts`).
- `#row` — present (layout row).

Form field ids/names (PostForm): `name`, `email`, `post`, `submit`, `csrf_token`.

JS hooks: `$(document).ready` (submit styling), `$(window).resize` (container + column reorder).
(There is dead CSS targeting `#login-password` with no matching element — not load-bearing.)

---

## 3. Page: retailers_collection ("Colección de administraciones")

- Route: `GET,POST /retailers_collection` → `retailers_collection()`; template
  `retailers_collection.html` (extends base.html; imports `wtf.html`, `map.html`).
- On GET: clears `session['retailer_region'/'retailer_province'/'retailer_town']` and deletes
  `/tmp/image.jpg`.
- On POST (only if `session['logged_in']` and form validates): if `owned == "Owned"` →
  `update_retailer(data)`, else `delete_retailer(data)`. If `/tmp/image.jpg` exists it is
  base64-encoded into `data['image']`. Re-renders the map with a single marker via `create_marker`.

### Form (RetailerForm via quick_form)
Field ids/names: see §0. The `owned` radio uses `name="owned"`, values `"Owned"` / `"Not owned"`.
`submit_save` (id `#submit_save`) is hidden unless logged in.

### Map (map.html `insert_map` macro)
- `#map` — the Leaflet map div (id is hard-required by `L.map('map')`).
- Globals created in the macro's inline script: `my_marker_own`, `my_marker_not`, `var map`,
  and `map.whenReady(on_map_ready)`. Marker icons load `/static/my_marker_own.png` and
  `/static/my_marker_not.png`.
- Server-generated marker JS (`create_marker` in routes.py) builds, per marker:
  `L.marker([lat,lng], {icon: my_marker_own|my_marker_not})` then
  `.on('click', click_on_marker).bindPopup('<region><br><province><br><town><br><retailer_number><br><retailer_name><br><retailer_street><br><retailer_street_number><br><retailer_postal_code><br><retailer_telephone><br><retailer_email><br><number>')`
  and adds it to `markerClusters_True` (owned) or `markerClusters_False` (not owned), then
  `map.addLayer(...)`. **The popup HTML is `<br>`-joined in this EXACT field order — `click_on_marker`
  parses it positionally (indices 0–10). This ordering is a hard contract.**
- Owned clusters use `iconCreateFunction` producing className
  `marker-cluster marker-cluster-owned-{small|medium|large}` (thresholds <10 / <100 / else).
  Not-owned clusters use default `marker-cluster marker-cluster-{small|medium|large}`.

### Element ids used by inline JS
- `#map_container` — replaced wholesale with new map HTML on every `/update_map` response, and with
  a `<img class="loading" src="./static/loading.gif">` spinner while loading.
- `#search_town` — town search input; value sent to `find_town()`.
- `#image` — the `<img>` whose `src` is set to a `data:image/webp;base64,...` photo or
  `./static/alt_image.png`.
- `#screenshot`, `#visualization`, `#screen_button` — webcam capture UI containers; their innerHTML
  is replaced by `change_mode()` / `change_button_mode()`.
- `#start_video_button` — hidden unless logged in.
- Retailer form fields (see §0) — read/written by `load_data`/`clear_data` and change handlers.
- `#number` — referenced but absent (see §0 note).

### Button onclick handlers
- "Mostrar todas" → `load_all_retailers()`; "Mostrar todas en la colección" → `load_all_retailers(true)`.
- "Buscar" (town) → `find_town()`.
- "Iniciar captura" → `enable_video()`; "Echar foto" → `take_screenshot()` (button text/class
  toggled between `.enable_video_button` / `.take_screenshot_button`).

### Inline JS functions (must keep these global names)
- `load_all_retailers(owned=false)` → `$.post('/update_map', {all_retailers:!owned, all_owned_retailers:owned})`.
- `find_town(owned=false)` → `$.post('/update_map', {all_retailers:false, all_owned_retailers:false, retailer_town:<#search_town>})`.
- `on_map_ready(e)` → sets `map_lock=true` (called by `map.whenReady`). `var map_lock` global.
- `load_data(datum)` → fills retailer fields via `set_value_or_default`; sets `owned` radio from
  `datum['number']` (`<NA>` ⇒ Not owned); then `$.post('/load_image', {retailer_region, retailer_province, retailer_town, retailer_number})`
  and sets `#image` src.
- `clear_data()` → empties retailer fields, sets `owned` radio to "Not owned".
- `click_on_marker(e)` → reads `this.getPopup().getContent()`, splits on `<br>` (positional order
  per §3 map), `update_session_multi([...])`, `set_value_or_default('retailer_region', ...)`,
  `load_provinces(...)`, `load_data(...)`. Bound to every marker by server JS.
- `enable_video()`, `take_screenshot()`, `change_mode(mode)`, `change_button_mode(mode)`,
  `handleSuccess(stream)`, `handleError(error)` — webcam → `$.post('/store_image', {image:<dataURL>})`.

### $(document).on('change', ...) bindings
- `#retailer_region` → `update_session('retailer_region', ...)`, `load_provinces(...)`, and
  `$.post('/update_map', {all_retailers:false, retailer_region, retailer_province:null, retailer_town:null, retailer_number:null})`.
- `#retailer_province` → `update_session`, `load_towns`, `$.post('/update_map', {... retailer_province ...})`.
- `#retailer_town` → `update_session`, `$.post('/update_map', {... retailer_province (from #retailer_province) , retailer_town ...})`.
- `#retailer_number` → guarded by `map_lock`; `$.post('/update_map', {... retailer_number, retailer_province, retailer_town ...})`
  then `$.post('/get_retailer_data', {retailer_region, retailer_province, retailer_town, retailer_number})`
  → `load_data(response)` or `clear_data()`.

### CSS classes referenced by JS / server-generated markup (must exist/keep names)
`loading` (spinner img), `screenshot` (image sizing), and the marker-cluster classes:
`marker-cluster`, `marker-cluster-owned-small`, `marker-cluster-owned-medium`,
`marker-cluster-owned-large`, `marker-cluster-small`, `marker-cluster-medium`,
`marker-cluster-large` (and their ` div` descendants). `enable_video_button`,
`take_screenshot_button` are toggled by JS.

### Backend routes used by this page
- `POST /update_map` — params (any subset, sent by the handlers above): `all_retailers`,
  `all_owned_retailers`, `retailer_town`, `retailer_number`, `retailer_region`,
  `retailer_province`. Returns rendered `insert_map(...)` HTML (map + markers script).
- `POST /get_retailer_data` — params `retailer_province`, `retailer_town`, `retailer_number`
  (also receives `retailer_region`). Returns JSON dict of retailer columns, or JSON `null`.
- `POST /load_image` — params `retailer_province`, `retailer_town`, `retailer_number`. Returns the
  base64 webp body string, or `''`.
- `POST /store_image` — param `image` (a `data:image/webp;base64,...` URL). Writes `/tmp/image.jpg`.
- `POST /update_provinces` (via `load_provinces`), `POST /update_towns` (via `load_towns`),
  `POST /update_session`, `POST /check_login` — see §6.

---

## 4. Pages: numbers_collection & numbers_filters ("Colección de números")

Both extend base.html, import `wtf.html`, load `./static/retailers_utils.js`, render the same
`NumberForm`, and share the navbar (links: `numbers_collection`, `numbers_statistics`,
`numbers_filters`), the `#current_number` label, and the `#search_number` search input.

Common element ids:
- `#current_number` — `<label>` holding the 5-digit current number; read/written as TEXT by
  `update_number` (`$("#current_number").text()` / `.text(pad(...,5))`). Initialized from
  `session['current_number']` server-side.
- `#search_number` — search box; `update_number(null,null)` reads it, validates 0–99999, toggles
  `.border-danger`.
- `#number_info` — container whose innerHTML is swapped to the loading spinner during
  `/get_number`, then restored. Holds the NumberForm.
- `#submit` — hidden unless logged in (`/check_login`), restyled on ready.

NumberForm field ids/names: see §0.

Common JS (in `retailers_utils.js`) — global function names that MUST be preserved:
- `pad(num, size)`, `resize_buttons()`, `toTitleCase(str)`, `set_value_or_default(key, value, title)`,
  `update_session(key, value)`, `update_session_multi(keys, values)`,
  `update_number(exp, number)`, `update_colors(number)`, `load_provinces(new_region, selection)`,
  `load_towns(new_province, selection)`, `get_filtered_list()`, `add_filter(name, label)`.
- Globals: `update_number_enabled`, `update_colors_enabled`.

Common `$(document).on('change', ...)` bindings (both pages):
- `#origin`, `#lot`, `#year`, `#coin` → disable their `option[value="Default"]`.
- `#retailer_region` → `update_session('retailer_region', value)` + `load_provinces(value)`.
- `#retailer_province` → `update_session('retailer_province', value)` + `load_towns(value)`.
- `#retailer_town` → `update_session('retailer_town', value)`.

`$(document).ready` (both): `update_colors($("#current_number").text())`, `resize_buttons()`,
`/check_login` → hide `#submit` if not "logged in", submit styling. `$(window).resize` → `resize_buttons()`.

CSS classes referenced by JS (both): `btn_number` (every number button; `resize_buttons` swaps
`btn-lg`/`btn-md`/`btn-sm`), `group_label` (font-size adjusted by `resize_buttons`), `loading`,
and the status-color classes toggled by `update_colors`: `btn-success` (Perfecto), `btn-warning`
(Defectuoso), `btn-secondary` (Falta), `btn-info` (Faltan Datos). `border-danger` on `#search_number`.

### 4a. numbers_collection specifics
- Route: `GET,POST /numbers_collection` → renders `numbers_collection.html`. POST (if logged in &
  valid) → `update_number(session['current_number'], datum)` in DB; `datum` keys equal to
  `'Default'` are dropped (status, origin, lot, year, coin, retailer_region/province/town/number, copies).
- `#hundred_container` — holds the 0–99 grid; its innerHTML is swapped to spinner during
  `update_colors`, then restored.
- Number buttons:
  - Decenas/unidades grid buttons have BOTH `name="button_number_{:02d}"` AND
    `id="button_number_{:02d}"` (00–99). `update_colors` recolors them by id `#button_number_NN`
    (uses `pad(i,2)`).
  - Dec.millar buttons: `name="button_number_{:05d}"`, `onclick="update_number(5, i*10000)"`.
  - Millares: `name="button_number_{:04d}"`, `onclick="update_number(4, i*1000)"`.
  - Centenas: `name="button_number_{:03d}"`, `onclick="update_number(3, i*100)"`.
  - Decenas/unidades: `onclick="update_number(2, i + j*10)"`.
  - Search "Buscar" button: `onclick="update_number(null, null)"`.

### 4b. numbers_filters specifics
- Route: `GET,POST /numbers_filters` → renders `numbers_filters.html`. POST behavior identical to
  numbers_collection (updates current number from the form).
- `#filter_container` — on ready, `add_filter(name,label)` is `prepend`-ed for each of (built bottom-up
  so final visible order top→bottom is): `status`(Estado), `origin`(Origen), `lot`(Sorteo),
  `year`(Año), `coin`(Moneda), `retailer_region`(Comunidad), `retailer_province`(Provincia),
  `retailer_town`(Municipio), `retailer_number`(Número), `copies`(Copias).
- `add_filter(name, label)` HTML produces, per filter row:
  - a range slider `input.slider_filter` with `id="slider_filter_<name>"` and
    `name="slider_filter_<name>"` (min 0, max 1, value 1), and
  - a text input with `id="filter_<name>"` and `name="filter[<name>]"`.
- `#filter_limit` — text/search input (default value "100"); read as the `limit`.
- Filter button: `name="filter_button"`, `onclick="get_filtered_list()"`.
- `#filtered_list` — results container; filled with a spinner then a list of result buttons:
  `<button onclick="update_number(0, <number>)" class="btn_number btn btn-lg btn-secondary ml-1 mb-1" name="button_number_<number>">`.
- `$(document).on('change','.slider_filter', ...)` and the ready loop set `disabled` on the matching
  `#filter_<name>` input when the slider value is 0.
- `get_filtered_list()` builds a `filters` array of `{name, filled:<slider val>, value:<#filter_<name> val>}`
  (only included when slider==0, OR slider!=0 AND the text value is non-empty), then
  `$.post('/get_filtered_numbers', {filters: JSON.stringify(filters), limit})`.

### Backend routes used by the numbers pages
- `POST /get_number` — param `new_number`. Sets `session['current_number']`; returns JSON of the
  number's DB record (read by `update_number`).
- `POST /get_existing_in_hundred` — param `number` (hundred base). Returns JSON list of statuses
  (length 100). Rows with `status=='Perfecto'` but missing data are returned as `"Faltan Datos"`.
- `POST /get_filtered_numbers` — params `filters` (JSON string), `limit`. Returns JSON list of
  matching numbers. (numbers_filters only.)
- `POST /update_provinces`, `POST /update_towns`, `POST /update_session`, `POST /check_login` — §6.

---

## 5. Pages: numbers_statistics & retailers_statistics ("Estadísticas")

Both extend base.html, load jQuery + Chart.js 3.6.2 + chartjs-plugin-datalabels + 
`./static/statistics_utils.js`, register `ChartDataLabels`, and on ready POST to fetch data and draw
charts into `<canvas>` elements selected by `document.getElementById(<id>)`.

`statistics_utils.js` functions (preserve names + signatures):
- `create_pie_chart(data, element, colors, title)` — `element` is a canvas id string.
- `create_bar_chart(data, element, colors, title, vertical=true)` — `element` is a canvas id string;
  bar labels >13 chars are truncated; datalabels hidden below 560px width.

### 5a. numbers_statistics
- Route: `GET,POST /numbers_statistics` → `numbers_statistics.html`.
- Canvas ids (hard-required by the chart calls):
  `graph_numbers_filled`, `graph_numbers_statuses`, `graph_numbers_origins`, `graph_numbers_coins`,
  `graph_numbers_years`, `graph_numbers_regions`, `graph_numbers_provinces`.
- On ready: `$.post('/get_numbers_statistics', {})` → builds the 7 charts. Response JSON keys:
  `numbers_filled` (pie), `numbers_statuses` (pie), `numbers_origins` (pie), `numbers_coins` (pie),
  `numbers_regions` (horizontal bar), `numbers_years` (bar), `numbers_provinces` (bar).

### 5b. retailers_statistics
- Route: `GET,POST /retailers_statistics` → `retailers_statistics.html`.
- Canvas ids: `graph_retailers_filled`, `graph_retailers_with_image`, `graph_retailers_regions`,
  `graph_retailers_provinces`.
- On ready: `$.post('/get_retailers_statistics', {})` → builds 4 charts. Response JSON keys:
  `retailers_filled` (pie), `retailers_with_image` (pie), `retailers_regions` (horizontal bar),
  `retailers_provinces` (bar).

### Backend
- `POST /get_numbers_statistics` — returns JSON dict (keys above).
- `POST /get_retailers_statistics` — returns JSON dict (keys above).

---

## 6. Shared AJAX endpoints (province/town/session cascades)

- `POST /update_provinces` — param `new_region`. Returns JSON list of provinces. Called by
  `load_provinces(new_region, selection)`, which rebuilds `#retailer_province` `<option>`s
  (first option `value="Default"` "Selecciona la provincia"), then optionally selects
  `selection['province']` and chains `load_towns`.
- `POST /update_towns` — param `new_province`. Returns JSON list of towns. Called by
  `load_towns(new_province, selection)`, which rebuilds `#retailer_town` `<option>`s (first option
  `value="Default"` "Selecciona la localidad"), then optionally sets town + `#retailer_number`.
- `POST /update_session` — params `key`, `value`. Stores `session[key]=value`. Used by
  `update_session` / `update_session_multi` to remember region/province/town.
- `POST /check_login` — returns `"logged in"` / `"not logged in"`; gates visibility of `#submit`,
  `#submit_save`, `#start_video_button`.

`load_provinces` also disables `select[name="retailer_region"] option[value="Default"]`;
`load_towns` disables `select[name="retailer_province"] option[value="Default"]`.

---

## 7. Hard invariants checklist (do NOT break)

1. Every WTForms field keeps its `id`==`name`==field-name; `#submit`, `#submit_save` ids; the
   `owned` radio keeps `name="owned"` with values `"Owned"` / `"Not owned"`; `csrf_token` hidden
   input via `form.hidden_tag()`.
2. Marker popup field order (region, province, town, retailer_number, name, street, street_number,
   postal_code, telephone, email, number) joined by `<br>` — parsed positionally by `click_on_marker`.
3. Leaflet map div id `map`; globals `map`, `my_marker_own`, `my_marker_not`, `on_map_ready`,
   `click_on_marker`, `markerClusters_True/False`; cluster CSS class names.
4. Number-button `name="button_number_*"` scheme; the 00–99 buttons ALSO need `id="button_number_NN"`
   for `update_colors`; status color classes `btn-success/btn-warning/btn-secondary/btn-info`;
   sizing classes `btn-lg/btn-md/btn-sm` and `btn_number`/`group_label` for `resize_buttons`.
5. Filter widgets: `slider_filter_<name>` (class `slider_filter`, id+name), `filter_<name>` (id) for
   names status/origin/lot/year/coin/retailer_region/retailer_province/retailer_town/retailer_number/
   copies; `#filter_limit`; `#filtered_list`; `name="filter_button"`.
6. Statistics canvas ids exactly as in §5; chart helper function names/signatures.
7. Container/holder ids used for innerHTML swaps: `#map_container`, `#number_info`,
   `#hundred_container`, `#filtered_list`, `#visualization`, `#screen_button`, `#image`.
8. Inputs read by JS: `#edit_mode_password`, `#search_number`, `#search_town`, `#current_number`
   (a label read via `.text()`).
9. Global JS function names: `login`, `logout`, `update_number`, `update_colors`, `load_provinces`,
   `load_towns`, `update_session`, `update_session_multi`, `get_filtered_list`, `add_filter`,
   `resize_buttons`, `pad`, `toTitleCase`, `set_value_or_default`, `load_all_retailers`, `find_town`,
   `on_map_ready`, `load_data`, `clear_data`, `click_on_marker`, `enable_video`, `take_screenshot`,
   `change_mode`, `change_button_mode`, `handleSuccess`, `handleError`, `create_pie_chart`,
   `create_bar_chart`.
10. The `"Default"` sentinel string is the placeholder/empty value across all selects; the password
    `'2Galletas!'` and the `/login`/`/logout` referrer-redirect contract; spinner image path
    `./static/loading.gif`; image fallbacks `./static/alt_image.png`, marker pngs.
