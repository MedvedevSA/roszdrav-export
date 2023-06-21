<template lang="">
  <div class="p-2 bg-sky-100">
    <p class="text-md">Файл: {{ curFileName }}</p>
  </div>
  <div class="p-1 bg-sky-50 flex">
    <select v-model="selectedFile" sise="2" class="file-select bg-white">
      <option v-for="item in fileSelectOptions" :key="item" :value="item">
        {{ item }}
      </option>
    </select>
    <button class="p-1 m-1 bg-cyan-400" @click="onSelectSubmit">Выбрать</button>

    <label for="files" class="p-1 m-1 bg-cyan-400">Загрузить файл</label>
    <input
      id="files"
      type="file"
      name="files"
      accept=".xlsx"
      style="visibility: hidden"
      multiple
      @change="uploadFile"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";

const baseUrl = "http://localhost:8000/";
const inputFile = ref(null);
const fileSelectOptions = ref([]);
const selectedFile = ref(null);
const curFileName = ref(null);

async function uploadFile(evt) {
  let formData = new FormData();
  formData.append("files", evt.target.files[0]);

  let response = await fetch(baseUrl + "upload_file", {
    method: "POST",
    body: formData,
  })
    .then(async function (response) {
      alert("Файл загружен");
      console.log(response);
      console.log(await response.json());
    })
    .catch(function (error) {
      alert("Что то пошло не так");
      console.log(error);
    });

  let result = await response.json();

  alert(result.message);
}

async function getCurrentFileName() {
  return await fetch(baseUrl + "current_file").then(async (response) => {
    return await response.json();
  });
}

async function fetchFiles() {
  const data = await fetch(baseUrl + "files").then(async (response) => {
    return await response.json();
  });
  return data;
}

async function onSelectSubmit() {
  let response = await fetch(baseUrl + "set_file", {
    method: "POST",
    body: selectedFile.value,
  })
    .then(async (response) => {
      return await response.json();
    })
    .catch(async (error) => {
      console.log(error);
    });
}
onMounted(async () => {
  fileSelectOptions.value = await fetchFiles();
  curFileName.value = await getCurrentFileName();
  // console.log(fileSelectOptions.value[0])
});
</script>

<style>
.file-select {
  overflow: scroll;
}
</style>
