(() => {
  const formInput = document.querySelectorAll('.C-login_input');
  
  formInput.forEach((input) => {
    if (input.value.length >= 1) {
      input.nextElementSibling.classList.add('C-login_input_active');
    }

    input.addEventListener('change', function() {
      const inputLength = input.value.length;
      const labelSister = input.nextElementSibling;
      const className = 'C-login_input_active'
      if (inputLength >= 1) {
        labelSister.classList.add(className);
      } else {
        labelSister.classList.remove(className);
      }
    })
  })
})();