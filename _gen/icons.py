"""Emoji arayüz ikonlarını tek tip SVG (Lucide) ikonlarla değiştirir. build.py sonunda (chrome'dan önce/sonra fark etmez) çalışır; idempotent.
Kapsam: araç kartları, ilgili araç kartları, kategori kartları, başlık etiketleri, hesaplayıcı başlıkları ve h1/h2/h3 başındaki emojiler.
Makale metni içindeki emojilere dokunmaz.
"""
import os, re, glob
from icon_svgs import P

CAT = {'maas': 'wallet', 'kamu': 'landmark', 'vergi': 'receipt', 'finans': 'coins', 'isletme': 'store', 'gayrimenkul': 'house',
       'arac': 'car', 'saglik': 'heart-pulse', 'egitim': 'graduation-cap', 'diger': 'calculator'}
CATPAGE = {'maas-hesaplamalari': 'wallet', 'memur-hesaplamalari': 'landmark', 'vergi-hesaplamalari': 'receipt', 'finans-hesaplamalari': 'coins',
           'isletme-hesaplamalari': 'store', 'emlak-hesaplamalari': 'house', 'arac-hesaplamalari': 'car', 'saglik-hesaplamalari': 'heart-pulse',
           'egitim-hesaplamalari': 'graduation-cap', 'gunluk-hesaplamalar': 'calculator'}
TOOL = {
 'net-maas-hesaplama': 'wallet', 'kidem-tazminati-hesaplama': 'briefcase', 'ihbar-tazminati-hesaplama': 'file-text', 'fazla-mesai-hesaplama': 'clock', 'desi-hesaplama': 'ruler', 'altin-hesaplama': 'coins', 'taksi-ucreti-hesaplama': 'car', 'bedelli-askerlik-hesaplama': 'shield-check', 'emekli-ikramiyesi-hesaplama': 'hand-coins', 'konut-kredisi-hesaplama': 'house',
 'saatlik-ucret-hesaplama': 'timer', 'maas-siralamasi': 'chart-bar', 'issizlik-maasi-hesaplama': 'shield-check', 'maas-zam-hesaplama': 'trending-up',
 'prim-hesaplama': 'badge-percent', 'emeklilik-yasi-hesaplama': 'hourglass', 'asgari-ucret-hesaplama': 'banknote', 'asgari-ucret-2027-hesaplama': 'trending-up', 'emekli-maasi-hesaplama': 'hand-coins', 'obp-hesaplama': 'graduation-cap', 'lgs-puan-hesaplama': 'graduation-cap', 'kpss-puan-hesaplama': 'landmark', 'ales-puan-hesaplama': 'graduation-cap',
 'yillik-izin-hesaplama': 'sun', 'turkiye-maaslari-2026': 'chart-column', 'memur-maaslari': 'landmark', 'ogretmen-maasi': 'graduation-cap',
 'polis-maasi': 'shield-check', 'hemsire-maasi': 'heart-pulse', 'doktor-maasi': 'activity', 'muhendis-maasi': 'ruler', 'memur-emekli-zammi-hesaplama': 'trending-up',
 'kdv-hesaplama': 'receipt', 'kdv-haric-hesaplama': 'receipt', 'gelir-vergisi-hesaplama': 'file-text', 'otv-hesaplama': 'car', 'amortisman-hesaplama': 'chart-line',
 'tapu-harci-hesaplama': 'house', 'mtv-hesaplama': 'car', 'damga-vergisi-hesaplama': 'file-text', 'ekonomi-takvimi': 'calendar-days',
 'kredi-hesaplama': 'credit-card', 'bilesik-faiz': 'chart-line', 'mevduat-faizi-hesaplama': 'piggy-bank', 'enflasyon-hesaplama': 'trending-up',
 'kredi-erken-kapama-hesaplama': 'credit-card', 'borc-kapatma-hesaplama': 'hand-coins', 'kredi-karti-asgari-odeme-hesaplama': 'credit-card',
 'kripto-kar-zarar-hesaplama': 'bitcoin', 'doviz-cevirici': 'arrow-left-right', 'para-deger-kaybi-hesaplama': 'trending-down', 'roi-hesaplama': 'percent',
 'yatirim-geri-donus-suresi-hesaplama': 'hourglass', 'para-sayma-hesaplama': 'banknote', 'kar-payi-hesaplama': 'coins', 'banka-komisyon-hesaplama': 'landmark',
 'yuzde-hesaplama': 'percent', 'indirim-hesaplama': 'tag', 'iskonto-hesaplama': 'badge-percent', 'kar-zarar-hesaplama': 'chart-line', 'kar-marji-hesaplama': 'chart-pie',
 'pazaryeri-komisyon-hesaplama': 'shopping-cart', 'trendyol-komisyon-hesaplama': 'shopping-cart', 'hepsiburada-komisyon-hesaplama': 'shopping-cart',
 'shopier-komisyon-hesaplama': 'shopping-cart', 'komisyon-hesaplama': 'hand-coins', 'ciro-hesaplama': 'chart-column', 'net-kar-hesaplama': 'coins',
 'brut-kar-hesaplama': 'coins', 'basa-bas-noktasi-hesaplama': 'scale', 'stok-karliligi-hesaplama': 'store', 'kira-getirisi-hesaplama': 'building-2',
 'kira-artis-hesaplama': 'house', 'metrekare-fiyat-hesaplama': 'ruler', 'arac-kredisi-hesaplama': 'car', 'arac-deger-kaybi-hesaplama': 'trending-down',
 'yakit-maliyeti-hesaplama': 'fuel', 'yakit-tuketimi-hesaplama': 'fuel', 'arac-muayene-gecikme-hesaplama': 'calendar', 'vucut-kitle-indeksi': 'scale',
 'bazal-metabolizma-hesaplama': 'flame', 'gunluk-kalori-ihtiyaci-hesaplama': 'apple', 'kalori-yakma-hesaplama': 'flame', 'ideal-kilo-hesaplama': 'scale',
 'hedef-kilo-suresi-hesaplama': 'hourglass', 'vucut-yag-orani-hesaplama': 'activity', 'bel-kalca-orani-hesaplama': 'ruler', 'protein-ihtiyaci-hesaplama': 'dumbbell',
 'su-ihtiyaci-hesaplama': 'droplet', 'not-ortalamasi-hesaplama': 'book-open', 'tyt-net-hesaplama': 'graduation-cap', 'ayt-net-hesaplama': 'graduation-cap',
 'kpss-net-hesaplama': 'graduation-cap', 'takdir-tesekkur-hesaplama': 'book-open', 'ortalama-hesaplama': 'calculator', 'gun-hesaplama': 'calendar-days',
 'yas-hesaplama': 'calendar', 'is-gunu-hesaplama': 'calendar', 'dosya-boyutu-donusturucu': 'hard-drive', 'internet-hizi-donusturucu': 'wifi',
 'dosya-indirme-suresi-hesaplama': 'file-down', 'veri-kullanim-hesaplama': 'smartphone', 'elektrik-faturasi-hesaplama': 'zap',
 'dogalgaz-faturasi-hesaplama': 'flame', 'su-faturasi-hesaplama': 'droplet', 'boya-hesaplama': 'paintbrush',
}
TOOL.update(CATPAGE)


def svg(name, cls='hzi'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{P.get(name, P["calculator"])}</svg>')


# emoji (+ varyasyon seçici / ZWJ dizileri) ve ardından gelen boşluk
EMO = r'(?:[\U0001F000-\U0001FAFF☀-➿⬀-⯿←-⇿⌀-⏿](?:️|‍[\U0001F000-\U0001FAFF☀-➿])*)+'
CSS = ('<style id="hz-icons">.hzi{width:1em;height:1em;display:inline-block;vertical-align:-.14em;flex-shrink:0}'
       '.ri .hzi,.kico .hzi,.kat-ico .hzi,.tc-ico .hzi,.sd-ico .hzi,.calc-icon .hzi,.rc-icon .hzi,.pop-ico .hzi,.ql i .hzi,.ri-icon .hzi,.ql-icon .hzi{width:22px;height:22px;color:#1a56db;vertical-align:middle}'
       '.calc-icon .hzi{color:#fff}.hero-tag .hzi,.hero-badge .hzi{margin-right:4px}'
       '.res-actions button[onclick="paylas()"],button.hz-wa{color:#15803d!important;border-color:#86efac!important;background:#f0fdf4!important;display:inline-flex;align-items:center;justify-content:center}'
       '.res-actions button[onclick="paylas()"]:hover,button.hz-wa:hover{background:#dcfce7!important}.hzb{margin-right:5px}.copy-btn.hz-wa{margin-top:-.4rem!important}.btn-copy.hz-wa{margin-left:6px}'
       '.main-grid>*{min-width:0}.sidebar table,aside table{min-width:0!important;width:100%!important}.sidebar td:first-child,aside td:first-child{white-space:normal!important}</style>')


def slug_of(href):
    m = re.search(r'([a-z0-9-]+)\.html', href)
    return m.group(1) if m else ''


def process(p, s):
    slug = os.path.basename(p)[:-5]
    # 1) kart içi ikonlar: href'e göre
    def card(m):
        return m.group(1) + svg(TOOL.get(slug_of(m.group(2)), 'calculator')) + m.group(4)
    s = re.sub(r'(<a class="(?:rc|kcard|kat-kart|related-card)"[^>]*href="([^"]+)"[^>]*>\s*<span class="(?:ri|kico|kat-ico|rc-icon)">)(.*?)(</span>)',
               card, s, flags=re.S)
    s = re.sub(r'(<a href="([^"]+)" class="related-item">\s*<span class="ri-icon">)(.*?)(</span>)', card, s, flags=re.S)
    s = re.sub(r'(<a class="ql"[^>]*href="([^"]+)"[^>]*>\s*<i>)(.*?)(</i>)', card, s, flags=re.S)
    s = re.sub(r'(<div class="side-title">)\s*' + EMO + r'\s*', lambda m: m.group(1), s)
    s = re.sub(r'(<a class="pop-item"[^>]*href="([^"]+)"[^>]*>.*?<div class="pop-ico">)(.*?)(</div>)', card, s, flags=re.S)
    # 2) başlık etiketi ve hesaplayıcı başlığı
    s = re.sub(r'(<span class="hero-tag">)\s*' + EMO + r'\s*', lambda m: m.group(1) + svg(TOOL.get(slug, 'calculator')), s)
    s = re.sub(r'(<(?:span|div) class="hero-badge">)\s*' + EMO + r'\s*', lambda m: m.group(1) + svg(TOOL.get(slug, 'calculator')), s)
    s = re.sub(r'(<div class="card-title">)\s*' + EMO + r'\s*', lambda m: m.group(1), s)
    s = re.sub(r'(<div class="calc-icon"[^>]*>)\s*' + EMO + r'\s*(</div>)', lambda m: m.group(1) + svg(TOOL.get(slug, 'calculator')) + m.group(2), s)
    # 3) h1/h2/h3 ve bölüm başlıklarının başındaki emojiler
    s = re.sub(r'(<h[123]\b[^>]*>(?:<span class="hico">)?)\s*' + EMO + r'\s*(?:</span>)?\s*', lambda m: m.group(1).replace('<span class="hico">', ''), s)
    # 3b) kopyala / paylaş butonlarındaki emoji
    BI = {'📋': 'copy', '💬': 'message-circle'}
    s = re.sub(r'(<button[^>]*onclick="(?:copy\w*|kopyala|paylas)\([^"]*\)"[^>]*>)\s*(📋|💬)\s*',
               lambda m: m.group(1) + svg(BI[m.group(2)], 'hzi hzb'), s)
    # 3c) bağlantı içindeki tek başına emoji ikonları → SVG (hedef sayfaya göre)
    s = re.sub(r'(<a\b[^>]*href="([^"]+)"[^>]*>\s*<(span|div|i)\b[^>]*>)\s*' + EMO + r'\s*(</\3>)', card, s)
    # 3d) metin başındaki emojiler (etiket, buton, rozet, liste, tablo...) — svg/script/style hariç
    parts = re.split(r'(<svg\b.*?</svg>|<script\b.*?</script>|<style\b.*?</style>)', s, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(<(?:a|span|strong|b|p|div|td|th|li|button|option|label|h[456]|small|em|summary|figcaption)\b[^>]*>)\s*'
                          + EMO + r'\s*(?=[^\s<]|<(?!/))', r'\1', parts[i])
    s = ''.join(parts)
    # 4) eski hesaplayıcılara WhatsApp paylaş
    s = re.sub(r'<script src="/assets/paylas.js" defer></script>\n?', '', s)
    if 'function paylas()' not in s and re.search(r'onclick="copy(?:Result|Res|KazaResult|All)\(', s):
        s = s.replace('</body>', '<script src="/assets/paylas.js" defer></script>\n</body>', 1)
    # 5) css
    s = re.sub(r'<style id="hz-icons">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    return s


INDEX_JS = None


def index_js(s):
    """Ana sayfa araç kartları JS ile çiziliyor: emoji yerine SVG haritası."""
    ix = {u: c for u, c in re.findall(r"url:'/([^']*)\.html',cat:'([^']*)'", s)}
    used = sorted(set(TOOL.get(u) or CAT.get(c, 'calculator') for u, c in ix.items()))
    m = 'var HZI=' + '{' + ','.join(f'"{n}":\'{P[n]}\'' for n in used) + '};var HZT={' + ','.join(f'"{u}":"{TOOL.get(u) or CAT.get(c, "calculator")}"' for u, c in ix.items()) + '};'
    m += ('function hzIco(t){var k=(t.url||"").replace(/^\\//,"").replace(/\\.html.*$/,"");var n=HZT[k]||"calculator";'
          'return \'<svg class="hzi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">\'+(HZI[n]||HZI.calculator)+\'</svg>\';}')
    s = re.sub(r'<script id="hz-ico-js">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('</head>', f'<script id="hz-ico-js">{m}</script>\n</head>', 1)
    s = s.replace('${t.ico}', '${hzIco(t)}')
    return s


def blog_clean(s):
    """Blog listesi: etiket/başlık/menü metinlerinin başındaki emojileri kaldırır (SVG kapak görsellerine dokunmaz)."""
    parts = re.split(r'(<svg\b.*?</svg>|<script\b.*?</script>|<style\b.*?</style>)', s, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'>(\s*)' + EMO + r'\s*', r'>\1', parts[i])
    return ''.join(parts)


def blog_say(s):
    """Blog listesi: kategori sayaçlarını ve toplam makale sayısını kartlardan yeniden hesaplar."""
    cats = re.findall(r'<a class="post-card"[^>]*data-cat="([^"]+)"', s)
    s = re.sub(r'Tüm Makaleler \(\d+\)', f'Tüm Makaleler ({len(cats)})', s)
    s = re.sub(r"Tümü \(\d+\)", f'Tümü ({len(cats)})', s)
    s = re.sub(r"(filterPosts\('([a-z]+)',null\);return false;\">[^<]*<span class=\"kc\">)\d+(</span>)",
               lambda m: m.group(1) + str(cats.count(m.group(2))) + m.group(3), s)
    return s


def run():
    n = 0
    for p in sorted(glob.glob('*.html') + glob.glob('blog/*.html')):
        if os.path.basename(p).startswith(('yandex_', 'google', 'blog-', 'kov-')):
            continue
        s = open(p, encoding='utf-8').read(); o = s
        s = process(p, s)
        if p == 'index.html':
            s = index_js(s)
        if p == 'blog.html':
            s = blog_say(s)
        if p == 'blog.html':
            s = blog_clean(s)
        if s != o:
            open(p, 'w', encoding='utf-8').write(s); n += 1
    return n


if __name__ == '__main__':
    import sys
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, '_gen')
    print(run())
