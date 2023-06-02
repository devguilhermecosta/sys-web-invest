(() => {
  const formInput = document.querySelectorAll('.C-login_input');
  
  formInput.forEach((input) => {
    const labelSister = input.nextElementSibling;
    const className = 'C-login_input_active';

    if (input.value.length >= 1) {
      labelSister.classList.add(className);
    }

    input.addEventListener('change', function() {
      const inputLength = input.value.length;
      if (inputLength >= 1) {
        labelSister.classList.add(className);
      } else {
        labelSister.classList.remove(className);
      }
    })
  })
})();