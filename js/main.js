import { initLightbox } from './lightbox.js';

initLightbox(document.getElementById('lightbox'));

for (const el of document.querySelectorAll('[data-year]')) {
  el.textContent = String(new Date().getFullYear());
}
