formElem.onsubmit = async (e) => {
    e.preventDefault();

    let response = await fetch('/testpost', {
      method: 'POST',
      body: new FormData(formElem)
    }).then(function(response){
        console.log(response)
    }).catch(function(error){
        console.log(error)
    });

    let result = await response.json();

    alert(result.message);
};


fileForm.onsubmit = async (e) => {
    e.preventDefault();

    let response = await fetch('/uploadxlsxdata/', {
      method: 'POST',
      body: new FormData(fileForm)
    }).then(function(response){
        alert("Файл загружен")
        console.log(response)
    }).catch(function(error){
        alert("Что то пошло не так")
        console.log(error)
    });

    let result = await response.json();

    alert(result.message);
};