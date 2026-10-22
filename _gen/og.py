"""Araç ve kategori sayfaları için 1200×630 paylaşım (OG) görselleri üretir: assets/og/<slug>.jpg
Var olan görselleri atlar (yeniden üretmek için: python3 _gen/og.py --force [slug ...]).
build.py, assets/og/<slug>.jpg bulunan sayfaların og:image / twitter:image etiketini otomatik bu görsele çevirir.
"""
import os, re, sys, glob, html as H
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
LOGO = open('assets/favicon.svg', encoding='utf-8').read()
_ix = open('index.html', encoding='utf-8').read()
ICO = {u: i for i, u in re.findall(r"\{ico:'([^']*)',name:'[^']*',desc:(?:'[^']*'|\"[^\"]*\"),url:'/([^']*)\.html'", _ix)}
PROTECT = {'maas-siralamasi'}  # elle tasarlanmış görseller
SKIP = {'index', '404', 'blog', 'hakkimizda', 'iletisim', 'gizlilik-politikasi', 'kullanim-sartlari', 'cerez-politikasi', 'yontem-ve-kaynaklar'}
CSS = """*{margin:0;padding:0;box-sizing:border-box}body{width:1200px;height:630px;overflow:hidden;font-family:Inter,-apple-system,Segoe UI,Roboto,Arial,sans-serif}
.c{width:1200px;height:630px;padding:60px 70px;display:flex;flex-direction:column;color:#fff;position:relative;background:linear-gradient(135deg,#0f307a 0%,#1341b0 55%,#1a56db 100%)}
.b{position:absolute;border-radius:50%;background:rgba(255,255,255,.07)}.top{display:flex;align-items:center;gap:14px;font-weight:800;font-size:30px;z-index:2}.top svg{width:52px;height:52px}
.ico{position:absolute;right:80px;top:150px;font-size:150px;opacity:.95;z-index:2}
h1{margin-top:auto;font-size:68px;font-weight:900;letter-spacing:-1.5px;line-height:1.05;max-width:900px;z-index:2}p{margin-top:18px;font-size:27px;font-weight:600;opacity:.9;max-width:960px;line-height:1.35;z-index:2}
.f{margin-top:28px;display:flex;gap:10px;z-index:2}.f span{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.28);border-radius:999px;padding:7px 16px;font-size:20px;font-weight:700}
.f .u{background:#fff;color:#1341b0;border:none;margin-left:auto}"""


def info(p):
    s = open(p, encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    if not m: return None
    h1 = re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', m.group(1)))).strip()
    h1 = re.sub(r'^[^\wÇĞİÖŞÜçğıöşü0-9]+', '', h1)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    d = H.unescape(d.group(1)) if d else ''
    sub = re.split(r'(?<=[.!?])\s', d)[0]
    if len(sub) > 125: sub = sub[:125].rsplit(' ', 1)[0].rstrip(',;:') + '…'
    ico = re.search(r'<span class="hero-tag">([^ <]+)', s)
    slug = os.path.basename(p)[:-5]
    return h1, sub, (ICO.get(slug) or (ico.group(1) if ico else '🧮'))


def main(force, only):
    os.makedirs('assets/og', exist_ok=True)
    pages = [p for p in sorted(glob.glob('*.html')) if p[:-5] not in SKIP and not p.startswith(('yandex_', 'google', 'blog-', 'kov-'))]
    todo = []
    for p in pages:
        slug = p[:-5]
        if only and slug not in only: continue
        if os.path.exists(f'assets/og/{slug}.jpg') and (not force or slug in PROTECT): continue
        s = open(p, encoding='utf-8').read()
        if 'noindex' in s: continue
        i = info(p)
        if i: todo.append((slug, i))
    if not todo: print('üretilecek görsel yok'); return
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': 1200, 'height': 630})
        for slug, (h1, sub, ico) in todo:
            size = 68 if len(h1) <= 28 else 58 if len(h1) <= 40 else 50
            doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="c">
<div class="b" style="width:520px;height:520px;right:-140px;top:-200px"></div><div class="b" style="width:300px;height:300px;right:260px;bottom:-200px"></div>
<div class="top">{LOGO}<span>Hesaplarsın</span></div><div class="ico">{ico}</div>
<h1 style="font-size:{size}px">{H.escape(h1)}</h1><p>{H.escape(sub)}</p>
<div class="f"><span>✓ Ücretsiz</span><span>2026 güncel</span><span class="u">hesaplarsin.com</span></div></div></body></html>'''
            pg.set_content(doc); pg.wait_for_timeout(80)
            pg.screenshot(path=f'assets/og/{slug}.jpg', type='jpeg', quality=82)
            # sayfadaki etiketi hemen güncelle
            p = slug + '.html'; s = open(p, encoding='utf-8').read(); u = f'https://hesaplarsin.com/assets/og/{slug}.jpg'
            s = re.sub(r'<meta property="og:image" content="[^"]*"', f'<meta property="og:image" content="{u}"', s)
            s = re.sub(r'<meta name="twitter:image" content="[^"]*"', f'<meta name="twitter:image" content="{u}"', s)
            s = re.sub(r'<meta property="og:image:height" content="\d+"', '<meta property="og:image:height" content="630"', s)
            open(p, 'w', encoding='utf-8').write(s)
        b.close()
    print(len(todo), 'görsel üretildi')


if __name__ == '__main__':
    a = sys.argv[1:]; f = '--force' in a
    main(f, set(x for x in a if x != '--force'))
