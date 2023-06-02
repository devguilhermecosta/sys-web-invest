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