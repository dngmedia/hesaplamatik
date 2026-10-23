"""Site geneli tek üst menü + tek alt bilgi ("site chrome").
Tüm sayfalardaki eski <nav>/<footer> bloklarını aynı tasarımla değiştirir. build.py'nin EN SONUNDA çalışır; idempotenttir.
Eski sayfa scriptleri #hamBtn / #navLinks bekler: başlıkta gizli yedek öğeler bırakılır, menü kendi id'leriyle (hzHam/hzLinks) çalışır.
"""
import os, re, glob

B = 'https://hesaplarsin.com'
LOGO = ('<svg width="28" height="28" viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="hzg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1341b0"/>'
        '<stop offset="1" stop-color="#1a56db"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="url(#hzg)"/><rect x="14" y="12" width="36" height="12" rx="3" fill="#fff" opacity=".95"/>'
        '<g fill="#fff"><rect x="14" y="30" width="9" height="9" rx="2"/><rect x="27.5" y="30" width="9" height="9" rx="2"/><rect x="41" y="30" width="9" height="9" rx="2" fill="#fbbf24"/>'
        '<rect x="14" y="43" width="9" height="9" rx="2"/><rect x="27.5" y="43" width="9" height="9" rx="2"/><rect x="41" y="43" width="9" height="9" rx="2" fill="#fbbf24"/></g></svg>')
NAV = [('maas-hesaplamalari', 'Maaş'), ('memur-hesaplamalari', 'Memur'), ('vergi-hesaplamalari', 'Vergi'), ('finans-hesaplamalari', 'Finans'),
       ('isletme-hesaplamalari', 'İşletme'), ('emlak-hesaplamalari', 'Emlak'), ('ekonomi-takvimi', 'Takvim'), ('blog', 'Blog')]

CSS = '''<style id="hz-chrome">
.hz-head{position:sticky;top:0;z-index:300;background:#fff;border-bottom:1px solid #e5e7eb;box-shadow:0 1px 4px rgba(0,0,0,.05);margin:0;padding:0;font-family:Inter,-apple-system,Segoe UI,Roboto,Arial,sans-serif}
.hz-head *{box-sizing:border-box}
.hz-in{max-width:1140px;margin:0 auto;padding:0 16px;height:60px;display:flex;align-items:center;gap:14px}
.hz-logo{display:flex;align-items:center;gap:9px;font-size:1.15rem;font-weight:800;color:#0f172a!important;text-decoration:none!important;white-space:nowrap;margin-right:auto}
.hz-nav{display:flex;align-items:center;gap:2px;background:none;padding:0;margin:0;position:static;box-shadow:none;border:0}
.hz-nav a{font-size:.86rem;font-weight:600;color:#475569!important;text-decoration:none!important;padding:7px 10px;border-radius:8px;white-space:nowrap;background:none}
.hz-nav a:hover,.hz-nav a.on{background:#e8f0fe;color:#1a56db!important}
.hz-nav a.hz-cta{margin-left:8px;background:#1a56db!important;color:#fff!important;font-weight:700!important;padding:8px 14px!important}
.hz-nav a.hz-cta:hover{background:#1341b0!important;color:#fff!important}
.hz-ham{display:none;background:none;border:0;cursor:pointer;padding:8px;margin:0}
.hz-ham span{display:block;width:22px;height:2px;background:#0f172a;margin:5px 0;border-radius:2px}
.hz-hide{display:none!important}
@media(max-width:960px){.hz-ham{display:block}.hz-nav{display:none;position:absolute;top:60px;left:0;right:0;background:#fff;flex-direction:column;align-items:stretch;padding:10px 16px 16px;border-bottom:1px solid #e5e7eb;box-shadow:0 8px 20px rgba(0,0,0,.08)}
.hz-nav.open{display:flex}.hz-nav a{padding:12px;font-size:.98rem}.hz-nav a.hz-cta{margin:6px 0 0;text-align:center}}
footer.hz-foot{background:#0f172a;color:#94a3b8;padding:40px 16px 22px;margin:48px 0 0;font-family:Inter,-apple-system,Segoe UI,Roboto,Arial,sans-serif;font-size:14px;line-height:1.6;text-align:left}
footer.hz-foot *{box-sizing:border-box}
.hz-fin{max-width:1140px;margin:0 auto}
.hz-fgrid{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:28px;margin-bottom:26px}
@media(max-width:760px){.hz-fgrid{grid-template-columns:1fr 1fr}.hz-fbrand{grid-column:1/-1}}
footer.hz-foot a.hz-logo{display:flex;color:#fff!important;margin:0 0 10px;font-size:1.15rem}
footer.hz-foot p{margin:0 0 8px;font-size:.84rem;color:#94a3b8}
footer.hz-foot .hz-ft{font-size:.84rem;font-weight:700;color:#fff;margin:0 0 10px;text-transform:none;letter-spacing:0}
footer.hz-foot a{display:block;color:#94a3b8!important;text-decoration:none!important;font-size:.84rem;margin:0 0 7px}
footer.hz-foot a:hover{color:#fff!important}
.hz-soc{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}.hz-soc a{display:inline-block;margin:0;border:1px solid #334155;border-radius:999px;padding:4px 12px}
.hz-fbot{border-top:1px solid #1e293b;padding-top:16px;font-size:.78rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
.hz-fbot a{display:inline!important;margin:0!important}
</style>'''

SCRIPT = '''<script id="hz-js">(function(){var b=document.getElementById('hzHam'),n=document.getElementById('hzLinks');if(!b||!n)return;
b.addEventListener('click',function(e){e.stopPropagation();var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);});
document.addEventListener('click',function(e){if(!n.contains(e.target)&&e.target!==b)n.classList.remove('open');});})();</script>'''


def header(active):
    links = ''.join(f'<a href="{B}/{s}.html"{" class=\"on\"" if s == active else ""}>{t}</a>' for s, t in NAV)
    return (f'<!--HZ-HEAD--><div class="hz-head" role="banner"><div class="hz-in">'
            f'<a class="hz-logo" href="{B}/" aria-label="Hesaplarsın ana sayfa">{LOGO}<span>Hesaplarsın</span></a>'
            f'<nav class="hz-nav" id="hzLinks" aria-label="Ana menü">{links}<a class="hz-cta" href="{B}/#araclar">Tüm Araçlar</a></nav>'
            f'<button class="hz-ham" id="hzHam" type="button" aria-label="Menüyü aç" aria-expanded="false"><span></span><span></span><span></span></button>'
            f'<span id="hamBtn" class="hz-hide"></span><span id="navLinks" class="hz-hide"></span>'
            f'</div></div><!--/HZ-HEAD-->')


FOOTER = (f'<!--HZ-FOOT--><footer class="hz-foot"><div class="hz-fin"><div class="hz-fgrid">'
          f'<div class="hz-fbrand"><a class="hz-logo" href="{B}/">{LOGO}<span>Hesaplarsın</span></a>'
          f'<p>Türkiye’nin ücretsiz hesaplama platformu: maaş, vergi, kredi, emeklilik ve daha fazlası; 2026 güncel resmî verilerle, kayıt gerektirmeden.</p>'
          f'<div class="hz-soc"><a href="https://www.instagram.com/hesaplarsin" target="_blank" rel="noopener noreferrer">Instagram</a><a href="https://x.com/hesaplarsin" target="_blank" rel="noopener noreferrer">X</a><a href="mailto:info@hesaplarsin.com">E-posta</a></div></div>'
          f'<div><div class="hz-ft">Popüler araçlar</div><a href="{B}/net-maas-hesaplama.html">Net Maaş Hesaplama</a><a href="{B}/kdv-hesaplama.html">KDV Hesaplama</a>'
          f'<a href="{B}/kredi-hesaplama.html">Kredi Hesaplama</a><a href="{B}/emeklilik-yasi-hesaplama.html">Emeklilik Hesaplama</a><a href="{B}/asgari-ucret-2027-hesaplama.html">Asgari Ücret 2027</a></div>'
          f'<div><div class="hz-ft">Kategoriler</div>' + ''.join(f'<a href="{B}/{s}.html">{t}</a>' for s, t in [
              ('maas-hesaplamalari', 'Maaş ve SGK'), ('memur-hesaplamalari', 'Kamu ve Memur'), ('vergi-hesaplamalari', 'Vergi'), ('finans-hesaplamalari', 'Finans ve Kredi'),
              ('isletme-hesaplamalari', 'İşletme'), ('emlak-hesaplamalari', 'Emlak ve Kira'), ('arac-hesaplamalari', 'Araç'), ('saglik-hesaplamalari', 'Sağlık'),
              ('egitim-hesaplamalari', 'Eğitim'), ('gunluk-hesaplamalar', 'Günlük')]) + '</div>'
          f'<div><div class="hz-ft">Hesaplarsın</div><a href="{B}/hakkimizda.html">Hakkımızda</a><a href="{B}/yontem-ve-kaynaklar.html">Yöntem ve Kaynaklar</a>'
          f'<a href="{B}/turkiye-maaslari-2026.html">Türkiye’de Maaşlar 2026</a><a href="{B}/ekonomi-takvimi.html">Ekonomi Takvimi</a><a href="{B}/blog.html">Blog</a>'
          f'<a href="{B}/iletisim.html">İletişim</a><a href="{B}/gizlilik-politikasi.html">Gizlilik Politikası</a><a href="{B}/kullanim-sartlari.html">Kullanım Şartları</a></div>'
          f'</div><div class="hz-fbot"><span>© 2026 Hesaplarsın · Sonuçlar bilgilendirme amaçlıdır; resmî işlemler için yetkili kurumlara danışın.</span>'
          f'<span><a href="mailto:info@hesaplarsin.com">info@hesaplarsin.com</a></span></div></div></footer><!--/HZ-FOOT-->')

# Başlık alanı (hero) farklı tasarlanmış eski sayfalar: site geneliyle aynı mavi başlık
HERO_FIX = {'kdv-hesaplama', 'net-maas-hesaplama', 'kredi-hesaplama', 'amortisman-hesaplama', 'komisyon-hesaplama'}
HERO_CSS = """<style id="hz-hero">
header.hero{background:linear-gradient(135deg,#0f307a 0%,#1341b0 50%,#1a56db 100%)!important;color:#fff!important;max-width:none!important;width:auto!important;margin:0 0 28px!important;padding:40px max(16px,calc((100vw - 1108px)/2)) 44px!important;text-align:left!important;border-radius:0!important;box-sizing:border-box!important;border:0!important}
header.hero h1{color:#fff!important;-webkit-text-fill-color:#fff!important;font-size:clamp(1.7rem,4vw,2.4rem)!important;font-weight:900!important;letter-spacing:-.5px!important;line-height:1.15!important;margin:12px 0 10px!important}
header.hero h1 span{background:none!important;-webkit-text-fill-color:#fbbf24!important;color:#fbbf24!important}
header.hero .hero-inner{max-width:none!important;margin:0!important;padding:0!important;text-align:left!important}
header.hero p,header.hero .hero-sub{color:rgba(255,255,255,.9)!important;max-width:680px!important;font-size:1rem!important;line-height:1.6!important;margin:0 0 6px!important}
header.hero .hero-badge,header.hero .hbadge,header.hero .hero-chip{background:rgba(255,255,255,.14)!important;color:#fff!important;border:1px solid rgba(255,255,255,.28)!important}
header.hero .hero-chip *{color:#fff!important}
header.hero .hero-chips{background:none!important;border:0!important;padding:0!important;margin-top:14px!important}
</style>"""

CAT = {  # sayfa -> menüde vurgulanacak kategori
    'maas': 'maas-hesaplamalari', 'kamu': 'memur-hesaplamalari', 'vergi': 'vergi-hesaplamalari', 'finans': 'finans-hesaplamalari',
    'isletme': 'isletme-hesaplamalari', 'gayrimenkul': 'emlak-hesaplamalari'}
SKIP = ('yandex_', 'google', 'blog-', 'kov-')


def active_for(p, s, idx):
    slug = p[:-5]
    if p.startswith('blog'):
        return 'blog'
    if slug in [x for x, _ in NAV]:
        return slug
    c = idx.get(slug)
    return CAT.get(c, '')


def run():
    ix = open('index.html', encoding='utf-8').read()
    idx = {u: c for u, c in re.findall(r"url:'/([^']*)\.html',cat:'([^']*)'", ix)}
    n = 0; skipped = []
    for p in sorted(glob.glob('*.html') + glob.glob('blog/*.html')):
        if os.path.basename(p).startswith(SKIP):
            continue
        s = open(p, encoding='utf-8').read(); o = s
        bi = s.find('<body')
        if bi < 0:
            skipped.append(p); continue
        head, body = s[:bi], s[bi:]
        # üst menü
        if '<!--HZ-HEAD-->' in body:
            body = re.sub(r'<!--HZ-HEAD-->.*?<!--/HZ-HEAD-->', lambda m: header(active_for(p, s, idx)), body, count=1, flags=re.S)
        else:
            m = re.search(r'<nav\b[^>]*>.*?</nav>', body, re.S) if p != '404.html' else re.search(r'<header>.*?</header>', body, re.S)
            if not m or m.start() > 6000:
                skipped.append(p); continue
            body = body[:m.start()] + header(active_for(p, s, idx)) + body[m.end():]
        # alt bilgi
        if '<!--HZ-FOOT-->' in body:
            body = re.sub(r'<!--HZ-FOOT-->.*?<!--/HZ-FOOT-->', lambda m: FOOTER, body, count=1, flags=re.S)
        else:
            m = re.search(r'<footer\b[^>]*>.*?</footer>', body, re.S)
            if m:
                body = body[:m.start()] + FOOTER + body[m.end():]
            else:
                body = body.replace('</body>', FOOTER + '\n</body>', 1)
        # css + js
        head = re.sub(r'<style id="hz-chrome">.*?</style>\n?', '', head, flags=re.S)
        head = head.replace('</head>', CSS + '\n</head>', 1)
        head = re.sub(r'<style id="hz-hero">.*?</style>\n?', '', head, flags=re.S)
        if p[:-5] in HERO_FIX:
            head = head.replace('</head>', HERO_CSS + '\n</head>', 1)
        body = re.sub(r'<script id="hz-js">.*?</script>\n?', '', body, flags=re.S)
        body = body.replace('</body>', SCRIPT + '\n</body>', 1)
        s = head + body
        if s != o:
            open(p, 'w', encoding='utf-8').write(s); n += 1
    return n, skipped


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(run())
