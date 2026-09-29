/*
 * paginate.js — self-numbering for the proposal documents.
 *
 * The document is authored as a sequence of fixed-height `.page` sections,
 * one per physical PDF page (see `.page { height: var(--page-h); overflow:
 * hidden }` in styles.css). That makes a page's number a pure function of its
 * position in the DOM, so we compute every number at load time instead of
 * storing any in the HTML.
 *
 * Runs in the browser preview and inside Puppeteer (build.mjs waits for the
 * `data-paginated` flag before printing). Nothing here is document-specific,
 * so the same file serves technical.html and commercial.html.
 *
 * What it fills:
 *   - .runner__page  -> the page's 1-based ordinal (zero-padded)
 *   - .toc__page     -> the ordinal of the page its TOC anchor (#href) targets
 */
(function () {
  function paginate() {
    var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
    var width = Math.max(2, String(pages.length).length);

    function pad(n) {
      var s = String(n);
      while (s.length < width) s = '0' + s;
      return s;
    }

    // Map each .page element to its 1-based physical ordinal.
    var ordinalOf = new Map();
    pages.forEach(function (pg, i) { ordinalOf.set(pg, i + 1); });

    // 1) Running page numbers in the top/bottom runners.
    pages.forEach(function (pg, i) {
      var slots = pg.querySelectorAll('.runner__page');
      for (var s = 0; s < slots.length; s++) slots[s].textContent = pad(i + 1);
    });

    // 2) TOC page numbers, resolved from each entry's anchor target.
    var unresolved = [];
    var entries = document.querySelectorAll('.toc__entry');
    for (var e = 0; e < entries.length; e++) {
      var entry = entries[e];
      var cell = entry.querySelector('.toc__page');
      if (!cell) continue;
      var href = entry.getAttribute('href') || '';
      var target = href.charAt(0) === '#' ? document.getElementById(href.slice(1)) : null;
      var pg = target ? target.closest('.page') : null;
      if (pg && ordinalOf.has(pg)) {
        cell.textContent = pad(ordinalOf.get(pg));
      } else {
        cell.textContent = '??';
        unresolved.push(href || '(no href)');
      }
    }
    if (unresolved.length) {
      console.warn('[paginate] TOC anchors did not resolve: ' + unresolved.join(', '));
    }

    document.documentElement.setAttribute('data-paginated', 'true');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', paginate);
  } else {
    paginate();
  }
})();
