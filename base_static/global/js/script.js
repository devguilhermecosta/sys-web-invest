import { createAnimationBall } from './src/modules.js'


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


// add the animation button into all buttons
(() => {
  const buttons = document.querySelectorAll('.C-login_button');

  if (buttons) {
    buttons.forEach((button) => {
      const link = button.querySelector('a');
      const parentForm = button.parentElement;
      const dataSet = parentForm.dataset.profits;
      const isFormProfits = dataSet;

      if (isFormProfits) {return;}
      
      button.addEventListener("click", () => {
        button.innerHTML = '';
        button.setAttribute('disabled', true);
        button.appendChild(createAnimationBall());
        
        if (link) {link.style.display = 'none';}
        parentForm.submit();
      })
    })
  } 
})();


// add the animation button into button upgrade box
(() => {
  const form = document.querySelector("#upgrade_box_form");

  if (form) {
    form.addEventListener("submit", function() {
      const subject = form.querySelector("#subject");
      const message = form.querySelector("#content");
      const button = form.querySelector("#upgrade_box_button");

      if (!subject || !message) {return}

      button.innerHTML = '';
      button.appendChild(createAnimationBall());
      button.style.setAttribute('disabled', true);
    })
  }
})();
