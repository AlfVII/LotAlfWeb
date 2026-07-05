<script setup>
import TheNavbar from './components/TheNavbar.vue'
import TheFooter from './components/TheFooter.vue'
</script>

<template>
  <TheNavbar />
  <main class="app-main"><router-view /></main>
  <TheFooter />
</template>

<style>
/* App shell — fit one screen, no page scroll (each view fills .app-main) */
html, body, #app { height: 100%; }
body { overflow: hidden; }
#app { display: flex; flex-direction: column; min-height: 0; }
.app-main { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; overflow: hidden; }
.navbar { flex: 0 0 auto; }
.navbar.bg-light { padding-top: .3rem; padding-bottom: .3rem; }
/* every routed view fills the main area and never scrolls the page */
.view { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; overflow: hidden; }
</style>
