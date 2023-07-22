// function for quit the suMenu
(() => {
  const menuMobile = document.querySelectorAll('.C-menu_mobile')[0];
  const subMenu = document.querySelector('#C-menu_ativos_checkox');

  if (menuMobile) {
    menuMobile.addEventListener("click", function() {
      if (subMenu.checked) {
        subMenu.checked = false;
      }
    })
  }
})();


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


// functions for create html elements
function createDefaultContainer() {
  const divContainer = document.createElement('div');
  divContainer.classList.add('C-product_form_container');
  return divContainer;
}

function createDefaultFrame() {
  const frame = document.createElement('div');
  frame.classList.add('C-product_form_confirm');
  return frame;
}

function createButton(value) {
  const button = document.createElement('button');
  button.classList.add('C-product_form_btn');
  button.innerHTML = value;
  return button;
}

function createDivFlexButton() {
  const divFlexButton = document.createElement('div');
  divFlexButton.classList.add('C-product_form_buttons');
  return divFlexButton;
}

function createTextElement(color, message) {
  const text = document.createElement('p');
  text.style.color = color;
  text.innerHTML = message;
  return text;
}


// create message alert
function createMessageAlert(color, message) {
  const body = document.body;
  const container = createDefaultContainer();
  const frame = createDefaultFrame();
  const text = createTextElement(color, message);
  const button = createButton('OK');

  frame.appendChild(text);
  frame.appendChild(button);
  container.appendChild(frame);
  body.appendChild(container);

  button.addEventListener('click', function() {
    body.removeChild(container);
  })
}


// create form confirmation fixed income
function createFormFixedIncome(form, buttonInput, input, message, messageAlert) {
  const formApply = form;
  const buttonSubmit = buttonInput;
  const inputValue = input;

  buttonSubmit.addEventListener('click', function(event) {
    event.preventDefault();

    function createFormConfirmation() {
      const body = document.body;
      const container = createDefaultContainer();
      const frame = createDefaultFrame();
      const text = createTextElement('white', message);
      const divFlex = createDivFlexButton();
      const buttonConfirm = createButton('Confirmar');
      const buttonCancel = createButton('Cancelar');

      divFlex.appendChild(buttonCancel);
      divFlex.appendChild(buttonConfirm);
      frame.appendChild(text);
      frame.appendChild(divFlex);

      container.appendChild(frame);
      body.appendChild(container);

      buttonConfirm.addEventListener('click', function() {
        formApply.submit();
        body.removeChild(container);
      })
      buttonCancel.addEventListener('click', function() {
        body.removeChild(container);
      })
    }

    inputValue.value === '' ? createMessageAlert('white', messageAlert) : createFormConfirmation();

    return inputValue;
  })
}


// prevent default form aplly
(() => {
  try {
    const form = document.querySelector('#form-apply');
    const button = document.querySelector('#btn-form-apply');
    const input = document.querySelectorAll('.C-fixed_income_input')[0];
    createFormFixedIncome(form, button, input, 'deseja confirmar a aplicação?', 'informe um valor');
  } catch(e){}
})();


// prevent default form redeem
(() => {
  try {
    const form = document.querySelector('#form-redeem');
    const button = document.querySelector('#btn-form-redeem');
    const input = document.querySelectorAll('.C-fixed_income_input')[1];
    createFormFixedIncome(form, button, input, 'deseja confirmar o resgate?', 'informe um valor');
  } catch(e){}
})();
