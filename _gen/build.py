"""Kullanım: python3 _gen/build.py  (repo kökünden)"""
import os, re, sys, json, glob, importlib
sys.path.insert(0, os.path.dirname(__file__))
from template import render, BASE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def registry():
    s = open('index.html', encoding='utf-8').read()
    reg = {}
    for m in re.finditer(r"\{ico:'([^']*)',name:'([^']*)',desc:(['\"])(.*?)\3,url:'/([^']+)\.html'", s):
        reg[m.group(5)] = dict(ico=m.group(1), name=m.group(2), desc=m.group(4))
    return reg

MODULES = [m for m in ['tools_diger', 'tools_saglik', 'tools_finans', 'tools_vergi', 'tools_egitim', 'tools_kamu', 'tools_takvim', 'tools_siralama', 'tools_pazaryeri', 'tools_para', 'tools_2027', 'tools_banka'] if os.path.exists(os.path.join(os.path.dirname(__file__), m + '.py'))]
tools = []
for m in MODULES:
    tools += importlib.import_module(m).TOOLS

reg = registry()
reg.update({k:v for k,v in {
  'yillik-izin-hesaplama': dict(ico='🏖️', name='Yıllık İzin Hesaplama', desc='Kıdeme göre yıllık izin hakkını hesapla.'),
  'asgari-ucret-hesaplama': dict(ico='💵', name='Asgari Ücret Hesaplama', desc='2026 asgari ücret net, brüt ve işveren maliyeti.'),
}.items() if k not in reg})
for t in tools:  # yeni araçlar registry'e
    reg.setdefault(t['slug'], dict(ico=t['ico'], name=t['name'], desc=t['desc'][:60]))
only = set(sys.argv[1:])
for t in tools:
    if only and t['slug'] not in only: continue
    html = render(t, reg)
    open(t['slug'] + '.html', 'w', encoding='utf-8').write(html)
    words = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S)).split())
    print(f"{t['slug']:45s} {words:5d} kelime  title={len(t['title'])} desc={len(t['desc'])}")
json.dump({t['slug']: dict(ico=t['ico'], name=t['name'], cat=t['cat']) for t in tools}, open('_gen/built.json', 'w'), ensure_ascii=False, indent=1)


# ── Ana sayfa: yaklaşan açıklamalar kutusu (ekonomi takvimi verisinden) ──
try:
    import tools_takvim as _tk, datetime as _dt
    _up = [e for e in _tk.EVENTS if _dt.date.fromisoformat(e[0]) >= _dt.date.today()][:4]
    _items = ''.join(
        f'<a href="{BASE}{e[4]}" style="display:flex;gap:12px;align-items:center;padding:12px 14px;border:1px solid #e5e7eb;border-radius:12px;background:#fff;text-decoration:none;color:#111827">'
        f'<span style="min-width:62px;text-align:center;font-weight:800;color:#1a56db;font-size:.82rem;line-height:1.2">{_tk.tr(e[0]).rsplit(" ",2)[0]}</span>'
        f'<span style="font-size:.86rem;font-weight:600">{e[2]}</span></a>' for e in _up)
    _html = ('<!-- TAKVIM-KUTU --><div style="max-width:1200px;margin:36px auto 0;padding:0 16px">'
             '<h2 class="section-title">📅 Yaklaşan Açıklamalar</h2>'
             f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px">{_items}</div>'
             f'<p style="margin-top:10px;font-size:.85rem"><a href="{BASE}/ekonomi-takvimi.html">Tüm ekonomi takvimini gör →</a></p></div><!-- /TAKVIM-KUTU -->')
    _s = open('index.html', encoding='utf-8').read()
    _s = re.sub(r'<!-- TAKVIM-KUTU -->.*?<!-- /TAKVIM-KUTU -->', lambda m: _html, _s, flags=re.S)
    open('index.html', 'w', encoding='utf-8').write(_s)
except Exception as _e:
    print('takvim kutusu hatası:', _e)


# ── Sayfaya özel paylaşım görselleri: assets/og/<slug>.jpg varsa og/twitter görselini değiştir ──
for _f in glob.glob('assets/og/*.jpg'):
    _slug = os.path.basename(_f)[:-4]
    if os.path.exists(_slug + '.html'):
        _s = open(_slug + '.html', encoding='utf-8').read()
        _u = f'{BASE}/assets/og/{_slug}.jpg'
        _s = re.sub(r'<meta property="og:image" content="[^"]*"', f'<meta property="og:image" content="{_u}"', _s)
        _s = re.sub(r'<meta name="twitter:image" content="[^"]*"', f'<meta name="twitter:image" content="{_u}"', _s)
        open(_slug + '.html', 'w', encoding='utf-8').write(_s)


# ── Bağlamsal iç bağlantı kutuları (links.py) ──
try:
    import links as _links
    print('iç bağlantı:', _links.run(), 'sayfa')
except Exception as _e:
    print('iç bağlantı hatası:', _e)


# ── Kategori (hub) sayfaları + /#kategori bağlantılarının kategori sayfalarına çevrilmesi ──
try:
    import kategoriler as _kat
    _r, _n = _kat.run()
    print('kategori sayfaları:', len(_r), '· bağlantısı düzeltilen sayfa:', _n)
except Exception as _e:
    print('kategori hatası:', _e)


# ── Kısa cevap kutuları (öne çıkan snippet hedefi) ──
try:
    import kisa_cevap as _kc
    print('kısa cevap:', _kc.run())
except Exception as _e:
    print('kısa cevap hatası:', _e)


# ── Veri sayfası: Türkiye'de Maaşlar 2026 ──
try:
    import veri_sayfasi as _vs
    print('veri sayfası:', _vs.run())
except Exception as _e:
    print('veri sayfası hatası:', _e)
