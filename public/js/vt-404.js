// public/js/vt-404.js
/* 404.html: filtra la lista de servicios mientras se escribe. Sin JS se ve la lista completa. */
(function () {
  'use strict';
  const campo = document.getElementById('vt-buscar-404');
  const lista = document.querySelectorAll('[data-vt-servicio-404]');
  const vacio = document.getElementById('vt-vacio-404');
  if (!campo || !vacio) return;
  const plano = (t) => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  campo.addEventListener('input', () => {
    const q = plano(campo.value.trim());
    let visibles = 0;
    lista.forEach((li) => {
      const ver = plano(li.textContent).includes(q);
      li.hidden = !ver;
      if (ver) visibles += 1;
    });
    vacio.hidden = visibles > 0;
  });
})();
