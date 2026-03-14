<script setup>
import { onMounted, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const map = ref(null)
const mapContainer = ref(null)

onMounted(() => {
  map.value = L.map(mapContainer.value).setView([20, 0], 2)

  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '© OpenStreetMap contributors © CARTO',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map.value)
})
</script>

<template>
  <div class="map-wrapper">
    <div ref="mapContainer" class="world-map"></div>
  </div>
</template>

<style scoped>
.map-wrapper {
  width: 100%;
  height: 100%;
}

.world-map {
  width: 100%;
  height: 100%;
}

/* .world-map { */
/*   width: 100%; */
/*   height: 100%; */
/*   filter: invert(100%) hue-rotate(210deg); */
/* } */
</style>
