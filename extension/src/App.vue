<template>
  <div class="flex-col w-96">
    <HeaderNav :curFileName="'asd'"/>
    <MainBody />
    <!-- <a href="https://vitejs.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a> -->
  </div>
</template>

<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
import MainBody from './components/MainBody.vue'

</script>

<style >
</style>
