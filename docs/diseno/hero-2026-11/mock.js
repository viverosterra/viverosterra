(() => {
  const P = document.querySelector('.vt-portada'); P.classList.add('vt-hero2');
  const grid = P.querySelector('.vt-portada__grid'); const izq = grid.firstElementChild; izq.classList.add('vt-hero2__tit');
  P.querySelector('.vt-kicker').textContent = 'Vivero y cuadrilla propia · Desde 2007';
  P.querySelector('h1').innerHTML = 'Pasto, jardines y plantas en Tampico.<span class="vt-serif">Con el precio por delante.</span>';
  P.querySelector('.vt-lede').textContent = 'Pasto San Agustín en rollo, diseño de jardines y +200 variedades de plantas, en Tampico, Madero y Altamira.';
  const tag = P.querySelector('.vt-etiqueta-x'); const trato = P.querySelector('.vt-portada__trato'); const cta = P.querySelector('[data-hero-cta]');
  cta.querySelector('.vt-btn--linea').remove();
  trato.innerHTML = ''; trato.append(cta);
  trato.insertAdjacentHTML('beforeend', '<p class="vt-hero2__alt"><a href="#medidor">Calcula tu patio&nbsp;→</a><a href="tel:+528333268008">Llamar 833 326 8008</a></p><p class="vt-hero2__prueba"><span class="vt-hero2__vivo">Abierto ahora</span><span>Respondemos en <b>menos de 1 hora</b></span><span><b>4.6</b> en Google (24 reseñas)</span><span><b>+900</b> clientes</span></p>');
  izq.after(tag); tag.after(trato);
})();
