<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  type: { type: String, default: 'pie' },        // 'pie' | 'bar'
  data: { type: Object, default: null },
  horizontal: { type: Boolean, default: false },
  color: { type: String, default: '#1E4D34' },
})

const el = ref(null)
let chart = null
const INK = ['#1E4D34', '#574231', '#2E5E3A', '#8A745C', '#3A2A1A', '#5A3E2B', '#7A8B6F', '#9C8B5E', '#46604A', '#B0A083']
const GRID = 'rgba(87,66,49,.14)'

function render() {
  if (chart) { chart.destroy(); chart = null }
  if (!el.value || !props.data) return
  const labels = Object.keys(props.data)
  const values = Object.values(props.data)
  Chart.defaults.font.family = "'Lora', Georgia, serif"
  Chart.defaults.color = '#574231'
  const cfg = props.type === 'pie'
    ? {
        type: 'pie',
        data: { labels, datasets: [{ data: values, backgroundColor: INK.slice(0, labels.length), borderColor: '#F4ECD8', borderWidth: 2 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, padding: 10 } } } },
      }
    : {
        type: 'bar',
        data: { labels, datasets: [{ data: values, backgroundColor: props.color, borderColor: '#1C1812', borderWidth: 1 }] },
        options: { indexAxis: props.horizontal ? 'y' : 'x', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: GRID } }, y: { grid: { color: GRID } } } },
      }
  chart = new Chart(el.value, cfg)
}

onMounted(render)
watch(() => props.data, render)
onBeforeUnmount(() => chart && chart.destroy())
</script>

<template><canvas ref="el"></canvas></template>
