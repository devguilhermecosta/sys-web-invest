// function for quit the suMenu
function closeMenu(id_submenu) {
  const menuMobile = document.querySelectorAll('.C-menu_mobile')[0];
  const subMenu = document.querySelector(`#${id_submenu}`);

  if (subMenu) {
    menuMobile.addEventListener("click", function() {
      if (subMenu.checked) {
        subMenu.checked = false;
      }
    })
  }
}
closeMenu('C-menu_ativos_checkox');
closeMenu('C-menu_admin_checkox');

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
  text.style.whiteSpace = 'nowrap';
  text.style.textAlign = 'center';
  text.style.padding = '10px';
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


// FIIs form for receipt income
(() => {
  const btnFiisReceiptIncome = document.querySelector('#fiis_btn_income');

  if (btnFiisReceiptIncome) {
    btnFiisReceiptIncome.addEventListener("click", function() {
      
    })
  }
})();

// form fiis receiv profis
(() => {
  const formFiisReceivProfis = document.querySelector('#form_fii_receiv_profis');

  if (formFiisReceivProfis) {
    formFiisReceivProfis.addEventListener("submit", function(event) {
      event.preventDefault();

      const form = new FormData(formFiisReceivProfis);
      const product = parseInt(form.get('product_id'));
      const select = formFiisReceivProfis.querySelector('#id_product_id');
      const productDesc = select.options[select.selectedIndex].innerHTML;
      const date = form.get('date');
      const value = parseFloat(form.get('value'));

      const body = document.body;
      let container = createDefaultContainer();

      if (product >= 1 && date.length > 0 && value > 0) {
        const formatedValue = value.toLocaleString(
          'pt-br',
          {
            style: 'currency',
            currency: 'BRL'
          });
        const frame = createDefaultFrame();
        const buttonContainer = createDivFlexButton();

        const message = createTextElement(
          'white',
          `<p>Deseja salvar o recebimento</p>
          <p>de ${formatedValue}</p>
          <p>para o produto ${productDesc}?</p>`,
          );
        
        const buttonConfirm = createButton('confirmar');
        const buttonCancel = createButton('cancelar');

        buttonContainer.appendChild(buttonConfirm);
        buttonContainer.appendChild(buttonCancel);
        frame.appendChild(message);
        frame.appendChild(buttonContainer);
        container.appendChild(frame)
        body.appendChild(container);

        buttonContainer.addEventListener("click", () => {
          body.removeChild(container);
        });

        buttonConfirm.addEventListener("click", function() {
          let urlPath = `/ativos/fiis/gerenciar-proventos/${product}/receber/`;
          let token = formFiisReceivProfis.querySelectorAll('input')[0].value;
          let labels = formFiisReceivProfis.querySelectorAll('.C-login_label');

          let xmlr = new XMLHttpRequest();

          xmlr.onreadystatechange = function() {
            if (xmlr.readyState === 4 && xmlr.status == 200) {
              let result = document.querySelector('#result');
              result.classList.add('messages');
              result.classList.add('message_success');
              result.innerHTML = 
              `Recebimento de ${formatedValue} lançado com sucesso para ${productDesc}`;
              formFiisReceivProfis.reset();
              labels.forEach((l) => {l.classList.remove('C-login_input_active')});
            }
          }
          xmlr.open('POST', urlPath);
          xmlr.setRequestHeader('X-CSRF-TOKEN', token)
          xmlr.send(form);
        })
        return;
      }

      createMessageAlert('white', 'Informe todos os dados');
    
    })
  }
})();

// new ajax
function createDataTable(date, code, value, handler, p_id) {
  const tableBody = document.querySelector('#table-body');
  let tableRow = document.createElement('tr');
  let tableDate = document.createElement('td');
  let tableCode = document.createElement('td');
  let tableValue = document.createElement('td');
  let tableHandler = document.createElement('td');
  let tableId = document.createElement('td');


  tableDate.innerHTML = date;
  tableCode.innerHTML = code;
  tableValue.innerHTML = value;
  tableHandler.innerHTML = handler;
  tableHandler.style.color = '#0f6e6a';
  tableId.innerHTML = p_id;

  tableRow.appendChild(tableDate);
  tableRow.appendChild(tableCode);
  tableRow.appendChild(tableValue);
  tableRow.appendChild(tableHandler);
  tableRow.appendChild(tableId);

  tableBody.appendChild(tableRow);
}

function createProfitsTable() {
  const elem = document.querySelector('#url');
  const path = elem.dataset.url;
  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState == 4 && request.status == 200) {
      const result = JSON.parse(request.responseText);
      const data = result.data;
      let date;

      data.map((el) => {
        date = new Date(el.date);

        createDataTable(
          date.toLocaleDateString(
            'pt-BR',
            {'timeZone': 'UTC'},
          ),
          el.product,
          el.value.toLocaleString(
            'pt-BR',
            {
              style: 'currency',
              currency: 'BRL',
            },
          ),
          el.handler === 'profits' ? 'PROVENTOS' : '',
          el.history_id);
      }
      )
    }
  }
  request.open('GET', path.toString(), true);
  request.send();
}

createProfitsTable();