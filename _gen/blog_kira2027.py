"""blog/kira-artisi-2027 yeniden yazımı (24 Ekim 2026). 3 Kasım ve sonrası verilerle AY26 sözlüğü güncellenip yeniden çalıştırılır."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newpost import make, tl, table, hero
B = 'https://hesaplarsin.com'
ORAN26 = [('Ocak', 34.88), ('Şubat', 33.98), ('Mart', 33.39), ('Nisan', 32.82), ('Mayıs', 32.43), ('Haziran', 32.24),
          ('Temmuz', 32.03), ('Ağustos', 31.90), ('Eylül', 31.79), ('Ekim', 31.49)]
# Yıllık TÜFE (%) — 2025 gerçekleşen; 2026 Tem–Ağu, kira oranlarındaki aylık farktan türetilmiş; Eyl 2026 TÜİK
Y = {'2025-10': 32.87, '2025-11': 31.07, '2025-12': 30.89, '2026-07': 31.96, '2026-08': 31.63, '2026-09': 29.73}
# OVP senaryosu: Ekim–Aralık 2026 yıllık TÜFE 2026 sonu %28,4'e, 2027 boyunca 2027 sonu %21'e doğrusal iner
for i, m in enumerate(('10', '11', '12')):
    Y['2026-' + m] = 29.73 + (28.4 - 29.73) * (i + 1) / 3
for k in range(1, 13):
    Y[f'2027-{k:02d}'] = 28.4 + (21.0 - 28.4) * k / 12
def ort(son_ay):  # son_ay = (yıl, ay): kira oranı = önceki 12 ayın yıllık TÜFE ortalaması
    y, m = son_ay; keys = []
    for _ in range(12):
        keys.append(f'{y}-{m:02d}'); m -= 1
        if m == 0: y, m = y - 1, 12
    return sum(Y[k] for k in keys) / 12, keys
O_OCAK27 = 31.49 + (Y['2026-10'] + Y['2026-11'] + Y['2026-12'] - Y['2025-10'] - Y['2025-11'] - Y['2025-12']) / 12
O_TEM27, _ = ort((2027, 6))
O_OCAK28, _ = ort((2027, 12))
t = lambda x: tl(x, 0) + ' TL'
p = lambda x: '%' + tl(x, 2)
K = 20000
body = f'''
  <p class="lead">Konut ve işyeri kiralarında yıllık artış, Türk Borçlar Kanunu gereği <strong>TÜFE’nin 12 aylık ortalamasıyla</strong> sınırlıdır. Bu nedenle 2027’de kiraların ne kadar artacağı, 2026 ve 2027’de enflasyonun nasıl seyredeceğine bağlı. Bu yazıda 2026’da ay ay uygulanan oranları, 2027 TÜFE beklentisini ve 2027’de kira zammı için tahminlerimizi bulacaksınız.</p>

  <div class="highlight-box">
    <p><strong>Kısaca:</strong></p>
    <p>• Ekim 2026 yasal kira artış oranı: <strong>%31,49</strong> (Kasım tahmini ~%31,2)</p>
    <p>• Orta Vadeli Program (Eylül 2026): 2026 sonu enflasyon beklentisi <strong>%28,4</strong>, 2027 sonu hedefi <strong>%21</strong></p>
    <p>• Ocak 2027 kira artış oranı tahmini: yaklaşık <strong>{p(O_OCAK27)}</strong> · Temmuz 2027: yaklaşık <strong>{p(O_TEM27)}</strong></p>
    <p>• Sınır hem konut hem çatılı işyeri kiralarında geçerlidir.</p>
  </div>

  <h2>Kira Artış Oranı Nasıl Belirlenir?</h2>
  <p>Türk Borçlar Kanunu’nun 344. maddesine göre konut ve çatılı işyeri kiralarında yenileme dönemindeki artış, bir önceki kira yılındaki <strong>TÜFE’nin 12 aylık ortalamalara göre değişim oranını</strong> geçemez. Oran her ayın 3’ünde TÜİK enflasyon bülteninde yayımlanır ve o ay yenilenen sözleşmelere uygulanır. Sözleşmede daha düşük bir oran yazıyorsa o oran geçerlidir.</p>
  <p>11 Haziran 2022 ile 1 Temmuz 2024 arasında konut kiralarında geçici olarak <strong>%25 sınırı</strong> uygulanmıştı. Bu dönem sona erdiğinden bugün tüm konut ve işyeri kiralarında 12 aylık TÜFE ortalaması esas alınıyor. Beş yılını dolduran kira sözleşmelerinde ise kira bedeli emsallere göre yeniden belirlenebilir (TBK m.344/3).</p>

  <h2>2026’da Ay Ay Kira Artış Oranları</h2>
''' + table(['Sözleşme yenileme ayı', 'Yasal azami artış', f'{t(K)} kira → yeni kira'], [[f'{a} 2026', p(o), t(K * (1 + o / 100))] for a, o in ORAN26], '2026 kira artış oranları') + f'''
  <p>Oranlar yıl boyunca yavaş yavaş düştü; çünkü 12 aylık ortalamaya giren yeni aylardaki yıllık enflasyon, çıkan aylardakinden düşük. Kendi kiranızı hesaplamak için <a href="{B}/kira-artis-hesaplama.html">kira artış hesaplama</a> aracını kullanabilirsiniz.</p>

  <h2>2027 TÜFE (TEFE-TÜFE) Tahmini</h2>
  <p>Hükümetin 7 Eylül 2026’da açıkladığı Orta Vadeli Program’a (2027–2029) göre yıl sonu enflasyon beklentileri:</p>
''' + table(['Yıl', 'Yıl sonu TÜFE (OVP)'], [['2026', '%28,4 (beklenti)'], ['2027', '%21 (hedef)'], ['2028', '%13,5 (hedef)'], ['2029', '%9 (hedef)']], 'OVP enflasyon hedefleri') + f'''
  <p>Kira artışında “TEFE” artık kullanılmıyor; yalnızca TÜFE’nin 12 aylık ortalaması esas alınıyor. Eylül 2026’da yıllık TÜFE %29,73 oldu.</p>

  <h2>2027 Kira Zam Oranı Tahmini</h2>
  <p>Kira oranı geçmiş 12 ayın ortalaması olduğu için enflasyondaki düşüşü gecikmeli yansıtır. Yıllık enflasyonun OVP’deki gibi 2026 sonunda %28,4’e, 2027 sonunda %21’e doğrusal olarak indiğini varsayarak hesapladığımız tahminler:</p>
''' + table(['Sözleşme yenileme ayı', 'Tahmini azami artış', f'{t(K)} kira → yeni kira'], [
    ['Ocak 2027', '≈ ' + p(O_OCAK27), t(K * (1 + O_OCAK27 / 100))],
    ['Temmuz 2027', '≈ ' + p(O_TEM27), t(K * (1 + O_TEM27 / 100))],
    ['Ocak 2028', '≈ ' + p(O_OCAK28), t(K * (1 + O_OCAK28 / 100))]], '2027 kira artışı tahmini') + f'''
  <p>Enflasyon OVP hedefinin üzerinde kalırsa oranlar tablodakinden yüksek olur. Ocak 2027 oranı, TÜİK’in 4 Ocak 2027’de açıklayacağı Aralık verisiyle kesinleşecek; bu sayfa her ay güncellenir.</p>

  <h2>Kiracı ve Ev Sahibi İçin Bilmeniz Gerekenler</h2>
  <ul>
    <li><strong>Sınırın üzerinde zam:</strong> Yasal oranın üzerindeki artış talebi kiracıyı bağlamaz; kiracı yasal orandaki artışla ödemeye devam edebilir.</li>
    <li><strong>Sözleşme ayı önemli:</strong> Uygulanacak oran, sözleşmenin yenilendiği aya göre belirlenir; kira başlangıç tarihinizi kontrol edin.</li>
    <li><strong>Beş yıl kuralı:</strong> Beş yılı dolduran sözleşmelerde ev sahibi, kira tespit davasıyla bedelin emsallere göre belirlenmesini isteyebilir.</li>
    <li><strong>Kira geliri vergisi:</strong> Ev sahipleri için 2026 konut kira istisnası 58.000 TL’dir; ayrıntılar <a href="{B}/blog/kira-geliri-vergisi-hesaplama.html">kira geliri vergisi rehberinde</a>.</li>
  </ul>

  <h2>Kaynaklar</h2>
  <p style="font-size:.88rem">6098 sayılı Türk Borçlar Kanunu m.344 · TÜİK Tüketici Fiyat Endeksi bültenleri (2025–2026) · Orta Vadeli Program 2027–2029 (7 Eylül 2026).</p>
'''
faq = [
    ('2027 TÜFE oranı tahmini ne kadar?', 'Orta Vadeli Program’a göre 2027 yıl sonu enflasyon hedefi %21’dir; 2026 sonu beklentisi %28,4’tür. Eylül 2026’da yıllık TÜFE %29,73 olmuştu.'),
    ('Ocak 2027 kira artış oranı ne kadar olacak?', f'Aralık 2026 verisiyle 4 Ocak 2027’de belli olacak. Enflasyonun OVP beklentisine yakın seyretmesi halinde oranın yaklaşık {p(O_OCAK27)} olacağını tahmin ediyoruz.'),
    ('2027 kira zam oranı tahmini nedir?', f'Tahminimize göre yasal azami artış Ocak 2027’de yaklaşık {p(O_OCAK27)}, Temmuz 2027’de yaklaşık {p(O_TEM27)} olur. Oranlar enflasyon düştükçe yıl içinde azalır.'),
    ('İşyeri kiralarında artış sınırı var mı?', 'Evet. TBK 344. maddedeki 12 aylık TÜFE ortalaması sınırı hem konut hem çatılı işyeri kiraları için geçerlidir.'),
    ('Kira artışında TEFE kullanılıyor mu?', 'Hayır. TEFE yerine Yİ-ÜFE kullanılmaya başlandı ve kira artışında yalnızca TÜFE’nin 12 aylık ortalaması esas alınır.'),
]
rel = [('🏠', 'Kira Artış Hesaplama', 'Ekim 2026: %31,49', f'{B}/kira-artis-hesaplama.html'),
       ('📅', 'Kasım 2026 Kira Artış Oranı', 'Tahmin ve tablo', f'{B}/blog/kasim-2026-kira-artis-orani.html'),
       ('📈', 'Enflasyon Hesaplama', 'Paranın alım gücü', f'{B}/enflasyon-hesaplama.html'),
       ('🧾', 'Kira Geliri Vergisi', '58.000 TL istisna', f'{B}/blog/kira-geliri-vergisi-hesaplama.html')]
if __name__ == '__main__':
    print(O_OCAK27, O_TEM27, O_OCAK28)
    print(make('kira-artisi-2027',
         'Kira Artış Oranı 2027 Tahmini – 2027 TÜFE Beklentisi ve Kira Zammı | Hesaplarsın',
         f'2027 kira zam oranı tahmini: Ocak 2027 ≈ {p(O_OCAK27)}, Temmuz 2027 ≈ {p(O_TEM27)}. OVP’ye göre 2027 TÜFE hedefi %21. 2026’da ay ay kira artış oranları ve hesaplama.',
         'kira artış oranı 2027, 2027 kira zam oranı tahmini, 2027 tüfe tahmini, 2027 tefe tüfe oranı, ocak 2027 kira artışı',
         'Kira Artış Oranı 2027', 'Kira Artış Oranı 2027: TÜFE Beklentisi ve Kira Zammı Tahmini',
         hero('🏠', 'Ocak 2027 tahmini', 'EKİM 2026 KİRA ORANI', '%31,49', 'OCAK 2027 TAHMİNİ', '≈ ' + p(O_OCAK27), '#065f46', '#10b981'),
         ['Kira', 'Gündem'], body, faq, rel, date='2026-10-24', date_tr='24 Ekim 2026'))
