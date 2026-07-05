import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('./views/HomeView.vue'), meta: { title: 'Tablón' } },
  { path: '/numeros', name: 'numbers', component: () => import('./views/NumbersView.vue'), meta: { title: 'Colección de números' } },
  { path: '/filtros', name: 'filtros', component: () => import('./views/FiltrosView.vue'), meta: { title: 'Filtros' } },
  { path: '/administraciones', name: 'retailers', component: () => import('./views/RetailersView.vue'), meta: { title: 'Colección de administraciones' } },
  { path: '/estadisticas-numeros', name: 'stats-numbers', component: () => import('./views/StatsNumbersView.vue'), meta: { title: 'Estadísticas de números' } },
  { path: '/estadisticas-administraciones', name: 'stats-retailers', component: () => import('./views/StatsRetailersView.vue'), meta: { title: 'Estadísticas de administraciones' } },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
