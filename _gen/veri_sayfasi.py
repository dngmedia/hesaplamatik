"""Veri sayfası: 'Türkiye'de Maaşlar 2026' — basın/blog kaynak göstermesi (link) hedefli, Dataset şemalı.
Veriler sitedeki diğer modüllerden okunur (tutarlılık için): tools_siralama (dağılım), tools_kamu (memur maaşları).
Güncelleme: Ocak 2027'de asgari ücret ve memur maaşları değişince otomatik yansır; tarih alanı GUNCEL elle güncellenir.
"""
import os, re, json, html
import tools_siralama as S
import tools_kamu as K
from kategoriler import shell

BASE = 'https://hesaplarsin.com'
SLUG = 'turkiye-maaslari-2026'
GUNCEL = ('2026-10-23', '23 Ekim 2026')
E = lambda t: html.escape(t, quote=True)


def tr(x, d=0):
    s = f"{x:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


NET = S.NET
BRUT = 33030.00


def alt_pay(x):
    c = S.CDF
    for i in range(1, len(c)):
        if x <= c[i][0]:
            a, b = c[i - 1], c[i]
            return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
    return 100 - 12.7 * (x / 2) ** -2


def ust_esik(p):
    return 2 * (12.7 / p) ** 0.5


MED = NET * 1.0556
UST10 = NET * ust_esik(10)
UST1 = NET * ust_esik(1)

# dağılım tablosu + çubuklar
DAG = [(0.5, 'Net asgari ücretin yarısı'), (1.0, 'Net asgari ücret'), (1.1, 'Asgari ücretin %10 fazlası'), (1.2, 'Asgari ücretin %20 fazlası'), (2.0, 'Net asgari ücretin 2 katı')]
dag_rows = ''.join(
    f'<tr><td>{ad}</td><td>{tr(NET * x)} ₺</td><td><div style="display:flex;align-items:center;gap:8px"><div style="height:12px;width:{alt_pay(x):.1f}%;max-width:160px;min-width:4px;background:#1a56db;border-radius:6px"></div><strong>%{tr(alt_pay(x), 1)}</strong></div></td></tr>'
    for x, ad in DAG)
DAG_T = ('<div class="table-wrap"><table><thead><tr><th>Eşik</th><th>Aylık net (2026)</th><th>Bu tutar ve altında kazananlar</th></tr></thead>'
         f'<tbody>{dag_rows}</tbody></table></div>')

mem = sorted(K.U.values(), key=lambda t: -t[1])
MEM_T = ('<div class="table-wrap"><table><thead><tr><th>Unvan (derece/kademe)</th><th>Net maaş, Temmuz–Aralık 2026</th><th>Net asgari ücretin katı</th></tr></thead><tbody>'
         + ''.join(f'<tr><td>{E(a)}</td><td>{tr(m)} ₺</td><td>{tr(m / NET, 2)}×</td></tr>' for a, m in mem) + '</tbody></table></div>')

TAR = [('Ocak 2023', 10008.00, 8506.80, '%54,7'), ('Temmuz 2023', 13414.50, 11402.32, '%34,0 (ara zam)'), ('2024', 20002.50, 17002.12, '%49,1'),
       ('2025', 26005.50, 22104.67, '%30,0'), ('2026', 33030.00, 28075.50, '%27,0')]
TAR_T = ('<div class="table-wrap"><table><thead><tr><th>Dönem</th><th>Brüt</th><th>Net</th><th>Artış</th></tr></thead><tbody>'
         + ''.join(f'<tr><td>{d}</td><td>{tr(b, 2)} ₺</td><td>{tr(n, 2)} ₺</td><td>{a}</td></tr>' for d, b, n, a in TAR) + '</tbody></table></div>')

YASAL_T = ('<div class="table-wrap"><table><thead><tr><th>Kalem</th><th>2026 tutarı</th></tr></thead><tbody>'
           + ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in [
               ('Brüt asgari ücret', '33.030,00 ₺'), ('Net asgari ücret', '28.075,50 ₺'), ('Asgari ücretin işverene maliyeti (2 puan teşvikle)', '40.214,03 ₺'),
               ('Kıdem tazminatı tavanı (Temmuz–Aralık 2026)', '73.729,87 ₺'), ('İşsizlik ödeneği üst sınırı (brüt asgari ücretin %80’i)', '26.424,00 ₺'),
               ('Saatlik brüt asgari ücret (225 saat)', '146,80 ₺'), ('Memur maaş katsayısı (Temmuz–Aralık 2026)', '1,575512')]) + '</tbody></table></div>')

OZET = [('Net asgari ücret', f'{tr(NET, 2)} ₺'), ('Tahmini medyan net maaş', f'≈ {tr(MED)} ₺'),
        ('Asgari ücret veya altında kazananlar', '%46,7'), ('En üst %10’a giriş (tahmini)', f'≈ {tr(UST10)} ₺'),
        ('Üniversite mezunu memur (9/1)', f'{tr(K.U["memur"][1])} ₺'), ('Uzman doktor (1/4)', f'{tr(K.U["uzman-doktor"][1])} ₺')]
OZET_H = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin:14px 0">' + ''.join(
    f'<div style="border:1.5px solid var(--border);border-radius:12px;padding:12px 14px;background:var(--card)"><div style="font-size:.78rem;color:var(--muted)">{a}</div><div style="font-size:1.25rem;font-weight:800;margin-top:2px">{b}</div></div>'
    for a, b in OZET) + '</div>'

ATIF = (f'<div style="border:2px dashed #93c5fd;border-radius:14px;padding:14px 16px;background:#f8fafc;font-size:.9rem;line-height:1.6">'
        f'<strong>📣 Bu verileri kullanabilirsiniz.</strong> Haber, rapor veya blog yazınızda tablolardan alıntı yapabilirsiniz; lütfen kaynak olarak '
        f'“<em>Hesaplarsın – Türkiye’de Maaşlar 2026</em>” ifadesini ve <a href="{BASE}/{SLUG}.html">{BASE.replace("https://", "")}/{SLUG}.html</a> bağlantısını belirtin. '
        f'Güncel olmayan bir rakam görürseniz <a href="mailto:info@hesaplarsin.com">info@hesaplarsin.com</a> adresine yazın.</div>')

TITLE = 'Türkiye’de Maaşlar 2026: Asgari Ücret, Medyan Maaş ve Memur Maaşları'
DESC = f'2026’da Türkiye’de maaş dağılımı: çalışanların %46,7’si asgari ücret veya altında, tahmini medyan net maaş ≈ {tr(MED)} ₺. Memur maaşları ve yasal tutarlar tablolarla.'
FAQ = [('Türkiye’de ortalama maaş ne kadar?', f'Özel sektör ücretli çalışanların yarısı net asgari ücretin yaklaşık 1,06 katının altında kazanıyor; bu da 2026 için tahmini medyan net maaşın yaklaşık {tr(MED)} ₺ olduğu anlamına gelir. Aritmetik ortalama, yüksek gelirliler nedeniyle medyandan yüksektir.'),
       ('Kaç kişi asgari ücret alıyor?', 'TÜİK Hanehalkı İşgücü Anketi mikro verisinden yapılan DİSK-AR derlemesine göre özel sektör ücretli çalışanların %46,7’si asgari ücret veya altında kazanıyor.'),
       ('En üst %10’a girmek için ne kadar kazanmak gerekir?', f'Tahmini olarak aylık net yaklaşık {tr(UST10)} ₺. Asgari ücretin 2 katının üzerindeki dağılım resmî kırılım olmadığından istatistiksel bir varsayımla (Pareto dağılımı) tahmin edilmiştir.'),
       ('Bu verileri haberimde kullanabilir miyim?', 'Evet. Kaynak olarak “Hesaplarsın – Türkiye’de Maaşlar 2026” ifadesini ve sayfa bağlantısını belirtmeniz yeterlidir.')]


def run():
    head, foot = shell()
    url = f'{BASE}/{SLUG}.html'
    lds = [
        {"@context": "https://schema.org", "@type": "Dataset", "name": "Türkiye’de Maaşlar 2026", "description": DESC, "url": url,
         "creator": {"@type": "Organization", "name": "Hesaplarsın", "url": BASE + "/"}, "license": "https://creativecommons.org/licenses/by/4.0/",
         "isAccessibleForFree": True, "temporalCoverage": "2026", "spatialCoverage": {"@type": "Place", "name": "Türkiye"}, "dateModified": GUNCEL[0],
         "keywords": ["asgari ücret", "medyan maaş", "memur maaşları", "maaş dağılımı", "Türkiye"]},
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "dateModified": GUNCEL[0], "datePublished": GUNCEL[0], "inLanguage": "tr",
         "author": {"@type": "Person", "name": "Duran Gönülalan", "jobTitle": "Hesaplarsın Kurucusu", "url": BASE + "/hakkimizda.html#kurucu"},
         "publisher": {"@type": "Organization", "name": "Hesaplarsın", "url": BASE + "/", "logo": {"@type": "ImageObject", "url": BASE + "/assets/icon-512.png"}},
         "image": [f'{BASE}/assets/og/{SLUG}.jpg'], "mainEntityOfPage": url},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Maaş ve SGK Hesaplamaları", "item": BASE + "/maas-hesaplamalari.html"},
            {"@type": "ListItem", "position": 3, "name": "Türkiye’de Maaşlar 2026", "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{E(TITLE)}</title>', h, count=1, flags=re.S)
    og = f'{BASE}/assets/og/{SLUG}.jpg' if os.path.exists(f'assets/og/{SLUG}.jpg') else f'{BASE}/assets/og-image.png'
    for pat, val in [(r'(<meta name="description" content=")[^"]*', DESC), (r'(<meta property="og:description" content=")[^"]*', DESC),
                     (r'(<meta name="twitter:description" content=")[^"]*', DESC), (r'(<meta property="og:title" content=")[^"]*', TITLE),
                     (r'(<meta name="twitter:title" content=")[^"]*', TITLE), (r'(<link rel="canonical" href=")[^"]*', url), (r'(<meta property="og:url" content=")[^"]*', url),
                     (r'(<meta property="og:image" content=")[^"]*', og), (r'(<meta name="twitter:image" content=")[^"]*', og)]:
        h = re.sub(pat, lambda m: m.group(1) + E(val), h, count=1)
    h = re.sub(r'<meta property="og:type" content="[^"]*"', '<meta property="og:type" content="article"', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    h = h.replace('</head>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in lds) + '</head>', 1)
    h = re.sub(r'<body data-tool="[^"]*">', f'<body data-tool="{SLUG}">', h)
    faq_html = ''.join(f'<div class="faq-item"><button class="faq-q" type="button" aria-expanded="false">{E(q)}</button><div class="faq-a"><p>{a}</p></div></div>' for q, a in FAQ)
    body = f'''<nav class="breadcrumb" aria-label="Breadcrumb">
  <a href="{BASE}/">Ana Sayfa</a><span aria-hidden="true">›</span><a href="{BASE}/maas-hesaplamalari.html">Maaş ve SGK Hesaplamaları</a><span aria-hidden="true">›</span><span aria-current="page">Türkiye’de Maaşlar 2026</span>
</nav>
<header class="hero"><div class="hero-inner">
  <span class="hero-tag">📊 Veri</span>
  <h1>Türkiye’de Maaşlar 2026</h1>
  <p>Asgari ücretten memur maaşlarına, Türkiye’de 2026’da kim ne kadar kazanıyor? Maaş dağılımı, tahmini medyan maaş, unvanlara göre memur maaşları ve yasal tutarlar tek sayfada.</p>
  <div class="hero-badges"><span class="hbadge">Güncelleme: {GUNCEL[1]}</span><span class="hbadge">Kaynak gösterilerek kullanılabilir</span></div>
</div></header>
<div class="article"><div class="article-inner" style="max-width:1000px">
  <h2>Özet: 2026’da maaşlar</h2>
  {OZET_H}
  {ATIF}
  <h2>Maaş dağılımı: Kaç kişi ne kadar kazanıyor?</h2>
  <p>Özel sektörde ücretli çalışanların neredeyse yarısı asgari ücret veya altında kazanıyor. Asgari ücretin 2 katını (aylık net {tr(NET * 2)} ₺) kazananlar çalışanların en üst %12,7’lik kesimindedir.</p>
  {DAG_T}
  <p style="font-size:.85rem;color:var(--muted)">Kaynak: TÜİK Hanehalkı İşgücü Anketi 2024 mikro verisinden DİSK-AR’ın derlediği, özel sektör ücretli çalışanların asgari ücrete göre kümülatif dağılımı; 2026 net asgari ücretine oranlanmıştır. Ara değerler doğrusal olarak hesaplanmıştır.</p>
  <h3>Medyan ve üst gelir dilimleri (tahmini)</h3>
  <ul><li><strong>Medyan net maaş:</strong> ≈ {tr(MED)} ₺ — çalışanların yarısı bunun altında, yarısı üstünde kazanır.</li>
  <li><strong>En üst %10’a giriş:</strong> ≈ {tr(UST10)} ₺ net.</li>
  <li><strong>En üst %1’e giriş:</strong> ≈ {tr(UST1)} ₺ net.</li></ul>
  <p style="font-size:.85rem;color:var(--muted)">Asgari ücretin 2 katının üzerindeki dilimler için resmî kırılım bulunmadığından değerler Pareto dağılımı varsayımıyla (α=2) tahmin edilmiştir. Kendi maaşınızın sırası için <a href="{BASE}/maas-siralamasi.html">Maaşım Türkiye’de kaçıncı sırada?</a> aracını kullanın.</p>
  <h2>Memur maaşları: Unvanlara göre (Temmuz–Aralık 2026)</h2>
  {MEM_T}
  <p style="font-size:.85rem;color:var(--muted)">Aile yardımı, ek ders, nöbet, döner sermaye ve bölgesel ödemeler hariç net tutarlar. Ocak 2027 tahminleri için <a href="{BASE}/memur-maaslari.html">memur maaşları</a> sayfasına bakın.</p>
  <h2>Asgari ücretin seyri (2023–2026)</h2>
  {TAR_T}
  <p>2027 asgari ücreti Aralık 2026 sonunda açıklanacak. Farklı zam senaryolarında yeni tutarı <a href="{BASE}/asgari-ucret-2027-hesaplama.html">asgari ücret 2027 hesaplama</a> aracıyla görebilirsiniz.</p>
  <h2>2026’da maaşa bağlı yasal tutarlar</h2>
  {YASAL_T}
  <h2>Yöntem ve kaynaklar</h2>
  <p>Maaş dağılımı TÜİK Hanehalkı İşgücü Anketi’ne (DİSK-AR derlemesi), memur maaşları Hazine ve Maliye Bakanlığı’nın katsayı genelgesi ve basında yayımlanan maaş tablolarına, asgari ücret ve yasal tutarlar Resmî Gazete’ye dayanır. Tüm parametreler ve güncelleme takvimi <a href="{BASE}/yontem-ve-kaynaklar.html">Yöntem ve Kaynaklar</a> sayfasında listelenmiştir. Hazırlayan: <a href="{BASE}/hakkimizda.html#kurucu">Duran Gönülalan</a>, Hesaplarsın kurucusu.</p>
  <h2>Sık Sorulan Sorular</h2>
  {faq_html}
</div></div>
'''
    script = '''<script>(function(){var hb=document.getElementById('hamBtn'),nl=document.getElementById('navLinks');if(hb&&nl){hb.addEventListener('click',function(){var o=nl.classList.toggle('open');hb.setAttribute('aria-expanded',o);});}
document.querySelectorAll('.faq-q').forEach(function(b){b.addEventListener('click',function(){var a=b.nextElementSibling;var o=a.classList.toggle('open');b.classList.toggle('open',o);b.setAttribute('aria-expanded',o);});});})();</script>'''
    open(f'{SLUG}.html', 'w', encoding='utf-8').write(h + body + foot + '\n' + script + '\n</body>\n</html>\n')
    return SLUG


if __name__ == '__main__':
    import sys
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, '_gen')
    print(run())
