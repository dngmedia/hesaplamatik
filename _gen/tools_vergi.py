"""Vergi, SGK/çalışma hayatı, enflasyon ve fatura hesaplamaları (2026 verileri)."""

TOOLS = []

# ───────────────────────── MTV ─────────────────────────
TOOLS.append(dict(
slug='mtv-hesaplama', name='MTV Hesaplama', cat='vergi', ico='🚗',
title='MTV Hesaplama 2026 ve 2027 Tahmini – Motor Hacmi, Yaş ve Değere Göre | Hesaplarsın',
desc='2026 motorlu taşıtlar vergisini (MTV) motor hacmi, yaş, tescil yılı ve taşıt değerine göre hesaplayın; 2027 MTV tahminini iki senaryoyla görün. Otomobil ve motosiklet.',
h1='🚗 MTV Hesaplama 2026',
lead='Aracınızın motor silindir hacmini, yaşını ve ilk tescil yılını seçin; 2026 yılı motorlu taşıtlar vergisini, Ocak–Temmuz taksit tutarlarını ve yeniden değerleme oranına göre 2027 MTV tahminini görün.',
form='''<div class="form-grid">
<div class="field"><label for="tip">Araç Tipi</label><select id="tip"><option value="oto">Otomobil, arazi taşıtı, kaptıkaçtı</option><option value="moto">Motosiklet</option></select></div>
<div class="field" id="f-tescil"><label for="tescil">İlk Tescil Tarihi</label><select id="tescil"><option value="yeni">1 Ocak 2018 ve sonrası</option><option value="eski">31 Aralık 2017 ve öncesi</option></select></div>
<div class="field"><label for="cc">Motor Silindir Hacmi</label><select id="cc"></select></div>
<div class="field"><label for="yas">Araç Yaşı <small>(2026 − model yılı + 1)</small></label><select id="yas"><option value="0">1 – 3 yaş</option><option value="1">4 – 6 yaş</option><option value="2">7 – 11 yaş</option><option value="3">12 – 15 yaş</option><option value="4">16 yaş ve üzeri</option></select></div>
<div class="field full" id="f-deger"><label for="deger">Taşıt Değeri (₺) <small>ilk tescildeki KDV hariç değer — fatura/ÖTV matrahı</small></label><input type="number" id="deger" placeholder="örn: 650.000" inputmode="decimal"></div>
</div>''',
js=r'''
// 2026 MTV tarifeleri (I sayılı tarife). Değerler: [1-3, 4-6, 7-11, 12-15, 16+]
var CC=['1300 cm³ ve altı','1301 – 1600 cm³','1601 – 1800 cm³','1801 – 2000 cm³','2001 – 2500 cm³','2501 – 3000 cm³','3001 – 3500 cm³','3501 – 4000 cm³','4001 cm³ ve üzeri'];
var YENI=[ // [değer üst sınırı, tutarlar]
 [[309100,[5750,4010,2238,1689,593]],[541500,[6319,4409,2459,1861,655]],[Infinity,[6902,4807,2693,2032,706]]],
 [[309100,[10016,7510,4354,3077,1181]],[541500,[11023,8264,4794,3375,1290]],[Infinity,[12028,9012,5220,3685,1408]]],
 [[775100,[19472,15226,8948,5458,2113]],[Infinity,[21251,16600,9775,5964,2307]]],
 [[775100,[30679,23625,13886,8264,3248]],[Infinity,[33474,25784,15147,9012,3547]]],
 [[968100,[46027,33413,20874,12465,4930]],[Infinity,[50217,36448,22768,13606,5378]]],
 [[1937500,[64175,55837,34878,18758,6875]],[Infinity,[70018,60905,38053,20466,7503]]],
 [[1937500,[97744,87954,52976,26443,9684]],[Infinity,[106641,95940,57791,28839,10578]]],
 [[3101800,[153684,132712,78152,34878,13886]],[Infinity,[167671,144770,85271,38053,15147]]],
 [[3683200,[251554,188627,111714,50206,19472]],[Infinity,[274415,205781,121873,54769,21251]]]];
var ESKI=[[5750,4010,2238,1689,593],[10016,7510,4354,3077,1181],[17705,13829,8145,4957,1917],[27898,21478,12624,7510,2958],[41840,30372,18977,11333,4479],[58347,50754,31704,17044,6255],[88859,79955,48158,24031,8813],[139721,120647,71048,31704,12624],[228681,171485,101555,45632,17705]];
var MCC=['100 – 250 cm³','251 – 650 cm³','651 – 1200 cm³','1201 cm³ ve üzeri'];
var MOTO=[[1069,799,589,362,136],[2214,1676,1069,589,362],[5719,3398,1676,1069,589],[13876,9167,5719,4540,2214]];
function doldur(){var m=el('tip').value==='moto', s=el('cc'); s.innerHTML=(m?MCC:CC).map(function(t,i){return '<option value="'+i+'">'+t+'</option>';}).join('');
  el('f-tescil').style.display=m?'none':''; degerGoster();}
function degerGoster(){el('f-deger').style.display=(el('tip').value==='oto'&&el('tescil').value==='yeni')?'':'none';}
function onReady(){doldur(); el('tip').addEventListener('change',doldur); el('tescil').addEventListener('change',degerGoster);}
var R27=[[0.20,'sınırlı artış, %20'],[0.2781,'tam oran, %27,81']];
function hesapla(){
  var m=el('tip').value==='moto', c=+el('cc').value, y=+el('yas').value, aciklama, d=v('deger');
  function tut(yy){ if(m) return MOTO[c][yy]; if(el('tescil').value==='eski') return ESKI[c][yy]; var k=YENI[c]; for(var i=0;i<k.length;i++){if(d<=k[i][0]) return k[i][1][yy];} }
  if(!m&&el('tescil').value==='yeni'&&!(d>0)) return '2018 ve sonrası tescilli otomobillerde taşıt değerini girin.';
  var t=tut(y);
  aciklama=m?'Motosiklet · '+MCC[c]:(el('tescil').value==='eski'?'2017 ve öncesi tescil · '+CC[c]:'2018 sonrası tescil · '+CC[c]+' · değer '+tl(d,0));
  var rows=[['1. taksit (Ocak 2026)',tl(t/2)],['2. taksit (Temmuz 2026)',tl(t/2)],['Araç yaşı grubu',el('yas').options[y].text],['Aylık ortalama maliyet',tl(t/12)]];
  R27.forEach(function(r){rows.push(['2027 tahmini ('+r[1]+')',tl(Math.floor(t*(1+r[0])),0),'hl']);});
  if(y<4){var t2=tut(y+1); rows.push(['2027’de bir üst yaş grubuna geçerseniz ('+el('yas').options[y+1].text+')',tl(Math.floor(t2*1.20),0)+' – '+tl(Math.floor(t2*1.2781),0)]);}
  return {main:['2026 yıllık MTV', tl(t,0)], sub:aciklama, rows:rows,
    note:'2027 tutarları tahminidir: MTV, Kasım’da açıklanan yeniden değerleme oranıyla artar, ancak Cumhurbaşkanı daha düşük oran belirleyebilir (2026’da oran %25,49 iken MTV %18,95 artırıldı). Taksitler Ocak ve Temmuz sonuna kadar ödenir; kesin tutarı GİB İnternet Vergi Dairesi’nden sorgulayın.'};
}''',
article='''
<h2 id="nedir">MTV (motorlu taşıtlar vergisi) nedir?</h2>
<p>Motorlu taşıtlar vergisi, trafik siciline kayıtlı araçlar için her yıl ödenen bir servet vergisidir. 197 sayılı Motorlu Taşıtlar Vergisi Kanunu’na göre vergiyi, aracın trafik kaydında sahibi görünen kişi öder. MTV tutarları her yıl yeniden değerleme oranında güncellenir ve <b>Ocak</b> ile <b>Temmuz</b> aylarında iki eşit taksitle ödenir.</p>

<h2 id="nasil">MTV nasıl hesaplanır?</h2>
<p>Otomobiller için MTV dört bilgiye göre belirlenir:</p>
<ul>
<li><b>Motor silindir hacmi (cm³):</b> Ruhsatta yazar; motor büyüdükçe vergi artar.</li>
<li><b>Araç yaşı:</b> Model yılından itibaren hesaplanır (model yılı 1. yaş kabul edilir). 2026’da 2024–2026 model araçlar 1–3 yaş grubundadır.</li>
<li><b>İlk tescil tarihi:</b> 1 Ocak 2018 ve sonrası tescil edilen otomobillerde taşıt değeri de dikkate alınır.</li>
<li><b>Taşıt değeri:</b> Aracın ilk iktisabındaki ÖTV matrahı (KDV ve ÖTV hariç bedel).</li>
</ul>

<h2 id="tarife-yeni">2026 MTV tablosu – 2018 ve sonrası tescilli otomobiller (özet)</h2>
<div class="table-wrap"><table><thead><tr><th>Motor hacmi</th><th>Taşıt değeri</th><th>1–3 yaş</th><th>4–6 yaş</th><th>7–11 yaş</th><th>12–15 yaş</th><th>16+ yaş</th></tr></thead><tbody>
<tr><td rowspan="3">1300 cm³ ve altı</td><td>309.100 ₺’ye kadar</td><td>5.750</td><td>4.010</td><td>2.238</td><td>1.689</td><td>593</td></tr>
<tr><td>309.100 – 541.500 ₺</td><td>6.319</td><td>4.409</td><td>2.459</td><td>1.861</td><td>655</td></tr>
<tr><td>541.500 ₺ üzeri</td><td>6.902</td><td>4.807</td><td>2.693</td><td>2.032</td><td>706</td></tr>
<tr><td rowspan="3">1301 – 1600 cm³</td><td>309.100 ₺’ye kadar</td><td>10.016</td><td>7.510</td><td>4.354</td><td>3.077</td><td>1.181</td></tr>
<tr><td>309.100 – 541.500 ₺</td><td>11.023</td><td>8.264</td><td>4.794</td><td>3.375</td><td>1.290</td></tr>
<tr><td>541.500 ₺ üzeri</td><td>12.028</td><td>9.012</td><td>5.220</td><td>3.685</td><td>1.408</td></tr>
<tr><td rowspan="2">1601 – 1800 cm³</td><td>775.100 ₺’ye kadar</td><td>19.472</td><td>15.226</td><td>8.948</td><td>5.458</td><td>2.113</td></tr>
<tr><td>775.100 ₺ üzeri</td><td>21.251</td><td>16.600</td><td>9.775</td><td>5.964</td><td>2.307</td></tr>
<tr><td rowspan="2">1801 – 2000 cm³</td><td>775.100 ₺’ye kadar</td><td>30.679</td><td>23.625</td><td>13.886</td><td>8.264</td><td>3.248</td></tr>
<tr><td>775.100 ₺ üzeri</td><td>33.474</td><td>25.784</td><td>15.147</td><td>9.012</td><td>3.547</td></tr>
</tbody></table></div>
<p>2000 cm³ üzeri motorlar ve tüm kademeler hesaplayıcıda yer almaktadır. Tutarlar Türk lirası ve yıllıktır.</p>

<h2 id="tarife-eski">2026 MTV tablosu – 2017 ve öncesi tescilli otomobiller</h2>
<div class="table-wrap"><table><thead><tr><th>Motor hacmi</th><th>1–3 yaş</th><th>4–6 yaş</th><th>7–11 yaş</th><th>12–15 yaş</th><th>16+ yaş</th></tr></thead><tbody>
<tr><td>1300 cm³ ve altı</td><td>5.750</td><td>4.010</td><td>2.238</td><td>1.689</td><td>593</td></tr>
<tr><td>1301 – 1600 cm³</td><td>10.016</td><td>7.510</td><td>4.354</td><td>3.077</td><td>1.181</td></tr>
<tr><td>1601 – 1800 cm³</td><td>17.705</td><td>13.829</td><td>8.145</td><td>4.957</td><td>1.917</td></tr>
<tr><td>1801 – 2000 cm³</td><td>27.898</td><td>21.478</td><td>12.624</td><td>7.510</td><td>2.958</td></tr>
<tr><td>2001 – 2500 cm³</td><td>41.840</td><td>30.372</td><td>18.977</td><td>11.333</td><td>4.479</td></tr>
<tr><td>2501 – 3000 cm³</td><td>58.347</td><td>50.754</td><td>31.704</td><td>17.044</td><td>6.255</td></tr>
</tbody></table></div>

<h2 id="odeme">MTV ne zaman ve nasıl ödenir?</h2>
<ul>
<li>1. taksit: 1–31 Ocak 2026, 2. taksit: 1–31 Temmuz 2026.</li>
<li>Ödeme; GİB İnternet Vergi Dairesi, e-Devlet, banka mobil uygulamaları ve vergi dairelerinden yapılabilir.</li>
<li>Süresinde ödenmeyen MTV için aylık gecikme zammı uygulanır ve MTV borcu olan araçlar için muayene ve satış işlemleri yapılamaz.</li>
<li>Engelli bireyler adına kayıtlı belirli araçlar MTV’den muaftır.</li>
</ul>
<p>Araç satın alırken ÖTV’yi <a href="/otv-hesaplama.html">ÖTV hesaplama</a>, yıllık yakıt giderini <a href="/yakit-maliyeti-hesaplama.html">yakıt maliyeti hesaplama</a>, kredi taksitlerini <a href="/arac-kredisi-hesaplama.html">araç kredisi hesaplama</a> ile planlayabilirsiniz.</p>
''',
faq=[
('2026 MTV ne zaman ödenir?','İlk taksit Ocak 2026, ikinci taksit Temmuz 2026 sonuna kadar ödenir. İki taksit eşittir.'),
('Araç yaşı MTV’de nasıl hesaplanır?','Model yılı 1. yaş kabul edilir. 2026 yılında 2026, 2025 ve 2024 model araçlar 1–3 yaş grubundadır.'),
('Taşıt değeri nedir, nereden öğrenirim?','2018 sonrası tescilli otomobillerde, aracın ilk satışındaki KDV ve ÖTV hariç bedelidir. Fatura veya GİB MTV sorgulama ekranında görülebilir; ikinci el araçlarda ilk tescildeki değer esas alınır.'),
('Elektrikli araçlar MTV öder mi?','Evet. Elektrikli otomobillerde motor gücüne (kW) göre ayrı kademeler bulunur ve genellikle benzinli muadillerinin belirli bir oranı uygulanır.'),
('MTV gecikme faizi ne kadar?','Vadesinde ödenmeyen MTV için her ay için gecikme zammı uygulanır. Güncel oranı GİB üzerinden kontrol edin.'),
],
related=['otv-hesaplama','arac-kredisi-hesaplama','yakit-maliyeti-hesaplama','arac-muayene-gecikme-hesaplama','arac-deger-kaybi-hesaplama'],
sources=[('GİB İnternet Vergi Dairesi – MTV','https://ivd.gib.gov.tr/'),('197 sayılı Motorlu Taşıtlar Vergisi Kanunu','https://www.mevzuat.gov.tr/mevzuatmetin/1.4.197.pdf')],
))

# ───────────────────────── ÖTV ─────────────────────────
TOOLS.append(dict(
slug='otv-hesaplama', name='ÖTV Hesaplama', cat='vergi', ico='🏷️',
title='ÖTV Hesaplama – Vergisiz Fiyattan Satış Fiyatı ve Tersi | Hesaplarsın',
desc='Özel tüketim vergisini (ÖTV) ve üzerine eklenen KDV’yi hesaplayın. Vergisiz fiyattan anahtar teslim fiyatı, satış fiyatından vergisiz bedeli bulun. Araç ve diğer ürünler için.',
h1='🏷️ ÖTV Hesaplama',
lead='Vergisiz fiyatı ve ÖTV oranını girin; ÖTV, KDV ve toplam satış fiyatını görün. Ya da satış fiyatından geriye giderek ürünün vergisiz bedelini bulun.',
form='''<div class="field full" style="margin-bottom:14px"><label>Hesaplama Yönü</label>
<div class="seg"><label><input type="radio" name="mod" value="ileri" checked onchange="lbl()">Vergisiz fiyattan satış fiyatı</label><label><input type="radio" name="mod" value="geri" onchange="lbl()">Satış fiyatından vergisiz fiyat</label></div></div>
<div class="form-grid">
<div class="field"><label for="fiyat" id="lbl-fiyat">Vergisiz Fiyat / ÖTV Matrahı (₺)</label><input type="number" id="fiyat" placeholder="örn: 900.000" inputmode="decimal"></div>
<div class="field"><label for="otv">ÖTV Oranı (%)</label><input type="number" id="otv" placeholder="örn: 80" inputmode="decimal">
<div class="qtags"><span class="qtag" onclick="el('otv').value=25">%25</span><span class="qtag" onclick="el('otv').value=50">%50</span><span class="qtag" onclick="el('otv').value=80">%80</span><span class="qtag" onclick="el('otv').value=150">%150</span></div></div>
<div class="field"><label for="kdv">KDV Oranı</label><select id="kdv"><option value="20" selected>%20</option><option value="10">%10</option><option value="1">%1</option><option value="0">KDV yok</option></select></div>
</div>''',
js=r'''
function lbl(){el('lbl-fiyat').textContent=radio('mod')==='ileri'?'Vergisiz Fiyat / ÖTV Matrahı (₺)':'Vergiler Dahil Satış Fiyatı (₺)';el('result').style.display='none';_last=null;}
function hesapla(){
  var f=v('fiyat'), o=v('otv')/100, k=parseFloat(el('kdv').value)/100; if(!(f>0)) return 'Fiyatı girin.'; if(!(o>=0)) return 'ÖTV oranını girin.';
  var m=radio('mod')==='ileri'?f:f/((1+o)*(1+k)), otv=m*o, kdv=(m+otv)*k, top=m+otv+kdv;
  return {main:[radio('mod')==='ileri'?'Vergiler dahil satış fiyatı':'Vergisiz fiyat (ÖTV matrahı)', tl(radio('mod')==='ileri'?top:m)],
    rows:[['Vergisiz fiyat',tl(m)],['ÖTV (%'+num(o*100,o*100%1?1:0)+')',tl(otv)],['KDV matrahı (fiyat + ÖTV)',tl(m+otv)],['KDV (%'+num(k*100,0)+')',tl(kdv)],['Toplam vergi',tl(otv+kdv),'neg'],['Satış fiyatı',tl(top)],['Toplam vergi yükü (vergisiz fiyata göre)',pct((otv+kdv)/m*100)]],
    note:'KDV, ÖTV dahil tutar üzerinden hesaplanır (vergi üstüne vergi). Otomobillerde ÖTV oranı matrah (vergisiz fiyat) dilimine göre belirlenir.'};
}''',
article='''
<h2 id="nedir">ÖTV nedir?</h2>
<p>Özel Tüketim Vergisi (ÖTV), 4760 sayılı Kanun kapsamında belirli mal gruplarının ilk satışında veya ithalatında bir kez alınan bir vergidir. Akaryakıt, otomobil ve diğer motorlu taşıtlar, alkollü içkiler ve tütün ürünleri, cep telefonu gibi bazı elektronik ürünler ve lüks tüketim malları ÖTV’ye tabidir. ÖTV listelere göre oransal (yüzde) veya maktu (sabit tutar) olarak uygulanır.</p>
<div class="table-wrap"><table><thead><tr><th>Liste</th><th>Kapsam</th><th>Uygulama</th></tr></thead><tbody>
<tr><td>(I) sayılı liste</td><td>Akaryakıt, LPG, doğal gaz</td><td>Litre/kg başına maktu tutar</td></tr>
<tr><td>(II) sayılı liste</td><td>Otomobil, motosiklet, tekne, uçak</td><td>Matrah dilimine göre oran</td></tr>
<tr><td>(III) sayılı liste</td><td>Alkollü içki, tütün, kolalı içecek</td><td>Oran + asgari maktu tutar</td></tr>
<tr><td>(IV) sayılı liste</td><td>Beyaz eşya, elektronik, kozmetik vb.</td><td>Oran</td></tr>
</tbody></table></div>

<h2 id="nasil">ÖTV ve KDV nasıl hesaplanır?</h2>
<p>ÖTV, ürünün vergisiz fiyatı (matrah) üzerinden hesaplanır. KDV ise ÖTV eklenmiş tutar üzerinden hesaplanır. Bu nedenle toplam vergi yükü, iki oranın toplamından daha yüksektir.</p>
<div class="formula">ÖTV = Vergisiz fiyat × ÖTV oranı<br>KDV = (Vergisiz fiyat + ÖTV) × KDV oranı<br>Satış fiyatı = Vergisiz fiyat × (1 + ÖTV oranı) × (1 + KDV oranı)</div>
<div class="example"><p><b>Örnek:</b> Vergisiz fiyatı 900.000 ₺ olan, %80 ÖTV’ye tabi bir otomobil:</p>
<p>ÖTV = 720.000 ₺ → KDV matrahı 1.620.000 ₺ → KDV (%20) = 324.000 ₺ → <b>Anahtar teslim fiyat 1.944.000 ₺</b>. Toplam vergi 1.044.000 ₺, yani vergisiz fiyatın %116’sı.</p></div>

<h2 id="geri">Satış fiyatından vergisiz fiyat nasıl bulunur?</h2>
<div class="formula">Vergisiz fiyat = Satış fiyatı ÷ [(1 + ÖTV oranı) × (1 + KDV oranı)]</div>
<p>Örneğin 1.944.000 ₺’lik araçta %80 ÖTV ve %20 KDV varsa: 1.944.000 ÷ (1,80 × 1,20) = 900.000 ₺.</p>

<h2 id="otomobil">Otomobilde ÖTV oranı nasıl belirlenir?</h2>
<p>Binek otomobillerde ÖTV oranı; motor silindir hacmine ve aracın <b>vergisiz satış fiyatına (matrah)</b> göre kademeli olarak belirlenir. Elektrikli ve hibrit araçlar için ayrıca motor gücü (kW) ve batarya özellikleri dikkate alınır. Matrah dilimleri Cumhurbaşkanı kararlarıyla sık değiştiğinden aracınıza uygulanacak güncel oranı bayiden veya GİB’in yayımladığı listeden kontrol edin. Engelli bireyler belirli şartlarla ÖTV muafiyetli araç alabilir.</p>
<p>Araç alımından sonra ödeyeceğiniz yıllık vergiyi <a href="/mtv-hesaplama.html">MTV hesaplama</a> ile, KDV’yi ayrıca incelemek için <a href="/kdv-hesaplama.html">KDV hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('ÖTV KDV’ye dahil mi?','Hayır, ters yönde: KDV, ÖTV eklenmiş fiyat üzerinden hesaplanır. Yani ÖTV de KDV’ye tabidir.'),
('Araba fiyatının ne kadarı vergi?','ÖTV oranına bağlıdır. %80 ÖTV ve %20 KDV’li bir otomobilde satış fiyatının yaklaşık %54’ü vergidir.'),
('ÖTV kaç kez ödenir?','ÖTV ilk iktisapta (ilk satış veya ithalat) bir kez alınır. İkinci el satışlarda tekrar ÖTV ödenmez.'),
('Telefonlarda ÖTV oranı ne kadar?','Cep telefonları (IV) sayılı listede yer alır ve vergisiz fiyat dilimine göre değişen oranlarda ÖTV uygulanır. Güncel oranlar Cumhurbaşkanı kararlarıyla belirlenir.'),
],
related=['kdv-hesaplama','mtv-hesaplama','arac-kredisi-hesaplama','kdv-haric-hesaplama','gelir-vergisi-hesaplama'],
sources=[('4760 sayılı Özel Tüketim Vergisi Kanunu','https://www.mevzuat.gov.tr/mevzuatmetin/1.5.4760.pdf')],
))

# ───────────────────────── TAPU HARCI ─────────────────────────
TOOLS.append(dict(
slug='tapu-harci-hesaplama', name='Tapu Harcı Hesaplama', cat='gayrimenkul', ico='🏡',
title='Tapu Harcı Hesaplama 2026 – Alıcı ve Satıcı Payı (%4) | Hesaplarsın',
desc='2026 tapu harcını satış bedeline göre hesaplayın: toplam %4, alıcı %2, satıcı %2. Döner sermaye ücreti, beyan değeri kuralı ve ev alırken toplam maliyet.',
h1='🏡 Tapu Harcı Hesaplama 2026',
lead='Ev, arsa veya dükkân satışında ödenecek tapu harcını hesaplayın. Alıcı ve satıcı payını, döner sermaye ücretini ve alıcının toplam masrafını görün.',
form='''<div class="form-grid">
<div class="field"><label for="bedel">Satış Bedeli (₺)</label><input type="number" id="bedel" placeholder="örn: 3.500.000" inputmode="decimal"></div>
<div class="field"><label for="rayic">Emlak Vergi Değeri (₺) <small>isteğe bağlı</small></label><input type="number" id="rayic" placeholder="belediyeden" inputmode="decimal"></div>
<div class="field"><label for="doner">Döner Sermaye Ücreti (₺)</label><input type="number" id="doner" value="6681" inputmode="decimal"></div>
<div class="field"><label for="odeyen">Harcı Kim Ödüyor?</label><select id="odeyen"><option value="ayri" selected>Alıcı ve satıcı ayrı ayrı (%2 + %2)</option><option value="alici">Tamamını alıcı öder (%4)</option></select></div>
<div class="field"><label for="komisyon">Emlakçı Komisyonu (%) <small>alıcı payı, isteğe bağlı</small></label><input type="number" id="komisyon" placeholder="örn: 2" inputmode="decimal"></div>
</div>''',
js=r'''
function hesapla(){
  var b=v('bedel'), r=v('rayic')||0, d=v('doner')||0, k=v('komisyon')||0; if(!(b>0)) return 'Satış bedelini girin.';
  var matrah=Math.max(b,r), toplam=matrah*0.04, ayri=el('odeyen').value==='ayri', alici=ayri?toplam/2:toplam, satici=ayri?toplam/2:0;
  var kom=b*k/100*1.2, aliciTop=alici+d+kom;
  return {main:['Toplam tapu harcı', tl(toplam)], sub:'Harç matrahı: '+tl(matrah)+(r>b?' (beyan, emlak vergi değerinin altında olamaz)':''),
    rows:[['Alıcı payı',tl(alici)],['Satıcı payı',tl(satici)],['Döner sermaye ücreti',tl(d)],['Emlakçı komisyonu (KDV dahil)',tl(kom)],['Alıcının toplam masrafı',tl(aliciTop),'hl'],['Alıcının masraflar dahil toplam ödemesi',tl(b+aliciTop)]],
    note:'Döner sermaye ücreti il ve işlem türüne göre değişir; varsayılan değer 2026 için yaklaşık ortalamadır. Kesin tutar tapu randevusunda (Web Tapu) gösterilir.'};
}''',
article='''
<h2 id="nedir">Tapu harcı nedir?</h2>
<p>Tapu harcı, gayrimenkulün satış, bağış, trampa gibi yollarla el değiştirmesi sırasında tapu müdürlüğünde yapılan işlem için devlete ödenen harçtır. 492 sayılı Harçlar Kanunu’na göre satış işlemlerinde tapu harcı <b>satış bedelinin %4’ü</b>dür ve kanunen alıcı ile satıcı tarafından <b>%2’şer</b> olarak ödenir. Taraflar, harcın tamamının tek bir tarafça ödenmesi konusunda anlaşabilir.</p>

<h2 id="nasil">Tapu harcı nasıl hesaplanır?</h2>
<div class="formula">Toplam tapu harcı = Satış bedeli × %4<br>Alıcı payı = Satış bedeli × %2 · Satıcı payı = Satış bedeli × %2</div>
<div class="example"><p><b>Örnek:</b> 3.500.000 ₺’ye satılan bir daire için:</p>
<p>Toplam harç: 3.500.000 × 0,04 = <b>140.000 ₺</b>. Alıcı 70.000 ₺, satıcı 70.000 ₺ öder. Buna döner sermaye ücreti eklenir.</p></div>

<h2 id="tablo">2026 tapu harcı tablosu</h2>
<p>Farklı satış bedellerinde tapu harcı ve alıcının başlıca masrafları (emlakçı komisyonu %2 + %20 KDV varsayımıyla):</p>
<div class="table-wrap"><table><thead><tr><th>Satış bedeli</th><th>Toplam harç (%4)</th><th>Alıcı harç payı (%2)</th><th>Komisyon (alıcı)</th><th>Alıcı harç + komisyon</th></tr></thead><tbody>
<tr><td>2.000.000 ₺</td><td>80.000 ₺</td><td>40.000 ₺</td><td>48.000 ₺</td><td>88.000 ₺</td></tr><tr><td>3.000.000 ₺</td><td>120.000 ₺</td><td>60.000 ₺</td><td>72.000 ₺</td><td>132.000 ₺</td></tr><tr><td>4.000.000 ₺</td><td>160.000 ₺</td><td>80.000 ₺</td><td>96.000 ₺</td><td>176.000 ₺</td></tr><tr><td>5.000.000 ₺</td><td>200.000 ₺</td><td>100.000 ₺</td><td>120.000 ₺</td><td>220.000 ₺</td></tr><tr><td>7.500.000 ₺</td><td>300.000 ₺</td><td>150.000 ₺</td><td>180.000 ₺</td><td>330.000 ₺</td></tr><tr><td>10.000.000 ₺</td><td>400.000 ₺</td><td>200.000 ₺</td><td>240.000 ₺</td><td>440.000 ₺</td></tr>
</tbody></table></div>
<p>Tabloya döner sermaye ücreti, sigorta ve kredi masrafları dahil değildir. Kendi tutarınız için yukarıdaki hesaplayıcıyı kullanın.</p>

<h2 id="adimlar">Tapu devri adım adım</h2>
<ol>
<li><b>Başvuru:</b> Alıcı veya satıcı Web Tapu üzerinden ya da tapu müdürlüğünden satış başvurusu yapar; satış bedeli beyan edilir.</li>
<li><b>Harç ve döner sermaye ödemesi:</b> Sistem harcı ve döner sermaye ücretini hesaplar; ödeme anlaşmalı bankalar veya internet bankacılığından yapılır.</li>
<li><b>Randevu:</b> Taraflar kimlikleri ve gerekiyorsa vekâletnameyle randevu saatinde tapu müdürlüğünde hazır bulunur.</li>
<li><b>İmza:</b> Resmî senet imzalanır, mülkiyet aynı gün alıcıya geçer.</li>
</ol>
<p>Satış bedelinin ödemesini tapu imzasıyla eş zamanlı yapmak için bankaların aracılık ettiği <b>güvenli ödeme</b> sistemlerinden yararlanabilirsiniz.</p>

<h2 id="satis-sonrasi">Satıcı açısından vergi: değer artış kazancı</h2>
<p>Konutu satın aldıktan sonraki <b>5 yıl içinde</b> satan kişi, alış ve satış bedeli arasındaki kazanç için değer artış kazancı vergisine tabi olabilir. 2026 yılında bu kazancın <b>150.000 ₺</b>’lik kısmı vergiden istisnadır. Alış bedeli, yeniden değerleme ile güncellenerek hesaplanır. Tapuda gerçek bedelin gösterilmesi bu hesapta hem alıcıyı hem satıcıyı korur. Miras yoluyla edinilen gayrimenkullerin satışında bu vergi doğmaz.</p>

<h2 id="matrah">Tapuda gösterilecek bedel ne olmalı?</h2>
<p>Tapu harcı, tapuda beyan edilen satış bedeli üzerinden alınır. Ancak beyan edilen bedel, gayrimenkulün belediyedeki <b>emlak vergisi değerinden</b> düşük olamaz. Gerçek satış bedelinin altında beyanda bulunmak vergi ziyaı cezasına yol açar; ayrıca konut kredisi kullanılan satışlarda ekspertiz değeri dikkate alınır. Gerçek bedelin tapuya yazılması hem yasal yükümlülük hem de ileride satışta değer artış kazancı vergisi açısından alıcının lehinedir.</p>

<h2 id="doner">Döner sermaye ücreti 2026</h2>
<p>Tapu işlemlerinde harca ek olarak Tapu ve Kadastro Genel Müdürlüğü döner sermaye ücreti alınır. Bu ücret ile, işlem türüne ve bağımsız bölüm sayısına göre değişir; 2026’da tek bağımsız bölümlü bir konut satışında genellikle <b>5.500–7.000 ₺</b> aralığındadır. Kesin tutar Web Tapu üzerinden başvuru yaparken gösterilir; hesaplayıcıdaki varsayılan değeri kendi tutarınızla değiştirebilirsiniz.</p>

<h2 id="toplam">Ev alırken ödenen diğer masraflar</h2>
<div class="table-wrap"><table><thead><tr><th>Masraf</th><th>Tutar / Oran</th></tr></thead><tbody>
<tr><td>Tapu harcı (alıcı payı)</td><td>Satış bedelinin %2’si</td></tr>
<tr><td>Döner sermaye ücreti</td><td>İle ve işleme göre, genellikle 5.500–7.000 ₺</td></tr>
<tr><td>Emlakçı komisyonu</td><td>Genellikle %2 + KDV (alıcı ve satıcıdan ayrı ayrı)</td></tr>
<tr><td>Zorunlu deprem sigortası (DASK)</td><td>Metrekare ve bölgeye göre</td></tr>
<tr><td>Konut kredisi masrafları</td><td>Ekspertiz, ipotek tesis, dosya ücreti</td></tr>
<tr><td>Abonelik devirleri</td><td>Elektrik, su, doğal gaz güvence bedelleri</td></tr>
</tbody></table></div>

<h2 id="istisna">Tapu harcı istisnaları</h2>
<ul>
<li>Kentsel dönüşüm kapsamındaki işlemler harçtan muaftır.</li>
<li>Mirasın intikalinde satış harcı yerine veraset ve intikal vergisi söz konusudur.</li>
</ul>
<p>Satın almayı düşündüğünüz evin birim fiyatını <a href="/metrekare-fiyat-hesaplama.html">metrekare fiyatı hesaplama</a>, yatırım getirisini <a href="/kira-getirisi-hesaplama.html">kira getirisi hesaplama</a> ile değerlendirebilirsiniz.</p>
''',
faq=[
('2026 tapu harcı yüzde kaç?','Satış bedelinin toplam %4’üdür: alıcı %2, satıcı %2 öder.'),
('Tapu harcını kim öder?','Kanuna göre alıcı ve satıcı %2’şer öder. Uygulamada tarafların anlaşmasıyla tamamı alıcı tarafından da ödenebilir; bu durumda devlet açısından her iki taraf da müteselsilen sorumludur.'),
('Tapu harcı emlak vergi değerinden düşük gösterilebilir mi?','Hayır. Beyan edilen bedel emlak vergisi değerinin altında olamaz ve gerçek satış bedelinin altında beyan vergi cezasına yol açar.'),
('5 milyon TL’lik evin tapu harcı ne kadar?','Toplam tapu harcı 5.000.000 × %4 = 200.000 TL’dir. Alıcı ve satıcı ayrı ayrı ödüyorsa her biri 100.000 TL öder; buna döner sermaye ücreti eklenir.'),
('Tapu harcı nereden ödenir?','Web Tapu üzerinden başvuru yapıldıktan sonra harç ve döner sermaye ücreti anlaşmalı bankalar, internet bankacılığı veya e-Devlet aracılığıyla ödenebilir.'),
],
related=['kira-getirisi-hesaplama','metrekare-fiyat-hesaplama','kira-artis-hesaplama','damga-vergisi-hesaplama','kredi-hesaplama'],
sources=[('492 sayılı Harçlar Kanunu','https://www.mevzuat.gov.tr/mevzuatmetin/1.5.492.pdf'),('Tapu ve Kadastro GM – Web Tapu','https://webtapu.tkgm.gov.tr/')],
))

# ───────────────────────── DAMGA VERGİSİ ─────────────────────────
TOOLS.append(dict(
slug='damga-vergisi-hesaplama', name='Damga Vergisi Hesaplama', cat='vergi', ico='📜',
title='Damga Vergisi Hesaplama 2026 – Sözleşme, Kira, Maaş (Binde 9,48) | Hesaplarsın',
desc='2026 damga vergisini hesaplayın: sözleşmelerde binde 9,48, kira sözleşmelerinde binde 1,89, ücretlerde binde 7,59. Azami tutar ve çok nüsha kuralı dahil.',
h1='📜 Damga Vergisi Hesaplama 2026',
lead='Sözleşme, kira kontratı, taahhütname veya maaş bordrosu için ödenecek damga vergisini belge türü ve tutara göre hesaplayın.',
form='''<div class="form-grid">
<div class="field full"><label for="tur">Belge Türü</label><select id="tur">
<option value="9.48">Belirli parayı içeren sözleşme, taahhütname (binde 9,48)</option>
<option value="1.89">Kira sözleşmesi (binde 1,89 – toplam kira üzerinden)</option>
<option value="7.59">Maaş, ücret, avans bordrosu (binde 7,59)</option>
<option value="5.69">İhale kararları (binde 5,69)</option>
<option value="1.89f">Fesih sözleşmesi, ikinci el araç satış sözleşmesi (binde 1,89)</option>
</select></div>
<div class="field" id="f-tutar"><label for="tutar" id="lbl-tutar">Sözleşme Tutarı (₺)</label><input type="number" id="tutar" placeholder="örn: 1.000.000" inputmode="decimal"></div>
<div class="field" id="f-ay" style="display:none"><label for="ay">Kira Süresi (ay)</label><input type="number" id="ay" value="12" inputmode="numeric"></div>
<div class="field"><label for="nusha">Nüsha Sayısı</label><input type="number" id="nusha" value="1" inputmode="numeric"></div>
</div>''',
js=r'''
var AZAMI=29115961.10;
function onReady(){el('tur').addEventListener('change',function(){var k=el('tur').value==='1.89';el('f-ay').style.display=k?'':'none';el('lbl-tutar').textContent=k?'Aylık Kira (₺)':(el('tur').value==='7.59'?'Brüt Ücret (₺)':'Sözleşme Tutarı (₺)');});}
function hesapla(){
  var t=v('tutar'), tur=el('tur').value, oran=parseFloat(tur)/1000, n=Math.max(1,Math.round(v('nusha')||1)); if(!(t>0)) return 'Tutarı girin.';
  var matrah=t, rows=[];
  if(tur==='1.89'){var ay=v('ay')||12; matrah=t*ay; rows.push(['Toplam kira (matrah)',tl(matrah)]);}
  var tek=matrah*oran, sinir=false; if(tek>AZAMI){tek=AZAMI;sinir=true;}
  rows.push(['Oran','binde '+num(oran*1000,2)]); rows.push(['Bir nüsha için damga vergisi',tl(tek)]); if(n>1) rows.push(['Nüsha sayısı',n]);
  if(tur==='7.59') rows.push(['Asgari ücret istisnası düşülmüş (bordro)',tl(Math.max(0,t-33030)*oran),'hl']);
  return {main:['Damga vergisi', tl(tek*n)], sub:sinir?'Azami tutar sınırı uygulandı':'', rows:rows,
    note:tur==='1.89'?'Kira sözleşmelerinde süre belirtilmemişse 1 yıllık kira esas alınır. Birden fazla nüshada her nüsha ayrı vergilendirilir.':(tur==='7.59'?'Ücretlerde asgari ücrete isabet eden kısım damga vergisinden istisnadır.':'Aynı belgenin birden fazla imzalı nüshası varsa her biri ayrıca vergiye tabidir.')};
}''',
article='''
<h2 id="nedir">Damga vergisi nedir?</h2>
<p>Damga vergisi, 488 sayılı Damga Vergisi Kanunu’na ekli tabloda sayılan kâğıtlar (sözleşmeler, taahhütnameler, kira kontratları, makbuzlar, bordrolar, beyannameler vb.) üzerinden alınan bir vergidir. Vergi, belgenin imzalanmasıyla doğar ve belgede yazılı tutar üzerinden <b>nispi</b> (binde oran) veya belli bir tutar içermeyen kâğıtlarda <b>maktu</b> (sabit) olarak alınır.</p>

<h2 id="oranlar">2026 damga vergisi oranları</h2>
<div class="table-wrap"><table><thead><tr><th>Belge</th><th>Oran / Tutar</th></tr></thead><tbody>
<tr><td>Belirli parayı ihtiva eden sözleşmeler, taahhütnameler</td><td>Binde 9,48</td></tr>
<tr><td>Kira sözleşmeleri (kira bedeli üzerinden)</td><td>Binde 1,89</td></tr>
<tr><td>Fesih sözleşmeleri, ikinci el araç satış sözleşmeleri</td><td>Binde 1,89</td></tr>
<tr><td>Maaş, ücret, avans ve kredi makbuzları</td><td>Binde 7,59</td></tr>
<tr><td>İhale kararları</td><td>Binde 5,69</td></tr>
<tr><td>Yıllık gelir vergisi beyannamesi</td><td>1.189,50 ₺ (maktu)</td></tr>
<tr><td>Kurumlar vergisi beyannamesi</td><td>1.605,80 ₺ (maktu)</td></tr>
<tr><td>KDV, muhtasar ve diğer beyannameler</td><td>791,00 ₺ (maktu)</td></tr>
<tr><td>Bir kâğıt için azami damga vergisi</td><td>29.115.961,10 ₺</td></tr>
</tbody></table></div>

<h2 id="nasil">Damga vergisi nasıl hesaplanır?</h2>
<div class="formula">Damga vergisi = Belgedeki tutar × Binde oran ÷ 1000 × Nüsha sayısı</div>
<div class="example"><p><b>Örnek 1 – Sözleşme:</b> 1.000.000 ₺’lik hizmet sözleşmesi, 2 nüsha: 1.000.000 × 9,48 ÷ 1000 = 9.480 ₺ × 2 = <b>18.960 ₺</b>.</p>
<p><b>Örnek 2 – Kira:</b> Aylık 20.000 ₺, 12 aylık kira sözleşmesi: 240.000 × 1,89 ÷ 1000 = <b>453,60 ₺</b>.</p></div>

<h2 id="kim-oder">Damga vergisini kim öder?</h2>
<p>Kanuna göre damga vergisini belgeyi imzalayanlar öder. Birden fazla imzası olan belgelerde taraflar müteselsilen sorumludur; uygulamada pay oranı sözleşmeyle belirlenir. Kira sözleşmelerinde damga vergisi genellikle kiracı tarafından ödenir; ancak kanuni sorumluluk her iki taraf içindir. Maaş bordrolarında ise vergi işveren tarafından kesilerek muhtasar beyanname ile ödenir.</p>

<h2 id="istisna">Önemli istisnalar</h2>
<ul>
<li>Ücretlerin asgari ücrete isabet eden kısmı damga vergisinden istisnadır. Bordro etkisini <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracında görebilirsiniz.</li>
<li>Kredi kullanımıyla ilgili bazı kâğıtlar, konut finansmanı sözleşmeleri ve kamu kurumlarına ait belirli belgeler istisna kapsamındadır.</li>
<li>Ön ödemeli konut satış sözleşmeleri ve kat karşılığı inşaat sözleşmeleri 2026 tablosunda binde 0 oranındadır.</li>
</ul>
<p>Gayrimenkul alım-satımında ayrıca <a href="/tapu-harci-hesaplama.html">tapu harcı</a> ödenir; damga vergisi tapu işlemlerine ayrıca uygulanmaz.</p>
''',
faq=[
('2026 damga vergisi oranı kaç?','Belirli parayı içeren sözleşmelerde binde 9,48, kira sözleşmelerinde binde 1,89, ücret bordrolarında binde 7,59’dur.'),
('Kira sözleşmesinde damga vergisi nasıl hesaplanır?','Sözleşme süresince ödenecek toplam kira binde 1,89 ile çarpılır. Süre belirtilmemişse 1 yıllık kira esas alınır.'),
('Damga vergisi ne zaman ödenir?','Beyanname ile ödenen damga vergisi, belgenin düzenlendiği ayı izleyen ayın 26’sına kadar muhtasar ve prim hizmet beyannamesi ile beyan edilip ödenir. Vergi dairesinden makbuz karşılığı da ödenebilir.'),
('Damga vergisi ödenmezse ne olur?','Vergi ziyaı cezası ve gecikme faizi uygulanır. Ayrıca belge geçerliliğini korur, ancak vergi borcu ve ceza taraflar için doğar.'),
],
related=['tapu-harci-hesaplama','kira-artis-hesaplama','net-maas-hesaplama','gelir-vergisi-hesaplama','kdv-hesaplama'],
sources=[('488 sayılı Damga Vergisi Kanunu','https://www.mevzuat.gov.tr/mevzuatmetin/1.3.488.pdf'),('PwC – Damga Vergisi Oran ve Tutarları','https://www.pwc.com.tr/tr/hizmetlerimiz/vergi/vergi-portali/pratik-bilgiler/oranlar/damga-vergisi-oran-ve-tutarlari.html')],
))

# ───────────────────────── ASGARİ ÜCRET ─────────────────────────
TOOLS.append(dict(
slug='asgari-ucret-hesaplama', name='Asgari Ücret Hesaplama', cat='maas', ico='💵',
title='Asgari Ücret 2026 – Net 28.075,50 TL, Brüt 33.030 TL | Hesaplarsın',
desc='2026 asgari ücret net 28.075,50 TL, brüt 33.030 TL. Kesintiler, işverene maliyeti (teşvikli/teşviksiz), günlük ve saatlik asgari ücret ile kısmi çalışma hesabı.',
h1='💵 Asgari Ücret 2026 Hesaplama',
lead='2026 yılı asgari ücretin net, brüt, günlük ve saatlik tutarlarını, kesintileri ve işverene toplam maliyetini görün. Eksik gün çalışanlar için kısmi hesaplama yapın.',
form='''<div class="form-grid">
<div class="field"><label for="gun">Çalışılan Gün <small>(tam ay = 30)</small></label><input type="number" id="gun" value="30" inputmode="numeric"></div>
<div class="field"><label for="tesvik">İşveren SGK İndirimi</label><select id="tesvik"><option value="0.2175">Teşviksiz (%21,75)</option><option value="0.1975" selected>2 puan indirim – genel (%19,75)</option><option value="0.1675">5 puan indirim – imalat (%16,75)</option></select></div>
</div>''',
side='''<div class="card"><div class="side-title">💵 2026 Asgari Ücret Özeti</div><div class="res-rows" style="font-size:.84rem">
<div class="res-row"><span>Brüt</span><b>33.030,00 ₺</b></div><div class="res-row"><span>Net</span><b style="color:var(--success)">28.075,50 ₺</b></div>
<div class="res-row"><span>Günlük brüt</span><b>1.101,00 ₺</b></div><div class="res-row"><span>Saatlik brüt</span><b>146,80 ₺</b></div></div></div>''',
js=r'''
var BR=33030;
function hesapla(){
  var g=Math.round(v('gun')); if(!(g>0&&g<=30)) return 'Çalışılan gün 1–30 arasında olmalı.';
  var b=BR/30*g, sgk=b*0.14, iss=b*0.01, net=b-sgk-iss, isv=parseFloat(el('tesvik').value), isvSgk=b*isv, isvIss=b*0.02;
  return {main:[g===30?'2026 net asgari ücret':g+' günlük net asgari ücret', tl(net)], sub:'Brüt: '+tl(b),
    rows:[['Brüt ücret',tl(b)],['SGK işçi payı (%14)','−'+tl(sgk),'neg'],['İşsizlik sigortası işçi payı (%1)','−'+tl(iss),'neg'],['Gelir vergisi','0,00 ₺ (istisna)'],['Damga vergisi','0,00 ₺ (istisna)'],['Net ücret',tl(net),'hl'],
      ['İşveren SGK payı (%'+num(isv*100,2)+')',tl(isvSgk)],['İşveren işsizlik payı (%2)',tl(isvIss)],['İşverene toplam maliyet',tl(b+isvSgk+isvIss)]]};
}''',
article='''
<h2 id="tutar">2026 asgari ücret ne kadar?</h2>
<p>Asgari Ücret Tespit Komisyonu kararıyla 1 Ocak 2026’dan itibaren geçerli olan asgari ücret <b>brüt 33.030,00 ₺</b>, <b>net 28.075,50 ₺</b>’dir. Asgari ücret tüm sektörler ve tüm illerde aynıdır; 16 yaşından küçükler ile büyükler arasındaki ayrım da kaldırılmıştır.</p>
<div class="table-wrap"><table><thead><tr><th>Kalem</th><th>Aylık</th><th>Günlük</th><th>Saatlik</th></tr></thead><tbody>
<tr><td>Brüt asgari ücret</td><td>33.030,00 ₺</td><td>1.101,00 ₺</td><td>146,80 ₺</td></tr>
<tr><td>SGK işçi payı (%14)</td><td>4.624,20 ₺</td><td></td><td></td></tr>
<tr><td>İşsizlik sigortası işçi payı (%1)</td><td>330,30 ₺</td><td></td><td></td></tr>
<tr><td>Gelir vergisi ve damga vergisi</td><td>0 ₺ (istisna)</td><td></td><td></td></tr>
<tr><td><b>Net asgari ücret</b></td><td><b>28.075,50 ₺</b></td><td>935,85 ₺</td><td>124,78 ₺</td></tr>
</tbody></table></div>

<h2 id="maliyet">Asgari ücretin işverene maliyeti 2026</h2>
<p>İşveren, brüt ücretin üzerine SGK işveren payı ve işsizlik sigortası işveren payı öder. 2026’da SGK işveren payı teşviksiz %21,75’tir. Prim borcu olmayan işverenlere genel olarak 2 puan, imalat sektöründe 5 puan indirim uygulanır. İşsizlik sigortası işveren payı %2’dir.</p>
<div class="table-wrap"><table><thead><tr><th>Senaryo</th><th>SGK işveren payı</th><th>İşsizlik (%2)</th><th>Toplam maliyet</th></tr></thead><tbody>
<tr><td>Teşviksiz (%21,75)</td><td>7.184,03 ₺</td><td>660,60 ₺</td><td>40.874,63 ₺</td></tr>
<tr><td>2 puan indirimli (%19,75)</td><td>6.523,43 ₺</td><td>660,60 ₺</td><td>40.214,03 ₺</td></tr>
<tr><td>5 puan indirimli – imalat (%16,75)</td><td>5.532,53 ₺</td><td>660,60 ₺</td><td>39.223,13 ₺</td></tr>
</tbody></table></div>

<h2 id="istisna">Asgari ücret vergi istisnası nedir?</h2>
<p>2022’den bu yana asgari ücret gelir vergisi ve damga vergisinden istisnadır. Üstelik bu istisna yalnızca asgari ücretlilere değil, tüm çalışanlara uygulanır: her çalışanın maaşından hesaplanan vergiden, asgari ücrete isabet eden vergi tutarı düşülür. Asgari ücretin üzerinde maaş alıyorsanız net ücretinizi <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracında görebilirsiniz.</p>

<h2 id="kismi">Eksik gün çalışmada asgari ücret nasıl hesaplanır?</h2>
<p>Ay içinde eksik çalışan işçinin ücreti, brüt asgari ücretin 30’a bölünüp çalışılan gün sayısıyla çarpılmasıyla bulunur. Hesaplayıcıdaki “Çalışılan Gün” alanına gün sayısını yazarak kısmi net ücreti görebilirsiniz. Saatlik çalışanlar için <a href="/saatlik-ucret-hesaplama.html">saatlik ücret hesaplama</a> aracını kullanabilirsiniz.</p>

<h2 id="yillik">Asgari ücretin yıllık tutarları (2026)</h2>
<div class="table-wrap"><table><thead><tr><th>Kalem</th><th>Aylık</th><th>Yıllık (12 ay)</th></tr></thead><tbody>
<tr><td>Brüt ücret</td><td>33.030,00 ₺</td><td>396.360,00 ₺</td></tr>
<tr><td>Net ücret (çalışanın eline geçen)</td><td>28.075,50 ₺</td><td>336.906,00 ₺</td></tr>
<tr><td>İşverene maliyet (2 puan teşvikli)</td><td>40.214,03 ₺</td><td>482.568,36 ₺</td></tr>
<tr><td>İşverene maliyet (teşviksiz)</td><td>40.874,63 ₺</td><td>490.495,56 ₺</td></tr>
</tbody></table></div>
<p>Net asgari ücret yıl boyunca değişmez; çünkü asgari ücretli çalışan gelir vergisi ödemediği için vergi dilimi geçişinden etkilenmez. Asgari ücretin üzerinde maaş alanların net ücreti ise yıl içinde vergi dilimi nedeniyle düşebilir; bunu <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracında ay seçerek görebilirsiniz.</p>

<h2 id="mesai">Asgari ücretle fazla mesai ve bayram çalışması</h2>
<div class="table-wrap"><table><thead><tr><th>Çalışma türü</th><th>Hesap</th><th>Brüt tutar</th></tr></thead><tbody>
<tr><td>Normal saat ücreti</td><td>33.030 ÷ 225 saat</td><td>146,80 ₺</td></tr>
<tr><td>Fazla mesai (haftalık 45 saati aşan)</td><td>146,80 × 1,5</td><td>220,20 ₺ / saat</td></tr>
<tr><td>Fazla sürelerle çalışma (sözleşmede 45 saatten az ise)</td><td>146,80 × 1,25</td><td>183,50 ₺ / saat</td></tr>
<tr><td>Ulusal bayram ve genel tatilde çalışma</td><td>1 günlük ek ücret</td><td>1.101,00 ₺ / gün</td></tr>
</tbody></table></div>
<p>Fazla mesai ve bayram ücretleri asgari ücret istisnasının dışında kalan kısım olduğu için bu ödemelerden gelir vergisi ve damga vergisi kesilebilir. Ayrıntılı hesap için <a href="/fazla-mesai-hesaplama.html">fazla mesai hesaplama</a> aracını kullanın.</p>

<h2 id="bes">Asgari ücretten BES kesintisi yapılır mı?</h2>
<p>Otomatik katılım sistemi kapsamındaki çalışanların brüt ücretinin <b>%3</b>’ü bireysel emeklilik sistemine aktarılır. Asgari ücretli bir çalışan için bu tutar ayda 990,90 ₺’dir ve net ücretten düşülür. Çalışan, sisteme dahil edildikten sonraki 2 ay içinde cayma hakkını kullanabilir; cayarsa kesilen tutar iade edilir.</p>

<h2 id="alti">Asgari ücretin altında maaş ödenebilir mi?</h2>
<p>Hayır. Tam süreli çalışan bir işçiye asgari ücretin altında ücret ödenemez; bu durum İş Kanunu’na göre idari para cezası gerektirir ve işçiye haklı nedenle fesih hakkı verir. Kısmi süreli (part-time) çalışanlarda ise asgari ücret, çalışılan saat oranında uygulanır: haftada 22,5 saat çalışan bir işçinin brüt asgari ücreti 16.515 ₺ olur.</p>

<h2 id="tarihce">Son yıllarda asgari ücret</h2>
<div class="table-wrap"><table><thead><tr><th>Dönem</th><th>Brüt</th><th>Net</th></tr></thead><tbody>
<tr><td>2026</td><td>33.030,00 ₺</td><td>28.075,50 ₺</td></tr>
<tr><td>2025</td><td>26.005,50 ₺</td><td>22.104,67 ₺</td></tr>
<tr><td>2024</td><td>20.002,50 ₺</td><td>17.002,12 ₺</td></tr>
<tr><td>Temmuz 2023</td><td>13.414,50 ₺</td><td>11.402,32 ₺</td></tr>
</tbody></table></div>
<p>2027 asgari ücreti Aralık 2026’da açıklanacak. Kurum tahminleri ve senaryolar için <a href="/blog/asgari-ucret-2027.html">Asgari Ücret 2027 yazımıza</a> bakın.</p>

<h2 id="etkiler">Asgari ücretin etkilediği diğer tutarlar</h2>
<ul>
<li><b>SGK prim tavanı:</b> Brüt asgari ücretin 9 katı (2026: 297.270 ₺; 2025’te 7,5 kattı).</li>
<li><b>Kıdem tazminatı:</b> Hesaplamada brüt ücret kullanılır; asgari ücretli için 1 yıllık kıdem tazminatı 33.030 ₺’dir. Bkz. <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı hesaplama</a>.</li>
<li><b>İşsizlik maaşı:</b> Üst sınırı brüt asgari ücretin %80’idir.</li>
<li><b>Fazla mesai:</b> Asgari ücretlinin fazla mesai saat ücreti 146,80 × 1,5 = 220,20 ₺ (brüt).</li>
</ul>
''',
faq=[
('2026 asgari ücret net ne kadar?','2026 yılı net asgari ücret 28.075,50 ₺’dir.'),
('2026 brüt asgari ücret ne kadar?','2026 yılı brüt asgari ücret 33.030,00 ₺’dir.'),
('Asgari ücretin işverene maliyeti ne kadar?','Teşviksiz 40.874,63 ₺, 2 puan SGK indirimiyle 40.214,03 ₺, imalat sektöründe 5 puan indirimle 39.223,13 ₺’dir.'),
('Asgari ücretten vergi kesiliyor mu?','Hayır. Asgari ücret gelir vergisi ve damga vergisinden istisnadır; yalnızca %14 SGK ve %1 işsizlik sigortası kesilir.'),
('Asgari ücret yılda kaç kez belirlenir?','Kanuna göre en az iki yılda bir belirlenir; yüksek enflasyon dönemlerinde yılda bir veya iki kez güncellenmiştir.'),
],
related=['net-maas-hesaplama','saatlik-ucret-hesaplama','kidem-tazminati-hesaplama','fazla-mesai-hesaplama','maas-zam-hesaplama','yillik-izin-hesaplama'],
sources=[('KPMG – 2026 Yılı Asgari Ücreti Açıklandı','https://kpmgvergi.com/yayinlar/mali-bultenler/sosyal-guvenlik/2026-yili-asgari-ucreti-aciklandi/3342'),('Çalışma ve Sosyal Güvenlik Bakanlığı','https://www.csgb.gov.tr/')],
))

# ───────────────────────── YILLIK İZİN ─────────────────────────
TOOLS.append(dict(
slug='yillik-izin-hesaplama', name='Yıllık İzin Hesaplama', cat='maas', ico='🏖️',
title='Yıllık İzin Hesaplama – Kaç Gün İzin Hakkım Var? (İş Kanunu) | Hesaplarsın',
desc='İşe giriş tarihinize ve yaşınıza göre İş Kanunu’ndaki yıllık ücretli izin hakkınızı (14, 20, 26 gün) hesaplayın. Kullanılmayan izin ücreti de hesaplanır.',
h1='🏖️ Yıllık İzin Hesaplama',
lead='İşe giriş tarihinizi ve doğum tarihinizi girin; İş Kanunu’na göre kaç gün yıllık ücretli izin hakkınız olduğunu ve işten ayrılırken kullanılmayan izin ücretinizi hesaplayın.',
form='''<div class="form-grid">
<div class="field"><label for="giris">İşe Giriş Tarihi</label><input type="date" id="giris"></div>
<div class="field"><label for="dogum">Doğum Tarihi</label><input type="date" id="dogum"></div>
<div class="field"><label for="hedef">Hesaplama Tarihi <small>(boş = bugün)</small></label><input type="date" id="hedef"></div>
<div class="field"><label for="kullanilan">Kullanılan İzin (gün) <small>toplam</small></label><input type="number" id="kullanilan" placeholder="örn: 20" inputmode="numeric"></div>
<div class="field"><label for="brut">Brüt Aylık Ücret (₺) <small>izin ücreti için</small></label><input type="number" id="brut" placeholder="örn: 45.000" inputmode="decimal"></div>
<div class="field"><label class="chk" style="margin-top:26px"><input type="checkbox" id="yer"> Yer altı işlerinde çalışıyorum (+4 gün)</label></div>
</div>''',
js=r'''
function hak(kidem,yas){var g=kidem<5?14:(kidem<15?20:26); if((yas<18||yas>=50)&&g<20) g=20; return g;}
function yasHesap(d,t){var y=t.getFullYear()-d.getFullYear(); if(t.getMonth()<d.getMonth()||(t.getMonth()===d.getMonth()&&t.getDate()<d.getDate())) y--; return y;}
function hesapla(){
  var g=parseDate('giris'), d=parseDate('dogum'), t=parseDate('hedef')||new Date(); if(!g) return 'İşe giriş tarihinizi seçin.'; if(!d) return 'Doğum tarihinizi seçin.';
  t=new Date(t.getFullYear(),t.getMonth(),t.getDate()); if(g>t) return 'İşe giriş tarihi gelecekte olamaz.';
  var tam=0, x=new Date(g); while(true){x=new Date(g.getFullYear()+tam+1,g.getMonth(),g.getDate()); if(x<=t) tam++; else break;}
  if(tam<1) return {main:['Yıllık izin hakkı','Henüz doğmadı'], sub:'İzne hak kazanmak için deneme süresi dahil en az 1 yıl çalışmak gerekir. İlk izin hakkı: '+dt(new Date(g.getFullYear()+1,g.getMonth(),g.getDate()))};
  var top=0, satir=[], ek=checked('yer')?4:0;
  for(var i=1;i<=tam;i++){var hk=new Date(g.getFullYear()+i,g.getMonth(),g.getDate()), yas=yasHesap(d,hk), gun=hak(i,yas)+ek; top+=gun; if(tam-i<6) satir.push('<tr><td>'+i+'. yıl ('+hk.toLocaleDateString('tr-TR')+')</td><td>'+gun+' gün</td></tr>');}
  var buYil=hak(tam,yasHesap(d,t))+ek, kul=v('kullanilan')||0, kalan=Math.max(0,top-kul), b=v('brut'), rows=[['Kıdem (tam yıl)',tam+' yıl'],['Bu yılki izin hakkı',buYil+' gün'],['Toplam hak edilen izin',top+' gün'],['Kullanılan izin',kul+' gün'],['Kalan izin',kalan+' gün','hl']];
  if(b>0) rows.push(['Kullanılmayan izin ücreti (brüt)',tl(b/30*kalan)]);
  return {main:['Yıllık izin hakkınız', buYil+' gün'], sub:tam+' yıllık kıdeminiz var · Toplam kalan izin: '+kalan+' gün', rows:rows,
    extra:'<table><thead><tr><th>Hak ediş yılı</th><th>İzin</th></tr></thead><tbody>'+satir.join('')+'</tbody></table>',
    note:'Hafta tatili, ulusal bayram ve genel tatil günleri izin süresine dahil edilmez. Toplu sözleşme veya iş sözleşmesiyle daha uzun izin verilebilir.'};
}''',
article='''
<h2 id="kac-gun">Yıllık izin kaç gün?</h2>
<p>4857 sayılı İş Kanunu’nun 53. maddesine göre, işyerinde deneme süresi dahil <b>en az bir yıl</b> çalışmış işçiler yıllık ücretli izne hak kazanır. İzin süresi kıdeme göre belirlenir:</p>
<div class="table-wrap"><table><thead><tr><th>Kıdem</th><th>Yıllık izin süresi</th></tr></thead><tbody>
<tr><td>1 yıldan 5 yıla kadar (5 yıl dahil)</td><td>14 gün</td></tr>
<tr><td>5 yıldan fazla, 15 yıldan az</td><td>20 gün</td></tr>
<tr><td>15 yıl (dahil) ve daha fazla</td><td>26 gün</td></tr>
</tbody></table></div>
<p><b>18 yaşından küçük</b> ve <b>50 yaşından büyük</b> işçilere verilecek yıllık izin süresi <b>20 günden az olamaz</b>. Yer altı işlerinde çalışanların izin süreleri 4’er gün artırılarak uygulanır. Bu süreler asgari sürelerdir; iş veya toplu iş sözleşmeleriyle artırılabilir.</p>

<h2 id="nasil">Yıllık izin hakkı nasıl hesaplanır?</h2>
<p>İzin hakkı, işe giriş tarihinin her yıl dönümünde doğar. Örneğin 15 Mart 2022’de işe başlayan biri ilk izin hakkını 15 Mart 2023’te kazanır. Kıdem yılı ve hak ediş tarihindeki yaş birlikte değerlendirilir.</p>
<div class="example"><p><b>Örnek:</b> 1 Şubat 2019’da işe başlayan, 1975 doğumlu bir çalışan için 2026 yılında:</p><p>Kıdem 7 yıl → 20 gün. 50 yaşından büyük olduğu için en az 20 gün kuralı zaten karşılanıyor. Toplam hak edilen izin: 1–5. yıllar (yaşı 50’nin altındaysa 14’er, üzerindeyse 20’şer) + 6–7. yıllar 20’şer gün.</p></div>

<h2 id="tatil">Hafta sonu ve bayramlar izinden sayılır mı?</h2>
<p>Hayır. İzin süresine rastlayan hafta tatili, ulusal bayram ve genel tatil günleri izin süresinden sayılmaz. Örneğin 14 günlük izin, Cumartesi çalışılmayan bir işyerinde yaklaşık 3 haftalık bir döneme karşılık gelir. İzin dönüş tarihinizi resmi tatilleri düşerek bulmak için <a href="/is-gunu-hesaplama.html">iş günü hesaplama</a> aracını kullanabilirsiniz.</p>

<h2 id="kullanim">Yıllık izin nasıl kullanılır?</h2>
<ul>
<li>İzin, işveren tarafından bölünemez; ancak tarafların anlaşmasıyla bir bölümü 10 günden az olmamak üzere en fazla üçe bölünebilir.</li>
<li>Yıllık izin hakkından vazgeçilemez ve izin yerine ücret ödenemez (iş sözleşmesi sona ermedikçe).</li>
<li>Kullanılmayan izinler bir sonraki yıla devreder ve zamanaşımı iş sözleşmesinin sona ermesinden itibaren başlar.</li>
<li>İşyeri dışında izin geçirecek işçiye talebi halinde gidiş-dönüş için toplam 4 güne kadar ücretsiz yol izni verilir.</li>
</ul>

<h2 id="ucret">Kullanılmayan izin ücreti nasıl hesaplanır?</h2>
<p>İş sözleşmesi herhangi bir nedenle sona erdiğinde, kullanılmamış yıllık izin süreleri son brüt ücret üzerinden ödenir.</p>
<div class="formula">İzin ücreti (brüt) = Son brüt aylık ücret ÷ 30 × Kullanılmayan izin günü</div>
<p>Bu ücret gelir vergisi, damga vergisi ve SGK primlerine tabidir. İşten ayrılırken alacağınız diğer haklar için <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı</a> ve <a href="/ihbar-tazminati-hesaplama.html">ihbar tazminatı</a> hesaplama araçlarına göz atın.</p>
''',
faq=[
('1 yılını dolduran işçi kaç gün izin kullanır?','1–5 yıl arası kıdemi olan işçi yılda en az 14 gün yıllık ücretli izin hakkına sahiptir; 18 yaşından küçük veya 50 yaşından büyükse en az 20 gün.'),
('Deneme süresi izin hesabına dahil mi?','Evet. Bir yıllık çalışma süresinin hesabında deneme süresi de dahil edilir.'),
('Cumartesi yıllık izinden sayılır mı?','Cumartesi çalışılan işyerlerinde Cumartesi iş günü sayıldığı için izinden düşülür. Cumartesi çalışılmayan işyerlerinde ise izin gününden sayılmaz.'),
('Kullanılmayan izinler yanar mı?','Hayır. Kullanılmayan izinler birikir ve iş sözleşmesi sona erdiğinde ücreti ödenmek zorundadır.'),
('Yıllık izin hakkı ne zaman doğar?','İşe giriş tarihinin yıl dönümünde doğar. Kıdeminiz 5 yılı geçtiği yıl dönümünden itibaren izniniz 20 güne çıkar.'),
],
related=['kidem-tazminati-hesaplama','ihbar-tazminati-hesaplama','is-gunu-hesaplama','net-maas-hesaplama','fazla-mesai-hesaplama'],
sources=[('4857 sayılı İş Kanunu m.53–60','https://www.mevzuat.gov.tr/mevzuatmetin/1.5.4857.pdf')],
howto=('Yıllık izin hakkı nasıl hesaplanır?',['İşe giriş tarihinizi girin.','Doğum tarihinizi girin (18 yaş altı ve 50 yaş üstü kuralı için).','Kullandığınız izin gününü ve isterseniz brüt ücretinizi ekleyip Hesapla’ya basın.']),
))

# ───────────────────────── EMEKLİLİK YAŞI ─────────────────────────
TOOLS.append(dict(
slug='emeklilik-yasi-hesaplama', name='Emeklilik Hesaplama', cat='maas', ico='🎖️',
title='Emeklilik Hesaplama 2026 – Ne Zaman Emekli Olurum? SSK, Bağ-Kur, Memur | Hesaplarsın',
desc='SSK, Bağ-Kur ve memurlar için emeklilik yaşınızı, eksik prim gününüzü ve tahmini emeklilik tarihinizi hesaplayın. EYT ve 2008 sonrası kademeli yaş dahil.',
h1='🎖️ Emeklilik Hesaplama – Ne Zaman Emekli Olurum?',
lead='Statünüzü (SSK, Bağ-Kur, memur), ilk sigorta giriş tarihinizi, doğum tarihinizi ve prim gününüzü girin; emeklilik grubunuzu, yaş şartınızı, eksik prim gününüzü ve tahmini emeklilik tarihinizi öğrenin.',
form='''<div class="field full" style="margin-bottom:14px"><label>Sigorta Statüsü</label><div class="seg"><label><input type="radio" name="stat" value="a" checked>SSK (4/a)</label><label><input type="radio" name="stat" value="b">Bağ-Kur (4/b)</label><label><input type="radio" name="stat" value="c">Memur (4/c)</label></div></div>
<div class="form-grid">
<div class="field"><label>Cinsiyet</label><div class="seg"><label><input type="radio" name="cins" value="k" checked>Kadın</label><label><input type="radio" name="cins" value="e">Erkek</label></div></div>
<div class="field"><label for="dogum">Doğum Tarihi</label><input type="date" id="dogum"></div>
<div class="field"><label for="giris">İlk Sigorta Giriş Tarihi</label><input type="date" id="giris"></div>
<div class="field"><label for="prim">Mevcut Prim Gün Sayısı <small>isteğe bağlı</small></label><input type="number" id="prim" placeholder="e-Devlet hizmet dökümünden" inputmode="numeric"></div>
</div>''',
js=r'''
function addY(d,y){return new Date(d.getFullYear()+y,d.getMonth(),d.getDate());}
function kademeYas(yil,k){ // 5510 m.28 – 01.05.2008 sonrası
  var t=[[2035,58,60],[2037,59,61],[2039,60,62],[2041,61,63],[2043,62,64],[2045,63,65],[2047,64,65]];
  for(var i=0;i<t.length;i++){if(yil<=t[i][0]) return k?t[i][1]:t[i][2];} return 65;}
function eytPrim(giris,k){ // 23.05.2002 itibarıyla sigortalılık süresine göre (4759 sayılı Kanun kademesi)
  var ref=new Date(2002,4,23), yil=(ref-giris)/(365.25*864e5);
  if(k){ if(yil>=17) return 5000; var s=Math.max(4,Math.floor(yil)); return Math.min(5975,5000+(17-s)*75); }
  if(yil>=21.5) return 5000; return Math.min(5975,5000+Math.ceil((21.5-yil)/1.5)*75);
}
function fmt(d){return d.toLocaleDateString('tr-TR');}
function hesapla(){
  var st=radio('stat')||'a', k=radio('cins')==='k', d=parseDate('dogum'), g=parseDate('giris'), p=v('prim');
  if(!d||!g) return 'Doğum tarihinizi ve ilk sigorta giriş tarihinizi seçin.'; if(g<=d) return 'Giriş tarihi doğum tarihinden sonra olmalı.';
  var stAd={a:'SSK (4/a)',b:'Bağ-Kur (4/b)',c:'Memur (4/c)'}[st];
  var grup, yas=null, primGerek, sure=null, rows=[], not='', yasTarih=null, sureTarih=null;
  if(g<=new Date(1999,8,8)){
    grup='EYT – 08.09.1999 ve öncesi girişli';
    if(st==='a'){ primGerek=eytPrim(g,k); sure=k?20:25; not='EYT grubunda SSK prim günü, 23.05.2002 tarihindeki sigortalılık sürenize göre 5000–5975 gün arasında kademelidir. '; }
    else { primGerek=k?7200:9000; sure=k?20:25; not=(st==='b'?'Bağ-Kur’da EYT kapsamındakiler için genel kural kadın 20 yıl (7200 gün), erkek 25 yıl (9000 gün) prim ödemesidir; geçiş hükümleri nedeniyle bazı kişilerde daha düşük olabilir. ':'Memurlarda EYT kapsamında kadın 20, erkek 25 yıl fiili hizmet aranır. '); }
    sureTarih=addY(g,sure);
    rows.push(['Yaş şartı','Yok (EYT düzenlemesi)']); rows.push([(st==='c'?'Hizmet süresi':'Sigortalılık süresi')+' şartı',sure+' yıl → '+fmt(sureTarih)]); rows.push(['Gereken prim günü'+(st==='a'?' (tahmini)':''),num(primGerek,0)+' gün']);
  } else if(g<new Date(2008,4,1)){
    grup='09.09.1999 – 30.04.2008 arası girişli'; yas=k?58:60; primGerek=st==='a'?7000:9000; yasTarih=addY(d,yas);
    rows.push(['Yaş şartı',yas+' yaş → '+fmt(yasTarih)]); rows.push(['Gereken prim günü',num(primGerek,0)+' gün'+(st==='c'?' (25 yıl hizmet)':'')]);
    if(st==='a') rows.push(['Alternatif','25 yıl sigortalılık + 4500 gün + aynı yaş şartı']);
  } else {
    grup='01.05.2008 ve sonrası girişli (5510 sayılı Kanun)'; primGerek=st==='a'?7200:9000;
    for(var y=d.getFullYear()+40;y<=d.getFullYear()+70;y++){var gy=kademeYas(y,k); if(y-d.getFullYear()>=gy){yas=gy;break;}}
    yasTarih=addY(d,yas);
    rows.push(['Yaş şartı (kademeli)',yas+' yaş → '+fmt(yasTarih)]); rows.push(['Gereken prim günü',num(primGerek,0)+' gün']);
    if(st==='b') not='Bağ-Kur için 9000 günün 7200’e indirilmesi gündemde olsa da Ekim 2026 itibarıyla yasalaşmamıştır; yasalaşırsa hesap güncellenecektir. ';
  }
  var primTarih=null;
  if(p>=0&&!isNaN(p)&&raw('prim')!==''){var eksik=Math.max(0,primGerek-p); rows.push(['Mevcut prim günü',num(p,0)+' gün']); rows.push(['Eksik prim günü',num(eksik,0)+' gün','hl']);
    primTarih=eksik>0?new Date(Date.now()+eksik/360*365.25*864e5):new Date(); if(eksik>0) rows.push(['Kesintisiz çalışırsanız prim tamamlanması',fmt(primTarih)]);}
  var tarihler=[yasTarih,sureTarih,primTarih].filter(function(x){return x;}), son=null;
  tarihler.forEach(function(x){if(!son||x>son)son=x;});
  var main, sub;
  if(son&&primTarih&&son<=new Date(Date.now()+864e5)){ main=['Emeklilik şartlarınız tamam görünüyor','Başvurabilirsiniz']; sub=stAd+' · '+grup+' · SGK’ya başvurmadan önce hizmet dökümünüzü kontrol edin'; rows.unshift(['Emeklilik grubunuz',grup]); }
  else if(son&&primTarih){ main=['Tahmini emeklilik tarihiniz', fmt(son)]; var yasO=son.getFullYear()-d.getFullYear()-((son.getMonth()<d.getMonth()||(son.getMonth()===d.getMonth()&&son.getDate()<d.getDate()))?1:0); sub=stAd+' · '+grup+' · o tarihte '+yasO+' yaşında olacaksınız'; rows.unshift(['Emeklilik grubunuz',grup]); }
  else { main=['Emeklilik grubunuz', grup]; sub=stAd+' · '+(yas?'emeklilik yaşınız: <b>'+yas+'</b>':'yaş şartı yok; süre ve prim şartı aranır')+' · tarih için prim gününüzü girin'; }
  return {main:main, sub:sub, rows:rows, note:not+'Sonuç genel kurallara göre hesaplanmıştır. Borçlanma, yıpranma payı, engellilik ve birden fazla statüde çalışma gibi durumlarda kurallar farklıdır; kesin sonucu e-Devlet “SGK Emeklilik Hesaplama” hizmetinden doğrulayın. Prim tamamlanma tarihi, yılda 360 gün kesintisiz prim varsayımıyla hesaplanır.'};
}''',
article='''
<h2 id="nasil">Emeklilik yaşı neye göre belirlenir?</h2>
<p>Türkiye’de SSK’lı (4/a) çalışanların emeklilik şartları, <b>ilk kez sigortalı olunan tarihe</b> göre üç ana gruba ayrılır. Her grup için yaş, sigortalılık süresi ve prim gün sayısı farklıdır. Emekli olabilmek için grubunuza ait tüm şartları birlikte tamamlamanız gerekir.</p>

<h2 id="gruplar">SSK (4/a) emeklilik şartları tablosu</h2>
<div class="table-wrap"><table><thead><tr><th>İlk sigorta girişi</th><th>Kadın</th><th>Erkek</th><th>Prim günü</th></tr></thead><tbody>
<tr><td>08.09.1999 ve öncesi (EYT)</td><td>Yaş şartı yok, 20 yıl sigortalılık</td><td>Yaş şartı yok, 25 yıl sigortalılık</td><td>5000 – 5975 gün</td></tr>
<tr><td>09.09.1999 – 30.04.2008</td><td>58 yaş</td><td>60 yaş</td><td>7000 gün (veya 25 yıl + 4500 gün + yaş)</td></tr>
<tr><td>01.05.2008 ve sonrası</td><td>58 yaş → kademeli 65</td><td>60 yaş → kademeli 65</td><td>7200 gün</td></tr>
</tbody></table></div>

<h2 id="statu">Bağ-Kur ve memurlar için emeklilik şartları</h2>
<div class="table-wrap"><table><thead><tr><th>İlk giriş</th><th>Bağ-Kur (4/b)</th><th>Memur (4/c)</th></tr></thead><tbody>
<tr><td>08.09.1999 ve öncesi (EYT)</td><td>Yaş şartı yok; kadın 20 yıl (7200 gün), erkek 25 yıl (9000 gün) prim</td><td>Yaş şartı yok; kadın 20, erkek 25 yıl hizmet</td></tr>
<tr><td>09.09.1999 – 30.04.2008</td><td>Kadın 58, erkek 60 yaş + 9000 gün</td><td>Kadın 58, erkek 60 yaş + 25 yıl (9000 gün) hizmet</td></tr>
<tr><td>01.05.2008 ve sonrası</td><td>58/60 yaş (2036’dan itibaren kademeli 65) + 9000 gün</td><td>58/60 yaş (kademeli 65) + 9000 gün</td></tr>
</tbody></table></div>
<p>Bağ-Kur’lular için 9000 günün SSK ile eşitlenip 7200 güne indirilmesi uzun süredir gündemde olsa da Ekim 2026 itibarıyla bu düzenleme yasalaşmamıştır. Yasalaşması hâlinde hesaplayıcı güncellenecektir.</p>

<h2 id="tarih">Emeklilik tarihim nasıl bulunur?</h2>
<p>Emekli olabilmek için grubunuzdaki şartların <b>hepsini</b> tamamlamanız gerekir: yaş, prim günü ve (EYT’de) sigortalılık süresi. Bu yüzden emeklilik tarihiniz, bu şartlardan <b>en son tamamlanacak olanın</b> tarihidir. Örneğin 2005’te işe başlamış, 1985 doğumlu bir erkek 60 yaşını 2045’te doldurur; 7000 prim gününü 2030’da tamamlasa bile 2045’i bekler. Hesaplayıcıya mevcut prim gününüzü girerseniz, kesintisiz çalışma varsayımıyla prim tamamlanma tarihini de hesaplar ve üç tarihten en geç olanı tahmini emeklilik tarihiniz olarak gösterir.</p>

<h2 id="eyt">EYT kapsamındakiler ne zaman emekli olur?</h2>
<p>Mart 2023’te yürürlüğe giren düzenlemeyle 8 Eylül 1999 ve öncesinde sigortalı olanlar için yaş şartı kaldırılmıştır. Bu gruptakiler, kadınlarda 20, erkeklerde 25 yıllık sigortalılık süresini ve işe giriş tarihlerine göre 5000 ile 5975 gün arasında değişen prim gün sayısını tamamladıklarında emekli olabilir. Prim gün sayısı, 23 Mayıs 2002 tarihindeki sigortalılık sürenize göre kademeli olarak belirlenir: sigortalılık süreniz uzadıkça gereken prim günü azalır.</p>

<h2 id="kademe">01.05.2008 sonrası girişliler için kademeli emeklilik yaşı</h2>
<div class="table-wrap"><table><thead><tr><th>Şartların tamamlandığı yıl</th><th>Kadın</th><th>Erkek</th></tr></thead><tbody>
<tr><td>2035 ve öncesi</td><td>58</td><td>60</td></tr><tr><td>2036 – 2037</td><td>59</td><td>61</td></tr><tr><td>2038 – 2039</td><td>60</td><td>62</td></tr>
<tr><td>2040 – 2041</td><td>61</td><td>63</td></tr><tr><td>2042 – 2043</td><td>62</td><td>64</td></tr><tr><td>2044 – 2045</td><td>63</td><td>65</td></tr>
<tr><td>2046 – 2047</td><td>64</td><td>65</td></tr><tr><td>2048 ve sonrası</td><td>65</td><td>65</td></tr>
</tbody></table></div>
<p>Örneğin 1990 doğumlu ve 2010’da işe başlamış bir kadın 58 yaşını 2048’de dolduracağından, bu yıl için geçerli yaş 65 olur; yani 2055’te emekli olabilir.</p>

<h2 id="prim">Prim gün sayımı nasıl öğrenirim?</h2>
<p>e-Devlet’te “SGK Tescil ve Hizmet Dökümü” ile toplam prim gününüzü ve ilk giriş tarihinizi görebilirsiniz. Askerlik, doğum ve yurt dışı borçlanmaları prim gününüzü artırabilir; doğum borçlanması ilk giriş tarihinizi değiştirmez, ancak askerlik borçlanması belirli şartlarla emeklilik şartlarını etkileyebilir. Kesin değerlendirme için SGK’nın “Ne Zaman Emekli Olabilirim?” servisini kullanın.</p>

<h2 id="diger">Bağ-Kur ve memurlar için farklılıklar</h2>
<p>Bağ-Kur’lular (4/b) ve memurlar (4/c) için prim gün sayıları ve geçiş hükümleri SSK’dan farklıdır. Hizmetiniz birden fazla statüde geçtiyse son 7 yıllık (2520 gün) çalışmanızda fazla prim ödediğiniz statüye göre emekli olursunuz. Bu hesaplayıcı yalnızca 4/a (SSK) kurallarını esas alır. Emeklilik planlamanıza yardımcı olması için <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı</a> ve <a href="/yas-hesaplama.html">yaş hesaplama</a> araçlarını da kullanabilirsiniz.</p>
''',
faq=[
('Ne zaman emekli olurum nasıl hesaplanır?','İlk sigorta giriş tarihiniz hangi gruba girdiğinizi belirler. Grubunuzun yaş, prim günü ve (EYT’de) sigortalılık süresi şartlarından en son tamamlanacak olanın tarihi emeklilik tarihinizdir. Yukarıdaki hesaplayıcıya statünüzü, doğum ve giriş tarihinizi ve prim gününüzü girerek tahmini tarihi görebilirsiniz.'),
('Bağ-Kur’lular kaç günle emekli olur?','1999 sonrası girişli Bağ-Kur’lular için prim şartı 9000 gündür (kadın 58, erkek 60 yaş; 2008 sonrası girişlilerde yaş kademeli artar). EYT kapsamındaki kadınlarda 7200, erkeklerde 9000 gündür. 7200 gün eşitlemesi Ekim 2026 itibarıyla yasalaşmamıştır.'),
('Memurlar kaç yılda emekli olur?','1999 öncesi girişli memurlar kadınsa 20, erkekse 25 yıl hizmetle yaş şartı olmadan emekli olur. 1999 sonrası girişlilerde 25 yıl (9000 gün) hizmetle birlikte kadın 58, erkek 60 yaş şartı aranır.'),
('EYT’liler kaç yaşında emekli olur?','08.09.1999 ve öncesi girişlilerde yaş şartı yoktur. Sigortalılık süresini (kadın 20, erkek 25 yıl) ve prim gün sayısını tamamladıklarında emekli olabilirler.'),
('2000 yılında işe giren kaç yaşında emekli olur?','09.09.1999 – 30.04.2008 arasında girişi olanlar kadınsa 58, erkekse 60 yaşında ve 7000 prim günüyle emekli olur.'),
('2008 sonrası girişliler kaç yaşında emekli olur?','Şartlarını 2035’e kadar tamamlayanlar kadın 58, erkek 60 yaşında emekli olur. 2036’dan itibaren yaş kademeli olarak 65’e yükselir. Prim şartı 7200 gündür.'),
('Prim günüm dolduysa yaşımı bekler miyim?','Evet. EYT kapsamı dışındaki gruplarda prim gün sayısını doldursanız bile yaş şartını beklemeniz gerekir.'),
('Askerlik borçlanması emekliliği öne çeker mi?','Prim gününüzü artırır. İşe girişten önceki askerlik süresinin borçlanılması, belirli durumlarda sigorta başlangıcını geriye çekebilir; SGK’dan teyit alınmalıdır.'),
],
related=['memur-emekli-zammi-hesaplama','kidem-tazminati-hesaplama','yas-hesaplama','net-maas-hesaplama','asgari-ucret-hesaplama'],
sources=[('5510 sayılı Sosyal Sigortalar ve GSS Kanunu','https://www.mevzuat.gov.tr/mevzuatmetin/1.5.5510.pdf'),('SGK – e-Devlet Emeklilik Hesaplama','https://www.turkiye.gov.tr/')],
))

# ───────────────────────── ENFLASYON ─────────────────────────
TUFE_JS = r'''var TUFE={2010:6.40,2011:10.45,2012:6.16,2013:7.40,2014:8.17,2015:8.81,2016:8.53,2017:11.92,2018:20.30,2019:11.84,2020:14.60,2021:36.08,2022:64.27,2023:64.77,2024:44.38,2025:30.89};'''
TOOLS.append(dict(
slug='enflasyon-hesaplama', name='Enflasyon Hesaplama', cat='finans', ico='📊',
title='Enflasyon Hesaplama – Yıllara Göre Paranın Bugünkü Değeri (TÜFE) | Hesaplarsın',
desc='2010’dan bugüne TÜİK yıllık TÜFE oranlarıyla geçmişteki paranın bugünkü karşılığını, iki yıl arasındaki kümülatif enflasyonu ve gelecekteki fiyatı hesaplayın.',
h1='📊 Enflasyon Hesaplama (TÜFE)',
lead='“2015’teki 1.000 lira bugün kaç lira eder?” TÜİK yıllık enflasyon verileriyle iki yıl arasındaki toplam enflasyonu, alım gücü kaybını ve gelecekteki fiyatları hesaplayın.',
form='''<div class="field full" style="margin-bottom:14px"><label>Hesaplama Türü</label>
<div class="seg"><label><input type="radio" name="mod" value="yil" checked onchange="modSec()">Yıllar arası (TÜİK)</label><label><input type="radio" name="mod" value="gelecek" onchange="modSec()">Gelecekteki fiyat</label><label><input type="radio" name="mod" value="fiyat" onchange="modSec()">İki fiyat arası oran</label></div></div>
<div class="form-grid">
<div class="field" id="f-tutar"><label for="tutar" id="lbl-tutar">Tutar (₺)</label><input type="number" id="tutar" placeholder="örn: 1.000" inputmode="decimal"></div>
<div class="field" id="f-y1"><label for="y1">Başlangıç Yılı (yıl sonu)</label><select id="y1"></select></div>
<div class="field" id="f-y2"><label for="y2">Bitiş Yılı (yıl sonu)</label><select id="y2"></select></div>
<div class="field" id="f-oran" style="display:none"><label for="oran">Yıllık Enflasyon Beklentisi (%)</label><input type="number" id="oran" placeholder="örn: 25" inputmode="decimal"></div>
<div class="field" id="f-yil" style="display:none"><label for="yil">Süre (yıl)</label><input type="number" id="yil" placeholder="örn: 5" inputmode="decimal"></div>
<div class="field" id="f-yeni" style="display:none"><label for="yeni">Yeni Fiyat (₺)</label><input type="number" id="yeni" placeholder="örn: 2.500" inputmode="decimal"></div>
</div>''',
js=TUFE_JS + r'''
function onReady(){var o='';for(var y=2009;y<=2025;y++)o+='<option value="'+y+'">'+y+'</option>';el('y1').innerHTML=o;el('y2').innerHTML=o;el('y1').value='2015';el('y2').value='2025';}
function modSec(){var m=radio('mod');el('f-y1').style.display=el('f-y2').style.display=m==='yil'?'':'none';el('f-oran').style.display=el('f-yil').style.display=m==='gelecek'?'':'none';
  el('f-yeni').style.display=m==='fiyat'?'':'none';el('lbl-tutar').textContent=m==='fiyat'?'Eski Fiyat (₺)':'Tutar (₺)';el('result').style.display='none';_last=null;}
function hesapla(){
  var m=radio('mod'), t=v('tutar'); if(!(t>0)) return 'Tutarı girin.';
  if(m==='yil'){
    var a=+el('y1').value, b=+el('y2').value; if(b<=a) return 'Bitiş yılı başlangıç yılından sonra olmalı.';
    var c=1, tab=[]; for(var y=a+1;y<=b;y++){c*=1+TUFE[y]/100; tab.push('<tr><td>'+y+'</td><td>%'+num(TUFE[y],2)+'</td><td>'+tl(t*c,0)+'</td></tr>');}
    var yillik=(Math.pow(c,1/(b-a))-1)*100;
    return {main:[a+' sonundaki '+tl(t,0)+' → '+b+' sonunda', tl(t*c)], sub:'Toplam (kümülatif) enflasyon: '+pct((c-1)*100,1),
      rows:[['Fiyatlar kaç kat arttı?',num(c,2)+' kat'],['Yıllık ortalama enflasyon',pct(yillik)],['Paranın alım gücü kaybı',pct((1-1/c)*100,1),'neg'],[b+' sonundaki '+tl(t,0)+'’nin '+a+' değeri',tl(t/c)]],
      extra:'<table><thead><tr><th>Yıl</th><th>Yıllık TÜFE</th><th>Tutarın karşılığı</th></tr></thead><tbody>'+tab.join('')+'</tbody></table>',
      note:'TÜİK Aralık ayı yıllık TÜFE değerleri kullanılmıştır. Eylül 2026 itibarıyla yıllık TÜFE %29,73’tür.'};
  }
  if(m==='gelecek'){
    var r=v('oran'), n=v('yil'); if(!(r>-100)||!(n>0)) return 'Enflasyon oranını ve süreyi girin.'; var c=Math.pow(1+r/100,n);
    return {main:[num(n,n%1?1:0)+' yıl sonraki karşılığı', tl(t*c)], sub:'Yıllık %'+num(r,2)+' enflasyonla', rows:[['Toplam fiyat artışı',pct((c-1)*100,1)],['Bugünkü '+tl(t,0)+'’nin o zamanki alım gücü',tl(t/c)],['Fiyatların ikiye katlanma süresi',num(Math.log(2)/Math.log(1+r/100),1)+' yıl']]};
  }
  var y=v('yeni'); if(!(y>0)) return 'Yeni fiyatı girin.';
  return {main:['Fiyat değişimi', pct((y/t-1)*100)], rows:[['Eski fiyat',tl(t)],['Yeni fiyat',tl(y)],['Fark',tl(y-t)],['Kat',num(y/t,2)+'x']]};
}''',
article='''
<h2 id="nedir">Enflasyon nedir, nasıl ölçülür?</h2>
<p>Enflasyon, mal ve hizmet fiyatlarının genel düzeyinin sürekli artmasıdır. Türkiye’de resmi enflasyon, TÜİK tarafından her ayın 3’ünde açıklanan <b>Tüketici Fiyat Endeksi (TÜFE)</b> ile ölçülür. TÜFE, hanelerin satın aldığı yüzlerce ürün ve hizmetten oluşan bir sepetin fiyatındaki değişimi gösterir. Enflasyon arttıkça aynı miktar parayla daha az ürün alınabilir; buna <b>alım gücü kaybı</b> denir.</p>

<h2 id="nasil">Yıllara göre enflasyon nasıl hesaplanır?</h2>
<p>İki yıl arasındaki toplam (kümülatif) enflasyon, aradaki yılların enflasyon oranları toplanarak değil, <b>çarpılarak</b> bulunur. Çünkü her yılın fiyat artışı bir önceki yılın artmış fiyatları üzerine eklenir.</p>
<div class="formula">Kümülatif artış = (1 + e₁) × (1 + e₂) × … × (1 + eₙ) − 1<br>Bugünkü karşılık = Geçmiş tutar × (1 + e₁) × … × (1 + eₙ)</div>
<div class="example"><p><b>Örnek:</b> 2023 sonundaki 1.000 ₺, 2024 (%44,38) ve 2025 (%30,89) enflasyonu sonrasında:</p><p>1.000 × 1,4438 × 1,3089 = <b>1.889,79 ₺</b>. Toplam enflasyon %89, yani iki yılda alım gücü yaklaşık %47 azalmıştır.</p></div>

<h2 id="tablo">Türkiye yıllık enflasyon oranları (TÜİK, Aralık)</h2>
<div class="table-wrap"><table><thead><tr><th>Yıl</th><th>Yıllık TÜFE</th><th>Yıl</th><th>Yıllık TÜFE</th></tr></thead><tbody>
<tr><td>2010</td><td>%6,40</td><td>2018</td><td>%20,30</td></tr><tr><td>2011</td><td>%10,45</td><td>2019</td><td>%11,84</td></tr>
<tr><td>2012</td><td>%6,16</td><td>2020</td><td>%14,60</td></tr><tr><td>2013</td><td>%7,40</td><td>2021</td><td>%36,08</td></tr>
<tr><td>2014</td><td>%8,17</td><td>2022</td><td>%64,27</td></tr><tr><td>2015</td><td>%8,81</td><td>2023</td><td>%64,77</td></tr>
<tr><td>2016</td><td>%8,53</td><td>2024</td><td>%44,38</td></tr><tr><td>2017</td><td>%11,92</td><td>2025</td><td>%30,89</td></tr>
</tbody></table></div>
<p>2026 yılında yıllık enflasyon Eylül ayı itibarıyla %29,73 olarak açıklanmıştır.</p>

<h2 id="reel">Reel getiri ve enflasyon</h2>
<p>Yatırımınızın gerçekten kazandırıp kazandırmadığını anlamak için getirisini enflasyonla karşılaştırmanız gerekir. %40 faiz getirisi, %30 enflasyon ortamında yaklaşık %7,7 reel getiriye karşılık gelir: 1,40 ÷ 1,30 − 1. Maaş artışınızın enflasyonun üzerinde olup olmadığını <a href="/maas-zam-hesaplama.html">maaş zam hesaplama</a>, birikiminizin getirisini <a href="/mevduat-faizi-hesaplama.html">mevduat faizi hesaplama</a> ile kontrol edebilirsiniz.</p>

<h2 id="kira">Enflasyon kira artışını nasıl etkiler?</h2>
<p>Konut ve işyeri kira artışları, yıllık değil <b>12 aylık ortalama TÜFE</b> ile sınırlandırılır. Güncel yasal oranı <a href="/kira-artis-hesaplama.html">kira artış hesaplama</a> sayfasında bulabilirsiniz. Paranızın gelecekte ne kadar değer kaybedeceğini senaryolarla görmek için <a href="/para-deger-kaybi-hesaplama.html">para değer kaybı hesaplama</a> aracını da kullanabilirsiniz.</p>
''',
faq=[
('2015’teki 100 TL bugün kaç TL eder?','TÜİK yıllık TÜFE verilerine göre 2015 sonundan 2025 sonuna kadar fiyatlar yaklaşık 13 kat artmıştır; 2015 sonundaki 100 ₺, 2025 sonunda yaklaşık 1.304 ₺’ye karşılık gelir. Kesin değeri hesaplayıcıda yılları seçerek görebilirsiniz.'),
('Kümülatif enflasyon neden yıllık oranların toplamı değil?','Her yılın fiyat artışı önceki yılın artmış fiyatlarına uygulandığı için oranlar bileşik olarak çarpılır. İki yıl %50 enflasyon toplam %100 değil %125 artış demektir.'),
('Enflasyon oranı ne zaman açıklanır?','TÜİK her ayın 3’ünde saat 10.00’da bir önceki ayın enflasyon verilerini açıklar.'),
('Yıllık enflasyon ile 12 aylık ortalama enflasyon farkı nedir?','Yıllık enflasyon bir ayın geçen yılın aynı ayına göre değişimidir. 12 aylık ortalama ise son 12 ayın endeks ortalamasının bir önceki 12 aya göre değişimidir ve kira artışlarında kullanılır.'),
],
related=['ekonomi-takvimi','para-deger-kaybi-hesaplama','maas-zam-hesaplama','kira-artis-hesaplama','mevduat-faizi-hesaplama','bilesik-faiz','roi-hesaplama'],
sources=[('TÜİK – Tüketici Fiyat Endeksi','https://data.tuik.gov.tr/'),('TCMB – Enflasyon Verileri','https://www.tcmb.gov.tr/')],
))

# ───────────────────────── FATURALAR ─────────────────────────
TOOLS.append(dict(
slug='elektrik-faturasi-hesaplama', name='Elektrik Faturası Hesaplama', cat='diger', ico='⚡',
title='Elektrik Faturası Hesaplama – kWh Tüketim ve Cihaz Bazlı | Hesaplarsın',
desc='Elektrik faturanızı kWh tüketimi ve birim fiyatla hesaplayın veya buzdolabı, klima, çamaşır makinesi gibi cihazlarınızın aylık elektrik maliyetini bulun.',
h1='⚡ Elektrik Faturası Hesaplama',
lead='Aylık kWh tüketiminizi ve birim fiyatı girerek faturanızı tahmin edin ya da bir cihazın gücü ve kullanım süresinden aylık kaç TL elektrik harcadığını hesaplayın.',
form='''<div class="field full" style="margin-bottom:14px"><label>Hesaplama Türü</label>
<div class="seg"><label><input type="radio" name="mod" value="fatura" checked onchange="modSec()">Fatura (kWh)</label><label><input type="radio" name="mod" value="cihaz" onchange="modSec()">Cihaz tüketimi</label></div></div>
<div class="form-grid">
<div class="field" id="f-kwh"><label for="kwh">Aylık Tüketim (kWh)</label><input type="number" id="kwh" placeholder="örn: 230" inputmode="decimal"></div>
<div class="field" id="f-watt" style="display:none"><label for="watt">Cihaz Gücü (Watt)</label><input type="number" id="watt" placeholder="örn: 1500" inputmode="decimal">
<div class="qtags"><span class="qtag" onclick="el('watt').value=150">Buzdolabı ~150W</span><span class="qtag" onclick="el('watt').value=1200">Klima ~1200W</span><span class="qtag" onclick="el('watt').value=2000">Fırın ~2000W</span><span class="qtag" onclick="el('watt').value=100">TV ~100W</span></div></div>
<div class="field" id="f-saat" style="display:none"><label for="saat">Günlük Kullanım (saat)</label><input type="number" id="saat" placeholder="örn: 6" inputmode="decimal"></div>
<div class="field"><label for="birim">Birim Fiyat (₺/kWh, vergiler dahil)</label><input type="number" id="birim" placeholder="faturanızdan, örn: 3,20" inputmode="decimal"></div>
</div>''',
js=r'''
function modSec(){var c=radio('mod')==='cihaz';el('f-kwh').style.display=c?'none':'';el('f-watt').style.display=el('f-saat').style.display=c?'':'none';el('result').style.display='none';_last=null;}
function hesapla(){
  var b=v('birim'); if(!(b>0)) return 'Birim fiyatı (₺/kWh) girin; faturanızda “toplam tutar ÷ tüketim” ile bulabilirsiniz.';
  if(radio('mod')==='cihaz'){var w=v('watt'), s=v('saat'); if(!(w>0)||!(s>0)) return 'Cihaz gücünü ve günlük kullanım süresini girin.';
    var gk=w*s/1000; return {main:['Aylık elektrik maliyeti', tl(gk*30*b)], sub:num(gk*30,1)+' kWh / ay', rows:[['Günlük tüketim',num(gk,2)+' kWh'],['Günlük maliyet',tl(gk*b)],['Yıllık tüketim',num(gk*365,0)+' kWh'],['Yıllık maliyet',tl(gk*365*b),'hl']],
      note:'Buzdolabı ve klima gibi termostatlı cihazlar sürekli tam güçte çalışmaz; gerçek tüketim etiket gücünün %30–60’ı olabilir.'};}
  var k=v('kwh'); if(!(k>0)) return 'Aylık tüketimi girin.';
  return {main:['Tahmini fatura', tl(k*b)], rows:[['Tüketim',num(k,0)+' kWh'],['Birim fiyat',tl(b,4)+' / kWh'],['Günlük ortalama',tl(k*b/30)],['Yıllık tahmini',tl(k*b*12)]]};
}''',
article='''
<h2 id="nasil">Elektrik faturası nasıl hesaplanır?</h2>
<p>Elektrik faturası temel olarak tüketilen enerji miktarı (kWh) ile birim fiyatın çarpılmasıyla oluşur. Türkiye’de mesken abonelerinin birim fiyatı; enerji bedeli, dağıtım bedeli, enerji fonu, TRT payı, belediye tüketim vergisi (BTV) ve KDV kalemlerinden oluşur. Tarifeler EPDK tarafından belirlenir ve dönemsel olarak güncellenir.</p>
<div class="formula">Fatura (₺) = Tüketim (kWh) × Vergiler dahil birim fiyat (₺/kWh)</div>
<p>Kendi birim fiyatınızı bulmanın en kolay yolu son faturanızdaki <b>toplam tutarı tüketilen kWh’e bölmektir</b>. Bu değeri hesaplayıcıya girerek gelecek ayların faturasını tahmin edebilirsiniz.</p>

<h2 id="cihaz">Bir cihaz ne kadar elektrik harcar?</h2>
<div class="formula">Günlük tüketim (kWh) = Güç (W) × Kullanım süresi (saat) ÷ 1000</div>
<div class="example"><p><b>Örnek:</b> 1.200 W’lık klima günde 6 saat çalışırsa: 1.200 × 6 ÷ 1000 = 7,2 kWh/gün → ayda 216 kWh. Birim fiyat 3,20 ₺ ise aylık maliyet ≈ <b>691 ₺</b>.</p></div>
<div class="table-wrap"><table><thead><tr><th>Cihaz</th><th>Tipik güç</th><th>Aylık tüketim (yaklaşık)</th></tr></thead><tbody>
<tr><td>Buzdolabı (A++)</td><td>100–200 W</td><td>25–40 kWh</td></tr><tr><td>Çamaşır makinesi</td><td>2.000 W</td><td>Yıkama başı ~1 kWh</td></tr>
<tr><td>Bulaşık makinesi</td><td>1.800 W</td><td>Yıkama başı ~1–1,5 kWh</td></tr><tr><td>Klima (12.000 BTU, inverter)</td><td>900–1.300 W</td><td>Kullanıma göre 100–300 kWh</td></tr>
<tr><td>Elektrikli fırın</td><td>2.000–2.500 W</td><td>Saatlik ~1,5–2 kWh</td></tr><tr><td>LED TV</td><td>60–120 W</td><td>10–20 kWh</td></tr><tr><td>Elektrikli su ısıtıcı</td><td>2.200 W</td><td>Günde birkaç dk → 5–10 kWh</td></tr>
</tbody></table></div>

<h2 id="tasarruf">Elektrik faturasını düşürmenin yolları</h2>
<ul>
<li>Enerji sınıfı yüksek (A ve üzeri) cihazlar tercih edin; eski buzdolapları tek başına tüketimin önemli kısmını oluşturabilir.</li>
<li>Klimayı 24–26°C’de kullanın; her 1 derece daha soğuk ayar tüketimi yaklaşık %6–8 artırır.</li>
<li>Çamaşır ve bulaşık makinelerini tam dolu ve eko programda çalıştırın.</li>
<li>Bekleme (stand-by) modundaki cihazları prizden çekin; LED aydınlatmaya geçin.</li>
<li>Çok zamanlı tarifeye geçerek yoğun tüketimi gece saatlerine kaydırabilirsiniz.</li>
</ul>
<p>Faturanızın neden yüksek geldiğini ayrıntılı incelemek için <a href="/blog/elektrik-faturasi-neden-yuksek.html">elektrik faturası neden yüksek</a> rehberimizi okuyabilirsiniz. Diğer giderleriniz için <a href="/dogalgaz-faturasi-hesaplama.html">doğal gaz</a> ve <a href="/su-faturasi-hesaplama.html">su faturası</a> hesaplama araçlarını kullanın.</p>
''',
faq=[
('1 kWh elektrik kaç TL?','Mesken birim fiyatı EPDK tarifesine ve vergilere göre değişir. Faturanızdaki toplam tutarı tüketime bölerek vergiler dahil birim fiyatınızı bulabilirsiniz.'),
('Klima ayda kaç TL elektrik yakar?','1.200 W’lık bir klima günde 6 saat çalışırsa ayda yaklaşık 216 kWh harcar. Bunu birim fiyatınızla çarparak aylık maliyeti bulabilirsiniz.'),
('Elektrik faturasında hangi vergiler var?','Enerji ve dağıtım bedellerine ek olarak belediye tüketim vergisi (%5), enerji fonu, TRT payı ve %20 KDV bulunur (bazı kalemler tarifeye dahil edilmiştir).'),
('Buzdolabı ne kadar elektrik harcar?','Yeni nesil A sınıfı bir buzdolabı ayda 25–40 kWh tüketir. 15 yaşından eski modeller bunun iki katını harcayabilir.'),
],
related=['dogalgaz-faturasi-hesaplama','su-faturasi-hesaplama','yakit-maliyeti-hesaplama','yuzde-hesaplama','kdv-hesaplama'],
))

TOOLS.append(dict(
slug='dogalgaz-faturasi-hesaplama', name='Doğal Gaz Faturası Hesaplama', cat='diger', ico='🔥',
title='Doğal Gaz Faturası Hesaplama – m³’ten kWh ve TL’ye | Hesaplarsın',
desc='Doğal gaz tüketiminizi (m³) kWh’e çevirin ve faturanızı tahmin edin. Kombi ve kalorifer kullanımına göre aylık doğal gaz maliyeti ve tasarruf ipuçları.',
h1='🔥 Doğal Gaz Faturası Hesaplama',
lead='Sayaçtan okuduğunuz m³ tüketimini girin; faturanızda kullanılan kWh karşılığını ve tahmini fatura tutarını hesaplayın.',
form='''<div class="form-grid">
<div class="field"><label for="m3">Tüketim (m³)</label><input type="number" id="m3" placeholder="örn: 180" inputmode="decimal"></div>
<div class="field"><label for="ust">Üst Isıl Değer (kcal/m³)</label><input type="number" id="ust" value="9155" inputmode="decimal"></div>
<div class="field"><label for="birim">Birim Fiyat</label><input type="number" id="birim" placeholder="faturanızdan" inputmode="decimal"></div>
<div class="field"><label for="birimTur">Birim Fiyatın Türü</label><select id="birimTur"><option value="kwh">₺ / kWh</option><option value="m3">₺ / m³</option></select></div>
</div>''',
js=r'''
function hesapla(){
  var m=v('m3'), u=v('ust')||9155, b=v('birim'); if(!(m>0)) return 'Tüketimi m³ olarak girin.';
  var kwh=m*u/860.42, rows=[['Tüketim',num(m,2)+' m³'],['kWh karşılığı',num(kwh,2)+' kWh'],['1 m³ =',num(u/860.42,2)+' kWh']];
  if(!(b>0)) return {main:['Enerji karşılığı', num(kwh,0)+' kWh'], rows:rows, note:'Tutarı görmek için faturanızdaki birim fiyatı girin.'};
  var tut=el('birimTur').value==='kwh'?kwh*b:m*b; rows.push(['Günlük ortalama (30 gün)',tl(tut/30)]);
  return {main:['Tahmini fatura', tl(tut)], sub:num(kwh,0)+' kWh', rows:rows, note:'Isıl değer bölgeye ve aya göre faturanızda yazar; varsayılan 9.155 kcal/m³ ortalama bir değerdir.'};
}''',
article='''
<h2 id="nasil">Doğal gaz faturası nasıl hesaplanır?</h2>
<p>Doğal gaz sayaçları tüketimi metreküp (m³) olarak ölçer, ancak faturalandırma 2015’ten bu yana enerji birimi olan <b>kilovatsaat (kWh)</b> üzerinden yapılır. Bunun için m³ cinsinden tüketim, gazın enerji içeriğini gösteren <b>üst ısıl değer</b> ile çarpılarak kWh’e dönüştürülür.</p>
<div class="formula">kWh = m³ × Üst ısıl değer (kcal/m³) ÷ 860,42<br>Fatura = kWh × Birim fiyat (₺/kWh)</div>
<div class="example"><p><b>Örnek:</b> 180 m³ tüketim, 9.155 kcal/m³ ısıl değer: 180 × 9.155 ÷ 860,42 = <b>1.915 kWh</b>. Bu değer faturadaki kWh birim fiyatıyla çarpılarak tutar bulunur.</p></div>

<h2 id="faturada">Faturada yer alan kalemler</h2>
<ul>
<li><b>Gaz bedeli:</b> BOTAŞ satış fiyatına dayalı enerji bedeli.</li>
<li><b>Sistem kullanım (dağıtım) bedeli:</b> Dağıtım şirketinin hizmet bedeli.</li>
<li><b>ÖTV ve KDV:</b> Doğal gazda ÖTV ve %20 KDV uygulanır.</li>
<li><b>Isıl değer:</b> Her ay farklı olabilir; faturanızın üzerinde yazar.</li>
</ul>

<h2 id="tuketim">Ortalama doğal gaz tüketimi ne kadar?</h2>
<div class="table-wrap"><table><thead><tr><th>Ev tipi (kombi)</th><th>Kış ayı tüketimi</th><th>Yaz ayı tüketimi</th></tr></thead><tbody>
<tr><td>1+1 (60–80 m²)</td><td>100–150 m³</td><td>10–20 m³</td></tr><tr><td>2+1 (90–110 m²)</td><td>150–220 m³</td><td>15–25 m³</td></tr>
<tr><td>3+1 (120–150 m²)</td><td>200–300 m³</td><td>20–30 m³</td></tr>
</tbody></table></div>
<p>Değerler binanın yalıtımına, iklime, kat konumuna ve termostat ayarına göre büyük farklılık gösterir.</p>

<h2 id="tasarruf">Doğal gaz faturası nasıl düşürülür?</h2>
<ul>
<li>Oda sıcaklığını 20–21°C’de tutun; her 1°C düşüş tüketimi yaklaşık %6 azaltır.</li>
<li>Kombinin bakımını her yıl yaptırın ve petek temizliğini ihmal etmeyin.</li>
<li>Kullanılmayan odaların peteklerini kısın, ancak tamamen kapatmayın (nem ve küf riski).</li>
<li>Pencere ve kapı aralıklarına fitil çekin; mümkünse dış cephe yalıtımı yaptırın.</li>
<li>Akıllı / oda termostatı kullanarak geceleri ve evde olmadığınız saatlerde sıcaklığı düşürün.</li>
</ul>
<p>Diğer fatura kalemleriniz için <a href="/elektrik-faturasi-hesaplama.html">elektrik faturası</a> ve <a href="/su-faturasi-hesaplama.html">su faturası</a> hesaplama araçlarını kullanabilirsiniz.</p>
''',
faq=[
('1 m³ doğal gaz kaç kWh?','Ortalama üst ısıl değer 9.155 kcal/m³ kabul edildiğinde 1 m³ doğal gaz yaklaşık 10,64 kWh’e eşittir.'),
('Doğal gaz neden kWh ile faturalandırılıyor?','Gazın enerji içeriği zamana ve kaynağa göre değiştiği için adil faturalandırma amacıyla tüketilen enerji (kWh) esas alınır.'),
('Isıl değeri nereden öğrenirim?','Faturanızda o döneme ait üst ısıl değer yazılıdır. Dağıtım şirketinin internet sitesinde de aylık değerler yayımlanır.'),
('Kombi kaç derecede kullanılmalı?','Radyatörlü sistemlerde kombi su sıcaklığını 50–60°C, oda termostatını 20–21°C’ye ayarlamak verimli kullanım sağlar.'),
],
related=['elektrik-faturasi-hesaplama','su-faturasi-hesaplama','yuzde-hesaplama','enflasyon-hesaplama','kdv-hesaplama'],
))

TOOLS.append(dict(
slug='su-faturasi-hesaplama', name='Su Faturası Hesaplama', cat='diger', ico='🚰',
title='Su Faturası Hesaplama – m³ Tüketim, Su ve Atık Su Bedeli | Hesaplarsın',
desc='Su sayacınızdaki m³ tüketimle su bedeli, atık su bedeli ve KDV dahil su faturanızı hesaplayın. Kişi başı günlük su tüketimi ve tasarruf yolları.',
h1='🚰 Su Faturası Hesaplama',
lead='Aylık su tüketiminizi ve belediyenizin m³ fiyatlarını girin; su bedeli, atık su bedeli ve vergiler dahil faturanızı ve kişi başı tüketiminizi görün.',
form='''<div class="form-grid">
<div class="field"><label for="m3">Aylık Tüketim (m³)</label><input type="number" id="m3" placeholder="örn: 15" inputmode="decimal"></div>
<div class="field"><label for="kisi">Hanedeki Kişi Sayısı</label><input type="number" id="kisi" value="3" inputmode="numeric"></div>
<div class="field"><label for="su">Su Birim Fiyatı (₺/m³)</label><input type="number" id="su" placeholder="belediye tarifesinden" inputmode="decimal"></div>
<div class="field"><label for="atik">Atık Su Birim Fiyatı (₺/m³)</label><input type="number" id="atik" placeholder="belediye tarifesinden" inputmode="decimal"></div>
<div class="field"><label for="kdv">KDV Oranı</label><select id="kdv"><option value="1" selected>%1 (konut suyu)</option><option value="10">%10</option><option value="20">%20</option></select></div>
<div class="field"><label for="ctv">ÇTV / sabit ücret (₺) <small>isteğe bağlı</small></label><input type="number" id="ctv" placeholder="örn: 30" inputmode="decimal"></div>
</div>''',
js=r'''
function hesapla(){
  var m=v('m3'), su=v('su'), at=v('atik')||0, k=parseFloat(el('kdv').value)/100, c=v('ctv')||0, n=Math.max(1,Math.round(v('kisi')||1));
  if(!(m>0)) return 'Tüketimi m³ olarak girin.'; if(!(su>0)) return 'Su birim fiyatını girin (faturanızda veya belediyenin sitesinde yazar).';
  var sb=m*su, ab=m*at, kdv=(sb+ab)*k, top=sb+ab+kdv+c, lt=m*1000/30/n;
  return {main:['Tahmini su faturası', tl(top)], sub:'Kişi başı günlük tüketim: '+num(lt,0)+' litre',
    rows:[['Su bedeli',tl(sb)],['Atık su bedeli',tl(ab)],['KDV',tl(kdv)],['ÇTV / sabit ücretler',tl(c)],['Kişi başı aylık',tl(top/n)],['1 m³’ün toplam maliyeti',tl(top/m)]],
    note:lt>150?'Kişi başı tüketiminiz Türkiye ortalamasının üzerinde; tesisatta kaçak olup olmadığını kontrol edin.':''};
}''',
article='''
<h2 id="nasil">Su faturası nasıl hesaplanır?</h2>
<p>Su faturası, sayaçta ölçülen metreküp (m³) tüketim üzerinden belediyenin (veya su idaresinin) belirlediği tarifeye göre hesaplanır. Faturada genellikle su bedeli, atık su bedeli, çevre temizlik vergisi (ÇTV) ve KDV yer alır. Bazı belediyeler kademeli tarife uygular; belirli bir tüketimin üzerindeki her m³ daha pahalıdır.</p>
<div class="formula">Fatura = m³ × (Su birim fiyatı + Atık su birim fiyatı) × (1 + KDV) + Sabit ücretler</div>
<div class="example"><p><b>Örnek:</b> 15 m³ tüketim, su 40 ₺/m³, atık su 20 ₺/m³, %1 KDV: (600 + 300) × 1,01 = <b>909 ₺</b> + ÇTV.</p></div>

<h2 id="birim">1 m³ su kaç litre?</h2>
<p>1 metreküp su <b>1.000 litre</b>dir. Ortalama bir duş (8 dakika) 60–80 litre, çamaşır makinesi bir yıkamada 40–60 litre, bulaşık makinesi 10–15 litre, tuvalet sifonu her kullanımda 6–9 litre su harcar.</p>

<h2 id="ortalama">Kişi başı ortalama su tüketimi</h2>
<p>TÜİK verilerine göre Türkiye’de belediye şebekesinden kişi başı günlük su tüketimi yaklaşık 200 litre civarındadır (kayıplar ve tüm kullanım türleri dahil). Konut içi tüketim genellikle kişi başı günde 100–150 litre arasındadır. 3 kişilik bir hanede aylık 10–15 m³ tüketim olağan kabul edilebilir.</p>

<h2 id="kacak">Su faturası neden yüksek geldi?</h2>
<ul>
<li><b>Tesisat kaçağı:</b> Tüm muslukları kapatıp sayacı izleyin; çark dönmeye devam ediyorsa kaçak vardır.</li>
<li><b>Sızdıran rezervuar:</b> Tuvalet rezervuarından sessizce akan su ayda birkaç m³ israfa yol açabilir.</li>
<li><b>Okuma dönemi:</b> Sayaç okuma aralığı 30 günden uzun olduğunda fatura yüksek görünebilir.</li>
<li><b>Kademeli tarife:</b> Belirli tüketimin üzerindeki m³’ler daha yüksek fiyatla hesaplanır.</li>
</ul>

<h2 id="tasarruf">Su tasarrufu için ipuçları</h2>
<ul>
<li>Musluklara perlatör (havalandırıcı) takarak debiyi %30–50 azaltın.</li>
<li>Duş süresini kısaltın, diş fırçalarken musluğu kapatın.</li>
<li>Çamaşır ve bulaşık makinelerini tam dolu çalıştırın.</li>
<li>Çift kademeli sifon (3/6 litre) kullanın.</li>
</ul>
<p>Diğer fatura kalemleriniz için <a href="/elektrik-faturasi-hesaplama.html">elektrik faturası</a> ve <a href="/dogalgaz-faturasi-hesaplama.html">doğal gaz faturası</a> hesaplama araçlarına göz atın.</p>
''',
faq=[
('1 ton su kaç m³?','1 ton su 1 m³’tür ve 1.000 litreye eşittir.'),
('Su faturasında KDV oranı nedir?','Konutlara verilen içme ve kullanma suyunda KDV oranı %1’dir; atık su bedeline de genellikle aynı oran uygulanır.'),
('Atık su bedeli nedir?','Kullanılan suyun kanalizasyon ve arıtma hizmetinin karşılığıdır; tüketilen her m³ su için ayrıca alınır.'),
('3 kişilik aile ayda ne kadar su harcar?','Genellikle 10–15 m³ arasıdır. 20 m³’ün üzeri tüketim, kaçak veya yüksek kullanım belirtisi olabilir.'),
],
related=['elektrik-faturasi-hesaplama','dogalgaz-faturasi-hesaplama','su-ihtiyaci-hesaplama','yuzde-hesaplama','kdv-hesaplama'],
))
