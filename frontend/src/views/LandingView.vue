<template>
  <div class="landing">

    <img class="bg-globe" :src="earthImage" alt="" />
    <img class="bg-layer-secondary" :src="backgroundImage" alt="" />

    <div class="overlay" />

    <router-link to="/" class="brand">
      <img :src="logoImage" alt="Worldview Logo" class="logo" />
    </router-link>

    <main class="content">
      <h1 class="title">
        Understand Global Perception<br />
      </h1>
      <p class="subtitle">
        Real-time country sentiment powered by global social data
      </p>

      <router-link to="/compare" class="cta-btn">
        <span class="cta-text">Explore Worldview</span>
        <span class="cta-arrow">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M3 9h12M10 4l5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
        </span>
      </router-link>
    </main>

    <div class="scanlines" />

  </div>
</template>

<script setup>
import earthImage from '../assets/Earth.png'
import backgroundImage from '../assets/Background.png'
import logoImage from '../assets/LogoWithText.png'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.landing {
  font-family: 'Syne', sans-serif;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #060e18;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-layer-secondary {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.4;
  pointer-events: none;
  z-index: 0;
}

.bg-globe {
  z-index: 1;
  position: absolute;
  width: min(200vh, 200vw);
  height: min(200vh, 200vw);
  top: 105%;
  left: 50%;
  translate: -50% -50%;
  object-fit: contain;
  opacity: 0.55;
  filter: saturate(0.7) brightness(0.8);
  animation: spin 120s linear infinite;
  pointer-events: none;
}

@keyframes spin {
  from {
    rotate: 0deg;
  }

  to {
    rotate: 360deg;
  }
}

.overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 70% at 50% 50%, transparent 30%, #060e18 100%),
    linear-gradient(to bottom, #060e18 0%, transparent 15%, transparent 80%, #060e18 100%),
    linear-gradient(to right, #060e18 0%, transparent 12%, transparent 88%, #060e18 100%);
  pointer-events: none;
}

.scanlines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(0deg,
      transparent,
      transparent 2px,
      rgba(0, 0, 0, 0.07) 2px,
      rgba(0, 0, 0, 0.07) 4px);
  pointer-events: none;
}

.brand .logo {
  height: 52px;
  width: auto;
  display: block;
}

.brand {
  position: absolute;
  top: 28px;
  left: 32px;
  z-index: 10;
  text-decoration: none;
  animation: fadeDown 0.8s ease both;
}

.content {
  position: relative;
  z-index: 10;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-top: -40px;
}

.title {
  font-size: clamp(30px, 4vw, 66px);
  font-weight: 300;
  line-height: 1.55;
  color: #f1f5f9;
  letter-spacing: -0.02em;
  opacity: 0;
  animation: fadeUp 0.8s 0.4s ease forwards;
  margin-bottom: -22px;
}

.subtitle {
  font-family: "Roboto", sans-serif;
  font-size: clamp(14px, 1.1vw, 18px);
  color: #728eb5;
  line-height: 1.6;
  font-weight: 400;
  opacity: 0;
  animation: fadeUp 0.8s 0.6s ease forwards;
  margin-bottom: 164px;
  padding-bottom: 4px;
}

.cta-btn {
  margin-top: 14px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 32px;
  border: 1px solid #1e3a5f;
  border-radius: 12px;
  background: #0d1b2a;
  color: #e2e8f0;
  text-decoration: none;
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.03em;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  opacity: 0;
  animation: fadeUp 0.8s 0.85s ease forwards;
  transition: border-color 0.25s, color 0.25s, box-shadow 0.25s;
}

.cta-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #3b82f618, #38bdf812);
  opacity: 0;
  transition: opacity 0.25s;
}

.cta-btn:hover {
  border-color: #3b82f6;
  color: #fff;
  box-shadow: 0 0 24px #3b82f633, 0 4px 16px rgba(0, 0, 0, 0.4);
}

.cta-btn:hover::before {
  opacity: 1;
}

.cta-text {
  position: relative;
  z-index: 1;
}

.cta-arrow {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  transition: transform 0.25s;
}

.cta-btn:hover .cta-arrow {
  transform: translateX(4px);
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(18px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
