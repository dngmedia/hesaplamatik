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
EVENTS = [(t, 'enflasyon', f'{v} enflasyonu', f'TÜİK, saat 10:00 · Belirler: {enf_etki(v)}', '/kira-artis-hesaplama.html') for t, v in ENF]
EVENTS += [
    ('2026-10-22', 'faiz', 'TCMB faiz kararı (PPK)', 'Politika faizi %37’den %36’ya indirildi (−100 baz puan)', '/mevduat-faizi-hesaplama.html'),
    ('2026-10-30', 'sinav', 'KPSS Önlisans sonuçları', 'ÖSYM 4 Ekim sınavının sonuçlarını açıklar (P93)', '/kpss-puan-hesaplama.html'),
    ('2026-11-19', 'sinav', 'KPSS Ortaöğretim sonuçları', 'ÖSYM 25 Ekim sınavının sonuçlarını açıklar (P94)', '/kpss-puan-hesaplama.html'),
    ('2026-11-29', 'sinav', 'ALES/3 sınavı', 'ÖSYM ALES/3 oturumu (sonuçlar 17 Aralık)', '/ales-puan-hesaplama.html'),
    ('2026-12-17', 'sinav', 'ALES/3 sonuçları', 'ÖSYM 29 Kasım ALES sonuçlarını açıklar', '/ales-puan-hesaplama.html'),
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
    ('2027-03-09', 'tatil', 'Ramazan Bayramı (9–11 Mart)', 'Arife 8 Mart yarım gün', '/is-gunu-hesaplama.html'),
    ('2027-03-31', 'vergi', 'Yıllık gelir vergisi beyannamesi son gün', '2026 gelirleri; 1–31 Mart, 1. taksit ödemesi', '/gelir-vergisi-hesaplama.html'),
    ('2027-05-16', 'tatil', 'Kurban Bayramı (16–19 Mayıs)', 'Arife 15 Mayıs yarım gün', '/is-gunu-hesaplama.html'),
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
<p>Ramazan Bayramı <b>9–11 Mart 2027</b> (arife 8 Mart yarım gün), Kurban Bayramı <b>16–19 Mayıs 2027</b> (arife 15 Mayıs yarım gün). Tüm resmî tatiller ve iki tarih arasındaki iş günü sayısı için <a href="/is-gunu-hesaplama.html">iş günü hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('Kasım ayında enflasyon ne zaman açıklanacak?', 'Ekim 2026 enflasyonu 3 Kasım 2026 Salı günü saat 10:00’da TÜİK tarafından açıklanacak. Kasım 2026 enflasyonu ise 3 Aralık 2026 Perşembe günü açıklanır.'),
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
