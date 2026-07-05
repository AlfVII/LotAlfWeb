<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'
import StatChart from '../components/StatChart.vue'

const d = ref(null)
const error = ref('')
onMounted(async () => {
  try { d.value = await api.statsNumbers() } catch (e) { error.value = e.message }
})
</script>

<template>
  <div class="view">
    <div class="fit-main">
      <div class="stats-head text-center mb-1">
        <h2 class="mb-0">Estado de la colección de números</h2>
        <svg class="divider" viewBox="0 0 200 14" width="200" height="14" role="presentation">
          <g fill="none" stroke="currentColor" stroke-width="0.8"><line x1="0" y1="7" x2="80" y2="7" /><line x1="120" y1="7" x2="200" y2="7" />
            <path d="M80 7 C88 7 92 2 98 4 C104 6 101 11 95 10 M120 7 C112 7 108 2 102 4 C96 6 99 11 105 10" /></g><circle cx="100" cy="7" r="1.5" fill="currentColor" />
        </svg>
      </div>

      <p v-if="error" class="text-center" style="color:var(--bermellon-hondo,#7C1420)">{{ error }}</p>

      <template v-if="d">
        <div class="row stats-row">
          <div class="col-md-3"><div class="card"><div class="card-body"><div class="chart-cap">Rellenados</div>
            <div class="chart-box"><StatChart type="pie" :data="d.numbers_filled" /></div></div></div></div>
          <div class="col-md-3"><div class="card"><div class="card-body"><div class="chart-cap">Estado</div>
            <div class="chart-box"><StatChart type="pie" :data="d.numbers_statuses" /></div></div></div></div>
          <div class="col-md-3"><div class="card"><div class="card-body"><div class="chart-cap">Origen</div>
            <div class="chart-box"><StatChart type="pie" :data="d.numbers_origins" /></div></div></div></div>
          <div class="col-md-3"><div class="card"><div class="card-body"><div class="chart-cap">Moneda</div>
            <div class="chart-box"><StatChart type="pie" :data="d.numbers_coins" /></div></div></div></div>
        </div>
        <div class="row stats-row">
          <div class="col-md-4"><div class="card"><div class="card-body"><div class="chart-cap">Por comunidad</div>
            <div class="chart-box"><StatChart type="bar" horizontal :data="d.numbers_regions" /></div></div></div></div>
          <div class="col-md-4"><div class="card"><div class="card-body"><div class="chart-cap">Por año</div>
            <div class="chart-box"><StatChart type="bar" :data="d.numbers_years" /></div></div></div></div>
          <div class="col-md-4"><div class="card"><div class="card-body"><div class="chart-cap">Por provincia</div>
            <div class="chart-box"><StatChart type="bar" :data="d.numbers_provinces" /></div></div></div></div>
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
</style>
