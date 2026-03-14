<script setup>
import LandingView from './views/LandingView.vue'
</script>

<template>
  <router-view v-slot="{ Component, route }">
    <Transition :name="route.meta.transition || ''" mode="out-in">
      <component :is="Component" />
    </Transition>
  </router-view>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
