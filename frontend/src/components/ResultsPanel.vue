<template>
  <div class="page">
    <Transition name="panel" appear>
      <div v-if="visible" class="panel">

        <div class="panel-top" :class="{ locked: loading }" @click="dismiss">
          <div class="panel-handle"></div>
          <div class="panel-header">
            <span class="dismiss-hint">↓ back to map</span>
            <div class="country-pills">
              <div class="country-pill" :style="`border-color: ${colorA}55; background: ${colorA}11`">
                <img :src="flagUrl(countryA.code2)" class="pill-flag" />
                <span>{{ countryA.name }}</span>
              </div>
              <span class="vs-label">vs</span>
              <div class="country-pill" :style="`border-color: ${colorB}55; background: ${colorB}11`">
                <img :src="flagUrl(countryB.code2)" class="pill-flag" />
                <span>{{ countryB.name }}</span>
              </div>
            </div>
            <div class="spacer"></div>
          </div>
        </div>

        <div v-if="loading" class="loading-body">
          <div class="progress-stages">
            <div v-for="(stage, i) in stages" :key="stage.key" class="stage-row" :class="{
              done: i < currentStage,
              active: i === currentStage,
              pending: i > currentStage,
            }">
              <div class="stage-icon">
                <span v-if="i < currentStage" class="icon-done">✓</span>
                <span v-else-if="i === currentStage" class="icon-spinner"></span>
                <span v-else class="icon-dot">·</span>
              </div>
              <span class="stage-label">{{ stage.label }}</span>
              <div v-if="i === currentStage" class="stage-bar">
                <div class="stage-bar-fill" :style="`width: ${stageProgress}%`"></div>
              </div>
              <span v-else-if="i < currentStage" class="stage-done-label">done</span>
              <span v-else class="stage-done-label" style="opacity:0">—</span>
            </div>
          </div>
        </div>

        <div v-else class="panel-body">

          <div class="platform-row" v-for="(platform, i) in platforms" :key="platform.key"
            :style="`animation-delay: ${i * 80}ms`">
            <div class="platform-label">
              <span class="platform-icon">{{ platform.icon }}</span>
              <span class="platform-name">{{ platform.label }}</span>
            </div>

            <div class="bar-group">
              <span class="score-chip" :style="`color: ${colorA}`">
                <img :src="flagUrl(countryA.code2)" class="score-flag" />
                {{ fmt(sentimentData[platform.key]?.a) }}
              </span>

              <div class="bar-track">
                <div class="bar-half bar-left">
                  <div class="bar-fill"
                    :style="`width: ${negPct(sentimentData[platform.key]?.a)}%; background: ${colorA}`">
                  </div>
                  <div class="bar-fill"
                    :style="`width: ${negPct(sentimentData[platform.key]?.b)}%; background: ${colorB}; opacity: 0.6`">
                  </div>
                </div>
                <div class="bar-center"></div>
                <div class="bar-half bar-right">
                  <div class="bar-fill"
                    :style="`width: ${posPct(sentimentData[platform.key]?.a)}%; background: ${colorA}`">
                  </div>
                  <div class="bar-fill"
                    :style="`width: ${posPct(sentimentData[platform.key]?.b)}%; background: ${colorB}; opacity: 0.6`">
                  </div>
                </div>
              </div>

              <span class="score-chip score-right" :style="`color: ${colorB}`">
                {{ fmt(sentimentData[platform.key]?.b) }}
                <img :src="flagUrl(countryB.code2)" class="score-flag" />
              </span>
            </div>

            <div class="bar-axis">
              <span>−1</span><span>0</span><span>+1</span>
            </div>
          </div>

          <div class="divider"></div>

          <div class="averages">
            <h3 class="section-title">Average Sentiment</h3>
            <div class="avg-row">
              <div class="avg-card" :style="`border-color: ${colorA}33`">
                <img :src="flagUrl(countryA.code2)" class="avg-flag" />
                <span class="avg-name">{{ countryA.name }}</span>
                <span class="avg-score" :style="`color: ${scoreColor(avgA)}`">{{ fmt(avgA) }}</span>
                <span class="avg-verdict">{{ sentimentLabel(avgA) }}</span>
              </div>
              <div class="avg-card" :style="`border-color: ${colorB}33`">
                <img :src="flagUrl(countryB.code2)" class="avg-flag" />
                <span class="avg-name">{{ countryB.name }}</span>
                <span class="avg-score" :style="`color: ${scoreColor(avgB)}`">{{ fmt(avgB) }}</span>
                <span class="avg-verdict">{{ sentimentLabel(avgB) }}</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'

const props = defineProps({
  sentimentData: { type: Object, default: null },
  countryA: { type: Object, required: true },
  countryB: { type: Object, required: true },
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['close'])

const colorA = '#3B82F6'
const colorB = '#F97316'

const visible = ref(true)

function dismiss() {
  if (props.loading) return
  visible.value = false
  setTimeout(() => emit('close'), 320)
}

const stages = [
  { key: 'reddit', label: `Scraping Reddit — ${props.countryA.name} & ${props.countryB.name}` },
  { key: 'twitter', label: `Scraping Twitter — ${props.countryA.name} & ${props.countryB.name}` },
  { key: 'news', label: 'Scraping news sources' },
  { key: 'analyse', label: 'Running sentiment analysis' },
  { key: 'done', label: 'Finalising results' },
]

const stageDurations = [3400, 3000, 2000, 1200, 700]

const currentStage = ref(0)
const stageProgress = ref(0)
let progressTimer = null

function startProgress() {
  currentStage.value = 0
  stageProgress.value = 0
  runStage(0)
}

function runStage(index) {
  clearInterval(progressTimer)
  stageProgress.value = 0

  const duration = stageDurations[index] ?? 1000
  const intervalMs = 50
  const totalSteps = duration / intervalMs
  let step = 0

  progressTimer = setInterval(() => {
    step++
    const raw = step / totalSteps
    stageProgress.value = Math.min(96, raw * 100 * (1.6 - raw * 0.7))

    if (step >= totalSteps) {
      clearInterval(progressTimer)
      stageProgress.value = 100
      setTimeout(() => {
        if (!props.loading) return // fetch finished while animating
        if (index < stages.length - 1) {
          currentStage.value = index + 1
          runStage(index + 1)
        }
      }, 220)
    }
  }, intervalMs)
}

function stopProgress() {
  clearInterval(progressTimer)
  currentStage.value = stages.length
  stageProgress.value = 100
}

watch(() => props.loading, (val) => {
  if (val) {
    visible.value = true
    startProgress()
  } else {
    stopProgress()
  }
}, { immediate: true })

onUnmounted(() => clearInterval(progressTimer))

const platforms = [
  { key: 'news', label: 'News', icon: '📰' },
  { key: 'reddit', label: 'Reddit', icon: '💬' },
  { key: 'twitter', label: 'Twitter', icon: '𝕏' },
]

function flagUrl(code2) {
  return `https://flagcdn.com/24x18/${code2?.toLowerCase()}.png`
}

function posPct(score) { return score > 0 ? Math.min(score * 100, 100) : 0 }
function negPct(score) { return score < 0 ? Math.min(Math.abs(score) * 100, 100) : 0 }

const avgA = computed(() => {
  if (!props.sentimentData) return null
  const vals = platforms.map(p => props.sentimentData[p.key]?.a).filter(v => v != null)
  return vals.length ? +(vals.reduce((s, v) => s + v, 0) / vals.length).toFixed(3) : null
})
const avgB = computed(() => {
  if (!props.sentimentData) return null
  const vals = platforms.map(p => props.sentimentData[p.key]?.b).filter(v => v != null)
  return vals.length ? +(vals.reduce((s, v) => s + v, 0) / vals.length).toFixed(3) : null
})

function fmt(v) {
  if (v == null) return '—'
  return (v >= 0 ? '+' : '') + Number(v).toFixed(3)
}
function scoreColor(v) {
  if (v == null) return '#64748b'
  if (v > 0.05) return '#4ade80'
  if (v < -0.05) return '#f87171'
  return '#94a3b8'
}
function sentimentLabel(v) {
  if (v == null) return ''
  if (v > 0.3) return 'Positive'
  if (v > 0.05) return 'Slightly positive'
  if (v < -0.3) return 'Negative'
  if (v < -0.05) return 'Slightly negative'
  return 'Neutral'
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.panel {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 78vh;
  background: #0d1b2a;
  border-top: 1px solid #1e3a5f;
  border-radius: 20px 20px 0 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 -16px 56px rgba(0, 0, 0, 0.7);
  z-index: 30;
  font-family: 'JetBrains Mono', monospace;
}

.panel-enter-active {
  transition: transform 0.55s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease;
}

.panel-leave-active {
  transition: transform 0.3s ease-in, opacity 0.2s ease;
}

.panel-enter-from,
.panel-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

.panel-top.locked {
  cursor: default;
  pointer-events: none;
}

.panel-top {
  flex-shrink: 0;
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid #1e3a5f;
  transition: background 0.15s;
}

.panel-top:hover {
  background: #0f2035;
}

.panel-top:hover .panel-handle {
  background: #3b82f6;
}

.panel-top:hover .dismiss-hint {
  opacity: 1;
}

.panel-handle {
  width: 40px;
  height: 4px;
  background: #1e3a5f;
  border-radius: 2px;
  margin: 12px auto 0;
  transition: background 0.15s;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 20px 14px;
}

.dismiss-hint {
  font-size: 11px;
  color: #3b82f6;
  letter-spacing: 0.04em;
  flex-shrink: 0;
  width: 80px;
  opacity: 0;
  transition: opacity 0.15s;
}

.country-pills {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: center;
}

.country-pill {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 4px 12px;
  border-radius: 20px;
  border: 1px solid;
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
}

.pill-flag {
  width: 18px;
  height: 14px;
  border-radius: 2px;
}

.vs-label {
  font-size: 10px;
  color: #334e68;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.spacer {
  flex: 0 0 80px;
}

.loading-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.progress-stages {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 500px;
}

.stage-row {
  display: flex;
  align-items: center;
  gap: 12px;
  transition: opacity 0.4s;
}

.stage-row.pending {
  opacity: 0.2;
}

.stage-row.done {
  opacity: 0.45;
}

.stage-row.active {
  opacity: 1;
}

.stage-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-done {
  font-size: 13px;
  color: #4ade80;
}

.icon-spinner {
  display: inline-block;
  width: 13px;
  height: 13px;
  border: 2px solid #1e3a5f;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.icon-dot {
  font-size: 20px;
  color: #334e68;
  line-height: 1;
}

.stage-label {
  font-size: 12px;
  color: #94a3b8;
  letter-spacing: 0.02em;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stage-row.active .stage-label {
  color: #e2e8f0;
}

.stage-bar {
  width: 120px;
  height: 3px;
  background: #1e3a5f;
  border-radius: 2px;
  overflow: hidden;
  flex-shrink: 0;
}

.stage-bar-fill {
  height: 100%;
  background: #3b82f6;
  border-radius: 2px;
  transition: width 0.18s ease-out;
}

.stage-done-label {
  font-size: 10px;
  color: #4ade80;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  width: 120px;
  text-align: right;
  flex-shrink: 0;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 28px 0 40px;
  display: flex;
  flex-direction: column;
  gap: 26px;
}

.platform-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 20px;
  animation: rowIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes rowIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.platform-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.platform-icon {
  font-size: 14px;
}

.platform-name {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #64748b;
}

.bar-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.score-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  width: 88px;
  flex-shrink: 0;
  letter-spacing: 0.02em;
}

.score-right {
  justify-content: flex-end;
}

.score-flag {
  width: 16px;
  height: 12px;
  border-radius: 2px;
}

.bar-track {
  flex: 1;
  height: 26px;
  display: flex;
  align-items: center;
  background: #0a1523;
  border: 1px solid #1e3a5f;
  border-radius: 4px;
  overflow: hidden;
}

.bar-half {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 3px;
  padding: 4px 0;
  overflow: hidden;
}

.bar-left {
  align-items: flex-end;
}

.bar-right {
  align-items: flex-start;
}

.bar-fill {
  height: 7px;
  border-radius: 2px;
  min-width: 2px;
  transition: width 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}

.bar-center {
  width: 1px;
  height: 100%;
  background: #1e3a5f;
  flex-shrink: 0;
}

.bar-axis {
  display: flex;
  justify-content: space-between;
  padding: 0 102px;
  font-size: 10px;
  color: #1e3a5f;
  letter-spacing: 0.04em;
}

.divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #1e3a5f, transparent);
}

.averages {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 0 20px;
}

.section-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #64748b;
}

.avg-row {
  display: flex;
  gap: 14px;
}

.avg-card {
  flex: 1;
  background: #091420;
  border: 1px solid;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  animation: rowIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) 240ms both;
}

.avg-flag {
  width: 26px;
  height: 19px;
  border-radius: 3px;
}

.avg-name {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
}

.avg-score {
  font-size: 30px;
  font-weight: 500;
  letter-spacing: -0.02em;
  line-height: 1;
}

.avg-verdict {
  font-size: 10px;
  color: #4a6a8a;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.page {
  font-family: "Roboto", sans-serif;

}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
