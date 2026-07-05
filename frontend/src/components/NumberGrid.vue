<script setup>
defineProps({ base: { type: Number, default: 0 }, statuses: { type: Array, default: () => [] } })
const emit = defineEmits(['select'])
const STATUS_CLASS = { Perfecto: 'btn-success', Defectuoso: 'btn-warning', Falta: 'btn-secondary', 'Faltan Datos': 'btn-info' }
const cls = (s) => STATUS_CLASS[s] || 'btn-secondary'
const pad2 = (i) => (i < 10 ? '0' : '') + i
</script>

<template>
  <div class="centena-grid">
    <button v-for="i in 100" :key="i" type="button"
      :id="'button_number_' + pad2(i - 1)" :name="'button_number_' + pad2(i - 1)"
      class="btn btn_number btn-lg" :class="cls(statuses[i - 1])"
      @click="emit('select', base + (i - 1))">{{ pad2(i - 1) }}</button>
  </div>
</template>

<style scoped>
.centena-grid { flex: 1 1 auto; min-height: 0; display: grid; grid-template-columns: repeat(10, 1fr); grid-auto-rows: 1fr; gap: 5px; }
.centena-grid .btn_number { min-width: 0; min-height: 0; height: 100%; padding: 0; font-size: clamp(13px, 1.35vw, 18px); }
</style>
