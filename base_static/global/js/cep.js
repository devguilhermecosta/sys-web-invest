// AJAX for Profile CEP
(() => {
  try {
    const inputCep = document.getElementById('id_cep');
    const adress = document.querySelector('#id_adress');
    const city = document.querySelector('#id_city');
    const uf = document.querySelector('#id_uf');
    inputCep.addEventListener('keyup', searchCep);
    
    function searchCep() {
      let cep = inputCep.value.replace('-', '');
  
      let url = `https://viacep.com.br/ws/${cep}/json`;
  
      const request = new XMLHttpRequest();
    
      request.onreadystatechange = function() {
        const defaulClass = 'C-input_xhr';

        if (request.readyState !== 4 && request.status !== 200) {
          adress.value = adress.innerHTML = '';
          city.value = city.innerHTML = '';
          uf.value = uf.innerHTML = '';
          
          adress.classList.remove(defaulClass);
          city.classList.remove(defaulClass);
          uf.classList.remove(defaulClass);
          return;
        } else {
          const r = JSON.parse(request.responseText);

          adress.innerHTML = adress.value = r.logradouro || '';
          city.value = city.innerHTML = r.localidade || '';
          uf.value = uf.innerHTML = r.uf || '';
          
          city.classList.add(defaulClass);
          adress.classList.add(defaulClass);
          uf.classList.add(defaulClass);
        }
      }
      request.open('GET', url, true);
      request.send();
    }
  } catch(e) {};
})();