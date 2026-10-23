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
    el.setAttribute('data-trnum', '');
    el.type = 'text';
    el.setAttribute('inputmode', 'decimal');
    el.setAttribute('autocomplete', 'off');
    Object.defineProperty(el, 'value', {
      configurable: true,
      get: function () { return norm(d.get.call(el)); },
      set: function (x) { d.set.call(el, x); }
    });
  }
  /* Sayfa CSS'indeki input[type=number] kurallarını text'e çevrilen alanlara da uygula (görünüm bozulmasın) */
  var css = false;
  function copyCss() {
    if (css) return; css = true;
    var re = /input\[type=["']?number["']?\]/g;
    function walk(rules, target) {
      for (var i = 0; i < rules.length; i++) {
        var r = rules[i];
        if (r.cssRules && r.media) { walk(r.cssRules, r); continue; }
        if (r.selectorText && re.test(r.selectorText)) {
          re.lastIndex = 0;
          var sel = r.selectorText.replace(re, 'input[data-trnum]');
          try { (target || sheetRef).insertRule(sel + '{' + r.style.cssText + '}', (target || sheetRef).cssRules.length); } catch (e) {}
        }
        re.lastIndex = 0;
      }
    }
    for (var j = 0; j < document.styleSheets.length; j++) {
      var sh = document.styleSheets[j], rules;
      try { rules = sh.cssRules; } catch (e) { continue; }
      if (!rules) continue;
      var sheetRef = sh;
      (function (sheet) { sheetRef = sheet; walk(Array.prototype.slice.call(sheet.cssRules), null); })(sh);
    }
  }
  var sheetRef = null;
  function run() {
    var l = document.querySelectorAll('input[type="number"]');
    var t = document.querySelectorAll('input[type="text"][inputmode="decimal"],input[type="text"][inputmode="numeric"]');
    if (l.length || t.length) copyCss();
    l.forEach(fix);
    t.forEach(function (e) { e.setAttribute('data-trnum', ''); });  /* sayfanın kendi metin alanlarına da aynı görünüm */
  }
  run();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
})();
