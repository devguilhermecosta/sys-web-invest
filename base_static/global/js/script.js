(() => {
  const formInput = document.querySelectorAll('.C-login_input');
  
  formInput.forEach((input) => {
    const inputLength = input.value.length;
    const labelSister = input.nextElementSibling;
    const className = 'C-login_input_active';

    if (inputLength >= 1) {
      labelSister.classList.add(className);
    }

    try {
      input.addEventListener('change', function() {
        const inputLengthInside = input.value.length;
        if (inputLengthInside >= 1) {
          labelSister.classList.add(className);
        } else {
          labelSister.classList.remove(className);
        }
      }) 
    }
    catch(e){}
  })
})();

// change eye from dashboard intro
(() => {
  try{
    const eyeInput = document.querySelector('#show-invest');
    const eyeIcon = document.querySelector('.eye-icon');
  
    eyeInput.addEventListener('change', function() {
      if (eyeInput.checked) {
        eyeIcon.innerHTML = 'visibility_off';
      } else if (!eyeInput.checked) {
        eyeIcon.innerHTML = 'visibility';
      }
    })
  }catch(e){};
})();

//

const inputCep = document.getElementById('id_cep');
inputCep.addEventListener('change', searchCep);

function searchCep() {
  let cep = inputCep.value.replace('-', '');
  let url = 'http://viacep.com.br/ws/' + cep + '/json';
  let xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        json = JSON.parse(xhr.responseText)
        console.log(json);
      }
    }
  }
  xhr.send();
}

// https://blog.matheuscastiglioni.com.br/requisicoes-ajax-com-javascript/#:~:text=O%20Javascript%20nativo%20possui%20um,protoc%C3%B3los%20HTTP%2C%20FILE%20e%20FTP.