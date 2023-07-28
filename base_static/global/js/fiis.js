import { createDefaultContainer } from './src/modules.js';
import { createDefaultFrame } from './src/modules.js';
import { createDivFlexButton } from './src/modules.js';
import { createTextElement } from './src/modules.js';
import { createButton } from './src/modules.js';
import { createMessageAlert } from './src/modules.js';
import { createGoogleIcon } from './src/modules.js';


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

              createProfitsTable(true);

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


// create link for history edit
function createHistoryLinkEdit(id) {
  const path = `historico/${id}/editar/`;
  let link = document.createElement('a');
  link.setAttribute('href', path);
  return link
}


// Create the earnings fii receipt table
function createDataTable(date, code, value, handler, p_id) {
  const tableBody = document.querySelector('#table-body');
  let spanEdit;
  let linkEdit;

  if (tableBody) {
    linkEdit = createHistoryLinkEdit(p_id);
    spanEdit = createGoogleIcon('edit', 'icon_edit');
    linkEdit.appendChild(spanEdit);

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
    tableDelete.appendChild(createGoogleIcon('delete_forever', 'icon_delete'));

    tableRow.appendChild(tableDate);
    tableRow.appendChild(tableCode);
    tableRow.appendChild(tableValue);
    tableRow.appendChild(tableHandler);
    tableRow.appendChild(tableEdit);
    tableRow.appendChild(tableDelete);

    tableBody.appendChild(tableRow);
  }
}


// clean the tbody
function cleanDataTable() {
  const tableBody = document.querySelector('#table-body');
  if (tableBody) {
    const tableData = tableBody.querySelectorAll('tr');
    tableData.forEach((tr) => {tableBody.removeChild(tr)});
  }
}


// populate the table 
function createProfitsTable(refresh=false) {
  const elem = document.querySelector('#url');

  if (elem) {
    const path = elem.dataset.url;
    let request = new XMLHttpRequest();

    request.onreadystatechange = function() {
      if (request.readyState == 4 && request.status == 200) {
        const result = JSON.parse(request.responseText);
        const data = result.data;
        let date = '';

        if (refresh) {
          cleanDataTable();
        }

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
}

createProfitsTable();
