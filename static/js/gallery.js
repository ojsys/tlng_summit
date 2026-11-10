/*
 * Lightweight lightbox for gallery photos.
 * Any link with [data-lightbox="group-name"] opens in the viewer; links in the
 * same group can be browsed with arrows, keyboard or swipe.
 */
(function () {
    'use strict';

    var links = document.querySelectorAll('a[data-lightbox]');
    if (!links.length) return;

    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Photo viewer');
    box.innerHTML =
        '<button class="lb-btn lb-close" aria-label="Close">&times;</button>' +
        '<button class="lb-btn lb-prev" aria-label="Previous photo"><i class="fas fa-chevron-left"></i></button>' +
        '<figure class="lb-figure"><img class="lb-img" alt=""><figcaption class="lb-caption"></figcaption></figure>' +
        '<button class="lb-btn lb-next" aria-label="Next photo"><i class="fas fa-chevron-right"></i></button>' +
        '<div class="lb-counter"></div>';
    document.body.appendChild(box);

    var img = box.querySelector('.lb-img');
    var caption = box.querySelector('.lb-caption');
    var counter = box.querySelector('.lb-counter');
    var group = [], index = 0, lastFocus = null;

    function show(i) {
        index = (i + group.length) % group.length;
        var link = group[index];
        img.classList.add('loading');
        img.onload = function () { img.classList.remove('loading'); };
        img.src = link.href;
        img.alt = link.dataset.caption || '';
        caption.textContent = link.dataset.caption || '';
        counter.textContent = group.length > 1 ? (index + 1) + ' / ' + group.length : '';
        box.classList.toggle('single', group.length < 2);
        [index + 1, index - 1].forEach(function (n) {           // preload neighbours
            var l = group[(n + group.length) % group.length];
            if (l) { (new Image()).src = l.href; }
        });
    }

    function open(link) {
        group = Array.prototype.filter.call(document.querySelectorAll('a[data-lightbox]'), function (l) {
            return l.dataset.lightbox === link.dataset.lightbox;
        });
        lastFocus = document.activeElement;
        box.classList.add('open');
        document.body.style.overflow = 'hidden';
        show(group.indexOf(link));
        box.querySelector('.lb-close').focus();
    }

    function close() {
        box.classList.remove('open');
        document.body.style.overflow = '';
        img.removeAttribute('src');
        if (lastFocus) lastFocus.focus();
    }

    document.addEventListener('click', function (e) {
        var link = e.target.closest('a[data-lightbox]');
        if (!link || e.metaKey || e.ctrlKey) return;
        if (document.body.classList.contains('cms-editing') && e.target.closest('[data-cms], .cms-photo-delete')) return;
        e.preventDefault();
        open(link);
    });
    box.querySelector('.lb-close').addEventListener('click', close);
    box.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
    box.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
    box.addEventListener('click', function (e) { if (e.target === box || e.target.classList.contains('lb-figure')) close(); });
    document.addEventListener('keydown', function (e) {
        if (!box.classList.contains('open')) return;
        if (e.key === 'Escape') close();
        else if (e.key === 'ArrowLeft') show(index - 1);
        else if (e.key === 'ArrowRight') show(index + 1);
    });

    var startX = null;
    box.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', function (e) {
        if (startX === null) return;
        var dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
        startX = null;
    });
})();
