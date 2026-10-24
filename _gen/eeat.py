"""Eski (elle yazılmış) araç sayfalarına güven sinyalleri ekler: görünür 'Son güncelleme · Hazırlayan · Yöntem' satırı,
WebApplication şemasına dateModified + author. Şablon sayfalarda bu bilgiler zaten var. İdempotent; build.py'de chrome'dan önce çalışır.
TARIH: içerik doğruluk kontrolünden geçen sayfaların tarihi; diğerleri 21 Ekim 2026 (Faz 1 denetimi).
"""
import os, re, json, glob

VARSAYILAN = '2026-10-21'
TARIH = {
    'net-maas-hesaplama': '2026-10-24', 'mevduat-faizi-hesaplama': '2026-10-24', 'kredi-karti-asgari-odeme-hesaplama': '2026-10-24',
    'kidem-tazminati-hesaplama': '2026-10-24', 'gelir-vergisi-hesaplama': '2026-10-24', 'bilesik-faiz': '2026-10-24',
    'komisyon-hesaplama': '2026-10-24', 'ihbar-tazminati-hesaplama': '2026-10-24', 'kdv-hesaplama': '2026-10-24', 'kredi-hesaplama': '2026-10-24',
}
AY = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
SKIP = {'index', 'blog', '404', 'iletisim', 'hakkimizda', 'gizlilik-politikasi', 'kullanim-sartlari', 'yontem-ve-kaynaklar', 'turkiye-maaslari-2026'}
AUTHOR = {'@type': 'Person', 'name': 'Duran Gönülalan', 'url': 'https://hesaplarsin.com/hakkimizda.html'}
CSS = ('<style id="hz-eeat">.hz-meta{max-width:900px;margin:0 auto 18px;padding:10px 14px;border:1px solid #e5e7eb;border-radius:10px;'
       'background:#f8fafc;font-size:.82rem;color:#475569;line-height:1.6}.hz-meta a{color:#1a56db}</style>')


def tr_tarih(d):
    y, m, g = d.split('-')
    return f'{int(g)} {AY[int(m) - 1]} {y}'


def isle(slug, s):
    d = TARIH.get(slug, VARSAYILAN)
    # 1) görünür satır
    s = re.sub(r'\n?<div class="hz-meta"[^>]*>.*?</div>\n?', '', s, flags=re.S)
    satir = (f'<div class="hz-meta" data-hz="eeat">Son güncelleme: <time datetime="{d}">{tr_tarih(d)}</time> · '
             f'Hazırlayan: <a href="https://hesaplarsin.com/hakkimizda.html">Duran Gönülalan</a>, Hesaplarsın kurucusu · '
             f'Rakamlar resmî kaynaklardan alınır: <a href="https://hesaplarsin.com/yontem-ve-kaynaklar.html">Yöntem ve kaynaklar</a></div>\n')
    m = re.search(r'<div class="article">|<div class="seo-wrap">|<article\b[^>]*>', s)
    if not m:
        return s, False
    s = s[:m.end()] + '\n' + satir + s[m.end():]
    # 2) şema
    def sema(mm):
        try:
            o = json.loads(mm.group(2))
        except Exception:
            return mm.group(0)
        if isinstance(o, dict) and o.get('@type') == 'WebApplication':
            o['dateModified'] = d
            o.setdefault('author', AUTHOR)
            return mm.group(1) + json.dumps(o, ensure_ascii=False) + mm.group(3)
        return mm.group(0)
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', sema, s, flags=re.S)
    s = re.sub(r'<style id="hz-eeat">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    return s, True


def run():
    built = set(json.load(open('_gen/built.json')))
    n = 0
    for p in sorted(glob.glob('*.html')):
        slug = p[:-5]
        if slug in built or slug in SKIP or slug.endswith(('-hesaplamalari', '-hesaplamalar')) or slug.startswith(('yandex', 'google', 'blog-', 'kov-')):
            continue
        s = open(p, encoding='utf-8').read()
        if 'location.replace(' in s and len(s) < 3000:
            continue
        y, ok = isle(slug, s)
        if ok and y != s:
            open(p, 'w', encoding='utf-8').write(y); n += 1
    return n


if __name__ == '__main__':
    import sys
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(run())
