export async function getCurrentTab() {
  let queryOptions = { active: true, currentWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

export async function currTabUrl() {
  return chrome.scripting
    .executeScript({
      target: { tabId: (await getCurrentTab()).id },
      func: () => {
        return document.URL
      },
    })
    .then((injectionResults) => {
      let url = null;
      for (const { result } of injectionResults) {
        url = new URL(result).origin;
      }
      return url;
    });
}


export async function injectFormData(formData) {
  return chrome.scripting
    .executeScript({
      target: { tabId: (await getCurrentTab()).id },
      func: setFormData,
      args: [formData]
    })
}


function customScript() {
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
        });  
      }  
    )  
    .catch(function(err) {  
      console.log('Fetch Error :-S', err);  
    });
}

function setFormData(formData){ 
  // Таблица РУ
  document.getElementsByName("q_no_ru")[0].value = formData.roszdrav_register || "2020/11872"
  document.getElementsByName("q_model")[0].value = formData.roszdrav_name || formData.nomenclature_name
  //
  document.getElementById("id_type-1").checked = true
  document.getElementById("id_dt_release").value = ""
  document.getElementById("id_dt_manufacture").value = formData.manuf_date
  document.getElementById("id_model_series").value = formData.batch
  document.getElementById("id_model_part").value = formData.batch
  document.getElementById("id_quantity").value = Object.values(formData.docs_list).map((el => el.count)).join(', ')
  //
  document.getElementById("id_no").value = Object.values(formData.docs_list).map((el => el.doc_number)).join(', ')
  document.getElementById("id_dt").value = formData.docs_list[0].doc_date
}
