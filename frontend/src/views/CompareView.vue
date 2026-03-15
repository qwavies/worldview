<template>
  <div class="page" :class="{ 'is-submitting': isSubmitting }">

    <header class="topbar">
      <router-link to="/" class="brand">
        <img :src="logoImage" alt="Worldview Logo" class="logo" />
      </router-link>

      <div class="selector-row">
        <div class="country-slot" :class="{ active: focusedSlot === 'A' }">
          <div class="input-fixed">
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
          <div class="input-fixed">
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
        <div class="topbar-spacer"></div>

      </div>
    </header>

    <div class="map-container" ref="mapEl"></div>

    <div class="zoom-controls">
      <button @click="zoomIn">+</button>
      <button @click="zoomOut">−</button>
      <button @click="resetView" title="Reset view">⌂</button>
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

    <div class="hint" v-if="showHint">Select two countries first</div>
    <div class="submit">
      <button @click="submitCompare" :disabled="isSubmitting">›</button>
    </div>

    <div v-if="unavailablePopup" class="unavailable-popup"
      :style="`left: ${unavailablePopup.x}px; top: ${unavailablePopup.y}px`">
      <span class="unavailable-icon">✕</span>
      {{ unavailablePopup.name }}: country unavailable
    </div>

    <ResultsPanel v-if="showPanel" :sentimentData="sentimentData" :countryA="selectedA" :countryB="selectedB"
      :loading="isSubmitting" @close="showPanel = false; sentimentData = null" />

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm'
import { feature } from 'https://cdn.jsdelivr.net/npm/topojson-client@3/+esm'
import logoImage from '../assets/LogoWithText.png'
import countryList from '../assets/countries.json'
import ResultsPanel from '../components/ResultsPanel.vue'

const colorA = '#3B82F6'
const colorB = '#F97316'

const countries = ref(countryList)
const selectedA = ref(null)
const selectedB = ref(null)
const searchA = ref('')
const searchB = ref('')
const showDropA = ref(false)
const showDropB = ref(false)
const focusedSlot = ref(null)

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

const mapEl = ref(null)
let svgEl = null, gEl = null, zoomBehavior = null, pathFn = null, worldData = null

const unavailablePopup = ref(null)
let unavailableTimer = null

function showUnavailable(name, event) {
  if (unavailableTimer) clearTimeout(unavailableTimer)
  const rect = mapEl.value.getBoundingClientRect()
  unavailablePopup.value = { name, x: event.clientX - rect.left, y: event.clientY - rect.top }
  unavailableTimer = setTimeout(() => { unavailablePopup.value = null }, 2500)
}

onMounted(async () => { await buildMap() })

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

  svgEl.append('rect')
    .attr('width', '100%')
    .attr('height', '100%')
    .attr('fill', '#0f1923')

  gEl = svgEl.append('g')

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
      if (!isSelectedCountry(d)) d3.select(this).attr('fill', '#2a4a6e')
      showTooltip(event, getCountryName(d))
    })
    .on('mousemove', moveTooltip)
    .on('mouseout', function () { hideTooltip(); updateHighlights() })
    .on('click', function (event, d) {
      const name = getCountryName(d)
      if (!name) return
      const match = countries.value.find(c => c.name.toLowerCase() === name.toLowerCase())
      if (!match) { showUnavailable(name || 'This territory', event); return }

      if (focusedSlot.value === 'A') selectCountry('A', match)
      else if (focusedSlot.value === 'B') selectCountry('B', match)
      else if (!selectedA.value) selectCountry('A', match)
      else selectCountry('B', match)
    })

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

function getCountryName(feature) { return feature.properties?.name || '' }

function isSelectedCountry(feature) {
  const name = getCountryName(feature)
  return (selectedA.value?.name === name) || (selectedB.value?.name === name)
}

function updateHighlights() {
  if (!gEl) return
  gEl.selectAll('.country')
    .attr('fill', d => {
      const name = getCountryName(d)
      if (selectedA.value?.name === name) return colorA
      if (selectedB.value?.name === name) return colorB
      return '#1a2e44'
    })
    .attr('stroke', d => {
      const name = getCountryName(d)
      if (selectedA.value?.name === name) return colorA
      if (selectedB.value?.name === name) return colorB
      return '#2d4a6b'
    })
    .attr('stroke-width', d => isSelectedCountry(d) ? 2 : 0.5)
    .attr('filter', d => {
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

function zoomIn() { svgEl?.transition().duration(300).call(zoomBehavior.scaleBy, 1.6) }
function zoomOut() { svgEl?.transition().duration(300).call(zoomBehavior.scaleBy, 0.625) }
function resetView() {
  svgEl?.transition().duration(600).call(zoomBehavior.transform, d3.zoomIdentity)
}

watch([selectedA, selectedB], updateHighlights)

const showHint = ref(false)
const isSubmitting = ref(false)
const sentimentData = ref(null)
const showPanel = ref(false)

async function submitCompare() {
  if (!selectedA.value || !selectedB.value) {
    showHint.value = true
    setTimeout(() => showHint.value = false, 2500)
    return
  }

  sentimentData.value = null
  isSubmitting.value = true
  showPanel.value = true
  resetView()

  try {

    const res = await fetch(`https://worldview-production.up.railway.app/sentiment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        countryA: selectedA.value.name,
        countryB: selectedB.value.name,
      })
    })
    if (!res.ok) throw new Error(`Server error: ${res.status}`)
    sentimentData.value = await res.json()
  } catch (err) {
    console.error('Failed to fetch sentiment:', err)
    showPanel.value = false
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.page {
  background: #080f1a;
  color: #cbd5e1;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.page.is-submitting .topbar,
.page.is-submitting .map-container,
.page.is-submitting .zoom-controls,
.page.is-submitting .legend,
.page.is-submitting .submit,
.page.is-submitting .hint {
  filter: blur(3px);
  pointer-events: none;
  transition: filter 0.4s ease;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 10px 20px;
  background: #0d1b2a;
  border-bottom: 1px solid #1e3a5f;
  height: 110px;
  overflow: visible;
  flex-shrink: 0;
  z-index: 10;
  transition: filter 0.4s ease;
}

.brand {
  text-decoration: none;
  flex-shrink: 0;
  display: block;
  width: 160px;
}

.topbar-spacer {
  width: 160px;
  flex-shrink: 0;
}

.selector-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  justify-content: center;
}

.logo {
  height: 32px;
  width: auto;
  display: block;
}


.country-slot {
  flex: 1;
  position: relative;
}

.input-fixed {
  position: relative;
  height: 60px;
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
  font-size: 14px;
  font-family: "Roboto", sans-serif;
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
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  z-index: 5;
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
  font-family: "Roboto", sans-serif;
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
  transition: filter 0.4s ease;
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
  transition: filter 0.4s ease;
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
  transition: filter 0.4s ease;
}

.legend-item {
  font-family: "Roboto", sans-serif;
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

.submit {
  position: absolute;
  bottom: 28px;
  right: 20px;
  z-index: 10;
  transition: filter 0.4s ease;
}

.submit button {
  width: 96px;
  height: 86px;
  background: #0d1b2a;
  border: 1px solid #1e3a5f;
  border-radius: 7px;
  color: #94a3b8;
  font-size: 98px;
  font-weight: 500;
  padding-bottom: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
}

.submit button:hover:not(:disabled) {
  background: #1a2e44;
  color: #e2e8f0;
}

.submit button:disabled {
  cursor: default;
  opacity: 0.4;
}

.hint {
  position: absolute;
  bottom: 122px;
  right: 20px;
  background: #0d1b2a;
  border: 1px solid #f97316;
  color: #f97316;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 13px;
  z-index: 10;
  animation: fadeIn 0.2s ease;
  transition: filter 0.4s ease;
}

.unavailable-popup {
  position: absolute;
  transform: translate(-10%, -10%);
  background: #0d1b2a;
  border: 1px solid #7f1d1d;
  color: #fca5a5;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 13px;
  white-space: nowrap;
  z-index: 20;
  pointer-events: none;
  animation: fadeIn 0.15s ease;
}

.unavailable-icon {
  font-size: 11px;
  margin-right: 5px;
  opacity: 0.7;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
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
</style>
