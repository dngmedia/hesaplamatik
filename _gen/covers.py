"""Blog yazıları için 1200×675 kapak görselleri üretir (Discover/OG) ve yazıya bağlar.
Kullanım: python3 _gen/covers.py [slug ...]   (repo kökünden; argümansız tüm yazılar)
"""
import os, re, sys, json, glob, html as H
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LOGO = open('assets/favicon.svg', encoding='utf-8').read()
OUT = 'assets/blog'
os.makedirs(OUT, exist_ok=True)

THEMES = {  # rozet anahtar kelimesi -> (renk1, renk2)
    'emekli': ('#1e3a8a', '#2563eb'), 'maaş': ('#1e3a8a', '#2563eb'), 'işçi': ('#7f1d1d', '#dc2626'),
    'vergi': ('#7c2d12', '#ea580c'), 'kira': ('#065f46', '#10b981'), 'gayrimenkul': ('#065f46', '#10b981'),
    'banka': ('#312e81', '#6366f1'), 'kredi': ('#312e81', '#6366f1'), 'ekonomi': ('#0f307a', '#1a56db'),
    'tazminat': ('#7f1d1d', '#dc2626'), 'sigorta': ('#134e4a', '#0d9488'), 'hukuk': ('#4c1d95', '#7c3aed'), 'veri': ('#0f307a', '#1a56db'),
}
DEFAULT = ('#0f307a', '#1a56db')

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:675px;font-family:'Inter',sans-serif;overflow:hidden}
.c{width:1200px;height:675px;position:relative;padding:64px 72px;display:flex;flex-direction:column;color:#fff;background:linear-gradient(135deg,var(--a) 0%,var(--b) 100%)}
.blob{position:absolute;border-radius:50%;background:rgba(255,255,255,.07)}
.top{display:flex;align-items:center;gap:14px;font-weight:800;font-size:30px;z-index:2}
.top svg{width:50px;height:50px}
.pill{margin-left:auto;background:#f59e0b;color:#fff;font-weight:800;font-size:24px;padding:10px 22px;border-radius:999px}
h1{z-index:2;margin-top:auto;font-weight:900;letter-spacing:-1.8px;line-height:1.08;max-width:1020px}
.foot{z-index:2;margin-top:34px;display:flex;align-items:center;gap:18px;font-size:24px;font-weight:600;opacity:.85}
.dot{width:8px;height:8px;border-radius:50%;background:#fbbf24}
"""


def theme(badges):
    t = ' '.join(badges).lower()
    for k, v in THEMES.items():
        if k in t:
            return v
    return DEFAULT


def info(path):
    s = open(path, encoding='utf-8').read()
    h1 = H.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))).strip()
    badges = [H.unescape(re.sub(r'<[^>]+>', '', b)).strip() for b in re.findall(r'<span class="meta-badge[^"]*">(.*?)</span>', s, re.S)]
    m = re.search(r'<span>📅 ([^<]+)</span>', s)
    date = m.group(1).strip() if m else ''
    cat = re.sub(r'^[^\wÇĞİÖŞÜçğıöşü]+', '', badges[-1]).strip() if badges else 'Rehber'
    return s, h1, badges, cat, date


def size(t):
    n = len(t)
    return 76 if n <= 45 else 66 if n <= 62 else 58 if n <= 80 else 50


def attach(path, slug, s, h1):
    url = f'https://hesaplarsin.com/assets/blog/{slug}.jpg'
    img = (f'<div class="article-hero"><img src="/assets/blog/{slug}.jpg" width="1200" height="675" alt="{H.escape(h1)}" '
           f'fetchpriority="high" decoding="async" style="width:100%;height:auto;display:block;border-radius:16px"></div>')
    s = re.sub(r'<div class="article-hero">.*?</svg>\s*</div>', img, s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', f'<meta property="og:image" content="{url}"', s)
    s = re.sub(r'<meta property="og:image:height" content="\d+"', '<meta property="og:image:height" content="675"', s)
    s = re.sub(r'<meta name="twitter:image" content="[^"]*"', f'<meta name="twitter:image" content="{url}"', s)
    def art(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if isinstance(d, dict) and d.get('@type') in ('Article', 'BlogPosting', 'NewsArticle'):
            d['image'] = [url]
            return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'
        return m.group(0)
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', art, s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)


def main(only):
    posts = sorted(glob.glob('blog/*.html'))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': 1200, 'height': 675})
        for path in posts:
            slug = os.path.basename(path)[:-5]
            if only and slug not in only:
                continue
            s, h1, badges, cat, date = info(path)
            a, c = theme(badges)
            doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="c" style="--a:{a};--b:{c}">
<div class="blob" style="width:560px;height:560px;right:-160px;top:-220px"></div>
<div class="blob" style="width:380px;height:380px;right:180px;bottom:-240px"></div>
<div class="top">{LOGO}<span>Hesaplarsın</span><span class="pill">{H.escape(cat)}</span></div>
<h1 style="font-size:{size(h1)}px">{H.escape(h1)}</h1>
<div class="foot"><span>hesaplarsin.com</span><span class="dot"></span><span>{H.escape(date)}</span></div>
</div></body></html>'''
            pg.set_content(doc)
            pg.wait_for_timeout(120)
            pg.screenshot(path=f'{OUT}/{slug}.jpg', type='jpeg', quality=86)
            attach(path, slug, s, h1)
            print('✓', slug)
        b.close()


if __name__ == '__main__':
    main(set(sys.argv[1:]))
