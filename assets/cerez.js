/* Hesaplarsın çerez bildirimi (KVKK + Google Consent Mode v2) */
(function () {
  var K = 'cerez';
  function get() { try { return localStorage.getItem(K); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(K, v); } catch (e) {} }
  function apply(v) {
    if (!window.gtag) return;
    var s = v === 'kabul' ? 'granted' : 'denied';
    gtag('consent', 'update', { ad_storage: s, ad_user_data: s, ad_personalization: s, analytics_storage: s });
  }
  function kapat() { var b = document.getElementById('cerez-bant'); if (b) b.remove(); }
  function ac() {
    if (document.getElementById('cerez-bant')) return;
    var d = document.createElement('div');
    d.id = 'cerez-bant';
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-label', 'Çerez bildirimi');
    d.style.cssText = 'position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:720px;margin:0 auto;background:#111827;color:#f9fafb;border-radius:14px;padding:16px 18px;box-shadow:0 10px 30px rgba(0,0,0,.25);font:500 14px/1.55 -apple-system,Segoe UI,Roboto,sans-serif;display:flex;flex-wrap:wrap;gap:12px;align-items:center';
    d.innerHTML = '<div style="flex:1 1 320px">🍪 Sitemizde analiz ve reklam amaçlı çerezler kullanıyoruz. Hesaplama verileriniz kaydedilmez. Ayrıntılar: <a href="/gizlilik-politikasi.html" style="color:#93c5fd">Gizlilik Politikası</a>.</div>' +
      '<div style="display:flex;gap:8px;flex-wrap:wrap"><button type="button" id="cerez-red" style="background:transparent;color:#f9fafb;border:1px solid #4b5563;border-radius:10px;padding:9px 14px;font-weight:700;cursor:pointer">Reddet</button>' +
      '<button type="button" id="cerez-kabul" style="background:#1a56db;color:#fff;border:0;border-radius:10px;padding:9px 16px;font-weight:800;cursor:pointer">Kabul et</button></div>';
    document.body.appendChild(d);
    document.getElementById('cerez-kabul').onclick = function () { set('kabul'); apply('kabul'); kapat(); };
    document.getElementById('cerez-red').onclick = function () { set('red'); apply('red'); kapat(); };
  }
  window.cerezTercihleri = ac;
  function init() {
    var v = get();
    if (v) apply(v); else ac();
    var f = document.querySelector('footer');
    if (f && !document.getElementById('cerez-link')) {
      var p = document.createElement('p');
      p.style.cssText = 'text-align:center;font-size:12px;margin:10px 0 0';
      p.innerHTML = '<a href="#" id="cerez-link" style="color:inherit;text-decoration:underline">Çerez tercihleri</a>';
      f.appendChild(p);
      document.getElementById('cerez-link').onclick = function (e) { e.preventDefault(); ac(); };
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

/* Hesaplarsın – GA4 olay takibi (hesapla, paylaş, kopyala, kart, araca geçiş, SSS) */
(function () {
  var slug = (location.pathname.replace(/^\/|\.html$/g, '') || 'anasayfa');
  var son = {};
  function ev(ad, p) {
    if (typeof gtag !== 'function') return;
    var k = ad + (p && p.tur || ''), t = Date.now();
    if (son[k] && t - son[k] < 3000) return; son[k] = t;
    p = p || {}; p.sayfa = slug;
    gtag('event', ad, p);
  }
  window.hsOlay = ev;
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button,a');
    if (!b) return;
    var oc = (b.getAttribute('onclick') || '').toLowerCase();
    var tx = (b.textContent || '').trim().toLowerCase();
    var cls = b.className || '';
    if (b.tagName === 'BUTTON') {
      if (/faq-q/.test(cls)) return ev('sss_ac', { tur: tx.slice(0, 80) });
      if (/kart/.test(oc)) return ev('kart_paylas', { tur: /indir/.test(oc) ? 'indir' : 'paylas' });
      if (/paylas|share|whatsapp/.test(oc + tx)) return ev('share', { method: /whatsapp/.test(oc + tx) ? 'whatsapp' : 'diger', content_type: 'sonuc', item_id: slug });
      if (/kopyala/.test(oc + tx)) return ev('sonuc_kopyala');
      if (/btn-calc/.test(cls) || /^run\(|hesapla\(/.test(oc) || /hesapla|göster|hesap/.test(tx)) return ev('hesapla', { arac: slug });
      return;
    }
    var h = b.getAttribute('href') || '';
    if (/^(https:\/\/hesaplarsin\.com)?\/?[a-z0-9-]+\.html/.test(h) && !/blog/.test(h) && slug !== h.replace(/^.*\/|\.html.*$/g, '')) {
      var hedef = h.replace(/^.*\/|\.html.*$/g, '');
      if (/hesapla|maas|takvim|siralama|faiz|tazminat|harc|ucret|zam/.test(hedef)) ev('araca_gecis', { tur: hedef, hedef: hedef });
    }
  }, true);
  /* otomatik hesaplayan sayfalar için: ilk girişte bir kez */
  var girdi = false;
  document.addEventListener('input', function (e) {
    if (girdi || !e.target.matches || !e.target.matches('main input, main select, .calc input, .calc select, input, select')) return;
    if (e.target.id === 'heroSearch') return;
    girdi = true; ev('arac_kullan', { arac: slug });
  }, true);
  document.addEventListener('DOMContentLoaded', function () {
    var s = document.getElementById('heroSearch');
    if (s) s.addEventListener('change', function () { if (s.value.trim()) ev('search', { search_term: s.value.trim().slice(0, 60) }); });
  });
})();
