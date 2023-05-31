<template>
  <template v-if="isTargetTab">
    <div>
      <h1>{{ msg }} {{}}</h1>

      <div class="card">
        <button type="button" @click="onClick">count is {{ count }}</button>
        <p>
          Edit
          <code>components/HelloWorld.vue</code> to test HMR
        </p>
      </div>

      <p>
        Check out
        <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
          >create-vue</a
        >, the official Vue + Vite starter
      </p>
      <p>
        Install
        <a href="https://github.com/vuejs/language-tools" target="_blank"
          >Volar</a
        >
        in your IDE for a better DX
      </p>
      <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
    </div>
  </template>
  <template v-else>
    <h4>Перейти:</h4>
    <a :href="targetSiteUrl" target="_blank"
      >Федеральная служба по надзору в сфере здравоохранения</a
    >
  </template>
</template>

<script setup>
import { currTabUrl } from "../scripts/inject.js";
import { ref, onMounted } from "vue";

const count = ref(0);
const targetSiteUrl = "https://www.roszdravnadzor.gov.ru";
const isTargetTab = ref(null);

async function onClick() {
  count.value++;
  console.log(await currTabUrl());
}

defineProps({
  msg: String,
});

onMounted(async () => {
  isTargetTab.value = (await currTabUrl()) === targetSiteUrl;
});
</script>

<style scoped>
.read-the-docs {
  color: #888;
}

h1 {
  width: 200px;
}
</style>
