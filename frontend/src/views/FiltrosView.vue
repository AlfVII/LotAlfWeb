<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'

const FIELDS = [
  { name: 'status', label: 'Estado' },
  { name: 'origin', label: 'Origen' },
  { name: 'year', label: 'Año' },
  { name: 'coin', label: 'Moneda' },
  { name: 'retailer_region', label: 'Comunidad' },
  { name: 'retailer_province', label: 'Provincia' },
  { name: 'retailer_town', label: 'Municipio' },
  { name: 'retailer_number', label: 'Nº administración' },
  { name: 'copies', label: 'Copias' },
]
// per-field: mode = ''(ignorar) | '0'(sin rellenar) | '1'(contiene)
const rows = ref(FIELDS.map((f) => ({ ...f, mode: '', value: '' })))
const limit = ref('100')
const results = ref([])
const loading = ref(false)
const pad5 = (n) => String(n).padStart(5, '0')

async function run() {
  const filters = []
  for (const r of rows.value) {
    if (r.mode === '0') filters.push({ name: r.name, filled: '0', value: '' })
    else if (r.mode === '1' && r.value !== '') filters.push({ name: r.name, filled: '1', value: r.value })
  }
  loading.value = true
  try { results.value = await api.filtered(filters, limit.value ? parseInt(limit.value, 10) : null) }
  catch (e) { results.value = [] } finally { loading.value = false }
}
onMounted(run)
</script>

<template>
  <div class="view">
    <div class="fit-main">
      <div class="row">
        <!-- filtros -->
        <div class="col-lg-5">
          <div class="bg-light p-2 filt-panel">
            <span class="nameplate d-inline-block mb-2">Buscar en la colección de números</span>
            <div v-for="r in rows" :key="r.name" class="form-row align-items-center filt-row">
              <label class="col-sm-4 col-form-label mb-0">{{ r.label }}</label>
              <div class="col-sm-4"><select class="form-control" v-model="r.mode">
                <option value="">— ignorar —</option><option value="0">Sin rellenar</option><option value="1">Contiene…</option>
              </select></div>
              <div class="col-sm-4"><input class="form-control" v-model="r.value" :disabled="r.mode !== '1'" placeholder="valor" /></div>
            </div>
            <div class="form-row align-items-center mt-2">
              <label class="col-sm-4 col-form-label mb-0">Límite</label>
              <div class="col-sm-4"><input class="form-control" v-model="limit" /></div>
              <div class="col-sm-4"><button class="btn btn-info btn-block" @click="run" :disabled="loading">Filtrar</button></div>
            </div>
          </div>
        </div>

        <!-- resultados -->
        <div class="col-lg-7">
          <div class="orla orla--verde p-3 results">
            <div class="text-center mb-2"><span class="engrave-caps" style="font-size:18px;">{{ results.length }} décimos</span></div>
            <div class="results-scroll">
              <router-link v-for="n in results" :key="n" :to="{ path: '/numeros', query: { n } }"
                class="btn btn_number btn-md m-1">{{ pad5(n) }}</router-link>
              <p v-if="!results.length && !loading" class="text-center" style="color:var(--tinta-sepia)">Sin resultados.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fit-main { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; padding: .45rem .6rem; }
.fit-main > .row { flex: 1 1 auto; min-height: 0; margin: 0; }
.fit-main > .row > [class^="col-"] { height: 100%; display: flex; flex-direction: column; min-height: 0; }
.filt-panel { flex: 1 1 auto; min-height: 0; overflow: auto; }
.filt-row { margin-top: .3rem; }
.filt-panel .form-control { min-height: 36px; }
.results { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }
.results-scroll { flex: 1 1 auto; min-height: 0; overflow: auto; text-align: center; }
.results-scroll .btn_number { min-width: 64px; }
</style>
