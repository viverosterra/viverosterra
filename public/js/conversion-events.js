(function () {
  if (typeof window.gtag !== 'function') return;

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href*="wa.me"]');
    if (!link) return;
    window.gtag('event', 'whatsapp_click', {
      page_path: location.pathname,
      link_url: link.href,
      link_text: (link.textContent || '').trim().slice(0, 80)
    });
  });

  var form = document.getElementById('mainForm');
  if (form) {
    form.addEventListener('submit', function () {
      window.gtag('event', 'lead_form_submit', {
        form_id: 'cuestionario',
        page_path: location.pathname
      });
    });
  }
})();
