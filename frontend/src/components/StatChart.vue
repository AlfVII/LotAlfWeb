<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  type: { type: String, default: 'pie' },        // 'pie' | 'bar'
  data: { type: Object, default: null },
  horizontal: { type: Boolean, default: false },
  color: { type: String, default: '#C65D2E' },
})

const el = ref(null)
let chart = null
// Warm 70s album polychrome: orange, mustard, olive, ribbon-red, kraft, chocolate…
const INK = ['#C65D2E', '#C6912E', '#6E7645', '#A9432E', '#B4934F', '#6B5138', '#8A6A42', '#3A2A1D', '#9C8B5E', '#A8461C']
const GRID = 'rgba(107,81,56,.16)'

function render() {
  if (chart) { chart.destroy(); chart = null }
  if (!el.value || !props.data) return
  const labels = Object.keys(props.data)
  const values = Object.values(props.data)
  Chart.defaults.font.family = "'Alegreya', Georgia, serif"
  Chart.defaults.color = '#6B5138'
  const cfg = props.type === 'pie'
    ? {
        type: 'pie',
        data: { labels, datasets: [{ data: values, backgroundColor: INK.slice(0, labels.length), borderColor: '#F4EAD0', borderWidth: 2 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, padding: 10 } } } },
      }
    : {
        type: 'bar',
        data: { labels, datasets: [{ data: values, backgroundColor: props.color, borderColor: '#372518', borderWidth: 1 }] },
        options: { indexAxis: props.horizontal ? 'y' : 'x', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: GRID } }, y: { grid: { color: GRID } } } },
      }
  chart = new Chart(el.value, cfg)
}

onMounted(render)
watch(() => props.data, render)
onBeforeUnmount(() => chart && chart.destroy())
</script>

<template><canvas ref="el"></canvas></template>
