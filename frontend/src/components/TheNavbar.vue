<script setup>
import { ref } from 'vue'
import { useAuth } from '../stores/auth'

const auth = useAuth()
const password = ref('')

async function doLogin() {
  if (await auth.login(password.value)) password.value = ''
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link class="navbar-brand" to="/">Los décimos de Ildefonso</router-link>
    <span class="engrave-caps d-none d-lg-inline-block ml-3" style="font-size:18px;">Desde 1955</span>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item"><router-link class="nav-link" to="/">Tablón</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/numeros">Colección de números</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/administraciones">Colección de administraciones</router-link></li>
      </ul>
    </div>

    <div>
      <ul class="navbar-nav flex-row align-items-center">
        <template v-if="!auth.isEditor">
          <li class="nav-item mr-2">
            <input type="password" class="form-control" id="edit_mode_password"
                   v-model="password" @keyup.enter="doLogin" placeholder="Identifíquese para editar" />
          </li>
          <li class="nav-item"><button class="btn btn-success" @click="doLogin">Identificarse</button></li>
        </template>
        <li class="nav-item" v-else>
          <button class="btn btn-danger" @click="auth.logout()">Salir de modo edición</button>
        </li>
      </ul>
    </div>
  </nav>
</template>
