"""Kamu & Memur kategorisi: memur maaşları ana sayfası ve meslek maaş sayfaları.
Veri: Temmuz–Aralık 2026 maaşları (basında yayımlanan, Ocak 2026 maaşlarına %13,52 Temmuz zammı uygulanmış tablolar;
aile yardımı, ek ders, nöbet, döner sermaye ve bölgesel ödemeler hariç). Katsayılar: Hazine ve Maliye Bakanlığı genelgesi.
Ocak 2027 için güncellenecek alanlar: U tutarları, DONEM metinleri, senaryo tablosu.
"""

TOOLS = []

U = {
    'ogretmen': ('Öğretmen (1/4)', 83287), 'uzman-ogretmen': ('Uzman Öğretmen (1/4)', 92200),
    'polis': ('Polis Memuru (8/1)', 92652), 'baskomiser': ('Başkomiser (3/1)', 101276),
    'hemsire': ('Hemşire, lisans (5/1)', 84879), 'uzman-doktor': ('Uzman Doktor (1/4)', 170764),
    'profesor': ('Profesör (1/4)', 153353), 'ars-gor': ('Araştırma Görevlisi (7/1)', 102813),
    'memur': ('Memur, üniversite mezunu (9/1)', 73103), 'sube-muduru': ('Şube Müdürü (1/4)', 107145),
    'teknisyen': ('Teknisyen, lise mezunu (11/1)', 75911), 'muhendis': ('Mühendis (1/4)', 109219),
    'vaiz': ('Vaiz (1/4)', 87016), 'avukat': ('Avukat (1/4)', 102168),
}
def _z(a):
    h = 1.0557 * (1 + a / 100) ** 3 - 1
    return 1.05 * (1 + max(0.0, (1 + h) / 1.07 - 1)) - 1


SC = [(a, _z(a)) for a in (0.6, 1.0, 1.4)]  # Ekim–Aralık aylık ort. enflasyon → Ocak 2027 memur zammı (hesaplayıcıyla aynı formül)


def tl(x):
    return f"{x:,.0f}".replace(',', '.')


def form(keys):
    opts = ''.join(f'<option value="{U[k][1]}">{U[k][0]} – {tl(U[k][1])} ₺</option>' for k in keys)
    return f'''<div class="form-grid">
<div class="field full"><label for="unvan">Unvan</label><select id="unvan">{opts}<option value="0">Diğer / kendi maaşımı gireceğim</option></select></div>
<div class="field"><label for="maas">Mevcut Net Maaşınız (₺) <small>bordronuzdaki tutar; boş bırakırsanız örnek maaş kullanılır</small></label><input type="number" id="maas" placeholder="örn: 85.000" inputmode="decimal"></div>
<div class="field"><label for="aylik">Ekim–Aralık aylık ort. enflasyon tahmini (%)</label><input type="number" id="aylik" value="1" inputmode="decimal"></div>
</div>'''


JS = r'''
var Q3=0.0557, TS=0.05, ONCEKI=0.07;
function zam(a){var h=(1+Q3)*Math.pow(1+a/100,3)-1, f=Math.max(0,(1+h)/(1+ONCEKI)-1); return {h:h,f:f,z:(1+TS)*(1+f)-1};}
function hesapla(){
  var m=v('maas'); if(!(m>0)) m=parseFloat(el('unvan').value); if(!(m>0)) return 'Mevcut net maaşınızı girin.';
  var a=v('aylik'); if(isNaN(a)) a=1; if(a<-2||a>10) return 'Aylık enflasyon tahmini −2 ile 10 arasında olmalı.';
  var r=zam(a), lo=zam(0.6), hi=zam(1.4), y=m*(1+r.z);
  return {main:['Ocak 2027 tahmini net maaş', tl(y)], sub:'%'+num(r.z*100,2)+' zamla (Temmuz–Aralık 2026 maaşı: '+tl(m)+')',
    rows:[['6 aylık enflasyon (Temmuz–Aralık)',pct(r.h*100)],['Toplu sözleşme zammı','%5,00'],['Enflasyon farkı',pct(r.f*100)],['Toplam zam',pct(r.z*100),'hl'],
          ['Aylık artış',tl(y-m)],['Düşük senaryo (aylık %0,6 enflasyon)',tl(m*(1+lo.z))],['Yüksek senaryo (aylık %1,4 enflasyon)',tl(m*(1+hi.z))]],
    note:'Temmuz–Eylül 2026 enflasyonu %5,57 olarak gerçekleşti. Kesin zam Aralık enflasyonunun açıklandığı Ocak 2027’nin ilk günlerinde belli olur. Aile yardımı, ek ders, nöbet ve döner sermaye ödemeleri hesaba dahil değildir.'};
}'''


def ocak_table(keys):
    head = '<tr><th>Unvan</th><th>Temmuz–Aralık 2026</th>' + ''.join(f'<th>Ocak 2027 (%{z*100:.2f})</th>'.replace('.', ',') for _, z in SC) + '</tr>'
    rows = ''.join(f'<tr><td>{U[k][0]}</td><td><b>{tl(U[k][1])} ₺</b></td>' + ''.join(f'<td>{tl(U[k][1]*(1+z))} ₺</td>' for _, z in SC) + '</tr>' for k in keys)
    return f'<div class="table-wrap"><table><thead>{head}</thead><tbody>{rows}</tbody></table></div>'


SCEN = '''<div class="table-wrap"><table><thead><tr><th>Ekim–Aralık aylık ort. enflasyon</th><th>6 aylık enflasyon</th><th>Enflasyon farkı</th><th>Ocak 2027 memur zammı</th></tr></thead><tbody>
<tr><td>%0,6</td><td>%7,48</td><td>%0,45</td><td>%5,47</td></tr>
<tr><td>%1,0</td><td>%8,77</td><td>%1,65</td><td>%6,74</td></tr>
<tr><td>%1,4</td><td>%10,07</td><td>%2,87</td><td>%8,01</td></tr>
</tbody></table></div>'''

NOTE = '<p><small>Tablolardaki tutarlar, basında yayımlanan Temmuz 2026 memur maaş tablolarından alınmıştır (Ocak 2026 maaşlarına %13,52 Temmuz zammı uygulanmış). Aile yardımı, ek ders, nöbet, döner sermaye ve bölgesel ödemeler hariçtir; derece, kademe, hizmet yılı ve kuruma göre değişir. Kendi bordronuzdaki tutarı hesaplayıcıya girerek kişisel sonucunuzu görebilirsiniz.</small></p>'

SOURCES = [('Hazine ve Maliye Bakanlığı – Mali ve Sosyal Haklar Genelgesi', 'https://www.hmb.gov.tr/'),
           ('657 sayılı Devlet Memurları Kanunu', 'https://www.mevzuat.gov.tr/mevzuatmetin/1.5.657.pdf'),
           ('TÜİK Tüketici Fiyat Endeksi', 'https://data.tuik.gov.tr/')]

ALL = list(U.keys())

# ───────────────────────── MEMUR MAAŞLARI (ANA) ─────────────────────────
TOOLS.append(dict(
slug='memur-maaslari', name='Memur Maaşları 2026–2027', cat='kamu', ico='🏛️',
title='Memur Maaşları 2027: Ocak Zammıyla Yeni Maaş Tablosu | Hesaplarsın',
desc='Memur maaşları 2026–2027: öğretmen, polis, hemşire, doktor ve 14 unvanın Temmuz 2026 maaşı, Ocak 2027 zam senaryoları ve maaş hesaplama.',
h1='🏛️ Memur Maaşları 2026–2027',
lead='14 unvanın Temmuz–Aralık 2026 maaşını ve Ocak 2027 zammıyla tahmini yeni maaşlarını görün. Kendi bordronuzdaki tutarı girerek kişisel hesaplama yapın.',
button='Ocak 2027 Maaşını Hesapla',
form=form(ALL), js=JS,
article=f'''
<p><b>Kısa cevap:</b> Temmuz–Aralık 2026 döneminde örnek maaşlar 1/4 öğretmen için <b>83.287 ₺</b>, 8/1 polis memuru için <b>92.652 ₺</b>, 5/1 hemşire için <b>84.879 ₺</b>, 1/4 uzman doktor için <b>170.764 ₺</b>’dir. Ocak 2027’de memurlar %5 toplu sözleşme zammı ve enflasyon farkıyla yaklaşık <b>%5,5–%8</b> zam alacak.</p>

<h2 id="tablo">Memur maaşları tablosu: Temmuz 2026 ve Ocak 2027 tahmini</h2>
{ocak_table(ALL)}
{NOTE}

<h2 id="zam">Ocak 2027 memur zammı ne kadar olacak?</h2>
<p>8. Dönem Toplu Sözleşme’ye göre memurlar 2027’nin ilk yarısında <b>%5</b> zam alır. 2026’nın ikinci yarısındaki %7’lik zam, Temmuz–Aralık enflasyonunun altında kalırsa aradaki fark <b>enflasyon farkı</b> olarak Ocak maaşına eklenir. Temmuz–Eylül döneminde enflasyon %5,57 oldu; zam oranını Ekim, Kasım ve Aralık enflasyonu belirleyecek:</p>
{SCEN}
<p>Senaryoların ayrıntılı açıklaması için <a href="/blog/memur-emekli-zammi-ocak-2027.html">Ocak 2027 memur ve emekli zammı</a> yazımıza, emekliler için <a href="/memur-emekli-zammi-hesaplama.html">memur ve emekli zammı hesaplama</a> aracına bakabilirsiniz.</p>

<h2 id="hesap">Memur maaşı nasıl hesaplanır?</h2>
<p>Memur maaşı 657 sayılı Devlet Memurları Kanunu’na göre gösterge puanlarının <b>katsayılarla</b> çarpılmasıyla bulunur. Katsayılar her Ocak ve Temmuz’da Hazine ve Maliye Bakanlığı genelgesiyle güncellenir. Temmuz–Aralık 2026 katsayıları:</p>
<div class="table-wrap"><table><thead><tr><th>Katsayı</th><th>Ocak–Haziran 2026</th><th>Temmuz–Aralık 2026</th></tr></thead><tbody>
<tr><td>Aylık katsayı</td><td>1,387871</td><td>1,575512</td></tr>
<tr><td>Taban aylık katsayısı</td><td>22,722793</td><td>25,794915</td></tr>
<tr><td>Yan ödeme katsayısı</td><td>0,440141</td><td>0,499649</td></tr>
</tbody></table></div>
<p>Maaşı oluşturan başlıca kalemler: <b>aylık (gösterge × aylık katsayı)</b>, <b>ek gösterge</b>, <b>taban aylık</b>, <b>kıdem aylığı</b>, <b>yan ödeme</b>, <b>özel hizmet tazminatı</b> ve varsa <b>makam/görev tazminatı</b>. Bunlara evli ve çocuklu memurlarda <b>aile yardımı</b> eklenir; gelir vergisi, damga vergisi ve emeklilik kesintileri düşülür.</p>

<h2 id="derece">Derece ve kademe ne demek?</h2>
<p>“1/4” gibi gösterimlerde ilk rakam <b>derece</b>, ikinci rakam <b>kademe</b>dir. Memur her yıl bir kademe ilerler; üç kademe ilerlemesi bir derece yükselmesine karşılık gelir (kadro şartlarına bağlı). Derece 15’ten 1’e doğru yükselir; 1. derece en yüksek derecedir. Dört yıllık üniversite mezunları genellikle 9. dereceden göreve başlar; lise ve önlisans mezunlarının başlangıç derecesi daha düşüktür. Bu yüzden aynı unvanda, kıdemli bir memurun maaşı yeni başlayandan belirgin şekilde yüksektir.</p>

<h2 id="odeme">Memur maaşları ne zaman yatar?</h2>
<p>Memur maaşları her ayın <b>15’inde peşin</b> olarak ödenir. Ocak 2027 zamlı maaşı 15 Ocak 2027’de yatacak. Kesin zam oranı, maaş ödemesinden önce, Ocak’ın ilk günlerinde açıklanan Aralık enflasyonuyla belli olur; zam geç açıklanırsa aradaki fark sonradan toplu ödenir.</p>

<h2 id="meslekler">Meslek meslek maaş rehberleri</h2>
<ul>
<li><a href="/ogretmen-maasi.html">Öğretmen maaşı 2027</a> – öğretmen, uzman öğretmen, ek ders ücreti</li>
<li><a href="/polis-maasi.html">Polis maaşı 2027</a> – polis memuru, başkomiser, rütbeler</li>
<li><a href="/hemsire-maasi.html">Hemşire maaşı 2027</a> – döner sermaye ve nöbet ödemeleri</li>
<li><a href="/doktor-maasi.html">Doktor maaşı 2027</a> – uzman doktor, profesör, araştırma görevlisi</li>
<li><a href="/muhendis-maasi.html">Mühendis maaşı 2027</a> – teknik hizmetler sınıfı, teknisyen</li>
</ul>
''',
faq=[
('Ocak 2027 memur maaşları ne kadar olacak?','Ocak 2027’de memurlar %5 toplu sözleşme zammı ve enflasyon farkı alacak. Ekim–Aralık enflasyonuna göre toplam zammın yaklaşık %5,5–%8 olması bekleniyor. Örneğin Temmuz 2026’da 83.287 ₺ olan 1/4 öğretmen maaşı %6,74 zamla yaklaşık 88.900 ₺ olur.'),
('En düşük memur maaşı ne kadar?','Tablodaki unvanlar arasında en düşük maaş 9/1 derecedeki üniversite mezunu memur için 73.103 ₺’dir. Lise mezunu ve daha düşük derecede başlayan bazı kadrolarda maaş daha düşük olabilir.'),
('Memur maaşları ne zaman yatar?','Memur maaşları her ayın 15’inde peşin ödenir. Ocak 2027 zamlı maaşı 15 Ocak 2027’de yatacak.'),
('Memur maaş katsayısı ne kadar?','Temmuz–Aralık 2026 döneminde aylık katsayı 1,575512, taban aylık katsayısı 25,794915, yan ödeme katsayısı 0,499649’dur. Ocak 2027 katsayıları zam oranı belli olduğunda yeniden belirlenecek.'),
('Memur emeklisi de aynı zammı alır mı?','Evet. Emekli Sandığı’na tabi memur emeklileri, memurlarla aynı oranda (toplu sözleşme zammı + enflasyon farkı) zam alır.'),
],
related=['ogretmen-maasi','polis-maasi','hemsire-maasi','doktor-maasi','muhendis-maasi','memur-emekli-zammi-hesaplama'],
sources=SOURCES,
))

# ───────────────────────── ÖĞRETMEN ─────────────────────────
TOOLS.append(dict(
slug='ogretmen-maasi', name='Öğretmen Maaşı 2027', cat='kamu', ico='👩‍🏫',
title='Öğretmen Maaşı 2027: Ocak Zammıyla Ne Kadar Olacak? | Hesaplarsın',
desc='Öğretmen maaşı 2027: Temmuz 2026’da 1/4 öğretmen 83.287 TL, uzman öğretmen 92.200 TL. Ocak 2027 zam senaryoları, ek ders ücreti ve maaş hesaplama.',
h1='👩‍🏫 Öğretmen Maaşı 2026–2027',
lead='Öğretmen ve uzman öğretmen maaşlarını, Ocak 2027 zammıyla tahmini yeni maaşı ve ek ders ücretini görün. Kendi bordronuzdaki net maaşı girerek hesaplayın.',
button='Öğretmen Maaşını Hesapla',
form=form(['ogretmen', 'uzman-ogretmen']), js=JS,
article=f'''
<p><b>Kısa cevap:</b> Temmuz–Aralık 2026 döneminde 1/4 derecedeki bir öğretmenin maaşı <b>83.287 ₺</b>, uzman öğretmenin maaşı <b>92.200 ₺</b>’dir. Ocak 2027’de %5 toplu sözleşme zammı ve enflasyon farkıyla öğretmen maaşının yaklaşık <b>87.800–90.000 ₺</b> aralığına çıkması bekleniyor.</p>

<h2 id="tablo">Öğretmen maaşları: Temmuz 2026 ve Ocak 2027 tahmini</h2>
{ocak_table(['ogretmen', 'uzman-ogretmen'])}
{NOTE}

<h2 id="kariyer">Uzman öğretmen ve başöğretmen ne kadar fazla alır?</h2>
<p>Öğretmenlik Meslek Kanunu’yla öğretmenlik kariyeri üç basamaklı hâle geldi: <b>öğretmen</b>, <b>uzman öğretmen</b> ve <b>başöğretmen</b>. Uzman öğretmenlik ve başöğretmenlik için belirli hizmet süresi ve eğitim şartlarının sağlanması gerekir. Kariyer basamağı yükseldikçe ek gösterge ve ödemeler artar. Temmuz 2026 tablosuna göre 1/4 derecede uzman öğretmen, öğretmenden aylık yaklaşık <b>8.900 ₺</b> fazla alır. Başöğretmenlerin maaşı uzman öğretmenden de yüksektir.</p>

<h2 id="ekders">Ek ders ücreti nasıl hesaplanır?</h2>
<p>Öğretmenler zorunlu ders saatinin üzerinde girdikleri her saat için ek ders ücreti alır. Ek ders ücreti, gösterge rakamının aylık katsayıyla çarpılmasıyla hesaplanır: gündüz dersleri için <b>140</b>, gece dersleri için <b>150</b> gösterge kullanılır.</p>
<div class="formula">Gündüz ek ders (brüt) = 140 × 1,575512 = 220,57 ₺<br>Gece ek ders (brüt) = 150 × 1,575512 = 236,33 ₺</div>
<p>Bu tutarlar Temmuz–Aralık 2026 aylık katsayısıyla hesaplanmış <b>brüt</b> tutarlardır; gelir vergisi ve damga vergisi kesildikten sonra net tutar öğretmenin vergi dilimine göre değişir. Ocak 2027’de aylık katsayı arttığında ek ders ücreti de aynı oranda artar. Destekleme ve yetiştirme kursları gibi bazı görevlerde ek ders ücreti artırımlı ödenir.</p>
<div class="example"><p><b>Örnek:</b> Ayda 40 saat gündüz ek ders giren bir öğretmenin brüt ek ders ücreti 40 × 220,57 = <b>8.822,80 ₺</b> olur.</p></div>

<h2 id="sozlesmeli">Sözleşmeli ve ücretli öğretmen maaşı</h2>
<p><b>Sözleşmeli öğretmenler</b>, kadrolu öğretmene yakın ama bir miktar daha düşük maaş alır ve belirli süreyi tamamlayınca kadroya geçer. <b>Ücretli öğretmenler</b> ise maaş almaz; girdikleri her ders saati için ek ders ücreti üzerinden ödeme alır. Bu nedenle ücretli öğretmenin aylık geliri, girdiği ders saatine ve okulların tatil dönemlerine göre değişir.</p>

<h2 id="tatil">Yaz tatilinde öğretmen maaşı yatar mı?</h2>
<p>Kadrolu ve sözleşmeli öğretmenlerin maaşı yaz ve ara tatillerde de her ayın 15’inde ödenmeye devam eder. Tatillerde ek ders yapılmadığı için yalnızca ek ders ücreti ödenmez. Ücretli öğretmenler ise ders yapılmayan dönemlerde ücret alamaz.</p>

<p>Diğer unvanlarla karşılaştırma için <a href="/memur-maaslari.html">memur maaşları tablosuna</a>, net maaşınızın kesinti dökümü için <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracına bakabilirsiniz.</p>
''',
faq=[
('Öğretmen maaşı 2027’de ne kadar olacak?','Temmuz 2026’da 83.287 ₺ olan 1/4 öğretmen maaşı, Ocak 2027’de beklenen %5,5–%8 zamla yaklaşık 87.800–90.000 ₺ olur. Kesin tutar Aralık enflasyonuyla belli olacak.'),
('Uzman öğretmen maaşı ne kadar?','Temmuz–Aralık 2026 döneminde 1/4 derecedeki uzman öğretmenin maaşı 92.200 ₺’dir; aynı derecedeki öğretmenden aylık yaklaşık 8.900 ₺ fazladır.'),
('Ek ders ücreti 2026’da ne kadar?','Temmuz–Aralık 2026 döneminde gündüz ek ders ücreti brüt 220,57 ₺ (140 × 1,575512), gece ek ders ücreti brüt 236,33 ₺’dir. Net tutar vergi dilimine göre değişir.'),
('Yeni atanan öğretmen maaşı ne kadar?','Yeni atanan öğretmenler genellikle 9. dereceden başlar ve maaşları 1/4 derecedeki öğretmenden daha düşüktür. Kesin tutar için bordrodaki net maaşınızı hesaplayıcıya girebilirsiniz.'),
('Öğretmenler yaz tatilinde maaş alır mı?','Evet. Kadrolu ve sözleşmeli öğretmenlerin maaşı tatillerde de ödenir; yalnızca ek ders ücreti tatil dönemlerinde ödenmez.'),
],
related=['memur-maaslari','polis-maasi','hemsire-maasi','memur-emekli-zammi-hesaplama','net-maas-hesaplama'],
sources=SOURCES + [('Öğretmenlik Meslek Kanunu (7528)', 'https://www.mevzuat.gov.tr/')],
))

# ───────────────────────── POLİS ─────────────────────────
TOOLS.append(dict(
slug='polis-maasi', name='Polis Maaşı 2027', cat='kamu', ico='👮',
title='Polis Maaşı 2027: Polis Memuru ve Başkomiser Maaşı | Hesaplarsın',
desc='Polis maaşı 2027: Temmuz 2026’da 8/1 polis memuru 92.652 TL, başkomiser 101.276 TL. Ocak 2027 zam tahmini, rütbeler ve maaş hesaplama.',
h1='👮 Polis Maaşı 2026–2027',
lead='Polis memuru ve başkomiser maaşlarını, Ocak 2027 zammıyla tahmini yeni maaşları görün. Kendi bordronuzdaki net maaşla kişisel hesaplama yapın.',
button='Polis Maaşını Hesapla',
form=form(['polis', 'baskomiser']), js=JS,
article=f'''
<p><b>Kısa cevap:</b> Temmuz–Aralık 2026 döneminde 8/1 derecedeki polis memurunun maaşı <b>92.652 ₺</b>, 3/1 derecedeki başkomiserin maaşı <b>101.276 ₺</b>’dir. Ocak 2027’de memur zammıyla polis memuru maaşının yaklaşık <b>97.700–100.100 ₺</b> aralığına çıkması bekleniyor.</p>

<h2 id="tablo">Polis maaşları: Temmuz 2026 ve Ocak 2027 tahmini</h2>
{ocak_table(['polis', 'baskomiser'])}
{NOTE}

<h2 id="neden">Polis maaşı neden diğer memurlardan yüksek?</h2>
<p>Polisler Emniyet Hizmetleri Sınıfı’nda yer alır. Bu sınıfta görevin riskli ve süreklilik gerektiren yapısı nedeniyle <b>özel hizmet tazminatı</b> ve <b>yan ödeme</b> tutarları genel idare hizmetlerine göre yüksektir. Bu yüzden aynı derecedeki bir polis memuru, üniversite mezunu bir memurdan belirgin şekilde fazla maaş alır: Temmuz 2026 tablosunda 8/1 polis memuru 92.652 ₺ iken 9/1 memur 73.103 ₺’dir.</p>

<h2 id="rutbe">Polis rütbeleri ve maaşa etkisi</h2>
<p>Emniyet teşkilatında polis memurları <b>polis memuru → kıdemli polis memuru → başpolis memuru</b> şeklinde ilerler. Amir sınıfında ise <b>komiser yardımcısı, komiser, başkomiser, emniyet amiri</b> ve üzeri rütbeler bulunur. Rütbe yükseldikçe ek gösterge, makam ve görev tazminatı gibi kalemler arttığı için maaş da yükselir. Polis meslek eğitim merkezlerinden (POMEM) ve polis meslek yüksekokullarından mezun olanlar polis memuru olarak göreve başlar; Polis Akademisi mezunları ise komiser yardımcısı rütbesiyle başlar.</p>

<h2 id="ek">Maaşa ek ödemeler</h2>
<ul>
<li><b>Fazla çalışma ücreti:</b> Mesai dışı görevlerde ilgili düzenlemelere göre ek ücret ödenir.</li>
<li><b>Aile yardımı:</b> Evli ve çocuklu polislerin maaşına eş ve çocuk yardımı eklenir.</li>
<li><b>Görev yeri:</b> Bazı bölgelerde ve birimlerde görev yapan personele ek ödemeler yapılabilir.</li>
</ul>
<p>Bu ödemeler kişiden kişiye değiştiği için tabloya dahil edilmemiştir. Kendi bordronuzdaki net tutarı hesaplayıcıya girerek Ocak 2027 maaşınızı tahmin edebilirsiniz.</p>

<h2 id="emekli">Polis emeklisi zammı</h2>
<p>Emniyet mensupları Emekli Sandığı’na tabidir; polis emeklileri de Ocak 2027’de memurlarla aynı oranda (toplu sözleşme zammı + enflasyon farkı) zam alır. Hesaplama için <a href="/memur-emekli-zammi-hesaplama.html">memur ve emekli zammı hesaplama</a> aracını kullanabilirsiniz.</p>

<p>Diğer unvanlarla karşılaştırma için <a href="/memur-maaslari.html">memur maaşları tablosuna</a> bakabilirsiniz.</p>
''',
faq=[
('Polis maaşı 2027’de ne kadar olacak?','Temmuz 2026’da 92.652 ₺ olan 8/1 polis memuru maaşı, Ocak 2027’de beklenen %5,5–%8 zamla yaklaşık 97.700–100.100 ₺ olur.'),
('Başkomiser maaşı ne kadar?','Temmuz–Aralık 2026 döneminde 3/1 derecedeki başkomiserin maaşı 101.276 ₺’dir.'),
('Yeni başlayan polis maaşı ne kadar?','Yeni başlayan polis memurları daha düşük derecede göreve başladığı için maaşları 8/1 derecedeki polis memurundan bir miktar düşüktür. Kesin tutar için ilk bordronuzu hesaplayıcıya girebilirsiniz.'),
('Polis maaşları ne zaman yatar?','Polis maaşları diğer memurlar gibi her ayın 15’inde peşin ödenir.'),
],
related=['memur-maaslari','ogretmen-maasi','hemsire-maasi','memur-emekli-zammi-hesaplama','kidem-tazminati-hesaplama'],
sources=SOURCES + [('3201 sayılı Emniyet Teşkilatı Kanunu', 'https://www.mevzuat.gov.tr/')],
))

# ───────────────────────── HEMŞİRE ─────────────────────────
TOOLS.append(dict(
slug='hemsire-maasi', name='Hemşire Maaşı 2027', cat='kamu', ico='👩‍⚕️',
title='Hemşire Maaşı 2027: Ocak Zammıyla Ne Kadar Olacak? | Hesaplarsın',
desc='Hemşire maaşı 2027: Temmuz 2026’da lisans mezunu 5/1 hemşire 84.879 TL. Ocak 2027 zam tahmini, döner sermaye, nöbet ücreti ve maaş hesaplama.',
h1='👩‍⚕️ Hemşire Maaşı 2026–2027',
lead='Kamu hastanelerinde çalışan hemşirelerin maaşını, Ocak 2027 zammıyla tahmini yeni maaşı ve maaşa eklenen döner sermaye ile nöbet ödemelerini görün.',
button='Hemşire Maaşını Hesapla',
form=form(['hemsire']), js=JS,
article=f'''
<p><b>Kısa cevap:</b> Temmuz–Aralık 2026 döneminde lisans mezunu, 5/1 derecedeki bir hemşirenin maaşı <b>84.879 ₺</b>’dir. Ocak 2027’de memur zammıyla bu tutarın yaklaşık <b>89.500–91.700 ₺</b> aralığına çıkması bekleniyor. Döner sermaye ve nöbet ücretleri bu tutara ayrıca eklenir.</p>

<h2 id="tablo">Hemşire maaşı: Temmuz 2026 ve Ocak 2027 tahmini</h2>
{ocak_table(['hemsire'])}
{NOTE}

<h2 id="doner">Döner sermaye ek ödemesi</h2>
<p>Kamu hastanelerinde çalışan hemşireler, maaşa ek olarak kurumun döner sermaye gelirinden <b>ek ödeme</b> alır. Bu ödeme hastanenin gelirine, hemşirenin çalıştığı birime, unvanına ve performans puanına göre her ay değişir. Yoğun bakım, acil ve ameliyathane gibi birimlerde çalışanların ek ödemesi genellikle daha yüksektir. Bu nedenle aynı derecedeki iki hemşirenin aylık toplam geliri farklı olabilir.</p>

<h2 id="nobet">Nöbet ve fazla çalışma ücreti</h2>
<p>Normal mesai dışında tutulan nöbetler için nöbet ücreti ödenir. Nöbet ücreti saat başına hesaplanır ve gece, hafta sonu ve bayram nöbetleri için tutarlar farklılaşır. Sık nöbet tutan bir hemşirenin aylık geliri, tablodaki maaşın belirgin şekilde üzerine çıkabilir.</p>

<h2 id="egitim">Lisans ve önlisans mezunu hemşire farkı</h2>
<p>Hemşirelik mesleğine bugün lisans mezunları kabul edilir; önceden önlisans veya sağlık meslek lisesi mezunu olarak göreve başlamış hemşireler de görev yapmaya devam etmektedir. Öğrenim durumu, göreve başlanan dereceyi ve ek göstergeyi etkilediği için lisans mezunu hemşirelerin maaşı genellikle daha yüksektir.</p>

<h2 id="ozel">Özel hastanede hemşire maaşı</h2>
<p>Özel hastanelerde çalışan hemşireler İş Kanunu’na tabidir; maaşları hastaneye, şehre ve deneyime göre serbestçe belirlenir ve asgari ücretin altında olamaz. Özel sektördeki brüt maaşınızın netini <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracıyla bulabilirsiniz.</p>

<p>Diğer sağlık çalışanlarının maaşları için <a href="/doktor-maasi.html">doktor maaşı</a>, tüm unvanlar için <a href="/memur-maaslari.html">memur maaşları tablosuna</a> bakabilirsiniz.</p>
''',
faq=[
('Hemşire maaşı 2027’de ne kadar olacak?','Temmuz 2026’da 84.879 ₺ olan 5/1 hemşire maaşı, Ocak 2027’de beklenen %5,5–%8 zamla yaklaşık 89.500–91.700 ₺ olur. Döner sermaye ve nöbet ücretleri buna ayrıca eklenir.'),
('Hemşirelere döner sermaye ne kadar ödenir?','Döner sermaye ek ödemesi hastanenin gelirine, birime ve performans puanına göre her ay değişir; sabit bir tutarı yoktur.'),
('Yeni atanan hemşire maaşı ne kadar?','Yeni atanan hemşireler daha düşük derecede başladığı için maaşları 5/1 derecedeki hemşireden düşüktür. Kendi bordronuzdaki net tutarla Ocak 2027 maaşınızı hesaplayabilirsiniz.'),
('Hemşire maaşları ne zaman yatar?','Kamuda çalışan hemşirelerin maaşı her ayın 15’inde peşin ödenir; döner sermaye ek ödemesi ise kurumun belirlediği tarihte ayrıca yatar.'),
],
related=['memur-maaslari','doktor-maasi','ogretmen-maasi','memur-emekli-zammi-hesaplama','net-maas-hesaplama'],
sources=SOURCES + [('6283 sayılı Hemşirelik Kanunu', 'https://www.mevzuat.gov.tr/')],
))

# ───────────────────────── DOKTOR ─────────────────────────
TOOLS.append(dict(
slug='doktor-maasi', name='Doktor Maaşı 2027', cat='kamu', ico='🩺',
title='Doktor Maaşı 2027: Uzman Doktor ve Profesör Maaşı | Hesaplarsın',
desc='Doktor maaşı 2027: Temmuz 2026’da 1/4 uzman doktor 170.764 TL, profesör 153.353 TL, araştırma görevlisi 102.813 TL. Ocak 2027 zam tahmini ve hesaplama.',
h1='🩺 Doktor Maaşı 2026–2027',
lead='Kamuda çalışan uzman doktor, profesör ve araştırma görevlisi maaşlarını, Ocak 2027 zammıyla tahmini yeni maaşları ve döner sermayenin etkisini görün.',
button='Doktor Maaşını Hesapla',
form=form(['uzman-doktor', 'profesor', 'ars-gor']), js=JS,
article=f'''
<p><b>Kısa cevap:</b> Temmuz–Aralık 2026 döneminde 1/4 derecedeki uzman doktorun maaşı <b>170.764 ₺</b>, profesörün maaşı <b>153.353 ₺</b>, 7/1 derecedeki araştırma görevlisinin maaşı <b>102.813 ₺</b>’dir. Ocak 2027’de memur zammıyla uzman doktor maaşının yaklaşık <b>180.000–184.400 ₺</b> aralığına çıkması bekleniyor.</p>

<h2 id="tablo">Doktor maaşları: Temmuz 2026 ve Ocak 2027 tahmini</h2>
{ocak_table(['uzman-doktor', 'profesor', 'ars-gor'])}
{NOTE}

<h2 id="doner">Döner sermaye doktor maaşını nasıl etkiler?</h2>
<p>Kamu hastanelerinde çalışan hekimlerin toplam gelirinde <b>döner sermaye ek ödemesi</b> önemli bir paya sahiptir. Ek ödeme; hastanenin gelirine, hekimin branşına, unvanına, yaptığı muayene ve işlem sayısına (performans puanına) göre her ay değişir. Bu nedenle cerrahi branşlarda ve yoğun hastanelerde çalışan uzman doktorların aylık geliri, tablodaki maaşın belirgin şekilde üzerine çıkabilir.</p>

<h2 id="akademik">Üniversite hastanelerinde akademik unvanlar</h2>
<p>Üniversite hastanelerinde hekimler <b>araştırma görevlisi (asistan) → doktor öğretim üyesi → doçent → profesör</b> şeklinde ilerler. Akademik unvan yükseldikçe ek gösterge ve akademik tazminat artar. Araştırma görevlileri uzmanlık eğitimini sürdürürken maaş ve nöbet ücreti alır; uzmanlık eğitimini tamamlayıp uzman olduktan sonra maaşları belirgin şekilde yükselir.</p>

<h2 id="pratisyen">Pratisyen doktor ve aile hekimi</h2>
<p>Pratisyen (tabip) doktorlar uzmanlara göre daha düşük ek gösterge ve ek ödeme alır. <b>Aile hekimleri</b> ise farklı bir sözleşmeli ödeme sistemine tabidir: gelirleri kayıtlı nüfusa, bölgeye ve performansa göre belirlenir. Bu nedenle aile hekimi maaşı, kadrolu hekim tablolarıyla doğrudan karşılaştırılamaz.</p>

<h2 id="nobet">Nöbet ücreti</h2>
<p>Mesai dışında tutulan nöbetler için hekimlere saat başına nöbet ücreti ödenir. Nöbet ücreti, hekimin unvanına ve nöbetin türüne (normal, icap, bayram) göre değişir. Asistan hekimlerin gelirinde nöbet ücretleri önemli bir paya sahiptir.</p>

<p>Diğer sağlık çalışanları için <a href="/hemsire-maasi.html">hemşire maaşı</a>, tüm unvanlar için <a href="/memur-maaslari.html">memur maaşları tablosuna</a> bakabilirsiniz.</p>
''',
faq=[
('Doktor maaşı 2027’de ne kadar olacak?','Temmuz 2026’da 170.764 ₺ olan 1/4 uzman doktor maaşı, Ocak 2027’de beklenen %5,5–%8 zamla yaklaşık 180.000–184.400 ₺ olur. Döner sermaye ek ödemesi bu tutara ayrıca eklenir.'),
('Profesör maaşı ne kadar?','Temmuz–Aralık 2026 döneminde 1/4 derecedeki profesörün maaşı 153.353 ₺’dir.'),
('Asistan doktor (araştırma görevlisi) maaşı ne kadar?','Temmuz–Aralık 2026 döneminde 7/1 derecedeki araştırma görevlisinin maaşı 102.813 ₺’dir; nöbet ücretleri ayrıca ödenir.'),
('Doktor maaşına döner sermaye dahil mi?','Tablodaki tutarlara döner sermaye dahil değildir. Döner sermaye ek ödemesi hastanenin gelirine ve hekimin performansına göre her ay değişir.'),
],
related=['memur-maaslari','hemsire-maasi','ogretmen-maasi','memur-emekli-zammi-hesaplama','net-maas-hesaplama'],
sources=SOURCES,
))

# ───────────────────────── MÜHENDİS ─────────────────────────
TOOLS.append(dict(
slug='muhendis-maasi', name='Mühendis Maaşı 2027', cat='kamu', ico='👷',
title='Mühendis Maaşı 2027: Kamuda Mühendis Ne Kadar Alır? | Hesaplarsın',
desc='Kamuda mühendis maaşı 2027: Temmuz 2026’da 1/4 derecede 109.219 TL. Ocak 2027 zam tahmini, teknik hizmetler sınıfı, özel sektör farkı ve hesaplama.',
h1='👷 Mühendis Maaşı 2026–2027',
lead='Kamuda çalışan mühendislerin maaşını, Ocak 2027 zammıyla tahmini yeni maaşı ve teknik hizmetler sınıfındaki maaş kalemlerini görün.',
button='Mühendis Maaşını Hesapla',
form=form(['muhendis', 'teknisyen']), js=JS,
article=f'''
<p><b>Kısa cevap:</b> Temmuz–Aralık 2026 döneminde kamuda 1/4 derecedeki bir mühendisin maaşı <b>109.219 ₺</b>’dir. Ocak 2027’de memur zammıyla bu tutarın yaklaşık <b>115.200–118.000 ₺</b> aralığına çıkması bekleniyor. Aynı dönemde lise mezunu 11/1 teknisyenin maaşı 75.911 ₺’dir.</p>

<h2 id="tablo">Mühendis ve teknisyen maaşı: Temmuz 2026 ve Ocak 2027 tahmini</h2>
{ocak_table(['muhendis', 'teknisyen'])}
{NOTE}

<h2 id="neden">Kamuda mühendis maaşı neden yüksek?</h2>
<p>Mühendisler, mimarlar ve şehir plancıları Teknik Hizmetler Sınıfı’nda yer alır. Bu kadrolarda <b>ek gösterge</b> ve <b>özel hizmet tazminatı</b> oranları genel idare hizmetlerindeki memurlara göre yüksektir. Bu yüzden 1/4 derecedeki bir mühendis, aynı derecedeki şube müdürüne yakın, üniversite mezunu 9/1 memurdan ise belirgin şekilde fazla maaş alır. Kıdem ilerledikçe ve derece yükseldikçe fark artar.</p>

<h2 id="kalemler">Mühendis maaşını oluşturan kalemler</h2>
<ul>
<li><b>Aylık ve ek gösterge:</b> Derece ve kademeye göre gösterge puanı aylık katsayıyla çarpılır.</li>
<li><b>Taban aylık ve kıdem aylığı:</b> Tüm memurlarda olduğu gibi hizmet yılına göre artar.</li>
<li><b>Yan ödeme ve özel hizmet tazminatı:</b> Teknik hizmetler sınıfında oranlar daha yüksektir.</li>
<li><b>Aile yardımı:</b> Evli ve çocuklu mühendislerin maaşına eklenir.</li>
<li><b>Ek ödeme:</b> Bazı kurumlarda (belediyeler, döner sermayeli kurumlar) kurumun gelirine bağlı ek ödemeler yapılabilir.</li>
</ul>

<h2 id="kpss">Kamuda mühendis olmak</h2>
<p>Bakanlıklara ve kamu kurumlarına mühendis alımı genellikle <b>KPSS puanı</b> ile yapılır; bazı kurumlar ayrıca sözlü veya uygulamalı sınav düzenler. Göreve başlayan mühendis genellikle 9. dereceden başlar ve her yıl kademe ilerler. Kurumların sözleşmeli mühendis alımlarında ise ücret, ilgili mevzuattaki sözleşme tavanlarına göre belirlenir.</p>

<h2 id="ozel">Özel sektörde mühendis maaşı</h2>
<p>Özel sektörde mühendis maaşları şirkete, sektöre, şehre ve deneyime göre serbestçe belirlenir. İş tekliflerinde konuşulan rakamın genellikle brüt olduğunu unutmayın. Teklif edilen brüt maaşın netini <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracıyla, yıl içindeki değişimini <a href="/blog/brutten-nete-maas-tablosu-2026.html">brütten nete maaş tablosuyla</a> görebilirsiniz.</p>

<p>Diğer unvanlarla karşılaştırma için <a href="/memur-maaslari.html">memur maaşları tablosuna</a> bakabilirsiniz.</p>
''',
faq=[
('Kamuda mühendis maaşı 2027’de ne kadar olacak?','Temmuz 2026’da 109.219 ₺ olan 1/4 derecedeki mühendis maaşı, Ocak 2027’de beklenen %5,5–%8 zamla yaklaşık 115.200–118.000 ₺ olur.'),
('Yeni başlayan mühendis maaşı ne kadar?','Kamuda yeni başlayan mühendisler genellikle 9. dereceden başladığı için maaşları 1/4 derecedeki mühendisten daha düşüktür. Kendi bordronuzdaki net tutarla Ocak 2027 maaşınızı hesaplayabilirsiniz.'),
('Teknisyen maaşı ne kadar?','Temmuz–Aralık 2026 döneminde lise mezunu 11/1 derecedeki teknisyenin maaşı 75.911 ₺’dir.'),
('Mühendis maaşı memurdan neden yüksek?','Mühendisler Teknik Hizmetler Sınıfı’nda yer alır; bu sınıfta ek gösterge ve özel hizmet tazminatı oranları genel idare hizmetlerine göre yüksektir.'),
],
related=['memur-maaslari','ogretmen-maasi','polis-maasi','memur-emekli-zammi-hesaplama','net-maas-hesaplama'],
sources=SOURCES,
))

# ───────────────────────── BEDELLİ ASKERLİK ─────────────────────────
# 7179 sayılı Askeralma Kanunu m.9: bedel = 300.000 gösterge × memur aylık katsayısı (17.04.2026 öncesi 240.000 gösterge);
# yoklama kaçağı/bakaya ek bedeli: her ay için 3.500 gösterge × katsayı (1–30 gün bir ay). Temmuz–Aralık 2026 katsayısı 1,575512 (MSB duyurusu 472.653,60 TL).
BED_G, BED_EK, BED_K = 300000, 3500, 1.575512
BED_SEN = [('Düşük senaryo (%5,47 zam)', 0.0547), ('Orta senaryo (%6,74 zam)', 0.0674), ('Yüksek senaryo (%8,01 zam)', 0.0801)]
def _b2(x):
    return f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
BED_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Dönem</th><th>Memur aylık katsayısı</th><th>Bedelli askerlik ücreti</th></tr></thead><tbody>'
    '<tr><td>1 Ocak – 16 Nisan 2026 (240.000 gösterge)</td><td>1,387871</td><td>333.089,04 ₺</td></tr>'
    '<tr><td>17 Nisan – 30 Haziran 2026</td><td>1,387871</td><td>416.361,30 ₺</td></tr>'
    f'<tr><td><b>1 Temmuz – 31 Aralık 2026 (güncel)</b></td><td>{str(BED_K).replace(".", ",")}</td><td><b>{_b2(BED_G * BED_K)} ₺</b></td></tr>'
    + ''.join(f'<tr><td>Ocak 2027 – {ad.lower()}</td><td>≈ {str(round(BED_K * (1 + z), 6)).replace(".", ",")}</td><td>≈ {_b2(BED_G * BED_K * (1 + z))} ₺</td></tr>' for ad, z in BED_SEN)
    + '</tbody></table></div>')
TOOLS.append(dict(
slug='bedelli-askerlik-hesaplama', name='Bedelli Askerlik Ücreti Hesaplama', cat='kamu', ico='🎖️',
title='Bedelli Askerlik Ücreti 2026 – Ocak 2027’de Ne Kadar Olacak? | Hesaplarsın',
desc=f'Bedelli askerlik ücreti Temmuz–Aralık 2026’da {_b2(BED_G * BED_K)} TL. Ocak 2027 tahmini ≈ {_b2(BED_G * BED_K * 1.0547)[:-3]} – {_b2(BED_G * BED_K * 1.0801)[:-3]} TL. Yoklama kaçağı ek bedeliyle hesaplayın.',
h1='🎖️ Bedelli Askerlik Ücreti Hesaplama – 2026 ve Ocak 2027',
lead='Bedelli askerlik ücreti, 300.000 gösterge rakamının ödeme günündeki memur aylık katsayısıyla çarpılmasıyla bulunur. Dönemi seçin; yoklama kaçağı veya bakaya durumunuz varsa geçen ay sayısını girin, ödemeniz gereken toplam bedeli görün.',
card_title='Bedelli Askerlik Hesaplayıcı', button='Hesapla',
form='''<div class="form-grid">
  <div class="field full"><label for="donem">Ödeme dönemi</label><select id="donem"><option value="guncel">1 Temmuz – 31 Aralık 2026 (güncel)</option>''' + ''.join(f'<option value="{z}">Ocak 2027 – {ad.lower()}</option>' for ad, z in BED_SEN) + '''<option value="ozel">Katsayıyı kendim gireceğim</option></select></div>
  <div class="field"><label for="ay">Yoklama kaçağı / bakaya süresi <small>ay (yoksa boş)</small></label><input type="number" id="ay" placeholder="0" inputmode="numeric"></div>
  <div class="field"><label for="katsayi">Memur aylık katsayısı <small>“kendim gireceğim” için</small></label><input type="number" id="katsayi" placeholder="örn: 1,575512" inputmode="decimal" step="any"></div>
</div>''',
js=f'var BG={BED_G}, BE={BED_EK}, BK={BED_K};' + r'''
function hesapla(){
  var d=el('donem').value, ay=Math.max(0,Math.ceil(v('ay')||0)), k, ad;
  if(d==='guncel'){k=BK; ad='1 Temmuz – 31 Aralık 2026';}
  else if(d==='ozel'){k=v('katsayi'); if(!(k>0)) return 'Memur aylık katsayısını girin (örn. 1,575512).'; ad='Girdiğiniz katsayı';}
  else {k=BK*(1+parseFloat(d)); ad='Ocak 2027 tahmini (%'+num(parseFloat(d)*100,2)+' zam)';}
  var bedel=BG*k, ek=ay*BE*k, top=bedel+ek;
  var rows=[['Memur aylık katsayısı',num(k,6)],['Bedel (300.000 × katsayı)',tl(bedel)]];
  if(ay>0){rows.push(['Ek bedel ('+ay+' ay × 3.500 × katsayı)',tl(ek)]); rows.push(['Toplam ödenecek',tl(top),'hl']);}
  return {main:['Bedelli askerlik ücreti', tl(top)], sub:ad+(ay>0?' · '+ay+' ay ek bedel dahil':''), rows:rows,
    note:'7179 sayılı Askeralma Kanunu 9. madde. Ek bedel, yoklama kaçağı, bakaya veya saklı durumunda geçen her ay için alınır; 1–30 gün bir ay sayılır. Bu durumdakilere ayrıca idari para cezası uygulanabilir. Ocak 2027 tutarları memur zammına göre tahmindir; kesin tutarı Milli Savunma Bakanlığı açıklar.'};
}''',
article=f'''<h2 id="nasil">Bedelli askerlik ücreti nasıl hesaplanır?</h2>
<p>7179 sayılı Askeralma Kanunu’nun 9. maddesine göre bedelli askerlik ücreti, <b>300.000 gösterge rakamının</b> ödemenin yapıldığı gün geçerli <b>memur aylık katsayısıyla</b> çarpılmasıyla bulunur. Memur aylık katsayısı her yıl Ocak ve Temmuz’da güncellendiği için bedelli ücreti de yılda iki kez değişir.</p>
<div class="formula">Bedelli askerlik ücreti = 300.000 × memur aylık katsayısı</div>
<div class="example"><p><b>Örnek:</b> Temmuz–Aralık 2026 döneminde katsayı 1,575512’dir: 300.000 × 1,575512 = <b>{_b2(BED_G * BED_K)} ₺</b>. Milli Savunma Bakanlığı’nın bu dönem için açıkladığı tutar da budur.</p></div>

<h2 id="donemler">Dönemlere göre bedelli askerlik ücreti</h2>
{BED_TABLO}
<p>17 Nisan 2026’dan önce gösterge rakamı 240.000 olduğu için bedel daha düşüktü. Ocak 2027 tutarı, memurların alacağı %5 toplu sözleşme zammı ile enflasyon farkına bağlıdır; zam oranı Aralık enflasyonu açıklandığında, Ocak başında kesinleşir. Senaryoların ayrıntısı için <a href="/memur-emekli-zammi-hesaplama.html">memur zammı hesaplama</a> sayfasına bakabilirsiniz.</p>

<h2 id="ocak">Ocak’tan önce ödemek avantajlı mı?</h2>
<p>Bedel, ödemenin yapıldığı gündeki katsayıyla hesaplanır. Bu yüzden Aralık sonuna kadar yapılan ödemelerde Temmuz–Aralık 2026 tutarı ({_b2(BED_G * BED_K)} ₺) geçerlidir; Ocak 2027’de katsayı artınca bedel de yaklaşık {_b2(BED_G * BED_K * 0.0547)[:-3]} – {_b2(BED_G * BED_K * 0.0801)[:-3]} ₺ artacak. Başvuru ve ödeme tarihlerini Milli Savunma Bakanlığı’nın dönem duyurusundan kontrol edin.</p>

<h2 id="ek">Yoklama kaçağı ve bakaya için ek bedel</h2>
<p>Yoklama kaçağı, bakaya veya saklı durumunda olanlar bedelli askerlikten yararlanmak için bedele ek olarak, bu durumda geçen <b>her ay için 3.500 gösterge × memur aylık katsayısı</b> kadar ek bedel öder. 1 ile 30 gün arası süre bir ay sayılır. Temmuz–Aralık 2026 döneminde aylık ek bedel <b>{_b2(BED_EK * BED_K)} ₺</b>’dir. Bu durumdakilere Askeralma Kanunu’na göre ayrıca idari para cezası uygulanabilir.</p>''',
faq=[('Bedelli askerlik ücreti 2026’da ne kadar?', f'1 Temmuz – 31 Aralık 2026 döneminde bedelli askerlik ücreti {_b2(BED_G * BED_K)} ₺’dir (300.000 × 1,575512).'),
     ('Ocak 2027’de bedelli askerlik ne kadar olacak?', f'Memur zammı senaryolarına göre Ocak 2027’de bedel yaklaşık {_b2(BED_G * BED_K * 1.0547)[:-3]} ile {_b2(BED_G * BED_K * 1.0801)[:-3]} ₺ arasında olacak. Kesin tutar Ocak başında memur katsayısı açıklanınca belli olur.'),
     ('Bedelli askerlik ücreti nasıl hesaplanır?', '300.000 gösterge rakamı, ödeme günündeki memur aylık katsayısıyla çarpılır. Katsayı Ocak ve Temmuz’da güncellendiği için ücret yılda iki kez değişir.'),
     ('Yoklama kaçağı bedelli ücreti ne kadar?', f'Bedele ek olarak kaçak ya da bakaya geçen her ay için 3.500 × memur aylık katsayısı kadar ek bedel ödenir. Temmuz–Aralık 2026’da aylık ek bedel {_b2(BED_EK * BED_K)} ₺’dir; ayrıca idari para cezası uygulanabilir.')],
related=['memur-emekli-zammi-hesaplama', 'memur-maaslari', 'yas-hesaplama', 'gun-hesaplama', 'net-maas-hesaplama'],
sources=[('7179 sayılı Askeralma Kanunu (madde 9)', 'https://www.mevzuat.gov.tr/'), ('Milli Savunma Bakanlığı – bedelli askerlik duyuruları', 'https://www.msb.gov.tr/')],
badges=['✓ Ücretsiz', 'Güncel: 472.653,60 ₺', 'Ocak 2027 Tahmini'],
))

import json
# ───────────────────────── EMEKLİ İKRAMİYESİ (MEMUR, 5434 m.89 / 5510 ek 82) ─────────────────────────
# İkramiye = her tam hizmet yılı için emekliliğe esas 1 aylık tutar. 1 aylık tutar:
#   (gösterge + ek gösterge) × aylık katsayı + 1.000 × taban aylık katsayısı + min(yıl,25) × 20 × aylık katsayı
#   + 9.500 × aylık katsayı × yansıtma oranı (mülga 5434 ek 70 oranları, 5510 geç. 4 ile uygulanır)
# Doğrulama: 1500 + 8000, 25+ yıl → 73.729,87 TL = Temmuz–Aralık 2026 kıdem tazminatı tavanı (ÇSGB).
# 30 yıl sınırı AYM 25.12.2014 E.2013/111 K.2014/195 (RG 7.1.2015) ile kaldırıldı.
EI_K, EI_TK = 1.575512, 25.794915
EI_ORAN = [(8400, 2.55), (7600, 2.15), (6400, 1.95), (4800, 1.65), (3600, 1.45), (2200, 0.85), (0, 0.55)]
EI_GOST = {1: [1320, 1380, 1440, 1500], 2: [1155, 1210, 1265, 1320, 1380, 1440], 3: [1020, 1065, 1110, 1155, 1210, 1265, 1320, 1380],
           4: [915, 950, 985, 1020, 1065, 1110, 1155, 1210, 1265], 5: [835, 865, 895, 915, 950, 985, 1020, 1065, 1110],
           6: [760, 785, 810, 835, 865, 895, 915, 950, 985], 7: [705, 720, 740, 760, 785, 810, 835, 865, 895],
           8: [660, 675, 690, 705, 720, 740, 760, 785, 810], 9: [620, 630, 645, 660, 675, 690, 705, 720, 740],
           10: [590, 600, 610, 620, 630, 645, 660, 675, 690], 11: [560, 570, 580, 590, 600, 610, 620, 630, 645],
           12: [545, 550, 555, 560, 570, 580, 590, 600, 610], 13: [530, 535, 540, 545, 550, 555, 560, 570, 580],
           14: [515, 520, 525, 530, 535, 540, 545, 550, 555], 15: [500, 505, 510, 515, 520, 525, 530, 535, 540]}
def _ei_oran(eg):
    return next(o for e, o in EI_ORAN if eg >= e)
def _ei(g, eg, y, k=EI_K, tk=EI_TK):
    p = [(g + eg) * k, 1000 * tk, min(y, 25) * 20 * k, 9500 * k * _ei_oran(eg)]
    return p, sum(p), sum(p) * y
assert abs(_ei(1500, 8000, 25)[1] - 73729.87) < 0.01, 'emekli ikramiyesi formülü kıdem tavanıyla tutmuyor'
EI_ORNEK = [('1/4', 1500, 3600, 20), ('1/4', 1500, 3600, 25), ('1/4', 1500, 3600, 30), ('1/4', 1500, 3600, 35),
            ('1/4', 1500, 4800, 30), ('1/4', 1500, 2200, 25), ('1/4', 1500, 0, 25), ('3/1', 1020, 0, 20)]
EI_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Derece/kademe</th><th>Ek gösterge</th><th>Hizmet yılı</th><th>1 aylık tutar</th><th>Emekli ikramiyesi (Temmuz–Aralık 2026)</th></tr></thead><tbody>'
    + ''.join(f'<tr><td>{d}</td><td>{tl(eg) if eg else "Yok"}</td><td>{y}</td><td>{_b2(_ei(g, eg, y)[1])} ₺</td><td><b>{_b2(_ei(g, eg, y)[2])} ₺</b></td></tr>' for d, g, eg, y in EI_ORNEK)
    + '</tbody></table></div>')
EI_ORAN_T = ('<div class="table-wrap"><table><thead><tr><th>Ek gösterge</th><th>Yansıtma oranı</th><th>Tazminat tutarı (9.500 × 1,575512 × oran)</th></tr></thead><tbody>'
    + ''.join(f'<tr><td>{lab}</td><td>%{int(round(o*100))}</td><td>{_b2(9500 * EI_K * o)} ₺</td></tr>' for lab, o in
              [('8.400 ve üzeri', 2.55), ('7.600 – 8.399', 2.15), ('6.400 – 7.599', 1.95), ('4.800 – 6.399', 1.65), ('3.600 – 4.799', 1.45), ('2.200 – 3.599', 0.85), ('2.200’den az veya yok', 0.55)])
    + '</tbody></table></div>')
_p, _a, _t = _ei(1500, 3600, 25)
EI_SEN_T = ('<div class="table-wrap"><table><thead><tr><th>Dönem</th><th>Aylık katsayı</th><th>1/4, 3.600 ek gösterge, 25 yıl</th><th>1/4, 3.600 ek gösterge, 30 yıl</th></tr></thead><tbody>'
    f'<tr><td><b>1 Temmuz – 31 Aralık 2026 (güncel)</b></td><td>1,575512</td><td><b>{_b2(_t)} ₺</b></td><td><b>{_b2(_ei(1500, 3600, 30)[2])} ₺</b></td></tr>'
    + ''.join(f'<tr><td>Ocak 2027 – {ad.lower()}</td><td>≈ {str(round(EI_K*(1+z), 6)).replace(".", ",")}</td><td>≈ {_b2(_ei(1500, 3600, 25, EI_K*(1+z), EI_TK*(1+z))[2])} ₺</td><td>≈ {_b2(_ei(1500, 3600, 30, EI_K*(1+z), EI_TK*(1+z))[2])} ₺</td></tr>' for ad, z in BED_SEN)
    + '</tbody></table></div>')
_dopts = ''.join(f'<option value="{d}"{" selected" if d == 1 else ""}>{d}. derece</option>' for d in range(1, 16))
TOOLS.append(dict(
slug='emekli-ikramiyesi-hesaplama', name='Emekli İkramiyesi Hesaplama', cat='kamu', ico='🏅',
title='Emekli İkramiyesi Hesaplama 2026 – Memur İkramiyesi Ne Kadar? | Hesaplarsın',
desc=f'Memur emekli ikramiyesi hesaplama 2026: derece, kademe, ek gösterge ve hizmet yılını girin. 1/4, 3.600 ek gösterge, 25 yıl: {_b2(_t)[:-3]} TL. Ocak 2027 tahmini.',
h1='🏅 Emekli İkramiyesi Hesaplama 2026 – Memur ve 4/C',
lead='Memur emekli ikramiyesi, her tam hizmet yılı için emekliliğe esas bir aylık tutar kadardır. Derecenizi, kademenizi, ek göstergenizi ve hizmet yılınızı girin; Temmuz–Aralık 2026 katsayılarıyla ikramiyenizi ve kalem kalem dökümünü, Ocak 2027 tahminiyle birlikte görün.',
card_title='Emekli İkramiyesi Hesaplayıcı', button='Hesapla',
form=f'''<div class="form-grid">
  <div class="field"><label for="derece">Derece</label><select id="derece">{_dopts}</select></div>
  <div class="field"><label for="kademe">Kademe</label><select id="kademe"></select></div>
  <div class="field"><label for="ekg">Ek gösterge <small>bordronuzda yazar; yoksa 0</small></label><input type="number" id="ekg" value="3600" inputmode="numeric" list="ekgl"><datalist id="ekgl"><option value="0"><option value="2200"><option value="3000"><option value="3600"><option value="4800"><option value="6400"><option value="7000"><option value="7600"><option value="8000"></datalist></div>
  <div class="field"><label for="yil">Tam hizmet yılı <small>ay kesirleri sayılmaz</small></label><input type="number" id="yil" value="25" inputmode="numeric"></div>
  <div class="field full"><label for="donem">Dönem</label><select id="donem"><option value="guncel">1 Temmuz – 31 Aralık 2026 (güncel katsayılar)</option>''' + ''.join(f'<option value="{z}">Ocak 2027 – {ad.lower()}</option>' for ad, z in BED_SEN) + '''</select></div>
</div>''',
js=f'var EK={EI_K}, ETK={EI_TK}, GOST={json.dumps(EI_GOST)}, ORAN={json.dumps(EI_ORAN)};' + r'''
function kademeDoldur(){var d=el('derece').value, s=el('kademe'), eski=s.value; s.innerHTML='';
  GOST[d].forEach(function(g,i){var o=document.createElement('option'); o.value=g; o.textContent=(i+1)+'. kademe – '+g+' gösterge'; s.appendChild(o);});
  s.selectedIndex=GOST[d].length-1;}
document.addEventListener('DOMContentLoaded',function(){kademeDoldur(); el('derece').addEventListener('change',kademeDoldur);});
if(document.readyState!=='loading'){kademeDoldur(); el('derece').addEventListener('change',kademeDoldur);}
function oranBul(eg){for(var i=0;i<ORAN.length;i++){if(eg>=ORAN[i][0]) return ORAN[i][1];} return 0.55;}
function hesapla(){
  if(!el('kademe').value) kademeDoldur();
  var g=parseFloat(el('kademe').value), eg=Math.max(0,v('ekg')||0), y=Math.floor(v('yil')||0), d=el('donem').value;
  if(!(y>=1)) return 'Tam hizmet yılınızı girin (en az 1).'; if(y>45) return 'Hizmet yılı 45’ten büyük olamaz.'; if(eg>9000) return 'Ek gösterge 9.000’den büyük olamaz.';
  var k=EK, tk=ETK, ad='1 Temmuz – 31 Aralık 2026';
  if(d!=='guncel'){var z=parseFloat(d); k=EK*(1+z); tk=ETK*(1+z); ad='Ocak 2027 tahmini (%'+num(z*100,2)+' zam)';}
  var o=oranBul(eg), a1=(g+eg)*k, a2=1000*tk, a3=Math.min(y,25)*20*k, a4=9500*k*o, ay=a1+a2+a3+a4, top=ay*y;
  return {main:['Emekli ikramiyesi', tl(top)], sub:ad+' · '+y+' yıl × '+tl(ay)+' (1 aylık tutar)',
    rows:[['Gösterge + ek gösterge aylığı (('+g+' + '+eg+') × '+num(k,6)+')',tl(a1)],['Taban aylığı (1.000 × '+num(tk,6)+')',tl(a2)],
          ['Kıdem aylığı ('+Math.min(y,25)+' yıl × 20 × katsayı)',tl(a3)],['Tazminat yansıtması (9.500 × katsayı × %'+Math.round(o*100)+')',tl(a4)],
          ['Emekliliğe esas 1 aylık tutar',tl(ay)],['Hizmet yılı',String(y)],['Emekli ikramiyesi',tl(top),'hl']],
    note:'5434 sayılı Kanun m.89 (5510 kapsamındaki 4/C’liler için ek m.82). İkramiye gelir vergisinden istisnadır (GVK m.25/7). 30 yıl sınırı 7 Ocak 2015’ten beri uygulanmıyor. Makam, görev veya temsil tazminatı alanlarda, SSK/Bağ-Kur’da geçen veya daha önce ikramiyesi ödenmiş sürelerde tutar farklı olur; kesin tutar SGK’nın emeklilik onayındadır. Ocak 2027 tutarı memur zammına göre tahmindir.'};
}''',
article=f'''<h2 id="nasil">Memur emekli ikramiyesi nasıl hesaplanır?</h2>
<p>5434 sayılı Emekli Sandığı Kanunu’nun 89. maddesine göre emekli olan memura <b>her tam hizmet yılı için emekliliğe esas bir aylık tutar</b> kadar emekli ikramiyesi ödenir. 2008 Ekim’inden sonra memur olanlar (5510 sayılı Kanun 4/C) da aynı esaslarla ikramiye alır. Bir aylık tutar dört kalemden oluşur:</p>
<div class="formula">1 aylık tutar = (gösterge + ek gösterge) × aylık katsayı + 1.000 × taban aylık katsayısı + kıdem aylığı + tazminat yansıtması<br>Emekli ikramiyesi = 1 aylık tutar × tam hizmet yılı</div>
<ul>
<li><b>Gösterge ve ek gösterge aylığı:</b> Derece-kademe göstergeniz (ör. 1. derece 4. kademe için 1.500) ile ek göstergeniz toplanıp memur aylık katsayısıyla (Temmuz–Aralık 2026: 1,575512) çarpılır.</li>
<li><b>Taban aylığı:</b> 1.000 × taban aylık katsayısı (Temmuz–Aralık 2026: 25,794915) = {_b2(1000*EI_TK)} ₺. Herkes için aynıdır.</li>
<li><b>Kıdem aylığı:</b> Her hizmet yılı için 20 gösterge, en fazla 25 yıl (500 gösterge) × aylık katsayı. 25 yılda {_b2(500*EI_K)} ₺.</li>
<li><b>Tazminat yansıtması:</b> En yüksek devlet memurunun gösterge toplamı olan 9.500 × aylık katsayı, ek göstergenize göre belirlenen oranla çarpılır (tablo aşağıda).</li>
</ul>
<div class="example"><p><b>Örnek:</b> 1/4 derece (1.500), 3.600 ek gösterge, 25 yıl hizmet: (1.500 + 3.600) × 1,575512 = {_b2(_p[0])} ₺; taban aylığı {_b2(_p[1])} ₺; kıdem aylığı 500 × 1,575512 = {_b2(_p[2])} ₺; tazminat 9.500 × 1,575512 × %145 = {_b2(_p[3])} ₺. Bir aylık tutar <b>{_b2(_a)} ₺</b>, ikramiye {_b2(_a)} × 25 = <b>{_b2(_t)} ₺</b>.</p></div>
<p>Formülün doğruluğunu kontrol etmenin kolay bir yolu var: en yüksek devlet memuru (1.500 + 8.000 gösterge, 25+ yıl) için bir yıllık ikramiye 73.729,87 ₺ çıkar. Bu tutar, Çalışma ve Sosyal Güvenlik Bakanlığı’nın açıkladığı Temmuz–Aralık 2026 <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı tavanının</a> ta kendisidir, çünkü tavan bu ikramiyeye bağlıdır.</p>

<h2 id="tablo">Örnek emekli ikramiyesi tutarları (Temmuz–Aralık 2026)</h2>
{EI_TABLO}

<h2 id="oran">Ek göstergeye göre tazminat yansıtma oranları</h2>
<p>İkramiyeye yansıyan tazminat, ek göstergenizin bulunduğu gruba göre değişir. Bu oranlar mülga 5434 sayılı Kanun ek 70. maddesindeki oranlardır ve 5510 sayılı Kanun’un geçici 4. maddesi uyarınca uygulanmaya devam eder.</p>
{EI_ORAN_T}
<p>Bu yüzden ek göstergedeki küçük bir fark ikramiyeyi ciddi değiştirebilir: 3.599 ile 3.600 ek gösterge arasında yansıtma oranı %85’ten %145’e çıkar.</p>

<h2 id="ocak">Ocak 2027’de emekli ikramiyesi ne kadar olacak?</h2>
<p>İkramiye, emekliliğin başladığı tarihteki katsayılarla hesaplanır. Ocak 2027’de memur aylık katsayısı ve taban aylık katsayısı memur zammı oranında artacağı için, Ocak’ta emekli olanın ikramiyesi de aynı oranda yükselir. Zam oranı Aralık enflasyonu açıklandığında kesinleşir; senaryolar <a href="/memur-emekli-zammi-hesaplama.html">memur zammı hesaplama</a> sayfasındaki yöntemle hesaplanmıştır.</p>
{EI_SEN_T}

<h2 id="30yil">30 yıl sınırı kalktı mı?</h2>
<p>Evet. Eskiden ikramiye en fazla 30 hizmet yılı için ödeniyordu. Anayasa Mahkemesi bu sınırı iptal etti (25.12.2014, E.2013/111, K.2014/195); karar 7 Ocak 2015’te Resmî Gazete’de yayımlandı. Bu tarihten sonra emekli olanlara 30 yılı aşan tam yıllar için de ikramiye ödenir. Kıdem aylığı ise hâlâ en fazla 25 yıl üzerinden hesaplanır.</p>

<h2 id="kimler">Kimler emekli ikramiyesi alır?</h2>
<p>Emekli ikramiyesi memurlara (5434 sayılı Kanun’a tabi olanlar ve 5510 sayılı Kanun 4/C kapsamındakiler) ödenir. SSK’lı (4/A) çalışanlara emekli ikramiyesi yerine işverenin ödediği <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı</a>, Bağ-Kur’lulara (4/B) ise ikramiye ödenmez. Memuriyetten önce SSK veya Bağ-Kur’da geçen süreler ve daha önce ikramiye ya da kıdem tazminatı ödenmiş süreler ikramiye hesabına girmez.</p>
<p>Emekli ikramiyesi gelir vergisinden istisnadır (Gelir Vergisi Kanunu m.25/7). Hesaplayıcı brüt ikramiyeyi gösterir; varsa kesintiler SGK’nın ödeme dökümünde yer alır.</p>''',
faq=[('Emekli ikramiyesi nasıl hesaplanır?', f'Memur emekli ikramiyesi, emekliliğe esas bir aylık tutarın tam hizmet yılı ile çarpılmasıyla bulunur. Bir aylık tutar; gösterge ve ek gösterge aylığı, taban aylığı, kıdem aylığı ve ek göstergeye göre tazminat yansıtmasından oluşur. 1/4 derece, 3.600 ek gösterge ve 25 yıl için Temmuz–Aralık 2026’da ikramiye {_b2(_t)} ₺’dir.'),
     ('25 yıllık memurun emekli ikramiyesi ne kadar?', f'1/4 derece ve 3.600 ek göstergeli bir memur için 25 yıllık ikramiye Temmuz–Aralık 2026 katsayılarıyla {_b2(_t)} ₺’dir. Ek gösterge ve derece-kademe farklıysa tutar değişir; hesaplayıcıya kendi bilgilerinizi girin.'),
     ('30 yıldan fazla hizmet için ikramiye ödenir mi?', 'Evet. Anayasa Mahkemesi’nin 7 Ocak 2015’te yayımlanan kararıyla 30 yıl sınırı kaldırıldı; bu tarihten sonra emekli olanlara 30 yılı aşan tam yıllar için de ikramiye ödenir. Kıdem aylığı ise en fazla 25 yıl üzerinden hesaplanır.'),
     ('Emekli ikramiyesinden vergi kesilir mi?', 'Emekli ikramiyesi Gelir Vergisi Kanunu’nun 25/7. maddesi gereği gelir vergisinden istisnadır. Kesin ödeme tutarını SGK’nın emeklilik onayı ve ödeme dökümünde görebilirsiniz.'),
     ('SSK ve Bağ-Kur emeklileri ikramiye alır mı?', 'Hayır. Emekli ikramiyesi memurlara ödenir. SSK’lı (4/A) işçiler emeklilikte işverenden kıdem tazminatı alır; Bağ-Kur’lulara ikramiye ödenmez. Bayram ikramiyesi ise ayrı bir ödemedir.'),
     ('Ocak 2027’de emekli olursam ikramiyem artar mı?', 'Evet. İkramiye emekliliğin başladığı tarihteki katsayılarla hesaplanır. Ocak 2027’de memur katsayıları zam oranında artacağı için ikramiye de yaklaşık aynı oranda yükselir; zam oranı Ocak başında kesinleşir.')],
related=['kidem-tazminati-hesaplama', 'memur-emekli-zammi-hesaplama', 'memur-maaslari', 'emekli-maasi-hesaplama', 'emeklilik-yasi-hesaplama'],
sources=[('5434 sayılı T.C. Emekli Sandığı Kanunu (m.89)', 'https://www.mevzuat.gov.tr/MevzuatMetin/1.3.5434.pdf'),
         ('ÇSGB – Temmuz 2026 kıdem tazminatı tavanı hesap tablosu', 'https://csgb.gov.tr/Media/5vuhphpb/kıdem-tazminatı-2026_temmuz-dönem.pdf'),
         ('Anayasa Mahkemesi kararı E.2013/111, K.2014/195 (30 yıl sınırı)', 'https://normkararlarbilgibankasi.anayasa.gov.tr/'),
         ('Memurlar.net – Özel hizmet aylığı (tazminat) oranları', 'https://www.memurlar.net/haber/1008033/emekli-maasinda-ozel-hizmet-ayligi-nedir-ve-nasil-hesaplanmaktadir.html')],
badges=['✓ Ücretsiz', 'Temmuz 2026 katsayıları', 'Ocak 2027 Tahmini'],
))
