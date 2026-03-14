<script setup>
import { ref } from 'vue'
import countryList from '../assets/countries.json'

const countries = ref(countryList)
const firstCountry = ref('')
const secondCountry = ref('')
</script>

<template>
  <aside class="sidebar">
    <h2>Compare</h2>
    <div class="compare-container">
      <div class="country-box">
        <label for="country-one">Country 1</label>
        <input list="country-options" id="country-one" v-model="firstCountry" />
      </div>

      <div class="arrow-down"><span>↓</span></div>

      <div class="country-box">
        <label for="country-two">Country 2</label>
        <input list="country-options" id="country-two" v-model="secondCountry" />
      </div>

      <datalist id="country-options">
        <option v-for="c in countries" :key="c.code3" :value="c.name">{{ c.name }}</option>
      </datalist>
    </div>
  </aside>

</template>

<style scoped>
.sidebar {
  width: 100%;
  height: 100vh;

  padding: 20px;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;

  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);

  overflow-y: auto;
}

.compare-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

.country-box {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 12px;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.arrow-down {
  text-align: center;
  font-size: 20px;
  margin: -5px 0;
}

body {
  margin: 0;
  padding: 0;
}
</style>
