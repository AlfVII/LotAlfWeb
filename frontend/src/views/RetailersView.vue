<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'
import { useAuth } from '../stores/auth'
import RetailerMap from '../components/RetailerMap.vue'

const auth = useAuth()
const markers = ref([])
const regions = ref([])
const provinces = ref([])
const towns = ref([])
const searchTown = ref('')
const saving = ref(false)
const scanning = ref(false)
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

async function fillFromExtracted(ex) {
  if (!ex) return
  const f = { ...form.value, owned: 'Owned' }
  for (const k of ['retailer_region', 'retailer_province', 'retailer_town', 'retailer_number',
    'retailer_name', 'retailer_street', 'retailer_street_number', 'retailer_postal_code', 'retailer_telephone']) {
    if (ex[k] != null && ex[k] !== '') f[k] = ex[k]
  }
  form.value = f
  if (f.retailer_region && f.retailer_region !== 'Default') {
    try { provinces.value = await api.provinces(f.retailer_region) } catch (e) { /* ignore */ }
  }
  if (f.retailer_province && f.retailer_province !== 'Default') {
    try { towns.value = await api.towns(f.retailer_province) } catch (e) { /* ignore */ }
  }
}

async function scanDecimo() {
  scanning.value = true
  ocrNote.value = ''
  try {
    const { front, back, extracted, ocr_error } = await api.scanDecimo()
    if (front) image.value = 'data:image/jpeg;base64,' + front
    imageBack.value = back ? 'data:image/jpeg;base64,' + back : null
    if (extracted) {
      await fillFromExtracted(extracted)
      ocrNote.value = 'Datos leídos del sello del décimo — revíselos y pulse Guardar.'
    } else {
      ocrNote.value = ocr_error ? `Escaneado (OCR no disponible: ${ocr_error})` : 'Escaneado.'
    }
  } catch (e) { alert(e.message) } finally { scanning.value = false }
}

onMounted(async () => {
  try { regions.value = await api.regions() } catch (e) { regions.value = [] }
  await loadAll(true)
})
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
            <div id="visualization"><img class="screenshot" id="image" :src="image" alt="anverso" /></div>
            <img v-if="imageBack" class="screenshot mt-2" :src="imageBack" alt="reverso" />
            <div id="screen_button" class="mt-2" v-if="auth.isEditor">
              <button class="btn btn-outline-success btn-block" @click="scanDecimo" :disabled="scanning">
                {{ scanning ? 'Escaneando…' : 'Escanear décimo (ambas caras)' }}
              </button>
            </div>
            <div v-if="ocrNote" class="mt-1" style="font-family:var(--font-caps);font-size:13px;color:var(--tinta-sepia)">{{ ocrNote }}</div>
          </div>
        </div>
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
</style>
