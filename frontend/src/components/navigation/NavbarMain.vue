<template>
  <div id="nav">
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand" exact-active-class=""
          >Farm Monitor</router-link
        >
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarCollapse"
          aria-controls="navbarCollapse"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" class="nav-link">About</router-link>
            </li>
            <li>
              <navbar-s-w-status-vue></navbar-s-w-status-vue>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script lang="ts" setup>
import NavbarSWStatusVue from "./NavbarSWStatus.vue";
</script>

<style>
#nav {
  padding: 35px;
}

#nav a {
  font-weight: bold;
  color: #c1c7ce;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
