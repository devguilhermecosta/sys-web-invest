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


// Function for change btn value into login page
(() => {
  try {
    const loginForm = document.querySelector('.C-login_form');
    let btnLogin = document.querySelector('#btn-login');
    btnLogin.addEventListener('click', function(event) {
      event.preventDefault();
    
      btnLogin.value = 'entrando...';
      loginForm.submit();
    })
  } catch(e){};
})();


// Function for change btn value into register page
(() => {
  try {
    const registerForm = document.querySelector('.C-form_register_form');
    let btnRegister = document.querySelector('#btn-register');
    btnRegister.addEventListener('click', function(event) {
      event.preventDefault();
    
      btnRegister.value = 'registrando...';
      registerForm.submit();
    })
  } catch(e){};
})();


// Function for change btn value into register page
(() => {
  try {
    const registerProfileForm = document.querySelector('.C-login_form');
    let btnCreateProfile = document.querySelector('.C-login_button[value=finalizar]');
    btnCreateProfile.addEventListener('click', function(event) {
      event.preventDefault();
    
      btnCreateProfile.value = 'criando perfil...';
      registerProfileForm.submit();
    })
  } catch(e){};
})();
