/* Hesaplarsın — eski hesaplayıcılarda "Kopyala" butonunun yanına WhatsApp paylaş butonu ekler.
   Paylaşılan metin, sayfanın kendi kopyalama fonksiyonunun ürettiği metindir (pano değiştirilmez). */
(function () {
  var SEL = 'button[onclick*="copyResult("],button[onclick*="copyRes("],button[onclick*="copyKazaResult("],button[onclick*="copyAll("]';
  var ICO = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="vertical-align:-2px;margin-right:5px"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>';

  function metniAl(btn) {
    var cb = navigator.clipboard, alinan = null, eski = cb && cb.writeText;
    if (cb) { try { cb.writeText = function (t) { alinan = String(t); return new Promise(function () {}); }; } catch (e) {} }
    try { (new Function(btn.getAttribute('onclick'))).call(btn); } catch (e) {}
    if (cb) { try { delete cb.writeText; if (cb.writeText !== eski) cb.writeText = eski; } catch (e) {} }
    return alinan;
  }

  function paylas(btn) {
    var url = location.href.split('#')[0].split('?')[0];
    var t = metniAl(btn);
    if (!t) t = document.title.split('|')[0].trim();
    else if (t.indexOf('\n') < 0) { var h = document.querySelector('h1'); t = (h ? h.textContent.trim() : document.title.split('|')[0].trim()) + ': ' + t; }
    t = t.replace(/\n?[─—-]{6,}\n?/g, '\n').trim();
    if (t.indexOf('hesaplarsin.com/') === -1) t += '\n\n' + url;
    window.open('https://wa.me/?text=' + encodeURIComponent(t), '_blank', 'noopener');
  }

  function kur() {
    if (typeof window.paylas === 'function') return;
    document.querySelectorAll(SEL).forEach(function (b) {
      if (b.dataset.hzPay) return;
      b.dataset.hzPay = '1';
      var p = document.createElement('button');
      p.type = 'button';
      p.className = b.className.replace(/\bcopy-btn\b/, 'copy-btn hz-wa');
      if (p.className.indexOf('hz-wa') < 0) p.className += ' hz-wa';
      p.innerHTML = ICO + 'WhatsApp’ta Paylaş';
      p.setAttribute('aria-label', 'Sonucu WhatsApp’ta paylaş');
      p.addEventListener('click', function () { paylas(b); });
      b.insertAdjacentElement('afterend', p);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', kur); else kur();
})();
