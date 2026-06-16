/* main.js -- utilidades compartidas de la interfaz */

/**
 * Autocompletado tipo desplegable para un campo de texto.
 * @param {string} inputId  - id del <input>
 * @param {string} listId   - id del <ul> donde se muestran las sugerencias
 * @param {string[]} items  - lista completa de opciones
 */
function setupAutocomplete(inputId, listId, items) {
  const input = document.getElementById(inputId);
  const list  = document.getElementById(listId);
  if (!input || !list) return;

  let activeIdx = -1;

  function normalize(str) {
    return str.toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  function showSuggestions(query) {
    const q = normalize(query.trim());
    list.innerHTML = '';
    activeIdx = -1;
    if (!q) { list.classList.remove('is-open'); return; }

    const matches = items.filter(item => normalize(item).includes(q));
    if (!matches.length) { list.classList.remove('is-open'); return; }

    matches.slice(0, 8).forEach((item, idx) => {
      const li = document.createElement('li');
      li.className = 'autocomplete-item';
      li.textContent = item;
      li.dataset.idx = idx;
      li.addEventListener('mousedown', (e) => {
        e.preventDefault();
        input.value = item;
        list.classList.remove('is-open');
        list.innerHTML = '';
      });
      list.appendChild(li);
    });
    list.classList.add('is-open');
  }

  function setActive(idx) {
    const items = list.querySelectorAll('.autocomplete-item');
    items.forEach(el => el.classList.remove('is-active'));
    if (idx >= 0 && idx < items.length) {
      items[idx].classList.add('is-active');
      activeIdx = idx;
    }
  }

  input.addEventListener('input', () => showSuggestions(input.value));
  input.addEventListener('focus', () => showSuggestions(input.value));

  input.addEventListener('keydown', (e) => {
    const listItems = list.querySelectorAll('.autocomplete-item');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActive(Math.min(activeIdx + 1, listItems.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActive(Math.max(activeIdx - 1, 0));
    } else if (e.key === 'Enter') {
      if (activeIdx >= 0 && listItems[activeIdx]) {
        e.preventDefault();
        input.value = listItems[activeIdx].textContent;
        list.classList.remove('is-open');
        list.innerHTML = '';
      }
    } else if (e.key === 'Escape') {
      list.classList.remove('is-open');
    }
  });

  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !list.contains(e.target)) {
      list.classList.remove('is-open');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  // Entrada escalonada de las tarjetas de casos de uso (landing)
  const cards = document.querySelectorAll('.usecase-card');
  cards.forEach((card, i) => {
    setTimeout(() => card.classList.add('is-visible'), i * 90);
  });

  // Scroll reveal: timeline "como funciona" y otros bloques .reveal
  const revealEls = document.querySelectorAll('.reveal, .uc-flow__item');

  if (!('IntersectionObserver' in window) || revealEls.length === 0) {
    revealEls.forEach((el) => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0, rootMargin: '0px 0px -10% 0px' });

  revealEls.forEach((el) => observer.observe(el));
});