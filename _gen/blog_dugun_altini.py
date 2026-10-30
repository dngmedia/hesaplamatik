"""blog/dugun-altini-rehberi – 29 Ekim 2026. Repo kökünden: python3 _gen/blog_dugun_altini.py
Fiyatlar: Kapalıçarşı (Truncgil Finans) 29.10.2026 09:50. Gramajlar: Hazine ve Maliye Bakanlığı, Sorularla Cumhuriyet Altını."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newpost import make, tl, table, hero
B = 'https://hesaplarsin.com'
t = lambda x: tl(x, 2) + ' TL'
# (ad, adet/gram, alış, satış, ağırlık g, birim)
F = {'ceyrek': ('Çeyrek altın', 10392.68, 10632.48, 1.754), 'yarim': ('Yarım altın', 20720.42, 21264.96, 3.508),
     'tam': ('Tam altın', 41570.74, 42399.85, 7.016), 'cumhuriyet': ('Cumhuriyet altını', 43082.0, 43724.0, 7.216),
     'b22': ('22 ayar bilezik (gram)', 5923.83, 5930.78, 1.0)}
ORN = [('ceyrek', 15), ('yarim', 4), ('tam', 2), ('cumhuriyet', 1), ('b22', 40)]
AL = sum(F[k][1] * n for k, n in ORN); SA = sum(F[k][2] * n for k, n in ORN)
HAS = sum(F[k][3] * n * 22 / 24 for k, n in ORN)
rows = [[F[k][0], (f'{n} gram' if k == 'b22' else f'{n} adet'), t(F[k][1] * n), t(F[k][2] * n)] for k, n in ORN]
rows.append(['<strong>Toplam</strong>', '', f'<strong>{t(AL)}</strong>', f'<strong>{t(SA)}</strong>'])
body = f'''
  <p class="lead">Düğünde, nişanda ya da sünnette takılan altınlar çoğu aile için ciddi bir birikimdir. Bu birikimin bugün kaç lira ettiğini doğru hesaplamak, bozdururken ya da saklarken doğru karar vermenin ilk adımıdır. Bu rehberde ziynet altınlarının gramajlarını, kuyumcunun alış ve satış fiyatı arasındaki farkı ve bozdurmadan önce dikkat etmeniz gerekenleri örnekle anlatıyoruz.</p>

  <div class="highlight-box">
    <p><strong>Kısaca:</strong></p>
    <p>• Bozdururken kuyumcunun <strong>alış</strong> fiyatı geçerlidir; bu fiyat satış fiyatının altındadır.</p>
    <p>• Çeyrek altın 1,754 gram, tam altın 7,016 gram, Cumhuriyet altını 7,216 gramdır; hepsi 22 ayardır.</p>
    <p>• Bilezik ve takılarda ödediğiniz işçilik bozdururken geri alınmaz; yalnızca altının gram değeri ödenir.</p>
    <p>• Kendi altınlarınızın güncel değerini <a href="{B}/altin-hesaplama.html">altın hesaplama</a> aracıyla saniyeler içinde görebilirsiniz.</p>
  </div>

  <h2>Ziynet Altınları Kaç Gram?</h2>
''' + table(['Altın', 'Ağırlık', 'Ayar', 'Saf altın'], [
    ['Çeyrek', '1,754 g', '22 ayar', '≈ 1,608 g'], ['Yarım', '3,508 g', '22 ayar', '≈ 3,216 g'], ['Tam', '7,016 g', '22 ayar', '≈ 6,431 g'],
    ['Cumhuriyet (Ata)', '7,216 g', '22 ayar', '≈ 6,615 g'], ['Gremse (ikibuçuk)', '17,540 g', '22 ayar', '≈ 16,078 g'], ['Beşli', '35,080 g', '22 ayar', '≈ 32,157 g'],
], 'Ziynet altın gramajları') + f'''
  <p>Gramajlar Darphane’nin bastığı ziynet ve Cumhuriyet altınlarına aittir. Çeyrek altının piyasa fiyatı içindeki saf altının değerinden biraz yüksektir; aradaki fark basım maliyeti (işçilik) ve kuyumcu payıdır.</p>

  <h2>Örnek: Düğünde Takılan Altınlar Ne Eder?</h2>
  <p>15 çeyrek, 4 yarım, 2 tam, 1 Cumhuriyet altını ve toplam 40 gram 22 ayar bilezik takılmış bir düğünü, 29 Ekim 2026 sabahki Kapalıçarşı fiyatlarıyla hesaplayalım:</p>
''' + table(['Altın', 'Miktar', 'Bozdurursanız (alış)', 'Satın alırsanız (satış)'], rows, 'Örnek düğün altını hesabı') + f'''
  <p>Bu altınları bozdurduğunuzda yaklaşık <strong>{t(AL)}</strong> alırsınız. Aynı altınları kuyumcudan satın almak ise yaklaşık <strong>{t(SA)}</strong> tutar; aradaki <strong>{t(SA - AL)}</strong> alış-satış farkıdır. Toplam saf altın miktarı yaklaşık {tl(HAS, 1)} gramdır. Fiyatlar gün içinde değişir; güncel tutar için <a href="{B}/altin-hesaplama.html">altın hesaplama</a> aracına kendi adetlerinizi girin.</p>

  <h2>Altın Bozdururken Nelere Dikkat Etmeli?</h2>
  <ol>
    <li><strong>Alış fiyatını sorun:</strong> Vitrinde ya da ekranda gördüğünüz fiyat genellikle satış fiyatıdır. Bozdururken size ödenecek olan kuyumcunun alış fiyatıdır.</li>
    <li><strong>Birkaç kuyumcudan fiyat alın:</strong> Alış fiyatları kuyumcudan kuyumcuya değişir. Büyük tutarlarda birkaç yerden teklif almak fark yaratabilir.</li>
    <li><strong>Altınların durumunu bilin:</strong> Bazı kuyumcular eski, aşınmış ya da ambalajı açılmış ziynet altınlarını yeni basılmışlardan biraz daha düşük fiyatla alabilir.</li>
    <li><strong>Bilezikte işçiliği hesaba katmayın:</strong> Bilezik bozdururken yalnızca altının gram değeri ödenir. Kuyumcu tartıp ayarını kontrol eder ve 22 ayar alış fiyatından hesaplar.</li>
    <li><strong>Fiş veya belge isteyin:</strong> Satılan altınların türü, adedi, gramı ve fiyatı yazılı olarak kayıt altında olsun.</li>
  </ol>

  <h2>Bozdurmak mı, Saklamak mı?</h2>
  <p>Bu karar tamamen kişisel ihtiyaca bağlıdır ve burada yatırım tavsiyesi vermiyoruz. Karar verirken şu noktaları göz önünde bulundurmak işe yarar:</p>
  <ul>
    <li><strong>Alış-satış farkı:</strong> Bozdurup daha sonra yeniden altın almak, yukarıdaki örnekteki gibi bir fark maliyeti doğurur.</li>
    <li><strong>Güvenli saklama:</strong> Evde saklanan altın hırsızlık ve kayıp riski taşır. Bazı bankalar fiziki altını altın hesabına kabul eder; koşulları ve kesintileri bankanızdan öğrenin.</li>
    <li><strong>Paranın ihtiyacı:</strong> Ev, eşya ya da borç kapatma gibi somut bir ihtiyaç varsa, bozdurulacak tutarı önceden hesaplamak kaç altının yeteceğini netleştirir.</li>
  </ul>
  <p>Altının yıllar içinde Türk lirası karşısındaki değerini, paranın değer kaybıyla karşılaştırmak için <a href="{B}/para-deger-kaybi-hesaplama.html">paranın değer kaybı hesaplama</a> aracını kullanabilirsiniz.</p>

  <h2>Kaynaklar</h2>
  <p style="font-size:.88rem">Gramajlar: Hazine ve Maliye Bakanlığı, “Sorularla Cumhuriyet Altını” (Darphane ziynet ve sikke ağırlıkları) · Fiyatlar: Kapalıçarşı piyasa fiyatları (Truncgil Finans), 29 Ekim 2026 09:50.</p>
'''
faq = [
    ('Düğünde takılan altınlar nasıl hesaplanır?', 'Her altın türünün adedi, o türün güncel fiyatıyla çarpılır; bilezikler için gram, 22 ayar gram fiyatıyla çarpılır. Bozdurmayı düşünüyorsanız kuyumcunun alış fiyatını esas alın. Altın hesaplama aracına adetleri girerek toplamı doğrudan görebilirsiniz.'),
    ('Çeyrek altın kaç gram?', 'Ziynet çeyrek altın 1,754 gram ve 22 ayardır; içinde yaklaşık 1,608 gram saf altın vardır.'),
    ('Altın bozdururken neden daha az para alırım?', 'Kuyumcunun sizden altın alırken ödediği alış fiyatı, size altın satarken istediği satış fiyatından düşüktür. Bilezik ve takılarda ayrıca işçilik bedeli geri ödenmez.'),
    ('Bilezik bozdururken işçilik geri alınır mı?', 'Hayır. Bilezik tartılır, ayarı kontrol edilir ve yalnızca altının gram değeri kuyumcunun alış fiyatından ödenir.'),
    ('Cumhuriyet altını mı tam altın mı daha değerli?', 'Cumhuriyet (Ata) altını 7,216 gram, tam ziynet altın 7,016 gramdır. İkisi de 22 ayar olduğu için Cumhuriyet altını biraz daha fazla altın içerir ve biraz daha pahalıdır.'),
]
rel = [('🪙', 'Altın Hesaplama', 'Canlı fiyatla altınların kaç TL?', f'{B}/altin-hesaplama.html'),
       ('💵', 'Para Sayma Hesaplama', 'Kaç tane 200 TL ne eder?', f'{B}/para-sayma-hesaplama.html'),
       ('📉', 'Paranın Değer Kaybı', 'Enflasyonla alım gücü', f'{B}/para-deger-kaybi-hesaplama.html'),
       ('💱', 'Döviz Çevirici', 'Dolar ve euro kaç TL?', f'{B}/doviz-cevirici.html')]
print(make('dugun-altini-rehberi',
     'Düğün Altını Hesaplama: Takılan Altınlar Ne Eder? | Hesaplarsın',
     f'Düğünde takılan çeyrek, yarım, tam altın ve bileziklerin değeri nasıl hesaplanır? Örnek: 15 çeyrek, 4 yarım, 2 tam ve 40 g bilezik ≈ {tl(AL, 0)} TL. Bozdururken dikkat.',
     'düğün altını hesaplama, takılan altınlar ne eder, altın bozdurma, çeyrek altın kaç gram, bilezik bozdurma, altın alış satış farkı',
     'Düğün Altını Rehberi', 'Düğün Altını Hesaplama: Takılan Altınlar Ne Eder, Bozdururken Nelere Dikkat Edilmeli?',
     hero('💍', 'Bozdururken alış fiyatı geçerli', 'ÇEYREK ALTIN – ALIŞ (29 EKİM)', t(F['ceyrek'][1]), 'ÖRNEK DÜĞÜN ALTINI (ALIŞ)', t(AL), '#78350f', '#d97706'),
     ['Altın', 'Rehber'], body, faq, rel, date='2026-10-29', date_tr='29 Ekim 2026'))
