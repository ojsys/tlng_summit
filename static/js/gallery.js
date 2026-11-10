/*
 * Photo viewer (modal lightbox) for gallery collages.
 *
 * Any link with [data-lightbox="group"] opens in the viewer. Links in the same
 * group (and not hidden by a filter) can be browsed with the arrows, the
 * thumbnail strip, the keyboard (← → Esc) or by swiping on touch screens.
 * Optional data attributes: data-caption, data-album-title, data-album-url, data-thumb.
 */
/*
 * Collage balancing: tiles of mixed sizes are packed by CSS grid (dense flow),
 * which can leave gaps in the last rows. This simulates the packing and, if
 * needed, shrinks big tiles near the end and stretches the final tile so the
 * collage always ends with a flush edge. Exposed as window.balanceCollages().
 */
(function () {
    'use strict';

    function spanOf(tile) {
        var c = tile.classList;
        if (c.contains('tile-xl')) return [2, 2];
        if (c.contains('tile-wide')) return [2, 1];
        if (c.contains('tile-tall')) return [1, 2];
        return [1, 1];
    }

    function holes(cols, spans) {
        var grid = [], maxRow = 0;
        function free(r, c, w, h) {
            for (var y = r; y < r + h; y++) for (var x = c; x < c + w; x++) if (grid[y] && grid[y][x]) return false;
            return true;
        }
        spans.forEach(function (s) {
            var w = Math.min(s[0], cols), h = s[1];
            for (var r = 0; ; r++) {
                for (var c = 0; c + w <= cols; c++) {
                    if (free(r, c, w, h)) {
                        for (var y = r; y < r + h; y++) {
                            grid[y] = grid[y] || [];
                            for (var x = c; x < c + w; x++) grid[y][x] = true;
                        }
                        maxRow = Math.max(maxRow, r + h);
                        return;
                    }
                }
            }
        });
        var empty = 0, lastRowEmpty = 0;
        for (var y = 0; y < maxRow; y++) for (var x = 0; x < cols; x++) {
            if (!(grid[y] && grid[y][x])) { empty++; if (y === maxRow - 1) lastRowEmpty++; }
        }
        return { empty: empty, lastRow: lastRowEmpty };
    }

    function balance(collage) {
        var tiles = Array.prototype.filter.call(collage.children, function (t) {
            t.style.gridColumn = t.style.gridRow = '';
            return t.classList.contains('collage-tile') && t.offsetParent !== null;
        });
        if (!tiles.length) return;
        var cols = getComputedStyle(collage).gridTemplateColumns.split(' ').filter(Boolean).length;
        var spans = tiles.map(spanOf);
        var result = holes(cols, spans);
        // Shrink big tiles, starting from the end, until the gaps disappear.
        for (var i = spans.length - 1; result.empty && i >= Math.max(0, spans.length - 12); i--) {
            if (spans[i][0] > 1 || spans[i][1] > 1) {
                spans[i] = [1, 1];
                tiles[i].style.gridColumn = 'span 1';
                tiles[i].style.gridRow = 'span 1';
                result = holes(cols, spans);
            }
        }
        // Any remaining gap is in the last row: stretch the final tile across it.
        if (result.empty && result.empty === result.lastRow) {
            var last = tiles[tiles.length - 1];
            last.style.gridColumn = 'span ' + Math.min(cols, spans[spans.length - 1][0] + result.lastRow);
        }
    }

    function balanceAll() {
        document.querySelectorAll('.collage').forEach(balance);
    }
    window.balanceCollages = balanceAll;

    var timer;
    window.addEventListener('resize', function () { clearTimeout(timer); timer = setTimeout(balanceAll, 120); });
    balanceAll();
})();

(function () {
    'use strict';

    if (!document.querySelector('a[data-lightbox]')) return;

    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Photo viewer');
    box.innerHTML =
        '<div class="lb-backdrop"></div>' +
        '<div class="lb-top">' +
        '  <div class="lb-info"><span class="lb-counter"></span><a class="lb-album" href="#"></a></div>' +
        '  <button type="button" class="lb-btn lb-close" aria-label="Close (Esc)"><i class="fas fa-times"></i></button>' +
        '</div>' +
        '<div class="lb-stage">' +
        '  <button type="button" class="lb-btn lb-nav lb-prev" aria-label="Previous photo"><i class="fas fa-chevron-left"></i></button>' +
        '  <figure class="lb-figure"><span class="lb-spinner" aria-hidden="true"></span><img class="lb-img" alt=""></figure>' +
        '  <button type="button" class="lb-btn lb-nav lb-next" aria-label="Next photo"><i class="fas fa-chevron-right"></i></button>' +
        '</div>' +
        '<div class="lb-bottom">' +
        '  <p class="lb-caption"></p>' +
        '  <div class="lb-thumbs" role="tablist" aria-label="Photos"></div>' +
        '</div>';
    document.body.appendChild(box);

    var img = box.querySelector('.lb-img');
    var figure = box.querySelector('.lb-figure');
    var caption = box.querySelector('.lb-caption');
    var counter = box.querySelector('.lb-counter');
    var albumLink = box.querySelector('.lb-album');
    var thumbs = box.querySelector('.lb-thumbs');
    var group = [], index = 0, lastFocus = null, closeTimer = null, groupName = '';

    function groupLinks(name) {
        return Array.prototype.filter.call(document.querySelectorAll('a[data-lightbox]'), function (l) {
            return l.dataset.lightbox === name && !l.closest('.is-filtered');
        });
    }

    function buildThumbs() {
        thumbs.innerHTML = '';
        box.classList.toggle('single', group.length < 2);
        if (group.length < 2) return;
        group.forEach(function (link, i) {
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'lb-thumb';
            b.setAttribute('role', 'tab');
            b.setAttribute('aria-label', 'Photo ' + (i + 1));
            var t = document.createElement('img');
            t.src = link.dataset.thumb || link.href;
            t.alt = '';
            t.loading = 'lazy';
            b.appendChild(t);
            b.addEventListener('click', function () { show(i); });
            thumbs.appendChild(b);
        });
    }

    function show(i) {
        index = (i + group.length) % group.length;
        var link = group[index];

        figure.classList.add('loading');
        var next = new Image();
        next.onload = next.onerror = function () {
            if (group[index] !== link) return;    // user moved on meanwhile
            img.src = link.href;
            img.alt = link.dataset.caption || link.dataset.albumTitle || '';
            figure.classList.remove('loading');
        };
        next.src = link.href;

        caption.textContent = link.dataset.caption || '';
        caption.hidden = !link.dataset.caption;
        counter.textContent = group.length > 1 ? (index + 1) + ' / ' + group.length : '';
        if (link.dataset.albumTitle) {
            albumLink.textContent = link.dataset.albumTitle;
            albumLink.href = link.dataset.albumUrl || '#';
            albumLink.hidden = false;
            albumLink.classList.toggle('static', groupName === 'album');
        } else {
            albumLink.hidden = true;
        }

        Array.prototype.forEach.call(thumbs.children, function (t, n) {
            var active = n === index;
            t.classList.toggle('active', active);
            t.setAttribute('aria-selected', active ? 'true' : 'false');
            if (active) t.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
        });

        [index + 1, index - 1].forEach(function (n) {          // preload neighbours
            var l = group[(n + group.length) % group.length];
            if (l) (new Image()).src = l.href;
        });
    }

    function open(link) {
        groupName = link.dataset.lightbox;
        group = groupLinks(groupName);
        lastFocus = document.activeElement;
        clearTimeout(closeTimer);
        buildThumbs();
        img.removeAttribute('src');
        box.classList.add('open');
        document.documentElement.classList.add('lb-lock');
        requestAnimationFrame(function () { box.classList.add('visible'); });
        show(Math.max(group.indexOf(link), 0));
        box.querySelector('.lb-close').focus({ preventScroll: true });
    }

    function close() {
        box.classList.remove('visible');
        document.documentElement.classList.remove('lb-lock');
        closeTimer = setTimeout(function () {
            box.classList.remove('open');
            img.removeAttribute('src');
        }, 250);
        if (lastFocus) lastFocus.focus({ preventScroll: true });
    }

    document.addEventListener('click', function (e) {
        var link = e.target.closest('a[data-lightbox]');
        if (!link || e.metaKey || e.ctrlKey || e.shiftKey) return;
        if (document.body.classList.contains('cms-editing') && e.target.closest('[data-cms], .cms-photo-delete')) return;
        e.preventDefault();
        open(link);
    });

    box.querySelector('.lb-close').addEventListener('click', close);
    box.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
    box.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
    box.querySelector('.lb-backdrop').addEventListener('click', close);
    box.querySelector('.lb-stage').addEventListener('click', function (e) {
        if (e.target === e.currentTarget || e.target === figure) close();
    });

    document.addEventListener('keydown', function (e) {
        if (!box.classList.contains('visible')) return;
        if (e.key === 'Escape') { e.preventDefault(); close(); }
        else if (e.key === 'ArrowLeft') show(index - 1);
        else if (e.key === 'ArrowRight') show(index + 1);
        else if (e.key === 'Tab') {                              // keep focus inside the viewer
            var focusable = box.querySelectorAll('button:not([hidden]), a:not([hidden])');
            var first = focusable[0], last = focusable[focusable.length - 1];
            if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
            else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
            else if (!box.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
        }
    });

    var startX = null, startY = null;
    box.addEventListener('touchstart', function (e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    }, { passive: true });
    box.addEventListener('touchend', function (e) {
        if (startX === null) return;
        var dx = e.changedTouches[0].clientX - startX;
        var dy = e.changedTouches[0].clientY - startY;
        if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(index + (dx < 0 ? 1 : -1));
        else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) close();  // swipe down to close
        startX = startY = null;
    });
})();
