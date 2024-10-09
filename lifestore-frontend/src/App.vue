<template>
  <div class="app-wrapper">
    <div class="app-container">
      <AppHeader />
      <main class="main-content">
        <router-view></router-view>
      </main>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter
  }
}
</script>

<style>
body {
  font-family: 'Roboto', sans-serif;
  background-color: #f0f2f5;
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-container {
  flex: 1;
  max-width: 800px;
  margin: 30px auto;
  width: 100%;
  box-sizing: border-box;
}
</style>