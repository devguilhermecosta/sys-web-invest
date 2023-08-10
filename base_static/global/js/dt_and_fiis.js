import { createMessageAlert } from './src/modules.js';
import { createFormSubmit } from './src/utils.js';


// create form confirmation fixed income
function createFormFixedIncome(form, buttonSubmit, inputValue, inputDate, message, messageAlert) {
  buttonSubmit.addEventListener("click", function() {
    form.addEventListener("submit", (e) => {e.preventDefault();})
    !inputValue.value || !inputDate.value ? createMessageAlert('white', messageAlert) : createFormSubmit(form, message);

    return [inputValue, inputDate]
  });
}


// prevent default form aplly
(() => {
  try {
    const form = document.querySelector('#form-apply');
    const button = document.querySelector('#btn-form-apply');
    const inputValue = form.querySelector('#id_value');
    const inputDate = form.querySelector('#id_date');
    createFormFixedIncome(form, button, inputValue, inputDate, 'deseja confirmar a aplicação?', 'informe uma data e valor');
  } catch(e){}
})();


// prevent default form redeem
(() => {
  try {
    const form = document.querySelector('#form-redeem');
    const button = document.querySelector('#btn-form-redeem');
    const inputValue = form.querySelector('#id_value');
    const inputDate = form.querySelector('#id_date');
    createFormFixedIncome(form, button, inputValue, inputDate, 'deseja confirmar o resgate?', 'informe uma data e valor');
  } catch(e){}
})();


// delete the fixed income object
(() => {
  const inputSupbmit = document.querySelector('#btn_delete');

  if (inputSupbmit) {
    const parentForm = inputSupbmit.parentElement;
    inputSupbmit.addEventListener("click", function() {
      parentForm.addEventListener("submit", (e) => {e.preventDefault()});
      createFormSubmit(
        parentForm,
        `Deseja realmente deletar este ativo?
        Se você deletá-lo, todo seu histórico de aplicação, resgate
        e recebimento de proventos será deletado também.`,
        )
    })
  }
})();


// function for fixed income history delete
(() => {
  const linkDelete = document.querySelectorAll('.fi_h_delete');

  if (linkDelete) {
    linkDelete.forEach((link) => {

      link.addEventListener("click", function() {
        const parentForm = link.parentElement;
        parentForm.addEventListener("submit", (e) => {e.preventDefault();})
        createFormSubmit(
          parentForm,
          'deseja realmente deletar este histórico?'
        )
      })
    })
  }
})();