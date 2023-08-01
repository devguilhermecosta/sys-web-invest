import { convertToBRL, convertToLocaleDateString, makeHandler } from "./src/modules.js";

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


function createDataTableProfits() {
  const inputPath = document.querySelector('#url-actions-history-profits');

  if (inputPath) {
    const path = inputPath.dataset.urlHistoryProfits;
    const xmlrRequest = new XMLHttpRequest();

    xmlrRequest.onreadystatechange = function() {
      if (xmlrRequest.readyState === 4 && xmlrRequest.status === 200) {
        const response = JSON.parse(xmlrRequest.responseText);
        const data = response.data;

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
