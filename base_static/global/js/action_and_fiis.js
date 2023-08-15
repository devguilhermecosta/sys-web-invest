import { deleteObject } from "./src/modules.js";


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
