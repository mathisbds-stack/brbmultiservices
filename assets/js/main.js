/* BRB Multiservices — script commun (menu mobile, année, pré-sélection du formulaire) */
(function () {
  'use strict';

  // Menu burger
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      nav.classList.toggle('is-open', open);
    };

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });

    window.matchMedia('(min-width: 960px)').addEventListener('change', function () {
      setOpen(false);
    });
  }

  // Année du copyright
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  // Contact : pré-sélectionne le type de besoin depuis ?besoin=service-1
  var select = document.getElementById('besoin');
  if (select && 'URLSearchParams' in window) {
    var besoin = new URLSearchParams(window.location.search).get('besoin');
    if (besoin && select.querySelector('option[value="' + CSS.escape(besoin) + '"]')) {
      select.value = besoin;
    }
  }
})();
