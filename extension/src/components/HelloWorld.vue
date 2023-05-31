<template>
  <template v-if="isTargetTab">
    <div>
      <h1>{{ msg }} {{}}</h1>
      <div>
        <button type="button" @click="onClick">count is {{ count }}</button>
      </div>

    </div>
  </template>
  <template v-else>
    <h4>Перейти:</h4>
    <a :href="targetSiteUrl[0]" target="_blank"
      >Федеральная служба по надзору в сфере здравоохранения</a
    >
  </template>
</template>

<script setup>
import { currTabUrl } from "../scripts/inject.js";
import { ref, onMounted } from "vue";

const count = ref(0);
const targetSiteUrl = [
  'https://roszdravnadzor.gov.ru',
  'https://www.roszdravnadzor.gov.ru',
  'https://gosuslugi.roszdravnadzor.gov.ru',
]

const isTargetTab = ref(null);

async function onClick() {
  count.value++;
  console.log(await currTabUrl());
}

defineProps({
  msg: String,
});

onMounted(async () => {
  const tabUrl = await currTabUrl()
  isTargetTab.value = targetSiteUrl.includes(tabUrl);
});
</script>

<style>
</style>
