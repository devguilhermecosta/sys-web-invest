(() => {
  const formInput = document.querySelectorAll('.C-login_input');
  
  formInput.forEach((input) => {
    const inputLength = input.value.length;
    const labelSister = input.nextElementSibling;
    const className = 'C-login_input_active';

    if (inputLength >= 1) {
      labelSister.classList.add(className);
    }

    input.addEventListener('change', function() {
      const inputLengthInside = input.value.length;
      if (inputLengthInside >= 1) {
        labelSister.classList.add(className);
      } else {
        labelSister.classList.remove(className);
      }
    })
  })
})();

// change eye from dashboard intro
(() => {
  const eyeInput = document.querySelector('#show-invest');
  const eyeIcon = document.querySelector('.eye-icon');

  eyeInput.addEventListener('change', function() {
    if (eyeInput.checked) {
      eyeIcon.innerHTML = 'visibility_off';
    } else if (!eyeInput.checked) {
      eyeIcon.innerHTML = 'visibility';
    }
  })
})();