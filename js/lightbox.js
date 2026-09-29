// Accessible image lightbox built on the native <dialog> element.
// Triggers: <button data-lightbox="group" data-full="src" data-caption="text"> containing an <img alt>.

export function initLightbox(dialog) {
  if (!dialog || typeof dialog.showModal !== 'function') return;

  const img = dialog.querySelector('.lightbox__img');
  const caption = dialog.querySelector('#lightbox-caption');
  const count = dialog.querySelector('.lightbox__count');
  const closeBtn = dialog.querySelector('[data-lb="close"]');
  let items = [];
  let index = 0;
  let opener = null;

  function show(i) {
    index = (i + items.length) % items.length;
    const trigger = items[index];
    const thumb = trigger.querySelector('img');
    img.src = trigger.dataset.full;
    img.alt = thumb ? thumb.alt : '';
    caption.textContent = trigger.dataset.caption || '';
    count.textContent = items.length > 1 ? `${index + 1} of ${items.length}` : '';
  }

  function open(trigger) {
    items = [...document.querySelectorAll(`[data-lightbox="${trigger.dataset.lightbox}"]`)];
    opener = trigger;
    dialog.toggleAttribute('data-single', items.length < 2);
    show(items.indexOf(trigger));
    dialog.showModal();
    closeBtn.focus();
  }

  document.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-lightbox]');
    if (trigger) open(trigger);
  });

  dialog.addEventListener('click', (event) => {
    const action = event.target.closest('[data-lb]')?.dataset.lb;
    if (action === 'close') dialog.close();
    else if (action === 'prev') show(index - 1);
    else if (action === 'next') show(index + 1);
    else if (event.target === dialog) dialog.close(); // backdrop click
  });

  dialog.addEventListener('keydown', (event) => {
    if (items.length < 2) return;
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(index - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(index + 1); }
  });

  dialog.addEventListener('close', () => {
    img.removeAttribute('src');
    opener?.focus();
  });
}
