"""Üretilen sayfaları headless Chrome ile test eder.
Kullanım: python3 _gen/test_pages.py [slug ...]
Her sayfa için TESTS içindeki girdiler doldurulur, Hesapla'ya basılır, sonuç ve JS hataları raporlanır.
"""
import os, sys, json, http.server, threading, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from tests_data import TESTS

PORT = 8765
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
handler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

only = sys.argv[1:]
fails = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 390, 'height': 900})
    pg.add_init_script("try{localStorage.setItem('cerez','kabul')}catch(e){}")
    errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.route('**/googletagmanager.com/**', lambda r: r.abort())
    for slug, cases in TESTS.items():
        if only and slug not in only: continue
        for ci, case in enumerate(cases):
            errors.clear()
            pg.goto(f'http://127.0.0.1:{PORT}/{slug}.html')
            for k, val in case.get('radio', {}).items():
                pg.click(f'label:has(input[name="{k}"][value="{val}"])')
            for k, val in case.get('fill', {}).items():
                loc = pg.locator('#' + k)
                tag = loc.evaluate('e=>e.tagName')
                if tag == 'SELECT': loc.select_option(str(val))
                else: loc.fill(str(val))
            if case.get('js'): pg.evaluate(case['js'])
            for k in case.get('check', []):
                pg.check('#' + k)
            for k in case.get('uncheck', []):
                pg.uncheck('#' + k)
            pg.click('.btn-calc')
            pg.wait_for_timeout(150)
            main = pg.locator('#result .res-main .v').all_inner_texts()
            toast = pg.locator('#toast').inner_text() if pg.locator('#toast').is_visible() else ''
            rows = pg.locator('#result .res-row').all_inner_texts()
            exp = case.get('expect')
            ok = not errors and (main or case.get('expect_toast'))
            if exp and (not main or exp not in main[0]): ok = False
            if case.get('expect_toast') and case['expect_toast'] not in toast: ok = False
            fails += 0 if ok else 1
            print(('✅' if ok else '❌'), slug, ci, '|', (main[0] if main else 'TOAST: ' + toast), '|', ' ; '.join(r.replace('\n', ': ') for r in rows[:4]), ('| ERR ' + '; '.join(errors) if errors else ''))
    # menü testi
    if not only:
        pg.goto(f'http://127.0.0.1:{PORT}/yas-hesaplama.html'); pg.set_viewport_size({'width': 390, 'height': 800}); pg.click('#hzHam')
        print('menü açılıyor:', pg.locator('#hzLinks').is_visible()); fails += 0 if pg.locator('#hzLinks').is_visible() else 1
    b.close()
# doğruluk denetimi: eski/yanlış rakam, tutmayan örnek hesap, süresi geçmiş veri
try:
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    import dogrula as _dg
    _dh = _dg.run()
    for _x in _dh: print('✗', _x)
    print('DOĞRULUK HATASI:', len(_dh)); fails += len(_dh)
except Exception as _e:
    print('doğruluk denetimi çalışmadı:', _e); fails += 1
print('HATA SAYISI:', fails)
