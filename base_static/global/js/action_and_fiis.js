import { deleteObject, createAnimationBall } from "./src/modules.js";


// delete the user_action and user_fii objects
deleteObject(
    'span_vi_delete',
    `Deseja realmente deletar este ativo?
    Se você deletá-lo, todo seu histórico de compra, venda
    e recebimento de proventos será deletado também.`,
  );
  
  
// delete the history objects
deleteObject(
  'span_vihist_delete',
  'Deseja realmente deletar este histórico?',
);


// preventdefault form update prices
// (() => {
//   const form = document.querySelector('#form-update-price');

//   if (form) {
//     form.addEventListener("submit", function(e) {
//       e.preventDefault();
      
//       let btnSubmit = form.querySelector('#btn-update');
//       let animationBall = createAnimationBall();

//       btnSubmit.innerHTML = '';
//       btnSubmit.setAttribute('disabled', true);
//       btnSubmit.appendChild(animationBall);

//       form.submit();
//     })
//   }
// })();