<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api'
import { useAuth } from '../stores/auth'
import NumberGrid from '../components/NumberGrid.vue'

const auth = useAuth()
const route = useRoute()
const current = ref(13452)
const search = ref('')
const statuses = ref([])
const regions = ref([])
const provinces = ref([])
const towns = ref([])
const saving = ref(false)
const ORIGINS = ['Default', 'Ordinario', 'Navidad', 'Extraordinario', 'Especial', 'Niño', 'Antiguo', 'Jueves', 'Escrito']
const STATUSES = ['Perfecto', 'Defectuoso', 'Falta']
const COINS = ['Default', 'Euro', 'Peseta']
const lots = Array.from({ length: 102 }, (_, i) => i + 1)
const years = Array.from({ length: new Date().getFullYear() - 1966 }, (_, i) => 1967 + i)

const form = ref(blank())
function blank() {
  return { status: 'Perfecto', origin: 'Default', lot: 'Default', year: 'Default', coin: 'Default',
           retailer_region: 'Default', retailer_province: 'Default', retailer_town: 'Default', retailer_number: '', copies: 1 }
}
const pad5 = (n) => String(n).padStart(5, '0')
const base = computed(() => current.value - (current.value % 100))

async function loadNumber(n) {
  if (isNaN(n) || n < 0 || n > 99999) return
  current.value = n
  try {
    const rec = await api.number(n)
    const f = blank()
    if (rec) {
      for (const k of Object.keys(f)) if (rec[k] != null && rec[k] !== '') f[k] = rec[k]
      if (rec.lot) f.lot = String(rec.lot).split('/')[0]
    }
    form.value = f
    if (f.retailer_region && f.retailer_region !== 'Default') {
      provinces.value = await api.provinces(f.retailer_region)
      if (f.retailer_province && f.retailer_province !== 'Default') towns.value = await api.towns(f.retailer_province)
    }
  } catch (e) { /* keep current form */ }
  await loadHundred()
}
async function loadHundred() {
  try { statuses.value = await api.hundred(base.value) } catch (e) { statuses.value = [] }
}
async function onRegion() {
  form.value.retailer_province = 'Default'; form.value.retailer_town = 'Default'; towns.value = []
  provinces.value = form.value.retailer_region !== 'Default' ? await api.provinces(form.value.retailer_region) : []
}
async function onProvince() {
  form.value.retailer_town = 'Default'
  towns.value = form.value.retailer_province !== 'Default' ? await api.towns(form.value.retailer_province) : []
}
function doSearch() {
  const n = parseInt(search.value, 10)
  if (!isNaN(n) && n >= 0 && n <= 99999) loadNumber(n)
}
async function save() {
  saving.value = true
  try { await api.updateNumber(current.value, { ...form.value }); await loadHundred() }
  catch (e) { alert(e.message) } finally { saving.value = false }
}

onMounted(async () => {
  try { regions.value = await api.regions() } catch (e) { regions.value = [] }
  const qn = parseInt(route.query.n, 10)
  await loadNumber(!isNaN(qn) && qn >= 0 && qn <= 99999 ? qn : current.value)
})
</script>

<template>
  <div class="view">
    <!-- sub-cabezal: secciones + número actual + búsqueda -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light mx-2 mt-2 subnav">
      <ul class="navbar-nav">
        <li class="nav-item"><router-link class="btn btn-outline-secondary mr-2" to="/estadisticas-numeros">Estadísticas</router-link></li>
        <li class="nav-item"><router-link class="btn btn-outline-secondary mr-2" to="/filtros">Filtros</router-link></li>
      </ul>
      <div class="d-flex align-items-center ml-auto">
        <span class="group_label mr-3">Número actual</span>
        <span class="cartouche cartouche--crest d-inline-block mr-4" style="padding-top:20px;">
          <svg class="voluta voluta--tl" style="width:30px;height:30px;top:0;" viewBox="0 0 64 64" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round" d="M2 62 C2 34 14 8 40 4 C26 10 22 24 26 34 C29 41 38 42 42 36 C45 31 41 26 36 28 C40 27 43 31 41 35" /></svg>
          <svg class="voluta voluta--tr" style="width:30px;height:30px;top:0;" viewBox="0 0 64 64" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round" d="M2 62 C2 34 14 8 40 4 C26 10 22 24 26 34 C29 41 38 42 42 36 C45 31 41 26 36 28 C40 27 43 31 41 35" /></svg>
          <label id="current_number" class="mb-0">{{ pad5(current) }}</label>
        </span>
        <input class="form-control mr-2" type="search" style="max-width:160px" v-model="search" @keyup.enter="doSearch" placeholder="Buscar número" />
        <button class="btn btn-outline-primary" type="button" @click="doSearch">Buscar</button>
      </div>
    </nav>

    <div class="fit-main">
      <div class="row">
        <!-- ficha del décimo -->
        <div class="col-lg-4">
          <div class="bg-light p-2 ficha-panel">
            <span class="engrave-caps d-inline-block mb-2" style="font-size:20px;">Ficha del décimo</span>
            <form class="form form-horizontal" @submit.prevent="save">
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Estado</label>
                <div class="col-sm-8"><select class="form-control" v-model="form.status"><option v-for="s in STATUSES" :key="s">{{ s }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Origen</label>
                <div class="col-sm-8"><select class="form-control" v-model="form.origin"><option v-for="o in ORIGINS" :key="o" :value="o">{{ o === 'Default' ? 'Selecciona el origen' : o }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Sorteo</label>
                <div class="col-sm-8"><select class="form-control" v-model="form.lot"><option value="Default">Selecciona el sorteo</option><option v-for="l in lots" :key="l" :value="l">{{ l }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Año</label>
                <div class="col-sm-8"><select class="form-control" v-model="form.year"><option value="Default">Selecciona el año</option><option v-for="y in years" :key="y" :value="y">{{ y }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Moneda</label>
                <div class="col-sm-8"><select class="form-control" v-model="form.coin"><option v-for="c in COINS" :key="c" :value="c">{{ c === 'Default' ? 'Selecciona la moneda' : c }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Comunidad</label>
                <div class="col-sm-8"><select class="form-control" v-model="form.retailer_region" @change="onRegion"><option value="Default">Selecciona la comunidad</option><option v-for="r in regions" :key="r" :value="r">{{ r }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Provincia</label>
                <div class="col-sm-8"><select class="form-control" v-model="form.retailer_province" @change="onProvince"><option value="Default">Selecciona la provincia</option><option v-for="p in provinces" :key="p" :value="p">{{ p }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Municipio</label>
                <div class="col-sm-8"><select class="form-control" v-model="form.retailer_town"><option value="Default">Selecciona la localidad</option><option v-for="t in towns" :key="t" :value="t">{{ t }}</option></select></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Número</label>
                <div class="col-sm-8"><input class="form-control" v-model="form.retailer_number" /></div></div>
              <div class="form-row mt-2"><label class="col-form-label col-sm-4">Copias</label>
                <div class="col-sm-8"><input class="form-control" v-model="form.copies" /></div></div>
              <div class="form-row mt-3" v-if="auth.isEditor"><div class="col-sm-12"><button type="submit" class="btn btn-info btn-block" :disabled="saving">Guardar</button></div></div>
            </form>
          </div>
        </div>

        <!-- la centena -->
        <div class="col-lg-8">
          <div class="orla orla--verde p-4 album">
            <div class="text-center mb-2 album-head">
              <h3 class="mb-0">Centena {{ String(base).slice(0, 3) }}<span style="color:var(--tinta-sepia)">00</span> – {{ String(base).slice(0, 3) }}<span style="color:var(--tinta-sepia)">99</span></h3>
            </div>
            <NumberGrid :base="base" :statuses="statuses" @select="loadNumber" />
            <hr class="hairline my-2" />
            <div class="album-legend d-flex flex-wrap justify-content-center" style="gap:1.2rem; font-family:var(--font-caps); font-size:16px;">
              <span><span class="btn btn_number btn-success legend-chip mr-2">07</span>Perfecto</span>
              <span><span class="btn btn_number btn-warning legend-chip mr-2">14</span>Defectuoso</span>
              <span><span class="btn btn_number btn-secondary legend-chip mr-2">21</span>Falta</span>
              <span><span class="btn btn_number btn-info legend-chip mr-2">35</span>Faltan datos</span>
            </div>
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
.ficha-panel .form-row { margin-top: .28rem; }
.ficha-panel .form-control { min-height: 36px; }
.ficha-panel .col-form-label { padding-top: .25rem; padding-bottom: .25rem; }
.album { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; padding: .7rem 1rem; }
.album-head, .album-legend { flex: 0 0 auto; }
.album-head :deep(h3) { font-size: 21px; }
.legend-chip { width: 40px; height: 34px; display: inline-grid; place-items: center; }
</style>
