import { createDefaultContainer } from './src/modules.js';
import { createDefaultFrame } from './src/modules.js';
import { createDivFlexButton } from './src/modules.js';
import { createTextElement } from './src/modules.js';
import { createButton } from './src/modules.js';
import { createMessageAlert } from './src/modules.js';
import { createGoogleIcon } from './src/modules.js';
import { convertToBRL, convertToLocaleDateString, makeHandler } from './src/modules.js';
import { cleanDataTable } from './src/modules.js';
import { createHistoryLinkDelete, confirmationBoxDeleteHistory, createHistoryLinkEdit } from './src/utils.js';
import { getTotalProfits } from './src/utils.js';


// form fiis receiv profis
(() => {
  const formFiisReceivProfis = document.querySelector('#form_fii_receiv_profis');

  if (formFiisReceivProfis) {
    formFiisReceivProfis.addEventListener("submit", function(event) {
      event.preventDefault();

      const form = new FormData(formFiisReceivProfis);
      const product = parseInt(form.get('userproduct'));
      const select = formFiisReceivProfis.querySelector('#id_userproduct');
      const productDesc = select.options[select.selectedIndex].innerHTML;
      const date = form.get('date');
      const value = parseFloat(form.get('unit_price'));

      const body = document.body;
      const container = createDefaultContainer();

      if (product >= 1 && date.length > 0 && value > 0) {
        const formatedValue = convertToBRL(value);
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

        buttonContainer.appendChild(buttonCancel);
        buttonContainer.appendChild(buttonConfirm);

        frame.appendChild(message);
        frame.appendChild(buttonContainer);

        container.appendChild(frame)
        body.appendChild(container);

        buttonCancel.addEventListener("click", () => {body.removeChild(container);});

        buttonConfirm.addEventListener("click", function() {
          const inputPath = document.querySelector('#url-receive-profits');
          let urlPath = inputPath.dataset.urlReceiveProfits;
          let token = formFiisReceivProfis.querySelectorAll('input')[0].value;
          let labels = formFiisReceivProfis.querySelectorAll('.C-login_label');

          let xmlr = new XMLHttpRequest();

          xmlr.onreadystatechange = function() {
            if (xmlr.readyState === 4 && xmlr.status == 200) {
              const oldMessage = document.querySelectorAll('.messages')[0];
              if (oldMessage) {oldMessage.parentElement.removeChild(oldMessage);}
              let result = document.querySelector('#result');
              result.classList.add('profits_messages');
              result.innerHTML = 
              `Recebimento de ${formatedValue} lançado com sucesso para ${productDesc}`;

              formFiisReceivProfis.reset();
              labels.forEach((l) => {l.classList.remove('C-login_input_active')});
              createProfitsTable(true);
              getTotalProfits();
            }
          }
          xmlr.open('POST', urlPath);
          xmlr.setRequestHeader('X-CSRF-TOKEN', token);
          xmlr.send(form);
          body.removeChild(container);
        })
        return;
      }

      createMessageAlert('white', 'Informe todos os dados');
    
    })
  }
})();


// Create the profits fii receipt table
function createDataTable(date, code, value, handler, p_id) {
  const tableBody = document.querySelector('#table-body');
  let spanEdit;
  let spanDelete;
  let linkEdit;
  let linkDelete;

  if (tableBody) {
    linkEdit = createHistoryLinkEdit(p_id);
    spanEdit = createGoogleIcon('edit', 'icon_edit');
    linkEdit.appendChild(spanEdit);

    linkDelete = createHistoryLinkDelete(p_id);
    spanDelete = createGoogleIcon('delete_forever', 'icon_delete');
    spanDelete.addEventListener("click", () => {confirmationBoxDeleteHistory(spanDelete, code)});
    linkDelete.appendChild(spanDelete);

    let tableRow = document.createElement('tr');
    let tableDate = document.createElement('td');
    let tableCode = document.createElement('td');
    let tableValue = document.createElement('td');
    let tableHandler = document.createElement('td');
    let tableEdit = document.createElement('td');
    let tableDelete = document.createElement('td');

    tableDate.innerHTML = date;
    tableCode.innerHTML = code;
    tableValue.innerHTML = value;
    tableHandler.innerHTML = handler;
    tableHandler.style.color = '#0f6e6a';
    tableEdit.appendChild(linkEdit);
    tableDelete.appendChild(linkDelete);

    tableRow.appendChild(tableDate);
    tableRow.appendChild(tableCode);
    tableRow.appendChild(tableValue);
    tableRow.appendChild(tableHandler);
    tableRow.appendChild(tableEdit);
    tableRow.appendChild(tableDelete);

    tableBody.appendChild(tableRow);
  }
}


// populate the table 
function createProfitsTable(refresh=false) {
  const elem = document.querySelector('#url-history-profits');
  
  if (elem && elem.dataset.urlHistoryProfits) {
    const path = elem.dataset.urlHistoryProfits;

    let request = new XMLHttpRequest();
    
    request.onreadystatechange = function() {
      if (request.readyState == 4 && request.status == 200) {
        const result = JSON.parse(request.responseText);
        const data = result.data;
        
        if (refresh) {cleanDataTable();}
        
        data.map((el) => {
          createDataTable(
            convertToLocaleDateString(el.date),
            el.product,
            convertToBRL(parseFloat(el.value)),
            makeHandler(el.handler),
            el.history_id);
        }
        )
      }
    }
    request.open('GET', path.toString(), true);
    request.send();
  }
}

createProfitsTable();
getTotalProfits()
