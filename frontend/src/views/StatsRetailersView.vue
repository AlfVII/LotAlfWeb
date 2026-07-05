<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'
import StatChart from '../components/StatChart.vue'

const d = ref(null)
const error = ref('')
const fmt = (n) => (n ?? 0).toLocaleString('es-ES')
const owned = computed(() => d.value?.retailers_filled?.Rellenados ?? 0)
const total = computed(() => d.value?.retailers_filled?.['Por rellenar'] ?? 0)
const withImg = computed(() => d.value?.retailers_with_image?.['Con imagen'] ?? 0)
onMounted(async () => {
  try { d.value = await api.statsRetailers() } catch (e) { error.value = e.message }
})
</script>

<template>
  <div class="view">
    <div class="fit-main">
      <div class="stats-head text-center mb-1">
        <h2 class="mb-0">Estado de la colección de administraciones</h2>
        <svg class="divider" viewBox="0 0 200 14" width="200" height="14" role="presentation">
          <g fill="none" stroke="currentColor" stroke-width="0.8"><line x1="0" y1="7" x2="80" y2="7" /><line x1="120" y1="7" x2="200" y2="7" />
            <path d="M80 7 C88 7 92 2 98 4 C104 6 101 11 95 10 M120 7 C112 7 108 2 102 4 C96 6 99 11 105 10" /></g><circle cx="100" cy="7" r="1.5" fill="currentColor" />
        </svg>
      </div>

      <p v-if="error" class="text-center" style="color:var(--bermellon-hondo,#7C1420)">{{ error }}</p>

      <template v-if="d">
        <div class="row stats-row">
          <div class="col-md-4"><div class="card"><div class="card-body"><div class="chart-cap">Conseguidas</div>
            <div class="chart-box"><StatChart type="pie" :data="{ Conseguidas: owned, 'Por conseguir': Math.max(total - owned, 0) }" /></div></div></div></div>
          <div class="col-md-4"><div class="card"><div class="card-body"><div class="chart-cap">Con fotografía</div>
            <div class="chart-box"><StatChart type="pie" :data="d.retailers_with_image" /></div></div></div></div>
          <div class="col-md-4"><div class="card"><div class="card-body text-center tally-body">
            <div class="tally-cap">Administraciones en la colección</div>
            <div class="tally">{{ fmt(owned) }}</div>
            <div class="tally-cap mb-2">de {{ fmt(total) }} de España</div>
            <hr class="my-2" style="border-color:var(--sepia-tenue)" />
            <div class="tally-cap">Con fotografía</div>
            <div class="tally">{{ fmt(withImg) }}</div>
          </div></div></div>
        </div>
        <div class="row stats-row">
          <div class="col-md-6"><div class="card"><div class="card-body"><div class="chart-cap">Por comunidad</div>
            <div class="chart-box"><StatChart type="bar" horizontal color="#574231" :data="d.retailers_regions" /></div></div></div></div>
          <div class="col-md-6"><div class="card"><div class="card-body"><div class="chart-cap">Por provincia</div>
            <div class="chart-box"><StatChart type="bar" color="#574231" :data="d.retailers_provinces" /></div></div></div></div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.fit-main { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; padding: .3rem .8rem .2rem; }
.stats-head { flex: 0 0 auto; }
.stats-head :deep(h2) { font-size: 23px; }
.stats-row { flex: 1 1 auto; min-height: 0; margin: 0; }
.stats-row > [class^="col-"] { height: 100%; display: flex; padding: .3rem; }
.stats-row :deep(.card) { flex: 1 1 auto; min-height: 0; width: 100%; display: flex; flex-direction: column; }
.stats-row :deep(.card-body) { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; padding: .4rem .6rem; }
.chart-cap { flex: 0 0 auto; font-family: var(--font-caps); font-size: 16px; color: var(--nogal); text-align: center; margin-bottom: .2rem; font-variant: small-caps; }
.chart-box { flex: 1 1 auto; min-height: 0; position: relative; }
.tally-body { justify-content: center; }
.tally { font-family: var(--font-numerador); font-weight: 800; color: var(--tinta); font-size: 40px; line-height: 1.1; }
.tally-cap { font-family: var(--font-caps); font-variant: small-caps; color: var(--tinta-sepia); letter-spacing: .04em; }
</style>
