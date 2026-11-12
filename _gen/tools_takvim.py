"""Ekonomi Takvimi 2026–2027 (tek URL, her açıklamadan sonra güncellenir).
Güncelleme: EVENTS listesine sonuçları 'sonuc' alanına yazın, tarih geçen satırlar otomatik "açıklandı" olur.
Kaynaklar: TÜİK yayın kuralı (ayın 3'ü, hafta sonuysa ilk iş günü, 10:00), TCMB PPK takvimi, SGK ödeme günleri, GİB vergi takvimi.
"""
import datetime as _d, json as _j

TOOLS = []
AY = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
GUN = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
BUGUN = _d.date.today()


def tr(s):
    d = _d.date.fromisoformat(s)
    return f'{d.day} {AY[d.month-1]} {d.year} {GUN[d.weekday()]}'


# ── Enflasyon açıklamaları (TÜİK) ──
ENF = []
for y, m in [(2026, 11), (2026, 12)] + [(2027, i) for i in range(1, 13)]:
    t = _d.date(y, m, 3)
    while t.weekday() >= 5:
        t += _d.timedelta(1)
    vm, vy = (m - 2) % 12 + 1, y if m > 1 else y - 1
    ENF.append((t.isoformat(), f'{AY[vm-1]} {vy}'))


def enf_etki(veri):
    ay = veri.split()[0]
    e = ['kira artış oranı']
    if ay == 'Ekim':
        e.append('yeniden değerleme oranı (Yİ-ÜFE)')
    if ay in ('Haziran', 'Aralık'):
        e.append('<b>memur ve emekli zammı kesinleşir</b>')
    return ', '.join(e)


# (tarih, grup, başlık, açıklama, link)
SONUC = {'Ekim 2026': '<b>Açıklandı:</b> aylık %2,58, yıllık %29,77 · Kasım kira artış oranı %31,23 · yeniden değerleme oranı %27,83'}
EVENTS = [(t, 'enflasyon', f'{v} enflasyonu', SONUC.get(v) or f'TÜİK, saat 10:00 · Belirler: {enf_etki(v)}', '/kira-artis-hesaplama.html') for t, v in ENF]
EVENTS += [
    ('2026-10-22', 'faiz', 'TCMB faiz kararı (PPK)', 'Politika faizi %37’den %36’ya indirildi (−100 baz puan)', '/mevduat-faizi-hesaplama.html'),
    ('2026-10-30', 'sinav', 'KPSS Önlisans sonuçları', 'ÖSYM 4 Ekim sınavının sonuçlarını açıklar (P93)', '/kpss-puan-hesaplama.html'),
    ('2026-11-19', 'sinav', 'KPSS Ortaöğretim sonuçları', 'ÖSYM 25 Ekim sınavının sonuçlarını açıklar (P94)', '/kpss-puan-hesaplama.html'),
    ('2026-11-29', 'sinav', 'ALES/3 sınavı', 'ÖSYM ALES/3 oturumu (sonuçlar 17 Aralık)', '/ales-puan-hesaplama.html'),
    ('2026-12-17', 'sinav', 'ALES/3 sonuçları', 'ÖSYM 29 Kasım ALES sonuçlarını açıklar', '/ales-puan-hesaplama.html'),
    ('2027-01-13', 'sinav', 'MSÜ başvuruları başlar', 'ÖSYM 2027 MSÜ başvuruları 13 Ocak – 10 Şubat (sınav 20 Mart)', '/gun-hesaplama.html'),
    ('2027-02-04', 'sinav', 'YKS 2027 başvuruları başlar', 'ÖSYM YKS başvuruları 4 Şubat – 2 Mart 2027', '/tyt-net-hesaplama.html'),
    ('2027-03-20', 'sinav', 'MSÜ sınavı', 'ÖSYM 2027 MSÜ (sonuçlar 15 Nisan)', '/tyt-net-hesaplama.html'),
    ('2027-04-18', 'sinav', 'ALES/1 sınavı', 'ÖSYM 2027 ALES/1 (sonuçlar 7 Mayıs)', '/ales-puan-hesaplama.html'),
    ('2027-06-19', 'sinav', 'YKS – TYT oturumu', 'ÖSYM 2027 YKS; AYT ve YDT 20 Haziran (sonuçlar 21 Temmuz)', '/tyt-net-hesaplama.html'),
    ('2027-06-20', 'sinav', 'YKS – AYT ve YDT oturumları', 'ÖSYM 2027 YKS ikinci gün', '/ayt-net-hesaplama.html'),
    ('2027-07-11', 'sinav', 'ALES/2 sınavı', 'ÖSYM 2027 ALES/2 (sonuçlar 30 Temmuz)', '/ales-puan-hesaplama.html'),
    ('2027-07-18', 'sinav', 'DGS sınavı', 'ÖSYM 2027 DGS (sonuçlar 12 Ağustos)', '/obp-hesaplama.html'),
    ('2027-07-21', 'sinav', 'YKS 2027 sonuçları', 'ÖSYM 19–20 Haziran YKS sonuçlarını açıklar', '/ayt-net-hesaplama.html'),
    ('2027-09-12', 'sinav', 'KPSS 2027 (GY-GK)', 'ÖSYM KPSS A Grubu Genel Yetenek–Genel Kültür (sonuçlar 13 Ekim)', '/kpss-puan-hesaplama.html'),
    ('2026-11-12', 'faiz', 'TCMB Enflasyon Raporu', 'Merkez Bankası enflasyon tahminlerini günceller', '/enflasyon-hesaplama.html'),
    ('2026-12-10', 'faiz', 'TCMB faiz kararı (PPK)', 'Para Politikası Kurulu toplantısı, saat 14:00', '/mevduat-faizi-hesaplama.html'),
    ('2027-01-21', 'faiz', 'TCMB faiz kararı (PPK)', 'Para Politikası Kurulu toplantısı', '/mevduat-faizi-hesaplama.html'),
    ('2027-02-11', 'faiz', 'TCMB Enflasyon Raporu', 'Merkez Bankası enflasyon tahminlerini günceller', '/enflasyon-hesaplama.html'),
    ('2027-03-18', 'faiz', 'TCMB faiz kararı (PPK)', 'Para Politikası Kurulu toplantısı', '/mevduat-faizi-hesaplama.html'),
    ('2027-04-22', 'faiz', 'TCMB faiz kararı (PPK)', 'Para Politikası Kurulu toplantısı', '/mevduat-faizi-hesaplama.html'),
    ('2027-05-13', 'faiz', 'TCMB Enflasyon Raporu', 'Merkez Bankası enflasyon tahminlerini günceller', '/enflasyon-hesaplama.html'),
    ('2027-06-10', 'faiz', 'TCMB faiz kararı (PPK)', 'Para Politikası Kurulu toplantısı', '/mevduat-faizi-hesaplama.html'),
    ('2026-11-30', 'vergi', 'Emlak vergisi 2. taksit son gün', '2026 emlak vergisinin ikinci taksiti', '/blog/yeniden-degerleme-orani-2026.html'),
    ('2026-12-31', 'maas', '2027 asgari ücretin açıklanması (beklenen)', 'Asgari Ücret Tespit Komisyonu kararı, Aralık sonu', '/asgari-ucret-hesaplama.html'),
    ('2027-01-01', 'maas', 'Yeni yıl tutarları yürürlüğe girer', 'Asgari ücret, vergi dilimleri, MTV ve harçlar, SGK tavanı', '/net-maas-hesaplama.html'),
    ('2027-01-15', 'maas', 'Memurlara Ocak zamlı maaş', 'Memur maaşları her ayın 15’inde peşin ödenir', '/memur-maaslari.html'),
    ('2027-02-01', 'vergi', 'MTV 1. taksit son gün', '31 Ocak Pazar olduğu için süre 1 Şubat’a uzar', '/mtv-hesaplama.html'),
    ('2027-03-09', 'tatil', 'Ramazan Bayramı (9–11 Mart)', 'Arife 8 Mart yarım gün', '/resmi-tatiller-2027.html'),
    ('2027-03-31', 'vergi', 'Yıllık gelir vergisi beyannamesi son gün', '2026 gelirleri; 1–31 Mart, 1. taksit ödemesi', '/gelir-vergisi-hesaplama.html'),
    ('2027-05-16', 'tatil', 'Kurban Bayramı (16–19 Mayıs)', 'Arife 15 Mayıs yarım gün', '/resmi-tatiller-2027.html'),
    ('2027-05-31', 'vergi', 'Emlak vergisi 1. taksit son gün', '2027 emlak vergisinin ilk taksiti', '/blog/yeniden-degerleme-orani-2026.html'),
    ('2027-07-15', 'maas', 'Memurlara Temmuz zamlı maaş', 'Haziran enflasyonuyla kesinleşen Temmuz zammı', '/memur-maaslari.html'),
    ('2027-08-02', 'vergi', 'MTV 2. taksit ve gelir vergisi 2. taksit son gün', '31 Temmuz Cumartesi olduğu için süre 2 Ağustos’a uzar', '/mtv-hesaplama.html'),
]
EVENTS.sort()
GRUP = {'enflasyon': '📈 Enflasyon', 'faiz': '🏦 Faiz', 'maas': '💼 Maaş & Zam', 'vergi': '🧾 Vergi', 'sinav': '🎓 Sınav', 'tatil': '🗓️ Tatil'}

JS = '''
var EV=''' + _j.dumps(EVENTS, ensure_ascii=False) + r''';
var AYL=['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
function d0(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2]);}
function trd(s){var d=d0(s);return d.getDate()+' '+AYL[d.getMonth()]+' '+d.getFullYear();}
function onReady(){el('grup').addEventListener('change',function(){run(false);}); run(false);}
function hesapla(){
  var g=el('grup').value, now=new Date(); now.setHours(0,0,0,0);
  var up=EV.filter(function(e){return (g==='hepsi'||e[1]===g)&&d0(e[0])>=now;});
  if(!up.length) return 'Bu kategoride yaklaşan tarih yok.';
  var f=up[0], gun=Math.round((d0(f[0])-now)/864e5);
  return {main:[f[2], gun===0?'Bugün':gun+' gün kaldı'], sub:trd(f[0])+' · '+f[3],
    rows:up.slice(1,8).map(function(e){var k=Math.round((d0(e[0])-now)/864e5);return ['<a href="'+e[4]+'">'+e[2]+'</a>',trd(e[0])+' ('+k+' gün)'];}),
    note:'Tarihler resmî kurumların yayın takvimlerine göre hazırlanmıştır; değişiklik olursa bu sayfa güncellenir.'};
}'''

FORM = '''<div class="form-grid"><div class="field full"><label for="grup">Hangi tarihler?</label><select id="grup">
<option value="hepsi">Tümü</option><option value="enflasyon">📈 Enflasyon ve kira artış oranı</option><option value="maas">💼 Maaş, zam ve asgari ücret</option>
<option value="faiz">🏦 Merkez Bankası faiz kararları</option><option value="vergi">🧾 Vergi ve ödeme son günleri</option><option value="sinav">🎓 Sınav sonuçları</option><option value="tatil">🗓️ Bayram ve tatiller</option></select></div></div>'''


def _row(e):
    t, g, b, a, l = e
    gec = _d.date.fromisoformat(t) < BUGUN
    return f'<tr><td>{tr(t)}</td><td><a href="{l}">{b}</a>{" <small>(geçti)</small>" if gec else ""}</td><td>{a}</td></tr>'


yakin = [e for e in EVENTS if BUGUN <= _d.date.fromisoformat(e[0]) <= BUGUN + _d.timedelta(45)]
YAKIN = '<div class="table-wrap"><table><thead><tr><th>Tarih</th><th>Ne oluyor?</th><th>Ayrıntı</th></tr></thead><tbody>' + ''.join(_row(e) for e in yakin) + '</tbody></table></div>'
ENF_T = '<div class="table-wrap"><table><thead><tr><th>Açıklanma tarihi</th><th>Verinin ait olduğu ay</th><th>Neyi belirler?</th></tr></thead><tbody>' + ''.join(
    f'<tr><td>{tr(t)}</td><td>{v}</td><td>{enf_etki(v)}</td></tr>' for t, v in ENF) + '</tbody></table></div>'
PPK_T = '<div class="table-wrap"><table><thead><tr><th>Tarih</th><th>Toplantı</th></tr></thead><tbody>' + ''.join(
    f'<tr><td>{tr(t)}</td><td>{b}</td></tr>' for t, g, b, a, l in EVENTS if g == 'faiz') + '</tbody></table></div>'
VERGI_T = '<div class="table-wrap"><table><thead><tr><th>Son gün</th><th>Ödeme / beyan</th><th>Not</th></tr></thead><tbody>' + ''.join(
    _row(e) for e in EVENTS if e[1] == 'vergi') + '</tbody></table></div>'
h_enf = ENF[0]

TOOLS.append(dict(
slug='ekonomi-takvimi', name='Ekonomi Takvimi 2026–2027', cat='finans', ico='📅',
title='Ekonomi Takvimi 2026–2027: Enflasyon, Zam ve Ödeme Tarihleri',
desc='Enflasyon ne zaman açıklanacak, emekli ve memur maaşı ne zaman yatacak, faiz kararı ne zaman? 2026–2027 ekonomi takvimi ve geri sayım.',
h1='📅 Ekonomi Takvimi 2026–2027',
lead='Enflasyon, kira artış oranı, memur ve emekli zammı, asgari ücret, faiz kararları ve vergi son günleri tek takvimde. Her açıklamadan sonra güncellenir.',
card_title='Sıradaki açıklamaya kaç gün kaldı?', button='Göster',
badges=['✓ Ücretsiz', 'Her ay güncellenir', 'Resmî takvimler'],
form=FORM, js=JS,
article=f'''
<p><b>Kısa cevap:</b> Sıradaki enflasyon verisi (<b>{h_enf[1]}</b>) <b>{tr(h_enf[0])}</b> saat 10:00’da TÜİK tarafından açıklanacak; aynı gün o ayın kira artış oranı da belli olur. Memur ve emekli zammını belirleyen Aralık 2026 enflasyonu <b>4 Ocak 2027</b>’de, 2027 asgari ücreti ise Aralık 2026’nın son günlerinde açıklanacak.</p>

<h2 id="yakin">Önümüzdeki 45 günde açıklanacaklar</h2>
{YAKIN}

<h2 id="enflasyon">Enflasyon ne zaman açıklanacak? TÜİK 2026–2027 takvimi</h2>
<p>TÜİK, tüketici fiyat endeksini (TÜFE) her ayın <b>3’ünde saat 10:00</b>’da açıklar; 3’ü hafta sonuna denk gelirse ilk iş gününe kayar. Aynı bültende yer alan “12 aylık ortalama” değişim, o ay yenilenen kira sözleşmelerinin yasal artış sınırıdır.</p>
{ENF_T}
<p>Kira artışınızı <a href="/kira-artis-hesaplama.html">kira artış hesaplama</a>, paranızın alım gücünü <a href="/enflasyon-hesaplama.html">enflasyon hesaplama</a> aracıyla bulabilirsiniz.</p>

<h2 id="emekli">Emekli maaşı ne zaman yatacak?</h2>
<p>SSK (4/a) emeklilerinin aylıkları her ayın <b>17’si ile 26’sı</b>, Bağ-Kur (4/b) emeklilerinin aylıkları <b>25’i ile 28’i</b> arasında, tahsis numarasının son hanesine göre ödenir:</p>
<div class="table-wrap"><table><thead><tr><th>Tahsis no. son hane</th><th>SSK (4/a)</th><th>Bağ-Kur (4/b)</th></tr></thead><tbody>
<tr><td>9</td><td>17’si</td><td>25’i</td></tr><tr><td>7</td><td>18’i</td><td>25’i</td></tr><tr><td>5</td><td>19’u</td><td>25’i</td></tr>
<tr><td>3</td><td>20’si</td><td>26’sı</td></tr><tr><td>1</td><td>21’i</td><td>26’sı</td></tr><tr><td>8</td><td>22’si</td><td>27’si</td></tr>
<tr><td>6</td><td>23’ü</td><td>27’si</td></tr><tr><td>4</td><td>24’ü</td><td>27’si</td></tr><tr><td>2</td><td>25’i</td><td>28’i</td></tr><tr><td>0</td><td>26’sı</td><td>28’i</td></tr>
</tbody></table></div>
<p>Memur emeklilerinin (Emekli Sandığı) ödeme günü e-Devlet’teki SGK emekli aylık bilgileri hizmetinden görülebilir. Ocak 2027’de SSK ve Bağ-Kur emeklileri Temmuz–Aralık 2026 enflasyonu kadar zam alacak; tahmin için <a href="/memur-emekli-zammi-hesaplama.html">memur ve emekli zammı hesaplama</a>.</p>

<h2 id="memur">Memur maaşı ne zaman yatar?</h2>
<p>Memur maaşları her ayın <b>15’inde peşin</b> ödenir. Ocak 2027 zammı Aralık enflasyonunun açıklanacağı 4 Ocak 2027’de kesinleşecek ve <b>15 Ocak 2027</b> maaşına yansıyacak. Temmuz zammı ise Haziran enflasyonuyla (5 Temmuz 2027) kesinleşir. Unvanlara göre maaşlar için <a href="/memur-maaslari.html">memur maaşları</a> sayfamıza bakın.</p>

<h2 id="asgari">Asgari ücret ne zaman açıklanacak?</h2>
<p>2027 asgari ücreti için Asgari Ücret Tespit Komisyonu’nun Aralık 2026’nın ilk haftalarında toplanması ve kararın <b>Aralık sonunda</b> açıklanması bekleniyor. Yeni asgari ücret <b>1 Ocak 2027</b>’de yürürlüğe girecek. Tahminler için <a href="/blog/asgari-ucret-2027.html">Asgari Ücret 2027</a> yazımıza bakın.</p>

<h2 id="faiz">Faiz kararı ne zaman? TCMB PPK toplantıları</h2>
<p>Merkez Bankası Para Politikası Kurulu (PPK) faiz kararlarını toplantı günü saat 14:00’te açıklar. Faiz kararları mevduat ve kredi faizlerini doğrudan etkiler. <strong>Son karar (22 Ekim 2026):</strong> politika faizi %37’den %36’ya indirildi; gecelik borç verme faizi %39, gecelik borçlanma faizi %34,5 oldu.</p>
{PPK_T}
<p>Mevduat getirinizi <a href="/mevduat-faizi-hesaplama.html">mevduat faizi hesaplama</a>, kredi taksitlerinizi <a href="/kredi-hesaplama.html">kredi hesaplama</a> aracıyla görebilirsiniz.</p>

<h2 id="vergi">Vergi ve ödeme takvimi</h2>
{VERGI_T}
<ul>
<li><b>KDV beyannamesi:</b> Her ayın 28’i (önceki ay için).</li>
<li><b>Muhtasar ve prim hizmet beyannamesi:</b> Her ayın 26’sı.</li>
<li>Son gün hafta sonuna veya resmî tatile denk gelirse süre ilk iş gününe uzar.</li>
</ul>

<h2 id="tatil">2027 bayram ve resmî tatiller</h2>
<p>Ramazan Bayramı <b>9–11 Mart 2027</b> (arife 8 Mart yarım gün), Kurban Bayramı <b>16–19 Mayıs 2027</b> (arife 15 Mayıs yarım gün). Tüm tatiller, köprü günleri ve kaç gün izinle kaç gün tatil yapılacağı için <a href="/resmi-tatiller-2027.html">2027 resmi tatiller ve köprü günleri</a> sayfasına, iki tarih arasındaki iş günü sayısı için <a href="/is-gunu-hesaplama.html">iş günü hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('Kasım 2026 enflasyonu ne zaman açıklanacak?', 'Kasım 2026 enflasyonu 3 Aralık 2026 Perşembe günü saat 10:00’da TÜİK tarafından açıklanacak. Ekim 2026 enflasyonu 3 Kasım’da açıklandı: aylık %2,58, yıllık %29,77.'),
('Memur ve emekli zammı ne zaman belli olacak?', 'Ocak 2027 zammını belirleyen Aralık 2026 enflasyonu 4 Ocak 2027 Pazartesi günü açıklanacak; zam oranları aynı gün kesinleşir.'),
('SSK emekli maaşı ayın kaçında yatar?', 'SSK emeklilerinin aylıkları her ayın 17’si ile 26’sı arasında, tahsis numarasının son hanesine göre ödenir. Son hanesi 9 olanlar 17’sinde, 0 olanlar 26’sında alır.'),
('Bağ-Kur emekli maaşı ayın kaçında yatar?', 'Bağ-Kur emeklilerinin aylıkları her ayın 25’i ile 28’i arasında ödenir: son hanesi 5, 7, 9 olanlar 25’inde; 1, 3 olanlar 26’sında; 4, 6, 8 olanlar 27’sinde; 0, 2 olanlar 28’inde.'),
('Merkez Bankası faiz kararı ne zaman?', 'Sıradaki PPK toplantısı 10 Aralık 2026’dadır. 2027’nin ilk toplantısı 21 Ocak 2027’de yapılacak.'),
('MTV ne zaman ödenir?', 'MTV Ocak ve Temmuz aylarında iki taksitte ödenir. 2027’de 1. taksit için son gün 1 Şubat 2027, 2. taksit için 2 Ağustos 2027’dir (31 Ocak ve 31 Temmuz hafta sonuna denk geliyor).'),
],
related=['kira-artis-hesaplama', 'memur-emekli-zammi-hesaplama', 'enflasyon-hesaplama', 'memur-maaslari', 'asgari-ucret-hesaplama'],
sources=[('TÜİK Ulusal Veri Yayımlama Takvimi', 'https://www.tuik.gov.tr/'), ('TCMB Para Politikası Kurulu toplantı takvimi', 'https://www.tcmb.gov.tr/'),
         ('SGK emekli aylık ödeme günleri', 'https://www.sgk.gov.tr/'), ('GİB Vergi Takvimi', 'https://www.gib.gov.tr/')],
))


# ══════════════ 2027 Resmi Tatiller ve Köprü Günleri (11 Kas 2026) ══════════════
# Kaynak: 2429 sayılı Ulusal Bayram ve Genel Tatiller Kanunu; dini bayram tarihleri Diyanet 2027 takvimi.
# (tarih, ad, gün değeri: 1 = tam gün, 0.5 = 13:00'ten sonra yarım gün)
RT = [('2027-01-01', 'Yılbaşı', 1),
      ('2027-03-08', 'Ramazan Bayramı arifesi', 0.5), ('2027-03-09', 'Ramazan Bayramı 1. gün', 1), ('2027-03-10', 'Ramazan Bayramı 2. gün', 1), ('2027-03-11', 'Ramazan Bayramı 3. gün', 1),
      ('2027-04-23', 'Ulusal Egemenlik ve Çocuk Bayramı', 1), ('2027-05-01', 'Emek ve Dayanışma Günü', 1),
      ('2027-05-15', 'Kurban Bayramı arifesi', 0.5), ('2027-05-16', 'Kurban Bayramı 1. gün', 1), ('2027-05-17', 'Kurban Bayramı 2. gün', 1), ('2027-05-18', 'Kurban Bayramı 3. gün', 1),
      ('2027-05-19', 'Kurban Bayramı 4. gün + Atatürk’ü Anma, Gençlik ve Spor Bayramı', 1),
      ('2027-07-15', 'Demokrasi ve Millî Birlik Günü', 1), ('2027-08-30', 'Zafer Bayramı', 1),
      ('2027-10-28', 'Cumhuriyet Bayramı arifesi', 0.5), ('2027-10-29', 'Cumhuriyet Bayramı', 1)]
_RT = {_d.date.fromisoformat(t): (a, v) for t, a, v in RT}


def _bos(d):
    """o gün çalışılmayan kısım: hafta sonu 1, tam tatil 1, yarım gün 0.5, değilse 0"""
    if d.weekday() >= 5:
        return 1
    return _RT.get(d, ('', 0))[1]


# Tatil kümeleri: birbirine en çok 1 gün uzak tatiller tek küme
_kume, _s = [], None
for t in sorted(_RT):
    if _s and (t - _s[-1]).days <= 2:
        _s.append(t)
    else:
        _s = [t]; _kume.append(_s)
KUME_AD = []
for k in _kume:
    a = _RT[k[0]][0]
    KUME_AD.append('Ramazan Bayramı' if 'Ramazan' in a else 'Kurban Bayramı ve 19 Mayıs' if 'Kurban' in a else 'Cumhuriyet Bayramı' if 'Cumhuriyet' in a else a)


def _plan(k, butce):
    """kümeyi içeren, izin ihtiyacı <= bütçe olan en uzun kesintisiz tatil penceresi"""
    en = None
    cek = [t for t in k if _RT[t][1] == 1]  # pencere tam gün tatillerin hepsini içermeli; arife dışarıda kalabilir
    for s0 in range(0, 10):
        s = cek[0] - _d.timedelta(s0)
        for e0 in range(0, 10):
            e = cek[-1] + _d.timedelta(e0)
            gunler = [s + _d.timedelta(i) for i in range((e - s).days + 1)]
            izin = sum(1 - _bos(g) for g in gunler)
            if izin > butce + 1e-9:
                continue
            uzun = len(gunler)
            if en is None or uzun > en[0] or (uzun == en[0] and izin < en[1]):
                en = (uzun, izin, s, e, [g for g in gunler if _bos(g) < 1])
    return en


def _tr_kisa(d):
    return f'{d.day} {AY[d.month-1]} {GUN[d.weekday()]}'


def _gun_s(x):
    return (f'{x:g}'.replace('.', ',')) + ' gün'


PLAN = []  # her küme için bütçe 0..4 (0,5 adım)
for k, ad in zip(_kume, KUME_AD):
    p, ham = {}, {}
    for b in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4]:
        ham[b] = _plan(k, b)
        u0 = ham[0][0]
        # bütçe içindeki en uzun tatil; ancak her izin günü en az 2 gün tatil kazandırmalı (yoksa köprü değil)
        aday = [ham[x] for x in ham if ham[x][1] == 0 or (ham[x][0] - u0) / ham[x][1] >= 2]
        u, iz, s, e, ig = max(aday, key=lambda r: (r[0], -r[1]))
        p[str(b)] = [u, iz, s.isoformat(), e.isoformat(), [g.isoformat() + ('|y' if _bos(g) == 0.5 else '') for g in ig]]
    PLAN.append([ad, k[0].isoformat(), p])

# yıl özeti
_yil = [_d.date(2027, 1, 1) + _d.timedelta(i) for i in range(365)]
HAFTAICI_TATIL = sum(v for t, (a, v) in _RT.items() if t.weekday() < 5)
IS_GUNU = sum(1 - _bos(g) for g in _yil)
AY_T = []
for m in range(1, 13):
    gs = [g for g in _yil if g.month == m]
    AY_T.append((AY[m-1], sum(1 for g in gs if g.weekday() < 5), sum(_RT.get(g, ('', 0))[1] for g in gs if g.weekday() < 5), sum(1 - _bos(g) for g in gs)))
assert abs(sum(r[3] for r in AY_T) - IS_GUNU) < 1e-9

RT_TABLO = '<div class="table-wrap"><table><thead><tr><th>Tarih</th><th>Gün</th><th>Tatil</th><th>Süre</th></tr></thead><tbody>' + ''.join(
    f'<tr><td>{_d.date.fromisoformat(t).day} {AY[int(t[5:7])-1]} 2027</td><td>{GUN[_d.date.fromisoformat(t).weekday()]}</td><td>{a}</td><td>{"Yarım gün (13:00’ten sonra)" if v == 0.5 else "Tam gün"}</td></tr>' for t, a, v in RT) + '</tbody></table></div>'


def _kopru_satir(i):
    ad, bas, p = PLAN[i]
    sat = []
    for b in ['0', '1', '1.5', '2', '3']:
        u, iz, s, e, ig = p[b]
        sat.append((float(b), u, iz, s, e, ig))
    # aynı sonucu veren bütçeleri ele
    out, son, u0 = [], None, sat[0][1]
    for b, u, iz, s, e, ig in sat:
        if son and son == (u, s, e):
            continue
        son = (u, s, e)
        if iz and (u - u0) / iz < 2:
            continue  # verimsiz: izin günü kadar tatil kazandırıyor, köprü değil
        izs = ', '.join(_tr_kisa(_d.date.fromisoformat(g.split('|')[0])) + (' (yarım gün)' if g.endswith('|y') else '') for g in ig) or '—'
        out.append(f'<tr><td>{ad}</td><td>{_gun_s(iz) if iz else "İzinsiz"}</td><td>{izs}</td><td>{_tr_kisa(_d.date.fromisoformat(s)) + ((' – ' + _tr_kisa(_d.date.fromisoformat(e))) if e != s else '')}</td><td><b>{u} gün</b></td></tr>')
    return ''.join(out)


KOPRU_T = '<div class="table-wrap"><table><thead><tr><th>Tatil</th><th>Kullanılan izin</th><th>İzin alınacak günler</th><th>Tatil aralığı</th><th>Toplam</th></tr></thead><tbody>' + ''.join(
    _kopru_satir(i) for i in range(len(PLAN))) + '</tbody></table></div>'
AY_TABLO = '<div class="table-wrap"><table><thead><tr><th>Ay</th><th>Hafta içi gün</th><th>Hafta içine denk gelen tatil</th><th>İş günü</th></tr></thead><tbody>' + ''.join(
    f'<tr><td>{a}</td><td>{h}</td><td>{_gun_s(t) if t else "–"}</td><td>{f"{w:g}".replace(".", ",")}</td></tr>' for a, h, t, w in AY_T) + \
    f'<tr><td><b>Toplam</b></td><td><b>{sum(r[1] for r in AY_T)}</b></td><td><b>{_gun_s(HAFTAICI_TATIL)}</b></td><td><b>{f"{IS_GUNU:g}".replace(".", ",")}</b></td></tr></tbody></table></div>'

_ram = PLAN[KUME_AD.index('Ramazan Bayramı')][2]
_kur = PLAN[KUME_AD.index('Kurban Bayramı ve 19 Mayıs')][2]
TOPLAM_TATIL = sum(v for t, a, v in RT)

RT_JS = '''
var PL=''' + _j.dumps(PLAN, ensure_ascii=False) + r''';
var RTL=''' + _j.dumps(RT, ensure_ascii=False) + r''';
var AYL=['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'],GNL=['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'];
function d0(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2]);}
function kd(s){var d=d0(s);return d.getDate()+' '+AYL[d.getMonth()]+' '+GNL[d.getDay()];}
function gs(x){return String(x).replace('.',',')+' gün';}
function onReady(){run(false);}
function hesapla(){
  var b=el('butce').value, now=new Date(); now.setHours(0,0,0,0);
  var sec=el('tatil').value, rows=[], ilk=null;
  PL.forEach(function(k,i){
    if(sec!=='hepsi'&&String(i)!==sec) return;
    var p=k[2][b], kal=Math.round((d0(k[1])-now)/864e5);
    var iz=p[4].length?p[4].map(function(g){var y=g.indexOf('|y')>0;return kd(g.split('|')[0])+(y?' (yarım)':'');}).join(', '):'izin gerekmez';
    if(kal>=0&&(!ilk||p[0]>ilk[1][0])) ilk=[k,p,kal];
    rows.push(['<b>'+k[0]+'</b>'+(kal>=0?' <small>('+kal+' gün kaldı)</small>':' <small>(geçti)</small>'), '<b>'+p[0]+' gün</b> tatil: '+kd(p[2])+' – '+kd(p[3])+'<br><small>İzin: '+iz+(p[1]?' ('+gs(p[1])+')':'')+'</small>']);
  });
  if(!rows.length) return 'Seçim bulunamadı.';
  var f=ilk||[PL[0],PL[0][2][b],0];
  return {main:[f[0][0], f[1][0]+' gün tatil'], sub:(ilk?f[2]+' gün kaldı · ':'')+kd(f[1][2])+' – '+kd(f[1][3])+(f[1][1]?' · '+gs(f[1][1])+' izinle':' · izin gerekmez'),
    rows:rows, note:'Hesap hafta sonu çalışmayan (Pazartesi–Cuma) çalışanlar içindir; arife günleri 13:00’ten sonra tatildir, sabahı yarım gün izin sayılır. Kamuda idari izin kararı ayrıca açıklanabilir.'};
}'''

RT_FORM = '''<div class="form-grid"><div class="field"><label for="butce">Kaç gün izin kullanabilirsiniz?</label><select id="butce">
<option value="0">İzin kullanmadan</option><option value="0.5">Yarım gün</option><option value="1">1 gün</option><option value="1.5" selected>1,5 gün</option><option value="2">2 gün</option><option value="2.5">2,5 gün</option><option value="3">3 gün</option><option value="4">4 gün</option></select></div>
<div class="field"><label for="tatil">Hangi tatil?</label><select id="tatil"><option value="hepsi">Tüm 2027 tatilleri</option>''' + ''.join(
    f'<option value="{i}">{k[0]}</option>' for i, k in enumerate(PLAN)) + '''</select></div></div>'''

TOOLS.append(dict(
slug='resmi-tatiller-2027', name='2027 Resmi Tatiller ve Köprü Günleri', cat='diger', ico='🗓️',
title='2027 Resmi Tatiller ve Köprü Günleri – Ramazan ve Kurban Bayramı Ne Zaman?',
desc=f'2027’de Ramazan Bayramı 9–11 Mart, Kurban Bayramı 16–19 Mayıs. {_gun_s(_ram["1.5"][1])} izinle {_ram["1.5"][0]}, {_gun_s(_kur["2"][1])} izinle {_kur["2"][0]} gün tatil. Tüm resmi tatiller, köprü günleri ve kaç gün kaldı.',
h1='🗓️ 2027 Resmi Tatiller ve Köprü Günleri',
lead='2027 bayram ve resmi tatil günlerini, hangi güne denk geldiklerini ve kaç gün izinle kaç günlük tatil yapabileceğinizi görün. Bayrama kaç gün kaldığını da hesaplar.',
card_title='Kaç gün izinle kaç gün tatil?', button='Planı Göster',
badges=['✓ Ücretsiz', 'Diyanet takvimi', '2429 s. Kanun'],
form=RT_FORM, js=RT_JS,
article=f'''
<p><b>Kısa cevap:</b> 2027’de <b>Ramazan Bayramı 9–11 Mart</b> (Salı–Perşembe, arife 8 Mart Pazartesi öğleden sonra), <b>Kurban Bayramı 16–19 Mayıs</b> (Pazar–Çarşamba, arife 15 Mayıs Cumartesi). Ramazan Bayramı’nda arife sabahı ve Cuma için {_gun_s(_ram["1.5"][1])} izin alırsanız <b>{_ram["1.5"][0]} gün</b>, Kurban Bayramı’nda Perşembe–Cuma için {_gun_s(_kur["2"][1])} izinle <b>{_kur["2"][0]} gün</b> kesintisiz tatil yapabilirsiniz.</p>

<h2 id="liste">2027 resmi tatil günleri listesi</h2>
<p>Resmi tatiller 2429 sayılı Ulusal Bayram ve Genel Tatiller Hakkında Kanun’la belirlenir; Ramazan ve Kurban bayramlarının tarihleri her yıl Diyanet İşleri Başkanlığı takvimine göre değişir. 2027’de 19 Mayıs, Kurban Bayramı’nın 4. gününe denk geliyor; bu yüzden yıl genelinde toplam {_gun_s(TOPLAM_TATIL)} resmi tatil var (normal yıllarda 15,5 gün).</p>
{RT_TABLO}

<h2 id="kopru">2027 köprü günleri: kaç gün izinle kaç gün tatil?</h2>
<p>Aşağıdaki tablo, kullandığınız her izin gününe en az iki gün tatil kazandıran köprüleri listeler. Hesap Pazartesi–Cuma çalışan biri içindir; arife günlerinde 13:00’e kadar çalışıldığı için arife sabahı <b>yarım gün izin</b> sayılır.</p>
{KOPRU_T}
<p>En verimli köprüler: <b>Ramazan Bayramı</b> ({_gun_s(_ram["1.5"][1])} izin → {_ram["1.5"][0]} gün) ve <b>Kurban Bayramı</b> ({_gun_s(_kur["2"][1])} izin → {_kur["2"][0]} gün). 1 Ocak, 23 Nisan ve 29 Ekim Cuma’ya, 30 Ağustos Pazartesi’ye denk geldiği için izin kullanmadan 3 günlük hafta sonu oluşuyor. 1 Mayıs ise Cumartesi’ye denk geliyor.</p>

<h2 id="is-gunu">2027’de kaç iş günü var?</h2>
<p>Hafta sonları ve hafta içine denk gelen resmi tatiller düşüldüğünde 2027’de <b>{f"{IS_GUNU:g}".replace(".", ",")} iş günü</b> vardır (yarım günler 0,5 sayılmıştır). Ay ay dağılım:</p>
{AY_TABLO}
<p>İki tarih arasındaki iş günü sayısını bulmak için <a href="/is-gunu-hesaplama.html">iş günü hesaplama</a>, takvim günü farkı için <a href="/gun-hesaplama.html">gün hesaplama</a> aracını kullanabilirsiniz.</p>

<h2 id="ramazan">2027 Ramazan ayı ve dini günler</h2>
<ul>
<li><b>İlk teravih:</b> 7 Şubat 2027 Pazar akşamı</li>
<li><b>Ramazan’ın başlangıcı (ilk oruç):</b> 8 Şubat 2027 Pazartesi</li>
<li><b>Kadir Gecesi:</b> 5 Mart 2027 Cuma</li>
<li><b>Ramazan Bayramı arifesi:</b> 8 Mart 2027 Pazartesi (13:00’ten sonra tatil)</li>
<li><b>Ramazan Bayramı:</b> 9–11 Mart 2027 (Salı, Çarşamba, Perşembe)</li>
<li><b>Kurban Bayramı arifesi:</b> 15 Mayıs 2027 Cumartesi</li>
<li><b>Kurban Bayramı:</b> 16–19 Mayıs 2027 (Pazar–Çarşamba)</li>
</ul>

<h2 id="calisma">Resmi tatilde çalışana ne ödenir?</h2>
<p>İş Kanunu m.47’ye göre ulusal bayram ve genel tatil günlerinde çalışan işçiye, o gün için ayrıca <b>bir günlük ücret</b> daha ödenir; yani tatilde çalışılan gün toplam iki yevmiye eder. Bu günlerde çalışılıp çalışılmayacağı toplu sözleşme veya iş sözleşmesiyle belirlenir; hüküm yoksa işçinin onayı gerekir. Tatil ücretinizi <a href="/fazla-mesai-hesaplama.html">fazla mesai hesaplama</a> aracıyla, yıllık izin hakkınızı <a href="/yillik-izin-hesaplama.html">yıllık izin hesaplama</a> aracıyla bulabilirsiniz.</p>
<p><b>Not:</b> Kamu kurumlarında bayramların uzatılması (idari izin) Cumhurbaşkanlığı genelgesiyle ayrıca açıklanır; 2027 için henüz bir karar yayımlanmadı. Karar açıklanırsa bu sayfa güncellenir. Özel sektörde idari izin kararı bağlayıcı değildir.</p>
''',
faq=[
('2027 Ramazan Bayramı ne zaman?', '2027 Ramazan Bayramı 9 Mart Salı başlayıp 11 Mart Perşembe günü sona eriyor. Arife 8 Mart Pazartesi; arife günü 13:00’ten sonra resmi tatildir.'),
('2027 Kurban Bayramı ne zaman?', '2027 Kurban Bayramı 16 Mayıs Pazar – 19 Mayıs Çarşamba arasındadır. Arife 15 Mayıs Cumartesi. Bayramın 4. günü 19 Mayıs Atatürk’ü Anma, Gençlik ve Spor Bayramı’na denk geliyor.'),
('2027’de Ramazan ne zaman başlıyor?', 'Diyanet takvimine göre 2027’de ilk oruç 8 Şubat Pazartesi tutulacak; ilk teravih 7 Şubat Pazar akşamı kılınacak. Kadir Gecesi 5 Mart Cuma.'),
('2027 köprü günleri hangileri?', f'Ramazan Bayramı için 8 Mart arife sabahı ve 12 Mart Cuma ({_gun_s(_ram["1.5"][1])}) izin alınırsa {_ram["1.5"][0]} gün, Kurban Bayramı için 20–21 Mayıs Perşembe–Cuma ({_gun_s(_kur["2"][1])}) izin alınırsa {_kur["2"][0]} gün tatil olur. 15 Temmuz Perşembe olduğu için 16 Temmuz Cuma izin alınırsa 4 gün tatil yapılır.'),
('2027 yılbaşı hangi güne denk geliyor?', '1 Ocak 2027 Cuma gününe denk geliyor; Cumartesi ve Pazar ile birlikte 3 günlük tatil oluşuyor.'),
('2027’de kaç gün resmi tatil var?', f'2027’de toplam {_gun_s(TOPLAM_TATIL)} resmi tatil var; 19 Mayıs Kurban Bayramı’nın 4. gününe denk geldiği için bir gün eksik. Bunun {_gun_s(HAFTAICI_TATIL)} hafta içine denk geliyor ve yıl genelinde {f"{IS_GUNU:g}".replace(".", ",")} iş günü kalıyor.'),
('Arife günü tatil mi?', 'Ramazan ve Kurban bayramlarının arifesi ile 28 Ekim, saat 13:00’ten itibaren yarım gün resmi tatildir. Sabah mesaisi normal çalışma süresidir.'),
],
related=['is-gunu-hesaplama', 'gun-hesaplama', 'yillik-izin-hesaplama', 'ekonomi-takvimi', 'fazla-mesai-hesaplama'],
sources=[('2429 sayılı Ulusal Bayram ve Genel Tatiller Hakkında Kanun', 'https://www.mevzuat.gov.tr/'), ('Diyanet İşleri Başkanlığı 2027 dini günler takvimi', 'https://www.diyanet.gov.tr/'),
         ('4857 sayılı İş Kanunu m.47 (genel tatil ücreti)', 'https://www.mevzuat.gov.tr/')],
))
