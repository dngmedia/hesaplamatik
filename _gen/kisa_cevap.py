"""'Kısa cevap' kutuları (öne çıkan snippet hedefi): en çok gösterim alan sayfalarda, 'nasıl hesaplanır' sorusuna
40–60 kelimelik net cevap + formül + örnek. build.py sonunda çalışır; <!-- KISA --> ... <!-- /KISA --> bloğu idempotenttir.
Kaynak rakamlar: 2026 asgari ücret 33.030 / 28.075,50; KDV %20; Ekim 2026 kira artış oranı %31,49; kurumlar vergisi %25.
"""
import os, re

# slug: (çapa metni, 'after' = çapadan hemen sonra / 'before' = çapadan önce kendi başlığıyla, başlık, cevap, formül, örnek)
D = {
 'saatlik-ucret-hesaplama': ('<h2 id="b-nasil">Saatlik ücret nasıl hesaplanır?</h2>', 'after', '',
   'Saatlik ücret, aylık ücretin <strong>225’e bölünmesiyle</strong> bulunur. 225, uygulamada aylık ücretin saat karşılığı bulunurken kullanılan çalışma saatidir (haftalık 45 saat esasına göre 30 gün × 7,5 saat). Brüt maaştan brüt saatlik ücret, net maaştan net saatlik ücret elde edilir.',
   'Saatlik ücret = Aylık ücret ÷ 225', '2026 brüt asgari ücret: 33.030 ₺ ÷ 225 = <strong>146,80 ₺</strong> · net: 28.075,50 ₺ ÷ 225 = <strong>124,78 ₺</strong>'),
 'komisyon-hesaplama': ('<h2>Komisyon Nasıl Hesaplanır?</h2>', 'after', '',
   'Komisyon, satış tutarının komisyon oranıyla çarpılıp <strong>100’e bölünmesiyle</strong> bulunur. Satıcının eline geçen net tutar, satış tutarından komisyonun çıkarılmasıyla hesaplanır. Komisyon faturalı bir hizmetse üzerine ayrıca KDV eklenir.',
   'Komisyon = Satış tutarı × Oran ÷ 100 · Net tutar = Satış − Komisyon', '100.000 ₺ satışta %3 komisyon: 100.000 × 3 ÷ 100 = <strong>3.000 ₺</strong>; satıcıya kalan <strong>97.000 ₺</strong>'),
 'kdv-hesaplama': ('<h2>KDV Nasıl Hesaplanır? Formüller</h2>', 'after', '',
   'KDV, KDV hariç fiyatın KDV oranıyla çarpılmasıyla bulunur; KDV dahil fiyat, hariç fiyata KDV eklenerek hesaplanır. KDV dahil bir fiyattan KDV’yi ayırmak için fiyat <strong>(1 + oran)</strong> sayısına bölünür. Türkiye’de 2026’da oranlar %1, %10 ve %20’dir.',
   'KDV = Hariç fiyat × Oran · Hariç fiyat = Dahil fiyat ÷ (1 + Oran)', '%20 KDV: 1.000 ₺ × 0,20 = <strong>200 ₺</strong> KDV, dahil fiyat <strong>1.200 ₺</strong> · 1.200 ₺ ÷ 1,20 = <strong>1.000 ₺</strong>'),
 'net-maas-hesaplama': ('<h2>Net Maaş Nasıl Hesaplanır? Formüller</h2>', 'after', '',
   'Net maaş, brüt maaştan <strong>%14 SGK işçi payı</strong>, <strong>%1 işsizlik sigortası</strong>, gelir vergisi ve damga vergisi düşülerek bulunur. 2026’da asgari ücrete isabet eden gelir ve damga vergisi istisna olduğundan, asgari ücretlinin net maaşı brütün tam %85’idir; daha yüksek maaşlarda vergi, istisna tutarı düşülerek hesaplanır.',
   'Net maaş = Brüt − SGK (%14) − İşsizlik (%1) − Gelir vergisi − Damga vergisi', '2026 asgari ücret: 33.030 ₺ brüt − 4.624,20 ₺ SGK − 330,30 ₺ işsizlik = <strong>28.075,50 ₺ net</strong>'),
 'metrekare-fiyat-hesaplama': ('<h2 id="b-nasil">Metrekare fiyatı nasıl hesaplanır?</h2>', 'after', '',
   'Metrekare fiyatı, evin veya arsanın satış fiyatının <strong>metrekaresine bölünmesiyle</strong> bulunur. İki ilanı karşılaştırırken ikisinde de aynı ölçüyü (brüt veya net m²) kullanın; aksi hâlde fark yanıltıcı olur.',
   'm² fiyatı = Satış fiyatı ÷ Metrekare', '4.500.000 ₺’lik 120 m² ev: 4.500.000 ÷ 120 = <strong>37.500 ₺/m²</strong>'),
 'indirim-hesaplama': ('<h2 id="b-indirimli-fiyat">İndirimli fiyat nasıl hesaplanır?</h2>', 'after', '',
   'İndirimli fiyat, fiyatın <strong>(1 − indirim oranı)</strong> ile çarpılmasıyla bulunur. İki fiyat arasındaki indirim yüzdesi ise fiyat farkının eski fiyata bölünüp 100 ile çarpılmasıyla hesaplanır.',
   'İndirimli fiyat = Fiyat × (1 − Oran ÷ 100) · İndirim % = (Eski − Yeni) ÷ Eski × 100', '1.200 ₺’ye %25 indirim: 1.200 × 0,75 = <strong>900 ₺</strong> · 1.200 ₺ → 900 ₺ indirimi = <strong>%25</strong>'),
 'yatirim-geri-donus-suresi-hesaplama': ('<h2 id="b-nedir">Geri dönüş (geri ödeme) süresi nedir?</h2>', 'before', 'Yatırım geri dönüş süresi nasıl hesaplanır?',
   'Geri dönüş süresi, yatırım tutarının yatırımın her dönem getirdiği <strong>net nakit girişine bölünmesiyle</strong> bulunur. Aylık net gelir kullanırsanız sonuç ay, yıllık net gelir kullanırsanız yıl olarak çıkar. Net nakit girişi, gelirden giderler ve vergiler düşüldükten sonra kalan tutardır.',
   'Geri dönüş süresi = Yatırım tutarı ÷ Dönemlik net nakit girişi', '1.000.000 ₺ yatırım, ayda 25.000 ₺ net getiri: 1.000.000 ÷ 25.000 = <strong>40 ay (≈3,3 yıl)</strong>'),
 'ortalama-hesaplama': ('<h2 id="b-aritmetik">Aritmetik ortalama nasıl hesaplanır?</h2>', 'after', '',
   'Aritmetik ortalama, sayıların <strong>toplamının sayı adedine bölünmesiyle</strong> bulunur. Ağırlıklı ortalamada ise her değer kendi ağırlığıyla (örneğin ders saati veya kredi) çarpılır, toplam, ağırlıkların toplamına bölünür.',
   'Ortalama = Sayıların toplamı ÷ Sayı adedi', '70, 85 ve 90: (70 + 85 + 90) ÷ 3 = 245 ÷ 3 = <strong>81,67</strong>'),
 'net-kar-hesaplama': ('<h2 id="b-nedir">Net kâr nedir?</h2>', 'before', 'Net kâr nasıl hesaplanır?',
   'Net kâr, satış gelirlerinden <strong>satılan malın maliyeti, faaliyet giderleri, finansman giderleri ve vergi</strong> düşüldükten sonra kalan tutardır. Net kâr marjı, net kârın net satışlara oranıdır. Şirketlerde 2026 kurumlar vergisi oranı %25’tir.',
   'Net kâr = Gelir − Maliyet − Giderler − Vergi · Net kâr marjı = Net kâr ÷ Net satış × 100', '1.000.000 ₺ gelir − 600.000 ₺ maliyet − 200.000 ₺ gider = 200.000 ₺ vergi öncesi kâr; %25 vergi sonrası <strong>150.000 ₺ net kâr</strong>, marj <strong>%15</strong>'),
 'kar-marji-hesaplama': ('<h2 id="b-nedir">Kâr marjı nedir?</h2>', 'before', 'Kâr marjı nasıl hesaplanır?',
   'Kâr marjı, satış fiyatı ile maliyet arasındaki farkın <strong>satış fiyatına bölünmesiyle</strong> bulunur. Aynı farkın maliyete bölünmesiyle bulunan orana ise kâr oranı (markup) denir; ikisi sık karıştırılır ve farklı sonuç verir.',
   'Kâr marjı = (Satış − Maliyet) ÷ Satış × 100 · Kâr oranı = (Satış − Maliyet) ÷ Maliyet × 100', '100 ₺’ye alınıp 150 ₺’ye satılan ürün: kâr marjı 50 ÷ 150 = <strong>%33,3</strong>, kâr oranı 50 ÷ 100 = <strong>%50</strong>'),
 'boya-hesaplama': ('<h2>Boya Hesaplama Nasıl Yapılır? 2026 Formülü</h2>', 'after', '',
   'Gereken boya miktarı, boyanacak alanın kat sayısıyla çarpılıp <strong>1 litre boyanın kapladığı alana bölünmesiyle</strong> bulunur. İç cephe boyaları 1 litrede tek katta yaklaşık 10–12 m² boyar. Döküntü ve rötuş için sonuca %10–15 fire payı ekleyin.',
   'Litre = Alan (m²) × Kat sayısı ÷ 1 litrenin boyadığı alan', '3×4 m oda, 2,6 m tavan: duvar alanı 2 × 2,6 × (3 + 4) = 36,4 m²; 2 kat, 10 m²/L → 7,3 L; %15 fire ile <strong>≈8,4 litre</strong>'),
 'ciro-hesaplama': ('<h2>Ciro Nedir? 2026 Kapsamlı Rehber</h2>', 'before', 'Ciro nasıl hesaplanır?',
   'Ciro, satılan ürün veya hizmet adedinin <strong>birim satış fiyatıyla çarpılmasıyla</strong> bulunur. Net ciro, brüt cirodan indirimler ve iadeler düşülerek hesaplanır. Ciro bir kâr göstergesi değildir; kâr için giderlerin de düşülmesi gerekir.',
   'Ciro = Satış adedi × Birim fiyat · Net ciro = Brüt ciro − İndirimler − İadeler', '500 adet × 200 ₺ = <strong>100.000 ₺</strong> brüt ciro; 5.000 ₺ iade ile <strong>95.000 ₺</strong> net ciro'),
 'yuzde-hesaplama': ('<h2>Yüzde Nedir? Temel Kavramlar</h2>', 'before', 'Yüzde nasıl hesaplanır?',
   'Bir sayının yüzdesi, sayının yüzde değeriyle çarpılıp <strong>100’e bölünmesiyle</strong> bulunur. İki değer arasındaki yüzde değişim ise farkın eski değere bölünüp 100 ile çarpılmasıyla hesaplanır; sonuç pozitifse artış, negatifse azalıştır.',
   'Yüzde = Sayı × Oran ÷ 100 · Değişim % = (Yeni − Eski) ÷ Eski × 100', '250’nin %20’si: 250 × 20 ÷ 100 = <strong>50</strong> · 80’den 100’e artış: 20 ÷ 80 × 100 = <strong>%25</strong>'),
 'kira-artis-hesaplama': ('<h2 id="b-oran">Ekim 2026 kira artış oranı ne kadar?</h2>', 'before', 'Kira artışı nasıl hesaplanır?',
   'Konut kiralarında yeni kira, mevcut kiranın <strong>12 aylık TÜFE ortalaması oranında</strong> artırılmasıyla bulunur; bu oran yasal üst sınırdır. Oran, kira döneminin yenilendiği aydan önceki ay için TÜİK’in açıkladığı 12 aylık ortalama değişimdir ve her ay yeniden belirlenir.',
   'Yeni kira = Mevcut kira × (1 + 12 aylık TÜFE ortalaması ÷ 100)', 'Ekim 2026’da yenilenen 20.000 ₺ kira: 20.000 × 1,3149 = <strong>26.298 ₺</strong> (%31,49 artış)'),
}

STYLE = ('border:2px solid #bfdbfe;background:#eff6ff;border-radius:14px;padding:16px 18px;margin:14px 0 22px;line-height:1.65;font-size:.95rem')


def block(slug):
    anchor, mode, baslik, cevap, formul, ornek = D[slug]
    inner = (f'<p style="margin:0 0 10px"><strong>Kısa cevap:</strong> {cevap}</p>'
             f'<p style="margin:0 0 8px;font-family:ui-monospace,Menlo,Consolas,monospace;background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:8px 10px;font-size:.88rem">{formul}</p>'
             f'<p style="margin:0"><strong>Örnek:</strong> {ornek}</p>')
    box = f'<div class="kisa-cevap" style="{STYLE}">{inner}</div>'
    return f'<!-- KISA -->{"<h2>" + baslik + "</h2>" if mode == "before" else ""}{box}<!-- /KISA -->'


def run():
    n, miss = 0, []
    for slug, (anchor, mode, *_r) in D.items():
        p = slug + '.html'
        if not os.path.exists(p):
            miss.append(slug); continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<!-- KISA -->.*?<!-- /KISA -->', '', s, flags=re.S)
        if anchor not in s:
            miss.append(slug); continue
        b = block(slug)
        s = s.replace(anchor, anchor + b, 1) if mode == 'after' else s.replace(anchor, b + anchor, 1)
        open(p, 'w', encoding='utf-8').write(s); n += 1
    return n, miss


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(run())
