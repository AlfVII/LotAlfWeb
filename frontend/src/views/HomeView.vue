<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'

const posts = ref([])
const form = ref({ name: '', email: '', post: '' })
const sending = ref(false)
const sent = ref(false)

async function load() {
  try { posts.value = await api.comments() } catch (e) { posts.value = [] }
}
async function submit() {
  if (!form.value.name || !form.value.email || !form.value.post) return
  sending.value = true
  try {
    await api.addComment({ name: form.value.name, email: form.value.email, comment: form.value.post })
    form.value = { name: '', email: '', post: '' }
    sent.value = true
    await load()
  } finally { sending.value = false }
}
onMounted(load)
</script>

<template>
  <div class="view">
    <!-- Portada — la cartela grabada -->
    <div class="orla cartouche text-center hero-orla">
      <svg v-for="c in ['tl','tr','bl','br']" :key="c" :class="`voluta voluta--${c}`" viewBox="0 0 64 64" aria-hidden="true">
        <path fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round"
          d="M2 62 C2 34 14 8 40 4 C26 10 22 24 26 34 C29 41 38 42 42 36 C45 31 41 26 36 28 C40 27 43 31 41 35" />
      </svg>
      <h1 class="mb-2">Los décimos de Ildefonso</h1>
      <div class="engrave-caps" style="font-size:20px;">· Coleccionando desde 1955 ·</div>
      <div class="d-flex justify-content-center my-3">
        <svg class="roseta" viewBox="0 0 100 100" aria-hidden="true">
          <g fill="none" stroke="currentColor" stroke-width="0.6">
            <ellipse v-for="r in [0,30,60,90,120,150]" :key="r" cx="50" cy="50" rx="40" ry="15" :transform="`rotate(${r} 50 50)`" />
            <circle cx="50" cy="50" r="6" />
          </g>
        </svg>
      </div>
      <p class="lead mb-2">Un álbum privado de décimos: la colección de todos los números,
        y un décimo de cada administración de lotería de España.</p>
      <p class="lead mb-0">Arriba encontrará mis dos colecciones. Si desea dejarme unas líneas, este es su lugar.</p>
    </div>

    <div class="container fit-body">
      <div class="row">
        <!-- Tablón -->
        <div class="col-sm-7 px-3 border-right border-secondary">
          <div class="text-center posts-head" style="margin:2px 0 8px;">
            <div class="engrave-caps" style="font-size:22px;">Últimas líneas del cuaderno</div>
            <svg class="divider" viewBox="0 0 240 16" width="240" height="16" role="presentation">
              <g fill="none" stroke="currentColor" stroke-width="0.8">
                <line x1="0" y1="8" x2="96" y2="8" /><line x1="144" y1="8" x2="240" y2="8" />
                <path d="M96 8 C104 8 108 3 114 5 C120 7 117 12 111 11 M144 8 C136 8 132 3 126 5 C120 7 123 12 129 11" />
              </g><circle cx="120" cy="8" r="1.6" fill="currentColor" />
            </svg>
          </div>
          <div class="posts-scroll">
            <p v-if="!posts.length" class="text-center" style="color:var(--tinta-sepia)">
              Aún no hay comentarios. Sea el primero en dejar unas líneas.
            </p>
            <div class="media my-3" v-for="(p, i) in posts" :key="i">
              <img class="d-flex rounded-circle avatar mr-3" width="56" height="56" :src="p.identicon" alt="" />
              <div class="media-body">
                <h5 class="mt-0 font-weight-bold">{{ p.name }}</h5>
                {{ p.comment }}
              </div>
            </div>
          </div>
        </div>

        <!-- Deje unas líneas -->
        <div class="col-sm-5 px-3">
          <div class="bg-light p-3" style="margin-top:18px;">
            <span class="engrave-caps mb-3 d-inline-block" style="font-size:22px;">Deje unas líneas</span>
            <form class="form form-horizontal mt-3" @submit.prevent="submit">
              <div class="form-row required">
                <label class="col-form-label col-sm-4">Nombre</label>
                <div class="col-sm-8"><input class="form-control" v-model="form.name" type="text" /></div>
              </div>
              <div class="form-row required mt-2">
                <label class="col-form-label col-sm-4">Correo</label>
                <div class="col-sm-8"><input class="form-control" v-model="form.email" type="email" /></div>
              </div>
              <div class="form-row required mt-2">
                <label class="col-form-label col-sm-4">Mensaje</label>
                <div class="col-sm-8"><textarea class="form-control" v-model="form.post" rows="4"></textarea></div>
              </div>
              <div class="form-row mt-3">
                <div class="col-sm-12 text-right">
                  <button type="submit" class="btn btn-info" :disabled="sending">Añadir comentario</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero-orla { flex: 0 0 auto; margin: .5rem .8rem; padding: .7rem 1.2rem; }
.hero-orla :deep(h1) { font-size: clamp(28px, 4vw, 42px); margin-bottom: .15rem; }
.hero-orla .roseta { width: 36px; height: 36px; }
.hero-orla .lead { font-size: 18px; margin-bottom: .15rem; line-height: 1.4; }
.fit-body { flex: 1 1 auto; min-height: 0; }
.fit-body > .row { height: 100%; margin: 0; }
.fit-body > .row > [class^="col-"] { height: 100%; display: flex; flex-direction: column; min-height: 0; }
.posts-head { flex: 0 0 auto; }
.posts-scroll { flex: 1 1 auto; min-height: 0; overflow: auto; padding-right: .4rem; }
</style>
