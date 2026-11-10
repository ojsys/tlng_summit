/*
 * Live editing for staff. Loaded only when the user is logged in as staff.
 * Elements rendered by the {% cms_* %} template tags carry data-cms attributes;
 * this script makes them editable when "Edit page" is switched on.
 */
(function () {
    'use strict';

    var bar = document.getElementById('cms-toolbar');
    if (!bar) return;

    var ENDPOINT = bar.dataset.endpoint;
    var CSRF = bar.dataset.csrf;
    var STORE_KEY = 'tlng-cms-edit';
    var toggleBtn = document.getElementById('cms-toggle');
    var editing = false;

    // ------------------------------------------------------------ utilities
    function remember(on) { try { localStorage.setItem(STORE_KEY, on ? '1' : '0'); } catch (e) { /* private mode */ } }
    function remembered() { try { return localStorage.getItem(STORE_KEY) === '1'; } catch (e) { return false; } }

    var toastEl, toastTimer;
    function toast(message, isError) {
        if (!toastEl) {
            toastEl = document.createElement('div');
            toastEl.className = 'cms-toast';
            toastEl.setAttribute('role', 'status');
            document.body.appendChild(toastEl);
        }
        toastEl.textContent = message;
        toastEl.classList.toggle('error', !!isError);
        toastEl.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, isError ? 6000 : 2200);
    }

    function post(url, body, isJson) {
        var headers = { 'X-CSRFToken': CSRF, 'X-Requested-With': 'XMLHttpRequest' };
        if (isJson) headers['Content-Type'] = 'application/json';
        return fetch(url, { method: 'POST', headers: headers, body: body, credentials: 'same-origin' })
            .then(function (r) {
                return r.json().catch(function () {
                    return { ok: false, error: r.status === 413 ? 'File is too large.' : 'Server error (' + r.status + '). Please try again.' };
                });
            })
            .catch(function () { return { ok: false, error: 'Network error. Check your connection and try again.' }; });
    }

    function targetFields(el) {
        var fd = new FormData();
        fd.append('model', el.dataset.cmsModel);
        fd.append('pk', el.dataset.cmsPk);
        fd.append('field', el.dataset.cmsField);
        return fd;
    }

    function sameTarget(el) {
        return document.querySelectorAll('[data-cms-model="' + el.dataset.cmsModel + '"][data-cms-pk="' +
            el.dataset.cmsPk + '"][data-cms-field="' + el.dataset.cmsField + '"]');
    }

    // ----------------------------------------------------------------- text
    var TEXT_SELECTOR = '[data-cms="text"], [data-cms="textarea"]';

    function readText(el) {
        return el.innerText.replace(/ /g, ' ').replace(/\n{3,}/g, '\n\n').trim();
    }

    function setTextEditable(el, on) {
        if (on) {
            try { el.contentEditable = 'plaintext-only'; } catch (e) { el.contentEditable = 'true'; }
            if (el.contentEditable !== 'plaintext-only') el.contentEditable = 'true';
            el.spellcheck = true;
        } else {
            el.removeAttribute('contenteditable');
        }
    }

    function saveText(el) {
        var value = readText(el);
        if (value === el.dataset.cmsOrig) return;
        var fd = targetFields(el);
        fd.append('value', value);
        el.classList.add('cms-saving');
        post(ENDPOINT, fd).then(function (res) {
            el.classList.remove('cms-saving');
            if (res.ok) {
                sameTarget(el).forEach(function (other) { if (other !== el) other.textContent = res.value; });
                el.textContent = res.value;
                el.dataset.cmsOrig = res.value;
                if (el.dataset.cmsList) rebuildList(el, res.value);
                el.classList.add('cms-saved');
                setTimeout(function () { el.classList.remove('cms-saved'); }, 1200);
                toast('Saved ✓');
            } else {
                el.textContent = el.dataset.cmsOrig;
                el.classList.add('cms-error');
                setTimeout(function () { el.classList.remove('cms-error'); }, 2500);
                toast(res.error || 'Could not save.', true);
            }
        });
    }

    function rebuildList(el, value) {
        var ul = el.previousElementSibling;
        if (!ul || !ul.classList.contains('cms-list-view')) return;
        ul.innerHTML = '';
        value.split('\n').forEach(function (line) {
            line = line.trim();
            if (!line) return;
            var li = document.createElement('li');
            if (ul.dataset.icon) {
                var i = document.createElement('i');
                i.className = 'fas ' + ul.dataset.icon + ' me-2';
                li.appendChild(i);
            }
            li.appendChild(document.createTextNode(line));
            ul.appendChild(li);
        });
    }

    document.addEventListener('focusin', function (e) {
        var el = e.target.closest && e.target.closest(TEXT_SELECTOR);
        if (el && editing) el.dataset.cmsOrig = readText(el);
    });
    document.addEventListener('focusout', function (e) {
        var el = e.target.closest && e.target.closest(TEXT_SELECTOR);
        if (el && editing) saveText(el);
    });
    document.addEventListener('keydown', function (e) {
        var el = e.target.closest && e.target.closest(TEXT_SELECTOR);
        if (!el || !editing) return;
        if (e.key === 'Escape') {
            el.textContent = el.dataset.cmsOrig;
            el.blur();
        } else if (e.key === 'Enter' && (el.dataset.cms === 'text' || e.metaKey || e.ctrlKey)) {
            e.preventDefault();
            el.blur();
        } else if (e.key === ' ' && el.closest('button')) {
            e.stopPropagation();
        }
    });
    document.addEventListener('paste', function (e) {
        var el = e.target.closest && e.target.closest(TEXT_SELECTOR);
        if (!el || !editing) return;
        e.preventDefault();
        var text = (e.clipboardData || window.clipboardData).getData('text/plain');
        if (el.dataset.cms === 'text') text = text.replace(/\s*\n\s*/g, ' ');
        document.execCommand('insertText', false, text);
    });
    // While editing, clicking text inside a link/button must not follow the link.
    document.addEventListener('click', function (e) {
        if (!editing) return;
        var editable = e.target.closest('[data-cms], .cms-img-btn, .cms-photo-delete');
        if (editable && e.target.closest('a, button:not(.cms-img-btn):not(.cms-photo-delete)')) {
            e.preventDefault();
        }
    }, true);

    // --------------------------------------------------------------- images
    var picker = document.createElement('input');
    picker.type = 'file';
    picker.accept = 'image/*';
    picker.hidden = true;
    document.body.appendChild(picker);
    var pickerTarget = null;

    var tip = document.createElement('div');
    tip.className = 'cms-img-tip';
    tip.textContent = 'Click to replace image';
    document.body.appendChild(tip);

    function chooseImage(el) { pickerTarget = el; picker.value = ''; picker.click(); }

    picker.addEventListener('change', function () {
        if (picker.files.length && pickerTarget) uploadImage(pickerTarget, picker.files[0]);
    });

    function uploadImage(el, file) {
        var fd = targetFields(el);
        fd.append('file', file);
        el.classList.add('cms-uploading');
        toast('Uploading image…');
        post(ENDPOINT, fd).then(function (res) {
            el.classList.remove('cms-uploading');
            if (!res.ok) { toast(res.error || 'Upload failed.', true); return; }
            sameTarget(el).forEach(function (target) {
                if (target.tagName === 'IMG') {
                    target.removeAttribute('srcset');
                    target.src = res.url;
                } else if (target.dataset.cmsBackground) {
                    target.style.setProperty('--custom-bg-url', 'url("' + res.url + '")');
                    target.classList.add('has-custom-bg');
                } else {
                    window.location.reload(); // placeholder element: re-render the real image
                }
            });
            toast('Image updated ✓');
        });
    }

    function setupImage(el) {
        if (el.dataset.cmsReady) return;
        el.dataset.cmsReady = '1';
        if (el.dataset.cmsBackground) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'cms-img-btn';
            btn.innerHTML = '<i class="fas fa-image"></i> Replace background';
            btn.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); chooseImage(el); });
            if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
            el.appendChild(btn);
            return;
        }
        el.addEventListener('click', function (e) {
            if (!editing) return;
            e.preventDefault();
            e.stopPropagation();
            chooseImage(el);
        });
        el.addEventListener('mousemove', function (e) {
            if (!editing) return;
            tip.style.display = 'block';
            tip.style.left = (e.clientX + 14) + 'px';
            tip.style.top = (e.clientY + 14) + 'px';
        });
        el.addEventListener('mouseleave', function () { tip.style.display = 'none'; });
        // Drag a file straight onto an image to replace it
        el.addEventListener('dragover', function (e) { if (editing && e.dataTransfer.types.indexOf('Files') > -1) e.preventDefault(); });
        el.addEventListener('drop', function (e) {
            if (!editing || !e.dataTransfer.files.length) return;
            e.preventDefault();
            e.stopPropagation();
            uploadImage(el, e.dataTransfer.files[0]);
        });
    }

    // ------------------------------------------------------ gallery manager
    function setupGallery() {
        var drop = document.getElementById('cms-gallery-drop');
        if (drop) {
            var input = drop.querySelector('input[type=file]');
            var status = document.getElementById('cms-gallery-status');
            drop.addEventListener('click', function (e) { if (e.target !== input) input.click(); });
            drop.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
            ['dragenter', 'dragover'].forEach(function (t) {
                drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.add('dragover'); });
            });
            ['dragleave', 'drop'].forEach(function (t) {
                drop.addEventListener(t, function () { drop.classList.remove('dragover'); });
            });
            drop.addEventListener('drop', function (e) { e.preventDefault(); uploadBatch(e.dataTransfer.files); });
            input.addEventListener('change', function () { uploadBatch(input.files); });

            var uploadBatch = function (fileList) {
                var files = Array.prototype.filter.call(fileList, function (f) { return /^image\//.test(f.type); });
                if (!files.length) { toast('Please choose image files.', true); return; }
                var done = 0, failed = [], i = 0, BATCH = 4;
                var next = function () {
                    if (i >= files.length) {
                        status.textContent = '';
                        if (failed.length) toast(failed.join(' • '), true);
                        if (done) { toast(done + ' photo' + (done > 1 ? 's' : '') + ' added ✓'); setTimeout(function () { location.reload(); }, 700); }
                        return;
                    }
                    var fd = new FormData();
                    files.slice(i, i + BATCH).forEach(function (f) { fd.append('files', f); });
                    i += BATCH;
                    status.textContent = 'Uploading… ' + Math.min(i, files.length) + ' of ' + files.length;
                    post(drop.dataset.uploadUrl, fd).then(function (res) {
                        done += (res.photos || []).length;
                        if (res.errors && res.errors.length) failed = failed.concat(res.errors);
                        else if (!res.ok && res.error) failed.push(res.error);
                        next();
                    });
                };
                next();
            };
        }

        document.querySelectorAll('.cms-photo-delete').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                if (!btn.classList.contains('confirm')) {
                    btn.classList.add('confirm');
                    btn.textContent = 'Click again to delete';
                    setTimeout(function () { btn.classList.remove('confirm'); btn.innerHTML = '<i class="fas fa-trash"></i>'; }, 3000);
                    return;
                }
                post(btn.dataset.url, new FormData()).then(function (res) {
                    if (res.ok) { btn.closest('.gallery-item').remove(); toast('Photo deleted'); }
                    else toast(res.error || 'Could not delete.', true);
                });
            });
        });

        // Drag photos to reorder
        var grid = document.querySelector('[data-reorder-url]');
        if (!grid) return;
        var dragged = null;
        grid.addEventListener('dragstart', function (e) {
            var item = e.target.closest('.gallery-item');
            if (!editing || !item) { return; }
            dragged = item;
            item.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        });
        grid.addEventListener('dragover', function (e) {
            if (!dragged) return;
            e.preventDefault();
            var over = e.target.closest('.gallery-item');
            grid.querySelectorAll('.drop-target').forEach(function (n) { n.classList.remove('drop-target'); });
            if (over && over !== dragged) over.classList.add('drop-target');
        });
        grid.addEventListener('drop', function (e) {
            if (!dragged) return;
            e.preventDefault();
            var over = e.target.closest('.gallery-item');
            if (over && over !== dragged) {
                var items = Array.prototype.slice.call(grid.querySelectorAll('.gallery-item'));
                grid.insertBefore(dragged, items.indexOf(dragged) < items.indexOf(over) ? over.nextSibling : over);
                var order = Array.prototype.map.call(grid.querySelectorAll('.gallery-item'), function (n) { return n.dataset.photoId; });
                if (window.balanceCollages) window.balanceCollages();
                post(grid.dataset.reorderUrl, JSON.stringify({ order: order }), true).then(function (res) {
                    toast(res.ok ? 'Order saved ✓' : (res.error || 'Could not save order.'), !res.ok);
                });
            }
        });
        grid.addEventListener('dragend', function () {
            if (dragged) dragged.classList.remove('dragging');
            grid.querySelectorAll('.drop-target').forEach(function (n) { n.classList.remove('drop-target'); });
            dragged = null;
        });
    }

    // --------------------------------------------------------------- toggle
    function setEditing(on) {
        editing = on;
        document.body.classList.toggle('cms-editing', on);
        document.querySelectorAll(TEXT_SELECTOR).forEach(function (el) { setTextEditable(el, on); });
        document.querySelectorAll('.gallery-item[data-photo-id]').forEach(function (el) { el.draggable = on; });
        if (!on) tip.style.display = 'none';
        toggleBtn.innerHTML = on
            ? '<i class="fas fa-check"></i> Done editing'
            : '<i class="fas fa-pen"></i> Edit page';
        toggleBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
        remember(on);
    }

    toggleBtn.addEventListener('click', function () { setEditing(!editing); });

    document.querySelectorAll('[data-cms="image"]').forEach(setupImage);
    setupGallery();

    // ?edit=1 (used by the admin "Edit site live" link) switches edit mode on
    var params = new URLSearchParams(window.location.search);
    var initial = params.has('edit') ? params.get('edit') === '1' : remembered();
    if (params.has('edit')) {
        params.delete('edit');
        var qs = params.toString();
        history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : '') + window.location.hash);
    }
    setEditing(initial);
})();
