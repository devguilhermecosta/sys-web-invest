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
  const adress = document.querySelector('#id_adress');
  const city = document.querySelector('#id_city');
  const uf = document.querySelector('#id_uf');
  inputCep.addEventListener('keyup', searchCep);
  
  function searchCep() {
    let cep = inputCep.value.replace('-', '');

    let url = `http://viacep.com.br/ws/${cep}/json`;

    const request = new XMLHttpRequest();
  
    request.onreadystatechange = function() {
      const defaulClass = 'C-input_xhr';
      if (request.readyState !== 4 && request.status !== 200) {
        adress.value = adress.innerHTML = '';
        city.value = city.innerHTML = '';
        uf.value = uf.innerHTML = '';
        
        adress.classList.remove(defaulClass);
        city.classList.remove(defaulClass);
        uf.classList.remove(defaulClass);
        return;
      } else {
        const json = JSON.parse(request.responseText);

        
        adress.innerHTML = adress.value = json.logradouro || '';
        city.value = city.innerHTML = json.localidade || '';
        uf.value = uf.innerHTML = json.uf || '';
        
        city.classList.add(defaulClass);
        adress.classList.add(defaulClass);
        uf.classList.add(defaulClass);
      }
    }
    request.open('GET', url, true);
    request.send();
  }
} catch(e) {};
})();


// Function for change btn value into login page
(() => {
  try {
    const loginForm = document.querySelector('.C-login_form');
    let btnLogin = document.querySelector('#btn-login');
    btnLogin.addEventListener('click', function(event) {
      event.preventDefault();
    
      btnLogin.value = 'entrando...';
      loginForm.submit();
    })
  } catch(e){};
})();

// Function for change btn value into register page
(() => {
  try {
    const registerForm = document.querySelector('.C-form_register_form');
    let btnRegister = document.querySelector('#btn-register');
    btnRegister.addEventListener('click', function(event) {
      event.preventDefault();
    
      btnRegister.value = 'registrando...';
      registerForm.submit();
    })
  } catch(e){};
})();

// Function for change btn value into register page
(() => {
  try {
    const registerProfileForm = document.querySelector('.C-login_form');
    let btnCreateProfile = document.querySelector('.C-login_button[value=finalizar]');
    btnCreateProfile.addEventListener('click', function(event) {
      event.preventDefault();
    
      btnCreateProfile.value = 'criando perfil...';
      registerProfileForm.submit();
    })
  } catch(e){};
})();

// prevent default for form aplly and redeem fixed income
(() => {
  try {
    const formApply = document.querySelector('#form-apply');
    const buttonSubmitFormApply = document.querySelector('#btn-form-apply');
  
    buttonSubmitFormApply.addEventListener("click", function(event) {
      event.preventDefault();
  
      const body = document.body;
      const divContainer = document.createElement('div');
      const divConfirm = document.createElement('div');
      const divFlexButton = document.createElement('div');
      const text = document.createElement('p');
      const buttonConfirm = document.createElement('button');
      const buttonCancel = document.createElement('button');
  
      buttonConfirm.innerHTML = 'Confirmar';
      buttonCancel.innerHTML = 'Cancelar';
      
      text.innerHTML = 'Deseja confirmar a aplicação?'
      text.style.color = 'white';
      
      divContainer.classList.add('C-product_form_container');
      divConfirm.classList.add('C-product_form_confirm');
      divFlexButton.classList.add('C-product_form_buttons');
      
      divFlexButton.appendChild(buttonCancel);
      divFlexButton.appendChild(buttonConfirm);
      divConfirm.appendChild(text);
      divConfirm.appendChild(divFlexButton);
      divContainer.appendChild(divConfirm);
      body.appendChild(divContainer);
  
      buttonConfirm.addEventListener('click', function() {
        formApply.submit();
      })
  
      buttonCancel.addEventListener('click', function() {
        body.removeChild(divContainer);
      })
    })
  } catch(e){}
})();