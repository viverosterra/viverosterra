/* Viveros Terra — navbar glass al hacer scroll (Mejora 9, compartido) */
(function () {
  var nav = document.querySelector('.terra-nav');
  if (!nav) return;
  var onScroll = function () {
    if (window.scrollY > 40) nav.classList.add('is-scrolled');
    else nav.classList.remove('is-scrolled');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
