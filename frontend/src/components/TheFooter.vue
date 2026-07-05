<template>
  <footer class="counter-footer on-green">
    <span class="engrave-caps">Los décimos de Ildefonso</span>
    <span class="legal">Una colección privada · Desde 1955 · Todos los números y un décimo de cada administración de España</span>
  </footer>
</template>

<style>
.counter-footer {
  flex: 0 0 auto;
  display: flex; align-items: baseline; justify-content: center; gap: .9rem;
  background: linear-gradient(180deg, var(--nogal-claro), var(--nogal));
  color: var(--marfil);
  border-top: 1px solid var(--nogal-claro);
  font-family: var(--font-caps);
  padding: .28rem .8rem;
}
.counter-footer .engrave-caps { font-size: 16px; white-space: nowrap; }
.counter-footer .legal { font-size: 13px; color: var(--marfil); opacity: .85; }
@media (max-width: 760px) {
  .counter-footer { flex-direction: column; gap: 0; text-align: center; }
}
</style>
