import { createDefaultContainer } from './src/modules.js';
import { createDefaultFrame } from './src/modules.js';
import { createButton } from './src/modules.js';
import { createDivFlexButton } from './src/modules.js';
import { createTextElement } from './src/modules.js';
import { createMessageAlert } from './src/modules.js';


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