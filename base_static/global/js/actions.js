import { convertToBRL, convertToLocaleDateString, makeHandler } from "./src/modules.js";
import { createMessageAlert } from "./src/modules.js";
import { createDefaultContainer } from "./src/modules.js";
import { createDefaultFrame } from "./src/modules.js";
import { createDivFlexButton } from "./src/modules.js";
import { createTextElement } from "./src/modules.js";
import { createButton } from "./src/modules.js";
import { cleanDataTable } from "./src/modules.js";


// function for receive profits
(() => {
  const form = document.querySelector('#actions-receive-profits-form');

  if (form) {
    form.addEventListener("submit", function(event) {
      event.preventDefault();

      const dataForm = new FormData(form);
      const productInput = form.querySelector("#id_user_product_id");
      const profitsTypeInput = form.querySelector('#id_profits_type');

      const product_id = parseInt(dataForm.get('user_product_id'));
      const productDesc = productInput.options[productInput.selectedIndex].innerHTML;
      const handler = profitsTypeInput.options[profitsTypeInput.selectedIndex].innerHTML;
      const date = dataForm.get('date');
      const totalValue = convertToBRL(parseFloat(dataForm.get('total_price')));

      if (!product_id || !handler || !date || !totalValue) {
        createMessageAlert('white', 'informe todos os dados');
        return
      }

      const body = document.body;
      const container = createDefaultContainer();
      const frame = createDefaultFrame();
      const text = createTextElement(
        'white', 
        `<p>deseja salvar o recebimento de</p> <p>${totalValue} para ${productDesc}?</p>` );
      const buttonFrame = createDivFlexButton();
      const buttonConfirm = createButton('confirmar');
      const buttonCancel = createButton('cancelar');

      buttonFrame.appendChild(buttonCancel);
      buttonFrame.appendChild(buttonConfirm);

      frame.appendChild(text);
      frame.appendChild(buttonFrame);

      container.appendChild(frame);
      body.appendChild(container);

      buttonCancel.addEventListener("click", () => {body.removeChild(container)});
      buttonConfirm.addEventListener("click", function() {
        const inputPath = document.querySelector('#url-actions-receive-profits');
        const path = inputPath.dataset.urlReceiveProfits;
        const token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        const labels = form.querySelectorAll('.C-login_label');

        const xmlrequest = new XMLHttpRequest();

        xmlrequest.onreadystatechange = function() {
          if (xmlrequest.readyState === 4 && xmlrequest.status === 200) {
            let result = document.querySelector('#result');
            result.classList.add('messages');
            result.classList.add('message_success');
            result.innerHTML = `Recebimento de ${totalValue} lançado com sucesso para ${productDesc}`;
            
            form.reset();
            labels.forEach((l) => {l.classList.remove('C-login_input_active')});
            body.removeChild(container);
            createDataTableProfits(true);
          }
        }
        xmlrequest.open('POST', path, true);
        xmlrequest.setRequestHeader('X-CSRF-TOKEN', token);
        xmlrequest.send(dataForm);
      })
    })
  }
})();


// Create the profits actions receipt table
function createDataTable(date, code, handler, tax, gross_value, final_value, h_id) {
  const tableBody = document.querySelector('#table-body');
  // let spanEdit;
  // let spanDelete;
  // let linkEdit;
  // let linkDelete;

  // if (tableBody) {
    // linkEdit = createHistoryLinkEdit(p_id);
    // spanEdit = createGoogleIcon('edit', 'icon_edit');
    // linkEdit.appendChild(spanEdit);

    // linkDelete = createHistoryLinkDelete(p_id);
    // spanDelete = createGoogleIcon('delete_forever', 'icon_delete');
    // spanDelete.addEventListener("click", function() {
    //   const form = this.parentElement;
    //   const container = createDefaultContainer();
    //   const frame = createDefaultFrame()
    //   const message = createTextElement(
    //     'white', 
    //     `<p>deseja mesmo deletar</p>
    //     <p>este provento de ${code}?</p>`,
    //     );
    //   const buttonContainer = createDivFlexButton();
    //   const buttonCancel = createButton('cancelar');
    //   const buttonConfirm = createButton('confirmar');
    
    //   const body = document.body;
      
    //   buttonContainer.appendChild(buttonCancel);
    //   buttonContainer.appendChild(buttonConfirm);

    //   frame.appendChild(message);
    //   frame.appendChild(buttonContainer);
      
    //   container.appendChild(frame)

    //   body.appendChild(container);
      
    //   buttonCancel.addEventListener("click", () => {body.removeChild(container)});
    //   buttonConfirm.addEventListener("click", function() {form.submit();});
    // })
    // linkDelete.appendChild(spanDelete);
  
    let tableRow = document.createElement('tr');
    let tableDate = document.createElement('td');
    let tableCode = document.createElement('td');
    let tableHandler = document.createElement('td');
    let tableTax = document.createElement('td');
    let tableGrossValue = document.createElement('td');
    let tableFinalValue = document.createElement('td');

    tableDate.innerHTML = date;
    tableCode.innerHTML = code;
    tableHandler.innerHTML = handler;
    tableTax.innerHTML = tax;
    tableGrossValue.innerHTML = gross_value;
    tableFinalValue.innerHTML = final_value;
    tableHandler.style.color = '#0f6e6a';

    // tableEdit.appendChild(linkEdit);
    // tableDelete.appendChild(linkDelete);

    tableRow.appendChild(tableDate);
    tableRow.appendChild(tableCode);
    tableRow.appendChild(tableHandler);
    tableRow.appendChild(tableTax);
    tableRow.appendChild(tableGrossValue);
    tableRow.appendChild(tableFinalValue);

    tableBody.appendChild(tableRow);
}


function createDataTableProfits(refresh=false) {
  const inputPath = document.querySelector('#url-actions-history-profits');

  if (inputPath) {
    const path = inputPath.dataset.urlHistoryProfits;
    const xmlrRequest = new XMLHttpRequest();

    xmlrRequest.onreadystatechange = function() {
      if (xmlrRequest.readyState === 4 && xmlrRequest.status === 200) {
        const response = JSON.parse(xmlrRequest.responseText);
        const data = response.data;

        if (refresh) {cleanDataTable();}

        data.map((history) => {
          createDataTable(
            convertToLocaleDateString(history.date),
            history.product,
            makeHandler(history.handler),
            convertToBRL(history.tax),
            convertToBRL(history.gross_value),
            convertToBRL(history.final_value),
          )
        })

      }
    }
    xmlrRequest.open('GET', path);
    xmlrRequest.send();
  }
}

createDataTableProfits();
