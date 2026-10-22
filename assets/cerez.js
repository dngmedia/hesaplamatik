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
