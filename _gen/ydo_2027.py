"""2027 yeniden değerleme paketi (3 blog). Kesin oran açıklanınca T değerini güncelleyip repo kökünden çalıştırın: python3 _gen/ydo_2027.py"""
import sys, math
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newpost import make, tl, table, hero
L, T = 0.20, 0.2781
fl = lambda x: math.floor(x)
def t0(x): return tl(x, 0) + ' TL'
def t2(x): return tl(x, 2) + ' TL'
B = 'https://hesaplarsin.com'
P = [('6 ay', 2806.50), ('1 yıl', 4103.00), ('2 yıl', 6698.50), ('3 yıl', 9516.00), ('3 yıldan fazla (10 yıl)', 13410.40)]
DEF = 1351.0
EH = [('A, A1, A2 (motosiklet)', 2239.90), ('B (otomobil)', 6754.60), ('F (traktör)', 11271.20)]
DK, VK = 1690.0, 425.0
YDC, IMEI = 1250.0, 54258.0
MTV = [('1300 cm³ ve altı', 5750), ('1301 – 1600 cm³', 10016), ('1601 – 1800 cm³', 19472), ('1801 – 2000 cm³', 30679)]

# ═══════════ 1) ANA YAZI ═══════════
body1 = f'''
  <p class="lead">Her yıl Kasım ayında açıklanan <strong>yeniden değerleme oranı</strong>, ertesi yıl ödenecek motorlu taşıtlar vergisinden pasaport ve ehliyet harçlarına, trafik cezalarından vergi istisnalarına kadar yüzlerce sabit tutarı belirler. 2027’de uygulanacak oran <strong>3 Kasım 2026</strong>’da TÜİK’in Ekim ayı üretici fiyatları verisiyle belli olacak. Bu yazıda oranın nasıl hesaplandığını, güncel tahmini ve 2027’de hangi kalemin ne kadar olacağını tek tabloda bulacaksınız.</p>

  <div class="highlight-box">
    <p><strong>Özet:</strong></p>
    <p>• Hesaplama: Yurt İçi Üretici Fiyat Endeksi’nin (Yİ-ÜFE) Ekim ayı yıllık değişimi</p>
    <p>• Açıklanma: TÜİK Ekim verisiyle <strong>3 Kasım 2026</strong>; ardından Hazine ve Maliye Bakanlığı tebliğiyle ilan edilir</p>
    <p>• Eylül 2026 Yİ-ÜFE yıllık değişimi: <strong>%27,81</strong> → oranın %26–%30 aralığında çıkması bekleniyor</p>
    <p>• Geçen yıl: oran %25,49 idi; MTV, harçlar ve damga vergisinde %18,95 uygulandı, cezalar ve vergi istisnaları tam oranla arttı</p>
  </div>

  <h2>Yeniden Değerleme Oranı Nedir, Nasıl Hesaplanır?</h2>
  <p>Vergi Usul Kanunu’nun mükerrer 298. maddesine göre yeniden değerleme oranı, <strong>Yİ-ÜFE’nin Ekim ayında bir önceki yılın aynı ayına göre değişimidir</strong>. Yani tüketici enflasyonu (TÜFE) değil, üretici fiyatları esas alınır. Oran Kasım ayında ilan edilir ve maktu (sabit tutarlı) vergi, harç ve cezalar ertesi yılın 1 Ocak’ından itibaren bu oranda artırılır.</p>
  <p>İdari para cezaları ise Kabahatler Kanunu’nun 17. maddesi uyarınca her takvim yılı başında yeniden değerleme oranında artırılır. Bu nedenle trafik cezaları, harçlar gibi indirimli artışa tabi tutulmaz ve genellikle tam oranla güncellenir.</p>

  <h2>2026 Yeniden Değerleme Oranı Tahmini</h2>
  <p>Yİ-ÜFE’nin yıllık değişimi Eylül 2026’da <strong>%27,81</strong> oldu. Ekim ayındaki aylık üretici enflasyonu geçen yılın Ekim ayına yakın gerçekleşirse oran bu seviyenin çevresinde, yani <strong>%26–%30 aralığında</strong> çıkacaktır. Aşağıdaki hesaplarda tam oran için %27,81’i, Cumhurbaşkanının geçen yılki gibi sınırlı artış belirleyeceği kalemler için %20’yi kullandık. Kesin oran 3 Kasım 2026’da açıklandığında bu sayfa güncellenecek.</p>

  <h2>2027’de Ne Ne Kadar Olacak? Toplu Tablo</h2>
  <p>2026’da geçerli tutarlar ve iki senaryoda 2027 tahmini:</p>
''' + table(['Kalem', '2026', '2027 – sınırlı artış (%20)', '2027 – tam oran (%27,81)'], [
    ['10 yıllık pasaport harcı', t2(P[4][1]), t0(fl(P[4][1] * (1 + L))), t0(fl(P[4][1] * (1 + T)))],
    ['B sınıfı ehliyet harcı', t2(EH[1][1]), t0(fl(EH[1][1] * (1 + L))), t0(fl(EH[1][1] * (1 + T)))],
    ['Yurt dışı çıkış harcı', t0(YDC), t0(fl(YDC * (1 + L))), t0(fl(YDC * (1 + T)))],
    ['IMEI kayıt (telefon) harcı', t0(IMEI), t0(fl(IMEI * (1 + L))), t0(fl(IMEI * (1 + T)))],
    ['MTV – 1.301–1.600 cm³, 1–3 yaş', t0(10016), t0(fl(10016 * (1 + L))), t0(fl(10016 * (1 + T)))],
    ['Kırmızı ışık cezası (ilk ihlal)', t0(5000), '—', t0(fl(5000 * (1 + T)))],
    ['Alkollü araç kullanma (ilk tespit)', t0(25000), '—', t0(fl(25000 * (1 + T)))],
    ['Seyir halinde cep telefonu (ilk ihlal)', t0(5000), '—', t0(fl(5000 * (1 + T)))],
    ['Konut kira geliri istisnası', t0(58000), '—', 'yaklaşık ' + t0(fl(58000 * (1 + T) / 1000) * 1000)],
    ['Değer artış kazancı istisnası', t0(150000), '—', 'yaklaşık ' + t0(fl(150000 * (1 + T) / 1000) * 1000)],
], 'Yeniden değerleme ile 2027 tutarları') + f'''
  <p>Harçlar ve MTV için iki senaryo verdik; çünkü bu kalemlerde Cumhurbaşkanı oranı düşürebiliyor. Trafik cezaları ve vergi istisnalarında geçmiş uygulama tam oranla artış yönünde olduğu için tek senaryo gösterdik. Vergi kanunlarındaki istisna ve hadler genellikle aşağı yuvarlanarak ilan edildiğinden “yaklaşık” ifadesini kullandık.</p>

  <h2>Kalem Kalem Ayrıntılı Rehberler</h2>
  <p>Her başlığın 2026 tutarlarını ve 2027 tahminlerini ayrıntılı tablolarla ayrı sayfalarda hazırladık:</p>
  <ul>
    <li><a href="{B}/mtv-hesaplama.html"><strong>MTV hesaplama (2026 + 2027 tahmini)</strong></a>: Aracınızın motor hacmi, yaşı ve değerine göre 2026 MTV’si ve iki senaryoda 2027 tutarı.</li>
    <li><a href="{B}/blog/pasaport-ehliyet-harci-2027.html"><strong>2027 pasaport, ehliyet, yurt dışı çıkış ve IMEI harçları</strong></a>: Süre ve sınıflara göre toplam ödenecek tutarlar.</li>
    <li><a href="{B}/blog/trafik-cezalari-2027.html"><strong>2027 trafik cezaları</strong></a>: Hız, kırmızı ışık, alkol, cep telefonu ve diğer cezaların tahmini yeni tutarları.</li>
    <li><a href="{B}/blog/vergi-dilimleri-2027.html"><strong>2027 gelir vergisi dilimleri</strong></a>: Dilim tutarlarının yeni yılda nasıl değişeceği.</li>
  </ul>

  <h2>Neden Bazı Kalemler Daha Az Artıyor?</h2>
  <p>Kanun, Cumhurbaşkanına MTV, harçlar ve damga vergisi gibi kalemlerde yeniden değerleme oranını uygulamama ya da daha düşük bir oran belirleme yetkisi verir. Nitekim 2025 için hesaplanan oran %25,49 olmasına rağmen 31 Aralık 2025’te yayımlanan kararla bu kalemler 2026’da <strong>%18,95</strong> artırıldı. Örneğin 10 yıllık pasaport harcı 11.274 TL’den 13.410,40 TL’ye, B sınıfı ehliyet harcı 5.678 TL’den 6.754,60 TL’ye yükseldi. Bu karar genellikle yılın son günlerinde açıklandığı için kesin 2027 tutarları da Aralık sonunda netleşecek.</p>

  <h2>Yeniden Değerleme Oranı ile Enflasyon Arasındaki Fark</h2>
  <p>Kira artışı ve emekli zammı TÜFE’ye (tüketici fiyatları), yeniden değerleme oranı ise Yİ-ÜFE’ye (üretici fiyatları) bağlıdır. Eylül 2026’da yıllık TÜFE %29,73, yıllık Yİ-ÜFE %27,81 oldu. Bu nedenle vergi ve harçlardaki artış, maaş ve kira artışlarından farklı çıkabilir. Kira artış sınırını <a href="{B}/kira-artis-hesaplama.html">kira artış hesaplama</a>, maaşınızın enflasyon karşısındaki durumunu <a href="{B}/enflasyon-hesaplama.html">enflasyon hesaplama</a> aracıyla görebilirsiniz.</p>

  <h2>Şirketler İçin Yeniden Değerleme</h2>
  <p>Aynı oran, bilanço esasına göre defter tutan işletmelerin amortismana tabi iktisadi kıymetlerini yeniden değerlemesinde de kullanılır. Varlıkların net değeri bu oranla artırılır ve oluşan fark özkaynakta değer artış fonu olarak izlenir. Amortisman hesaplarınız için <a href="{B}/amortisman-hesaplama.html">amortisman hesaplama</a> aracını kullanabilirsiniz.</p>

  <h2>Kaynaklar</h2>
  <p style="font-size:.88rem">213 sayılı Vergi Usul Kanunu mükerrer 298. madde · 5326 sayılı Kabahatler Kanunu 17. madde · TÜİK Yurt İçi Üretici Fiyat Endeksi (Eylül 2026) · 31 Aralık 2025 tarihli Resmî Gazete (10783 sayılı Cumhurbaşkanı Kararı ve 98 Seri No’lu Harçlar Kanunu Genel Tebliği) · 7574 sayılı Kanun (Resmî Gazete, 27 Şubat 2026).</p>
'''
faq1 = [
    ('2026 yeniden değerleme oranı ne zaman açıklanacak?', 'Oran, TÜİK’in 3 Kasım 2026’da açıklayacağı Ekim ayı Yİ-ÜFE verisiyle belli olur; Hazine ve Maliye Bakanlığı ardından tebliğle ilan eder. Bu oran 1 Ocak 2027’den itibaren uygulanır.'),
    ('2026 yeniden değerleme oranı kaç olacak?', 'Eylül 2026’da Yİ-ÜFE yıllık değişimi %27,81 oldu. Ekim verisine bağlı olarak oranın %26–%30 aralığında çıkması bekleniyor.'),
    ('Yeniden değerleme oranı nasıl hesaplanır?', 'Vergi Usul Kanunu mükerrer 298. maddeye göre Yurt İçi Üretici Fiyat Endeksi’nin Ekim ayındaki yıllık değişim oranıdır. TÜFE değil, üretici fiyatları esas alınır.'),
    ('2027’de pasaport ve ehliyet ne kadar olacak?', f'Harçlar %20 artırılırsa 10 yıllık pasaport harcı yaklaşık {t0(fl(P[4][1]*1.2))}, B sınıfı ehliyet harcı yaklaşık {t0(fl(EH[1][1]*1.2))} olur. Tam oran (%27,81) uygulanırsa bu tutarlar {t0(fl(P[4][1]*(1+T)))} ve {t0(fl(EH[1][1]*(1+T)))} olur.'),
    ('Trafik cezaları 2027’de ne kadar artacak?', 'İdari para cezaları Kabahatler Kanunu gereği her yıl yeniden değerleme oranında artırılır. Oran %27,81 civarında çıkarsa 5.000 TL’lik kırmızı ışık cezası yaklaşık 6.390 TL’ye yükselir.'),
    ('Yeniden değerleme oranı maaşları etkiler mi?', 'Doğrudan etkilemez; maaş, emekli aylığı ve kira artışları TÜFE’ye bağlıdır. Ancak gelir vergisi dilimleri bu oranla güncellendiği için net maaşı dolaylı olarak etkiler.'),
]
rel1 = [('🚗', 'MTV Hesaplama', '2026 MTV ve 2027 tahmini', f'{B}/mtv-hesaplama.html'),
        ('🛂', '2027 Pasaport ve Ehliyet Harçları', 'Süre ve sınıfa göre tutarlar', f'{B}/blog/pasaport-ehliyet-harci-2027.html'),
        ('🚦', '2027 Trafik Cezaları', 'Hız, alkol, kırmızı ışık', f'{B}/blog/trafik-cezalari-2027.html'),
        ('📊', 'Vergi Dilimleri 2027', 'Gelir vergisi tarifesi tahmini', f'{B}/blog/vergi-dilimleri-2027.html')]
print(make('yeniden-degerleme-orani-2026',
     'Yeniden Değerleme Oranı 2026: 2027 MTV, Harç ve Cezalar | Hesaplarsın',
     'Yeniden değerleme oranı 3 Kasım 2026’da belli olacak (Eylül Yİ-ÜFE %27,81). 2027 MTV, harç, trafik cezası ve vergi istisnası tahminleri tek tabloda.',
     'yeniden değerleme oranı 2026, yeniden değerleme oranı 2027, 2027 mtv, 2027 harçlar, 2027 trafik cezaları, yİ-üfe ekim 2026',
     'Yeniden Değerleme Oranı 2026', 'Yeniden Değerleme Oranı 2026: 2027’de MTV, Harçlar ve Cezalar Ne Kadar Olacak?',
     hero('📈', '3 Kasım 2026’da açıklanacak', 'EYLÜL Yİ-ÜFE (YILLIK)', '%27,81', '2027 TAHMİNİ ARALIK', '%26 – %30', '#7c2d12', '#ea580c'),
     ['Vergi', 'Gündem'], body1, faq1, rel1, date='2026-10-24', date_tr='24 Ekim 2026'))

# ═══════════ 2) PASAPORT / EHLİYET ═══════════
body2 = f'''
  <p class="lead">Pasaport, ehliyet, yurt dışı çıkış ve yurt dışından getirilen telefonların IMEI kayıt harçları her yıl yeniden değerleme oranına bağlı olarak artırılır. 2027 tutarları, 3 Kasım 2026’da açıklanacak oran ve Aralık sonunda yayımlanacak Cumhurbaşkanı kararıyla netleşecek. Bu yazıda <strong>2026’da ödenen tutarları</strong> ve iki senaryoda <strong>2027 tahminlerini</strong> bulacaksınız.</p>

  <div class="highlight-box">
    <p><strong>Kısaca:</strong></p>
    <p>• 2026’da 10 yıllık pasaport: {t2(P[4][1])} harç + {t2(DEF)} defter = <strong>{t2(P[4][1] + DEF)}</strong></p>
    <p>• 2026’da B sınıfı ehliyet: {t2(EH[1][1])} harç + {t0(DK)} kart + {t0(VK)} vakıf payı = <strong>{t2(EH[1][1] + DK + VK)}</strong></p>
    <p>• 2026’da harçlar %18,95 arttı. 2027’de artışın %20 ile %27,81 arasında olması bekleniyor.</p>
    <p>• İşlemini yıl sonuna kadar tamamlayanlar 2026 tarifesinden öder.</p>
  </div>

  <h2>2026 Pasaport Ücretleri</h2>
''' + table(['Pasaport süresi', 'Harç', 'Defter bedeli', 'Toplam'], [[a, t2(b), t2(DEF), t2(b + DEF)] for a, b in P], '2026 pasaport ücretleri') + f'''
  <p>Tutarlar umuma mahsus (bordo) pasaport içindir. Harç vergi dairesine, bankalara veya online olarak; defter bedeli Nüfus Müdürlüğüne ödenir. Başvuru öncesi Nüfus ve Vatandaşlık İşleri Genel Müdürlüğü’nün güncel ücret sayfasını kontrol edin.</p>

  <h2>2027 Pasaport Ücreti Ne Kadar Olacak?</h2>
''' + table(['Pasaport süresi', '2027 – %20 artışla (toplam)', '2027 – %27,81 artışla (toplam)'],
            [[a, t0(fl(b * (1 + L)) + DEF), t0(fl(b * (1 + T)) + DEF)] for a, b in P], '2027 pasaport tahmini') + f'''
  <p>Tablodaki toplamlarda defter bedeli 2026 tutarıyla ({t2(DEF)}) sabit varsayılmıştır; defter bedeli ayrıca belirlendiği için 2027’de değişebilir.</p>

  <h2>2026 Ehliyet (Sürücü Belgesi) Ücretleri</h2>
''' + table(['Sınıf', 'Harç', 'Kart (değerli kağıt) bedeli', 'Vakıf payı', 'Toplam'],
            [[a, t2(b), t0(DK), t0(VK), t2(b + DK + VK)] for a, b in EH], '2026 ehliyet ücretleri') + f'''
  <p>Kurs ve sınav ücretleri bu tutarlara dahil değildir. Diğer sınıflardaki harç tutarları için Nüfus Müdürlüğü ücret tablosuna bakılmalıdır.</p>

  <h2>2027 Ehliyet Ücreti Ne Kadar Olacak?</h2>
''' + table(['Sınıf', '2027 harç – %20', '2027 harç – %27,81', 'Tahmini toplam (kart ve vakıf payı dahil)'],
            [[a, t0(fl(b * (1 + L))), t0(fl(b * (1 + T))), t0(fl(b * (1 + L)) + DK + VK) + ' – ' + t0(fl(b * (1 + T)) + DK + VK)] for a, b in EH], '2027 ehliyet tahmini') + f'''
  <p>Kart bedeli ve vakıf payı 2026 tutarlarıyla sabit varsayılmıştır.</p>

  <h2>Yurt Dışı Çıkış Harcı 2027</h2>
  <p>Yurt dışına çıkan Türk vatandaşlarından alınan yurt dışı çıkış harcı 1 Ocak 2026’dan itibaren <strong>{t0(YDC)}</strong> olarak uygulanıyor (2025’te 1.000 TL’ydi). Bu harç Cumhurbaşkanı kararıyla belirlendiği için diğer harçlardan farklı oranda artırılabilir. Yeniden değerleme oranına paralel bir artışta 2027 tutarı yaklaşık <strong>{t0(fl(YDC * (1 + L)))} – {t0(fl(YDC * (1 + T)))}</strong> aralığında olur.</p>

  <h2>IMEI Kayıt Harcı 2027</h2>
  <p>Yurt dışından getirilen cep telefonlarının Türkiye’de kullanılabilmesi için ödenen IMEI kayıt (kullanım izni) harcı 2026’da <strong>{t0(IMEI)}</strong>. 2027’de %20 artışla yaklaşık <strong>{t0(fl(IMEI * (1 + L)))}</strong>, tam oranla yaklaşık <strong>{t0(fl(IMEI * (1 + T)))}</strong> olması bekleniyor. Telefonu yıl sonundan önce kaydettirenler 2026 tutarını öder.</p>

  <h2>Zamdan Önce İşlem Yapmak Mantıklı mı?</h2>
  <p>Harçlar 1 Ocak’ta artacağı için pasaport veya ehliyet işlemini zaten planlıyorsanız Aralık sonuna kadar tamamlamak, 10 yıllık pasaportta {t0(fl(P[4][1] * L))} ile {t0(fl(P[4][1] * T))} arasında tasarruf sağlayabilir. Randevuların yıl sonunda yoğunlaştığını göz önünde bulundurup erkenden randevu alın.</p>
  <p>Diğer kalemlerdeki 2027 artışlarını <a href="{B}/blog/yeniden-degerleme-orani-2026.html">yeniden değerleme oranı rehberinde</a>, aracınızın 2027 vergisini <a href="{B}/mtv-hesaplama.html">MTV hesaplama</a> aracında görebilirsiniz.</p>

  <h2>Kaynaklar</h2>
  <p style="font-size:.88rem">492 sayılı Harçlar Kanunu ve 98 Seri No’lu Harçlar Kanunu Genel Tebliği (Resmî Gazete, 31 Aralık 2025) · 10783 sayılı Cumhurbaşkanı Kararı (%18,95 artış) · Yurt Dışına Çıkış Harcı Uygulama Genel Tebliği değişikliği (31 Aralık 2025) · Nüfus ve Vatandaşlık İşleri Genel Müdürlüğü ücret tabloları.</p>
'''
faq2 = [
    ('2026’da 10 yıllık pasaport ne kadar?', f'Harç {t2(P[4][1])}, defter bedeli {t2(DEF)} olmak üzere toplam {t2(P[4][1] + DEF)}.'),
    ('2027’de pasaport ne kadar olacak?', f'Harçlar %20 artırılırsa 10 yıllık pasaportun toplam maliyeti yaklaşık {t0(fl(P[4][1]*1.2)+DEF)}, tam oranla (%27,81) yaklaşık {t0(fl(P[4][1]*(1+T))+DEF)} olur. Kesin tutar Aralık sonunda belli olur.'),
    ('2026’da B sınıfı ehliyet ücreti ne kadar?', f'Harç {t2(EH[1][1])}, kart bedeli {t0(DK)} ve vakıf payı {t0(VK)} ile toplam {t2(EH[1][1]+DK+VK)}. Kurs ve sınav ücretleri hariçtir.'),
    ('2027’de ehliyet harcı ne kadar olacak?', f'B sınıfı ehliyet harcının %20 artışla yaklaşık {t0(fl(EH[1][1]*1.2))}, tam oranla yaklaşık {t0(fl(EH[1][1]*(1+T)))} olması bekleniyor.'),
    ('2027 IMEI kayıt ücreti ne kadar olacak?', f'2026’da {t0(IMEI)} olan IMEI kayıt harcının 2027’de {t0(fl(IMEI*1.2))} ile {t0(fl(IMEI*(1+T)))} arasında olması bekleniyor.'),
    ('Yurt dışı çıkış harcı 2027’de ne kadar?', f'2026’da {t0(YDC)}. Yeniden değerleme oranına paralel bir artışta 2027’de yaklaşık {t0(fl(YDC*1.2))} – {t0(fl(YDC*(1+T)))} aralığında olur.'),
]
rel2 = [('📈', 'Yeniden Değerleme Oranı 2026', '2027’de neler ne kadar artacak?', f'{B}/blog/yeniden-degerleme-orani-2026.html'),
        ('🚦', '2027 Trafik Cezaları', 'Tahmini yeni ceza tutarları', f'{B}/blog/trafik-cezalari-2027.html'),
        ('🚗', 'MTV Hesaplama', '2026 MTV ve 2027 tahmini', f'{B}/mtv-hesaplama.html'),
        ('💱', 'Döviz Çevirici', 'Seyahat öncesi kur hesabı', f'{B}/doviz-cevirici.html')]
print(make('pasaport-ehliyet-harci-2027',
     '2027 Pasaport Ücretleri: 10 Yıllık Pasaport Ne Kadar Olacak? | Hesaplarsın',
     f'2027 pasaport ücretleri tahmini: 10 yıllık pasaport {t0(fl(P[4][1]*(1+L))+DEF)} – {t0(fl(P[4][1]*(1+T))+DEF)}, 1 yıllık {t0(fl(P[1][1]*(1+L))+DEF)} – {t0(fl(P[1][1]*(1+T))+DEF)}. 2026 tarifesi, ehliyet ve yurt dışı çıkış harcı tablolarla.',
     '2027 pasaport harcı, 2027 ehliyet harcı, pasaport ücreti 2027, ehliyet ücreti 2027, yurt dışı çıkış harcı 2027, imei kayıt ücreti 2027',
     '2027 Pasaport ve Ehliyet Harçları', '2027 Pasaport Ücretleri ve Ehliyet Harcı Ne Kadar Olacak? Yurt Dışı Çıkış ve IMEI',
     hero('🛂', 'Ocak 2027’de zamlanıyor', '10 YILLIK PASAPORT (2026)', t2(P[4][1] + DEF), 'B SINIFI EHLİYET (2026)', t2(EH[1][1] + DK + VK), '#7c2d12', '#ea580c'),
     ['Vergi', 'Harçlar'], body2, faq2, rel2, date='2026-10-24', date_tr='24 Ekim 2026'))

# ═══════════ 3) TRAFİK CEZALARI ═══════════
er = lambda x: x * 0.75
def satir(a, x, ek=''):
    y = fl(x * (1 + T))
    return [a, t0(x), t0(y), t0(fl(er(y))), ek]
HIZ = [('6–10 km/s', 2000, ''), ('11–15 km/s', 4000, ''), ('16–20 km/s', 6000, ''), ('21–25 km/s', 8000, ''), ('26–35 km/s', 12000, ''),
       ('36–45 km/s', 15000, ''), ('46–55 km/s', 20000, '30 gün ehliyet'), ('56–65 km/s', 25000, '60 gün ehliyet'), ('66 km/s ve üzeri', 30000, '90 gün ehliyet')]
KI = [('1. ihlal', 5000, ''), ('2. ihlal', 10000, ''), ('3. ihlal', 15000, '30 gün ehliyet'), ('4. ihlal', 20000, '60 gün ehliyet'), ('5. ihlal', 30000, '90 gün ehliyet'), ('6. ihlal', 80000, 'Ehliyet iptali')]
AL = [('İlk tespit (0,50 promil üzeri)', 25000, '6 ay ehliyet'), ('5 yıl içinde 2. tespit', 50000, '2 yıl ehliyet'), ('5 yıl içinde 3. ve sonrası', 150000, '5 yıl ehliyet'), ('Alkol testini reddetme', 150000, '5 yıl ehliyet')]
DG = [('Seyir halinde cep telefonu (1. ihlal)', 5000, ''), ('Cep telefonu (1 yıl içinde 2. ihlal)', 10000, ''), ('Cep telefonu (3. ve sonrası)', 20000, '30 gün ehliyet'),
      ('Emniyet kemeri takmama (sürücü)', 2500, ''), ('Çocuğu koruyucu sistem olmadan taşıma', 5000, ''), ('Ehliyetsiz araç kullanma', 40000, ''),
      ('Geri alınmış/iptal ehliyetle araç kullanma', 200000, ''), ('Emniyet şeridi ihlali', 11631, ''), ('Dur ihtarına uymayıp kaçma', 200000, '60 gün ehliyet'),
      ('Araçta radar tespit cihazı bulundurma', 185000, '')]
H = ['İhlal', '2026', '2027 tahmini', '2027 erken ödeme (%25 indirimli)', 'Ek yaptırım']
body3 = f'''
  <p class="lead">Trafik cezaları 27 Şubat 2026’da Resmî Gazete’de yayımlanan <strong>7574 sayılı Kanun</strong> ile baştan belirlendi; hız, kırmızı ışık, alkol ve cep telefonu cezaları kat kat arttı. İdari para cezaları Kabahatler Kanunu gereği her yıl başında <strong>yeniden değerleme oranında</strong> güncellendiği için bu tutarların 1 Ocak 2027’de bir kez daha artması bekleniyor. Bu yazıda 2026 tutarlarını ve oranın %27,81 civarında çıkması halinde 2027 tahminlerini bulacaksınız.</p>

  <div class="highlight-box">
    <p><strong>Kısaca:</strong></p>
    <p>• 2027 artışını belirleyecek yeniden değerleme oranı <strong>3 Kasım 2026</strong>’da belli olacak (Eylül itibarıyla %27,81).</p>
    <p>• Kırmızı ışık ve cep telefonu cezası 5.000 TL’den yaklaşık <strong>{t0(fl(5000*(1+T)))}</strong>’ye çıkabilir.</p>
    <p>• Alkollü araç kullanmanın ilk cezası 25.000 TL’den yaklaşık <strong>{t0(fl(25000*(1+T)))}</strong>’ye yükselebilir.</p>
    <p>• Ceza tebliğden itibaren 15 gün içinde ödenirse <strong>%25 indirim</strong> uygulanır.</p>
  </div>

  <h2>Hız Cezaları 2027 (Yerleşim Yeri İçi)</h2>
''' + table(H, [satir(a, x, e) for a, x, e in HIZ], 'Hız cezaları') + f'''
  <p>Aşım miktarı, hız sınırının ne kadar üzerinde gidildiğine göre hesaplanır. Yerleşim yeri dışında aynı tutarlar daha yüksek aşım eşiklerinde uygulanır; örneğin yerleşim dışında ilk kademe 11–15 km/s aşımdır.</p>

  <h2>Kırmızı Işık Cezası 2027</h2>
''' + table(H, [satir(a, x, e) for a, x, e in KI], 'Kırmızı ışık cezaları') + f'''
  <p>Tekrarlar bir yıllık süre içinde sayılır. Altıncı ihlalde sürücü belgesi iptal edilir.</p>

  <h2>Alkollü Araç Kullanma Cezası 2027</h2>
''' + table(H, [satir(a, x, e) for a, x, e in AL], 'Alkol cezaları') + f'''
  <p>Uyuşturucu veya uyarıcı madde etkisinde araç kullanmanın cezası da 150.000 TL’dir ve sürücü belgesi iptal edilir.</p>

  <h2>Cep Telefonu, Emniyet Kemeri ve Diğer Cezalar</h2>
''' + table(H, [satir(a, x, e) for a, x, e in DG], 'Diğer trafik cezaları') + f'''

  <h2>2027 Tutarları Nasıl Hesaplanıyor?</h2>
  <p>5326 sayılı Kabahatler Kanunu’nun 17. maddesine göre idari para cezaları her takvim yılı başında, o yıl için belirlenen yeniden değerleme oranında artırılarak uygulanır. Tablolardaki 2027 tahminleri, Eylül 2026 itibarıyla hesaplanan <strong>%27,81</strong> oranıyla ve küsuratlar atılarak hesaplanmıştır. Oran Ekim verisiyle %26 ile %30 arasında çıkarsa tutarlar buna göre birkaç yüz lira değişebilir. Örneğin 5.000 TL’lik bir ceza %26 artışla {t0(5000*1.26)}, %30 artışla {t0(5000*1.30)} olur.</p>
  <p>Geçen yıl da aynı yöntem uygulandı: 2025’te 993 TL olan hatalı park cezası, 2026’da %25,49 oranıyla 1.246 TL’ye yükseldi. 7574 sayılı Kanun’la belirlenen yeni tutarların 2027’de ilk kez bu kurala göre güncellenmesi bekleniyor; kesin liste Ocak başında Emniyet Genel Müdürlüğü tarafından yayımlanır ve bu sayfa güncellenir.</p>

  <h2>Erken Ödeme İndirimi ve İtiraz</h2>
  <ul>
    <li><strong>Erken ödeme:</strong> Ceza tebliğden itibaren 15 gün içinde ödenirse cezanın dörtte biri (%25) indirilir (Kabahatler Kanunu m.17/6). İndirimli ödeme, itiraz hakkını ortadan kaldırmaz. 6.390 TL’lik bir ceza erken ödemede 4.792,50 TL olur.</li>
    <li><strong>İtiraz:</strong> Tebliğden itibaren 15 gün içinde sulh ceza hâkimliğine itiraz edilebilir.</li>
    <li><strong>Sorgulama:</strong> Cezalarınızı e-Devlet’teki “Araca Yazılan Trafik Cezası Sorgulama” ve “Sürücü Ceza Puanı Sorgulama” hizmetlerinden görebilirsiniz.</li>
  </ul>
  <p>Diğer 2027 artışlarını <a href="{B}/blog/yeniden-degerleme-orani-2026.html">yeniden değerleme oranı rehberinde</a>, aracınızın 2027 vergisini <a href="{B}/mtv-hesaplama.html">MTV hesaplama</a> aracında, gecikmiş muayene cezasını <a href="{B}/arac-muayene-gecikme-hesaplama.html">araç muayene gecikme cezası hesaplama</a> aracında bulabilirsiniz.</p>

  <h2>Kaynaklar</h2>
  <p style="font-size:.88rem">2918 sayılı Karayolları Trafik Kanunu ve 7574 sayılı Kanun (Resmî Gazete, 27 Şubat 2026) · 5326 sayılı Kabahatler Kanunu 17. madde · TÜİK Yİ-ÜFE (Eylül 2026). Yeni yılın kesin tutarları için Emniyet Genel Müdürlüğü duyurusu esas alınmalıdır.</p>
'''
faq3 = [
    ('2027 trafik cezaları ne kadar artacak?', 'İdari para cezaları her yıl yeniden değerleme oranında artırılır. 3 Kasım 2026’da açıklanacak oran Eylül verisine göre %27,81 civarındadır; bu durumda cezalar yaklaşık %28 artar.'),
    ('2027’de kırmızı ışık cezası ne kadar olacak?', f'2026’da ilk ihlal için 5.000 TL olan kırmızı ışık cezasının 2027’de yaklaşık {t0(fl(5000*(1+T)))} olması bekleniyor; erken ödemede yaklaşık {t0(fl(er(fl(5000*(1+T)))))}.'),
    ('2027’de alkol cezası ne kadar olacak?', f'İlk tespitte 25.000 TL olan ceza yaklaşık {t0(fl(25000*(1+T)))}, 5 yıl içinde ikinci tespitte 50.000 TL olan ceza yaklaşık {t0(fl(50000*(1+T)))} olabilir.'),
    ('2027 hız cezası ne kadar?', f'Yerleşim yeri içinde 6–10 km/s aşımın cezası 2.000 TL’den yaklaşık {t0(fl(2000*(1+T)))}’ye, 66 km/s ve üzeri aşımın cezası 30.000 TL’den yaklaşık {t0(fl(30000*(1+T)))}’ye çıkabilir.'),
    ('Trafik cezasında erken ödeme indirimi var mı?', 'Evet. Tebliğden itibaren 15 gün içinde ödenen trafik cezalarında %25 indirim uygulanır.'),
    ('2026’da kesilen ceza 2027’de ödenirse artar mı?', 'Hayır. Ceza, ihlalin yapıldığı tarihteki tutar üzerinden kesilir; ödemenin 2027’ye kalması tutarı değiştirmez. Ancak süresinde ödenmeyen cezalara gecikme zammı eklenir.'),
]
rel3 = [('📈', 'Yeniden Değerleme Oranı 2026', '2027’de neler ne kadar artacak?', f'{B}/blog/yeniden-degerleme-orani-2026.html'),
        ('🚗', 'MTV Hesaplama', '2026 MTV ve 2027 tahmini', f'{B}/mtv-hesaplama.html'),
        ('🛂', '2027 Pasaport ve Ehliyet Harçları', 'Süre ve sınıfa göre tutarlar', f'{B}/blog/pasaport-ehliyet-harci-2027.html'),
        ('🔧', 'Araç Muayene Gecikme Cezası', 'Gecikme süresine göre ceza', f'{B}/arac-muayene-gecikme-hesaplama.html')]
print(make('trafik-cezalari-2027',
     '2027 Trafik Cezaları Ne Kadar Olacak? Hız, Alkol, Kırmızı Işık | Hesaplarsın',
     '2027 trafik cezaları tahmini: kırmızı ışık ve cep telefonu ≈ 6.390 TL, alkol ≈ 31.952 TL. Hız cezaları ve erken ödeme indirimli tutarlar tablolarla.',
     '2027 trafik cezaları, trafik cezaları 2027, 2027 hız cezası, 2027 kırmızı ışık cezası, 2027 alkol cezası, trafik cezası ne kadar',
     '2027 Trafik Cezaları', '2027 Trafik Cezaları Ne Kadar Olacak? Hız, Kırmızı Işık, Alkol ve Diğer Cezalar',
     hero('🚦', 'Ocak 2027’de güncelleniyor', 'KIRMIZI IŞIK (2027 TAHMİNİ)', t0(fl(5000 * (1 + T))), 'ALKOL – İLK TESPİT', t0(fl(25000 * (1 + T))), '#7f1d1d', '#dc2626'),
     ['Gündem', 'Trafik'], body3, faq3, rel3, date='2026-10-24', date_tr='24 Ekim 2026'))

# ═══════════ 4) VERGİ DİLİMLERİ 2027 ═══════════
U26 = [190000, 400000, 1500000, 5300000]       # ücret
D26 = [190000, 400000, 1000000, 5300000]       # ücret dışı
U25 = [158000, 330000, 1200000, 4300000]
OR = ['%15', '%20', '%27', '%35', '%40']
def kes(x): return fl(x / 1000) * 1000
def gv(m, d=U26):
    o = [.15, .20, .27, .35, .40]; v = 0; prev = 0
    for i, lim in enumerate(d + [10**12]):
        if m <= prev: break
        v += (min(m, lim) - prev) * o[i]; prev = lim
    return v
def satirlar(d):
    r = []; prev = 0
    for i, lim in enumerate(d):
        r.append([OR[i], f'{t0(prev)} – {t0(lim)}' if prev else f'0 – {t0(lim)}']); prev = lim
    r.append([OR[4], t0(prev) + ' üzeri'])
    return r
tarife = table(['Oran', 'Ücret gelirleri (2026)', 'Ücret dışı gelirler (2026)'],
               [[a[0], a[1], b[1]] for a, b in zip(satirlar(U26), satirlar(D26))], '2026 gelir vergisi tarifesi')
t27 = table(['Dilim üst sınırı (ücret)', '2026', '2027 – %20 artışla', '2027 – %27,81 artışla'],
            [[f'{OR[i]} dilimi', t0(x), t0(kes(x * 1.20)), t0(kes(x * (1 + T)))] for i, x in enumerate(U26)], '2027 vergi dilimi tahmini')
ORN = 600000
def ay_gecis(brut, sinir):
    m = brut * 0.85
    for ay in range(1, 13):
        if m * ay > sinir: return ay
    return None
AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
gecis = table(['Aylık brüt ücret', 'Aylık vergi matrahı', '%20 dilimine geçiş', '%27 dilimine geçiş'],
              [[t0(b), t0(b * 0.85)] + [(AYLAR[ay_gecis(b, s) - 1] if ay_gecis(b, s) else 'Yıl içinde geçmez') for s in (190000, 400000)] for b in (40000, 50000, 60000, 75000, 100000, 150000)],
              'Dilim geçiş ayları')
body4 = f'''
  <p class="lead">Türkiye’de gelir vergisi artan oranlıdır: kazancınızın her dilime düşen kısmı o dilimin oranıyla vergilendirilir. Dilim sınırları her yıl güncellenir ve 2027 tarifesi, 3 Kasım 2026’da belli olacak <strong>yeniden değerleme oranı</strong> esas alınarak Aralık sonunda ilan edilecek. Bu yazıda <strong>2026’da geçerli dilimleri</strong>, <strong>2027 tahminini</strong> ve maaşınızın yılın hangi ayında üst dilime geçeceğini bulacaksınız.</p>

  <div class="highlight-box">
    <p><strong>2026 Gelir Vergisi Dilimleri (Ücret):</strong></p>
    <p>• %15 → 0 – 190.000 TL</p>
    <p>• %20 → 190.000 – 400.000 TL</p>
    <p>• %27 → 400.000 – 1.500.000 TL (ücret dışı gelirlerde 1.000.000 TL’ye kadar)</p>
    <p>• %35 → 1.500.000 – 5.300.000 TL</p>
    <p>• %40 → 5.300.000 TL üzeri</p>
  </div>

  <h2>2026 Gelir Vergisi Tarifesi</h2>
''' + tarife + f'''
  <p>Ücret gelirleriyle diğer gelirler (serbest meslek, kira, ticari kazanç vb.) arasındaki tek fark %27 diliminin üst sınırıdır: ücretlilerde 1.500.000 TL, diğer gelirlerde 1.000.000 TL. Tarife <strong>yıllık</strong> matrah üzerinden uygulanır; maaşlarda ise yıl başından itibaren biriken (kümülatif) matrah esas alınır.</p>

  <h2>2027 Vergi Dilimleri Ne Kadar Olacak?</h2>
  <p>Dilim sınırları Gelir Vergisi Kanunu’nun 103. maddesine göre yeniden değerleme oranında artırılır, ancak son yıllarda artış bu oranın altında kaldı: 2026’da yeniden değerleme oranı %25,49 olmasına rağmen dilimler yaklaşık %20–25 artırıldı (ilk dilim 158.000 TL’den 190.000 TL’ye çıktı). Eylül 2026 itibarıyla oran %27,81 seviyesinde olduğu için iki senaryo hesapladık:</p>
''' + t27 + f'''
  <p>Tutarlar bin liranın altındaki kısımlar atılarak gösterilmiştir. Kesin 2027 tarifesi Aralık 2026 sonunda yayımlanacak ve bu yazı güncellenecek.</p>

  <h2>Gelir Vergisi Nasıl Hesaplanır? Örnek</h2>
  <p>Yıllık {t0(ORN)} ücret matrahı için 2026 tarifesiyle vergi:</p>
''' + table(['Dilim', 'Matrah', 'Oran', 'Vergi'], [
    ['1. dilim', t0(190000), '%15', t0(190000 * .15)], ['2. dilim', t0(210000), '%20', t0(210000 * .20)],
    ['3. dilim', t0(ORN - 400000), '%27', t0((ORN - 400000) * .27)], ['<strong>Toplam</strong>', t0(ORN), '', '<strong>' + t0(gv(ORN)) + '</strong>']], 'Örnek hesap') + f'''
  <p>Toplam vergi {t0(gv(ORN))}, yani efektif oran yaklaşık <strong>%{tl(gv(ORN) / ORN * 100, 1)}</strong>’dir. Üst dilime girmek tüm gelirinizin o oranla vergilendirileceği anlamına gelmez; yalnızca sınırı aşan kısım yüksek oranla vergilendirilir.</p>

  <h2>Maaşım Yılın Hangi Ayında Üst Dilime Geçer?</h2>
  <p>Bordroda gelir vergisi, yıl başından itibaren biriken matrah üzerinden hesaplanır. Matrah, brüt ücretten %14 SGK ve %1 işsizlik primi düşülerek bulunur. Biriken matrah dilim sınırını aştığı ay net maaşınız düşer. 2026 tarifesine göre geçiş ayları:</p>
''' + gecis + f'''
  <p>Asgari ücrete isabet eden vergi istisna edildiği için asgari ücretliler gelir vergisi ödemez; daha yüksek maaşlarda da asgari ücret kadar kısım vergiden istisnadır. Bu nedenle net maaştaki düşüş, tablodaki ayda vergi oranı farkı kadar değil daha sınırlı olur. Kendi net maaşınızı ay ay görmek için <a href="{B}/net-maas-hesaplama.html">net maaş hesaplama</a>, yıllık vergi tutarınızı görmek için <a href="{B}/gelir-vergisi-hesaplama.html">gelir vergisi hesaplama</a> aracını kullanabilirsiniz.</p>

  <h2>Hangi Gelirler Bu Tarifeye Tabi?</h2>
  <ul>
    <li><strong>Ücret:</strong> İşveren tarafından her ay kesilir; tek işverenden ücret alanlar genellikle beyanname vermez.</li>
    <li><strong>Serbest meslek ve ticari kazanç:</strong> Yıllık beyannameyle Mart ayında beyan edilir; ücret dışı tarife uygulanır.</li>
    <li><strong>Kira geliri:</strong> Konut kiralarında 2026 için 58.000 TL istisna vardır; aşan kısım tarifeye göre vergilendirilir. Ayrıntılar <a href="{B}/blog/kira-geliri-vergisi-hesaplama.html">kira geliri vergisi rehberinde</a>.</li>
    <li><strong>Değer artışı ve arızi kazançlar:</strong> İstisna tutarlarını aşan kısım beyan edilir.</li>
  </ul>
  <p>Diğer 2027 artışlarını <a href="{B}/blog/yeniden-degerleme-orani-2026.html">yeniden değerleme oranı rehberinde</a> bulabilirsiniz.</p>

  <h2>Kaynaklar</h2>
  <p style="font-size:.88rem">193 sayılı Gelir Vergisi Kanunu 103. madde · Gelir İdaresi Başkanlığı 2026 gelir vergisi tarifesi · TÜİK Yİ-ÜFE (Eylül 2026).</p>
'''
faq4 = [
    ('2026 gelir vergisi dilimleri nedir?', 'Ücretlerde 190.000 TL’ye kadar %15, 400.000 TL’ye kadar %20, 1.500.000 TL’ye kadar %27, 5.300.000 TL’ye kadar %35, üzeri %40’tır. Ücret dışı gelirlerde %27 dilimi 1.000.000 TL’de biter.'),
    ('2027 vergi dilimleri ne kadar olacak?', f'Dilimler %20 artırılırsa ilk dilim {t0(kes(190000*1.2))}, tam oranla (%27,81) {t0(kes(190000*(1+T)))} olur. Kesin tarife Aralık 2026 sonunda açıklanacak.'),
    ('2027 vergi dilimleri ne zaman açıklanacak?', 'Yeniden değerleme oranı 3 Kasım 2026’da TÜİK verisiyle belli olur; yeni tarife genellikle Aralık ayının son günlerinde Resmî Gazete’de yayımlanır.'),
    ('Üst dilime geçince bütün maaşım mı yüksek oranla vergilenir?', 'Hayır. Yalnızca dilim sınırını aşan kısım üst oranla vergilendirilir. Örneğin 600.000 TL yıllık matrahta ortalama vergi oranı yaklaşık %20,8’dir.'),
    ('Maaşım hangi ay %20 dilimine geçer?', 'Aylık 60.000 TL brüt ücrette vergi matrahı 51.000 TL olur; biriken matrah 190.000 TL’yi Nisan ayında aşar ve o aydan itibaren %20 dilimi uygulanır.'),
    ('Asgari ücretli vergi öder mi?', 'Hayır. Asgari ücrete isabet eden gelir ve damga vergisi istisna edildiği için asgari ücretliler bu vergileri ödemez.'),
]
rel4 = [('🧾', 'Gelir Vergisi Hesaplama', '2026 tarifesiyle vergi', f'{B}/gelir-vergisi-hesaplama.html'),
        ('💼', 'Net Maaş Hesaplama', 'Ay ay net maaş', f'{B}/net-maas-hesaplama.html'),
        ('📈', 'Yeniden Değerleme Oranı 2026', '2027’de neler artacak?', f'{B}/blog/yeniden-degerleme-orani-2026.html'),
        ('🏠', 'Kira Geliri Vergisi', '58.000 TL istisna', f'{B}/blog/kira-geliri-vergisi-hesaplama.html')]
if __name__ == '__main__':
    print(make('vergi-dilimleri-2027',
         'Gelir Vergisi Dilimleri 2027 – 2026 Tarifesi ve 2027 Tahmini | Hesaplarsın',
         '2026 gelir vergisi dilimleri: 190.000 / 400.000 / 1.500.000 / 5.300.000 TL. 2027 dilimleri tahmini, örnek hesap ve maaşınızın hangi ay üst dilime geçeceği tablosu.',
         'vergi dilimleri 2027, gelir vergisi dilimleri 2027, 2026 vergi dilimleri, gelir vergisi tarifesi 2027, vergi dilimi ne zaman değişir',
         'Gelir Vergisi Dilimleri 2027', 'Gelir Vergisi Dilimleri 2027: Yeni Limitler Ne Kadar Olacak?',
         hero('🧾', 'Aralık 2026’da açıklanacak', '2026 İLK DİLİM', '190.000 TL · %15', '2027 TAHMİNİ', f'{t0(kes(190000*1.2))} – {t0(kes(190000*(1+T)))}', '#7c2d12', '#ea580c'),
         ['Vergi', 'Rehber'], body4, faq4, rel4, date='2026-10-24', date_tr='24 Ekim 2026'))
