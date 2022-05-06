//let injectFile = document.getElementById('inject-file');
let injectFunction = document.getElementById('inject-function');

async function getCurrentTab() {
  let queryOptions = { active: true, currentWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

//injectFile.addEventListener('click', async () => {
  //let tab = await getCurrentTab();

  //chrome.scripting.executeScript({
    //target: {tabId: tab.id},
    //files: ['content-script.js']
  //});
//});

//const inputElement = document.getElementById("input-file");

//inputElement.addEventListener("change", handleFiles, false);
//function handleFiles() {
  //const fileList = this.files; /* now you can work with the file list */
  //console.log(fileList)
  //alert(fileList)
//}

function customScript() {

  let url = 'https://192.168.1.193:8000/zdrav';

  fetch(url)  
    .then(  
      function(response) {  
        if (response.status !== 200) {  
          console.log('Looks like there was a problem. Status Code: ' +  
            response.status);  
          return;  
        }

        // Examine the text in the response  
        response.json().then(function(data) {  
          // Первая страница
          /**
          * 
          document.getElementById("id_f").value = test
          document.getElementById("id_i").value = test
          document.getElementById("id_o").value = test
          document.getElementById("id_email").value = test
          document.getElementById("id_phone").value = test
  
          */
          document.getElementById("id_type-1").checked = true

          document.getElementById("id_dt_release").value = ""
          document.getElementById("id_dt_manufacture").value = data.dt_manufacture
          document.getElementById("id_model_series").value = data.bach
          document.getElementById("id_model_part").value = data.bach
          document.getElementById("id_quantity").value = data.quantity


          // Таблица РУ

          document.getElementsByName("q_no_ru")[0].value = "2020/11872"
          document.getElementsByName("q_model")[0].value = data.name

          document.getElementById("id_no").value = data.id_no
          document.getElementById("id_dt").value = data.id_dt
        });  
      }  
    )  
    .catch(function(err) {  
      console.log('Fetch Error :-S', err);  
    });
}

function showAlert(givenName) {
  alert(`Hello, ${givenName}`);
}




injectFunction.addEventListener('click', async () => {

  let tab = await getCurrentTab();
  chrome.scripting.executeScript({
      target: {tabId: tab.id},
      func: customScript,
    });

  //input_series = tab.getElementById("id_model_series")
  //input_series.value = "asd"
  /**
   * 
  let name = 'World';
  chrome.scripting.executeScript({
    target: {tabId: tab.id},
    func: showAlert,
    args: [tab.title]
  });
   */
});
