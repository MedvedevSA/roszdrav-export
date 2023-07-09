<template lang="">
  <div class="flex justify-between items-stretch gap-2 p-1 bg-sky-50">
    <div class="flex justify-center items-stretch gap-2">
      <div class="bg-white rounded">
        <select v-model="selectedFile" required class="h-full w-40 p-2 bg-white">
          <option v-for="item in fileSelectOptions" :key="item" :value="item">
            {{ item }}
          </option>
        </select>
      </div>

      <div class="bg-blue-300 rounded">
        <button class="h-full p-2" @click="setCurrentFile">
          Выбрать
        </button>
      </div>
    </div>

    <div class="bg-blue-300 rounded">
      <p class="h-full p-2 text-center">
        <label for="files">Загрузить файл</label>
        <input
          id="files"
          type="file"
          name="files"
          accept=".xlsx"
          class="max-w-0"
          style="visibility: hidden"
          multiple
          @change="uploadFile"
        />
      </p>
    </div>
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



async function fetchFiles() {
  return await fetch(baseUrl + "files").then(async (response) => {
    return await response.json();
  });
}

async function getCurrentFileName() {
  return await fetch(baseUrl + "current_file").then(async (response) => {
    return await response.json();
  });
}

async function setCurrentFile() {
  await fetch(baseUrl + "set_file", {
    method: "POST",
    body: selectedFile.value,
  })
    .then(async (response) => {
      alert("Выбран файл: " + selectedFile.value);
      return await response.json();
    })
    .catch(async (error) => {
      console.log(error);
    });
}

onMounted(async () => {
  fileSelectOptions.value = await fetchFiles();
  curFileName.value = await getCurrentFileName();
  selectedFile.value = curFileName.value;
});
</script>
