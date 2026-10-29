"""Para sayma (banknot) hesaplayıcı: 'X tane 200 TL ne kadar eder' tipi aramalar için."""
TOOLS = []

DEN = [200, 100, 50, 20, 10, 5, 1]


def tr(x):
    return f"{x:,.0f}".replace(',', '.')


ADET = [10, 25, 50, 75, 100, 150, 200, 225, 250, 300, 350, 400, 500, 1000]
T200 = ''.join(f'<tr><td>{a} tane</td><td>{tr(a * 200)} ₺</td><td>{tr(a * 100)} ₺</td><td>{tr(a * 50)} ₺</td></tr>' for a in ADET)
TABLO = ('<div style="overflow-x:auto"><table class="veri-tablo" aria-label="Banknot adet tablosu"><thead><tr><th>Adet</th><th>200 ₺’lik</th><th>100 ₺’lik</th><th>50 ₺’lik</th></tr></thead>'
         f'<tbody>{T200}</tbody></table></div>')

FORM = '<div class="form-grid">' + ''.join(
    f'<div class="field"><label for="b{d}">{d} ₺ {"madeni para" if d == 1 else "banknot"} <small>adet</small></label><input type="number" id="b{d}" placeholder="0" inputmode="numeric"></div>'
    for d in DEN) + '</div>'

JS = r'''
var DEN=[200,100,50,20,10,5,1];
function hesapla(){
  var top=0,adet=0,rows=[];
  DEN.forEach(function(d){var n=v('b'+d)||0; if(n<0||n%1) n=Math.round(Math.abs(n)); if(n>0){top+=n*d;adet+=n;rows.push([n+' × '+d+' ₺',tl(n*d)]);}});
  if(!adet) return 'En az bir banknot için adet girin (örn. 200 ₺ kutusuna 225).';
  var deste=Math.floor(adet/100);
  rows.push(['Toplam banknot / para adedi',num(adet,0)+' adet'+(deste?' ('+deste+' deste'+(adet%100?' + '+(adet%100)+' adet':'')+')':'')]);
  rows.push(['Ortalama değer',tl(top/adet)]);
  return {main:['Toplam tutar',tl(top)],sub:num(adet,0)+' adet para',rows:rows,
    note:'1 deste = 100 banknot. Örneğin 1 deste 200 ₺ = 20.000 ₺, 1 deste 100 ₺ = 10.000 ₺.'};
}
'''

TOOLS.append(dict(
slug='para-sayma-hesaplama', name='Para Sayma Hesaplama', cat='finans', ico='💵',
title='Kaç Tane 200 TL Ne Kadar Eder? Para Sayma Hesaplama ve Tablo | Hesaplarsın',
desc='25 tane 200 TL 5.000 TL, 75 tane 15.000 TL, 250 tane 50.000 TL eder. Banknot adedini girin; toplam tutarı ve deste sayısını anında görün.',
h1='💵 Para Sayma Hesaplama',
lead='Her banknottan kaç tane olduğunu yazın; toplam tutarı, deste sayısını ve banknot dağılımını anında görün. Kasa sayımı, düğün takısı, harçlık birikimi ya da elden ödeme kontrolü için.',
card_title='Banknot Sayma Hesaplayıcı', button='Toplamı Hesapla',
form=FORM, js=JS,
article=f'''<h2 id="tablo">Kaç tane 200 TL ne kadar eder? Hazır tablo</h2>
<p>En çok sorulan adetler için toplam tutarlar. Formül basittir: <strong>adet × banknot değeri</strong>. Örneğin 225 tane 200 ₺ = 225 × 200 = <strong>45.000 ₺</strong>; 350 tane 200 ₺ = <strong>70.000 ₺</strong>.</p>
{TABLO}
<h2 id="deste">Deste nedir, 1 deste para kaç TL?</h2>
<p>Bankalarda ve kasalarda banknotlar 100’lük paketler halinde sayılır; buna <strong>deste</strong> denir. Yani:</p>
<ul><li>1 deste 200 ₺ = 100 × 200 = <strong>20.000 ₺</strong></li>
<li>1 deste 100 ₺ = <strong>10.000 ₺</strong></li>
<li>1 deste 50 ₺ = <strong>5.000 ₺</strong></li>
<li>1 deste 20 ₺ = <strong>2.000 ₺</strong></li></ul>
<p>Bankalar genellikle 10 desteyi (1.000 banknot) bir <strong>paket</strong> olarak bantlar. 1 paket 200 ₺ = 200.000 ₺ eder.</p>
<h2 id="tersten">Tersten hesap: Bir tutar kaç tane 200 TL eder?</h2>
<p>Tutarı banknot değerine bölün. Örneğin 100.000 ₺ = 100.000 ÷ 200 = <strong>500 tane 200 ₺</strong>; 50.000 ₺ = <strong>250 tane 200 ₺</strong>. Tutar tam bölünmüyorsa kalan kısmı küçük banknotlarla tamamlarsınız: 45.150 ₺ = 225 tane 200 ₺ + 1 tane 100 ₺ + 1 tane 50 ₺.</p>
<h2 id="ipucu">Elden büyük tutar sayarken dikkat</h2>
<ul><li>Banknotları önce değerine göre ayırın, sonra 100’lük desteler yapın; her desteyi ayrı sayıp üstüne not edin.</li>
<li>Toplamı bu hesaplayıcıyla kontrol edin ve karşı tarafla birlikte doğrulayın.</li>
<li>Büyük tutarlı ödemelerde banka havalesi hem iz bırakır hem sayım hatasını ortadan kaldırır.</li></ul>
<p>Döviz karşılığı için <a href="https://hesaplarsin.com/doviz-cevirici.html">döviz çevirici</a>, yüzde hesapları için <a href="https://hesaplarsin.com/yuzde-hesaplama.html">yüzde hesaplama</a> aracını kullanabilirsiniz.</p>''',
faq=[('225 tane 200 TL ne kadar eder?', '225 × 200 = 45.000 TL eder.'),
     ('350 tane 200 TL kaç TL?', '350 × 200 = 70.000 TL eder.'),
     ('500 adet 200 TL ne kadar?', '500 × 200 = 100.000 TL eder; bu da 5 deste 200 TL demektir.'),
     ('1 deste 200 TL kaç para?', '1 deste 100 banknottan oluşur: 100 × 200 = 20.000 TL.'),
     ('100 bin TL kaç tane 200 TL eder?', '100.000 ÷ 200 = 500 tane 200 TL banknot eder.')],
related=['yuzde-hesaplama', 'doviz-cevirici', 'enflasyon-hesaplama', 'gun-hesaplama'],
badges=['✓ Ücretsiz', 'Anında Sonuç', 'Kayıt Gerektirmez'],
))

# ═════════════════════════ ALTIN ═════════════════════════
# Gramajlar: Hazine ve Maliye Bakanlığı "Sorularla Cumhuriyet Altını" (Darphane ziynet ve sikke ağırlıkları). 22 ayar = 916,67 milyem.
# Canlı fiyat: finans.truncgil.com/v4/today.json (alış/satış, CORS açık). Yedek: api.gold-api.com XAU (USD/ons) × USD/TRY.
ALTIN_T = [  # anahtar, ad, truncgil kodu, birim, ağırlık (g), milyem
    ('ceyrek', 'Çeyrek altın', 'CEYREKALTIN', 'adet', 1.754, 22 / 24),
    ('yarim', 'Yarım altın', 'YARIMALTIN', 'adet', 3.508, 22 / 24),
    ('tam', 'Tam altın', 'TAMALTIN', 'adet', 7.016, 22 / 24),
    ('cumhuriyet', 'Cumhuriyet altını', 'CUMHURIYETALTINI', 'adet', 7.216, 22 / 24),
    ('ata', 'Ata altın', 'ATAALTIN', 'adet', 7.216, 22 / 24),
    ('gremse', 'Gremse (ikibuçuk)', 'GREMSEALTIN', 'adet', 17.54, 22 / 24),
    ('besli', 'Beşli altın', 'BESLIALTIN', 'adet', 35.08, 22 / 24),
    ('gram', 'Gram altın (24 ayar)', 'GRA', 'gram', 1.0, 0.995),
    ('b22', '22 ayar bilezik', 'YIA', 'gram', 1.0, 22 / 24),
    ('a18', '18 ayar altın', '18AYARALTIN', 'gram', 1.0, 18 / 24),
    ('a14', '14 ayar altın', '14AYARALTIN', 'gram', 1.0, 14 / 24),
]
def _g3(x):
    return f'{x:,.3f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
ALTIN_FORM = ('''<div class="field full" style="margin-bottom:14px"><label>Ne hesaplamak istiyorsunuz?</label>
<div class="seg"><label><input type="radio" name="mod" value="deger" checked>Altınlarım kaç TL?</label><label><input type="radio" name="mod" value="butce">Bütçemle kaç altın alırım?</label></div></div>
<div class="field full" style="margin-bottom:14px"><label>Fiyat</label>
<div class="seg"><label><input type="radio" name="fiyat" value="Buying" checked>Bozdurursam (alış)</label><label><input type="radio" name="fiyat" value="Selling">Satın alırsam (satış)</label></div></div>
<div class="form-grid">'''
 + ''.join(f'<div class="field"><label for="{k}">{ad} <small>{b}</small></label><input type="number" id="{k}" placeholder="0" inputmode="decimal"></div>' for k, ad, _, b, _, _ in ALTIN_T)
 + '''<div class="field"><label for="butce">Bütçe (₺) <small>bütçe modu için</small></label><input type="number" id="butce" placeholder="örn: 50000" inputmode="decimal"></div>
<div class="field"><label for="manuel">Gram altın fiyatı (₺) <small>isteğe bağlı – boşsa canlı fiyat</small></label><input type="number" id="manuel" placeholder="canlı fiyat" inputmode="decimal"></div>
</div>
<p id="altinDurum" style="font-size:.78rem;color:var(--muted);margin-top:10px">Canlı fiyatlar yükleniyor…</p>''')
ALTIN_JS = ('var AT=' + str([[k, ad, kod, b, w, round(m, 5)] for k, ad, kod, b, w, m in ALTIN_T]).replace("'", '"') + ';' + r'''
var AP=null, AKAYNAK='', AZAMAN='';
function aFmt(n){return n.toLocaleString('tr-TR',{minimumFractionDigits:2,maximumFractionDigits:2})+' ₺';}
function aTablo(){
  var tb=document.getElementById('altinTablo'); if(!tb||!AP) return;
  tb.innerHTML=AT.map(function(t){var p=AP[t[2]]; if(!p) return '';
    return '<tr><td>'+t[1]+(t[3]==='gram'?' <small>(gram)</small>':'')+'</td><td>'+aFmt(p.Buying)+'</td><td>'+aFmt(p.Selling)+'</td></tr>';}).join('');
  var z=document.getElementById('altinZaman'); if(z) z.textContent=AZAMAN+' · '+AKAYNAK;
  var d=el('altinDurum'); if(d) d.innerHTML='Canlı fiyat: gram altın <b>'+aFmt(AP.GRA.Selling)+'</b> (satış) · '+AZAMAN;
}
function aYedek(){
  return Promise.all([fetch('https://api.gold-api.com/price/XAU',{cache:'no-store'}).then(function(r){return r.json();}),
    fetch('https://api.frankfurter.dev/v1/latest?from=USD&to=TRY',{cache:'no-store'}).then(function(r){return r.json();})]).then(function(x){
    var g=x[0].price/31.1034768*x[1].rates.TRY; if(!(g>0)) throw 0; AP={};
    AT.forEach(function(t){var f=t[3]==='gram'?t[5]/0.995:t[4]*t[5]/0.995; AP[t[2]]={Buying:g*f,Selling:g*f};});
    AKAYNAK='uluslararası ons fiyatından tahmini has değer (işçilik hariç)'; AZAMAN=new Date().toLocaleString('tr-TR'); aTablo();});
}
fetch('https://finans.truncgil.com/v4/today.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json();}).then(function(d){
  if(!d.GRA||!(d.GRA.Selling>0)) throw 0; AP={}; AT.forEach(function(t){if(d[t[2]]&&d[t[2]].Selling>0) AP[t[2]]=d[t[2]];});
  AKAYNAK='Kapalıçarşı piyasa fiyatı (Truncgil Finans)'; AZAMAN=d.Update_Date||''; aTablo();
}).catch(function(){aYedek().catch(function(){var d=el('altinDurum'); if(d) d.textContent='Canlı fiyat alınamadı; gram altın fiyatını elle girerek hesaplayabilirsiniz.';});});
function hesapla(){
  var man=v('manuel'), yon=radio('fiyat')||'Buying', mod=radio('mod')||'deger', fiyat={}, kaynak;
  if(man>0){ AT.forEach(function(t){fiyat[t[0]]=t[3]==='gram'?man*t[5]/0.995:man*t[4]*t[5]/0.995;}); kaynak='Girdiğiniz gram fiyatıyla has değer (işçilik hariç)'; }
  else if(AP){ AT.forEach(function(t){var p=AP[t[2]]; if(p) fiyat[t[0]]=p[yon];}); kaynak=AKAYNAK+' · '+AZAMAN; }
  else return 'Canlı fiyatlar henüz yüklenmedi. Birkaç saniye bekleyin ya da gram altın fiyatını elle girin.';
  if(mod==='butce'){
    var b=v('butce'); if(!(b>0)) return 'Bütçe modunda “Bütçe (₺)” alanına tutar girin.';
    var sf={}; if(man>0) sf=fiyat; else AT.forEach(function(t){var p=AP[t[2]]; if(p) sf[t[0]]=p.Selling;});
    var rows=AT.filter(function(t){return sf[t[0]];}).map(function(t){var n=b/sf[t[0]];
      return [t[1], t[3]==='gram'?num(n,2)+' gram':Math.floor(n)+' adet <small>(adet fiyatı '+tl(sf[t[0]])+')</small>'];});
    return {main:['Bütçeniz', tl(b)], sub:'Satış fiyatıyla alabileceğiniz miktarlar', rows:rows, note:kaynak+'. Kuyumcuda ödeyeceğiniz tutar işçilik ve kuyumcu farkına göre değişebilir.'};
  }
  var top=0, rows=[], has=0;
  AT.forEach(function(t){var n=v(t[0]); if(n>0&&fiyat[t[0]]){var d=n*fiyat[t[0]]; top+=d; has+=n*t[4]*t[5]; rows.push([num(n,t[3]==='gram'?2:0)+' '+(t[3]==='gram'?'gr ':'× ')+t[1], tl(d)]);}});
  if(!rows.length) return 'En az bir altın türü için adet veya gram girin (örn. çeyrek altın: 5).';
  rows.push(['Toplam has (saf) altın','≈ '+num(has,2)+' gram']);
  return {main:['Altınlarınızın değeri', tl(top)], sub:(yon==='Buying'?'Bozdurursanız (kuyumcu alış fiyatı)':'Satın alırsanız (kuyumcu satış fiyatı)'), rows:rows, note:kaynak+'. Fiyatlar bilgilendirme amaçlıdır; kuyumcudan kuyumcuya değişebilir.'};
}''')
ALTIN_GRAMAJ = ('<div class="table-wrap"><table><thead><tr><th>Altın türü</th><th>Ağırlık</th><th>Ayar</th><th>Saf (has) altın</th></tr></thead><tbody>'
    + ''.join(f'<tr><td>{ad}</td><td>{_g3(w)} g</td><td>22 ayar</td><td>{_g3(w * m)} g</td></tr>' for k, ad, _, b, w, m in ALTIN_T if b == 'adet')
    + '</tbody></table></div>')

TOOLS.append(dict(
slug='altin-hesaplama', name='Altın Hesaplama', cat='finans', ico='🪙',
title='Altın Hesaplama – Gram, Çeyrek, Tam Altın Kaç TL? Canlı Fiyatlarla | Hesaplarsın',
desc='Canlı fiyatlarla altın hesaplama: gram, çeyrek, yarım, tam, Cumhuriyet altını ve 22 ayar bilezik kaç TL? Düğünde takılan altınların değerini ve bütçenizle kaç altın alacağınızı görün.',
h1='🪙 Altın Hesaplama – Canlı Fiyatlarla Altın Kaç TL?',
lead='Elinizdeki ya da düğünde takılan çeyrek, yarım, tam, Cumhuriyet altınlarını ve gram/bilezik miktarını girin; canlı alış veya satış fiyatıyla toplam değerini görün. Bütçe modunda, paranızla kaç gram ya da kaç çeyrek altın alabileceğinizi hesaplayın.',
card_title='Altın Değeri Hesaplayıcı', button='Hesapla',
form=ALTIN_FORM,
js=ALTIN_JS,
article=f'''<h2 id="canli">Canlı altın fiyatları</h2>
<p>Aşağıdaki tablo sayfa açıldığında Kapalıçarşı piyasa fiyatlarıyla güncellenir. <b>Alış</b>, kuyumcunun sizden altın alırken (siz bozdururken) ödediği fiyattır; <b>satış</b>, size altın satarken istediği fiyattır.</p>
<div class="table-wrap"><table><thead><tr><th>Altın</th><th>Alış</th><th>Satış</th></tr></thead><tbody id="altinTablo"><tr><td colspan="3">Fiyatlar yükleniyor…</td></tr></tbody></table></div>
<p style="font-size:.8rem;color:var(--muted)">Son güncelleme: <span id="altinZaman">—</span>. Fiyatlar bilgilendirme amaçlıdır; kuyumcudan kuyumcuya ve gün içinde değişir.</p>

<h2 id="dugun">Düğünde takılan altınlar nasıl hesaplanır?</h2>
<p>Düğün, nişan veya sünnette takılan altınların toplam değerini bulmak için her türün adedini girmeniz yeterlidir. Örneğin 12 çeyrek, 3 yarım, 2 tam altın ve 30 gram 22 ayar bilezik için hesaplayıcı her kalemi ayrı ayrı fiyatlar, toplam tutarı ve içindeki saf (has) altın miktarını gösterir. Altınları bozdurmayı düşünüyorsanız <b>alış</b>, aynı altınları yeniden almanın maliyetini görmek istiyorsanız <b>satış</b> fiyatını seçin.</p>

<h2 id="gramaj">Çeyrek, yarım, tam altın kaç gram?</h2>
<p>Darphane’nin bastığı ziynet ve Cumhuriyet altınları 22 ayardır (916,67 milyem). Resmî ağırlıklar:</p>
{ALTIN_GRAMAJ}
<p>Ziynet altınların (çeyrek, yarım, tam, gremse, beşli) ağırlığı Cumhuriyet sikkelerinden biraz düşüktür: tam ziynet altın 7,016 gram, Cumhuriyet (Ata) altını 7,216 gramdır. Bu yüzden Cumhuriyet altını tam altından biraz daha pahalıdır.</p>

<h2 id="fark">Çeyrek altın neden 1,6 gram altından pahalı?</h2>
<p>Çeyrek altının içinde yaklaşık 1,608 gram saf altın bulunur, ancak piyasa fiyatı bu has değerin üzerindedir. Aradaki fark <b>işçilik</b> (basım maliyeti) ve kuyumcu kârıdır. Aynı nedenle altın bozdururken kuyumcunun alış fiyatı, satış fiyatının altında kalır. Yatırım amacıyla alımlarda gram altın ve has altının işçilik farkı daha düşüktür.</p>

<h2 id="bilezik">Bilezik ve takı altını nasıl hesaplanır?</h2>
<p>Bilezikler genellikle 22 ayar, takılar 14 veya 18 ayardır. Değer, gram × o ayarın gram fiyatıyla bulunur: 30 gram 22 ayar bilezik = 30 × 22 ayar gram fiyatı. Ayar, 24 parçada kaç parçanın saf altın olduğunu gösterir: 22 ayar %91,7, 18 ayar %75, 14 ayar %58,5 saf altın içerir. Kuyumcular takı bozdururken işçiliği ödemez; yalnızca altın değerini, kendi alış fiyatından hesaplar.</p>

<h2 id="kaynak">Fiyatlar nereden geliyor?</h2>
<p>Canlı fiyatlar Kapalıçarşı piyasa verilerini yayımlayan Truncgil Finans’tan alınır. Bu kaynağa ulaşılamazsa hesaplayıcı uluslararası ons fiyatını (ABD doları) güncel dolar kuruyla gram fiyatına çevirir ve altınların <b>has değerini</b> işçilik hariç gösterir. Gram fiyatını kendiniz girerseniz hesap, girdiğiniz fiyat ve resmî gramajlar üzerinden yapılır.</p>''',
faq=[('Çeyrek altın kaç gram?', 'Ziynet çeyrek altın 1,754 gram ve 22 ayardır; içinde yaklaşık 1,608 gram saf altın bulunur. Yarım altın 3,508 gram, tam altın 7,016 gramdır.'),
     ('Cumhuriyet altını ile tam altın arasındaki fark nedir?', 'İkisi de 22 ayardır. Cumhuriyet (Ata) altını 7,216 gram, tam ziynet altın 7,016 gramdır. Bu 0,2 gramlık fark nedeniyle Cumhuriyet altını biraz daha pahalıdır.'),
     ('Altın bozdururken hangi fiyat geçerli?', 'Kuyumcunun alış fiyatı geçerlidir. Alış fiyatı, size altın satarken uyguladığı satış fiyatından düşüktür; aradaki fark kuyumcunun payıdır.'),
     ('22 ayar bilezik nasıl hesaplanır?', 'Bileziğin gramı, 22 ayar altının gram fiyatıyla çarpılır. Bozdururken işçilik ödenmez; kuyumcu yalnızca altın değerini alış fiyatından hesaplar.'),
     ('14 ayar altın ne demek?', '14 ayar, 24 parçanın 14’ünün saf altın olduğunu gösterir; yani altının yaklaşık %58,5’i saftır (585 milyem). 18 ayar %75, 22 ayar %91,7 saf altın içerir.'),
     ('Düğünde takılan altınların değeri nasıl hesaplanır?', 'Çeyrek, yarım, tam ve Cumhuriyet altınlarının adedini, bileziklerin ise gramını hesaplayıcıya girin. Araç her kalemi güncel fiyatla çarpar ve toplam değeri gösterir.')],
related=['doviz-cevirici', 'para-deger-kaybi-hesaplama', 'enflasyon-hesaplama', 'mevduat-faizi-hesaplama', 'kripto-kar-zarar-hesaplama'],
sources=[('Hazine ve Maliye Bakanlığı – Sorularla Cumhuriyet Altını (Darphane gramajları)', 'https://ms.hmb.gov.tr/uploads/sites/7/2021/05/Sorularla_Cumhuriyet_Altini.pdf'), ('Truncgil Finans – piyasa fiyatları', 'https://finans.truncgil.com/')],
badges=['✓ Ücretsiz', 'Canlı Fiyat', 'Düğün Altını'],
))
