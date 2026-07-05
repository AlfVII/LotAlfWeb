<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import L from 'leaflet'

const props = defineProps({ markers: { type: Array, default: () => [] } })
const emit = defineEmits(['select'])
const el = ref(null)
let map = null
let layer = null

function esc(s) { return String(s ?? '').replace(/</g, '&lt;') }

function draw() {
  if (!map) return
  if (layer) layer.remove()
  layer = L.layerGroup().addTo(map)
  for (const m of props.markers) {
    if (m.lat == null || m.lng == null) continue
    const cm = L.circleMarker([m.lat, m.lng], m.owned
      ? { radius: 8, color: '#2B1D14', weight: 1, fillColor: '#C65D2E', fillOpacity: 0.92 }
      : { radius: 7, color: '#6E7645', weight: 1.5, fillColor: '#F4EAD0', fillOpacity: 0.85 })
    cm.bindPopup(`${esc(m.town)} · Admón nº ${esc(m.number)}<br>${esc(m.name)}`)
    cm.on('click', () => emit('select', m))
    cm.addTo(layer)
  }
  const pts = props.markers.filter((m) => m.lat != null && m.lng != null)
  if (pts.length) {
    const lat = pts.reduce((a, m) => a + m.lat, 0) / pts.length
    const lng = pts.reduce((a, m) => a + m.lng, 0) / pts.length
    map.setView([lat, lng], map.getZoom())
  }
}

onMounted(() => {
  map = L.map(el.value, { scrollWheelZoom: false }).setView([40.2, -3.6], 6)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap', maxZoom: 18 }).addTo(map)
  setTimeout(() => map && map.invalidateSize(), 0)
  draw()
})
watch(() => props.markers, draw, { deep: true })
onBeforeUnmount(() => map && map.remove())
</script>

<template><div ref="el" id="map"></div></template>

<style scoped>#map { height: 100%; }</style>
