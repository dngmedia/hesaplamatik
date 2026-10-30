"""Zaman, matematik, günlük kullanım ve araç (yakıt) hesaplamaları."""

HOLIDAYS_JS = r'''
// Resmi tatiller (tam gün) ve arife yarım günleri — 2025, 2026, 2027
var TATIL = {
 '2025-01-01':'Yılbaşı','2025-03-30':'Ramazan Bayramı 1. gün','2025-03-31':'Ramazan Bayramı 2. gün','2025-04-01':'Ramazan Bayramı 3. gün',
 '2025-04-23':'Ulusal Egemenlik ve Çocuk Bayramı','2025-05-01':'Emek ve Dayanışma Günü','2025-05-19':'Atatürk’ü Anma, Gençlik ve Spor Bayramı',
 '2025-06-06':'Kurban Bayramı 1. gün','2025-06-07':'Kurban Bayramı 2. gün','2025-06-08':'Kurban Bayramı 3. gün','2025-06-09':'Kurban Bayramı 4. gün',
 '2025-07-15':'Demokrasi ve Millî Birlik Günü','2025-08-30':'Zafer Bayramı','2025-10-29':'Cumhuriyet Bayramı',
 '2026-01-01':'Yılbaşı','2026-03-20':'Ramazan Bayramı 1. gün','2026-03-21':'Ramazan Bayramı 2. gün','2026-03-22':'Ramazan Bayramı 3. gün',
 '2026-04-23':'Ulusal Egemenlik ve Çocuk Bayramı','2026-05-01':'Emek ve Dayanışma Günü','2026-05-19':'Atatürk’ü Anma, Gençlik ve Spor Bayramı',
 '2026-05-27':'Kurban Bayramı 1. gün','2026-05-28':'Kurban Bayramı 2. gün','2026-05-29':'Kurban Bayramı 3. gün','2026-05-30':'Kurban Bayramı 4. gün',
 '2026-07-15':'Demokrasi ve Millî Birlik Günü','2026-08-30':'Zafer Bayramı','2026-10-29':'Cumhuriyet Bayramı',
 '2027-01-01':'Yılbaşı','2027-03-09':'Ramazan Bayramı 1. gün','2027-03-10':'Ramazan Bayramı 2. gün','2027-03-11':'Ramazan Bayramı 3. gün',
 '2027-04-23':'Ulusal Egemenlik ve Çocuk Bayramı','2027-05-01':'Emek ve Dayanışma Günü','2027-05-19':'Atatürk’ü Anma, Gençlik ve Spor Bayramı',
 '2027-05-16':'Kurban Bayramı 1. gün','2027-05-17':'Kurban Bayramı 2. gün','2027-05-18':'Kurban Bayramı 3. gün',
 '2027-07-15':'Demokrasi ve Millî Birlik Günü','2027-08-30':'Zafer Bayramı','2027-10-29':'Cumhuriyet Bayramı'
};
TATIL['2027-05-19']='Kurban Bayramı 4. gün / 19 Mayıs';
var ARIFE = {'2025-03-29':1,'2025-06-05':1,'2025-10-28':1,'2026-03-19':1,'2026-05-26':1,'2026-10-28':1,'2027-03-08':1,'2027-05-15':1,'2027-10-28':1};
function ymd(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
'''

TOOLS = []

# ───────────────────────── YAŞ ─────────────────────────
TOOLS.append(dict(
slug='yas-hesaplama', name='Yaş Hesaplama', cat='diger', ico='🎂',
title='Yaş Hesaplama – Kaç Yaşındayım? Yıl, Ay, Gün Olarak | Hesaplarsın',
desc='Doğum tarihinizi girin; yaşınızı yıl, ay, gün olarak öğrenin. Doğum gününüze kalan gün, okula başlama yaşı (ay), ehliyet ve askerlik yaşı tek sayfada.',
h1='🎂 Yaş Hesaplama – Kaç Yaşındayım?',
lead='Doğum tarihinizi girin; tam yaşınızı yıl-ay-gün olarak, toplam yaşadığınız gün sayısını ve bir sonraki doğum gününüze kalan süreyi saniyeler içinde öğrenin.',
form='''<div class="form-grid">
  <div class="field"><label for="dogum">Doğum Tarihi</label><input type="date" id="dogum" min="1900-01-01"></div>
  <div class="field"><label for="hedef">Hesaplama Tarihi <small>(boş = bugün)</small></label><input type="date" id="hedef"></div>
</div>''',
js=r'''
function okulYasi(d,h){
  var ry=(h.getMonth()>8)?h.getFullYear()+1:h.getFullYear(), ref=new Date(ry,8,30);
  var ay=(ry-d.getFullYear())*12+(8-d.getMonth())-(d.getDate()>30?1:0);
  if(ay<36||ay>84) return [];
  var dn=ay<57?'1. sınıf için erken (66 ay gerekir)':ay<66?'Anaokulu yaşında; 1. sınıfa kayıt olamaz':ay<69?'1. sınıf zorunlu değil, veli dilekçesiyle kayıt olabilir':ay<72?'1. sınıf zorunlu, veli dilekçesiyle ertelenebilir':ay<78?'1. sınıf zorunlu (erteleme yalnızca RAM kararıyla)':'1. sınıf zorunlu, erteleme yok';
  return [['Okul yaşı (30 Eylül '+ry+')', ay+' ay · '+dn,'hl']];
}
function hesapla(){
  var d=parseDate('dogum'); if(!d) return 'Lütfen doğum tarihinizi seçin.';
  var h=parseDate('hedef')||new Date(); h=new Date(h.getFullYear(),h.getMonth(),h.getDate());
  if(d>h) return 'Doğum tarihi, hesaplama tarihinden sonra olamaz.';
  var y=h.getFullYear()-d.getFullYear(), m=h.getMonth()-d.getMonth(), g=h.getDate()-d.getDate();
  if(g<0){m--; g+=new Date(h.getFullYear(),h.getMonth(),0).getDate();}
  if(m<0){y--; m+=12;}
  var gun=Math.round((h-d)/864e5);
  var sonraki=new Date(h.getFullYear(),d.getMonth(),d.getDate()); if(sonraki<h) sonraki.setFullYear(h.getFullYear()+1);
  var kalan=Math.round((sonraki-h)/864e5);
  var burclar=[[1,20,'Oğlak'],[2,19,'Kova'],[3,21,'Balık'],[4,20,'Koç'],[5,21,'Boğa'],[6,22,'İkizler'],[7,23,'Yengeç'],[8,23,'Aslan'],[9,23,'Başak'],[10,23,'Terazi'],[11,22,'Akrep'],[12,22,'Yay'],[13,1,'Oğlak']];
  var mm=d.getMonth()+1, dd=d.getDate(), burc='Oğlak';
  for(var i=0;i<12;i++){ if(mm===burclar[i][0] && dd<burclar[i][1]){burc=i===0?'Oğlak':burclar[i-1][2];break;} if(mm===burclar[i][0]){burc=burclar[i][2];break;} }
  return {
    main:['Yaşınız', y+' yaş '+m+' ay '+g+' gün'],
    sub: kalan===0?'🎉 Bugün doğum gününüz! İyi ki doğdunuz.':'Bir sonraki doğum gününüze <b>'+kalan+' gün</b> kaldı ('+(y+1)+'. yaş)',
    rows:[
      ['Toplam yaşanan gün', num(gun,0)+' gün'],
      ['Toplam hafta', num(Math.floor(gun/7),0)+' hafta '+(gun%7)+' gün'],
      ['Toplam ay', num(y*12+m,0)+' ay'],
      ['Toplam saat (yaklaşık)', num(gun*24,0)+' saat'],
      ['Doğduğunuz gün', d.toLocaleDateString('tr-TR',{weekday:'long'})],
      ['Sonraki doğum günü', dt(sonraki)],
      ['Burcunuz', burc]
    ].concat(okulYasi(d,h))};
}''',
article='''
<h2 id="nasil">Yaş nasıl hesaplanır?</h2>
<p>Yaş, doğum tarihinden itibaren geçen tam yıl sayısıdır. Hesaplama yapılırken önce iki tarih arasındaki yıl farkı bulunur; ardından hesaplama tarihindeki ay ve gün, doğum tarihindeki ay ve günden küçükse yıl farkından bir çıkarılır. Çünkü o yıl için doğum günü henüz gelmemiştir. Kalan ay ve gün de aynı mantıkla bulunur.</p>
<div class="formula">Yaş (yıl) = Hesaplama yılı − Doğum yılı<br>Doğum günü henüz gelmediyse → Yaş − 1</div>
<div class="example"><p><b>Örnek:</b> 15 Mart 1995 doğumlu biri için 21 Ekim 2026 tarihinde:</p>
<p>2026 − 1995 = 31 yıl. Mart ayı geçtiği için yıl düşülmez. Mart 15 → Ekim 15 arası 7 ay, Ekim 15 → Ekim 21 arası 6 gün.</p>
<p>Sonuç: <b>31 yaş 7 ay 6 gün</b>.</p></div>

<h2 id="belirli-tarih">Belirli bir tarihteki yaşımı nasıl öğrenirim?</h2>
<p>Hesaplayıcıdaki “Hesaplama Tarihi” alanına geçmişte ya da gelecekte herhangi bir tarihi yazabilirsiniz. Bu özellik özellikle şu durumlarda işe yarar:</p>
<ul>
<li><b>Sınav ve başvurular:</b> KPSS, polis veya askeri okul başvurularında “başvuru tarihi itibarıyla” yaş şartı aranır.</li>
<li><b>Ehliyet:</b> B sınıfı ehliyet için 18 yaşını doldurmuş olmak gerekir; sınav tarihindeki yaşınızı kontrol edebilirsiniz.</li>
<li><b>Emeklilik:</b> Emeklilikte yaş şartının hangi tarihte dolacağını görmek için <a href="/emeklilik-yasi-hesaplama.html">emeklilik yaşı hesaplama</a> aracını kullanabilirsiniz.</li>
<li><b>Okula başlama:</b> İlkokula kayıtta çocuğun eylül ayı sonu itibarıyla yaşı dikkate alınır.</li>
</ul>

<h2 id="gun-sayisi">Kaç gün yaşadım?</h2>
<p>Toplam yaşanan gün sayısı, doğum tarihi ile bugün arasındaki takvim günlerinin toplamıdır; artık yıllardaki 29 Şubat günleri de hesaba otomatik olarak dahil edilir. Ortalama bir yıl 365,25 gün kabul edilirse 30 yaşındaki biri yaklaşık 10.957 gün yaşamış olur. İki tarih arasındaki farkı farklı amaçlarla bulmak için <a href="/gun-hesaplama.html">gün hesaplama</a> aracını kullanabilirsiniz.</p>

<h2 id="dogum-gunu">Doğum günüme kaç gün kaldı?</h2>
<p>Bir sonraki doğum gününe kalan süre, bu yılki doğum günü geçtiyse gelecek yılın aynı tarihine, geçmediyse bu yılki tarihe göre hesaplanır. 29 Şubat doğumlular için artık yıl olmayan yıllarda doğum günü genellikle 1 Mart olarak kabul edilir.</p>

<h2 id="yasal-yaslar">Türkiye’de önemli yasal yaş sınırları</h2>
<div class="table-wrap"><table><thead><tr><th>Durum</th><th>Yaş</th></tr></thead><tbody>
<tr><td>Ergin olma (reşit olma)</td><td>18</td></tr>
<tr><td>B sınıfı sürücü belgesi</td><td>18</td></tr>
<tr><td>Oy kullanma</td><td>18</td></tr>
<tr><td>Milletvekili seçilebilme</td><td>18</td></tr>
<tr><td>Cumhurbaşkanı adaylığı</td><td>40</td></tr>
<tr><td>Çalışma hayatına giriş (hafif işler, okul dışı)</td><td>15</td></tr>
</tbody></table></div>
''',
faq=[
('Yaş hesaplamada doğum günü dahil edilir mi?','Evet. Doğum gününüz geldiği gün bir yaş büyümüş sayılırsınız. Örneğin 10 Mayıs doğumlu biri 10 Mayıs günü yeni yaşına girer.'),
('29 Şubat doğumluların yaşı nasıl hesaplanır?','Yaş yine tam yıl farkı olarak hesaplanır. Artık yıl olmayan yıllarda doğum günü resmi işlemlerde genellikle 1 Mart kabul edilir.'),
('Ay ve gün olarak yaşımı nasıl bulurum?','Hesaplayıcı yaşınızı yıl, ay ve gün olarak ayrı ayrı gösterir. Ayrıca toplam ay, hafta, gün ve saat değerlerini de listeler.'),
('Hangi gün doğduğumu öğrenebilir miyim?','Evet. Sonuç tablosundaki “Doğduğunuz gün” satırı, doğum tarihinizin haftanın hangi gününe denk geldiğini gösterir.'),
('Girdiğim bilgiler kaydediliyor mu?','Hayır. Hesaplama tamamen tarayıcınızda yapılır; doğum tarihiniz hiçbir sunucuya gönderilmez veya saklanmaz.'),
],
related=['gun-hesaplama','is-gunu-hesaplama','emeklilik-yasi-hesaplama','ortalama-hesaplama','yuzde-hesaplama'],
howto=('Yaş nasıl hesaplanır?',['Doğum tarihinizi seçin.','İsterseniz farklı bir hesaplama tarihi girin; boş bırakırsanız bugün esas alınır.','Hesapla butonuna basın; yaşınız yıl, ay ve gün olarak gösterilir.']),
))

# ───────────────────────── GÜN ─────────────────────────
TOOLS.append(dict(
slug='gun-hesaplama', name='Gün Hesaplama', cat='diger', ico='📅',
title='Gün Hesaplama – İki Tarih Arası Kaç Gün? Kaç Gün Kaldı, Kaç Gün Oldu | Hesaplarsın',
desc='İki tarih arasındaki gün, hafta, ay ve yıl farkını hesaplayın ya da bir tarihe gün ekleyip çıkarın. Kaç gün kaldı, kaç gün geçti sorularına anında cevap.',
h1='📅 Gün Hesaplama – İki Tarih Arası Kaç Gün?',
lead='İki tarih arasındaki gün sayısını bulun veya bir tarihe gün ekleyip çıkararak hangi tarihe denk geldiğini öğrenin. Kaç gün kaldı, kaç gün oldu sorularının cevabı burada.',
form='''<div class="field full" style="margin-bottom:14px"><label>İşlem</label>
<div class="seg"><label><input type="radio" name="mod" value="fark" checked onchange="modSec()">İki tarih arası</label><label><input type="radio" name="mod" value="ekle" onchange="modSec()">Tarihe gün ekle / çıkar</label></div></div>
<div class="form-grid">
  <div class="field"><label for="t1">Başlangıç Tarihi</label><input type="date" id="t1"></div>
  <div class="field" id="f-t2"><label for="t2">Bitiş Tarihi <small>(boş = bugün)</small></label><input type="date" id="t2"></div>
  <div class="field" id="f-gun" style="display:none"><label for="gun">Gün Sayısı <small>(çıkarmak için eksi yazın)</small></label><input type="number" id="gun" placeholder="örn: 90 veya -30" inputmode="numeric"></div>
  <div class="field full" id="f-dahil"><label class="chk"><input type="checkbox" id="dahil"> Bitiş gününü de say (+1 gün)</label></div>
</div>''',
js=r'''
function modSec(){var e=radio('mod')==='ekle';el('f-t2').style.display=e?'none':'';el('f-dahil').style.display=e?'none':'';el('f-gun').style.display=e?'':'none';el('result').style.display='none';_last=null;}
function hesapla(){
  var a=parseDate('t1'); if(!a) return 'Lütfen başlangıç tarihini seçin.';
  if(radio('mod')==='ekle'){
    var n=v('gun'); if(isNaN(n)) return 'Eklenecek gün sayısını girin.';
    var r=new Date(a); r.setDate(r.getDate()+Math.round(n));
    return {main:[(n>=0?'+':'')+num(n,0)+' gün sonrası', r.toLocaleDateString('tr-TR',{day:'numeric',month:'long',year:'numeric'})],
      sub:r.toLocaleDateString('tr-TR',{weekday:'long'}),
      rows:[['Başlangıç',dt(a)],['Eklenen gün',num(n,0)],['Sonuç tarihi',dt(r)]]};
  }
  var b=parseDate('t2')||new Date(); b=new Date(b.getFullYear(),b.getMonth(),b.getDate());
  var ters=b<a; if(ters){var t=a;a=b;b=t;}
  var g=Math.round((b-a)/864e5)+(checked('dahil')?1:0);
  var y=b.getFullYear()-a.getFullYear(), m=b.getMonth()-a.getMonth(), d=b.getDate()-a.getDate();
  if(d<0){m--; d+=new Date(b.getFullYear(),b.getMonth(),0).getDate();} if(m<0){y--; m+=12;}
  var hs=0, son=new Date(b); if(checked('dahil')) son.setDate(son.getDate()+1); for(var x=new Date(a);x<son;x.setDate(x.getDate()+1)){var w=x.getDay(); if(w===0||w===6) hs++;}
  return {main:['İki tarih arası', num(g,0)+' gün'],
    sub:(y?y+' yıl ':'')+(m?m+' ay ':'')+d+' gün'+(ters?' (tarihler yer değiştirildi)':''),
    rows:[['Hafta',num(g/7,1)+' hafta'],['Ay (ortalama)',num(g/30.4375,2)+' ay'],['Yıl',num(g/365.25,2)+' yıl'],
      ['Saat',num(g*24,0)+' saat'],['Hafta sonu günü',num(hs,0)+' gün'],['Hafta içi günü',num(g-hs,0)+' gün'],
      ['Başlangıç',dt(a)],['Bitiş',dt(b)]],
    note:'Resmi tatilleri düşerek çalışma günü hesaplamak için <a href="/is-gunu-hesaplama.html">iş günü hesaplama</a> aracını kullanın.'};
}''',
article='''
<h2 id="nasil">İki tarih arasındaki gün sayısı nasıl hesaplanır?</h2>
<p>İki tarih arasındaki gün sayısı, başlangıç tarihinden bitiş tarihine kadar geçen takvim günlerinin toplamıdır. Ayların 28, 29, 30 veya 31 gün çekmesi ve artık yıllar elle hesaplamayı zorlaştırır; bu araç bunları otomatik olarak dikkate alır.</p>
<p>Varsayılan hesaplamada başlangıç günü sayılır, bitiş günü sayılmaz. Örneğin 1 Ocak ile 2 Ocak arası <b>1 gün</b>dür. Kira, izin veya rapor gibi hem ilk hem son günün sayıldığı durumlar için “Bitiş gününü de say” kutusunu işaretleyin.</p>
<div class="formula">Gün farkı = Bitiş tarihi − Başlangıç tarihi<br>Bitiş günü dahil ise → Gün farkı + 1</div>
<div class="example"><p><b>Örnek:</b> 1 Mart 2026 ile 15 Haziran 2026 arası:</p><p>Mart (31) + Nisan (30) + Mayıs (31) + 14 gün = <b>106 gün</b> (yaklaşık 15,1 hafta).</p></div>

<h2 id="ekle-cikar">Bir tarihe gün nasıl eklenir veya çıkarılır?</h2>
<p>“Tarihe gün ekle / çıkar” modunu seçip başlangıç tarihini ve gün sayısını girin. Geriye doğru gitmek için gün sayısını eksi (örneğin −45) yazmanız yeterlidir. Bu özellik şu sorulara cevap verir:</p>
<ul>
<li>Bugünden 90 gün sonrası hangi tarih? (garanti, iade ve deneme süreleri)</li>
<li>Faturanın son ödeme tarihinden 30 gün önce ne zamandı?</li>
<li>Hamileliğin 280. günü hangi tarihe denk geliyor?</li>
<li>Askerlik, staj veya proje teslim tarihine kaç gün kaldı?</li>
</ul>

<h2 id="kullanim">Gün hesaplama nerelerde kullanılır?</h2>
<ul>
<li><b>Hukuki süreler:</b> İtiraz, temyiz ve ödeme süreleri gün olarak verilir. Son gün resmi tatile denk gelirse süre bir sonraki iş gününe uzar.</li>
<li><b>Faiz ve vade:</b> Mevduat ve gecikme faizi gün sayısı üzerinden hesaplanır. Bkz. <a href="/mevduat-faizi-hesaplama.html">mevduat faizi hesaplama</a>.</li>
<li><b>İzin ve tazminat:</b> Kıdem tazminatında çalışma süresi gün bazında dikkate alınır. Bkz. <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı hesaplama</a>.</li>
<li><b>Kişisel sayaçlar:</b> Tanışma yıldönümü, sigarayı bırakma, düğüne kalan gün gibi.</li>
</ul>

<h2 id="ay-gunleri">Aylar kaç gün çeker?</h2>
<div class="table-wrap"><table><thead><tr><th>31 gün</th><th>30 gün</th><th>28 / 29 gün</th></tr></thead><tbody>
<tr><td>Ocak, Mart, Mayıs, Temmuz, Ağustos, Ekim, Aralık</td><td>Nisan, Haziran, Eylül, Kasım</td><td>Şubat (artık yılda 29)</td></tr>
</tbody></table></div>
<p>Artık yıllar 4’e tam bölünen yıllardır; ancak 100’e bölünüp 400’e bölünmeyen yıllar artık yıl değildir. 2028 bir sonraki artık yıldır.</p>
''',
faq=[
('İki tarih arası hesaplamada ilk ve son gün sayılır mı?','Varsayılan olarak başlangıç günü sayılır, bitiş günü sayılmaz. Her iki günün de sayılması gerekiyorsa “Bitiş gününü de say” seçeneğini işaretleyin; sonuca 1 gün eklenir.'),
('Bugünden itibaren 100 gün sonrası hangi tarih?','“Tarihe gün ekle / çıkar” modunu seçin, başlangıç tarihine bugünü yazın ve gün sayısına 100 girin. Sonuç tarihi ve haftanın günü gösterilir.'),
('Kaç gün kaldığını nasıl hesaplarım?','Başlangıç tarihine bugünü, bitiş tarihine hedef günü yazın. Sonuç, hedef tarihe kalan gün sayısını verir.'),
('Hafta sonları hariç gün sayısını nasıl bulurum?','Sonuç tablosunda hafta içi gün sayısı ayrıca gösterilir. Resmi tatilleri de düşmek için iş günü hesaplama aracını kullanın.'),
('Bir yıl kaç gündür?','Normal yıl 365, artık yıl 366 gündür. Ortalama yıl uzunluğu 365,25 gün kabul edilir.'),
],
related=['is-gunu-hesaplama','yas-hesaplama','mevduat-faizi-hesaplama','kidem-tazminati-hesaplama','ortalama-hesaplama'],
howto=('İki tarih arası gün nasıl hesaplanır?',['İşlem olarak “İki tarih arası”nı seçin.','Başlangıç ve bitiş tarihlerini girin.','Gerekirse bitiş gününü dahil edin ve Hesapla’ya basın.']),
))

# ───────────────────────── İŞ GÜNÜ ─────────────────────────
TOOLS.append(dict(
slug='is-gunu-hesaplama', name='İş Günü Hesaplama', cat='diger', ico='🗓️',
title='İş Günü Hesaplama 2026 – Resmi Tatiller Hariç Kaç İş Günü? | Hesaplarsın',
desc='İki tarih arasındaki iş günü sayısını 2026 ve 2027 resmi tatilleri, bayramlar ve arife yarım günleri düşülerek hesaplayın. Cumartesi çalışma seçeneği dahil.',
h1='🗓️ İş Günü Hesaplama (2026–2027 Resmi Tatiller Dahil)',
lead='Hafta sonları, resmi tatiller, Ramazan ve Kurban bayramları düşülerek iki tarih arasında kaç iş günü olduğunu hesaplayın veya bir tarihe iş günü ekleyin.',
form='''<div class="field full" style="margin-bottom:14px"><label>İşlem</label>
<div class="seg"><label><input type="radio" name="mod" value="fark" checked onchange="modSec()">İki tarih arası iş günü</label><label><input type="radio" name="mod" value="ekle" onchange="modSec()">Tarihe iş günü ekle</label></div></div>
<div class="form-grid">
  <div class="field"><label for="t1">Başlangıç Tarihi</label><input type="date" id="t1" min="2025-01-01" max="2027-12-31"></div>
  <div class="field" id="f-t2"><label for="t2">Bitiş Tarihi</label><input type="date" id="t2" min="2025-01-01" max="2027-12-31"></div>
  <div class="field" id="f-n" style="display:none"><label for="n">Eklenecek İş Günü</label><input type="number" id="n" placeholder="örn: 10" inputmode="numeric"></div>
  <div class="field full"><label class="chk"><input type="checkbox" id="cmt"> Cumartesi iş günü sayılsın</label>
  <label class="chk"><input type="checkbox" id="arife" checked> Arife günlerini yarım gün say</label></div>
</div>''',
js=r'''
''' + HOLIDAYS_JS + r'''
function modSec(){var e=radio('mod')==='ekle';el('f-t2').style.display=e?'none':'';el('f-n').style.display=e?'':'none';el('result').style.display='none';_last=null;}
function gunDegeri(d){var w=d.getDay(),k=ymd(d); if(w===0) return 0; if(w===6&&!checked('cmt')) return 0; if(TATIL[k]) return 0; if(ARIFE[k]&&checked('arife')) return 0.5; return 1;}
function hesapla(){
  var a=parseDate('t1'); if(!a) return 'Başlangıç tarihini seçin.';
  if(a.getFullYear()<2025||a.getFullYear()>2027) return 'Tatil verisi 2025–2027 yıllarını kapsar.';
  if(radio('mod')==='ekle'){
    var n=v('n'); if(!(n>0)) return 'Eklenecek iş günü sayısını girin.';
    var d=new Date(a), say=0, guv=0;
    while(say<n && guv<2000){ d.setDate(d.getDate()+1); say+=gunDegeri(d)===1?1:0; guv++; }
    if(d.getFullYear()>2027) return 'Sonuç tatil verisinin kapsadığı yılların dışında kalıyor.';
    return {main:[num(n,0)+' iş günü sonrası', d.toLocaleDateString('tr-TR',{day:'numeric',month:'long',year:'numeric'})], sub:d.toLocaleDateString('tr-TR',{weekday:'long'}),
      rows:[['Başlangıç',dt(a)],['Takvim günü farkı',num(Math.round((d-a)/864e5),0)+' gün']], note:'Başlangıç günü sayılmaz; ertesi günden itibaren tam iş günleri sayılır.'};
  }
  var b=parseDate('t2'); if(!b) return 'Bitiş tarihini seçin.'; if(b<a) return 'Bitiş tarihi başlangıçtan önce olamaz.';
  if(b.getFullYear()>2027) return 'Tatil verisi 2027 sonuna kadar geçerlidir.';
  var tg=0, is=0, hs=0, rt=[], yarim=0;
  for(var d=new Date(a); d<=b; d.setDate(d.getDate()+1)){
    tg++; var w=d.getDay(), k=ymd(d), val=gunDegeri(d);
    if(TATIL[k] && w!==0 && !(w===6&&!checked('cmt'))) rt.push('<tr><td>'+d.toLocaleDateString('tr-TR')+'</td><td>'+TATIL[k]+'</td></tr>');
    else if(w===0||(w===6&&!checked('cmt'))) hs++;
    if(val===0.5){ yarim++; }
    is+=val;
  }
  return {main:['Toplam iş günü', num(is,is%1?1:0)+' gün'], sub:a.toLocaleDateString('tr-TR')+' – '+b.toLocaleDateString('tr-TR')+' (her iki gün dahil)',
    rows:[['Takvim günü',num(tg,0)],['Hafta sonu ('+(checked('cmt')?'Pazar':'Cumartesi + Pazar')+')',num(hs,0)],['Hafta içine denk gelen resmi tatil',num(rt.length,0)],['Arife (yarım gün)',num(yarim,0)],['İş saati (9 saat/gün)',num(is*9,1)+' saat']],
    extra: rt.length?'<table><thead><tr><th>Tarih</th><th>Düşülen resmi tatil</th></tr></thead><tbody>'+rt.join('')+'</tbody></table>':''};
}''',
article='''
<h2 id="is-gunu-nedir">İş günü nedir?</h2>
<p>İş günü; hafta sonu tatilleri ile ulusal bayram ve genel tatil günleri dışında kalan, kamu kurumlarının ve çoğu özel işyerinin açık olduğu günlerdir. Türkiye’de kamu kurumları için iş günleri Pazartesi–Cuma arasıdır. Cumartesi günü çalışan işyerlerinde (örneğin perakende, üretim) Cumartesi de iş günü sayılır; bunun için hesaplayıcıdaki ilgili kutuyu işaretleyin.</p>

<h2 id="nasil">İki tarih arası iş günü nasıl hesaplanır?</h2>
<p>Önce iki tarih arasındaki toplam takvim günü bulunur. Ardından bu günlerden Cumartesi–Pazar günleri ve hafta içine denk gelen resmi tatiller çıkarılır. Ramazan ve Kurban bayramı arifeleri ile 28 Ekim, 13.00’ten sonra tatil olduğundan <b>yarım gün</b> olarak sayılır.</p>
<div class="formula">İş günü = Takvim günü − Hafta sonu − Resmi tatiller − (Arife × 0,5)</div>

<h2 id="tatiller-2026">2026 resmi tatil günleri</h2>
<div class="table-wrap"><table><thead><tr><th>Tatil</th><th>Tarih</th><th>Gün</th></tr></thead><tbody>
<tr><td>Yılbaşı</td><td>1 Ocak 2026</td><td>Perşembe</td></tr>
<tr><td>Ramazan Bayramı arifesi (yarım gün)</td><td>19 Mart 2026</td><td>Perşembe</td></tr>
<tr><td>Ramazan Bayramı</td><td>20–22 Mart 2026</td><td>Cuma–Pazar</td></tr>
<tr><td>Ulusal Egemenlik ve Çocuk Bayramı</td><td>23 Nisan 2026</td><td>Perşembe</td></tr>
<tr><td>Emek ve Dayanışma Günü</td><td>1 Mayıs 2026</td><td>Cuma</td></tr>
<tr><td>Atatürk’ü Anma, Gençlik ve Spor Bayramı</td><td>19 Mayıs 2026</td><td>Salı</td></tr>
<tr><td>Kurban Bayramı arifesi (yarım gün)</td><td>26 Mayıs 2026</td><td>Salı</td></tr>
<tr><td>Kurban Bayramı</td><td>27–30 Mayıs 2026</td><td>Çarşamba–Cumartesi</td></tr>
<tr><td>Demokrasi ve Millî Birlik Günü</td><td>15 Temmuz 2026</td><td>Çarşamba</td></tr>
<tr><td>Zafer Bayramı</td><td>30 Ağustos 2026</td><td>Pazar</td></tr>
<tr><td>Cumhuriyet Bayramı arifesi (yarım gün)</td><td>28 Ekim 2026</td><td>Çarşamba</td></tr>
<tr><td>Cumhuriyet Bayramı</td><td>29 Ekim 2026</td><td>Perşembe</td></tr>
</tbody></table></div>

<h2 id="tatiller-2027">2027 resmi tatil günleri</h2>
<div class="table-wrap"><table><thead><tr><th>Tatil</th><th>Tarih</th></tr></thead><tbody>
<tr><td>Yılbaşı</td><td>1 Ocak 2027 (Cuma)</td></tr>
<tr><td>Ramazan Bayramı</td><td>Arife 8 Mart (yarım gün), bayram 9–11 Mart 2027</td></tr>
<tr><td>23 Nisan</td><td>23 Nisan 2027 (Cuma)</td></tr>
<tr><td>1 Mayıs</td><td>1 Mayıs 2027 (Cumartesi)</td></tr>
<tr><td>Kurban Bayramı</td><td>Arife 15 Mayıs (yarım gün), bayram 16–19 Mayıs 2027</td></tr>
<tr><td>19 Mayıs</td><td>19 Mayıs 2027 (Kurban Bayramı 4. günüyle çakışır)</td></tr>
<tr><td>15 Temmuz</td><td>15 Temmuz 2027 (Perşembe)</td></tr>
<tr><td>30 Ağustos</td><td>30 Ağustos 2027 (Pazartesi)</td></tr>
<tr><td>29 Ekim</td><td>Arife 28 Ekim (yarım gün), 29 Ekim 2027 (Cuma)</td></tr>
</tbody></table></div>
<p>Dini bayram tarihleri Diyanet İşleri Başkanlığı takvimine göre belirlenir. Hükümet tarafından ilan edilebilecek ek idari izinler (köprü günleri) resmi tatil sayılmaz ve hesaplamaya dahil edilmez.</p>

<h2 id="yillik">Bir yılda kaç iş günü var?</h2>
<p>Pazartesi–Cuma çalışılan bir işyerinde bir yılda yaklaşık 260–261 hafta içi gün bulunur. 2026’da hafta içine denk gelen 10 resmi tatil günü düşüldüğünde Pazartesi–Cuma çalışan bir işyeri için <b>251 iş günü</b> kalır; üç arife günü yarım gün sayılırsa bu sayı <b>249,5</b> olur. Kesin sayıyı hesaplayıcıda 1 Ocak–31 Aralık 2026 aralığını seçerek görebilirsiniz.</p>

<h2 id="kullanim">İş günü hesabı nerelerde gerekir?</h2>
<ul>
<li><b>Hukuki ve idari süreler:</b> Bazı kanunlarda süreler “iş günü” olarak verilir.</li>
<li><b>Kargo ve teslimat:</b> “3–5 iş günü içinde teslim” vaatleri iş günü üzerinden hesaplanır.</li>
<li><b>Yıllık izin:</b> İzin süresine hafta tatili ve resmi tatiller dahil edilmez. Hakkınızı <a href="/yillik-izin-hesaplama.html">yıllık izin hesaplama</a> ile öğrenin.</li>
<li><b>Proje planlama ve fazla mesai:</b> Aylık çalışma saatini bulmak için iş günü sayısı kullanılır. Bkz. <a href="/fazla-mesai-hesaplama.html">fazla mesai hesaplama</a>.</li>
</ul>
''',
faq=[
('Cumartesi iş günü mü?','Kamu kurumları ve bankalar için Cumartesi iş günü değildir. Ancak İş Kanunu’na göre haftalık 45 saatlik çalışma 6 güne yayılabildiğinden Cumartesi çalışılan işyerlerinde iş günü sayılır.'),
('Arife günleri iş günü mü?','Ramazan ve Kurban bayramı arifeleri ile 28 Ekim, öğleden sonra (13.00) tatil olduğu için yarım iş günü olarak kabul edilir. İsterseniz bu seçeneği kapatıp tam gün sayabilirsiniz.'),
('Hafta sonuna denk gelen resmi tatil iş gününden düşülür mü?','Hayır. Zaten çalışılmayan bir güne denk geldiği için iş günü sayısını ayrıca azaltmaz. Hesaplayıcı yalnızca hafta içine denk gelen tatilleri düşer.'),
('Başlangıç ve bitiş günleri hesaba dahil mi?','“İki tarih arası” modunda başlangıç ve bitiş günleri dahildir. “Tarihe iş günü ekle” modunda ise başlangıç günü sayılmaz, ertesi günden itibaren sayılır.'),
('Köprü günleri (idari izin) hesaba katılıyor mu?','Hayır. İdari izinler yalnızca kamu çalışanları için geçerlidir ve resmi tatil sayılmaz; bu nedenle iş günü hesabına dahil edilmez.'),
],
related=['gun-hesaplama','yillik-izin-hesaplama','fazla-mesai-hesaplama','yas-hesaplama','saatlik-ucret-hesaplama'],
sources=[('Borsa İstanbul 2026 tatil tablosu','https://www.borsaistanbul.com/files/pay-piyasasi-2026-yili-tatil-tablosu.pdf'),('2429 sayılı Ulusal Bayram ve Genel Tatiller Kanunu','https://www.mevzuat.gov.tr/mevzuatmetin/1.3.2429.pdf')],
))

# ───────────────────────── ORTALAMA ─────────────────────────
TOOLS.append(dict(
slug='ortalama-hesaplama', name='Ortalama Hesaplama', cat='diger', ico='➗',
title='Ortalama Hesaplama – Sayıların Ortalaması Nasıl Bulunur? | Hesaplarsın',
desc='70, 85 ve 90’ın ortalaması 81,67. Sayıları yapıştırın; aritmetik ve ağırlıklı ortalama, medyan, mod ve standart sapma tek seferde çıksın. Ücretsiz, kayıt gerektirmez.',
h1='➗ Ortalama Hesaplama',
lead='Sayılarınızı yapıştırın; aritmetik ortalama, medyan, mod, en büyük-en küçük değer, açıklık ve standart sapma tek tıkla hesaplansın. Ağırlıklı ortalama modu da mevcut.',
form='''<div class="field full" style="margin-bottom:14px"><label>Ortalama Türü</label>
<div class="seg"><label><input type="radio" name="mod" value="aritmetik" checked onchange="modSec()">Aritmetik</label><label><input type="radio" name="mod" value="agirlikli" onchange="modSec()">Ağırlıklı</label></div></div>
<div class="field full"><label for="sayilar" id="lbl">Sayılar <small>(boşluk, satır veya noktalı virgül ile ayırın)</small></label>
<textarea id="sayilar" rows="5" placeholder="örn: 85 70 92 64,5 78"></textarea></div>
<div class="field full" id="f-agr" style="display:none;margin-top:12px"><label for="agirlik">Ağırlıklar <small>(sayılarla aynı sırada)</small></label>
<textarea id="agirlik" rows="3" placeholder="örn: 4 3 2 2 1"></textarea></div>''',
js=r'''
function modSec(){el('f-agr').style.display=radio('mod')==='agirlikli'?'':'none';if(_last)run(false);}
function liste(id){return raw(id).split(/[\s;\n]+/).map(function(s){s=s.trim();if(!s)return NaN;if(/^-?\d{1,3}(\.\d{3})+(,\d+)?$/.test(s))s=s.replace(/\./g,'');return parseFloat(s.replace(',','.'));}).filter(function(x){return !isNaN(x);});}
function hesapla(){
  var a=liste('sayilar'); if(a.length<1) return 'En az bir sayı girin.';
  if(radio('mod')==='agirlikli'){
    var w=liste('agirlik'); if(w.length!==a.length) return 'Sayı ('+a.length+') ve ağırlık ('+w.length+') adetleri eşit olmalı.';
    var sw=w.reduce(function(t,x){return t+x;},0); if(sw===0) return 'Ağırlıkların toplamı sıfır olamaz.';
    var s=a.reduce(function(t,x,i){return t+x*w[i];},0);
    var tf=function(x){return num(x,4).replace(/0+$/,'').replace(/,$/,'');}; return {main:['Ağırlıklı ortalama', tf(s/sw)], rows:[['Σ (sayı × ağırlık)',tf(s)],['Σ ağırlık',tf(sw)],['Sayı adedi',a.length]]};
  }
  var n=a.length, top=a.reduce(function(t,x){return t+x;},0), ort=top/n, s=a.slice().sort(function(x,y){return x-y;});
  var med=n%2?s[(n-1)/2]:(s[n/2-1]+s[n/2])/2;
  var f={},mx=0; a.forEach(function(x){f[x]=(f[x]||0)+1;if(f[x]>mx)mx=f[x];});
  var mod=mx>1?Object.keys(f).filter(function(k){return f[k]===mx;}).map(function(k){return num(+k,2);}).join(' · '):'Yok (tekrar eden değer yok)';
  var vs=a.reduce(function(t,x){return t+(x-ort)*(x-ort);},0);
  var g=a.every(function(x){return x>0;})?Math.exp(a.reduce(function(t,x){return t+Math.log(x);},0)/n):null;
  var fmt=function(x){return num(x,4).replace(/0+$/,'').replace(/,$/,'');};
  return {main:['Aritmetik ortalama', fmt(ort)], sub:n+' sayının toplamı '+fmt(top),
    rows:[['Medyan (ortanca)',fmt(med)],['Mod (tepe değer)',mod],['En küçük',fmt(s[0])],['En büyük',fmt(s[n-1])],['Açıklık (aralık)',fmt(s[n-1]-s[0])],
      ['Standart sapma (örneklem)',n>1?fmt(Math.sqrt(vs/(n-1))):'—'],['Standart sapma (popülasyon)',fmt(Math.sqrt(vs/n))],['Geometrik ortalama',g?fmt(g):'— (yalnızca pozitif sayılar)'],['Sıralı liste',s.map(fmt).join(', ')]]};
}''',
article='''
<h2 id="aritmetik">Aritmetik ortalama nasıl hesaplanır?</h2>
<p>Aritmetik ortalama, bir veri kümesindeki tüm sayıların toplanıp sayı adedine bölünmesiyle bulunur. Günlük hayatta “ortalama” denince genellikle aritmetik ortalama kastedilir: sınav notları, aylık harcamalar veya günlük adım sayısı gibi.</p>
<div class="formula">Ortalama = (x₁ + x₂ + … + xₙ) ÷ n</div>
<div class="example"><p><b>Örnek:</b> 85, 70, 92, 64 ve 78 notlarının ortalaması:</p><p>(85 + 70 + 92 + 64 + 78) ÷ 5 = 389 ÷ 5 = <b>77,8</b></p></div>

<h2 id="agirlikli">Ağırlıklı ortalama nedir?</h2>
<p>Her değerin önemi (ağırlığı) farklıysa ağırlıklı ortalama kullanılır. Üniversitede dersin kredisi, lisede haftalık ders saati, sınavlarda vize-final yüzdeleri birer ağırlıktır. Her sayı kendi ağırlığıyla çarpılır, çarpımlar toplanır ve ağırlıkların toplamına bölünür.</p>
<div class="formula">Ağırlıklı ortalama = Σ(xᵢ × wᵢ) ÷ Σwᵢ</div>
<div class="example"><p><b>Örnek:</b> Matematik 80 (4 saat), Türkçe 90 (5 saat), Fizik 60 (2 saat):</p><p>(80×4 + 90×5 + 60×2) ÷ (4+5+2) = 890 ÷ 11 = <b>80,91</b></p></div>
<p>Okul notları için hazır bir araç arıyorsanız <a href="/not-ortalamasi-hesaplama.html">not ortalaması hesaplama</a> sayfasını kullanabilirsiniz.</p>

<h2 id="medyan-mod">Medyan ve mod nedir?</h2>
<p><b>Medyan (ortanca)</b>, sayılar küçükten büyüğe sıralandığında tam ortada kalan değerdir. Sayı adedi çiftse ortadaki iki sayının ortalaması alınır. Medyan, uç değerlerden (örneğin çok yüksek bir maaş) etkilenmediği için gelir ve fiyat analizlerinde ortalamadan daha anlamlı olabilir.</p>
<p><b>Mod (tepe değer)</b>, veri kümesinde en sık tekrar eden değerdir. Hiçbir değer tekrar etmiyorsa mod yoktur; birden fazla değer aynı sıklıkta tekrar ediyorsa birden fazla mod olabilir.</p>

<h2 id="sapma">Standart sapma ne işe yarar?</h2>
<p>Standart sapma, değerlerin ortalama etrafında ne kadar dağıldığını gösterir. Düşük standart sapma verilerin ortalamaya yakın, yüksek standart sapma ise dağınık olduğunu anlatır. Bir sınıfın notları içinden alınan örnek için <b>örneklem</b> (n−1’e bölünür), tüm topluluk için <b>popülasyon</b> (n’ye bölünür) standart sapması kullanılır.</p>

<h2 id="turler">Ortalama türlerinin karşılaştırması</h2>
<div class="table-wrap"><table><thead><tr><th>Tür</th><th>Ne zaman kullanılır?</th></tr></thead><tbody>
<tr><td>Aritmetik</td><td>Değerler benzer önemdeyse (not, sıcaklık, harcama)</td></tr>
<tr><td>Ağırlıklı</td><td>Değerlerin önemi farklıysa (kredi, ders saati, yüzde payı)</td></tr>
<tr><td>Medyan</td><td>Uç değerler varsa (maaş, ev fiyatı)</td></tr>
<tr><td>Geometrik</td><td>Oranlar ve büyüme hızları (yıllık getiri, enflasyon)</td></tr>
</tbody></table></div>
''',
faq=[
('Ortalama nasıl bulunur?','Tüm sayılar toplanır ve sayı adedine bölünür. Örneğin 10, 20 ve 30’un ortalaması (10+20+30)/3 = 20’dir.'),
('Ondalıklı sayıları nasıl yazmalıyım?','Ondalık ayırıcı olarak virgül veya nokta kullanabilirsiniz (64,5 veya 64.5). Sayıları boşluk, noktalı virgül ya da alt alta yazarak ayırın.'),
('Medyan ile ortalama arasındaki fark nedir?','Ortalama tüm değerlerin toplamına dayanır ve uç değerlerden etkilenir. Medyan ise sıralı listenin ortasındaki değerdir ve uç değerlerden etkilenmez.'),
('Negatif sayıların ortalaması alınabilir mi?','Evet. Aritmetik ortalama, medyan ve standart sapma negatif sayılarla da hesaplanır. Yalnızca geometrik ortalama pozitif sayı gerektirir.'),
],
related=['not-ortalamasi-hesaplama','yuzde-hesaplama','tyt-net-hesaplama','gun-hesaplama','indirim-hesaplama'],
))

# ───────────────────────── İNDİRİM ─────────────────────────
TOOLS.append(dict(
slug='indirim-hesaplama', name='İndirim Hesaplama', cat='isletme', ico='🏷️',
title='İndirim Hesaplama – Yüzde Kaç İndirim? İndirimli Fiyat Bulma | Hesaplarsın',
desc='1.200 TL’ye %25 indirim = 900 TL. İndirimli fiyatı, indirim yüzdesini ve indirimden önceki fiyatı tek tıkla bulun; çift indirim (%20+%10) dahil.',
h1='🏷️ İndirim Hesaplama',
lead='%30 indirimli fiyat ne kadar? 1.500 ₺’lik ürün 1.050 ₺’ye düştüyse yüzde kaç indirim yapılmış? Üç farklı indirim hesabını ve çift indirimi tek araçta yapın.',
form='''<div class="field full" style="margin-bottom:14px"><label>Ne hesaplamak istiyorsunuz?</label>
<div class="seg"><label><input type="radio" name="mod" value="fiyat" checked onchange="modSec()">İndirimli fiyat</label><label><input type="radio" name="mod" value="oran" onchange="modSec()">İndirim oranı</label><label><input type="radio" name="mod" value="eski" onchange="modSec()">Eski (etiket) fiyat</label></div></div>
<div class="form-grid">
  <div class="field" id="f-normal"><label for="normal">Normal Fiyat (₺)</label><input type="number" id="normal" placeholder="örn: 1500" inputmode="decimal"></div>
  <div class="field" id="f-indirimli" style="display:none"><label for="indirimli">İndirimli Fiyat (₺)</label><input type="number" id="indirimli" placeholder="örn: 1050" inputmode="decimal"></div>
  <div class="field" id="f-oran"><label for="oran">İndirim Oranı (%)</label><input type="number" id="oran" placeholder="örn: 30" inputmode="decimal">
    <div class="qtags"><span class="qtag" onclick="el('oran').value=10">%10</span><span class="qtag" onclick="el('oran').value=20">%20</span><span class="qtag" onclick="el('oran').value=30">%30</span><span class="qtag" onclick="el('oran').value=50">%50</span></div></div>
  <div class="field" id="f-oran2"><label for="oran2">Ek İndirim (%) <small>isteğe bağlı</small></label><input type="number" id="oran2" placeholder="örn: 10 (sepette)" inputmode="decimal"></div>
</div>''',
js=r'''
function modSec(){var m=radio('mod');el('f-normal').style.display=m==='eski'?'none':'';el('f-indirimli').style.display=m==='fiyat'?'none':'';
el('f-oran').style.display=m==='oran'?'none':'';el('f-oran2').style.display=m==='fiyat'?'':'none';el('result').style.display='none';_last=null;}
function hesapla(){
  var m=radio('mod');
  if(m==='fiyat'){
    var p=v('normal'),o=v('oran'),o2=v('oran2')||0; if(!(p>0)) return 'Normal fiyatı girin.'; if(isNaN(o)||o<0||o>100) return 'İndirim oranı 0–100 arasında olmalı.';
    var f1=p*(1-o/100), f2=f1*(1-o2/100), top=(1-f2/p)*100;
    var rows=[['Normal fiyat',tl(p)],['İndirim (%'+num(o,o%1?1:0)+')','−'+tl(p-f1),'neg']];
    if(o2>0){rows.push(['İlk indirim sonrası',tl(f1)]);rows.push(['Ek indirim (%'+num(o2,o2%1?1:0)+')','−'+tl(f1-f2),'neg']);rows.push(['Toplam (gerçek) indirim oranı',pct(top)]);}
    rows.push(['Toplam tasarruf',tl(p-f2),'hl']);
    return {main:['İndirimli fiyat', tl(f2)], rows:rows, note:o2>0?'Art arda indirimler toplanmaz: %'+num(o,0)+' + %'+num(o2,0)+' indirim, %'+num(o+o2,0)+' değil <b>%'+num(top,2)+'</b> indirime eşittir.':''};
  }
  if(m==='oran'){
    var p=v('normal'),f=v('indirimli'); if(!(p>0)||isNaN(f)) return 'Normal ve indirimli fiyatı girin.'; if(f>p) return 'İndirimli fiyat normal fiyattan büyük; bu bir zam. Yüzde hesaplama aracını kullanın.';
    return {main:['İndirim oranı', pct((p-f)/p*100)], rows:[['Normal fiyat',tl(p)],['İndirimli fiyat',tl(f)],['İndirim tutarı',tl(p-f),'hl']]};
  }
  var f=v('indirimli'),o=v('oran'); if(!(f>0)) return 'İndirimli fiyatı girin.'; if(!(o>=0&&o<100)) return 'İndirim oranı 0–100 arasında olmalı.';
  var p=f/(1-o/100);
  return {main:['İndirim öncesi fiyat', tl(p)], rows:[['İndirimli fiyat',tl(f)],['İndirim oranı',pct(o)],['İndirim tutarı',tl(p-f)]]};
}''',
article='''
<h2 id="indirimli-fiyat">İndirimli fiyat nasıl hesaplanır?</h2>
<p>İndirimli fiyatı bulmak için ürünün normal fiyatı, indirim oranının yüzdesiyle çarpılır ve bulunan indirim tutarı fiyattan çıkarılır. Daha kısa yolu, fiyatı doğrudan <b>(1 − oran/100)</b> ile çarpmaktır.</p>
<div class="formula">İndirim tutarı = Fiyat × Oran ÷ 100<br>İndirimli fiyat = Fiyat × (1 − Oran ÷ 100)</div>
<div class="example"><p><b>Örnek:</b> 1.500 ₺’lik montta %30 indirim:</p><p>İndirim: 1.500 × 0,30 = 450 ₺ → İndirimli fiyat: 1.500 − 450 = <b>1.050 ₺</b></p></div>

<h2 id="oran">İndirim oranı nasıl bulunur?</h2>
<p>Eski ve yeni fiyat biliniyorsa aradaki fark eski fiyata bölünüp 100 ile çarpılır. Böylece “1.200 ₺’den 900 ₺’ye düşen ürün yüzde kaç indirimli?” sorusunun cevabı bulunur.</p>
<div class="formula">İndirim oranı (%) = (Eski fiyat − Yeni fiyat) ÷ Eski fiyat × 100</div>
<div class="example"><p><b>Örnek:</b> (1.200 − 900) ÷ 1.200 × 100 = <b>%25</b> indirim.</p></div>

<h2 id="eski-fiyat">İndirimli fiyattan eski fiyat nasıl bulunur?</h2>
<p>Sık yapılan hata, indirimli fiyata aynı oranı eklemektir. %20 indirimli 800 ₺’lik ürünün eski fiyatı 960 ₺ değil, <b>800 ÷ 0,80 = 1.000 ₺</b>’dir. Çünkü indirim, eski fiyat üzerinden uygulanmıştır.</p>
<div class="formula">Eski fiyat = İndirimli fiyat ÷ (1 − Oran ÷ 100)</div>

<h2 id="cift-indirim">Çift indirim (%20 + %10) nasıl hesaplanır?</h2>
<p>“Kasada ek %10” veya “sepette %20” gibi kampanyalarda ikinci indirim, ilk indirimden sonra kalan fiyata uygulanır. Bu yüzden oranlar toplanmaz. %20 + %10 indirim toplamda <b>%28</b> indirime eşittir: 100 × 0,80 × 0,90 = 72.</p>
<div class="table-wrap"><table><thead><tr><th>Kampanya</th><th>Gerçek toplam indirim</th></tr></thead><tbody>
<tr><td>%10 + %10</td><td>%19</td></tr><tr><td>%20 + %10</td><td>%28</td></tr><tr><td>%30 + %20</td><td>%44</td></tr><tr><td>%50 + %20</td><td>%60</td></tr>
</tbody></table></div>

<h2 id="dikkat">İndirim alışverişinde dikkat edilecekler</h2>
<ul>
<li>Ticaret Bakanlığı’nın Haksız Ticari Uygulamalar Yönetmeliği’ne göre indirim öncesi fiyat, son <b>30 gün</b> içindeki en düşük fiyat olmalıdır. Kampanyadan hemen önce zamlanıp “indirimli” gösterilen ürünlere dikkat edin.</li>
<li>İşletmeler indirimi KDV dahil fiyat üzerinden gösterir. KDV hesabı için <a href="/kdv-hesaplama.html">KDV hesaplama</a> aracını kullanabilirsiniz.</li>
<li>Toptan alımlarda kullanılan ardışık ticari indirimler için <a href="/iskonto-hesaplama.html">iskonto hesaplama</a> aracı daha uygundur.</li>
</ul>
''',
faq=[
('%25 indirim nasıl hesaplanır?','Fiyatı 0,75 ile çarpın. Örneğin 2.000 ₺’lik ürün %25 indirimle 2.000 × 0,75 = 1.500 ₺ olur.'),
('İki fiyat arasındaki indirim yüzdesi nasıl bulunur?','Fiyat farkını eski fiyata bölüp 100 ile çarpın. 500 ₺’den 400 ₺’ye düşen ürün: (500−400)/500×100 = %20.'),
('%50 + %20 indirim %70 mi eder?','Hayır. İkinci indirim kalan fiyata uygulanır: 100 × 0,5 × 0,8 = 40, yani toplam indirim %60’tır.'),
('İndirimli fiyattan orijinal fiyat nasıl bulunur?','İndirimli fiyatı (1 − indirim oranı) değerine bölün. %40 indirimle 600 ₺’ye satılan ürünün eski fiyatı 600 / 0,60 = 1.000 ₺’dir.'),
],
related=['iskonto-hesaplama','yuzde-hesaplama','kar-marji-hesaplama','kdv-hesaplama','kar-zarar-hesaplama'],
))

# ───────────────────────── VERİ KULLANIM ─────────────────────────
TOOLS.append(dict(
slug='veri-kullanim-hesaplama', name='Mobil Veri Kullanım Hesaplama', cat='diger', ico='📶',
title='Veri Kullanım Hesaplayıcı – Aylık Kaç GB İnternet Yeterli? | Hesaplarsın',
desc='1 saat HD video yaklaşık 0,7 GB, 1 saat Instagram/TikTok 0,6 GB harcar. Günlük kullanımınızı girin; aylık kaç GB internet ve hangi paket gerektiğini görün.',
h1='📶 Mobil Veri Kullanım Hesaplama – Kaç GB Yeter?',
lead='Günde ne kadar video izlediğinizi, sosyal medyada vakit geçirdiğinizi ve müzik dinlediğinizi girin; aylık kaç GB internete ihtiyacınız olduğunu görün.',
form='''<p style="font-size:.82rem;color:var(--muted);margin-bottom:12px">Günlük ortalama kullanım sürelerinizi <b>dakika</b> olarak girin (Wi-Fi hariç, yalnızca mobil veri).</p>
<div class="form-grid">
  <div class="field"><label for="video">Video (YouTube, Netflix)</label><input type="number" id="video" placeholder="dk/gün" inputmode="numeric"></div>
  <div class="field"><label for="kalite">Video Kalitesi</label><select id="kalite"><option value="0.3">Düşük (480p)</option><option value="0.7" selected>HD (720p)</option><option value="1.5">Full HD (1080p)</option><option value="3">4K</option></select></div>
  <div class="field"><label for="sosyal">Sosyal medya (Instagram, TikTok)</label><input type="number" id="sosyal" placeholder="dk/gün" inputmode="numeric"></div>
  <div class="field"><label for="muzik">Müzik / Podcast</label><input type="number" id="muzik" placeholder="dk/gün" inputmode="numeric"></div>
  <div class="field"><label for="gorusme">Görüntülü görüşme</label><input type="number" id="gorusme" placeholder="dk/gün" inputmode="numeric"></div>
  <div class="field"><label for="web">Web, e-posta, mesajlaşma</label><input type="number" id="web" placeholder="dk/gün" inputmode="numeric"></div>
  <div class="field"><label for="oyun">Online oyun</label><input type="number" id="oyun" placeholder="dk/gün" inputmode="numeric"></div>
  <div class="field"><label for="harita">Navigasyon / harita</label><input type="number" id="harita" placeholder="dk/gün" inputmode="numeric"></div>
</div>''',
js=r'''
// Saatlik tahmini tüketim (GB/saat)
function hesapla(){
  var k=parseFloat(el('kalite').value);
  var kalemler=[['Video',(v('video')||0)/60*k],['Sosyal medya',(v('sosyal')||0)/60*0.6],['Müzik / podcast',(v('muzik')||0)/60*0.07],
    ['Görüntülü görüşme',(v('gorusme')||0)/60*0.8],['Web ve mesajlaşma',(v('web')||0)/60*0.06],['Online oyun',(v('oyun')||0)/60*0.08],['Navigasyon',(v('harita')||0)/60*0.03]];
  var gun=kalemler.reduce(function(t,x){return t+x[1];},0); if(gun<=0) return 'En az bir kullanım süresi girin.';
  var ay=gun*30, oneri=[5,10,15,20,30,40,50,75,100].find(function(p){return p>=ay*1.1;})||'Sınırsız';
  return {main:['Aylık tahmini ihtiyaç', num(ay,1)+' GB'], sub:'Önerilen paket: <b>'+(typeof oneri==='number'?oneri+' GB':oneri)+'</b> (%10 pay ile)',
    rows:kalemler.filter(function(x){return x[1]>0;}).map(function(x){return [x[0], num(x[1]*30,2)+' GB/ay'];}).concat([['Günlük toplam',num(gun*1000,0)+' MB']]),
    note:'Değerler uygulama ve sıkıştırma ayarlarına göre değişen yaklaşık ortalamalardır.'};
}''',
article='''
<h2 id="kac-gb">Aylık kaç GB internet yeterli?</h2>
<p>Aylık mobil veri ihtiyacı kullanım alışkanlıklarına göre büyük farklılık gösterir. Yalnızca mesajlaşma ve e-posta kullanan biri için 5 GB yeterliyken, her gün bir saat HD video izleyen bir kullanıcı ayda 20 GB’ın üzerine çıkabilir. En büyük veri tüketicisi videodur; ardından sosyal medya (özellikle otomatik oynatılan videolar) ve görüntülü görüşme gelir.</p>
<div class="table-wrap"><table><thead><tr><th>Kullanıcı profili</th><th>Tipik kullanım</th><th>Aylık ihtiyaç</th></tr></thead><tbody>
<tr><td>Hafif</td><td>WhatsApp, e-posta, haber, harita</td><td>3–5 GB</td></tr>
<tr><td>Orta</td><td>Günde 1 saat sosyal medya, müzik</td><td>10–20 GB</td></tr>
<tr><td>Yoğun</td><td>Günlük video, TikTok/Reels, görüntülü görüşme</td><td>30–50 GB</td></tr>
<tr><td>Çok yoğun</td><td>Mobil veriyle dizi/film izleme, hotspot</td><td>75 GB +</td></tr>
</tbody></table></div>

<h2 id="tuketim">Uygulamalar ne kadar internet harcar?</h2>
<p>Aşağıdaki değerler, hesaplayıcının kullandığı saatlik yaklaşık tüketim miktarlarıdır:</p>
<div class="table-wrap"><table><thead><tr><th>Etkinlik</th><th>Saatlik yaklaşık tüketim</th></tr></thead><tbody>
<tr><td>Video – 480p</td><td>~300 MB</td></tr><tr><td>Video – 720p (HD)</td><td>~700 MB</td></tr><tr><td>Video – 1080p (Full HD)</td><td>~1,5 GB</td></tr><tr><td>Video – 4K</td><td>~3 GB ve üzeri</td></tr>
<tr><td>Instagram / TikTok</td><td>~600 MB</td></tr><tr><td>Görüntülü görüşme</td><td>~800 MB</td></tr><tr><td>Müzik akışı (yüksek kalite)</td><td>~70 MB</td></tr>
<tr><td>Web gezintisi, mesajlaşma</td><td>~60 MB</td></tr><tr><td>Online oyun</td><td>~50–100 MB</td></tr><tr><td>Navigasyon</td><td>~30 MB</td></tr>
</tbody></table></div>

<h2 id="tasarruf">Mobil veri kullanımını azaltmanın yolları</h2>
<ul>
<li>Sosyal medya uygulamalarında “veri tasarrufu” modunu açın ve videoların otomatik oynatılmasını kapatın.</li>
<li>YouTube ve Netflix’te mobil veri için video kalitesini 480p ile sınırlandırın; bu tek ayar tüketimi yarıdan fazla azaltır.</li>
<li>Müzik ve dizileri Wi-Fi’dayken çevrimdışı indirin.</li>
<li>Uygulama ve işletim sistemi güncellemelerini yalnızca Wi-Fi’da yapacak şekilde ayarlayın.</li>
<li>Telefon ayarlarındaki “Veri kullanımı” ekranından en çok tüketen uygulamaları kontrol edin.</li>
</ul>
<p>Dosya indirme süresini öğrenmek isterseniz <a href="/dosya-indirme-suresi-hesaplama.html">dosya indirme süresi hesaplama</a>, birim dönüşümleri için <a href="/internet-hizi-donusturucu.html">internet hızı dönüştürücü</a> araçlarına göz atın.</p>
''',
faq=[
('1 GB internet ne kadar gider?','Yaklaşık 1,5 saat HD video, 15 saat müzik dinleme veya 15–20 saat web gezintisi ve mesajlaşma için yeterlidir.'),
('20 GB internet kime yeter?','Günde yaklaşık 30–45 dakika sosyal medya, biraz müzik ve kısa videolar izleyen orta düzey kullanıcılar için genellikle yeterlidir.'),
('WhatsApp ne kadar internet harcar?','Yazılı mesajlaşma çok az veri harcar (saatte birkaç MB). Sesli arama dakikada yaklaşık 0,5–1 MB, görüntülü arama ise dakikada 5–15 MB tüketir.'),
('Hotspot (paylaşım) kullanımı hesaba dahil mi?','Hayır. Bilgisayara internet paylaşıyorsanız yazılım güncellemeleri ve büyük indirmeler nedeniyle tüketim çok artabilir; ihtiyacınızı buna göre yüksek tutun.'),
],
related=['internet-hizi-donusturucu','dosya-indirme-suresi-hesaplama','dosya-boyutu-donusturucu','yuzde-hesaplama','gun-hesaplama'],
))

# ───────────────────────── İNTERNET HIZI ─────────────────────────
TOOLS.append(dict(
slug='internet-hizi-donusturucu', name='İnternet Hızı Dönüştürücü', cat='diger', ico='🚀',
title='Mbps MB/s Dönüştürme – İnternet Hızı Çevirici | Hesaplarsın',
desc='Mbps, MB/s, Kbps, KB/s ve Gbps birimleri arasında internet hızı dönüştürün. 100 Mbps kaç MB/s? Megabit ve megabayt farkını örneklerle öğrenin.',
h1='🚀 İnternet Hızı Dönüştürücü (Mbps ↔ MB/s)',
lead='İnternet sağlayıcınızın verdiği Mbps değerinin gerçek indirme hızında kaç MB/s ettiğini görün. Bit ve bayt cinsinden tüm hız birimlerini birbirine çevirin.',
form='''<div class="form-grid">
  <div class="field"><label for="deger">Hız Değeri</label><input type="number" id="deger" placeholder="örn: 100" inputmode="decimal"></div>
  <div class="field"><label for="birim">Birim</label><select id="birim">
    <option value="1e3">Kbps (kilobit/s)</option><option value="1e6" selected>Mbps (megabit/s)</option><option value="1e9">Gbps (gigabit/s)</option>
    <option value="8e3">KB/s (kilobayt/s)</option><option value="8e6">MB/s (megabayt/s)</option><option value="8e9">GB/s (gigabayt/s)</option></select></div>
</div>
<div class="qtags"><span class="qtag" onclick="el('deger').value=16;el('birim').value='1e6';run()">16 Mbps</span><span class="qtag" onclick="el('deger').value=50;el('birim').value='1e6';run()">50 Mbps</span><span class="qtag" onclick="el('deger').value=100;el('birim').value='1e6';run()">100 Mbps</span><span class="qtag" onclick="el('deger').value=1000;el('birim').value='1e6';run()">1 Gbps</span></div>''',
js=r'''
function hesapla(){
  var x=v('deger'); if(!(x>0)) return 'Bir hız değeri girin.';
  var bps=x*parseFloat(el('birim').value), f=function(n){return n>=100?num(n,0):(n>=1?num(n,2):num(n,4));};
  var gbDk=bps/8e9*60, sure=function(gb){var s=gb*8e9/bps; return s<60?num(s,0)+' sn':(s<3600?num(s/60,1)+' dk':num(s/3600,1)+' saat');};
  return {main:['Gerçek indirme hızı', f(bps/8e6)+' MB/s'], sub:f(bps/1e6)+' Mbps',
    rows:[['Kbps',f(bps/1e3)],['Mbps',f(bps/1e6)],['Gbps',f(bps/1e9)],['KB/s',f(bps/8e3)],['MB/s',f(bps/8e6)],['GB/s',f(bps/8e9)],
      ['Dakikada indirilebilen',num(gbDk,2)+' GB'],['1 GB dosya indirme süresi',sure(1)],['5 GB oyun / film',sure(5)]],
    note:'Gerçek hızlar protokol yükü ve Wi-Fi kayıpları nedeniyle genellikle %5–15 daha düşüktür.'};
}''',
article='''
<h2 id="fark">Mbps ile MB/s arasındaki fark nedir?</h2>
<p>İnternet sağlayıcıları hızı <b>Mbps</b> (megabit/saniye) cinsinden belirtir; indirme programları ve tarayıcılar ise genellikle <b>MB/s</b> (megabayt/saniye) gösterir. 1 bayt 8 bitten oluştuğu için MB/s değeri Mbps değerinin 8’de biridir. Küçük “b” bit, büyük “B” bayt anlamına gelir.</p>
<div class="formula">MB/s = Mbps ÷ 8<br>Mbps = MB/s × 8</div>
<div class="example"><p><b>Örnek:</b> 100 Mbps fiber bağlantı ile ideal koşullarda 100 ÷ 8 = <b>12,5 MB/s</b> indirme hızı elde edilir. 1 GB’lık bir dosya yaklaşık 80 saniyede iner.</p></div>

<h2 id="tablo">İnternet hızı dönüşüm tablosu</h2>
<div class="table-wrap"><table><thead><tr><th>Paket hızı</th><th>MB/s karşılığı</th><th>1 GB indirme süresi</th></tr></thead><tbody>
<tr><td>8 Mbps</td><td>1 MB/s</td><td>~17 dk</td></tr><tr><td>16 Mbps</td><td>2 MB/s</td><td>~8,3 dk</td></tr><tr><td>25 Mbps</td><td>3,1 MB/s</td><td>~5,3 dk</td></tr>
<tr><td>50 Mbps</td><td>6,25 MB/s</td><td>~2,7 dk</td></tr><tr><td>100 Mbps</td><td>12,5 MB/s</td><td>~80 sn</td></tr><tr><td>200 Mbps</td><td>25 MB/s</td><td>~40 sn</td></tr>
<tr><td>500 Mbps</td><td>62,5 MB/s</td><td>~16 sn</td></tr><tr><td>1000 Mbps (1 Gbps)</td><td>125 MB/s</td><td>~8 sn</td></tr>
</tbody></table></div>

<h2 id="neden-dusuk">İnternet hızım neden paket hızından düşük?</h2>
<ul>
<li><b>Bit-bayt farkı:</b> En yaygın yanlış anlama; 100 Mbps paket 100 MB/s değil 12,5 MB/s’tir.</li>
<li><b>Wi-Fi:</b> Modem uzaklığı, duvarlar ve 2,4 GHz bandı hızı ciddi düşürür. Ölçümü kabloyla yapın.</li>
<li><b>Protokol yükü:</b> TCP/IP başlıkları nedeniyle verinin bir kısmı kontrol bilgisine harcanır.</li>
<li><b>Karşı sunucu:</b> İndirdiğiniz sitenin sunucusu yavaşsa sizin hızınız fark etmez.</li>
<li><b>Altyapı:</b> VDSL hatlarda santrale uzaklık, fiberde bina içi kablolama hızı sınırlar.</li>
</ul>

<h2 id="ihtiyac">Hangi hız kime yeter?</h2>
<p>Tek kişi için web, sosyal medya ve HD video 16–25 Mbps ile rahat karşılanır. Aynı anda birkaç cihazda 4K yayın, online oyun ve görüntülü toplantı yapılan evlerde 100 Mbps ve üzeri tercih edilmelidir. Aylık mobil veri ihtiyacınızı <a href="/veri-kullanim-hesaplama.html">veri kullanım hesaplama</a> aracıyla bulabilirsiniz.</p>
''',
faq=[
('100 Mbps kaç MB/s eder?','100 Mbps = 100 ÷ 8 = 12,5 MB/s’tir. Gerçek kullanımda bu değer genellikle 11–12 MB/s civarında ölçülür.'),
('1 Gbps kaç MB/s?','1 Gbps = 1000 Mbps = 125 MB/s’tir.'),
('MB ile Mb aynı şey mi?','Hayır. MB (megabayt) dosya boyutu, Mb (megabit) veri aktarım hızı için kullanılır. 1 MB = 8 Mb’dir.'),
('İndirme hızı mı yükleme hızı mı önemli?','Video izleme ve dosya indirme için indirme (download), video yayını, bulut yedekleme ve görüntülü görüşme için yükleme (upload) hızı önemlidir.'),
],
related=['dosya-indirme-suresi-hesaplama','dosya-boyutu-donusturucu','veri-kullanim-hesaplama','yuzde-hesaplama','ortalama-hesaplama'],
))

# ───────────────────────── YAKIT TÜKETİMİ ─────────────────────────
TOOLS.append(dict(
slug='yakit-tuketimi-hesaplama', name='Yakıt Tüketimi Hesaplama', cat='arac', ico='⛽',
title='Yakıt Tüketimi Hesaplama – 100 km’de Kaç Litre Yakar? | Hesaplarsın',
desc='Aldığınız yakıt ve gittiğiniz kilometreye göre aracınızın 100 km’de kaç litre yaktığını, km başına maliyetini ve depoyla kaç km gidebileceğinizi hesaplayın.',
h1='⛽ Yakıt Tüketimi Hesaplama – Arabam 100 km’de Kaç Yakar?',
lead='Depoyu doldurduktan sonra gittiğiniz mesafeyi ve aldığınız litreyi girin; aracınızın gerçek ortalama tüketimini, km başına yakıt maliyetini ve menzilini öğrenin.',
form='''<div class="form-grid">
  <div class="field"><label for="km">Gidilen Mesafe (km)</label><input type="number" id="km" placeholder="örn: 520" inputmode="decimal"></div>
  <div class="field"><label for="litre">Kullanılan Yakıt (litre)</label><input type="number" id="litre" placeholder="örn: 34,5" inputmode="decimal"></div>
  <div class="field"><label for="fiyat">Litre Fiyatı (₺) <small>isteğe bağlı</small></label><input type="number" id="fiyat" placeholder="örn: 47,50" inputmode="decimal"></div>
  <div class="field"><label for="depo">Depo Hacmi (litre) <small>isteğe bağlı</small></label><input type="number" id="depo" placeholder="örn: 50" inputmode="decimal"></div>
</div>''',
js=r'''
function hesapla(){
  var km=v('km'), l=v('litre'), f=v('fiyat'), d=v('depo'); if(!(km>0)||!(l>0)) return 'Mesafe ve kullanılan yakıtı girin.';
  var t=l/km*100, rows=[['Kilometre başına yakıt',num(l/km,3)+' litre'],['1 litreyle gidilen yol',num(km/l,2)+' km']];
  if(f>0){rows.push(['Toplam yakıt maliyeti',tl(l*f)]);rows.push(['Km başına maliyet',tl(l*f/km)]);rows.push(['100 km maliyeti',tl(t*f),'hl']);}
  if(d>0) rows.push(['Tam depo menzili',num(d/t*100,0)+' km']);
  var yorum=t<5?'Çok ekonomik':t<7?'Ekonomik':t<9?'Ortalama':t<12?'Yüksek':'Çok yüksek';
  return {main:['Ortalama tüketim', num(t,2)+' L / 100 km'], sub:'Değerlendirme: '+yorum, rows:rows};
}''',
article='''
<h2 id="nasil">Yakıt tüketimi nasıl hesaplanır?</h2>
<p>Gerçek yakıt tüketimini ölçmenin en güvenilir yolu “depo doldur–depo doldur” yöntemidir. Depoyu tamamen doldurun ve kilometre sayacını (tripmetre) sıfırlayın. Bir sonraki tam doldurmada pompa ekranında görünen litre miktarını ve tripmetredeki kilometreyi not edin. Bu iki değer hesaplayıcıya girildiğinde aracınızın gerçek ortalama tüketimi ortaya çıkar.</p>
<div class="formula">100 km’de tüketim (L) = Kullanılan yakıt (L) ÷ Gidilen yol (km) × 100</div>
<div class="example"><p><b>Örnek:</b> 520 km yolda 34,5 litre yakıt kullanıldıysa:</p><p>34,5 ÷ 520 × 100 = <b>6,63 L/100 km</b>. Litre fiyatı 47,50 ₺ ise 100 km’nin maliyeti 6,63 × 47,50 ≈ <b>315 ₺</b>’dir.</p></div>

<h2 id="normal">Bir araba 100 km’de kaç litre yakmalı?</h2>
<div class="table-wrap"><table><thead><tr><th>Araç tipi</th><th>Şehir içi</th><th>Şehir dışı</th></tr></thead><tbody>
<tr><td>Küçük benzinli (1.0–1.4)</td><td>6–8 L</td><td>4,5–5,5 L</td></tr>
<tr><td>Orta sınıf dizel (1.5–1.6)</td><td>5–6,5 L</td><td>3,8–4,8 L</td></tr>
<tr><td>Orta sınıf benzinli (1.5–1.6)</td><td>7–9 L</td><td>5–6 L</td></tr>
<tr><td>SUV (benzinli)</td><td>9–12 L</td><td>6,5–8 L</td></tr>
<tr><td>Hibrit</td><td>4–5 L</td><td>4,5–5,5 L</td></tr>
<tr><td>LPG (litre)</td><td>Benzine göre ~%20–25 fazla litre</td><td></td></tr>
</tbody></table></div>
<p>Değerler genel ortalamalardır; aynı model araç bile sürüş tarzına göre %20’ye varan fark gösterebilir.</p>

<h2 id="etkenler">Yakıt tüketimini artıran faktörler</h2>
<ul>
<li><b>Hız:</b> 90 km/s’nin üzerinde hava direnci hızla artar; 130 km/s’de tüketim 90 km/s’ye göre %25–30 yükselebilir.</li>
<li><b>Sert hızlanma ve frenleme:</b> Trafikte ani kalkışlar tüketimi belirgin şekilde artırır.</li>
<li><b>Lastik basıncı:</b> Düşük basınç yuvarlanma direncini artırır; ayda bir kontrol edin.</li>
<li><b>Klima ve yük:</b> Klima %5–10, tavan bagajı ve fazla yük de ek tüketim getirir.</li>
<li><b>Kısa mesafeler ve rölanti:</b> Motor ısınmadan yapılan kısa yolculuklar ve uzun rölantiler verimsizdir.</li>
<li><b>Bakım:</b> Kirli hava filtresi, eski buji ve yanlış motor yağı tüketimi yükseltir.</li>
</ul>

<h2 id="devir">Düşük tüketim için hangi devirde gidilmeli?</h2>
<p>Benzinli araçlarda genellikle 2.000–2.500, dizel araçlarda 1.500–2.000 devir aralığı en verimli bölgedir. Mümkün olan en yüksek vitesi kullanmak, ani gaz yerine kademeli hızlanmak ve trafiği önceden okuyup motor freni ile yavaşlamak en etkili tasarruf yöntemleridir.</p>
<p>Planladığınız bir yolculuğun toplam yakıt masrafını hesaplamak için <a href="/yakit-maliyeti-hesaplama.html">yakıt maliyeti hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('Arabamın kaç yaktığını nasıl öğrenirim?','Depoyu fulleyip tripmetreyi sıfırlayın, bir sonraki fullemede aldığınız litreyi ve gittiğiniz km’yi hesaplayıcıya girin. Araç bilgisayarındaki değer genellikle %5–10 iyimser gösterir.'),
('100 km’de 7 litre yakmak çok mu?','Orta sınıf benzinli bir araç için şehir içinde normal, uzun yolda ise biraz yüksek sayılır. Dizel bir araç için ortalamanın üzerindedir.'),
('Klima yakıt tüketimini ne kadar artırır?','Şehir içinde yaklaşık %5–10 artış yapabilir. Otoyolda ise camları açmak hava direncini artırdığından klima çoğu zaman daha verimlidir.'),
('Km başına yakıt maliyeti nasıl hesaplanır?','Toplam yakıt tutarını gidilen kilometreye bölün. Hesaplayıcıya litre fiyatını girerseniz km ve 100 km maliyeti otomatik gösterilir.'),
],
related=['yakit-maliyeti-hesaplama','arac-kredisi-hesaplama','mtv-hesaplama','arac-deger-kaybi-hesaplama','arac-muayene-gecikme-hesaplama'],
))

# ───────────────────────── YAKIT MALİYETİ ─────────────────────────
TOOLS.append(dict(
slug='yakit-maliyeti-hesaplama', name='Yakıt Maliyeti Hesaplama', cat='arac', ico='🛣️',
title='Yol Masrafı Hesaplama – Yakıt Maliyeti, Kişi Başı Pay | Hesaplarsın',
desc='Gideceğiniz mesafe, aracınızın 100 km tüketimi ve yakıt fiyatına göre yolculuk yakıt masrafını, gidiş-dönüş tutarını ve kişi başı payı hesaplayın.',
h1='🛣️ Yakıt Maliyeti Hesaplama – Yol Masrafı Ne Kadar?',
lead='İstanbul–Ankara arası benzin kaç para tutar? Mesafeyi, aracınızın tüketimini ve yakıt fiyatını girin; gidiş-dönüş masrafınızı ve kişi başı payı görün.',
form='''<div class="form-grid">
  <div class="field"><label for="km">Mesafe (km)</label><input type="number" id="km" placeholder="örn: 450" inputmode="decimal">
   <div class="qtags"><span class="qtag" onclick="el('km').value=450">İst–Ank ~450</span><span class="qtag" onclick="el('km').value=155">Bursa–İst ~155</span><span class="qtag" onclick="el('km').value=330">Bursa–İzmir ~330</span></div></div>
  <div class="field"><label for="tuketim">Tüketim (L / 100 km)</label><input type="number" id="tuketim" placeholder="örn: 6,5" inputmode="decimal"></div>
  <div class="field"><label for="fiyat">Yakıt Litre Fiyatı (₺)</label><input type="number" id="fiyat" placeholder="örn: 47,50" inputmode="decimal"></div>
  <div class="field"><label for="kisi">Kişi Sayısı</label><input type="number" id="kisi" value="1" min="1" inputmode="numeric"></div>
  <div class="field"><label for="otoyol">Otoyol / köprü ücreti (₺) <small>isteğe bağlı</small></label><input type="number" id="otoyol" placeholder="tek yön" inputmode="decimal"></div>
  <div class="field" style="justify-content:flex-end"><label class="chk"><input type="checkbox" id="gd"> Gidiş-dönüş hesapla</label></div>
</div>''',
js=r'''
function hesapla(){
  var km=v('km'), t=v('tuketim'), f=v('fiyat'), k=Math.max(1,Math.round(v('kisi')||1)), o=v('otoyol')||0, c=checked('gd')?2:1;
  if(!(km>0)||!(t>0)||!(f>0)) return 'Mesafe, tüketim ve yakıt fiyatını girin.';
  var L=km*c*t/100, y=L*f, top=y+o*c;
  return {main:['Toplam yol masrafı', tl(top)], sub:(c===2?'Gidiş-dönüş ':'Tek yön ')+num(km*c,0)+' km',
    rows:[['Gereken yakıt',num(L,2)+' litre'],['Yakıt maliyeti',tl(y)],['Otoyol / köprü',tl(o*c)],['Km başına maliyet',tl(top/(km*c))],['Kişi başı pay ('+k+' kişi)',tl(top/k),'hl']]};
}''',
article='''
<h2 id="nasil">Yol masrafı nasıl hesaplanır?</h2>
<p>Bir yolculuğun yakıt masrafını bulmak için üç bilgi yeterlidir: gidilecek mesafe, aracın 100 km’de yaktığı litre ve yakıtın litre fiyatı. Önce gereken toplam litre bulunur, ardından litre fiyatıyla çarpılır.</p>
<div class="formula">Gereken yakıt (L) = Mesafe (km) × Tüketim (L/100 km) ÷ 100<br>Yakıt masrafı (₺) = Gereken yakıt × Litre fiyatı</div>
<div class="example"><p><b>Örnek:</b> 450 km’lik yolda 100 km’de 6,5 litre yakan araç, litresi 47,50 ₺ olan yakıtla:</p><p>450 × 6,5 ÷ 100 = 29,25 litre → 29,25 × 47,50 = <b>1.389,38 ₺</b>. Gidiş-dönüş yaklaşık 2.779 ₺, 3 kişiye bölündüğünde kişi başı ~926 ₺.</p></div>

<h2 id="mesafeler">Popüler güzergâhların yaklaşık mesafeleri</h2>
<div class="table-wrap"><table><thead><tr><th>Güzergâh</th><th>Yaklaşık mesafe</th></tr></thead><tbody>
<tr><td>İstanbul – Ankara</td><td>450 km</td></tr><tr><td>İstanbul – İzmir (otoyol)</td><td>480 km</td></tr><tr><td>Bursa – İstanbul (Osmangazi Köprüsü)</td><td>155 km</td></tr>
<tr><td>Bursa – İzmir</td><td>330 km</td></tr><tr><td>Ankara – Antalya</td><td>480 km</td></tr><tr><td>İstanbul – Antalya</td><td>700 km</td></tr>
</tbody></table></div>
<p>Mesafeler güzergâha göre değişir; kesin değeri navigasyon uygulamanızdan alabilirsiniz.</p>

<h2 id="tuketim">Aracımın tüketimini bilmiyorsam ne yapmalıyım?</h2>
<p>Araç bilgisayarındaki ortalama değeri kullanabilir ya da daha doğrusu <a href="/yakit-tuketimi-hesaplama.html">yakıt tüketimi hesaplama</a> aracıyla gerçek tüketiminizi ölçebilirsiniz. Uzun yol (otoyol) tüketimi, şehir içi tüketimden genellikle %20–30 düşüktür; hesabı otoyol ağırlıklı bir yolculuk için yapıyorsanız şehir dışı değerini girin.</p>

<h2 id="ek-masraf">Yolculukta yakıt dışındaki masraflar</h2>
<ul>
<li><b>Otoyol ve köprü geçişleri:</b> Osmangazi, Yavuz Sultan Selim, Çanakkale 1915 köprüleri ve otoyollar toplam maliyeti önemli ölçüde artırabilir. Güncel ücretleri KGM ve işletmeci sitelerinden kontrol edin.</li>
<li><b>Lastik ve bakım payı:</b> Uzun yolculuklarda km başına yıpranma payı da göz önünde bulundurulmalıdır.</li>
<li><b>Otopark:</b> Şehir merkezlerinde otopark ücreti eklenebilir.</li>
</ul>
<p>Yakıt fiyatları EPDK ve dağıtım şirketlerince sık güncellenir; hesaplamada pompa fiyatını girmeniz en doğru sonucu verir.</p>
''',
faq=[
('İstanbul–Ankara arası benzin kaç para?','Yaklaşık 450 km’dir. 100 km’de 7 litre yakan bir araçla 31,5 litre yakıt gerekir; bunu güncel litre fiyatıyla çarparak tutarı bulabilirsiniz.'),
('Yol masrafı kişi başı nasıl bölünür?','Yakıt ve otoyol ücretlerinin toplamı yolcu sayısına bölünür. Hesaplayıcıya kişi sayısını girdiğinizde kişi başı pay otomatik hesaplanır.'),
('LPG’li araç için nasıl hesaplarım?','LPG tüketimini (L/100 km) ve LPG litre fiyatını girin. LPG’li araçlar benzine göre litre olarak daha fazla tüketir ancak litre fiyatı daha düşüktür.'),
('Elektrikli araçlar için hesaplama yapılabilir mi?','Bu araç litre bazlıdır. Elektrikli araçlarda 100 km’de tüketilen kWh ile şarj kWh fiyatını çarparak benzer bir hesap yapabilirsiniz.'),
],
related=['yakit-tuketimi-hesaplama','arac-kredisi-hesaplama','mtv-hesaplama','arac-deger-kaybi-hesaplama','yuzde-hesaplama'],
))


# ───────────────────────── DESİ ─────────────────────────
import math as _m
def _dtr(x, d=2):
    s = f'{x:,.{d}f}'; return s.replace(',', 'X').replace('.', ',').replace('X', '.')
_DK = [('Küçük kutu (ayakkabı kutusu)', 30, 20, 12), ('Orta boy koli', 40, 30, 20), ('Büyük koli', 50, 40, 30), ('Taşınma kolisi', 60, 40, 40), ('Bavul boyutu', 75, 50, 30), ('Çok büyük koli', 80, 60, 50)]
rows = ''.join(f'<tr><td>{a}</td><td>{e} × {b} × {y} cm</td><td>{_dtr(e*b*y/3000)}</td><td>{_m.ceil(e*b*y/3000-1e-9)}</td></tr>' for a, e, b, y in _DK)
TOOLS.append(dict(
slug='desi-hesaplama', name='Desi Hesaplama', cat='isletme', ico='📦',
title='Desi Hesaplama – Kargo Desi Nasıl Hesaplanır? (÷ 3000) | Hesaplarsın',
desc='Kargo desi hesaplama: paketin en, boy ve yüksekliğini girin, desi ve ücrete esas ağırlığı anında görün. 40×30×20 cm koli 8 desidir. Yurt içi 3000, yurt dışı 5000 bölen.',
h1='📦 Desi Hesaplama – Kargo Desi ve Ücrete Esas Ağırlık',
lead='Paketinizin en, boy ve yükseklik ölçülerini santimetre olarak, isterseniz gerçek ağırlığını da girin; kargo firmalarının fiyatlandırmada kullandığı desiyi ve desi ile kilogramdan hangisinin esas alınacağını görün.',
card_title='Kargo Desi Hesaplayıcı', button='Desiyi Hesapla',
form='''<div class="form-grid">
  <div class="field"><label for="en">En (cm)</label><input type="number" id="en" placeholder="örn: 40" inputmode="decimal"></div>
  <div class="field"><label for="boy">Boy (cm)</label><input type="number" id="boy" placeholder="örn: 30" inputmode="decimal"></div>
  <div class="field"><label for="yuk">Yükseklik (cm)</label><input type="number" id="yuk" placeholder="örn: 20" inputmode="decimal"></div>
  <div class="field"><label for="kg">Gerçek ağırlık (kg) <small>isteğe bağlı</small></label><input type="number" id="kg" placeholder="örn: 5" inputmode="decimal"></div>
  <div class="field"><label for="adet">Paket adedi</label><input type="number" id="adet" value="1" inputmode="numeric"></div>
  <div class="field"><label for="bolen">Gönderi türü</label><select id="bolen"><option value="3000" selected>Yurt içi kargo (÷ 3000)</option><option value="5000">Uluslararası ekspres (÷ 5000)</option><option value="6000">Hava kargo – IATA (÷ 6000)</option></select></div>
</div>''',
js=r'''
function hesapla(){
  var e=v('en'), b=v('boy'), y=v('yuk'), kg=v('kg')||0, n=Math.max(1,Math.round(v('adet')||1)), bol=parseFloat(el('bolen').value);
  if(!(e>0&&b>0&&y>0)) return 'Paketin en, boy ve yükseklik ölçülerini girin.';
  var d=e*b*y/bol, dy=Math.ceil(d-1e-9), esas=Math.max(d,kg), hangi=kg>d?'gerçek ağırlık (kg)':'desi';
  var rows=[['Hacim',num(e*b*y,0)+' cm³'],['Desi (tam değer)',num(d,2)],['Desi (üste yuvarlanmış)',num(dy,0)],
    ['Gerçek ağırlık',kg?num(kg,2)+' kg':'girilmedi'],['Ücrete esas ağırlık (paket başı)',num(esas,2)+(kg>d?' kg':' desi'),'hl']];
  if(n>1) rows.push(['Toplam ('+n+' paket)',num(esas*n,2)+(kg>d?' kg':' desi')]);
  return {main:['Paketin desisi', num(d,2)+' desi'], sub:'Ücretlendirmede <b>'+hangi+'</b> esas alınır'+(n>1?' · '+n+' paket toplam '+num(esas*n,2):''), rows:rows,
    note:'Desi = En × Boy × Yükseklik (cm) ÷ '+bol+'. Kargo firmaları desi ile kilogramdan büyük olanı fiyatlandırır; çoğu firma küsuratlı desiyi bir üst tam sayıya yuvarlar. Kesin desi ve ücret için gönderi yapacağınız firmanın tarifesine bakın.'};
}''',
article=f'''<h2 id="nedir">Desi nedir?</h2>
<p>Desi, kargo gönderilerinde paketin kapladığı hacmi ağırlık cinsinden ifade eden birimdir. Kargo araçlarında yer, ağırlık kadar değerlidir: büyük ama hafif bir koli, küçük ama ağır bir paket kadar alan kaplar. Bu yüzden kargo firmaları paketin <b>gerçek ağırlığı (kg)</b> ile <b>desisini</b> karşılaştırır ve hangisi büyükse ücreti ona göre belirler. Fiyatlandırmada 1 desi, 1 kilogram gibi değerlendirilir.</p>

<h2 id="formul">Desi nasıl hesaplanır?</h2>
<div class="formula">Desi = En (cm) × Boy (cm) × Yükseklik (cm) ÷ 3000</div>
<p>Türkiye’de yurt içi kargo firmaları desiyi 3000’e bölerek hesaplar. Uluslararası ekspres kargoda bölen genellikle 5000, hava kargoda ise IATA standardı olan 6000’dir; bölen büyüdükçe aynı paketin desisi küçülür.</p>
<div class="example"><p><b>Örnek:</b> 40 × 30 × 20 cm ölçülerindeki bir koli: 40 × 30 × 20 = 24.000 cm³; 24.000 ÷ 3000 = <b>8 desi</b>. Koli 5 kg geliyorsa ücret 8 desi üzerinden, 12 kg geliyorsa 12 kg üzerinden hesaplanır.</p></div>

<h2 id="tablo">Koli ölçülerine göre desi tablosu</h2>
<div class="table-wrap"><table><thead><tr><th>Paket</th><th>Ölçü</th><th>Desi</th><th>Üste yuvarlanmış</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Tablo yurt içi kargo için 3000 bölenle hesaplanmıştır. Ölçüler paketin en dış noktalarından, ambalaj dahil alınmalıdır.</p>

<h2 id="kg">Desi mi, kilogram mı? Hangisi esas alınır?</h2>
<p>Kargo ücreti her zaman desi ile gerçek ağırlıktan <b>büyük olana</b> göre belirlenir. Yastık, battaniye, oyuncak gibi hafif ama hacimli ürünlerde desi; kitap, alet, sıvı gibi küçük ama ağır ürünlerde kilogram belirleyicidir. Örneğin 60 × 40 × 40 cm’lik bir yorgan kolisi yalnızca 4 kg gelse de 32 desi üzerinden ücretlendirilir.</p>

<h2 id="dusurme">Desiyi düşürmenin yolları</h2>
<ul>
<li><b>Ürüne uygun koli seçin:</b> Gereğinden büyük koli, boşluğu dolduran malzemeyle birlikte desiyi gereksiz yere artırır.</li>
<li><b>Vakumlu poşet kullanın:</b> Tekstil ürünlerinde hacmi yarıya kadar düşürebilir.</li>
<li><b>Yüksekliği azaltın:</b> Üç ölçü çarpıldığı için tek bir kenarı 10 cm kısaltmak bile desiyi belirgin şekilde düşürür.</li>
<li><b>Pazaryeri anlaşmalarını kontrol edin:</b> Trendyol ve Hepsiburada gibi pazaryerleri satıcılar için desi aralıklarına göre anlaşmalı kargo fiyatları uygular; ürünün desi aralığını bilmek kâr hesabını doğrudan etkiler.</li>
</ul>
<p>Satış başına elinize kalan tutarı kargo dahil görmek için <a href="/pazaryeri-komisyon-hesaplama.html">pazaryeri komisyon hesaplama</a> ve <a href="/kar-marji-hesaplama.html">kâr marjı hesaplama</a> araçlarını kullanabilirsiniz.</p>''',
faq=[('1 desi kaç kg?', 'Kargo fiyatlandırmasında 1 desi 1 kilogram gibi değerlendirilir. Paketin desisi ile gerçek ağırlığı karşılaştırılır ve büyük olan ücrete esas alınır.'),
     ('Desi hesaplama formülü nedir?', 'Yurt içi kargoda desi = en × boy × yükseklik (cm) ÷ 3000’dir. Uluslararası ekspres kargoda genellikle 5000, hava kargoda 6000 bölen kullanılır.'),
     ('40x30x20 koli kaç desi?', '40 × 30 × 20 = 24.000 cm³; 24.000 ÷ 3000 = 8 desidir.'),
     ('Desi küsuratlı çıkarsa ne olur?', 'Çoğu kargo firması küsuratlı desiyi bir üst tam sayıya yuvarlar; örneğin 7,2 desi 8 desi olarak fiyatlandırılabilir. Yuvarlama kuralı firmadan firmaya değişebilir.'),
     ('Zarf gönderilerinde desi hesaplanır mı?', 'Evrak ve dosya gönderileri genellikle desi yerine sabit “dosya/zarf” tarifesiyle ücretlendirilir. Zarfın içine kalın ürün konduğunda koli tarifesine geçilebilir.')],
related=['pazaryeri-komisyon-hesaplama', 'trendyol-komisyon-hesaplama', 'hepsiburada-komisyon-hesaplama', 'kar-marji-hesaplama', 'kar-zarar-hesaplama'],
sources=[('IATA – hacimsel ağırlık (6000 cm³/kg) standardı', 'https://www.iata.org/')],
badges=['✓ Ücretsiz', 'Yurt içi ÷3000', 'Yurt dışı ÷5000'],
))

# ───────────────────────── TAKSİ ÜCRETİ ─────────────────────────
# İstanbul: İBB Meclisi, 20.07.2026'dan itibaren (BirGün 16.09.2026, Sabah 19.07.2026). Ankara: 01.03.2026'dan itibaren (Cumhuriyet).
TAKSI = [  # anahtar, ad, açılış, km, dakika, minimum
    ('ist_sari', 'İstanbul – sarı taksi', 71.94, 47.92, 9.98, 230),
    ('ist_d', 'İstanbul – D segment / elektrikli', 82.73, 55.10, 11.47, 265),
    ('ist_donusum', 'İstanbul – UKOME dönüşümlü', 93.52, 62.29, 12.97, 300),
    ('ist_lux', 'İstanbul – lüks taksi', 122.30, 81.46, 16.96, 400),
    ('ankara', 'Ankara', 65.0, 40.0, 7.0, 200),
]
def _t2(x):
    return f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
TAKSI_TARIFE = ('<div class="table-wrap"><table><thead><tr><th>Şehir / sınıf</th><th>Açılış</th><th>Km başı</th><th>Dakika başı</th><th>İndi-bindi (en az)</th></tr></thead><tbody>'
    + ''.join(f'<tr><td>{ad}</td><td>{_t2(a)} ₺</td><td>{_t2(k)} ₺</td><td>{_t2(d)} ₺</td><td>{_t2(m)} ₺</td></tr>' for _, ad, a, k, d, m in TAKSI) + '</tbody></table></div>')
TAKSI_ORNEK = ('<div class="table-wrap"><table><thead><tr><th>Mesafe</th><th>İstanbul sarı taksi</th><th>Ankara</th></tr></thead><tbody>'
    + ''.join(f'<tr><td>{km} km</td>' + ''.join(f'<td>{_t2(max(m, a + k * km))} ₺</td>' for key, _, a, k, d, m in TAKSI if key in ('ist_sari', 'ankara')) + '</tr>' for km in (2, 5, 10, 15, 20, 30, 40, 50))
    + '</tbody></table></div>')
TOOLS.append(dict(
slug='taksi-ucreti-hesaplama', name='Taksi Ücreti Hesaplama', cat='arac', ico='🚕',
title='Taksi Ücreti Hesaplama 2026 – İstanbul, Ankara Taksimetre | Hesaplarsın',
desc=f'Taksi ücreti hesaplama: mesafe ve bekleme süresini girin, güncel tarifeyle ödeyeceğiniz tutarı görün. İstanbul sarı taksi açılış {_t2(71.94)} ₺, km {_t2(47.92)} ₺; 10 km yaklaşık {_t2(71.94 + 479.2)} ₺.',
h1='🚕 Taksi Ücreti Hesaplama – Güncel Taksimetre Tarifesi',
lead='Şehri ve taksi sınıfını seçin, gideceğiniz mesafeyi ve trafikte bekleme süresini girin; güncel resmî tarifeyle taksimetrenin yazacağı tutarı görün. Diğer şehirler için açılış, km ve dakika ücretini kendiniz girebilirsiniz.',
card_title='Taksimetre Hesaplayıcı', button='Ücreti Hesapla',
form='''<div class="form-grid">
  <div class="field full"><label for="tarife">Şehir / taksi sınıfı</label><select id="tarife">''' + ''.join(f'<option value="{k}">{ad}</option>' for k, ad, *_ in TAKSI) + '''<option value="ozel">Diğer şehir – tarifeyi kendim gireceğim</option></select></div>
  <div class="field"><label for="km">Mesafe (km)</label><input type="number" id="km" placeholder="örn: 10" inputmode="decimal"></div>
  <div class="field"><label for="dk">Trafikte bekleme / yavaş gidiş <small>dakika</small></label><input type="number" id="dk" placeholder="örn: 5" inputmode="decimal"></div>
  <div class="field"><label for="kisi">Kişi sayısı <small>ücreti bölmek için</small></label><input type="number" id="kisi" value="1" inputmode="numeric"></div>
  <div class="field"><label for="acilis">Açılış ücreti (₺) <small>diğer şehir</small></label><input type="number" id="acilis" inputmode="decimal"></div>
  <div class="field"><label for="kmu">Km ücreti (₺) <small>diğer şehir</small></label><input type="number" id="kmu" inputmode="decimal"></div>
  <div class="field"><label for="dku">Dakika ücreti (₺) <small>diğer şehir</small></label><input type="number" id="dku" inputmode="decimal"></div>
  <div class="field"><label for="min">İndi-bindi / en az ücret (₺) <small>diğer şehir</small></label><input type="number" id="min" inputmode="decimal"></div>
</div>''',
js='var TK=' + str({k: [ad, a, km, d, m] for k, ad, a, km, d, m in TAKSI}).replace("'", '"') + ';' + r'''
function hesapla(){
  var s=el('tarife').value, km=v('km'), dk=v('dk')||0, n=Math.max(1,Math.round(v('kisi')||1)), t;
  if(!(km>0)) return 'Gideceğiniz mesafeyi km olarak girin.';
  if(s==='ozel'){ t=['Girdiğiniz tarife', v('acilis')||0, v('kmu'), v('dku')||0, v('min')||0]; if(!(t[2]>0)) return 'Diğer şehir için en az km ücretini girin (taksimetre tarifesi şehrinizin belediyesinden öğrenilebilir).'; }
  else t=TK[s];
  var mesafe=km*t[2], zaman=dk*t[3], top=t[1]+mesafe+zaman, minU=top<t[4];
  if(minU) top=t[4];
  var rows=[['Açılış',tl(t[1])],['Mesafe ('+num(km,1)+' km × '+tl(t[2])+')',tl(mesafe)]];
  if(dk>0) rows.push(['Bekleme ('+num(dk,0)+' dk × '+tl(t[3])+')',tl(zaman)]);
  if(minU) rows.push(['İndi-bindi (en az ücret) uygulandı',tl(t[4]),'hl']);
  if(n>1) rows.push(['Kişi başı ('+n+' kişi)',tl(top/n),'hl']);
  return {main:['Tahmini taksi ücreti', tl(top)], sub:t[0]+' · '+num(km,1)+' km'+(dk>0?' + '+num(dk,0)+' dk bekleme':''), rows:rows,
    note:'Taksimetre araç hareket ederken mesafeye, dururken ya da çok yavaş giderken zamana göre işler; bekleme süresini trafikte durduğunuz toplam süre olarak girin. Köprü, tünel ve otoyol geçiş ücretleri tutara dahil değildir ve yolcu tarafından ayrıca ödenir.'};
}''',
article=f'''<h2 id="tarife">Güncel taksi tarifeleri</h2>
{TAKSI_TARIFE}
<p>İstanbul tarifesi İstanbul Büyükşehir Belediyesi kararıyla 20 Temmuz 2026’dan, Ankara tarifesi 1 Mart 2026’dan beri uygulanıyor. Taksi ücretleri yılda bir veya iki kez güncellenir; yeni tarife açıklandığında tabloyu güncelliyoruz.</p>

<h2 id="nasil">Taksi ücreti nasıl hesaplanır?</h2>
<div class="formula">Taksi ücreti = Açılış + (Km × km ücreti) + (Bekleme dakikası × dakika ücreti)</div>
<p>Taksimetre biner binmez açılış ücretini yazar. Araç hareket ettikçe mesafe ücreti, trafikte durduğunda veya çok yavaş ilerlediğinde zaman ücreti işler. Hesaplanan tutar şehrin <b>indi-bindi (en az) ücretinin</b> altında kalırsa en az ücret ödenir; İstanbul’da sarı taksiyle 1–2 km’lik kısa yolculuklar bu yüzden 230 ₺ tutar.</p>
<div class="example"><p><b>Örnek:</b> İstanbul’da sarı taksiyle 10 km yol ve trafikte toplam 8 dakika bekleme: 71,94 + (10 × 47,92) + (8 × 9,98) = <b>{_t2(71.94 + 479.2 + 79.84)} ₺</b>.</p></div>

<h2 id="km">Kilometreye göre taksi ücreti tablosu</h2>
<p>Bekleme olmadan, yalnızca mesafeye göre yaklaşık tutarlar:</p>
{TAKSI_ORNEK}
<p>Yoğun trafikte bekleme süresi tutarı belirgin şekilde artırır. İstanbul sarı taksi için her 10 dakikalık bekleme yaklaşık 100 ₺ ekler.</p>

<h2 id="ipucu">Taksi ücretini etkileyen diğer kalemler</h2>
<ul>
<li><b>Köprü, tünel ve otoyol:</b> Geçiş ücretleri taksimetreye dahil değildir; yolcu ayrıca öder.</li>
<li><b>Taksi sınıfı:</b> İstanbul’da D segment, elektrikli, dönüşümlü ve lüks taksilerin tarifesi sarı taksiden yüksektir.</li>
<li><b>Havalimanı yolculukları:</b> Uzun mesafede tutarı belirleyen kilometre ücretidir; trafik yoğunsa bekleme süresi de eklenir.</li>
<li><b>Diğer şehirler:</b> Tarifeyi il belediyesi (UKOME veya belediye meclisi) belirler. Şehrinizin açılış, km ve dakika ücretini girerek aynı hesabı yapabilirsiniz.</li>
</ul>
<p>Kendi aracınızla aynı yolun maliyetini karşılaştırmak için <a href="/yakit-maliyeti-hesaplama.html">yakıt maliyeti hesaplama</a> aracını kullanabilirsiniz.</p>''',
faq=[('İstanbul’da taksi açılış ücreti ne kadar?', 'İstanbul’da sarı taksinin açılış ücreti 71,94 ₺, kilometre ücreti 47,92 ₺, dakika ücreti 9,98 ₺ ve indi-bindi (en az) ücreti 230 ₺’dir. Tarife 20 Temmuz 2026’dan beri uygulanıyor.'),
     ('Ankara’da taksi ücreti ne kadar?', 'Ankara’da 1 Mart 2026’dan beri açılış 65 ₺, kilometre 40 ₺, dakika 7 ₺ ve indi-bindi ücreti 200 ₺’dir.'),
     ('İndi-bindi ücreti nedir?', 'Kısa mesafeli yolculuklarda ödenen en az ücrettir. Taksimetre bu tutarın altında kalsa bile yolcu en az indi-bindi ücretini öder.'),
     ('Taksimetre beklerken de para yazar mı?', 'Evet. Araç dururken veya çok yavaş ilerlerken taksimetre dakika başına zaman ücreti işletir. Bu yüzden trafikte aynı mesafe daha pahalıya gelir.'),
     ('Köprü ve otoyol ücreti taksi ücretine dahil mi?', 'Hayır. Köprü, tünel ve otoyol geçiş ücretleri taksimetreye dahil değildir ve yolcu tarafından ayrıca ödenir.')],
related=['yakit-maliyeti-hesaplama', 'yakit-tuketimi-hesaplama', 'gun-hesaplama', 'yuzde-hesaplama', 'doviz-cevirici'],
sources=[('BirGün – İstanbul taksi ücretleri 2026 (İBB tarifesi)', 'https://www.birgun.net/haber/istanbul-taksi-ucretleri-2026-acilis-kilometre-ve-indi-bindi-fiyatlari-584162'), ('Cumhuriyet – Ankara taksi tarifesi', 'https://www.cumhuriyet.com.tr/ekonomi/ankara-da-taksi-tarifelerine-zam-geldi-acilis-ucreti-o-seviyeye-ulasti-2483922')],
badges=['✓ Ücretsiz', 'İstanbul · Ankara', 'Güncel Tarife'],
))
