"""blog/aralik-2026-kira-artis-orani (20 Kas 2026). 3 Aralık 2026'da TÜİK Kasım verisi açıklanınca KESIN doldurulup yeniden çalıştırılır."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newpost import make, tl, table, hero
from blog_kira2027 import ORAN26, ARA_SEN, Y
B = 'https://hesaplarsin.com'
KESIN = None   # 3 Aralık'ta: (oran, aylık TÜFE, yıllık TÜFE) ör. (31.08, 0.62, 29.44)
assert ORAN26[-1] == ('Kasım', 31.23)
p = lambda x: '%' + tl(x, 2)
t = lambda x: tl(x, 0) + ' TL'
o_mid = ARA_SEN[1][2]; o_lo = ARA_SEN[0][2]; o_hi = ARA_SEN[2][2]
O = KESIN[0] if KESIN else o_mid
KIRALAR = [10000, 15000, 20000, 25000, 30000, 40000, 50000]
ust = (f'<p>• Aralık 2026 kira artış oranı: <strong>{p(KESIN[0])}</strong> (TÜİK, 3 Aralık 2026)</p>' if KESIN else
       f'<p>• Aralık 2026 kira artış oranı tahmini: <strong>yaklaşık {p(o_mid)}</strong> (senaryolara göre {p(o_lo)} – {p(o_hi)})</p>'
       f'<p>• Kesin oran <strong>3 Aralık 2026 Perşembe saat 10:00</strong>’da TÜİK’in Kasım enflasyonuyla açıklanacak</p>')
body = f'''
  <p class="lead">Aralık 2026’da kira sözleşmesi yenilenecek kiracılar ve ev sahipleri için yasal azami artış, TÜFE’nin <strong>12 aylık ortalamasına</strong> göre belirlenir. Bu oran 3 Aralık’ta açıklanacak Kasım enflasyonuyla kesinleşir; aşağıda olası senaryoları ve kiranızın ne kadar olacağını bulabilirsiniz.</p>

  <div class="highlight-box">
    <p><strong>Kısaca:</strong></p>
    {ust}
    <p>• Kasım 2026 oranı: <strong>%31,23</strong> · Ekim 2026: <strong>%31,49</strong></p>
    <p>• Sınır hem konut hem çatılı işyeri kiralarında geçerlidir (TBK m.344).</p>
  </div>

  <h2>Aralık 2026 Kira Artış Oranı Ne Kadar Olacak?</h2>
  <p>Kira artış oranı, son 12 ayın yıllık enflasyon ortalamasıdır. Aralık oranında Kasım 2025’in yıllık enflasyonu (%31,07) hesaptan çıkar, yerine Kasım 2026 girer. Ekim 2026’da yıllık TÜFE %29,77 olduğundan, Kasım 2025’teki aylık %0,87’lik artışın ardından Kasım 2026’nın aylık enflasyonuna göre üç senaryo:</p>
''' + table(['Kasım 2026 aylık TÜFE', 'Kasım 2026 yıllık TÜFE', 'Aralık 2026 kira artış oranı'],
            [[p(m), p(y), '≈ ' + p(o)] for m, y, o in ARA_SEN], 'Aralık 2026 kira artış oranı senaryoları') + f'''
  <p>Aylık enflasyon hangi aralıkta gelirse gelsin oran <strong>%31 civarında</strong> kalır ve Kasım’daki %31,23’ün biraz altında olur. Tahminler, 12 aylık ortalamanın yıllık enflasyon oranlarının ortalamasına yakın seyretmesi varsayımıyla hesaplanmıştır; TÜİK’in endeks üzerinden açıkladığı resmî oran birkaç yüzde onda bir farklı olabilir.</p>

  <h2>Aralık 2026 Kira Zammı Tablosu</h2>
  <p>Mevcut kiranıza göre Aralık’ta istenebilecek en yüksek yeni kira ({"kesin oran" if KESIN else "≈ " + p(O) + " tahminiyle"}):</p>
''' + table(['Mevcut kira', 'Azami artış', 'Yeni kira (en fazla)'], [[t(k), t(k * O / 100), t(k * (1 + O / 100))] for k in KIRALAR], 'Aralık 2026 kira zammı tablosu') + f'''
  <p>Kendi kiranızı hesaplamak için <a href="{B}/kira-artis-hesaplama.html">kira artış hesaplama</a> aracını kullanabilirsiniz. Oran açıklandığı gün araç ve bu sayfa güncellenir.</p>

  <h2>2026 Kira Artış Oranları (Ay Ay)</h2>
''' + table(['Sözleşme yenileme ayı', 'Yasal azami artış'], [[f'{a} 2026', p(o)] for a, o in ORAN26] + [['Aralık 2026', (p(KESIN[0]) if KESIN else '≈ ' + p(o_mid) + ' (3 Aralık’ta)')]], '2026 kira artış oranları') + f'''
  <p>Oran Ocak’tan bu yana her ay düşüyor; çünkü yüksek enflasyonlu 2025 ayları 12 aylık ortalamadan çıkıyor. 2027’de kiraların nasıl seyredeceği için <a href="{B}/blog/kira-artisi-2027.html">2027 kira artışı tahmini</a> yazımıza bakabilirsiniz.</p>

  <h2>Kiracı ve Ev Sahibi Nelere Dikkat Etmeli?</h2>
  <ul>
    <li><strong>Hangi ayın oranı?</strong> Sözleşmenin yenilendiği ayda açıklanan son oran uygulanır. Aralık’ta yenilenen sözleşmeler için 3 Aralık’ta açıklanacak oran geçerlidir.</li>
    <li><strong>Üst sınırdır:</strong> Taraflar daha düşük bir artışta anlaşabilir; sözleşmedeki oran yasal sınırın altındaysa sözleşme oranı uygulanır.</li>
    <li><strong>5 yıl kuralı:</strong> 5 yılı dolduran kira ilişkilerinde kira, mahkemece emsal kiralara göre yeniden belirlenebilir (TBK m.344/3).</li>
    <li><strong>İşyeri kiraları:</strong> Aynı sınır çatılı işyerleri için de geçerlidir. Kiracı şirketse %20 stopaj ayrıca hesaplanır; bkz. <a href="{B}/kira-stopaji-hesaplama.html">kira stopajı hesaplama</a>.</li>
  </ul>

  <h2>Kaynaklar</h2>
  <ul>
    <li>TÜİK Tüketici Fiyat Endeksi bültenleri (Kasım 2025: aylık %0,87, yıllık %31,07; Ekim 2026: yıllık %29,77, 12 aylık ortalama %31,23)</li>
    <li>6098 sayılı Türk Borçlar Kanunu m.344</li>
  </ul>
'''
faq = [
    ('Aralık 2026 kira artış oranı ne zaman açıklanacak?', 'TÜİK Kasım 2026 enflasyonunu 3 Aralık 2026 Perşembe saat 10:00’da açıklayacak. Aralık kira artış oranı, açıklanan TÜFE’nin 12 aylık ortalamasıdır.'),
    ('Aralık 2026 kira artış oranı ne kadar olacak?', (f'Aralık 2026 kira artış oranı {p(KESIN[0])} oldu.' if KESIN else f'Kasım aylık enflasyonu %0,3 ile %1 arasında gelirse oran yaklaşık {p(o_lo)} ile {p(o_hi)} arasında olur; yani %31 civarında, Kasım’daki %31,23’ün biraz altında.')),
    ('20.000 TL kira Aralık’ta ne kadar olur?', f'{"Kesin oranla" if KESIN else "Yaklaşık " + p(O) + " tahminiyle"} 20.000 TL kira en fazla {t(20000 * (1 + O / 100))} olur.'),
    ('Kira artış oranı neden her ay değişiyor?', 'Oran, son 12 ayın yıllık TÜFE ortalamasıdır. Her ay bir eski ay hesaptan çıkıp yeni ay girdiği için oran değişir; enflasyon düştükçe oran da yavaşça düşer.'),
    ('Ev sahibi yasal sınırdan fazla zam isteyebilir mi?', 'Hayır. Konut ve çatılı işyeri kiralarında yenilenen dönemde artış, 12 aylık TÜFE ortalamasını geçemez. Fazlası için kiracı ödeme yükümlülüğü altında değildir.'),
]
rel = [('🏠', 'Kira Artış Hesaplama', 'Yeni kiranızı hesaplayın', f'{B}/kira-artis-hesaplama.html'),
       ('📅', 'Kasım 2026 Kira Artış Oranı', '%31,23', f'{B}/blog/kasim-2026-kira-artis-orani.html'),
       ('📈', '2027 Kira Artışı Tahmini', 'Ocak ve Temmuz 2027', f'{B}/blog/kira-artisi-2027.html'),
       ('🏢', 'Kira Stopajı Hesaplama', 'İşyeri kirasında %20', f'{B}/kira-stopaji-hesaplama.html')]
if __name__ == '__main__':
    title = (f'Aralık 2026 Kira Artış Oranı Belli Oldu: {p(KESIN[0])} – Kira Zammı Tablosu | Hesaplarsın' if KESIN else
             'Aralık 2026 Kira Artış Oranı Ne Kadar Olacak? Tahmin ve Kira Zammı Tablosu | Hesaplarsın')
    desc = (f'Aralık 2026 kira artış oranı {p(KESIN[0])} (TÜİK). Kiranıza göre yeni kira tablosu ve ay ay 2026 oranları.' if KESIN else
            f'Aralık 2026 kira artış oranı 3 Aralık’ta açıklanacak; tahminimiz ≈ {p(o_mid)}. 10.000–50.000 TL kiralar için yeni kira tablosu, senaryolar ve ay ay 2026 oranları.')
    make('aralik-2026-kira-artis-orani', title, desc,
         'aralık ayı kira artış oranı, aralık 2026 kira artış oranı, aralık kira zammı, kira artış oranı aralık 2026',
         'Aralık 2026 Kira Artış Oranı', 'Aralık 2026 Kira Artış Oranı' + (' Belli Oldu' if KESIN else ': Ne Kadar Olacak?'),
         hero('🏠', 'Aralık 2026', 'KASIM 2026 ORANI', '%31,23', 'ARALIK 2026' + ('' if KESIN else ' TAHMİNİ'), (p(KESIN[0]) if KESIN else '≈ ' + p(o_mid)), '#065f46', '#10b981'),
         ['Kira', 'Gündem'], body, faq, rel, date='2026-11-20', date_tr='20 Kasım 2026')
    print('ok', round(o_lo, 2), round(o_mid, 2), round(o_hi, 2))
