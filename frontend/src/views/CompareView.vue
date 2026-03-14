<template>
  <div class="page">
    <header class="topbar">
      <router-link to="/" class="brand-link">Worldview</router-link>

      <div class="selector-row">
        <div class="country-slot" :class="{ active: focusedSlot === 'A' }">
          <div class="slot-label">Country A</div>
          <div class="autocomplete-wrap">
            <input ref="inputA" v-model="searchA" @input="onSearchA" @focus="focusedSlot = 'A'; showDropA = true"
              @blur="delayClose('A')" @keydown.enter="selectFirst('A')" @keydown.escape="showDropA = false"
              placeholder="Search country…" class="country-input"
              :style="selectedA ? `border-color: ${colorA}55; background: ${colorA}11` : ''" />
            <div v-if="selectedA" class="flag-chip" :style="`background: ${colorA}22`">
              <img :src="flagUrl(selectedA.code2)" :alt="selectedA.name" class="flag-img" />
              <span>{{ selectedA.name }}</span>
              <button class="clear-btn" @mousedown.prevent="clearA">×</button>
            </div>
            <ul v-if="showDropA && filteredA.length" class="dropdown">
              <li v-for="c in filteredA.slice(0, 8)" :key="c.code2" @mousedown.prevent="selectCountry('A', c)"
                class="drop-item">
                <img :src="flagUrl(c.code2)" class="drop-flag" />
                {{ c.name }}
              </li>
            </ul>
          </div>
        </div>

        <button class="swap-btn" @click="swapCountries" title="Swap countries">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <path d="M6 10 L22 10 M16 5 L22 10 L16 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
            <path d="M22 18 L6 18 M12 13 L6 18 L12 23" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
        </button>

        <div class="country-slot" :class="{ active: focusedSlot === 'B' }">
          <div class="slot-label">Country B</div>
          <div class="autocomplete-wrap">
            <input ref="inputB" v-model="searchB" @input="onSearchB" @focus="focusedSlot = 'B'; showDropB = true"
              @blur="delayClose('B')" @keydown.enter="selectFirst('B')" @keydown.escape="showDropB = false"
              placeholder="Search country…" class="country-input"
              :style="selectedB ? `border-color: ${colorB}55; background: ${colorB}11` : ''" />
            <div v-if="selectedB" class="flag-chip" :style="`background: ${colorB}22`">
              <img :src="flagUrl(selectedB.code2)" :alt="selectedB.name" class="flag-img" />
              <span>{{ selectedB.name }}</span>
              <button class="clear-btn" @mousedown.prevent="clearB">×</button>
            </div>
            <ul v-if="showDropB && filteredB.length" class="dropdown">
              <li v-for="c in filteredB.slice(0, 8)" :key="c.code2" @mousedown.prevent="selectCountry('B', c)"
                class="drop-item">
                <img :src="flagUrl(c.code2)" class="drop-flag" />
                {{ c.name }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </header>

    <div class="map-container" ref="mapEl"></div>

    <div class="zoom-controls">
      <button @click="zoomIn">+</button>
      <button @click="zoomOut">−</button>
      <button @click="resetView" title="Reset view">⌂</button>
    </div>
    <div class="hint" v-if="showHint">Select two countries first</div>
    <div class="submit">
      <button @click="submitCompare">></button>
    </div>

    <div class="legend" v-if="selectedA || selectedB">
      <div v-if="selectedA" class="legend-item">
        <span class="legend-dot" :style="`background:${colorA}`"></span>
        <img :src="flagUrl(selectedA.code2)" class="legend-flag" />
        {{ selectedA.name }}
      </div>
      <div v-if="selectedB" class="legend-item">
        <span class="legend-dot" :style="`background:${colorB}`"></span>
        <img :src="flagUrl(selectedB.code2)" class="legend-flag" />
        {{ selectedB.name }}
      </div>
    </div>

  </div>
</template>




<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm'
import { feature } from 'https://cdn.jsdelivr.net/npm/topojson-client@3/+esm'
import { useRouter } from 'vue-router'
import countryList from '../assets/countries.json'

const countries = ref(countryList)
const router = useRouter()

const showHint = ref(false)

const colorA = '#3B82F6'  // blue
const colorB = '#F97316'  // orange

const selectedA = ref(null)
const selectedB = ref(null)
const searchA = ref('')
const searchB = ref('')
const showDropA = ref(false)
const showDropB = ref(false)
const focusedSlot = ref(null)
const mapEl = ref(null)

let svgEl = null, gEl = null, zoomBehavior = null, pathFn = null, worldData = null

const filteredA = computed(() =>
  countries.value.filter(c =>
    c.name.toLowerCase().includes(searchA.value.toLowerCase()) && c !== selectedA.value
  )
)
const filteredB = computed(() =>
  countries.value.filter(c =>
    c.name.toLowerCase().includes(searchB.value.toLowerCase()) && c !== selectedB.value
  )
)

function onSearchA() { showDropA.value = true }
function onSearchB() { showDropB.value = true }

function selectCountry(slot, country) {
  if (slot === 'A') { selectedA.value = country; searchA.value = ''; showDropA.value = false }
  else { selectedB.value = country; searchB.value = ''; showDropB.value = false }
  updateHighlights()
  zoomToCountry(country)
}

function selectFirst(slot) {
  const list = slot === 'A' ? filteredA.value : filteredB.value
  if (list.length) selectCountry(slot, list[0])
}

function clearA() { selectedA.value = null; searchA.value = ''; updateHighlights() }
function clearB() { selectedB.value = null; searchB.value = ''; updateHighlights() }

function delayClose(slot) {
  setTimeout(() => {
    if (slot === 'A') showDropA.value = false
    else showDropB.value = false
    if (focusedSlot.value === slot) focusedSlot.value = null
  }, 150)
}

function swapCountries() {
  const tmp = selectedA.value
  selectedA.value = selectedB.value
  selectedB.value = tmp
  updateHighlights()
}

function flagUrl(code2) {
  return `https://flagcdn.com/24x18/${code2.toLowerCase()}.png`
}

onMounted(async () => {
  await buildMap()
})

async function buildMap() {
  const width = mapEl.value.clientWidth
  const height = mapEl.value.clientHeight

  const projection = d3.geoNaturalEarth1()
    .scale(width / 6.2)
    .translate([width / 2, height / 2])

  pathFn = d3.geoPath().projection(projection)

  zoomBehavior = d3.zoom()
    .scaleExtent([0.5, 12])
    .on('zoom', (e) => gEl.attr('transform', e.transform))

  svgEl = d3.select(mapEl.value)
    .append('svg')
    .attr('width', '100%')
    .attr('height', '100%')
    .style('cursor', 'grab')
    .call(zoomBehavior)

  // ocean background
  svgEl.append('rect')
    .attr('width', '100%')
    .attr('height', '100%')
    .attr('fill', '#0f1923')

  gEl = svgEl.append('g')

  // Load world topo
  const topo = await d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
  worldData = feature(topo, topo.objects.countries)

  const graticule = d3.geoGraticule()
  gEl.append('path')
    .datum(graticule())
    .attr('d', pathFn)
    .attr('fill', 'none')
    .attr('stroke', '#1e3a5f')
    .attr('stroke-width', 0.4)

  gEl.selectAll('.country')
    .data(worldData.features)
    .enter()
    .append('path')
    .attr('class', 'country')
    .attr('d', pathFn)
    .attr('fill', '#1a2e44')
    .attr('stroke', '#2d4a6b')
    .attr('stroke-width', 0.5)
    .style('cursor', 'pointer')
    .on('mouseover', function (event, d) {
      const name = getCountryName(d)
      const isSelected = isSelectedCountry(d)
      if (!isSelected) d3.select(this).attr('fill', '#2a4a6e')
      showTooltip(event, name)
    })
    .on('mousemove', moveTooltip)
    .on('mouseout', function (event, d) {
      hideTooltip()
      updateHighlights()
    })
    .on('click', function (event, d) {
      const name = getCountryName(d)
      if (!name) return
      const match = countries.value.find(c =>
        c.name.toLowerCase() === name.toLowerCase()
      )
      if (!match) return
      if (focusedSlot.value === 'A') selectCountry('A', match)
      else if (focusedSlot.value === 'B') selectCountry('B', match)
      else {
        // auto-pick slot
        if (!selectedA.value) selectCountry('A', match)
        else if (!selectedB.value) selectCountry('B', match)
        else selectCountry('A', match)
      }
    })

  // Tooltip div
  d3.select(mapEl.value)
    .append('div')
    .attr('id', 'map-tooltip')
    .style('position', 'absolute')
    .style('background', '#0d1b2a')
    .style('color', '#e2e8f0')
    .style('padding', '5px 10px')
    .style('border-radius', '6px')
    .style('font-size', '13px')
    .style('pointer-events', 'none')
    .style('opacity', '0')
    .style('border', '1px solid #2d4a6b')
    .style('transition', 'opacity 0.1s')
}

// Country name lookup from numeric ID
const numericToAlpha2 = {}
onMounted(() => {
})

function getCountryName(feature) {
  return feature.properties?.name || ''
}

function isSelectedCountry(feature) {
  const name = getCountryName(feature)
  return (selectedA.value && selectedA.value.name === name) ||
    (selectedB.value && selectedB.value.name === name)
}

function updateHighlights() {
  if (!gEl) return
  gEl.selectAll('.country')
    .attr('fill', (d) => {
      const name = getCountryName(d)
      if (selectedA.value && selectedA.value.name === name) return colorA
      if (selectedB.value && selectedB.value.name === name) return colorB
      return '#1a2e44'
    })
    .attr('stroke', (d) => {
      const name = getCountryName(d)
      if (selectedA.value && selectedA.value.name === name) return colorA
      if (selectedB.value && selectedB.value.name === name) return colorB
      return '#2d4a6b'
    })
    .attr('stroke-width', (d) => {
      const name = getCountryName(d)
      return isSelectedCountry(d) ? 2 : 0.5
    })
    .attr('filter', (d) => {
      if (!isSelectedCountry(d)) return null
      const name = getCountryName(d)
      const col = selectedA.value?.name === name ? colorA : colorB
      return `drop-shadow(0 0 6px ${col})`
    })
}

function zoomToCountry(country) {
  if (!gEl || !worldData) return
  const feat = worldData.features.find(f =>
    getCountryName(f).toLowerCase() === country.name.toLowerCase()
  )
  if (!feat) return
  const [[x0, y0], [x1, y1]] = pathFn.bounds(feat)
  const width = mapEl.value.clientWidth
  const height = mapEl.value.clientHeight
  const dx = x1 - x0, dy = y1 - y0
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2
  const scale = Math.min(2, 0.8 / Math.max(dx / width, dy / height))
  const tx = width / 2 - scale * cx
  const ty = height / 2 - scale * cy

  svgEl.transition().duration(750).call(
    zoomBehavior.transform,
    d3.zoomIdentity.translate(tx, ty).scale(scale)
  )
}

function showTooltip(event, name) {
  if (!name) return
  const tip = document.getElementById('map-tooltip')
  if (!tip) return
  tip.textContent = name
  tip.style.opacity = '1'
}

function moveTooltip(event) {
  const tip = document.getElementById('map-tooltip')
  if (!tip) return
  const rect = mapEl.value.getBoundingClientRect()
  tip.style.left = (event.clientX - rect.left + 12) + 'px'
  tip.style.top = (event.clientY - rect.top - 28) + 'px'
}

function hideTooltip() {
  const tip = document.getElementById('map-tooltip')
  if (tip) tip.style.opacity = '0'
}

// Zoom controls
function zoomIn() { svgEl?.transition().duration(300).call(zoomBehavior.scaleBy, 1.6) }
function zoomOut() { svgEl?.transition().duration(300).call(zoomBehavior.scaleBy, 0.625) }
function resetView() {
  svgEl?.transition().duration(600).call(
    zoomBehavior.transform, d3.zoomIdentity
  )
}


function submitCompare() {
  if (!selectedA.value || !selectedB.value) {
    showHint.value = true
    setTimeout(() => showHint.value = false, 2500)
    return
  }
  router.push({
    path: '/submission',
    query: { countryA: selectedA.value.code2, countryB: selectedB.value.code2 }
  })
}

watch([selectedA, selectedB], updateHighlights)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.page {
  font-family: 'Syne', sans-serif;
  background: #080f1a;
  color: #cbd5e1;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 10px 20px;
  background: #0d1b2a;
  border-bottom: 1px solid #1e3a5f;
  flex-shrink: 0;
  z-index: 10;
}

.title {
  font-weight: 700;
  font-size: 16px;
  color: #60a5fa;
  white-space: nowrap;
  letter-spacing: 0.02em;
}

.selector-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.country-slot {
  flex: 1;
  position: relative;
}

.slot-label {
  font-size: 10px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.1em;
  color: #475569;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.autocomplete-wrap {
  position: relative;
}

.country-input {
  width: 100%;
  background: #112033;
  border: 1px solid #1e3a5f;
  border-radius: 8px;
  padding: 8px 12px;
  color: #e2e8f0;
  font-family: 'Syne', sans-serif;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s, background 0.2s;
}

.country-input::placeholder {
  color: #334e68;
}

.country-input:focus {
  border-color: #3b82f6;
}

.flag-chip {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 5px 10px;
  border-radius: 6px;
  margin-top: 4px;
  font-size: 13px;
  font-weight: 600;
}

.flag-img {
  width: 20px;
  height: 15px;
  border-radius: 2px;
}

.clear-btn {
  background: none;
  border: none;
  color: #64748b;
  font-size: 16px;
  cursor: pointer;
  margin-left: auto;
  line-height: 1;
  padding: 0 2px;
}

.clear-btn:hover {
  color: #e2e8f0;
}

.dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: #0d1b2a;
  border: 1px solid #1e3a5f;
  border-radius: 8px;
  list-style: none;
  z-index: 100;
  max-height: 260px;
  overflow-y: auto;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.drop-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.1s;
}

.drop-item:hover {
  background: #1a2e44;
}

.drop-flag {
  width: 20px;
  height: 15px;
  border-radius: 2px;
}

.swap-btn {
  background: #112033;
  border: 1px solid #1e3a5f;
  border-radius: 8px;
  color: #60a5fa;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.2s, color 0.2s, transform 0.2s;
}

.swap-btn:hover {
  background: #1a2e44;
  color: #93c5fd;
  transform: scale(1.08);
}

.map-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  min-height: 0;
}

.map-container :deep(svg) {
  display: block;
}

.zoom-controls {
  position: absolute;
  bottom: 28px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 10;
}

.zoom-controls button {
  width: 36px;
  height: 36px;
  background: #0d1b2a;
  border: 1px solid #1e3a5f;
  border-radius: 7px;
  color: #94a3b8;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
}

.zoom-controls button:hover {
  background: #1a2e44;
  color: #e2e8f0;
}

.legend {
  position: absolute;
  bottom: 28px;
  left: 70px;
  background: #0d1b2acc;
  border: 1px solid #1e3a5f;
  border-radius: 10px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 10;
  backdrop-filter: blur(6px);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-flag {
  width: 20px;
  height: 15px;
  border-radius: 2px;
}

.compare-button {
  right: 10px
}

.submit {
  position: absolute;
  bottom: 28px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 10;
}

.submit button {
  width: 66px;
  height: 46px;
  background: #0d1b2a;
  border: 1px solid #1e3a5f;
  border-radius: 7px;
  color: #94a3b8;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
}

.hint {
  position: absolute;
  bottom: 92px;
  right: 20px;
  background: #0d1b2a;
  border: 1px solid #f97316;
  color: #f97316;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 13px;
  z-index: 10;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.brand-link {
  font-size: 18px;
  font-weight: 700;
  color: #e2e8f0;
  letter-spacing: 0.04em;
  text-decoration: none;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.brand-link:hover {
  color: #e2e8f0;
}
</style>
