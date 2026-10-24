"""blog/elektrik-faturasi-neden-yuksek yeniden yazımı (24 Ekim 2026 doğruluk denetimi). Repo kökünden: python3 _gen/blog_elektrik.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newpost import make, tl, table, hero
B = 'https://hesaplarsin.com'
E, D = 1000.0, 400.0          # varsayımsal enerji ve dağıtım bedeli
BTV = E * 0.05; KDV = (E + D + BTV) * 0.10; TOP = E + D + BTV + KDV
t = lambda x: tl(x, 2) + ' TL'
body = f'''
  <p class="lead">Elektrik faturası yalnızca tükettiğiniz kWh’in bedelinden oluşmaz: dağıtım bedeli, belediye tüketim vergisi ve KDV de eklenir. 2026’da faturaları en çok etkileyen değişiklik ise meskenler için yıllık tüketim sınırının <strong>5.000 kWh’ten 4.000 kWh’e</strong> düşürülmesi oldu. Bu yazıda faturanızdaki kalemleri, sınırı aşınca ne olduğunu ve faturayı düşürmenin yollarını bulacaksınız.</p>

  <div class="highlight-box">
    <p><strong>2026 Elektrik Faturası Özeti (mesken):</strong></p>
    <p>• Kalemler: aktif enerji bedeli + dağıtım bedeli + elektrik tüketim vergisi (BTV) + KDV</p>
    <p>• BTV: enerji bedelinin <strong>%5</strong>’i · KDV: <strong>%10</strong> (işyerlerinde %20)</p>
    <p>• TRT payı ve enerji fonu <strong>1 Ocak 2022’den beri faturada yok</strong></p>
    <p>• Yıllık tüketim sınırı: <strong>4.000 kWh</strong> (aylık ortalama ~333 kWh). Aşanlar sübvansiyonsuz son kaynak tarifesine geçer.</p>
  </div>

  <h2>Faturanızda Hangi Kalemler Var?</h2>
''' + table(['Kalem', 'Nasıl hesaplanır?', 'Not'], [
    ['Aktif enerji bedeli', 'Tüketim (kWh) × enerji birim fiyatı', 'Faturanın en büyük kalemi'],
    ['Dağıtım bedeli', 'Tüketim (kWh) × dağıtım birim fiyatı', 'Şebekenin bakım, işletme ve yatırım maliyeti'],
    ['Elektrik ve havagazı tüketim vergisi (BTV)', 'Enerji bedelinin %5’i (mesken)', 'Belediyelere aktarılır; dağıtım bedeline uygulanmaz'],
    ['KDV', '(Enerji + dağıtım + BTV) × %10', 'Mesken aboneleri; işyerlerinde %20'],
], 'Elektrik faturası kalemleri') + f'''
  <p>Birim fiyatlar EPDK tarafından belirlenir ve dönemsel olarak güncellenir. Güncel tarifeleri EPDK’nın tarife tablolarından görebilirsiniz.</p>

  <h2>Örnek: Fatura Nasıl Oluşur?</h2>
  <p>Kalemlerin birbirine etkisini görmek için enerji bedeli {t(E)}, dağıtım bedeli {t(D)} olan varsayımsal bir mesken faturası:</p>
''' + table(['Kalem', 'Hesap', 'Tutar'], [
    ['Aktif enerji bedeli', '—', t(E)], ['Dağıtım bedeli', '—', t(D)],
    ['BTV (%5)', f'{t(E)} × 0,05', t(BTV)], ['KDV (%10)', f'({t(E + D + BTV)}) × 0,10', t(KDV)],
    ['<strong>Toplam</strong>', '', '<strong>' + t(TOP) + '</strong>']], 'Örnek fatura') + f'''
  <p>Yani vergiler, enerji ve dağıtım bedelinin toplamına yaklaşık <strong>%{tl((BTV + KDV) / (E + D) * 100, 1)}</strong> ekler. Kendi faturanız için toplam tutarı tüketilen kWh’e bölerek vergiler dahil birim fiyatınızı bulabilir ve <a href="{B}/elektrik-faturasi-hesaplama.html">elektrik faturası hesaplama</a> aracıyla sonraki ayları tahmin edebilirsiniz.</p>

  <h2>Yıllık 4.000 kWh Sınırı: Aşarsanız Ne Olur?</h2>
  <p>Meskenlerde elektrik, devlet desteğiyle belirlenen ulusal tarifeden satılır. Ancak yıllık tüketimi belirli bir sınırı aşan aboneler bu desteğin dışında kalır ve <strong>son kaynak tedarik tarifesi (SKTT)</strong> ile faturalandırılır. SKTT’de elektrik sübvansiyonsuz, maliyete dayalı fiyattan satıldığı için birim fiyat belirgin şekilde yükselir.</p>
''' + table(['Yıl', 'Mesken yıllık sınırı', 'Aylık ortalama karşılığı'], [
    ['2025', '5.000 kWh', '~417 kWh'], ['2026', '4.000 kWh', '~333 kWh']], 'Yıllık tüketim sınırı') + f'''
  <p>Sınır, bir önceki yılın toplam tüketimine göre uygulanır: 2025’te 4.000 kWh’i aşan haneler 2026’da son kaynak tarifesinden faturalandırılabilir. Kalabalık aileler, elektrikle ısınan veya yazın yoğun klima kullanan haneler bu sınıra en hızlı ulaşanlardır. Yıllık tüketiminizi son 12 faturanızdaki kWh’leri toplayarak kontrol edebilirsiniz.</p>

  <h2>Elektrik Faturası Neden Yüksek Gelir?</h2>
  <ul>
    <li><strong>Mevsim etkisi:</strong> Kışın elektrikli ısıtıcı, yazın klima kullanımı tüketimi iki-üç katına çıkarabilir.</li>
    <li><strong>Fatura dönemi uzunluğu:</strong> Sayaç okuma aralığı 30 yerine 35 gün olursa tüketim de o kadar fazla görünür.</li>
    <li><strong>Tahmini okuma:</strong> Sayaç okunamadığında tahmini tüketim yazılır, sonraki gerçek okumada fark tek faturaya yansır.</li>
    <li><strong>Yıllık sınırın aşılması:</strong> Son kaynak tarifesine geçen hanelerde aynı tüketim çok daha pahalıya gelir.</li>
    <li><strong>Eski veya arızalı cihazlar:</strong> Eski buzdolapları, termosifonlar ve sürekli çalışan cihazlar fark edilmeden çok tüketir.</li>
  </ul>

  <h2>Faturanızı Düşürecek 8 Yöntem</h2>
  <ol>
    <li><strong>LED aydınlatma:</strong> LED ampuller akkor ampullere göre yaklaşık %80 daha az enerji harcar.</li>
    <li><strong>Üç zamanlı tarife:</strong> Çamaşır, bulaşık ve şarj işlerini gece saatlerine kaydırabiliyorsanız tedarikçinizden üç zamanlı tarifeye geçmeyi değerlendirin.</li>
    <li><strong>Bekleme modunu kapatın:</strong> TV, modem ve şarj aletleri beklemede de enerji çeker; anahtarlı priz kullanın.</li>
    <li><strong>Enerji etiketi:</strong> Yeni cihaz alırken yüksek verimlilik sınıfını seçin; buzdolabı gibi 7/24 çalışan cihazlarda fark büyüktür.</li>
    <li><strong>Buzdolabı ayarı:</strong> Buzdolabını 3–5 °C, dondurucuyu −18 °C’ye ayarlayın.</li>
    <li><strong>Tam yükle çalıştırın:</strong> Çamaşır ve bulaşık makinesini yarım dolu çalıştırmayın.</li>
    <li><strong>Klima bakımı:</strong> Kirli filtre tüketimi artırır; filtreleri düzenli temizleyin ve klimayı 24–26 °C’de kullanın.</li>
    <li><strong>Tüketimi takip edin:</strong> Cihazlarınızın aylık maliyetini <a href="{B}/elektrik-faturasi-hesaplama.html">elektrik faturası hesaplama</a> aracının cihaz bölümünde görebilirsiniz.</li>
  </ol>

  <h2>Kaynaklar</h2>
  <p style="font-size:.88rem">EPDK tarife tabloları ve 30 Ekim 2025 tarihli kararla belirlenen 2026 son kaynak tedarik limiti · 3065 sayılı KDV Kanunu ve indirimli oran kararları · 2464 sayılı Belediye Gelirleri Kanunu (elektrik ve havagazı tüketim vergisi).</p>
'''
faq = [
    ('Elektrikte KDV oranı 2026’da kaç?', 'Mesken (konut) abonelerinde elektrik KDV oranı %10’dur. İşyeri aboneliklerinde %20 uygulanır. KDV; enerji bedeli, dağıtım bedeli ve tüketim vergisinin toplamı üzerinden hesaplanır.'),
    ('Elektrik faturasında TRT payı var mı?', 'Hayır. TRT payı (%2) ve enerji fonu (%1) 1 Ocak 2022’den itibaren elektrik faturalarından kaldırıldı.'),
    ('Elektrik faturasında hangi kalemler var?', 'Mesken faturası aktif enerji bedeli, dağıtım bedeli, enerji bedelinin %5’i oranında elektrik tüketim vergisi (BTV) ve %10 KDV’den oluşur.'),
    ('Yıllık 4.000 kWh sınırı nedir?', '2026’da meskenler için yıllık elektrik tüketim sınırı 4.000 kWh’tir (2025’te 5.000 kWh). Bu sınırı aşan haneler devlet destekli tarifeden çıkarılıp son kaynak tedarik tarifesiyle, yani daha yüksek birim fiyatla faturalandırılabilir.'),
    ('Ayda kaç kWh elektrik normaldir?', 'Hane büyüklüğüne ve ısınma şekline göre değişir. Yıllık 4.000 kWh sınırı aylık ortalama yaklaşık 333 kWh’e denk gelir; bu seviyenin altında kalmak destekli tarifede kalmanızı sağlar.'),
]
rel = [('⚡', 'Elektrik Faturası Hesaplama', 'kWh ve cihaz bazlı maliyet', f'{B}/elektrik-faturasi-hesaplama.html'),
       ('🔥', 'Doğalgaz Faturası Hesaplama', 'm³ ve kWh ile fatura tahmini', f'{B}/dogalgaz-faturasi-hesaplama.html'),
       ('🧾', 'KDV Oranları 2026', 'Hangi üründe yüzde kaç?', f'{B}/blog/kdv-oranlari-2026.html'),
       ('💧', 'Su Faturası Hesaplama', 'Aylık su gideri', f'{B}/su-faturasi-hesaplama.html')]
print(make('elektrik-faturasi-neden-yuksek',
     'Elektrik Faturası Neden Yüksek? 2026 KDV, 4.000 kWh Sınırı ve Fatura Kalemleri | Hesaplarsın',
     'Elektrik faturası kalemleri 2026: mesken KDV %10, tüketim vergisi %5, TRT payı yok. Yıllık 4.000 kWh sınırını aşınca ne olur, fatura neden yüksek gelir, nasıl düşer?',
     'elektrik faturası neden yüksek, elektrik kdv oranı 2026, elektrik faturası kalemleri, 4000 kwh sınırı, son kaynak tedarik tarifesi, elektrik tüketim vergisi',
     'Elektrik Faturası Neden Yüksek?', 'Elektrik Faturası Neden Yüksek? 2026 Fatura Kalemleri, KDV ve 4.000 kWh Sınırı',
     hero('⚡', '2026 sınırı: 4.000 kWh/yıl', 'MESKEN KDV', '%10', 'TÜKETİM VERGİSİ (BTV)', '%5', '#0f307a', '#1a56db'),
     ['Enerji', 'Rehber'], body, faq, rel, date='2026-10-24', date_tr='24 Ekim 2026'))
