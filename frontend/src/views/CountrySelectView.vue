<script setup>
import CountrySelect from '../components/CountrySelect.vue'
import SideBar from '../components/SideBar.vue'
</script>

<template>
  <div class="app-layout">
    <aside class="sidebar-wrapper">
      <SideBar />
    </aside>

    <main class="main-content">
      <CountrySelect />
    </main>
  </div>
</template>


<style scoped>
body {
  margin: 0;
  padding: 0;
}

.app-layout {
  display: flex;
  height: 98vh;
  width: 100%;
  overflow: hidden;
}

.sidebar-wrapper {
  width: 300px;
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  height: 100%;
  overflow: hidden;
}
</style>
