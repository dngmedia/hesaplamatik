"""Bağlamsal iç bağlantı kutusu: her sayfaya, konusuyla ilgili rehber/araç linkleri ekler.
Search Console + iç link taramasına göre zayıf bağlanan sayfaları güçlendirmek için.
Idempotent: <!-- ICLINK --> ... <!-- /ICLINK --> bloğunu her çalıştırmada yeniden yazar.
Kullanım: build.py sonunda otomatik çalışır.
"""
import os, re

B = 'https://hesaplarsin.com/'
N = {  # hedef -> görünen ad
 'para-sayma-hesaplama': 'Para sayma (kaç tane 200 TL ne eder?)', 'boya-hesaplama': 'Boya hesaplama (kaç litre boya lazım?)',
 'maas-siralamasi': 'Maaşım Türkiye’de kaçıncı sırada?', 'muhendis-maasi': 'Mühendis maaşı 2026', 'doktor-maasi': 'Doktor maaşı 2026',
 'hemsire-maasi': 'Hemşire maaşı 2026', 'ogretmen-maasi': 'Öğretmen maaşı 2026', 'polis-maasi': 'Polis maaşı 2026', 'memur-maaslari': 'Memur maaşları 2026',
 'issizlik-maasi-hesaplama': 'İşsizlik maaşı hesaplama', 'kdv-haric-hesaplama': 'KDV hariç fiyat hesaplama', 'prim-hesaplama': 'Satış primi hesaplama',
 'veri-kullanim-hesaplama': 'Veri (GB) kullanım hesaplama', 'para-deger-kaybi-hesaplama': 'Paranın değer kaybı hesaplama', 'yakit-tuketimi-hesaplama': 'Yakıt tüketimi (100 km’de kaç litre)',
 'arac-muayene-gecikme-hesaplama': 'Araç muayene gecikme cezası', 'dogalgaz-faturasi-hesaplama': 'Doğalgaz faturası hesaplama', 'su-faturasi-hesaplama': 'Su faturası hesaplama',
 'elektrik-faturasi-hesaplama': 'Elektrik faturası hesaplama', 'kredi-erken-kapama-hesaplama': 'Kredi erken kapama hesaplama', 'kredi-karti-asgari-odeme-hesaplama': 'Kredi kartı asgari ödeme',
 'kripto-kar-zarar-hesaplama': 'Kripto kâr/zarar hesaplama', 'otv-hesaplama': 'ÖTV hesaplama', 'stok-karliligi-hesaplama': 'Stok kârlılığı hesaplama',
 'borc-kapatma-hesaplama': 'Borç kapatma hesaplama', 'damga-vergisi-hesaplama': 'Damga vergisi hesaplama', 'indirim-hesaplama': 'İndirim hesaplama',
 'pazaryeri-komisyon-hesaplama': 'Pazaryeri komisyon hesaplama (Trendyol, Hepsiburada)', 'emeklilik-yasi-hesaplama': 'Emeklilik hesaplama – ne zaman emekli olurum?',
 'ekonomi-takvimi': 'Ekonomi takvimi (enflasyon, faiz kararı tarihleri)', 'net-maas-hesaplama': 'Net maaş hesaplama', 'kidem-tazminati-hesaplama': 'Kıdem tazminatı hesaplama',
 'ihbar-tazminati-hesaplama': 'İhbar tazminatı hesaplama', 'kira-artis-hesaplama': 'Kira artış hesaplama', 'tapu-harci-hesaplama': 'Tapu harcı hesaplama',
 'metrekare-fiyat-hesaplama': 'Metrekare fiyatı hesaplama', 'enflasyon-hesaplama': 'Enflasyon hesaplama', 'yuzde-hesaplama': 'Yüzde hesaplama', 'kdv-hesaplama': 'KDV hesaplama',
 'gelir-vergisi-hesaplama': 'Gelir vergisi hesaplama', 'fazla-mesai-hesaplama': 'Fazla mesai hesaplama', 'saatlik-ucret-hesaplama': 'Saatlik ücret hesaplama',
 'asgari-ucret-hesaplama': 'Asgari ücret hesaplama', 'internet-hizi-donusturucu': 'İnternet hızı dönüştürücü', 'yakit-maliyeti-hesaplama': 'Yakıt maliyeti hesaplama',
 'mtv-hesaplama': 'MTV hesaplama',
 'blog/dask-sigortasi-hesaplama': 'Rehber: DASK sigortası nasıl hesaplanır?', 'blog/nafaka-hesaplama': 'Rehber: Nafaka nasıl hesaplanır?',
 'blog/brutten-nete-maas-tablosu-2026': 'Brütten nete maaş tablosu 2026', 'blog/elektrik-faturasi-neden-yuksek': 'Rehber: Elektrik faturası neden yüksek geliyor?',
 'blog/ihbar-tazminati-hesaplama': 'Rehber: İhbar tazminatı ve süreleri', 'blog/kasim-2026-kira-artis-orani': 'Kasım 2026 kira artış oranı',
 'blog/tapu-harci-hesaplama': 'Rehber: Tapu harcı kim öder, nasıl hesaplanır?', 'blog/yeniden-degerleme-orani-2026': 'Yeniden değerleme oranı 2026',
 'blog/kdv-oranlari-2026': 'KDV oranları 2026 – ürün ürün tablo', 'blog/emeklilik-hesaplama-2026': 'Rehber: Emeklilik şartları 2026',
 'blog/kidem-tazminati-2027': 'Kıdem tazminatı tavanı 2027', 'blog/memur-emekli-zammi-ocak-2027': 'Ocak 2027 memur ve emekli zammı tahmini',
 'blog/asgari-ucret-2027': 'Asgari ücret 2027 beklentileri', 'blog/fazla-mesai-haklari-2026': 'Rehber: Fazla mesai hakları 2026',
 'blog/net-maas-nasil-hesaplanir': 'Rehber: Net maaş nasıl hesaplanır?', 'blog/komisyon-hesaplama-rehberi': 'Rehber: Komisyon nasıl hesaplanır?',
 'blog/kira-geliri-vergisi-hesaplama': 'Rehber: Kira geliri vergisi', 'blog/sgk-primi-hesaplama-rehberi': 'Rehber: SGK primi nasıl hesaplanır?',
 'blog/banka-kredisi-taksit-hesaplama': 'Rehber: Kredi taksiti nasıl hesaplanır?', 'blog/enflasyon-etkisi-2026': 'Enflasyonun maaşa etkisi 2026',
 'blog/vergi-dilimleri-2027': 'Gelir vergisi dilimleri 2027', 'blog/kira-artisi-2027': 'Kira artışı 2027',
}
M = {  # kaynak sayfa -> hedefler
 'komisyon-hesaplama': ['para-sayma-hesaplama', 'pazaryeri-komisyon-hesaplama', 'prim-hesaplama', 'blog/komisyon-hesaplama-rehberi'],
 'yuzde-hesaplama': ['para-sayma-hesaplama', 'indirim-hesaplama', 'kdv-haric-hesaplama'],
 'doviz-cevirici': ['para-sayma-hesaplama', 'para-deger-kaybi-hesaplama', 'enflasyon-hesaplama'],
 'metrekare-fiyat-hesaplama': ['boya-hesaplama', 'tapu-harci-hesaplama', 'blog/tapu-harci-hesaplama'],
 'kira-artis-hesaplama': ['blog/kasim-2026-kira-artis-orani', 'boya-hesaplama', 'ekonomi-takvimi', 'blog/kira-geliri-vergisi-hesaplama'],
 'net-maas-hesaplama': ['maas-siralamasi', 'blog/brutten-nete-maas-tablosu-2026', 'issizlik-maasi-hesaplama', 'memur-maaslari'],
 'asgari-ucret-hesaplama': ['maas-siralamasi', 'blog/brutten-nete-maas-tablosu-2026', 'blog/asgari-ucret-2027'],
 'saatlik-ucret-hesaplama': ['fazla-mesai-hesaplama', 'maas-siralamasi', 'prim-hesaplama'],
 'kidem-tazminati-hesaplama': ['issizlik-maasi-hesaplama', 'blog/ihbar-tazminati-hesaplama', 'blog/kidem-tazminati-2027'],
 'ihbar-tazminati-hesaplama': ['issizlik-maasi-hesaplama', 'blog/ihbar-tazminati-hesaplama', 'kidem-tazminati-hesaplama'],
 'memur-maaslari': ['muhendis-maasi', 'doktor-maasi', 'hemsire-maasi', 'maas-siralamasi'],
 'ogretmen-maasi': ['muhendis-maasi', 'doktor-maasi', 'polis-maasi'],
 'polis-maasi': ['muhendis-maasi', 'hemsire-maasi', 'ogretmen-maasi'],
 'hemsire-maasi': ['doktor-maasi', 'muhendis-maasi', 'memur-maaslari'],
 'doktor-maasi': ['hemsire-maasi', 'muhendis-maasi', 'memur-maaslari'],
 'muhendis-maasi': ['doktor-maasi', 'ogretmen-maasi', 'memur-maaslari'],
 'kdv-hesaplama': ['kdv-haric-hesaplama', 'blog/kdv-oranlari-2026', 'pazaryeri-komisyon-hesaplama'],
 'fazla-mesai-hesaplama': ['prim-hesaplama', 'blog/fazla-mesai-haklari-2026', 'saatlik-ucret-hesaplama'],
 'enflasyon-hesaplama': ['para-deger-kaybi-hesaplama', 'ekonomi-takvimi', 'blog/enflasyon-etkisi-2026'],
 'internet-hizi-donusturucu': ['veri-kullanim-hesaplama', 'dosya-indirme-suresi-hesaplama'],
 'yakit-maliyeti-hesaplama': ['yakit-tuketimi-hesaplama', 'mtv-hesaplama', 'arac-muayene-gecikme-hesaplama'],
 'mtv-hesaplama': ['arac-muayene-gecikme-hesaplama', 'otv-hesaplama', 'yakit-tuketimi-hesaplama'],
 'arac-kredisi-hesaplama': ['otv-hesaplama', 'kredi-erken-kapama-hesaplama', 'mtv-hesaplama'],
 'elektrik-faturasi-hesaplama': ['blog/elektrik-faturasi-neden-yuksek', 'dogalgaz-faturasi-hesaplama', 'su-faturasi-hesaplama'],
 'kredi-hesaplama': ['kredi-erken-kapama-hesaplama', 'kredi-karti-asgari-odeme-hesaplama', 'borc-kapatma-hesaplama', 'blog/banka-kredisi-taksit-hesaplama'],
 'mevduat-faizi-hesaplama': ['para-deger-kaybi-hesaplama', 'ekonomi-takvimi', 'kripto-kar-zarar-hesaplama'],
 'tapu-harci-hesaplama': ['blog/tapu-harci-hesaplama', 'damga-vergisi-hesaplama', 'metrekare-fiyat-hesaplama'],
 'kar-marji-hesaplama': ['stok-karliligi-hesaplama', 'pazaryeri-komisyon-hesaplama', 'indirim-hesaplama'],
 'kar-zarar-hesaplama': ['stok-karliligi-hesaplama', 'kripto-kar-zarar-hesaplama'],
 'gelir-vergisi-hesaplama': ['blog/vergi-dilimleri-2027', 'blog/yeniden-degerleme-orani-2026', 'damga-vergisi-hesaplama', 'blog/kira-geliri-vergisi-hesaplama'],
 'memur-emekli-zammi-hesaplama': ['blog/memur-emekli-zammi-ocak-2027', 'emeklilik-yasi-hesaplama', 'ekonomi-takvimi'],
 'maas-zam-hesaplama': ['maas-siralamasi', 'blog/enflasyon-etkisi-2026', 'ekonomi-takvimi'],
 'yas-hesaplama': ['emeklilik-yasi-hesaplama'],
 'gun-hesaplama': ['is-gunu-hesaplama', 'yas-hesaplama', 'ekonomi-takvimi'],
 'dosya-boyutu-donusturucu': ['dosya-indirme-suresi-hesaplama', 'veri-kullanim-hesaplama', 'internet-hizi-donusturucu'],
 'tyt-net-hesaplama': ['ayt-net-hesaplama', 'kpss-net-hesaplama', 'takdir-tesekkur-hesaplama'],
 'not-ortalamasi-hesaplama': ['takdir-tesekkur-hesaplama', 'ayt-net-hesaplama'],
 'vucut-kitle-indeksi': ['bel-kalca-orani-hesaplama', 'hedef-kilo-suresi-hesaplama'],
 'ideal-kilo-hesaplama': ['hedef-kilo-suresi-hesaplama', 'bel-kalca-orani-hesaplama'],
 'roi-hesaplama': ['kripto-kar-zarar-hesaplama', 'yatirim-geri-donus-suresi-hesaplama'],
 'blog/kira-artisi-2027': ['blog/kasim-2026-kira-artis-orani', 'ekonomi-takvimi'],
 'blog/sgk-primi-hesaplama-rehberi': ['blog/brutten-nete-maas-tablosu-2026', 'issizlik-maasi-hesaplama'],
 'blog/net-maas-nasil-hesaplanir': ['blog/brutten-nete-maas-tablosu-2026', 'maas-siralamasi'],
 'blog/kidem-tazminati-2027': ['blog/ihbar-tazminati-hesaplama', 'issizlik-maasi-hesaplama'],
 'blog/emeklilik-hesaplama-2026': ['emeklilik-yasi-hesaplama', 'memur-emekli-zammi-hesaplama'],
 'blog/enflasyon-etkisi-2026': ['blog/yeniden-degerleme-orani-2026', 'para-deger-kaybi-hesaplama'],
 'blog/vergi-dilimleri-2027': ['blog/yeniden-degerleme-orani-2026', 'blog/kira-geliri-vergisi-hesaplama'],
 'blog/komisyon-hesaplama-rehberi': ['pazaryeri-komisyon-hesaplama', 'trendyol-komisyon-hesaplama'],
 'blog/kira-geliri-vergisi-hesaplama': ['blog/nafaka-hesaplama', 'kira-getirisi-hesaplama'],
 'blog/banka-kredisi-taksit-hesaplama': ['blog/dask-sigortasi-hesaplama', 'kredi-erken-kapama-hesaplama'],
 'blog/tapu-harci-hesaplama': ['blog/dask-sigortasi-hesaplama', 'damga-vergisi-hesaplama'],
 'blog/fazla-mesai-haklari-2026': ['blog/nafaka-hesaplama', 'prim-hesaplama'],
}
for k in ('trendyol-komisyon-hesaplama', 'hepsiburada-komisyon-hesaplama', 'shopier-komisyon-hesaplama'):
    N.setdefault(k, k.replace('-', ' ').title())
N['trendyol-komisyon-hesaplama'] = 'Trendyol komisyon hesaplama'
N['memur-emekli-zammi-hesaplama'] = 'Memur ve emekli zammı hesaplama'
N['is-gunu-hesaplama'] = 'İş günü hesaplama'; N['yas-hesaplama'] = 'Yaş hesaplama'; N['ayt-net-hesaplama'] = 'AYT net hesaplama'
N['kpss-net-hesaplama'] = 'KPSS net hesaplama'; N['takdir-tesekkur-hesaplama'] = 'Takdir teşekkür hesaplama'; N['bel-kalca-orani-hesaplama'] = 'Bel-kalça oranı'
N['hedef-kilo-suresi-hesaplama'] = 'Hedef kiloya kaç günde inerim?'; N['yatirim-geri-donus-suresi-hesaplama'] = 'Yatırım geri dönüş süresi'
N['dosya-indirme-suresi-hesaplama'] = 'Dosya indirme süresi'; N['kira-getirisi-hesaplama'] = 'Kira getirisi hesaplama'

M.update({
 'su-faturasi-hesaplama': ['dogalgaz-faturasi-hesaplama', 'elektrik-faturasi-hesaplama', 'blog/elektrik-faturasi-neden-yuksek'],
 'dogalgaz-faturasi-hesaplama': ['su-faturasi-hesaplama', 'elektrik-faturasi-hesaplama', 'blog/elektrik-faturasi-neden-yuksek'],
 'kira-getirisi-hesaplama': ['boya-hesaplama', 'tapu-harci-hesaplama', 'kira-artis-hesaplama'],
 'ayt-net-hesaplama': ['takdir-tesekkur-hesaplama', 'tyt-net-hesaplama', 'kpss-net-hesaplama'],
 'dosya-indirme-suresi-hesaplama': ['veri-kullanim-hesaplama', 'internet-hizi-donusturucu'],
 'arac-deger-kaybi-hesaplama': ['yakit-tuketimi-hesaplama', 'arac-muayene-gecikme-hesaplama', 'mtv-hesaplama'],
 'otv-hesaplama': ['yakit-tuketimi-hesaplama', 'arac-kredisi-hesaplama', 'mtv-hesaplama'],
})
N['arac-kredisi-hesaplama'] = 'Taşıt kredisi hesaplama'; N['asgari-ucret-2027-hesaplama'] = 'Asgari ücret 2027 zam hesaplama'
N['banka-komisyon-hesaplama'] = 'Banka komisyonu (EFT, havale, POS) hesaplama'
M['komisyon-hesaplama'] = M['komisyon-hesaplama'][:2] + ['banka-komisyon-hesaplama'] + M['komisyon-hesaplama'][2:]
N['turkiye-maaslari-2026'] = 'Türkiye’de maaşlar 2026 (dağılım ve istatistikler)'
for _k in ('maas-siralamasi', 'net-maas-hesaplama', 'memur-maaslari'): M.setdefault(_k, []); M[_k] = ['turkiye-maaslari-2026'] + [x for x in M[_k] if x != 'turkiye-maaslari-2026']
N['kar-payi-hesaplama'] = 'Kâr payı hesaplama (katılım hesabı, temettü)'
M['mevduat-faizi-hesaplama'] = ['kar-payi-hesaplama'] + M['mevduat-faizi-hesaplama']
M['asgari-ucret-hesaplama'] = ['asgari-ucret-2027-hesaplama'] + M['asgari-ucret-hesaplama']
M['blog/asgari-ucret-2027'] = ['asgari-ucret-2027-hesaplama', 'net-maas-hesaplama']; N['tyt-net-hesaplama'] = 'TYT net hesaplama'

N['emekli-maasi-hesaplama'] = 'Emekli maaşı hesaplama 2026 (en düşük aylık, Ocak 2027)'
for _k in ('memur-emekli-zammi-hesaplama', 'emeklilik-yasi-hesaplama', 'blog/memur-emekli-zammi-ocak-2027', 'blog/emeklilik-hesaplama-2026'):
    M.setdefault(_k, []); M[_k] = ['emekli-maasi-hesaplama'] + [x for x in M[_k] if x != 'emekli-maasi-hesaplama']
M['emekli-maasi-hesaplama'] = ['memur-emekli-zammi-hesaplama', 'emeklilik-yasi-hesaplama', 'blog/memur-emekli-zammi-ocak-2027']
N['not-ortalamasi-hesaplama'] = N.get('not-ortalamasi-hesaplama', 'Not ortalaması hesaplama'); N['obp-hesaplama'] = 'OBP hesaplama (diploma notundan YKS puanına katkı)'
for _k in ('tyt-net-hesaplama', 'ayt-net-hesaplama', 'not-ortalamasi-hesaplama'):
    M.setdefault(_k, []); M[_k] = ['obp-hesaplama'] + [x for x in M[_k] if x != 'obp-hesaplama']
M['obp-hesaplama'] = ['tyt-net-hesaplama', 'ayt-net-hesaplama', 'not-ortalamasi-hesaplama']

N['lgs-puan-hesaplama'] = 'LGS puan hesaplama (netten tahmini puan)'; N['kpss-puan-hesaplama'] = 'KPSS puan hesaplama (P3, P93, P94)'
N['kpss-net-hesaplama'] = N.get('kpss-net-hesaplama', 'KPSS net hesaplama')
for _k in ('obp-hesaplama', 'not-ortalamasi-hesaplama', 'takdir-tesekkur-hesaplama'):
    M.setdefault(_k, []); M[_k] = ['lgs-puan-hesaplama'] + [x for x in M[_k] if x != 'lgs-puan-hesaplama']
M.setdefault('kpss-net-hesaplama', []); M['kpss-net-hesaplama'] = ['kpss-puan-hesaplama'] + [x for x in M['kpss-net-hesaplama'] if x != 'kpss-puan-hesaplama']
for _k in ('memur-maaslari',):
    M.setdefault(_k, []); M[_k] = M[_k] + ['kpss-puan-hesaplama'] if 'kpss-puan-hesaplama' not in M[_k] else M[_k]
M['lgs-puan-hesaplama'] = ['obp-hesaplama', 'not-ortalamasi-hesaplama', 'takdir-tesekkur-hesaplama']
M['kpss-puan-hesaplama'] = ['kpss-net-hesaplama', 'memur-maaslari', 'yas-hesaplama']

def block(src):
    items = [t for t in M.get(src, []) if t != src and os.path.exists(t + '.html')]
    if not items:
        return ''
    links = ' · '.join(f'<a href="{B}{t}.html" style="text-decoration:underline">{N[t]}</a>' for t in items)
    return ('<!-- ICLINK --><div style="max-width:1100px;margin:18px auto 0;padding:0 16px"><div style="border:1px solid #e2e8f0;border-radius:12px;padding:12px 16px;font-size:.9rem;line-height:1.7;background:#f8fafc">'
            f'🔗 <strong>Bunlar da işinize yarayabilir:</strong> {links}</div></div><!-- /ICLINK -->')


def run():
    n = 0
    for src in M:
        p = src + '.html'
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'\n?<!-- ICLINK -->.*?<!-- /ICLINK -->\n?', '\n', s, flags=re.S)
        b = block(src)
        if not b:
            continue
        if '<footer' in s:
            s = s.replace('<footer', b + '\n<footer', 1)
        else:
            continue
        open(p, 'w', encoding='utf-8').write(s); n += 1
    return n


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(run(), 'sayfaya iç bağlantı kutusu eklendi')
