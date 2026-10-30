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

# ── İnce sayfalara ek içerik (ek_icerik.py) ──
try:
    from ek_icerik import EK as _EK
    for t in tools:
        e = _EK.get(t['slug'])
        if e:
            t['article'] = t['article'] + e.get('article', '')
            t['faq'] = list(t['faq']) + list(e.get('faq', []))
except Exception as _e:
    print('ek içerik hatası:', _e)

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
# Ana sayfadaki 'Gündemdeki Hesaplamalar' bağlantıları (sezona göre güncelle; arama verisine göre seçilir)
GUNDEM = [('blog/kasim-2026-kira-artis-orani.html', 'Kasım 2026 kira artış oranı'), ('kira-artis-hesaplama.html', 'Kira artış hesaplama'),
          ('emekli-maasi-hesaplama.html', 'Emekli maaşı 2026'), ('memur-emekli-zammi-hesaplama.html', 'Ocak 2027 memur ve emekli zammı'),
          ('asgari-ucret-2027-hesaplama.html', 'Asgari ücret 2027'), ('kpss-puan-hesaplama.html', 'KPSS puan hesaplama'), ('ales-puan-hesaplama.html', 'ALES puan hesaplama'), ('blog/trafik-cezalari-2027.html', '2027 trafik cezaları'), ('blog/yeniden-degerleme-orani-2026.html', '2027 MTV ve harçlar'), ('kredi-karti-asgari-odeme-hesaplama.html', 'Kredi kartı asgari ödeme'),
          ('takdir-tesekkur-hesaplama.html', 'Takdir teşekkür hesaplama'), ('yas-hesaplama.html', 'Yaş ve okula başlama yaşı')]
# Ana sayfada öne çıkan sayfalar (Search Console'da 5–10. sırada olup ilk 3'e taşınmak istenenler; ayda bir gözden geçir)
ONE_CIKAN = [('kpss-puan-hesaplama.html', 'KPSS puan hesaplama', 'Önlisans sonuçları açıklandı: netinden P93 puanı'),
             ('altin-hesaplama.html', 'Altın hesaplama', 'Gram, çeyrek, tam altın kaç TL? Canlı fiyat'),
             ('para-sayma-hesaplama.html', 'Kaç tane 200 TL ne kadar eder?', 'Banknot adedinden toplam tutar ve tablo'),
             ('blog/kasim-2026-kira-artis-orani.html', 'Kasım 2026 kira artış oranı', 'Tahmin ve kira zammı tablosu'),
             ('blog/kira-artisi-2027.html', 'Kira artışı 2027 tahmini', '2027 TÜFE beklentisi ve kira zammı'),
             ('yatirim-geri-donus-suresi-hesaplama.html', 'Yatırım geri dönüş süresi', 'Dükkân, ev veya makine kaç yılda öder?'),
             ('komisyon-hesaplama.html', 'Komisyon hesaplama', 'Satış komisyonu ve net tutar'),
             ('metrekare-fiyat-hesaplama.html', 'Metrekare fiyatı hesaplama', 'Evin m² fiyatı ve ilan karşılaştırma'),
             ('ortalama-hesaplama.html', 'Ortalama hesaplama', 'Ortalama, medyan ve Google yorum puanı'),
             ('indirim-hesaplama.html', 'İndirim hesaplama', 'Yüzde kaç indirim, indirimli fiyat'),
             ('saatlik-ucret-hesaplama.html', 'Saatlik ücret hesaplama', 'Maaşım saatte kaç TL?')]
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
             f'<p style="margin-top:10px;font-size:.85rem"><a href="{BASE}/ekonomi-takvimi.html">Tüm ekonomi takvimini gör →</a></p>'
             '<h2 class="section-title" style="margin-top:26px">Gündemdeki Hesaplamalar</h2>'
             '<div style="display:flex;flex-wrap:wrap;gap:8px">' + ''.join(
                 f'<a href="{BASE}/{u}" style="padding:8px 14px;border:1px solid #c7dafc;border-radius:999px;background:#f0f6ff;color:#1a56db;font-size:.85rem;font-weight:600;text-decoration:none">{t}</a>'
                 for u, t in GUNDEM) + '</div>'
             '<h2 class="section-title" style="margin-top:26px">Öne Çıkan Hesaplamalar</h2>'
             '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px">' + ''.join(
                 f'<a href="{BASE}/{u}" style="display:block;padding:12px 14px;border:1px solid #e5e7eb;border-radius:12px;background:#fff;text-decoration:none;color:#111827">'
                 f'<span style="display:block;font-weight:700;font-size:.9rem;color:#1a56db">{t}</span><span style="display:block;font-size:.8rem;color:#6b7280;margin-top:3px">{d}</span></a>'
                 for u, t, d in ONE_CIKAN) + '</div></div><!-- /TAKVIM-KUTU -->')
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


# ── Eski araç sayfalarına güncelleme tarihi + yazar (E-E-A-T) ──
try:
    import eeat as _ee
    print('eeat:', _ee.run())
except Exception as _e:
    print('eeat hatası:', _e)


# ── Emoji arayüz ikonları → tek tip SVG (Lucide) ──
try:
    import icons as _ic
    print('ikonlar:', _ic.run())
except Exception as _e:
    print('ikon hatası:', _e)

# ── Site geneli tek menü + tek alt bilgi (EN SONDA kalmalı) ──
try:
    import chrome as _ch
    print('menü/footer:', _ch.run())
except Exception as _e:
    print('menü/footer hatası:', _e)
