// animate input field
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


// AJAX for Profile CEP
(() => {
try {
  const inputCep = document.getElementById('id_cep');
  inputCep.addEventListener('change', searchCep);
  
  function searchCep() {
    let cep = inputCep.value.replace('-', '');
    const adress = document.querySelector('#id_adress');
    const city = document.querySelector('#id_city');
    const uf = document.querySelector('#id_uf');
  
    let url = `http://viacep.com.br/ws/${cep}/json`;
    let request = new XMLHttpRequest();
  
    request.open('GET', url, true);
    
    request.onreadystatechange = function() {
        if (request.readyState === 4) {
          if (request.status === 200) {
            const json = JSON.parse(request.responseText);
    
            adress.innerHTML = `${json.logradouro}`;
            adress.value = `${json.logradouro}`;
    
            city.parentNode.classList.toggle('C-input_xhr');
            city.value = json.localidade;
            city.innerHTML = json.localidade;
    
            uf.parentNode.classList.toggle('C-input_xhr');
            uf.value = json.uf;
            uf.innerHTML = json.uf;
          }
        }
      }
      request.send();
  }
} catch(e) {};
})();
