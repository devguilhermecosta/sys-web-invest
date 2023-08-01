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
  text.style.whiteSpace = 'nowrap';
  text.style.textAlign = 'center';
  text.style.padding = '10px';
  text.innerHTML = message;
  return text;
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
