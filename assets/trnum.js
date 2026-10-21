/* Hesaplarsın: Türkçe sayı girişi. "50.000" -> 50000, "34,5" -> 34.5 */
(function () {
  var d = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
  function norm(v) {
    v = String(v == null ? '' : v).trim().replace(/[\s₺%]/g, '');
    if (!v) return v;
    if (v.indexOf(',') > -1) return v.replace(/\./g, '').replace(',', '.');
    if (/^-?\d{1,3}(\.\d{3})+$/.test(v)) return v.replace(/\./g, '');
    return v;
  }
  function fix(el) {
    if (el.__trnum) return;
    el.__trnum = true;
    el.type = 'text';
    el.setAttribute('inputmode', 'decimal');
    el.setAttribute('autocomplete', 'off');
    Object.defineProperty(el, 'value', {
      configurable: true,
      get: function () { return norm(d.get.call(el)); },
      set: function (x) { d.set.call(el, x); }
    });
  }
  function run() { document.querySelectorAll('input[type="number"]').forEach(fix); }
  run();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
})();
