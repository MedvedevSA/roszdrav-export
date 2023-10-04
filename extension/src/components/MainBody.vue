<template>
  <template v-if="isTargetTab">
    <div class="flex-col p-2">
      <div class="flex">

        <button
          type="button"
          class="p-2 m-2 rounded-sm bg-blue-300 float-right"
          @click="onClick"
        >
          Заполнить
        </button>

        <div class="flex m-1 p-1">

        <button
          @click="countIncr(-1)"
          type="button"
          class="ml-2 w-8 bg-blue-200 rounded-l-sm border"
        >
          -
        </button>

        <!-- <div class="m-2 p-2 bg-cyan-400">
          {{ count }}
        </div> -->
        <input
          v-model="count"
          type="number"
          class="border border-1 w-12"
        />

        <button
          @click="countIncr(1)"
          type="button"
          class="mr-2 w-8 bg-blue-200 rounded-r-sm border"
        >
          +
        </button>
        </div>       

        <div class="p-1 m-2 text-sm rounded-md border-black border">
          <p><i>Всего записей:</i> {{ formData.length }}</p>
        </div>
      </div>


      <div v-for="value in Object.values(formData[count-1])" class="p-2">
        {{ value }}
      </div>
    </div>
  </template>

  <template v-else>
    <div class="p-2 bg-slate-400 text-xl font-bold">
      <h4>Перейти:</h4>
      <a
        class="text-cyan-900 hover:underline"
        :href="targetSiteUrl[0]"
        target="_blank"
        >Федеральная служба по надзору в сфере здравоохранения</a
      >
    </div>
  </template>
</template>

<script setup>
import { currTabUrl, injectFormData } from "@/scripts/inject.js";
import { ref, onMounted, watch } from "vue";

const count = ref(0);
const formData = ref([]);

const targetSiteUrl = [
  "https://roszdravnadzor.gov.ru",
  "https://www.roszdravnadzor.gov.ru",
  "https://gosuslugi.roszdravnadzor.gov.ru",
];

const isTargetTab = ref(null);

// function validateCount(evt) {
//   console.log(evt);
//   if (count.value < 0) {
//     count.value = 0;
//   } else if (count.value > formData.value.length) {
//     count.value = formData.value.length - 1;
//   }
// }
function countIncr(incr) {
  console.log(count)

  let newVal = count.value + incr
  newVal = newVal <= formData.value.length ? newVal : count.value
  newVal = newVal > 0 ? newVal : count.value

  count.value = Number(newVal)
  localStorage.setItem("count", count.value);
}

function restoreCount() {
  count.value = localStorage.getItem('count') || 1
}

async function onClick() {
  console.log();
  await getRawData();
  await injectFormData(formData.value[count.value - 1]);
}

async function getRawData() {
  const url = "http://localhost:8000/raw_data";

  let data = await fetch(url).then(async (resp) => {
    return await resp.json();
  });
  return data;
}

onMounted(async () => {
  const tabUrl = await currTabUrl();
  isTargetTab.value = targetSiteUrl.includes(tabUrl);
  formData.value = await getRawData();
  console.log(formData.value);
  restoreCount();
  console.log('on custom')
});
</script>

<style></style>
