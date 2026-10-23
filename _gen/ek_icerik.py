"""İnce araç sayfaları için ek içerik (AdSense "düşük değerli içerik" riskine karşı).
build.py, araç listesi yüklendikten sonra EK[slug] içindeki makale bölümlerini ve SSS'leri ilgili araca ekler.
Tablolardaki tüm sayılar aşağıdaki fonksiyonlarla HESAPLANIR (elle yazılmaz) — formül değişirse tablo da değişir.
Fiyat/tarife gibi sık değişen değerler kullanılmaz; tablolar fiyattan bağımsız tutulur.
"""
import math


def f(x, d=0):
    """Türkçe sayı biçimi: 1.234,5"""
    s = f'{x:,.{d}f}'
    return s.replace(',', '§').replace('.', ',').replace('§', '.')


def tablo(basliklar, satirlar):
    h = ''.join(f'<th>{b}</th>' for b in basliklar)
    r = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in s) + '</tr>' for s in satirlar)
    return f'<div class="table-wrap"><table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'


EK = {}

# ───────────── TAKDİR / TEŞEKKÜR ─────────────
_h = 35
EK['takdir-tesekkur-hesaplama'] = dict(article=f'''
<h2 id="hangi-ders">Hangi dersin notu ortalamayı daha çok etkiler?</h2>
<p>Dönem sonu ortalaması ağırlıklı hesaplandığı için her dersin etkisi haftalık ders saatiyle orantılıdır. Haftada {_h} saat ders gören bir öğrenci için bir dersteki <b>10 puanlık artışın</b> ortalamaya etkisi:</p>
''' + tablo(['Dersin haftalık saati', 'Ortalamaya etkisi (+10 puan)', 'Örnek ders'], [
    ['1 saat', '+' + f(10 * 1 / _h, 2), 'Seçmeli / rehberlik'], ['2 saat', '+' + f(10 * 2 / _h, 2), 'Görsel sanatlar, beden eğitimi'],
    ['3 saat', '+' + f(10 * 3 / _h, 2), 'Yabancı dil, fen dersleri'], ['4 saat', '+' + f(10 * 4 / _h, 2), 'Fen bilimleri (ortaokul)'],
    ['5 saat', '+' + f(10 * 5 / _h, 2), 'Türkçe / Türk dili ve edebiyatı'], ['6 saat', '+' + f(10 * 6 / _h, 2), 'Matematik (bazı sınıflar)']]) + f'''
<p>Ders saatleri sınıf düzeyine ve okul türüne göre değişir; kendi ders programınızdaki saatleri hesaplayıcıya girerek gerçek etkiyi görebilirsiniz.</p>

<h2 id="kac-puan-eksik">Takdire kaç puan eksiğim var? Örnek hesap</h2>
<p>Ortalamanız 82,40 ve haftalık toplam ders saatiniz {_h} ise takdir sınırı olan 85,00’e ulaşmak için gereken ek “puan × saat” miktarı:</p>
<div class="formula">(85,00 − 82,40) × {_h} = {f((85 - 82.4) * _h, 0)} puan·saat</div>
<div class="example"><p>Bu açığı kapatmanın birkaç yolu: 5 saatlik bir dersi <b>{f((85 - 82.4) * _h / 5, 1)} puan</b>, 4 saatlik bir dersi <b>{f((85 - 82.4) * _h / 4, 1)} puan</b> veya hem 3 saatlik hem 2 saatlik iki dersi ayrı ayrı yaklaşık <b>{f((85 - 82.4) * _h / 5, 1)} puan</b> yükseltmek.</p></div>
<p>Pratik ipucu: Notunuzu yükseltmenin en kolay olduğu ders ile ders saati en yüksek dersin kesişimine odaklanın. Az saatli bir derste 100 almak, çok saatli bir derste 5 puan artıştan daha az etki yaratabilir.</p>
''', faq=[('Takdir için hangi derse çalışmalıyım?', 'Haftalık ders saati en yüksek ve notunuzun hâlâ yükselebileceği derslere öncelik verin. 5 saatlik bir derste 10 puan artış, 35 saatlik programda ortalamayı yaklaşık 1,43 puan yükseltir.')])

# ───────────── DOĞAL GAZ ─────────────
_k = lambda m3, isil=9155: m3 * isil / 860.42
EK['dogalgaz-faturasi-hesaplama'] = dict(article='''
<h2 id="m3-kwh-tablo">m³ – kWh dönüşüm tablosu</h2>
<p>Faturanızdaki kWh değerini kontrol etmek için aşağıdaki tabloyu kullanabilirsiniz. Değerler ortalama 9.155 kcal/m³ üst ısıl değerle hesaplanmıştır:</p>
''' + tablo(['Tüketim', 'kWh karşılığı', 'Tipik dönem'], [
    [f'{m} m³', f(_k(m), 0) + ' kWh', d] for m, d in [(25, 'Yaz ayı, sadece sıcak su'), (50, 'Bahar / sonbahar'), (100, 'Kış, küçük daire'),
                                                      (150, 'Kış, 2+1 daire'), (200, 'Kış, 3+1 daire'), (300, 'Soğuk kış, büyük ev')]]) + f'''
<h2 id="isil-deger-etkisi">Isıl değer faturayı ne kadar değiştirir?</h2>
<p>Aynı metreküp tüketimde, gazın ısıl değeri ay ay değiştiği için faturadaki kWh de değişir. 180 m³ tüketim için:</p>
''' + tablo(['Üst ısıl değer', 'kWh', 'Ortalamaya göre fark'], [
    [f(i) + ' kcal/m³', f(_k(180, i), 0), ('%' + ('+' if i >= 9155 else '−') + f(abs(_k(180, i) / _k(180) - 1) * 100, 1)) if i != 9155 else 'Referans']
    for i in (9000, 9100, 9155, 9250, 9350)]) + '''
<p>Fark küçük görünse de kış aylarında yüzlerce metreküp tüketildiğinde fatura tutarına birkaç yüz liraya kadar yansıyabilir. Bu yüzden farklı aylara ait faturaları karşılaştırırken m³ değil kWh değerine bakmak daha doğrudur.</p>
<h2 id="okuma">Faturanızı adım adım kontrol edin</h2>
<ol>
<li>Faturadaki ilk ve son endeks farkından m³ tüketimi bulun.</li>
<li>Bu değeri faturadaki üst ısıl değerle çarpıp 860,42’ye bölün; kWh’i bulursunuz.</li>
<li>kWh’i birim fiyatla çarpın; sonuç vergiler öncesi gaz bedeline yakın olmalıdır.</li>
<li>Okuma süresinin kaç gün olduğuna bakın: 35 günlük bir dönem, 30 günlük döneme göre doğal olarak daha yüksek tüketim gösterir.</li>
</ol>
''', faq=[('100 m³ doğal gaz kaç kWh eder?', f'Ortalama 9.155 kcal/m³ ısıl değerle 100 m³ yaklaşık {f(_k(100), 0)} kWh’e eşittir. Kesin değer için faturanızdaki ısıl değeri kullanın.')])

# ───────────── İNTERNET HIZI ─────────────
def _sure(gb, mbps):
    s = gb * 8000 / mbps
    if s < 60: return f(s, 0) + ' sn'
    if s < 3600: return f(s / 60, 0) + ' dk'
    return f(s / 3600, 1) + ' saat'


_hiz = [16, 50, 100, 500, 1000]
EK['internet-hizi-donusturucu'] = dict(article='''
<h2 id="indirme-sureleri">Hızınıza göre indirme süreleri</h2>
<p>Paket hızının pratikte ne anlama geldiğini görmek için yaygın dosya boyutlarının teorik indirme sürelerini hesapladık (1 GB = 8.000 megabit, bağlantının tam hızda çalıştığı varsayımıyla):</p>
''' + tablo(['Dosya'] + [f'{h} Mbps' for h in _hiz], [
    [ad] + [_sure(gb, h) for h in _hiz] for ad, gb in [('Fotoğraf albümü (200 MB)', 0.2), ('Film – HD (4 GB)', 4), ('Telefon güncellemesi (6 GB)', 6),
                                                         ('Oyun (50 GB)', 50), ('Büyük oyun (150 GB)', 150)]]) + '''
<p>Gerçek süre genellikle %10–30 daha uzundur: Wi-Fi kayıpları, sunucunun gönderim hızı ve ağdaki diğer cihazlar hızı düşürür. Dosya boyutundan süre hesaplamak için <a href="/dosya-indirme-suresi-hesaplama.html">dosya indirme süresi hesaplama</a> aracını kullanabilirsiniz.</p>
<h2 id="test">Hız testini doğru yapmak</h2>
<ul>
<li>Testi mümkünse modeme kablo ile bağlı bir bilgisayardan yapın; Wi-Fi testi modem yerine kablosuz bağlantıyı ölçer.</li>
<li>Test sırasında diğer cihazlardaki indirmeleri ve video akışlarını durdurun.</li>
<li>Günün farklı saatlerinde (özellikle 20:00–23:00 yoğunluğunda) en az üç test yapıp ortalamasını alın.</li>
<li>Sonucu Mbps olarak not edin; bu tablodaki gibi MB/s’ye çevirmek için 8’e bölün.</li>
</ul>
''', faq=[('100 Mbps ile 50 GB oyun kaç dakikada iner?', f'Teorik olarak {_sure(50, 100)} sürer (50 × 8.000 ÷ 100 saniye). Pratikte sunucu ve Wi-Fi kayıplarıyla bu süre biraz uzar.')])

# ───────────── KÂR / ZARAR ─────────────
def _kz(alis, satis, masraf):
    m = alis + masraf; k = satis - m
    return [f(masraf) + ' ₺', f(k) + ' ₺', '%' + f(k / m * 100, 1), '%' + f(k / satis * 100, 1)]


def _ind(maliyet, fiyat, ind):
    s = fiyat * (1 - ind / 100); k = s - maliyet; k0 = fiyat - maliyet
    return [f'%{ind}', f(s) + ' ₺', f(k) + ' ₺', '%' + f((1 - k / k0) * 100, 0)]


EK['kar-zarar-hesaplama'] = dict(article='''
<h2 id="masraf-etkisi">Ek masrafların kâra etkisi</h2>
<p>Alış fiyatı 500 ₺, satış fiyatı 800 ₺ olan bir ürünü düşünelim. Kargo, komisyon ve ambalaj gibi birim başı masraflar arttıkça kâr nasıl eriyor?</p>
''' + tablo(['Birim masraf', 'Birim kâr', 'Kâr oranı', 'Kâr marjı'], [_kz(500, 800, m) for m in (0, 50, 100, 150, 200)]) + '''
<p>Tabloda görüldüğü gibi 150 ₺’lik masraf, kâğıt üzerindeki %60’lık kâr oranını yarıdan fazla düşürür. Online satışta masrafları birim maliyete eklemeden yapılan hesap, gerçek kârı olduğundan çok daha yüksek gösterir.</p>
<h2 id="indirim-etkisi">İndirim yapınca kârın ne kadarı gider?</h2>
<p>Maliyeti 700 ₺, normal satış fiyatı 1.000 ₺ olan bir ürün (birim kâr 300 ₺) için indirim oranına göre kâr:</p>
''' + tablo(['İndirim', 'İndirimli fiyat', 'Kalan kâr', 'Kârdaki erime'], [_ind(700, 1000, i) for i in (5, 10, 15, 20, 25, 30)]) + '''
<p>%10’luk bir indirim kârın üçte birini götürür; %30 indirimde ise ürün maliyetine satılır. İndirimin kârı korumak için ne kadar ek satış gerektirdiğini görmek için <a href="/indirim-hesaplama.html">indirim hesaplama</a> ve <a href="/kar-marji-hesaplama.html">kâr marjı hesaplama</a> araçlarını birlikte kullanabilirsiniz.</p>
''', faq=[('%20 indirim yaparsam kârım ne kadar azalır?', 'Kâr marjınıza bağlıdır. Maliyeti 700 ₺, fiyatı 1.000 ₺ olan üründe %20 indirim kârı 300 ₺’den 100 ₺’ye, yani üçte birine düşürür.')])

# ───────────── NOT ORTALAMASI ─────────────
EK['not-ortalamasi-hesaplama'] = dict(article='''
<h2 id="ikinci-donem">Yıl sonu ortalaması için ikinci dönem ne almalıyım?</h2>
<p>Ortaöğretimde bir dersin yıl sonu puanı, iki dönem puanının aritmetik ortalamasıdır. Hedeflediğiniz yıl sonu puanına ulaşmak için ikinci dönemde gereken puan:</p>
<div class="formula">Gereken 2. dönem puanı = Hedef × 2 − 1. dönem puanı</div>
''' + tablo(['1. dönem puanı', 'Hedef 50 (geçme)', 'Hedef 70', 'Hedef 85'], [
    [f(d1)] + [(f(h * 2 - d1) if h * 2 - d1 <= 100 else 'Ulaşılamaz') if h * 2 - d1 > 0 else '—' for h in (50, 70, 85)] for d1 in (30, 40, 50, 60, 70, 80, 90)]) + '''
<p>Örneğin birinci dönem 40 alan bir öğrencinin dersten geçmesi için ikinci dönemde en az 60 alması gerekir. Takdir ve teşekkür ise her dönem ayrı değerlendirilir; dönem ortalamanızı hesaplayıcının üst bölümünde ders saatleriyle birlikte hesaplayabilirsiniz.</p>
<h2 id="gano-ornek">Üniversitede GANO: kredili örnek</h2>
<p>Bir dönemde dört ders alan bir öğrencinin ağırlıklı ortalaması şöyle hesaplanır:</p>
''' + tablo(['Ders', 'Kredi (AKTS)', 'Harf notu', 'Katsayı', 'Kredi × katsayı'], [
    ['Matematik I', '6', 'BA', '3,50', f(6 * 3.5, 1)], ['Fizik I', '5', 'CB', '2,50', f(5 * 2.5, 1)],
    ['İngilizce', '3', 'AA', '4,00', f(3 * 4, 1)], ['Programlama', '6', 'BB', '3,00', f(6 * 3, 1)],
    ['<b>Toplam</b>', '<b>20</b>', '', '', '<b>' + f(6 * 3.5 + 5 * 2.5 + 12 + 18, 1) + '</b>']]) + f'''
<p>Dönem ortalaması = {f(6 * 3.5 + 5 * 2.5 + 12 + 18, 1)} ÷ 20 = <b>{f((6 * 3.5 + 5 * 2.5 + 12 + 18) / 20, 2)}</b>. Harf notu katsayıları üniversiteden üniversiteye küçük farklılıklar gösterebilir; kendi üniversitenizin yönetmeliğini kontrol edin.</p>
''', faq=[('1. dönem 45 aldım, geçmek için 2. dönem kaç almalıyım?', 'Yıl sonu puanı iki dönemin ortalaması olduğu için 50 × 2 − 45 = 55 puan almanız gerekir.')])

# ───────────── VERİ KULLANIMI ─────────────
_saat = {'Video 480p': 0.3, 'Video 720p (HD)': 0.7, 'Video 1080p': 1.5, 'Instagram / TikTok': 0.6, 'Görüntülü görüşme': 0.8, 'Müzik akışı': 0.07}
EK['veri-kullanim-hesaplama'] = dict(article='''
<h2 id="paket-ne-kadar">Paketim kaç saat yeter?</h2>
<p>Hesaplayıcının kullandığı saatlik tüketim değerleriyle, yaygın paket büyüklüklerinin her bir etkinlik için tek başına kaç saat yettiğini hesapladık:</p>
''' + tablo(['Etkinlik', '10 GB', '20 GB', '40 GB'], [
    [ad] + [f(gb / s, 0) + ' saat' for gb in (10, 20, 40)] for ad, s in _saat.items()]) + '''
<p>Örneğin 20 GB’lık bir paket, yalnızca 1080p video izlenirse yaklaşık 13 saatte biter; aynı paketle 280 saatten fazla müzik dinlenebilir. Kısa video uygulamaları videolar otomatik oynadığı için en çok fark edilmeden veri tüketen uygulamalardır.</p>
<h2 id="gunluk-butce">Aylık paketi günlük bütçeye çevirin</h2>
''' + tablo(['Aylık paket', 'Günlük ortalama', 'Günde HD video karşılığı'], [
    [f'{gb} GB', f(gb * 1000 / 30, 0) + ' MB', f(gb / 30 / 0.7 * 60, 0) + ' dk'] for gb in (10, 20, 30, 50)]) + '''
<p>Ayın ilk yarısında paketin yarısından fazlasını harcadıysanız, telefonunuzun ayarlarından uygulama bazında veri kullanımına bakarak en çok tüketen uygulamayı bulun ve video kalitesini düşürün.</p>
''', faq=[('20 GB internet kaç saat video izler?', f'Yaklaşık değerlerle 720p (HD) kalitede {f(20 / 0.7, 0)} saat, 1080p kalitede {f(20 / 1.5, 0)} saat, 480p kalitede ise {f(20 / 0.3, 0)} saat video izlenebilir.')])

# ───────────── HEDEF KİLO ─────────────
EK['hedef-kilo-suresi-hesaplama'] = dict(article='''
<h2 id="aciga-gore">Günlük kalori açığına göre haftalık kayıp</h2>
<p>1 kg yağ ≈ 7.700 kcal varsayımıyla, sürdürülen günlük açığın haftalık ve aylık karşılığı:</p>
''' + tablo(['Günlük açık', 'Haftalık kayıp', '30 günde', '5 kg için süre'], [
    [f(a) + ' kcal', f(a * 7 / 7700, 2) + ' kg', f(a * 30 / 7700, 1) + ' kg', f(5 / (a * 7 / 7700), 0) + ' hafta'] for a in (250, 400, 500, 750, 1000)]) + '''
<p>Bu tablo teorik bir üst sınırdır: Kilo verdikçe günlük enerji ihtiyacınız azaldığı için aynı açığı korumak giderek zorlaşır. Bu nedenle ilerleyen haftalarda kayıp hızının yavaşlaması normaldir.</p>
<h2 id="acik-nasil">Kalori açığı nasıl oluşturulur?</h2>
<ul>
<li><b>Beslenme:</b> Günlük ihtiyacınızı <a href="/gunluk-kalori-ihtiyaci-hesaplama.html">günlük kalori ihtiyacı</a> aracıyla bulun ve ondan 300–500 kcal eksik alın. Şekerli içecekleri bırakmak tek başına günde 200–300 kcal açık sağlayabilir.</li>
<li><b>Hareket:</b> 70 kg’lık biri için 45 dakikalık normal tempolu yürüyüş yaklaşık 190 kcal yakar; ayrıntı için <a href="/kalori-yakma-hesaplama.html">kalori yakma hesaplama</a> aracını kullanın.</li>
<li><b>Protein:</b> Kilo verirken kas kaybını sınırlamak için protein alımını korumak önemlidir. İhtiyacınızı <a href="/protein-ihtiyaci-hesaplama.html">protein ihtiyacı</a> aracıyla görebilirsiniz.</li>
</ul>
''', faq=[('Günde 500 kalori açıkla ayda kaç kilo verilir?', f'Teorik olarak 500 × 30 ÷ 7.700 ≈ {f(500 * 30 / 7700, 1)} kg. İlk haftalarda su kaybıyla daha hızlı, sonrasında daha yavaş ilerleme görülebilir.')])

# ───────────── PRİM ─────────────
_kad = [(100000, 0.02), (200000, 0.03), (None, 0.05)]


def _prim(satis):
    kalan, alt, top = satis, 0, 0
    for ust, o in _kad:
        dilim = (min(satis, ust) if ust else satis) - alt
        if dilim <= 0: break
        top += dilim * o; alt = ust or alt
    return top


EK['prim-hesaplama'] = dict(article='''
<h2 id="kademeli-ornek">Kademeli prim: satış tutarına göre örnek tablo</h2>
<p>Aşağıdaki örnek sistemde ilk 100.000 ₺ satış için %2, 100.000–200.000 ₺ arası için %3, 200.000 ₺ üzeri için %5 prim ödeniyor (her oran yalnızca kendi dilimine uygulanır):</p>
''' + tablo(['Aylık satış', 'Brüt prim', 'Ortalama prim oranı', 'Düz %3 sistemle'], [
    [f(s) + ' ₺', f(_prim(s)) + ' ₺', '%' + f(_prim(s) / s * 100, 2), f(s * 0.03) + ' ₺'] for s in (80000, 150000, 250000, 400000)]) + '''
<p>Kademeli sistem düşük satışta düz orandan daha az, yüksek satışta daha fazla prim öder; bu nedenle hedefi aşan satışı ödüllendirmek için tercih edilir. Kendi sisteminizi hesaplayıcıya girerek karşılaştırabilirsiniz.</p>
<h2 id="pazarlik">Prim sisteminde nelere dikkat edilmeli?</h2>
<ul>
<li><b>Matrah:</b> Prim cirodan mı, tahsil edilen tutardan mı, yoksa kâr üzerinden mi hesaplanıyor? İadeler ve iptaller primden düşülüyor mu?</li>
<li><b>Ödeme dönemi:</b> Aylık mı, çeyreklik mi? Ayrılırsanız hak edilmiş prim ödeniyor mu?</li>
<li><b>Yazılı olması:</b> Prim sisteminin iş sözleşmesinde veya yazılı bir prim yönetmeliğinde yer alması, olası anlaşmazlıklarda en güçlü dayanaktır.</li>
<li><b>Net etkisi:</b> Prim brüt ücrete eklendiği için yüksek primli aylarda gelir vergisi dilimi yükselebilir; net etkiyi <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracıyla görebilirsiniz.</li>
</ul>
''', faq=[('Kademeli primde 250.000 ₺ satışa ne kadar prim düşer?', f'%2 / %3 / %5 kademeli örnek sistemde: 100.000 × %2 + 100.000 × %3 + 50.000 × %5 = {f(_prim(250000))} ₺ brüt prim.')])

# ───────────── KPSS NET ─────────────
EK['kpss-net-hesaplama'] = dict(article='''
<h2 id="net-tablo">Doğru ve yanlış sayısına göre net tablosu</h2>
<p>KPSS’de 4 yanlış 1 doğruyu götürür (net = doğru − yanlış ÷ 4). 60 soruluk bir testte farklı senaryolar:</p>
''' + tablo(['Doğru', 'Yanlış', 'Boş', 'Net', 'Kaybedilen net'], [
    [str(d), str(y), str(60 - d - y), f(d - y / 4, 2), f(y / 4, 2)] for d, y in [(40, 0), (40, 8), (40, 20), (45, 12), (50, 8), (52, 8), (55, 4)]]) + '''
<p>Aynı 40 doğruyla 20 yanlış yapan aday, hiç yanlış yapmayan adaydan 5 net geride kalır. Emin olmadığınız soruda iki şıkkı eleyebiliyorsanız işaretlemek genellikle beklenen değer açısından avantajlıdır; hiç fikriniz yoksa boş bırakmak daha güvenlidir.</p>
<h2 id="tahmin">Tahmin etmek mantıklı mı?</h2>
<p>5 şıklı bir soruda rastgele işaretlemenin beklenen net katkısı sıfırdır: %20 ihtimalle +1, %80 ihtimalle −0,25. Ancak iki şık elenmişse doğru cevap olasılığı %33’e çıkar ve beklenen katkı <b>+''' + f(1 / 3 - 2 / 3 * 0.25, 2) + ''' net</b> olur. Üç şık elendiğinde bu değer <b>+''' + f(0.5 - 0.5 * 0.25, 2) + ''' net</b>’e yükselir.</p>
''', faq=[('KPSS’de boş bırakmak mı tahmin etmek mi?', 'Hiç fikriniz yoksa boş bırakın; rastgele işaretlemenin beklenen katkısı sıfırdır. En az iki şıkkı eleyebiliyorsanız işaretlemek ortalamada net kazandırır.')])

# ───────────── ROI ─────────────
def _yil(r, n): return ((1 + r) ** (1 / n) - 1) * 100


EK['roi-hesaplama'] = dict(article='''
<h2 id="yilliklandirma">Aynı ROI, farklı süre: yıllık getiri tablosu</h2>
<p>Toplam ROI tek başına yanıltıcıdır; %50 getirinin 1 yılda mı yoksa 5 yılda mı elde edildiği büyük fark yaratır. Bileşik yıllık getiri (CAGR) ile karşılaştırma:</p>
''' + tablo(['Toplam ROI', '1 yılda', '2 yılda', '3 yılda', '5 yılda'], [
    ['%' + f(r * 100)] + ['%' + f(_yil(r, n), 1) for n in (1, 2, 3, 5)] for r in (0.2, 0.5, 1.0, 2.0)]) + '''
<div class="formula">Yıllık getiri = (1 + Toplam ROI)<sup>1 ÷ yıl</sup> − 1</div>
<p>Örneğin 5 yılda %100 getiri (paranızın ikiye katlanması), yıllık bazda yaklaşık %14,9’a karşılık gelir. Bu oranı aynı dönemdeki enflasyon ve mevduat faiziyle karşılaştırmak, yatırımın gerçekten kazandırıp kazandırmadığını gösterir. Bunun için <a href="/enflasyon-hesaplama.html">enflasyon hesaplama</a> ve <a href="/mevduat-faizi-hesaplama.html">mevduat faizi hesaplama</a> araçlarını kullanabilirsiniz.</p>
<h2 id="reklam-ornek">Örnek: reklam kampanyası ROI’si</h2>
<p>Bir işletme reklama 20.000 ₺ harcıyor ve kampanyadan 90.000 ₺ ciro elde ediyor. Ürünlerin ortalama brüt kâr marjı %30 ise:</p>
<div class="example"><p>Kampanyadan gelen brüt kâr = 90.000 × %30 = <b>27.000 ₺</b></p><p>ROI = (27.000 − 20.000) ÷ 20.000 = <b>%35</b> · ROAS = 90.000 ÷ 20.000 = <b>4,5</b></p></div>
<p>ROAS 4,5 kulağa çok iyi gelse de gerçek getiri kâr marjına bağlıdır. Marj %20 olsaydı brüt kâr 18.000 ₺ olur ve kampanya zarar ederdi.</p>
''', faq=[('5 yılda %100 getiri yıllık kaç yüzdeye eşittir?', 'Bileşik olarak yaklaşık %14,9’dur: (1 + 1)^(1/5) − 1. Basitçe 100’ü 5’e bölmek (%20) gerçek yıllık getiriyi olduğundan yüksek gösterir.')])

# ───────────── MAAŞ ZAM ─────────────
def _reel(z, e): return ((1 + z / 100) / (1 + e / 100) - 1) * 100


EK['maas-zam-hesaplama'] = dict(article='''
<h2 id="reel-tablo">Zam ve enflasyona göre reel değişim tablosu</h2>
<p>Satırlar aldığınız zammı, sütunlar aynı dönemdeki enflasyonu gösterir. Hücredeki değer, alım gücünüzdeki gerçek değişimdir:</p>
''' + tablo(['Zam \\ Enflasyon', '%25', '%30', '%35', '%40'], [
    ['%' + f(z)] + [('+' if _reel(z, e) >= 0 else '−') + '%' + f(abs(_reel(z, e)), 1) for e in (25, 30, 35, 40)] for z in (20, 25, 30, 35, 40, 50)]) + '''
<div class="formula">Reel değişim = (1 + Zam oranı) ÷ (1 + Enflasyon) − 1</div>
<p>Dikkat: Zam ile enflasyonu basitçe çıkarmak (örneğin %40 − %30 = %10) reel artışı olduğundan yüksek gösterir; doğru hesapla bu değer %7,7’dir. Geçmiş dönem enflasyonunu <a href="/enflasyon-hesaplama.html">enflasyon hesaplama</a> aracıyla bulabilirsiniz.</p>
<h2 id="kayip-telafi">Kaybı telafi etmek için gereken zam</h2>
<p>Son zammınızdan bu yana fiyatlar %X arttıysa, alım gücünüzü korumak için de tam %X zam gerekir. Ancak ara dönemde yaşanan kaybı da telafi etmek istiyorsanız daha yüksek bir oran talep etmeniz gerekir; çünkü maaşınız sabitken geçen her ay alım gücünüz biraz daha azalmıştır.</p>
''', faq=[('%40 zam aldım, enflasyon %30, gerçek artış ne kadar?', f'Reel artış (1,40 ÷ 1,30) − 1 ≈ %{f(_reel(40, 30), 1)}’dir; basit çıkarma ile bulunan %10 olduğundan yüksektir.')])

# ───────────── SU FATURASI ─────────────
EK['su-faturasi-hesaplama'] = dict(article='''
<h2 id="hane-tuketim">Hane büyüklüğüne göre aylık tüketim tahmini</h2>
<p>Konut içi tüketimi kişi başı günde 100, 130 ve 150 litre kabul ederek 30 günlük tahmini tüketim:</p>
''' + tablo(['Hane', 'Tasarruflu (100 L)', 'Ortalama (130 L)', 'Yüksek (150 L)'], [
    [f'{n} kişi'] + [f(n * l * 30 / 1000, 1) + ' m³' for l in (100, 130, 150)] for n in (1, 2, 3, 4, 5)]) + '''
<p>Faturanızdaki m³ değeri bu aralıkların belirgin şekilde üzerindeyse tesisat kaçağı ihtimalini kontrol etmekte fayda var. Bahçe sulaması, havuz veya sık çamaşır yıkama tüketimi doğal olarak artırır.</p>
<h2 id="kacak-maliyet">Küçük kaçaklar ne kadar su harcar?</h2>
''' + tablo(['Kaçak türü', 'Günlük kayıp (yaklaşık)', 'Aylık kayıp'], [
    ['Damlayan musluk (saniyede 1 damla)', '~20 L', f(20 * 30 / 1000, 1) + ' m³'], ['Sessizce akan rezervuar', '~200 L', f(200 * 30 / 1000, 1) + ' m³'],
    ['Belirgin akan rezervuar', '~1.000 L', f(1000 * 30 / 1000, 0) + ' m³']]) + '''
<p>Sızdıran bir rezervuar, tek kişilik bir hanenin aylık tüketimine yakın miktarda suyu boşa harcayabilir. Rezervuara birkaç damla gıda boyası damlatın; sifonu çekmeden klozet içinde renk görünüyorsa sızıntı vardır.</p>
''', faq=[('4 kişilik aile ayda kaç m³ su harcar?', 'Kişi başı günde 130 litre konut içi tüketimle yaklaşık 15,6 m³ harcar; tasarruflu kullanımda bu değer 12 m³ civarına iner.')])

# ───────────── SU İHTİYACI ─────────────
EK['su-ihtiyaci-hesaplama'] = dict(article='''
<h2 id="aktivite-tablo">Kilo ve egzersize göre toplam günlük su</h2>
<p>Hesaplayıcının formülüyle (kilo × 33 ml + her 30 dakika egzersiz için 350 ml), ılıman havada toplam sıvı ihtiyacı:</p>
''' + tablo(['Kilo', 'Egzersiz yok', '30 dk egzersiz', '60 dk egzersiz', '90 dk egzersiz'], [
    [f'{k} kg'] + [f(k * 0.033 + d / 30 * 0.35, 1) + ' L' for d in (0, 30, 60, 90)] for k in (50, 60, 70, 80, 90, 100)]) + '''
<p>Değerler içecek ve yiyeceklerden gelen toplam sıvıyı kapsar; yaklaşık %20’si besinlerden karşılandığı için içilmesi gereken miktar tablodakinden biraz azdır.</p>
<h2 id="gun-plani">Örnek bir günlük su planı (2,3 litre)</h2>
''' + tablo(['Zaman', 'Miktar'], [['Uyanınca', '1 bardak (200 ml)'], ['Kahvaltıda', '1 bardak (200 ml)'], ['Öğleye kadar', '1 şişe (500 ml)'],
                                   ['Öğle yemeğinde', '1 bardak (200 ml)'], ['Öğleden sonra', '1 şişe (500 ml)'], ['Akşam yemeğinde', '1 bardak (200 ml)'],
                                   ['Akşam', '2,5 bardak (500 ml)'], ['<b>Toplam</b>', '<b>2,3 L</b>']]) + '''
<p>Suyu gün içine yaymak, akşam saatlerinde bir anda çok su içmekten daha konforludur ve gece uykunuzu bölme ihtimalini azaltır.</p>
''', faq=[('70 kilo ve günde 1 saat spor yapan biri ne kadar su içmeli?', f'Formüle göre 70 × 0,033 + 2 × 0,35 ≈ {f(70 * 0.033 + 0.7, 1)} litre toplam sıvı; sıcak havada 0,5 litre daha eklenebilir.')])

# ───────────── KALORİ YAKMA ─────────────
_met = [('Normal yürüyüş (5 km/s)', 3.5), ('Ağırlık antrenmanı (orta)', 5.0), ('Bisiklet (orta)', 8.0), ('Koşu (10 km/s)', 9.8)]
EK['kalori-yakma-hesaplama'] = dict(article='''
<h2 id="kiloya-gore">Kiloya göre 1 saatte yakılan kalori</h2>
<p>Aynı aktivitede harcanan enerji vücut ağırlığıyla doğru orantılıdır. Compendium MET değerleriyle 60 dakika için hesaplanmıştır:</p>
''' + tablo(['Aktivite'] + [f'{k} kg' for k in (55, 70, 85, 100)], [
    [ad] + [f(m * 3.5 * k / 200 * 60, 0) + ' kcal' for k in (55, 70, 85, 100)] for ad, m in _met]) + '''
<h2 id="yiyecek-esdeger">Yediklerinizi yakmak için ne kadar hareket gerekir?</h2>
<p>70 kg’lık bir yetişkin için yaygın yiyeceklerin enerjisini harcamak için gereken yaklaşık süre:</p>
''' + tablo(['Yiyecek (yaklaşık kalori)', 'Normal yürüyüş', 'Koşu (10 km/s)'], [
    [y, f(kc / (3.5 * 3.5 * 70 / 200), 0) + ' dk', f(kc / (9.8 * 3.5 * 70 / 200), 0) + ' dk'] for y, kc in
    [('1 dilim ekmek (~70 kcal)', 70), ('1 kutu kola (~140 kcal)', 140), ('1 simit (~300 kcal)', 300), ('1 dilim baklava (~200 kcal)', 200), ('1 dürüm (~600 kcal)', 600)]]) + '''
<p>Bu tablo, kilo yönetiminde beslenmenin egzersizden daha belirleyici olmasının nedenini gösterir: bir simitlik enerjiyi yürüyerek harcamak yaklaşık 1 saat sürer.</p>
''', faq=[('85 kiloluk biri 1 saat yürüyüşte kaç kalori yakar?', f'Normal tempoda (3,5 MET) yaklaşık {f(3.5 * 3.5 * 85 / 200 * 60, 0)} kcal yakar.')])

# ───────────── YAKIT MALİYETİ ─────────────
EK['yakit-maliyeti-hesaplama'] = dict(article='''
<h2 id="litre-tablo">Mesafe ve tüketime göre gereken yakıt (litre)</h2>
<p>Fiyatlar sık değiştiği için tabloyu litre cinsinden hazırladık; sonucu güncel litre fiyatıyla çarpmanız yeterli:</p>
''' + tablo(['Mesafe', '5 L/100 km', '6 L/100 km', '7 L/100 km', '8 L/100 km', '10 L/100 km'], [
    [f(km) + ' km'] + [f(km * t / 100, 1) + ' L' for t in (5, 6, 7, 8, 10)] for km in (100, 250, 450, 600, 1000)]) + '''
<div class="example"><p><b>Örnek:</b> 100 km’de 7 litre yakan bir araçla 450 km’lik yol için 31,5 litre gerekir. Litre fiyatı 45 ₺ olsaydı yakıt maliyeti 31,5 × 45 = 1.417,5 ₺ olurdu.</p></div>
<h2 id="fiyat-etkisi">Fiyat artışı yolculuğa ne kadar yansır?</h2>
<p>Litre fiyatındaki her 1 ₺’lik artış, 100 km’de 7 litre yakan bir araçta her 100 km için 7 ₺ ek maliyet demektir. Yılda 15.000 km yol yapan bir sürücü için bu, yıllık yaklaşık 1.050 litre yakıt ve <b>her 1 ₺ zam için 1.050 ₺</b> ek gider anlamına gelir.</p>
''', faq=[('1000 km yol kaç litre benzin yakar?', 'Aracın tüketimine bağlıdır: 100 km’de 6 litre yakan araç 60 litre, 8 litre yakan araç 80 litre harcar. Sonucu güncel litre fiyatıyla çarpın.')])

# ───────────── STOK KÂRLILIĞI ─────────────
EK['stok-karliligi-hesaplama'] = dict(article='''
<h2 id="ornek-karsilastirma">Örnek: iki ürünün stok kârlılığı</h2>
<p>Aynı mağazadaki iki ürünü karşılaştıralım. A ürününün marjı düşük ama hızlı dönüyor; B ürününün marjı yüksek ama yavaş satılıyor:</p>
''' + tablo(['Gösterge', 'A ürünü', 'B ürünü'], [
    ['Yıllık satış (maliyet bazında)', '600.000 ₺', '300.000 ₺'], ['Brüt kâr marjı', '%20', '%40'],
    ['Yıllık brüt kâr', f(600000 / 0.8 * 0.2) + ' ₺', f(300000 / 0.6 * 0.4) + ' ₺'], ['Ortalama stok (maliyet)', '50.000 ₺', '100.000 ₺'],
    ['Stok devir hızı', f(600000 / 50000, 0) + ' kez/yıl', f(300000 / 100000, 0) + ' kez/yıl'],
    ['Stokta kalma süresi', f(365 / 12, 0) + ' gün', f(365 / 3, 0) + ' gün'],
    ['GMROI (brüt kâr ÷ ortalama stok)', f(600000 / 0.8 * 0.2 / 50000, 2), f(300000 / 0.6 * 0.4 / 100000, 2)]]) + '''
<p>B ürünü daha yüksek marjlı görünse de stoğa bağlanan her 1 ₺ için A ürünü 3 ₺, B ürünü 2 ₺ brüt kâr üretir. Raf alanı ve nakit sınırlıysa A ürünü daha verimlidir.</p>
<h2 id="olu-stok">Ölü stok maliyeti</h2>
<p>Satılmayan stok yalnızca bağlanan para değildir; depolama, sigorta, fire ve enflasyon karşısında değer kaybı da yaratır. Bu maliyetler genellikle yıllık stok değerinin %20–30’u olarak tahmin edilir. 100.000 ₺’lik bir yıl boyunca satılmayan stok, işletmeye 20.000–30.000 ₺ gizli maliyet yükleyebilir.</p>
''', faq=[('Düşük marjlı ürün mü yüksek marjlı ürün mü daha kârlı?', 'Tek başına marja bakılmaz. Brüt kârın ortalama stoğa oranı (GMROI) daha iyi bir göstergedir: hızlı dönen düşük marjlı ürün, yavaş dönen yüksek marjlı üründen daha kârlı olabilir.')])

# ───────────── YAKIT TÜKETİMİ ─────────────
EK['yakit-tuketimi-hesaplama'] = dict(article='''
<h2 id="km-litre">L/100 km ↔ km/L dönüşüm tablosu</h2>
<p>Bazı araç bilgisayarları ve yabancı kaynaklar tüketimi “1 litreyle kaç km” olarak gösterir. İki birim arasındaki dönüşüm:</p>
''' + tablo(['L/100 km', 'km/L', '1.000 km için yakıt'], [
    [f(t, 1), f(100 / t, 1), f(t * 10, 0) + ' L'] for t in (4, 5, 5.5, 6, 6.5, 7, 8, 9, 10, 12)]) + '''
<div class="formula">km/L = 100 ÷ (L/100 km)</div>
<h2 id="depo-yontemi">Depo doldurma yöntemiyle doğru ölçüm</h2>
<ol>
<li>Depoyu tabancanın otomatik kestiği noktaya kadar doldurun ve kilometre sayacını sıfırlayın.</li>
<li>Normal kullanımınıza devam edin; en az 300–400 km yol yapın.</li>
<li>Aynı istasyonda, mümkünse aynı pompada depoyu yine tabanca kesene kadar doldurun.</li>
<li>Alınan litreyi gidilen kilometreye bölüp 100 ile çarpın. Üç dolumun ortalaması tek ölçümden çok daha güvenilirdir.</li>
</ol>
<p>Araç bilgisayarlarının gösterdiği ortalama tüketim genellikle gerçek değerden %3–8 daha iyimserdir.</p>
''', faq=[('1 litre ile 15 km gitmek 100 km’de kaç litre eder?', f'100 ÷ 15 ≈ {f(100 / 15, 1)} L/100 km’dir.')])

# ───────────── DAMGA VERGİSİ ─────────────
EK['damga-vergisi-hesaplama'] = dict(article='''
<h2 id="kira-tablo">Kira sözleşmesi damga vergisi tablosu (binde 1,89)</h2>
<p>Kira sözleşmelerinde vergi, sözleşme süresince ödenecek toplam kira üzerinden hesaplanır. 12 aylık sözleşmeler için:</p>
''' + tablo(['Aylık kira', 'Yıllık toplam (matrah)', 'Damga vergisi (1 nüsha)'], [
    [f(k) + ' ₺', f(k * 12) + ' ₺', f(k * 12 * 1.89 / 1000, 2) + ' ₺'] for k in (10000, 15000, 20000, 30000, 50000)]) + '''
<p>Süresi belirsiz kira sözleşmelerinde uygulamada bir yıllık kira bedeli esas alınır. Sözleşme birden fazla nüsha imzalanıyorsa her nüsha için ayrıca vergi doğar.</p>
<h2 id="sozlesme-tablo">Genel sözleşmeler için örnekler (binde 9,48)</h2>
''' + tablo(['Sözleşme bedeli', '1 nüsha', '2 nüsha'], [
    [f(t) + ' ₺', f(t * 9.48 / 1000, 2) + ' ₺', f(t * 9.48 / 1000 * 2, 2) + ' ₺'] for t in (100000, 250000, 500000, 1000000, 5000000)]) + '''
<p>Nüsha sayısı vergi tutarını doğrudan katladığı için, taraflardan yalnızca birinin elinde asıl nüsha kalacak şekilde düzenleme yapmak ve diğer tarafa onaylı suret vermek uygulamada sık tercih edilen bir yoldur. Kesin uygulama için bir mali müşavire danışmanız önerilir.</p>
''', faq=[('Aylık 15.000 ₺ kira için damga vergisi ne kadar?', f'12 aylık sözleşmede 180.000 × 1,89 ÷ 1000 = {f(180000 * 1.89 / 1000, 2)} ₺ (tek nüsha).')])

# ───────────── PROTEİN ─────────────
EK['protein-ihtiyaci-hesaplama'] = dict(article='''
<h2 id="kilo-tablo">Kiloya göre günlük protein tablosu</h2>
''' + tablo(['Kilo', 'Hareketsiz (0,8 g/kg)', 'Aktif (1,2 g/kg)', 'Kilo verirken (1,6 g/kg)', 'Kas kazanımı (2,0 g/kg)'], [
    [f'{k} kg'] + [f(k * r, 0) + ' g' for r in (0.8, 1.2, 1.6, 2.0)] for k in (50, 60, 70, 80, 90, 100)]) + '''
<h2 id="ornek-menu">Örnek: yaklaşık ''' + f(2 * 6 + 0.6 * 17 + 1.5 * 31 + 5 + 2 * 10 + 0.2 * 21 + 2.5 * 9 + 3, 0) + ''' g protein içeren bir gün</h2>
''' + tablo(['Öğün', 'İçerik', 'Protein (yaklaşık)'], [
    ['Kahvaltı', '2 yumurta + 60 g beyaz peynir', f(2 * 6 + 0.6 * 17, 0) + ' g'], ['Öğle', '150 g tavuk göğsü + bulgur pilavı', f(1.5 * 31 + 5, 0) + ' g'],
    ['Ara öğün', '200 g süzme yoğurt + 20 g badem', f(2 * 10 + 0.2 * 21, 0) + ' g'], ['Akşam', '1,5 porsiyon mercimek yemeği (250 g) + 1 dilim ekmek', f(2.5 * 9 + 3, 0) + ' g'],
    ['<b>Toplam</b>', '', '<b>' + f(2 * 6 + 0.6 * 17 + 1.5 * 31 + 5 + 2 * 10 + 0.2 * 21 + 2.5 * 9 + 3, 0) + ' g</b>']]) + '''
<p>Değerler yaklaşıktır ve pişirme yöntemine göre değişir. Protein ihtiyacınızı karşılarken toplam kalori ihtiyacınızı da gözetmek için <a href="/gunluk-kalori-ihtiyaci-hesaplama.html">günlük kalori ihtiyacı</a> aracını kullanabilirsiniz.</p>
''', faq=[('80 kilo biri günde kaç gram protein almalı?', 'Hareketsiz bir yetişkin için yaklaşık 64 g (0,8 g/kg); düzenli ağırlık antrenmanı yapan biri için 128–176 g (1,6–2,2 g/kg) aralığı önerilir.')])

# ───────────── ELEKTRİK FATURASI ─────────────
_cihaz = [('LED ampul', 9, 5), ('Buzdolabı (A++ ortalama)', 45, 24), ('Televizyon (55")', 100, 4), ('Bilgisayar (masaüstü)', 200, 5),
          ('Çamaşır makinesi (yıkama başına ~1 kWh)', None, None), ('Klima (12.000 BTU, inverter)', 1000, 6), ('Elektrikli ısıtıcı', 2000, 4), ('Su ısıtıcısı (kettle)', 2000, 0.25)]
EK['elektrik-faturasi-hesaplama'] = dict(article='''
<h2 id="cihaz-kwh">Cihazların aylık tahmini tüketimi (kWh)</h2>
<p>Ortalama güç ve günlük kullanım süresi varsayımlarıyla 30 günlük tüketim. Tutarı bulmak için kWh değerini faturanızdaki birim fiyatla çarpın:</p>
''' + tablo(['Cihaz', 'Ortalama güç', 'Günlük kullanım', 'Aylık tüketim'], [
    ([ad, f(w) + ' W', (f(h, 2) if h < 1 else f(h, 0)) + ' saat', f(w * h * 30 / 1000, 1) + ' kWh'] if w else [ad, '—', 'Haftada 4 yıkama', f(4 * 4.3, 0) + ' kWh'])
    for ad, w, h in _cihaz]) + '''
<p>Buzdolabı kompresörü sürekli çalışmadığı için ortalama güç değeri kullanılmıştır. Klima ve ısıtıcı gibi yüksek güçlü cihazlar, birkaç saatlik kullanımla bile faturanın en büyük kalemine dönüşebilir.</p>
<h2 id="bekleme">Bekleme modunun yıllık maliyeti</h2>
<p>Televizyon, oyun konsolu, modem ve şarj cihazları kapalıyken de az miktarda elektrik çeker. Evdeki toplam bekleme gücü 15 W ise yıllık tüketim 15 × 24 × 365 ÷ 1000 = <b>''' + f(15 * 24 * 365 / 1000, 0) + ''' kWh</b> eder. Anahtarlı uzatma kablosuyla gece cihazları tamamen kapatmak bu tüketimi büyük ölçüde ortadan kaldırır.</p>
''', faq=[('Klima ayda kaç kWh elektrik harcar?', f'1.000 W ortalama çeken inverter bir klima günde 6 saat çalışırsa ayda yaklaşık {f(1000 * 6 * 30 / 1000, 0)} kWh harcar. Tutar için bunu faturanızdaki kWh fiyatıyla çarpın.')])

# ───────────── PAZARYERLERİ: platforma özgü fiyat kademesi tabloları ─────────────
# tools_pazaryeri ile aynı formül: komisyon KDV dahil fiyattan, komisyon ve hizmet bedeline %20 KDV, %1 stopaj KDV hariç fiyattan.
from tools_pazaryeri import P as _P


def _kesinti(F, r, H, kdv):
    Fh = F / (1 + kdv / 100); C = F * r / 100
    return C * 1.2 + H * 1.2 + Fh * 0.01


def _pz_tablo(platform, kat_index, kdv=None):
    ad, H, ks = _P[platform]; k = ks[kat_index]; r = k[1]; kdv = kdv or (k[2] if len(k) > 2 else 20)
    rows = []
    for F in (100, 250, 500, 1000, 2500):
        kes = _kesinti(F, r, H, kdv)
        rows.append([f(F) + ' ₺', f(kes, 2) + ' ₺', '%' + f(kes / F * 100, 1), f(F - kes, 2) + ' ₺'])
    return k[0], r, H, kdv, tablo(['Satış fiyatı (KDV dahil)', 'Toplam kesinti*', 'Kesinti oranı', 'Hesaba yatan (kargo hariç)'], rows)


def _pz(platform, kat_index, giris, sonuc, soru, ek='da', kdv=None):
    kat, r, H, kdv, t = _pz_tablo(platform, kat_index, kdv)
    ad = _P[platform][0]
    sabit = f(H * 1.2, 2)
    kucuk = _kesinti(100, r, H, kdv)
    return dict(article=f'''
<h2 id="fiyat-kademe">{ad}’{ek} fiyata göre kesinti oranı</h2>
<p>{giris} Aşağıdaki tablo <b>{kat}</b> {"" if platform == "shopier" else ""}(komisyon %{f(r, 2)}, ürün KDV’si %{kdv}) {"satış kademesi" if platform == "shopier" else "kategorisi"} için hesaplanmıştır:</p>
{t}
<p class="source-note">* Komisyon ve KDV’si, {sabit} ₺ (KDV dahil) sabit {"işlem ücreti" if platform == "shopier" else "hizmet bedeli"} ve %1 e-ticaret stopajı dahil; kargo ve ürün maliyeti hariç. Oranlar yaklaşıktır, kesin oran için satıcı panelinizi kontrol edin.</p>
<p>{sonuc}</p>
''', faq=[(soru, f'Bu kategoride 100 ₺’lik satışta toplam kesinti yaklaşık {f(kucuk, 2)} ₺ (%{f(kucuk, 1)}) olur; kargo ve ürün maliyeti ayrıca düşülür.')])


EK['trendyol-komisyon-hesaplama'] = _pz('trendyol', 0,
    'Trendyol’da sabit platform hizmet bedeli her siparişte aynı tutarda kesildiği için, düşük fiyatlı ürünlerde toplam kesintinin satışa oranı belirgin şekilde yükselir.',
    'Düşük fiyatlı ürünlerde sabit bedelin etkisini azaltmanın en etkili yolu ürünleri set veya paket halinde satmaktır: iki ürünü tek siparişte satmak sabit hizmet bedelini ve kargoyu bir kez öder.',
    'Trendyol’da 100 ₺’lik giyim ürününde toplam kesinti ne kadar?')
EK['hepsiburada-komisyon-hesaplama'] = _pz('hepsiburada', 0,
    'Hepsiburada’da komisyon oranları kategoriye göre Trendyol’dan düşük de yüksek de olabilir; giyimde daha düşüktür. Ancak sabit hizmet bedeli daha yüksek olduğu için küçük sepetlerde toplam kesinti artabilir.',
    'Bu nedenle Hepsiburada’da düşük fiyatlı ürünlerde fiyatı belirlerken sabit bedeli birim maliyete eklemek, yüksek fiyatlı ürünlerde ise komisyon oranına odaklanmak daha doğru bir yaklaşımdır. Aynı ürünün platformlar arası karşılaştırması için <a href="/pazaryeri-komisyon-hesaplama.html">pazaryeri komisyon hesaplama</a> aracını kullanabilirsiniz.',
    'Hepsiburada’da 100 ₺’lik giyim ürününde toplam kesinti ne kadar?')
EK['shopier-komisyon-hesaplama'] = _pz('shopier', 0,
    'Shopier bir pazaryeri değil, kendi müşterinize satış yaptığınız bir ödeme ve mağaza altyapısıdır; bu yüzden komisyon oranı pazaryerlerinin çok altındadır ve sabit işlem ücreti düşüktür.',
    'Karşılaştırma için: aynı 500 ₺’lik giyim satışında pazaryerlerinde toplam kesinti genellikle %20’nin üzerindeyken Shopier’de %10’un altında kalır. Ancak Shopier’de müşteriyi kendiniz bulursunuz; Instagram reklamı veya içerik üretimi için harcadığınız tutar bu farkın bir kısmını geri alır.',
    'Shopier’de 100 ₺’lik satışta toplam kesinti ne kadar?', ek='de', kdv=10)

# Genel pazaryeri sayfası: üç platform, aynı fiyat — fiyat seviyesine göre karşılaştırma
_rows = []
for F in (150, 500, 2000):
    rr = [f(F) + ' ₺']
    for pl, ki in (('trendyol', 0), ('hepsiburada', 0), ('shopier', 0)):
        ad, H, ks = _P[pl]; k = ks[ki]
        rr.append(f(F - _kesinti(F, k[1], H, 10), 2) + ' ₺')
    _rows.append(rr)
EK['pazaryeri-komisyon-hesaplama'] = dict(article='''
<h2 id="fiyat-seviyesi">Fiyat seviyesine göre platform karşılaştırması</h2>
<p>Giyim kategorisinde (ürün KDV’si %10), kargo hariç, satış başına hesabınıza yatan tutar. Pazaryerlerinde varsayılan komisyon oranları, Shopier’de yeni satıcı kademesi kullanılmıştır:</p>
''' + tablo(['Satış fiyatı', 'Trendyol', 'Hepsiburada', 'Shopier'], _rows) + '''
<p>Fark yalnızca komisyondan gelmez: Pazaryerleri müşteriyi size getirir, Shopier’de ise trafiği kendiniz oluşturursunuz. Doğru karşılaştırma için pazaryeri kesintisini, kendi kanalınızda müşteri kazanmak için harcayacağınız reklam bütçesiyle kıyaslayın.</p>
<h2 id="karar">Hangi kanal ne zaman mantıklı?</h2>
<ul>
<li><b>Yeni marka, takipçi kitlesi yok:</b> Pazaryerleri hazır trafik sağladığı için yüksek kesintiye rağmen ilk satışları almak için daha hızlıdır.</li>
<li><b>Sadık müşteri kitlesi veya güçlü sosyal medya hesabı var:</b> Shopier veya kendi siteniz, kesinti farkını doğrudan kârınıza ekler.</li>
<li><b>Düşük fiyatlı ürün:</b> Sabit hizmet bedellerinin oranı yükseldiği için paket satış veya minimum sepet tutarı belirlemek kârlılığı korur.</li>
<li><b>Yüksek fiyatlı ürün:</b> Sabit bedellerin etkisi azalır, belirleyici olan kategori komisyon oranıdır.</li>
</ul>
''', faq=[('150 ₺’lik ürün için hangi platform daha kârlı?', 'Giyim kategorisindeki örnek oranlarla 150 ₺’lik satışta hesaba yatan tutar Trendyol’da ' + _rows[0][1] + ', Hepsiburada’da ' + _rows[0][2] + ', Shopier’de ' + _rows[0][3] + ' olur (kargo hariç). Shopier’de müşteriyi kendiniz bulmanız gerektiğini unutmayın.')])

# ═════════════ 2. PARTİ ═════════════

# ───────────── İSKONTO ─────────────
def _esd(*o):
    k = 1
    for x in o: k *= (1 - x / 100)
    return (1 - k) * 100


_zin = [(10, 5), (20, 10), (20, 10, 5), (25, 10), (30, 10, 5), (40, 10), (50, 10, 5)]
EK['iskonto-hesaplama'] = dict(article='''
<h2 id="esdeger-tablo">Zincirleme iskontoların eşdeğer oranları</h2>
<p>Bayi ve toptan fiyat listelerinde sık görülen iskonto zincirlerinin tek bir orana karşılığı. Son sütun, oranları yanlışlıkla toplamanın ne kadar hata yaptırdığını gösterir:</p>
''' + tablo(['İskonto zinciri', 'Eşdeğer tek iskonto', 'Toplanırsa (yanlış)', '10.000 ₺ listede net fiyat'], [
    [' + '.join('%' + f(x) for x in z), '%' + f(_esd(*z), 2), '%' + f(sum(z)), f(10000 * (1 - _esd(*z) / 100), 2) + ' ₺'] for z in _zin]) + '''
<p>Örneğin “%20 + %10 + %5” iskonto, liste fiyatından %35 değil <b>%31,6</b> indirim demektir. Teklifleri karşılaştırırken her zaman eşdeğer orana veya doğrudan net fiyata bakın.</p>
<h2 id="hedef-net">İstediğim net fiyat için kaç iskonto gerekir?</h2>
<div class="formula">Gereken iskonto = 1 − (Hedef net fiyat ÷ Liste fiyatı)</div>
<div class="example"><p><b>Örnek:</b> Liste fiyatı 12.500 ₺ olan bir ürünü 9.000 ₺’ye almak istiyorsanız gereken toplam iskonto 1 − 9.000 ÷ 12.500 = <b>%28</b>. Satıcı zaten %20 veriyorsa, ikinci kademe olarak istemeniz gereken ek iskonto 1 − 0,72 ÷ 0,80 = <b>%10</b> olur.</p></div>
''', faq=[('%20 + %10 iskonto toplam kaç yüzde eder?', 'Toplam %30 değil, %28’dir: 1 − 0,80 × 0,90 = 0,28. İkinci iskonto, ilk iskontodan sonra kalan tutara uygulanır.')])

# ───────────── SAATLİK ÜCRET ─────────────
EK['saatlik-ucret-hesaplama'] = dict(article='''
<h2 id="maas-tablo">Brüt maaşa göre saatlik, günlük ve fazla mesai ücreti</h2>
<p>Aylık 225 saat ve 30 gün esasına göre hesaplanmıştır (fazla mesai: saatlik ücretin %50 fazlası):</p>
''' + tablo(['Aylık brüt', 'Günlük', 'Saatlik', 'Fazla mesai (1 saat)', 'Genel tatilde çalışma (ek ödeme, 1 gün)'], [
    [f(b, 2) + ' ₺', f(b / 30, 2) + ' ₺', f(b / 225, 2) + ' ₺', f(b / 225 * 1.5, 2) + ' ₺', f(b / 30, 2) + ' ₺'] for b in (33030, 40000, 50000, 60000, 80000, 100000)]) + '''
<p>Son sütun, ulusal bayram veya genel tatil gününde çalışan işçiye o gün için ödenen <b>ek</b> bir günlük ücreti gösterir; yani işçi o gün için toplamda iki günlük ücret alır. Tutarlar brüttür; net karşılığı için <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracını kullanın.</p>
<h2 id="serbest">Serbest çalışanlar saat ücretini nasıl belirler?</h2>
<p>Serbest çalışanlar ayın tamamını faturalayamaz; teklif hazırlama, iletişim, muhasebe ve boşta geçen süreler de vardır. Pratik bir yöntem:</p>
<div class="formula">Saat ücreti = (Hedef aylık gelir + Aylık işletme giderleri) ÷ Faturalanabilir saat</div>
<div class="example"><p><b>Örnek:</b> Aylık 60.000 ₺ gelir hedefi, 10.000 ₺ gider (muhasebe, yazılım, ekipman, sigorta) ve ayda 110 faturalanabilir saat: (60.000 + 10.000) ÷ 110 ≈ <b>''' + f(70000 / 110, 0) + ''' ₺/saat</b>. Vergi ve sosyal güvenlik primlerini de hedef gelire eklemeyi unutmayın.</p></div>
''', faq=[('50.000 ₺ brüt maaşın saatlik ücreti ne kadar?', f'50.000 ÷ 225 = {f(50000 / 225, 2)} ₺ brüt saatlik ücret; 1 saatlik fazla mesai {f(50000 / 225 * 1.5, 2)} ₺ eder.')])

# ───────────── METREKARE FİYAT ─────────────
EK['metrekare-fiyat-hesaplama'] = dict(article='''
<h2 id="hizli-tablo">m² fiyatına göre toplam fiyat tablosu</h2>
''' + tablo(['m² birim fiyatı', '75 m²', '100 m²', '125 m²', '150 m²'], [
    [f(p) + ' ₺'] + [f(p * m) + ' ₺' for m in (75, 100, 125, 150)] for p in (20000, 30000, 40000, 50000, 75000)]) + '''
<h2 id="net-fiyat">Net metrekare üzerinden gerçek birim fiyat</h2>
<p>İlanlardaki birim fiyat genellikle brüt alan üzerinden verilir. Kullanılabilir alanı karşılaştırmak için fiyatı net alana bölmek daha doğrudur. 4.000.000 ₺’lik, 120 m² brüt bir daire için:</p>
''' + tablo(['Net / brüt oranı', 'Net alan', 'Brüt m² fiyatı', 'Net m² fiyatı'], [
    ['%' + f(o), f(120 * o / 100, 0) + ' m²', f(4000000 / 120) + ' ₺', f(4000000 / (120 * o / 100)) + ' ₺'] for o in (85, 80, 75, 70)]) + '''
<p>Aynı ilan fiyatına sahip iki daireden net/brüt oranı düşük olanın kullanılabilir metrekaresi gerçekte %10–20 daha pahalıdır. Tapu ve iskân belgesindeki alanları ilanla karşılaştırmak bu yüzden önemlidir. Alım masraflarını görmek için <a href="/tapu-harci-hesaplama.html">tapu harcı hesaplama</a> aracını kullanabilirsiniz.</p>
''', faq=[('Brüt 120 m² daire net kaç m² olur?', 'Bina tipine göre genellikle %75–85 arasında, yani yaklaşık 90–102 m² net alan olur. Kesin değer tapu ve proje belgelerinde yazar.')])

# ───────────── VÜCUT YAĞ ORANI ─────────────
EK['vucut-yag-orani-hesaplama'] = dict(article='''
<h2 id="kutle">Yağ kütlesi ve yağsız kütle</h2>
<p>Yağ oranını kilogram cinsine çevirmek, ilerlemeyi takip etmeyi kolaylaştırır. 80 kg’lık biri için:</p>
''' + tablo(['Yağ oranı', 'Yağ kütlesi', 'Yağsız kütle (kas, kemik, su)'], [
    ['%' + f(o), f(80 * o / 100, 1) + ' kg', f(80 * (1 - o / 100), 1) + ' kg'] for o in (12, 15, 20, 25, 30, 35)]) + f'''
<h2 id="hedef-oran">Hedef yağ oranına ulaşmak için kaç kilo yağ verilmeli?</h2>
<p>Yağsız kütlenin korunduğu varsayımıyla hedef kilo şöyle bulunur:</p>
<div class="formula">Hedef kilo = Yağsız kütle ÷ (1 − Hedef yağ oranı)</div>
<div class="example"><p><b>Örnek:</b> 80 kg ve %25 yağ oranındaki birinin yağsız kütlesi 60 kg’dır. %20’ye inmek için hedef kilo 60 ÷ 0,80 = <b>75 kg</b>, yani yaklaşık <b>5 kg yağ</b> vermesi gerekir. %15 hedefi için bu değer {f(80 - 60 / 0.85, 1)} kg’dır.</p></div>
<p>Kilo verirken kas kaybını sınırlamak için yeterli protein alımı ve direnç antrenmanı önemlidir. Tartıdaki kilo aynı kalırken yağ oranının düşmesi, kas kazanıp yağ kaybettiğinizi gösterir; bu nedenle ölçümleri 2–4 haftada bir aynı koşullarda tekrarlayın.</p>
''', faq=[('80 kilo ve %25 yağ oranında kaç kilo yağ var?', '80 × 0,25 = 20 kg yağ ve 60 kg yağsız kütle vardır. %20’ye inmek için yaklaşık 5 kg yağ vermek gerekir.')])

# ───────────── YAŞ ─────────────
EK['yas-hesaplama'] = dict(article='''
<h2 id="yas-gun">Yaşa göre yaklaşık yaşanan gün, hafta ve saat</h2>
''' + tablo(['Yaş', 'Gün (yaklaşık)', 'Hafta', 'Saat'], [
    [str(y), f(y * 365.2425), f(y * 365.2425 / 7), f(y * 365.2425 * 24)] for y in (1, 10, 18, 25, 30, 40, 50, 65)]) + f'''
<p>Değerler artık yılları da hesaba katan ortalama yıl uzunluğuyla (365,2425 gün) hesaplanmıştır; kesin gün sayınız için hesaplayıcıya doğum tarihinizi girin.</p>
<h2 id="kilometre-taslari">Gün sayısıyla kilometre taşları</h2>
''' + tablo(['Kilometre taşı', 'Yaklaşık yaş karşılığı'], [
    [f(g) + '. gün', f(g / 365.2425, 1) + ' yaş'] for g in (1000, 5000, 10000, 15000, 20000, 25000)]) + '''
<p>10.000. gün yaklaşık 27 yaş 5 ay civarına denk gelir ve bazı insanlar bu günü ikinci bir doğum günü gibi kutlar. Doğum tarihinizi girerek kendi 10.000. gününüzün tam tarihini <a href="/gun-hesaplama.html">gün hesaplama</a> aracıyla bulabilirsiniz (doğum tarihine 10.000 gün ekleyin).</p>
''', faq=[('10.000 gün kaç yaş eder?', f'Yaklaşık {f(10000 / 365.2425, 2)} yıl, yani 27 yaş 4–5 ay civarıdır.')])

# ───────────── YATIRIM GERİ DÖNÜŞ ─────────────
def _geri(yatirim, aylik, artis):
    ay, top, a = 0, 0.0, aylik
    while top < yatirim and ay < 600:
        top += a; ay += 1
        if ay % 12 == 0: a *= (1 + artis / 100)
    return ay


def _ay_yil(ay):
    y, m = divmod(ay, 12)
    return (f'{y} yıl ' if y else '') + (f'{m} ay' if m else '').strip()


EK['yatirim-geri-donus-suresi-hesaplama'] = dict(article='''
<h2 id="artis-etkisi">Nakit girişi yıllık artarsa süre ne kadar kısalır?</h2>
<p>1.200.000 ₺ yatırım ve ayda 25.000 ₺ başlangıç net nakit girişi için, girişin her yıl belirli oranda arttığı senaryolar:</p>
''' + tablo(['Yıllık artış', 'Geri dönüş süresi', 'Ay'], [
    ['%' + f(a), _ay_yil(_geri(1200000, 25000, a)), str(_geri(1200000, 25000, a))] for a in (0, 10, 20, 30, 40)]) + '''
<p>Yüksek enflasyon dönemlerinde kira ve fiyat artışları nominal geri dönüş süresini belirgin biçimde kısaltır. Ancak aynı dönemde paranın değeri de düştüğü için, karar verirken <a href="/enflasyon-hesaplama.html">enflasyon</a> etkisini ayrıca değerlendirmek gerekir.</p>
<h2 id="gunes-ornek">Örnek: çatı güneş paneli yatırımı</h2>
<p>Bir evin çatısına 250.000 ₺’ye güneş enerjisi sistemi kurulduğunu ve sistemin ayda ortalama 5.000 ₺ elektrik faturası tasarrufu sağladığını varsayalım:</p>
''' + tablo(['Senaryo', 'Geri dönüş süresi'], [
    ['Elektrik fiyatı sabit', _ay_yil(_geri(250000, 5000, 0))], ['Elektrik fiyatı yılda %25 artarsa', _ay_yil(_geri(250000, 5000, 25))],
    ['Elektrik fiyatı yılda %40 artarsa', _ay_yil(_geri(250000, 5000, 40))]]) + '''
<p>Bakım, inverter değişimi ve panel verim kaybı gibi giderler hesaba eklendiğinde süre biraz uzar. Gerçek tasarrufunuzu son 12 ayın faturalarından hesaplamak en güvenilir yöntemdir.</p>
''', faq=[('Kira her yıl %20 artarsa dükkân kaç yılda amorti eder?', f'1.200.000 ₺ fiyat ve ayda 25.000 ₺ başlangıç kirasıyla yaklaşık {_ay_yil(_geri(1200000, 25000, 20))} sürer; kira sabit kalsaydı 4 yıl olurdu.')])

# ───────────── KİRA GETİRİSİ ─────────────
EK['kira-getirisi-hesaplama'] = dict(article='''
<h2 id="getiri-tablo">Fiyat ve kiraya göre brüt getiri ve amortisman</h2>
''' + tablo(['Daire fiyatı', 'Aylık 15.000 ₺', 'Aylık 20.000 ₺', 'Aylık 25.000 ₺', 'Aylık 30.000 ₺'], [
    [f(p) + ' ₺'] + ['%' + f(k * 12 / p * 100, 1) + ' · ' + f(p / (k * 12), 1) + ' yıl' for k in (15000, 20000, 25000, 30000)] for p in (3000000, 4000000, 5000000, 6000000, 8000000)]) + '''
<p>Her hücrede önce yıllık brüt getiri oranı, ardından kiranın sabit kaldığı varsayımıyla amortisman süresi yer alır.</p>
<h2 id="net-ornek">Brütten nete: örnek hesap</h2>
<p>5.000.000 ₺’lik daireden ayda 25.000 ₺ kira alındığını varsayalım (yıllık 300.000 ₺, brüt getiri %6). Yıllık giderler:</p>
''' + tablo(['Gider kalemi', 'Yıllık tutar (örnek)'], [
    ['Emlak vergisi', '5.000 ₺'], ['DASK ve konut sigortası', '6.000 ₺'], ['Bakım ve onarım', '15.000 ₺'],
    ['Boş kalma (yılda 1 ay)', '25.000 ₺'], ['<b>Toplam gider</b>', '<b>51.000 ₺</b>']]) + f'''
<p>Net yıllık gelir 300.000 − 51.000 = 249.000 ₺, net getiri ise <b>%{f(249000 / 5000000 * 100, 2)}</b> olur. Kira geliri vergisi bu hesaba dahil değildir; beyan ve istisna tutarı için <a href="/blog/kira-geliri-vergisi-hesaplama.html">kira geliri vergisi rehberine</a> bakabilirsiniz.</p>
''', faq=[('5 milyonluk daire ayda kaç kiraya %6 getiri sağlar?', 'Yıllık 300.000 ₺, yani ayda 25.000 ₺ kira %6 brüt getiri demektir. Giderler düşüldüğünde net getiri genellikle %4,5–5,5 aralığına iner.')])

# ───────────── ORTALAMA ─────────────
_maas = [30000, 32000, 35000, 38000, 250000]
_ort = sum(_maas) / len(_maas)
EK['ortalama-hesaplama'] = dict(article=f'''
<h2 id="aykiri">Aykırı değer ortalamayı nasıl bozar?</h2>
<p>Beş kişilik bir ekipte maaşlar: {', '.join(f(x) for x in _maas)} ₺. Patronun maaşı diğerlerinden çok yüksek olduğu için:</p>
''' + tablo(['Ölçü', 'Değer', 'Yorum'], [
    ['Aritmetik ortalama', f(_ort) + ' ₺', 'Ekipte kimse bu kadar kazanmıyor'], ['Medyan (ortanca)', f(sorted(_maas)[2]) + ' ₺', 'Tipik çalışanı daha iyi temsil eder'],
    ['Patron hariç ortalama', f(sum(_maas[:4]) / 4) + ' ₺', 'Aykırı değer çıkarıldığında']]) + '''
<p>Bu yüzden maaş, ev fiyatı ve gelir gibi verilerde haberlerde genellikle medyan kullanılır. Hesaplayıcı ortalama ve medyanı birlikte verdiği için ikisi arasındaki büyük fark, verinizde aykırı bir değer olduğunu gösterir.</p>
<h2 id="vize-final">Vize ve final: geçmek için finalden kaç almalıyım?</h2>
<p>Vize %40, final %60 ağırlıklı ve geçme notu 50 olan bir derste gereken final notu:</p>
<div class="formula">Gereken final = (50 − Vize × 0,40) ÷ 0,60</div>
''' + tablo(['Vize notu', 'Gereken final (ortalama 50 için)', 'Gereken final (ortalama 60 için)'], [
    [str(v)] + [f(max(0, (h - v * 0.4) / 0.6), 1) if (h - v * 0.4) / 0.6 <= 100 else 'Ulaşılamaz' for h in (50, 60)] for v in (20, 30, 40, 50, 60, 70, 80)]) + '''
<p>Birçok üniversitede ayrıca final notunun kendisinin de belirli bir alt sınırın (örneğin 40 veya 50) üzerinde olması şartı aranır; kendi yönetmeliğinizi kontrol edin.</p>
''', faq=[('Vize 40 aldım, finalden kaç almalıyım?', f'Vize %40, final %60 ağırlıklıysa ortalama 50 için finalden en az {f((50 - 40 * 0.4) / 0.6, 1)} almanız gerekir.')])

# ───────────── GÜNLÜK KALORİ ─────────────
def _bmh(e, kg, boy, yas): return 10 * kg + 6.25 * boy - 5 * yas + (5 if e else -161)


_akt = [('Hareketsiz', 1.2), ('Az hareketli', 1.375), ('Orta hareketli', 1.55), ('Çok hareketli', 1.725)]
EK['gunluk-kalori-ihtiyaci-hesaplama'] = dict(article='''
<h2 id="ornek-tablo">Örnek kişiler için günlük kalori ihtiyacı</h2>
<p>Mifflin-St Jeor denklemi ve aktivite katsayılarıyla, 30 yaşındaki örnek kişiler için:</p>
''' + tablo(['Kişi', 'Bazal metabolizma'] + [a for a, _ in _akt], [
    [ad, f(_bmh(e, kg, b, 30)) + ' kcal'] + [f(_bmh(e, kg, b, 30) * k) for _, k in _akt] for ad, e, kg, b in
    [('Kadın, 165 cm, 60 kg', False, 60, 165), ('Kadın, 165 cm, 75 kg', False, 75, 165), ('Erkek, 178 cm, 75 kg', True, 75, 178), ('Erkek, 178 cm, 90 kg', True, 90, 178)]]) + '''
<h2 id="yas-etkisi">Yaş ilerledikçe ihtiyaç nasıl değişir?</h2>
<p>Formülde her yaş yılı bazal metabolizmayı 5 kcal düşürür. 178 cm, 75 kg, orta hareketli bir erkek için:</p>
''' + tablo(['Yaş', 'Günlük ihtiyaç (orta hareketli)'], [[str(y), f(_bmh(True, 75, 178, y) * 1.55) + ' kcal'] for y in (20, 30, 40, 50, 60, 70)]) + '''
<p>On yılda yaklaşık 75–80 kcal’lik düşüş küçük görünse de, beslenme alışkanlıkları değişmezse yılda birkaç kiloluk artışa yol açabilir. Düzenli kuvvet antrenmanı kas kütlesini koruyarak bu düşüşü yavaşlatır.</p>
''', faq=[('30 yaşında 75 kilo bir erkek günde kaç kalori almalı?', f'178 cm boyunda ve orta hareketliyse yaklaşık {f(_bmh(True, 75, 178, 30) * 1.55)} kcal; hareketsizse yaklaşık {f(_bmh(True, 75, 178, 30) * 1.2)} kcal.')])

# ───────────── TYT NET ─────────────
EK['tyt-net-hesaplama'] = dict(article='''
<h2 id="hedef-net">Hedef nete ulaşmak için kaç doğru gerekir?</h2>
<p>Yanlış sayınıza göre hedef nete ulaşmak için gereken doğru sayısı (Doğru = Hedef net + Yanlış ÷ 4):</p>
''' + tablo(['Hedef net', '0 yanlış', '4 yanlış', '8 yanlış', '12 yanlış'], [
    [str(n)] + [str(math.ceil(n + y / 4)) for y in (0, 4, 8, 12)] for n in (20, 30, 40, 50, 60, 70, 80, 90)]) + f'''
<p>Toplam 120 soruda 8 yanlış yapan bir aday 80 net için en az 82 doğru yapmalıdır; yanlışlar 12’ye çıkarsa 83 doğru gerekir. Yanlış sayısını azaltmak, özellikle yüksek net hedeflerinde ek soru çözmek kadar etkilidir.</p>
<h2 id="sure">Soru başına ne kadar süre var?</h2>
<p>TYT’de 120 soru için 165 dakika verilir; soru başına ortalama <b>{f(165 / 120, 2)} dakika</b> (yaklaşık {f(165 / 120 * 60, 0)} saniye) düşer. Paragraf soruları ve problem soruları bu ortalamanın üzerinde süre isterken, bilgi soruları daha hızlı çözülür. Deneme sınavlarında her testi bitirdiğiniz dakikayı not ederek kendi süre dağılımınızı çıkarmak, sınav günü zaman yönetimini kolaylaştırır.</p>
''', faq=[('TYT’de 80 net için kaç doğru gerekir?', 'Hiç yanlış yapmazsanız 80 doğru yeterlidir. 8 yanlışla 82, 12 yanlışla 83 doğru gerekir.')])

# ───────────── GÜN HESAPLAMA ─────────────
EK['gun-hesaplama'] = dict(article='''
<h2 id="donusum">Gün sayısının hafta, ay ve yıl karşılığı</h2>
''' + tablo(['Gün', 'Hafta', 'Ay (ortalama 30,44 gün)', 'Yıl'], [
    [f(g), f(g / 7, 1), f(g / 30.436875, 1), f(g / 365.2425, 2)] for g in (30, 45, 60, 90, 100, 180, 365, 500, 1000)]) + '''
<p>“3 ay” ile “90 gün” her zaman aynı değildir: Ocak–Mart arası 90 (artık yılda 91) gün çekerken, Temmuz–Eylül arası 92 gündür. Sözleşmelerde ve yasal sürelerde sürenin gün olarak mı ay olarak mı yazıldığına dikkat edin.</p>
<h2 id="sure-kurallari">Yasal sürelerde gün nasıl sayılır?</h2>
<ul>
<li>Gün olarak belirlenen sürelerde, sürenin başladığı gün hesaba katılmaz; süre son günün bitimiyle sona erer.</li>
<li>Hafta veya ay olarak belirlenen süreler, başladığı güne karşılık gelen son hafta veya ayın aynı gününde biter.</li>
<li>Son gün resmi tatile denk gelirse süre, tatili izleyen ilk iş gününün bitimine kadar uzar.</li>
</ul>
<p>Bu genel kurallar usul kanunlarında yer alır; tebligat, itiraz ve dava süreleri gibi kritik durumlarda bir hukukçuya danışın. İş günü sayısını bulmak için <a href="/is-gunu-hesaplama.html">iş günü hesaplama</a> aracını kullanabilirsiniz.</p>
''', faq=[('1000 gün kaç yıl eder?', f'Yaklaşık {f(1000 / 365.2425, 2)} yıl, yani 2 yıl 9 ay civarıdır.')])
