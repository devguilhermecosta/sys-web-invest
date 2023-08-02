import { createDefaultContainer, createDefaultFrame, createTextElement } from "./modules.js";
import { createButton, createDivFlexButton } from "./modules.js";


// function for link history edit
export function createHistoryLinkEdit(id) {
  const path = `historico/${id}/editar/`;
  let link = document.createElement('a');
  link.setAttribute('href', path);
  return link
}


// function for link history delete
export function createHistoryLinkDelete(id) {
  const path = `historico/${id}/deletar/`;
  const token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  
  const paramsTokenInput = {
    type: 'hidden',
    value: token,
    name: 'csrfmiddlewaretoken',
  }
  let tokenInput = document.createElement('input');
  for (const [k, v] of Object.entries(paramsTokenInput)) {
    tokenInput.setAttribute(k, v);
  }

  const paramsForm = {
    action: path,
    method: 'POST',
    enctype: 'multipart/form-data',
  }
  let form = document.createElement('form');
  for (const [key, value] of Object.entries(paramsForm)) {
    form.setAttribute(key, value);
  }
  form.appendChild(tokenInput);

  return form;
}


// function box confirmation history delete
export function confirmationBoxDeleteHistory(elem, code) {
  const form = elem.parentElement;
  const container = createDefaultContainer();
  const frame = createDefaultFrame()
  const message = createTextElement(
    'white', 
    `<p>deseja mesmo deletar</p>
    <p>este provento de ${code}?</p>`,
    );
  const buttonContainer = createDivFlexButton();
  const buttonCancel = createButton('cancelar');
  const buttonConfirm = createButton('confirmar');

  const body = document.body;
  
  buttonContainer.appendChild(buttonCancel);
  buttonContainer.appendChild(buttonConfirm);

  frame.appendChild(message);
  frame.appendChild(buttonContainer);
  
  container.appendChild(frame)

  body.appendChild(container);
  
  buttonCancel.addEventListener("click", () => {body.removeChild(container)});
  buttonConfirm.addEventListener("click", () => {form.submit();});
}


// get the total amount received in profits (FIIs and Actions)
export function getTotalProfits() {
  const url = document.querySelector('#url-total-profits');

  if (url) {
    const path = url.dataset.urlTotalProfits;
    let xmlrequest = new XMLHttpRequest()

    xmlrequest.onreadystatechange = function() {
      if (xmlrequest.readyState === 4 && xmlrequest.status === 200) {
        const response = JSON.parse(xmlrequest.responseText);
        let elem = document.querySelector('#total_profits_fiis');
        elem.innerHTML = response.value.toLocaleString(
          'pt-BR',
          {
            style: 'currency',
            currency: 'BRL',
          }
        );
      }
    }
    xmlrequest.open('GET', path);
    xmlrequest.send();
  }
}

getTotalProfits();