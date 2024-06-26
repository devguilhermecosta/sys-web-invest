import { createFormSubmit } from './utils.js';

// functions for create html elements
export function createDefaultContainer() {
  const divContainer = document.createElement('div');
  divContainer.classList.add('C-product_form_container');
  return divContainer;
}


export function createDefaultFrame() {
  const frame = document.createElement('div');
  frame.classList.add('C-product_form_confirm');
  return frame;
}


export function createButton(value) {
  const button = document.createElement('button');
  button.classList.add('C-product_form_btn');
  button.innerHTML = value;
  return button;
}


export function createDivFlexButton() {
  const divFlexButton = document.createElement('div');
  divFlexButton.classList.add('C-product_form_buttons');
  return divFlexButton;
}


export function createTextElement(color, message) {
  const text = document.createElement('p');
  text.style.color = color;
  text.style.whiteSpace = 'normal';
  text.style.textAlign = 'center';
  text.style.padding = '10px';
  text.innerHTML = message;
  return text;
}


export function createAnimationBall() {
  const spanBall = document.createElement('span');
  spanBall.classList.add('animation_ball');
  return spanBall;
}


// Google Icon
export function createGoogleIcon(innerHTML, aditionalCssClass='') {
  let span = document.createElement('span');
  span.innerHTML = innerHTML;
  span.classList.add('material-symbols-outlined');

  if (aditionalCssClass) {
    span.classList.add(aditionalCssClass);
  }

  return span;
}


// create message alert
export function createMessageAlert(color, message) {
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


// clean the tbody
export function cleanDataTable() {
  const tableBody = document.querySelector('#table-body');
  if (tableBody) {
    const tableData = tableBody.querySelectorAll('tr');
    tableData.forEach((tr) => {tableBody.removeChild(tr)});
  }
}


// converto to BRL money
export function convertToBRL(value) {
  return value.toLocaleString(
    'pt-BR',
    {
      style: 'currency',
      currency: 'BRL',
    }
  )
}


// convert to local date
export function convertToLocaleDateString(date) {
  let newDate = new Date(date);
  return newDate.toLocaleDateString(
    'pt-BR',
    {'timeZone': 'UTC'},
  )
}


// translate the data handler to pt-br
export function makeHandler(handler) {
  switch(handler) {
    case 'profits':
      return 'proventos'
    case 'dividends':
      return 'dividendos'
    case 'jscp':
      return 'jscp'
    case 'remuneration':
      return 'remuneração'
    case 'renting':
      return 'aluguel'
    case _:
      return ''
  }
}

// function for delete objects
export function deleteObject(css_class_btn_action, message) {
  const spanDelete = document.querySelectorAll(`.${css_class_btn_action}`);
  if (spanDelete) {
    spanDelete.forEach((el) => {
      el.addEventListener("click", function() {
        const parentForm = el.parentElement;
        createFormSubmit(
          parentForm,
          message,
          );
      })
    })
  }
}