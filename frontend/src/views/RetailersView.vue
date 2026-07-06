<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { api } from '../api'
import { useAuth } from '../stores/auth'
import RetailerMap from '../components/RetailerMap.vue'

const auth = useAuth()
const markers = ref([])
const showZoom = ref(false)
// Note: the scanner script (tools/scan_duplex.ps1) already rotates both faces to
// upright landscape, so the images arrive correctly oriented — no client-side
// rotation needed here (and the OCR gets upright images too).
const regions = ref([])
const provinces = ref([])
const towns = ref([])
const searchTown = ref('')
const saving = ref(false)
const scanning = ref('')  // '' | 'escaneando' | 'leyendo'
const PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='360' height='250'%3E%3Crect width='360' height='250' fill='%23F4ECD8'/%3E%3Cg fill='none' stroke='%23574231' stroke-width='1'%3E%3Crect x='14' y='14' width='332' height='222'/%3E%3Crect x='20' y='20' width='320' height='210'/%3E%3C/g%3E%3Cg fill='%238A745C' font-family='Georgia,serif' text-anchor='middle'%3E%3Ctext x='180' y='120' font-size='17' letter-spacing='3'%3ESIN FOTOGRAF%C3%8DA%3C/text%3E%3C/g%3E%3C/svg%3E"
const image = ref(PLACEHOLDER)
const imageBack = ref(null)
const ocrNote = ref('')

const form = ref(blank())
function blank() {
  return { retailer_region: 'Default', retailer_province: 'Default', retailer_town: 'Default', retailer_number: '',
           retailer_name: '', retailer_street: '', retailer_street_number: '', retailer_postal_code: '',
           retailer_telephone: '', retailer_email: '', retailer_latitude: '', retailer_longitude: '', owned: 'Not owned' }
}

async function loadAll(owned = false) {
  try { markers.value = await api.retailerMap({ scope: owned ? 'owned' : 'all' }) } catch (e) { markers.value = [] }
}
async function findTown() {
  if (!searchTown.value) return
  try { markers.value = await api.retailerMap({ town: searchTown.value }) } catch (e) { markers.value = [] }
}
async function onRegion() {
  form.value.retailer_province = 'Default'; form.value.retailer_town = 'Default'; towns.value = []
  provinces.value = form.value.retailer_region !== 'Default' ? await api.provinces(form.value.retailer_region) : []
  try { markers.value = await api.retailerMap({ region: form.value.retailer_region }) } catch (e) { /* ignore */ }
}
async function onProvince() {
  form.value.retailer_town = 'Default'
  towns.value = form.value.retailer_province !== 'Default' ? await api.towns(form.value.retailer_province) : []
  try { markers.value = await api.retailerMap({ province: form.value.retailer_province }) } catch (e) { /* ignore */ }
}
async function onTown() {
  try { markers.value = await api.retailerMap({ province: form.value.retailer_province, town: form.value.retailer_town }) } catch (e) { /* ignore */ }
}

async function selectMarker(m) {
  const f = blank()
  f.retailer_region = m.region || 'Default'; f.retailer_province = m.province || 'Default'
  f.retailer_town = m.town || 'Default'; f.retailer_number = m.number ?? ''
  f.retailer_name = m.name || ''; f.retailer_street = m.street || ''
  f.retailer_street_number = m.street_number || ''; f.retailer_postal_code = m.postal_code || ''
  f.retailer_telephone = m.telephone || ''; f.retailer_email = m.email || ''
  f.retailer_latitude = m.lat ?? ''; f.retailer_longitude = m.lng ?? ''
  f.owned = m.owned ? 'Owned' : 'Not owned'
  form.value = f
  if (f.retailer_region !== 'Default') provinces.value = await api.provinces(f.retailer_region)
  if (f.retailer_province !== 'Default') towns.value = await api.towns(f.retailer_province)
  ocrNote.value = ''
  try {
    const { image: img, image_back: back } = await api.retailerImage({ province: f.retailer_province, town: f.retailer_town, number: f.retailer_number })
    image.value = img ? 'data:image/webp;base64,' + img : PLACEHOLDER
    imageBack.value = back ? 'data:image/webp;base64,' + back : null
  } catch (e) { image.value = PLACEHOLDER; imageBack.value = null }
}

async function save() {
  saving.value = true
  try {
    const payload = { ...form.value }
    if (image.value && image.value !== PLACEHOLDER && image.value.includes('base64,'))
      payload.image = image.value.split('base64,')[1]
    if (imageBack.value && imageBack.value.includes('base64,'))
      payload.image_back = imageBack.value.split('base64,')[1]
    await api.saveRetailer(payload)
    ocrNote.value = 'Guardado.'
  } catch (e) { alert(e.message) } finally { saving.value = false }
}

// A <select> only shows a value that exactly matches an option. The OCR returns
// free-text place names, so snap each to the matching dropdown option ignoring
// case and accents (e.g. "navas de san juan" -> "Navas de San Juan").
function snapToOption(value, options) {
  if (!value) return value
  const norm = (s) => s.toString().normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim()
  return options.find((o) => norm(o) === norm(value)) || value
}

async function fillFromExtracted(ex) {
  if (!ex) return
  const f = { ...form.value, owned: 'Owned' }
  for (const k of ['retailer_region', 'retailer_province', 'retailer_town', 'retailer_number',
    'retailer_name', 'retailer_street', 'retailer_street_number', 'retailer_postal_code', 'retailer_telephone']) {
    if (ex[k] != null && ex[k] !== '') f[k] = ex[k]
  }
  // Load the cascading option lists, snapping each field to a real option as we go.
  if (f.retailer_region && f.retailer_region !== 'Default') {
    f.retailer_region = snapToOption(f.retailer_region, regions.value)
    try { provinces.value = await api.provinces(f.retailer_region) } catch (e) { /* ignore */ }
    f.retailer_province = snapToOption(f.retailer_province, provinces.value)
  }
  if (f.retailer_province && f.retailer_province !== 'Default') {
    try { towns.value = await api.towns(f.retailer_province) } catch (e) { /* ignore */ }
    f.retailer_town = snapToOption(f.retailer_town, towns.value)
  }
  form.value = f
}

// Scan only — no LLM, no cost. Just capture both faces and let the user type the
// fields in by hand. The paid button below adds the Claude vision read.
async function scanSolo() {
  ocrNote.value = ''
  try {
    scanning.value = 'escaneando'
    const { front, back } = await api.scanDuplex()
    if (front) image.value = 'data:image/jpeg;base64,' + front
    imageBack.value = back ? 'data:image/jpeg;base64,' + back : null
    ocrNote.value = 'Escaneado (sin IA). Rellene los datos y pulse Guardar.'
  } catch (e) { alert(e.message) } finally { scanning.value = '' }
}

async function scanDecimo() {
  ocrNote.value = ''
  try {
    scanning.value = 'escaneando'
    const { front, back } = await api.scanDuplex()
    scanning.value = 'leyendo'
    const { front: f2, back: b2, extracted, ocr_error } = await api.scanRead({ front, back })
    if (f2) image.value = 'data:image/jpeg;base64,' + f2
    imageBack.value = b2 ? 'data:image/jpeg;base64,' + b2 : null
    if (extracted) {
      await fillFromExtracted(extracted)
      ocrNote.value = 'Datos leídos del sello del décimo — revíselos y pulse Guardar.'
    } else {
      ocrNote.value = ocr_error ? `Escaneado (OCR no disponible: ${ocr_error})` : 'Escaneado.'
    }
  } catch (e) { alert(e.message) } finally { scanning.value = '' }
}

function onKey(e) { if (e.key === 'Escape') showZoom.value = false }
onMounted(async () => {
  window.addEventListener('keydown', onKey)
  try { regions.value = await api.regions() } catch (e) { regions.value = [] }
  await loadAll(true)
})
onUnmounted(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <div class="view">
    <nav class="navbar navbar-expand-lg navbar-light bg-light mx-2 mt-2 subnav">
      <ul class="navbar-nav">
        <li class="nav-item"><button class="btn btn-outline-info mr-2" @click="loadAll(false)">Mostrar todas</button></li>
        <li class="nav-item"><button class="btn btn-outline-info mr-2" @click="loadAll(true)">Mostrar todas en la colección</button></li>
        <li class="nav-item"><router-link class="btn btn-outline-secondary mr-2" to="/estadisticas-administraciones">Estadísticas</router-link></li>
      </ul>
      <form class="form-inline ml-auto" @submit.prevent="findTown">
        <input class="form-control mr-2" type="search" style="max-width:200px" v-model="searchTown" placeholder="Buscar localidad" />
        <button class="btn btn-outline-primary" type="submit">Buscar</button>
      </form>
    </nav>

    <div class="fit-main">
      <div class="row">
        <!-- ficha -->
        <div class="col-lg-3">
          <div class="bg-light p-2 ficha-panel">
            <span class="nameplate d-inline-block mb-2">Ficha de la administración</span>
            <form class="form form-horizontal" @submit.prevent="save">
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Comunidad</label>
                <div class="col-sm-7"><select class="form-control" v-model="form.retailer_region" @change="onRegion"><option value="Default">—</option><option v-for="r in regions" :key="r" :value="r">{{ r }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Provincia</label>
                <div class="col-sm-7"><select class="form-control" v-model="form.retailer_province" @change="onProvince"><option value="Default">—</option><option v-for="p in provinces" :key="p" :value="p">{{ p }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Municipio</label>
                <div class="col-sm-7"><select class="form-control" v-model="form.retailer_town" @change="onTown"><option value="Default">—</option><option v-for="t in towns" :key="t" :value="t">{{ t }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Número</label>
                <div class="col-sm-7"><input class="form-control" v-model="form.retailer_number" /></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Nombre</label>
                <div class="col-sm-7"><input class="form-control" v-model="form.retailer_name" /></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Calle</label>
                <div class="col-sm-7"><input class="form-control" v-model="form.retailer_street" /></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Nº de calle</label>
                <div class="col-sm-7"><input class="form-control" v-model="form.retailer_street_number" /></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Cód. postal</label>
                <div class="col-sm-7"><input class="form-control" v-model="form.retailer_postal_code" /></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Nº teléfono</label>
                <div class="col-sm-7"><input class="form-control" v-model="form.retailer_telephone" /></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-5">Correo elec.</label>
                <div class="col-sm-7"><input class="form-control" v-model="form.retailer_email" /></div></div>
              <div class="form-row mt-3"><div class="col-12 radio">
                <label><input type="radio" name="owned" value="Owned" v-model="form.owned" /> Está en la colección</label>
                <label><input type="radio" name="owned" value="Not owned" v-model="form.owned" /> Falta en la colección</label>
              </div></div>
              <div class="form-row mt-2" v-if="auth.isEditor"><div class="col-12"><button type="submit" class="btn btn-info btn-block" :disabled="saving">Guardar</button></div></div>
            </form>
          </div>
        </div>

        <!-- el mapa -->
        <div class="col-lg-5">
          <div id="map_container"><RetailerMap :markers="markers" @select="selectMarker" /></div>
          <div class="text-center mt-1 map-cap"><span class="engrave-caps" style="font-size:16px;">Las administraciones de España</span></div>
        </div>

        <!-- la estampa -->
        <div class="col-lg-4">
          <div id="screenshot" style="text-align:center;">
            <div id="visualization" class="estampa-slot">
              <img class="screenshot estampa" id="image" :src="image" alt="anverso" @click="showZoom = true" title="Ampliar" />
            </div>
            <div v-if="imageBack" class="estampa-slot mt-2">
              <img class="screenshot estampa" :src="imageBack" alt="reverso" @click="showZoom = true" title="Ampliar" />
            </div>
            <div class="mt-2" v-if="image !== PLACEHOLDER">
              <button class="btn btn-outline-secondary btn-sm" @click="showZoom = true">🔍 Ampliar</button>
            </div>
            <div id="screen_button" class="mt-2" style="display:flex;gap:6px" v-if="auth.isEditor">
              <button class="btn btn-outline-secondary" style="flex:1" @click="scanSolo" :disabled="!!scanning"
                      title="Escanea ambas caras sin leer los datos (gratis)">
                {{ scanning === 'escaneando' ? 'Escaneando…' : 'Escanear (sin IA)' }}
              </button>
              <button class="btn btn-outline-success" style="flex:1" @click="scanDecimo" :disabled="!!scanning"
                      title="Escanea y lee los datos del sello con IA">
                {{ scanning === 'leyendo' ? 'Leyendo…' : scanning === 'escaneando' ? 'Escaneando…' : 'Escanear + leer (IA)' }}
              </button>
            </div>
            <div v-if="ocrNote" class="mt-1" style="font-family:var(--font-caps);font-size:13px;color:var(--tinta-sepia)">{{ ocrNote }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Zoom modal: full-size front + back -->
    <div v-if="showZoom" class="zoom-overlay" @click="showZoom = false">
      <button class="zoom-close" @click.stop="showZoom = false" aria-label="Cerrar">×</button>
      <div class="zoom-body" @click.stop>
        <img class="zoom-img" :src="image" alt="anverso ampliado" />
        <img v-if="imageBack" class="zoom-img" :src="imageBack" alt="reverso ampliado" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.subnav { flex: 0 0 auto; }
.fit-main { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; padding: .45rem .6rem; }
.fit-main > .row { flex: 1 1 auto; min-height: 0; margin: 0; }
.fit-main > .row > [class^="col-"] { height: 100%; display: flex; flex-direction: column; min-height: 0; }
.ficha-panel { flex: 1 1 auto; min-height: 0; overflow: auto; }
.ficha-panel .form-row { margin-top: .22rem; }
.ficha-panel .form-control { min-height: 34px; }
.ficha-panel .col-form-label { padding-top: .2rem; padding-bottom: .2rem; }
#map_container { flex: 1 1 auto; min-height: 0; }
.map-cap { flex: 0 0 auto; }
.radio label { display: block; margin-bottom: .1rem; }
input[type=radio] { accent-color: var(--verde-botella); width: 17px; height: 17px; vertical-align: -2px; }

/* Scanned décimo: fit within the panel instead of rendering at native size */
.estampa-slot { display: flex; justify-content: center; }
.estampa {
  display: block;
  max-width: 100%;
  height: auto;
  max-height: 32vh;      /* keep both faces visible without overflowing the column */
  object-fit: contain;
  cursor: zoom-in;
}

/* Zoom modal */
.zoom-overlay {
  position: fixed; inset: 0; z-index: 1080;
  background: rgba(20, 14, 8, 0.82);
  display: flex; align-items: center; justify-content: center;
  padding: 3vh 2vw; cursor: zoom-out;
}
.zoom-body {
  display: flex; flex-wrap: wrap; gap: 14px;
  align-items: center; justify-content: center;
  max-height: 94vh; overflow: auto; cursor: default;
}
.zoom-img {
  max-width: 46vw; max-height: 90vh;
  height: auto; object-fit: contain;
  border: 1px solid var(--nogal, #574231);
  background: var(--crema, #f4ecd8);
  box-shadow: 0 6px 30px rgba(0,0,0,.5);
}
.zoom-close {
  position: fixed; top: 14px; right: 20px; z-index: 1090;
  width: 44px; height: 44px; border-radius: 50%;
  border: none; background: rgba(255,255,255,.9); color: #333;
  font-size: 28px; line-height: 1; cursor: pointer;
}
@media (max-width: 900px) { .zoom-img { max-width: 92vw; } }
</style>
