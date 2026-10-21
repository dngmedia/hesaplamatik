"""Eğitim ve sınav hesaplamaları."""

TOOLS = []

def net_satirlari(dersler):
    """dersler: [(id, ad, soru)] → doğru/yanlış giriş satırları"""
    h = '<div class="res-rows" style="margin-bottom:6px">'
    h += '<div class="res-row" style="font-weight:700;background:#fff"><span style="flex:1">Test</span><span style="width:80px;text-align:center">Doğru</span><span style="width:80px;text-align:center">Yanlış</span></div>'
    for i, ad, soru in dersler:
        h += (f'<div class="res-row" style="align-items:center"><span style="flex:1">{ad} <small style="color:var(--muted)">({soru} soru)</small></span>'
              f'<input type="number" id="{i}d" placeholder="0" inputmode="numeric" style="width:72px;margin-right:8px" aria-label="{ad} doğru">'
              f'<input type="number" id="{i}y" placeholder="0" inputmode="numeric" style="width:72px" aria-label="{ad} yanlış"></div>')
    return h + '</div>'

NET_JS = r'''
function netHesap(liste,boluk){var rows=[],top=0,hata='';liste.forEach(function(x){var d=v(x[0]+'d')||0,y=v(x[0]+'y')||0;if(d<0||y<0||d+y>x[2])hata=x[1]+' için doğru + yanlış en fazla '+x[2]+' olabilir.';var n=d-y/boluk;top+=n;rows.push([x[1],num(n,2)+' net <small style="color:var(--muted)">('+d+'D '+y+'Y '+(x[2]-d-y)+'B)</small>']);});return {rows:rows,top:top,hata:hata};}
'''

# ───────────────────────── TYT ─────────────────────────
TYT = [('tr', 'Türkçe', 40), ('sos', 'Sosyal Bilimler', 20), ('mat', 'Temel Matematik', 40), ('fen', 'Fen Bilimleri', 20)]
TOOLS.append(dict(
slug='tyt-net-hesaplama', name='TYT Net Hesaplama', cat='egitim', ico='📝',
title='TYT Net Hesaplama 2026 – 4 Yanlış 1 Doğruyu Götürür | Hesaplarsın',
desc='TYT doğru ve yanlış sayılarınızla Türkçe, Sosyal, Matematik ve Fen netlerinizi ve toplam netinizi hesaplayın. OBP katkısı ve net artırma taktikleri dahil.',
h1='📝 TYT Net Hesaplama 2026',
lead='Deneme veya sınav sonucunuzdaki doğru ve yanlış sayılarını girin; her testin netini, toplam TYT netinizi ve diploma notunuzun yerleştirme puanına katkısını görün.',
form=net_satirlari(TYT) + '''<div class="form-grid" style="margin-top:12px"><div class="field"><label for="dip">Diploma Notu <small>(50–100, OBP için)</small></label><input type="number" id="dip" placeholder="örn: 85" inputmode="decimal"></div></div>''',
js=NET_JS + r'''
var DERS=''' + str([list(x) for x in TYT]).replace("'", '"') + r''';
function hesapla(){
  var r=netHesap(DERS,4); if(r.hata) return r.hata;
  var rows=r.rows.slice(), dip=v('dip');
  if(dip>=50&&dip<=100){var obp=dip*5; rows.push(['OBP (diploma × 5)',num(obp,2)]); rows.push(['Yerleştirme puanına OBP katkısı (×0,12)','+'+num(obp*0.12,2)+' puan','hl']);}
  return {main:['Toplam TYT neti', num(r.top,2)+' / 120'], sub:'Başarı oranı: '+pct(r.top/120*100,1), rows:rows,
    note:'Ham puan, her testin netinin ÖSYM’nin o yıl için belirlediği katsayılarla çarpılmasıyla hesaplanır; katsayılar sınav sonrasında belli olduğundan burada puan tahmini verilmemiştir.'};
}''',
article='''
<h2 id="nasil">TYT neti nasıl hesaplanır?</h2>
<p>Temel Yeterlilik Testi’nde (TYT) yanlış cevaplar doğru cevapların bir kısmını götürür: <b>4 yanlış 1 doğruyu</b> götürür. Boş bırakılan sorular nete etki etmez. Her test için net ayrı ayrı hesaplanır ve toplanır.</p>
<div class="formula">Net = Doğru sayısı − (Yanlış sayısı ÷ 4)</div>
<div class="example"><p><b>Örnek:</b> Türkçe’de 32 doğru, 6 yanlış: 32 − 6 ÷ 4 = <b>30,5 net</b>.</p></div>

<h2 id="dagilim">TYT soru dağılımı (2026)</h2>
<div class="table-wrap"><table><thead><tr><th>Test</th><th>Soru</th><th>İçerik</th></tr></thead><tbody>
<tr><td>Türkçe</td><td>40</td><td>Paragraf, dil bilgisi, sözcükte ve cümlede anlam</td></tr>
<tr><td>Sosyal Bilimler</td><td>20</td><td>Tarih 5, Coğrafya 5, Felsefe 5, Din Kültürü 5 (veya ek Felsefe)</td></tr>
<tr><td>Temel Matematik</td><td>40</td><td>Matematik ve geometri</td></tr>
<tr><td>Fen Bilimleri</td><td>20</td><td>Fizik 7, Kimya 7, Biyoloji 6</td></tr>
<tr><td><b>Toplam</b></td><td><b>120</b></td><td>165 dakika</td></tr>
</tbody></table></div>

<h2 id="puan">TYT puanı nasıl hesaplanır?</h2>
<p>TYT puanı; her testteki netlerin ÖSYM’nin standart puan yöntemiyle hesapladığı ağırlıklarla çarpılması ve sabit bir taban puanın eklenmesiyle oluşur. Katsayılar, o yılki adayların ortalama ve standart sapmalarına göre belirlendiğinden sınav öncesinde kesin olarak bilinemez. Bu nedenle internetteki “TYT puan hesaplama” araçlarının tümü geçmiş yıl katsayılarıyla <b>tahmin</b> yapar.</p>
<p>TYT’den en az <b>150 ham puan</b> alan adaylar ön lisans tercihi yapabilir ve AYT puanları hesaplanır. Lisans tercihi için AYT puan türlerinin (SAY, EA, SÖZ, DİL) hesaplanabilmesi için TYT’de 150 puan barajının geçilmesi gerekir.</p>

<h2 id="obp">OBP (diploma notu) puana nasıl eklenir?</h2>
<p>Ortaöğretim Başarı Puanı (OBP), diploma notunun 5 ile çarpılmasıyla bulunur (50–100 arası diploma notu → 250–500 OBP). Yerleştirme puanına OBP’nin <b>%12’si</b> eklenir. Bir önceki yıl bir programa yerleşen adaylarda bu katkı yarıya düşer.</p>
<div class="example"><p><b>Örnek:</b> Diploma notu 85 → OBP 425 → yerleştirme puanına +51 puan.</p></div>
<p>Diploma notunuzu hesaplamak için <a href="/not-ortalamasi-hesaplama.html">not ortalaması hesaplama</a> aracını kullanabilirsiniz.</p>

<h2 id="taktik">TYT netini artırma taktikleri</h2>
<ul>
<li><b>Emin olmadığınız soruyu boş bırakın:</b> 4 seçenekten 2’sini eleyebiliyorsanız tahmin yapmak istatistiksel olarak avantajlıdır; hiç eleyemiyorsanız boş bırakmak daha güvenlidir.</li>
<li><b>Paragraf hızınızı artırın:</b> Türkçe testinde soruların yarısından fazlası paragraf sorusudur.</li>
<li><b>Temel matematiği sağlamlaştırın:</b> Sayı problemleri ve temel kavramlar en çok net kazandıran konulardır.</li>
<li><b>Deneme analizi yapın:</b> Her denemeden sonra yanlışlarınızı konu bazında not edin; net artışınızı bu araçla takip edin.</li>
</ul>
<p>AYT netlerinizi hesaplamak için <a href="/ayt-net-hesaplama.html">AYT net hesaplama</a>, KPSS için <a href="/kpss-net-hesaplama.html">KPSS net hesaplama</a> araçlarını kullanabilirsiniz.</p>
''',
faq=[
('TYT’de kaç yanlış bir doğruyu götürür?','TYT’de 4 yanlış 1 doğruyu götürür. Net = Doğru − Yanlış ÷ 4 formülüyle hesaplanır.'),
('TYT kaç sorudan oluşur?','Toplam 120 soru: 40 Türkçe, 20 Sosyal Bilimler, 40 Temel Matematik ve 20 Fen Bilimleri.'),
('TYT’de 150 puan için kaç net gerekir?','Geçmiş yıllarda 150 baraj puanı için yaklaşık 15–25 net yeterli olmuştur; kesin değer o yılki ortalamalara bağlıdır.'),
('Boş bırakılan sorular neti etkiler mi?','Hayır. Boş bırakılan sorular neti azaltmaz ya da artırmaz.'),
('OBP katkısı nasıl hesaplanır?','Diploma notu 5 ile çarpılarak OBP bulunur ve OBP’nin %12’si yerleştirme puanına eklenir.'),
],
related=['ayt-net-hesaplama','kpss-net-hesaplama','not-ortalamasi-hesaplama','takdir-tesekkur-hesaplama','ortalama-hesaplama'],
sources=[('ÖSYM – YKS Kılavuzu','https://www.osym.gov.tr/')],
))

# ───────────────────────── KPSS ─────────────────────────
KPSS = [('tr', 'Türkçe', 30), ('mat', 'Matematik', 30), ('tar', 'Tarih', 27), ('cog', 'Coğrafya', 18), ('vat', 'Vatandaşlık', 9), ('gun', 'Güncel Bilgiler', 6)]
TOOLS.append(dict(
slug='kpss-net-hesaplama', name='KPSS Net Hesaplama', cat='egitim', ico='📝',
title='KPSS Net Hesaplama 2026 – Genel Yetenek ve Genel Kültür Neti | Hesaplarsın',
desc='KPSS lisans Genel Yetenek (Türkçe, Matematik) ve Genel Kültür (Tarih, Coğrafya, Vatandaşlık, Güncel) netlerinizi hesaplayın. Eğitim Bilimleri neti de eklenebilir.',
h1='📝 KPSS Net Hesaplama 2026',
lead='KPSS lisans GY-GK testindeki doğru ve yanlış sayılarınızı girin; ders bazında netlerinizi, Genel Yetenek ve Genel Kültür toplamlarınızı anında görün.',
form=net_satirlari(KPSS) + net_satirlari([('eb', 'Eğitim Bilimleri (isteğe bağlı)', 80)]),
js=NET_JS + r'''
var GY=[["tr","Türkçe",30],["mat","Matematik",30]], GK=[["tar","Tarih",27],["cog","Coğrafya",18],["vat","Vatandaşlık",9],["gun","Güncel Bilgiler",6]];
function hesapla(){
  var a=netHesap(GY,4), b=netHesap(GK,4), e=netHesap([["eb","Eğitim Bilimleri",80]],4); if(a.hata||b.hata||e.hata) return a.hata||b.hata||e.hata;
  var rows=a.rows.concat([['<b>Genel Yetenek toplam</b>','<b>'+num(a.top,2)+' / 60</b>']]).concat(b.rows).concat([['<b>Genel Kültür toplam</b>','<b>'+num(b.top,2)+' / 60</b>']]);
  if(v('ebd')>0||v('eby')>0) rows.push(['Eğitim Bilimleri',num(e.top,2)+' / 80']);
  return {main:['GY + GK toplam net', num(a.top+b.top,2)+' / 120'], sub:'Genel Yetenek '+num(a.top,2)+' · Genel Kültür '+num(b.top,2), rows:rows,
    note:'KPSS puanı (P3, P10 vb.) netlerin standart puana dönüştürülmesiyle hesaplanır ve sınava girenlerin ortalamalarına bağlıdır.'};
}''',
article='''
<h2 id="nasil">KPSS neti nasıl hesaplanır?</h2>
<p>Kamu Personeli Seçme Sınavı’nda (KPSS) her testte <b>4 yanlış 1 doğruyu götürür</b>. Net, doğru sayısından yanlış sayısının dörtte birinin çıkarılmasıyla bulunur. Boş bırakılan sorular nete etki etmez.</p>
<div class="formula">Net = Doğru − (Yanlış ÷ 4)</div>
<div class="example"><p><b>Örnek:</b> Tarih testinde 20 doğru, 4 yanlış: 20 − 4 ÷ 4 = <b>19 net</b>.</p></div>

<h2 id="dagilim">KPSS lisans soru dağılımı (2026)</h2>
<div class="table-wrap"><table><thead><tr><th>Oturum</th><th>Ders</th><th>Soru</th></tr></thead><tbody>
<tr><td rowspan="2">Genel Yetenek (60)</td><td>Türkçe</td><td>30</td></tr><tr><td>Matematik (geometri dahil)</td><td>30</td></tr>
<tr><td rowspan="4">Genel Kültür (60)</td><td>Tarih</td><td>27</td></tr><tr><td>Coğrafya</td><td>18</td></tr><tr><td>Vatandaşlık</td><td>9</td></tr><tr><td>Güncel Bilgiler</td><td>6</td></tr>
</tbody></table></div>
<p>GY-GK oturumu toplam 120 sorudan oluşur ve 130 dakika sürer. Öğretmen adayları ayrıca Eğitim Bilimleri ve ÖABT oturumlarına girer.</p>

<h2 id="puan">KPSS puan türleri</h2>
<p>KPSS’de netler doğrudan puan değildir. Her testin neti, o sınava giren tüm adayların ortalaması ve standart sapması kullanılarak standart puana dönüştürülür; ardından puan türüne göre ağırlıklandırılır.</p>
<div class="table-wrap"><table><thead><tr><th>Puan türü</th><th>Kullanım alanı</th></tr></thead><tbody>
<tr><td>P3</td><td>Lisans mezunları için çoğu memur kadrosu (GY %50 + GK %50)</td></tr>
<tr><td>P10</td><td>Öğretmenlik (GY-GK + Eğitim Bilimleri)</td></tr>
<tr><td>P93</td><td>Ön lisans mezunları</td></tr>
<tr><td>P94</td><td>Ortaöğretim (lise) mezunları</td></tr>
<tr><td>P121</td><td>Öğretmenlik (ÖABT dahil)</td></tr>
</tbody></table></div>

<h2 id="hedef">KPSS’de iyi bir net kaçtır?</h2>
<p>Atanma için gereken net, kadro türüne, tercih edilen şehre ve o yılın ilanına göre çok değişir. Genel bir fikir vermesi açısından P3 puan türünde 80 ve üzeri puanlar için GY-GK’da genellikle 90 net civarı ve üzeri gerekmektedir. Hedefinizi belirlerken bir önceki yılın taban puanlarını incelemek en sağlıklı yoldur.</p>

<h2 id="taktik">KPSS netini artırma önerileri</h2>
<ul>
<li>Genel Kültür’de Tarih ve Coğrafya 45 soruyla belirleyicidir; kronolojik çalışma ve harita okumaya ağırlık verin.</li>
<li>Vatandaşlık ve Güncel Bilgiler az soruya rağmen hızlı net kazandırır; güncel gelişmeleri sınava yakın tekrar edin.</li>
<li>Türkçe’de paragraf hızınızı, Matematik’te problem çözme pratiğinizi artırın.</li>
<li>Her denemeden sonra netlerinizi ders bazında kaydedip gelişimi takip edin; ortalama netinizi <a href="/ortalama-hesaplama.html">ortalama hesaplama</a> ile bulabilirsiniz.</li>
</ul>
''',
faq=[
('KPSS’de kaç yanlış bir doğruyu götürür?','KPSS’de 4 yanlış 1 doğruyu götürür.'),
('KPSS lisans kaç soru?','Genel Yetenek 60 ve Genel Kültür 60 olmak üzere toplam 120 sorudur.'),
('KPSS Genel Kültür soru dağılımı nedir?','Tarih 27, Coğrafya 18, Vatandaşlık 9 ve Güncel Bilgiler 6 soru.'),
('Net ile KPSS puanı aynı şey mi?','Hayır. Netler, tüm adayların sonuçlarına göre standart puana dönüştürülür; bu nedenle aynı net farklı yıllarda farklı puan getirebilir.'),
],
related=['tyt-net-hesaplama','ayt-net-hesaplama','not-ortalamasi-hesaplama','ortalama-hesaplama','yas-hesaplama'],
sources=[('ÖSYM – KPSS','https://www.osym.gov.tr/')],
))

# ───────────────────────── NOT ORTALAMASI ─────────────────────────
TOOLS.append(dict(
slug='not-ortalamasi-hesaplama', name='Not Ortalaması Hesaplama', cat='egitim', ico='📚',
title='Not Ortalaması Hesaplama – Lise, Ortaokul ve Üniversite (GANO) | Hesaplarsın',
desc='Ders notları ve haftalık ders saatleri (lise/ortaokul) ya da kredi ve harf notlarıyla (üniversite) ağırlıklı not ortalamanızı hesaplayın. 4’lük ve 100’lük sistem.',
h1='📚 Not Ortalaması Hesaplama',
lead='Lise ve ortaokul için ders notu ve haftalık ders saatiyle ağırlıklı ortalamanızı, üniversite için kredi ve harf notuyla dönem ortalamanızı (GANO) hesaplayın.',
form='''<div class="field full" style="margin-bottom:14px"><label>Sistem</label>
<div class="seg"><label><input type="radio" name="mod" value="lise" checked onchange="modSec()">Lise / Ortaokul (100’lük)</label><label><input type="radio" name="mod" value="uni" onchange="modSec()">Üniversite (4’lük, harf notu)</label></div></div>
<div id="dersler"></div>
<button type="button" class="btn-reset" style="margin-top:6px" onclick="satir()">+ Ders ekle</button>''',
js=r'''
var HARF={'AA':4,'BA':3.5,'BB':3,'CB':2.5,'CC':2,'DC':1.5,'DD':1,'FD':0.5,'FF':0};
function satir(ad,not,saat){var uni=radio('mod')==='uni', d=document.createElement('div'); d.className='form-grid ders'; d.style.marginBottom='8px'; d.style.gridTemplateColumns='2fr 1fr 1fr';
  d.innerHTML='<input type="text" placeholder="Ders adı" value="'+(ad||'')+'">'+(uni?'<select>'+Object.keys(HARF).map(function(h){return '<option'+(h===not?' selected':'')+'>'+h+'</option>';}).join('')+'</select>':'<input type="text" inputmode="decimal" placeholder="Not" value="'+(not||'')+'">')+'<input type="text" inputmode="decimal" placeholder="'+(uni?'Kredi/AKTS':'Ders saati')+'" value="'+(saat||'')+'">';
  el('dersler').appendChild(d); d.querySelectorAll('input,select').forEach(function(i){i.addEventListener('input',function(){if(_last)run(false);});i.addEventListener('change',function(){if(_last)run(false);});});}
function modSec(){el('dersler').innerHTML='';var uni=radio('mod')==='uni';
  (uni?[['Matematik I','BA',6],['Fizik I','CB',5],['Türk Dili','AA',2],['Programlama','BB',5]]:[['Türk Dili ve Edebiyatı','',5],['Matematik','',6],['Fizik','',2],['Tarih','',2],['İngilizce','',4]]).forEach(function(x){satir(x[0],x[1],x[2]);});el('result').style.display='none';_last=null;}
function onReady(){modSec();}
function onReset(){modSec();}
function n(s){s=String(s).trim().replace(',','.');return s===''?NaN:parseFloat(s);}
function hesapla(){
  var uni=radio('mod')==='uni', top=0, ag=0, sayi=0, tab=[];
  document.querySelectorAll('#dersler .ders').forEach(function(d){var c=d.children, ad=c[0].value||'Ders', not=uni?HARF[c[1].value]:n(c[1].value), w=n(c[2].value);
    if(isNaN(not)||isNaN(w)||w<=0) return; if(!uni&&(not<0||not>100)) return; top+=not*w; ag+=w; sayi++; tab.push('<tr><td>'+esc(ad)+'</td><td>'+(uni?c[1].value+' ('+num(not,1)+')':num(not,2))+'</td><td>'+num(w,w%1?1:0)+'</td></tr>');});
  if(!sayi) return 'En az bir ders için not ve '+(uni?'kredi':'ders saati')+' girin.';
  var o=top/ag;
  if(uni){var y=o>=3.5?'Yüksek onur (genellikle)':o>=3?'Onur (genellikle)':o>=2?'Başarılı':'Koşullu / başarısız riski';
    return {main:['Dönem ortalaması (4’lük)', num(o,2)], sub:y+' · 100’lük karşılığı (YÖK tablosu) ≈ '+num(yok(o),2), rows:[['Toplam kredi',num(ag,1)],['Ağırlıklı puan toplamı',num(top,2)],['Ders sayısı',sayi]],
      extra:'<table><thead><tr><th>Ders</th><th>Not</th><th>Kredi</th></tr></thead><tbody>'+tab.join('')+'</tbody></table>'};}
  var belge=o>=85?'🏆 Takdir belgesi aralığında':o>=70?'🎉 Teşekkür belgesi aralığında':o>=50?'Geçer not ortalaması':'Ortalama 50’nin altında';
  return {main:['Ağırlıklı not ortalaması', num(o,2)], sub:belge, rows:[['Toplam ders saati',num(ag,0)],['Ders sayısı',sayi],['Diploma notu olsaydı OBP (× 5)',num(o*5,2)]],
    extra:'<table><thead><tr><th>Ders</th><th>Not</th><th>Saat</th></tr></thead><tbody>'+tab.join('')+'</tbody></table>'};
}
function yok(g){var t=[[4,100],[3.5,88.33],[3,76.67],[2.5,65],[2,53.33],[1.5,41.67],[1,30],[0,0]];for(var i=0;i<t.length-1;i++){if(g>=t[i+1][0]){var a=t[i+1],b=t[i];return a[1]+(g-a[0])*(b[1]-a[1])/(b[0]-a[0]);}}return 0;}
''',
article='''
<h2 id="lise">Lise ve ortaokulda not ortalaması nasıl hesaplanır?</h2>
<p>MEB okullarında dönem veya yıl sonu ortalaması, her dersin puanının <b>haftalık ders saati</b> ile çarpılması, bu çarpımların toplanması ve toplam ders saatine bölünmesiyle hesaplanır. Böylece haftada 6 saat olan Matematik, 2 saatlik bir dersten daha fazla etki eder.</p>
<div class="formula">Ortalama = Σ(Ders puanı × Haftalık ders saati) ÷ Σ(Haftalık ders saati)</div>
<div class="example"><p><b>Örnek:</b> Edebiyat 80 (5 saat), Matematik 70 (6 saat), Fizik 90 (2 saat):</p><p>(400 + 420 + 180) ÷ 13 = <b>76,92</b></p></div>
<p>Dersin dönem puanı ise o dersteki yazılı sınav ve performans notlarının aritmetik ortalamasıdır. Lisede yıl sonu ortalamasının 50 ve üzeri olması sınıf geçmek için gereklidir; ayrıca başarısız ders sayısına ilişkin kurallar uygulanır.</p>

<h2 id="belge">Takdir ve teşekkür için kaç ortalama gerekir?</h2>
<div class="table-wrap"><table><thead><tr><th>Ortalama</th><th>Belge</th></tr></thead><tbody>
<tr><td>85,00 ve üzeri</td><td>Takdir belgesi</td></tr><tr><td>70,00 – 84,99</td><td>Teşekkür belgesi</td></tr>
</tbody></table></div>
<p>Belge almak için ortalamanın yanında okul yönetmeliğindeki diğer şartlar da aranır. Ayrıntılar için <a href="/takdir-tesekkur-hesaplama.html">takdir teşekkür hesaplama</a> sayfasına bakabilirsiniz.</p>

<h2 id="universite">Üniversitede not ortalaması (GANO) nasıl hesaplanır?</h2>
<p>Üniversitelerde her dersin harf notu 4’lük sistemdeki katsayısına çevrilir ve dersin kredisi (veya AKTS’si) ile çarpılır. Dönem ortalaması (DNO/YANO) yalnızca o dönemin dersleriyle, genel akademik not ortalaması (GANO) ise tüm dönemlerin dersleriyle hesaplanır.</p>
<div class="formula">GANO = Σ(Harf notu katsayısı × Kredi) ÷ Σ(Kredi)</div>
<div class="table-wrap"><table><thead><tr><th>Harf</th><th>Katsayı</th><th>Harf</th><th>Katsayı</th></tr></thead><tbody>
<tr><td>AA</td><td>4,0</td><td>DC</td><td>1,5</td></tr><tr><td>BA</td><td>3,5</td><td>DD</td><td>1,0</td></tr><tr><td>BB</td><td>3,0</td><td>FD</td><td>0,5</td></tr>
<tr><td>CB</td><td>2,5</td><td>FF</td><td>0,0</td></tr><tr><td>CC</td><td>2,0</td><td></td><td></td></tr>
</tbody></table></div>
<p>Harf notu aralıkları ve onur/yüksek onur sınırları üniversiteden üniversiteye değişebilir; kendi yönetmeliğinizi kontrol edin. 4’lük not, YÖK dönüşüm tablosu ile 100’lük sisteme çevrilir (örneğin 3,00 ≈ 76,67).</p>

<h2 id="vize-final">Ders geçme notu nasıl hesaplanır?</h2>
<p>Üniversitede bir dersin başarı notu genellikle vize ve final notlarının ağırlıklı ortalamasıdır (örneğin %40 vize + %60 final). Farklı ağırlıklarla hesaplama yapmak için <a href="/ortalama-hesaplama.html">ortalama hesaplama</a> aracının “ağırlıklı” modunu kullanabilirsiniz.</p>
''',
faq=[
('Lise not ortalaması nasıl hesaplanır?','Her ders puanı haftalık ders saatiyle çarpılır, çarpımlar toplanır ve toplam ders saatine bölünür.'),
('Takdir almak için ortalama kaç olmalı?','85,00 ve üzeri ortalama takdir, 70,00–84,99 arası teşekkür belgesi için gereklidir; ek şartlar okul yönetmeliğinde belirtilir.'),
('4’lük not 100’lük sisteme nasıl çevrilir?','YÖK’ün dönüşüm tablosu kullanılır. Örneğin 3,00 yaklaşık 76,67’ye, 3,50 yaklaşık 88,33’e karşılık gelir.'),
('AKTS mi kredi mi kullanılmalı?','Üniversitenizin ortalama hesaplamasında hangisini kullandığını kontrol edin; Bologna sürecindeki çoğu üniversite AKTS’yi esas alır.'),
],
related=['takdir-tesekkur-hesaplama','ortalama-hesaplama','tyt-net-hesaplama','ayt-net-hesaplama','kpss-net-hesaplama'],
))

# ───────────────────────── TAKDİR TEŞEKKÜR ─────────────────────────
TOOLS.append(dict(
slug='takdir-tesekkur-hesaplama', name='Takdir Teşekkür Hesaplama', cat='egitim', ico='🏆',
title='Takdir Teşekkür Hesaplama 2026 – Kaç Puanla Takdir Alınır? | Hesaplarsın',
desc='Ders notlarınız ve haftalık ders saatlerinizle ortalamanızı hesaplayın; takdir (85+) veya teşekkür (70–84,99) belgesi alıp alamayacağınızı ve hedef için gereken notu görün.',
h1='🏆 Takdir Teşekkür Hesaplama',
lead='Ders notlarınızı ve haftalık ders saatlerini girin; ortalamanızı, takdir veya teşekkür belgesi alıp alamayacağınızı ve bir üst belge için ortalamanızın kaç puan artması gerektiğini öğrenin.',
form='''<div id="dersler"></div>
<button type="button" class="btn-reset" style="margin-top:6px" onclick="satir()">+ Ders ekle</button>
<div class="form-grid" style="margin-top:12px"><div class="field full"><label class="chk"><input type="checkbox" id="basarisiz"> Başarısız (50’nin altında) dersim var</label><label class="chk"><input type="checkbox" id="disiplin"> Bu dönem disiplin cezası aldım</label></div></div>''',
js=r'''
var VARSAYILAN=[['Türkçe / Edebiyat',5],['Matematik',5],['Fen Bilimleri / Fizik',4],['Sosyal Bilgiler / Tarih',3],['İngilizce',3],['Din Kültürü',2],['Beden Eğitimi',2],['Görsel Sanatlar / Müzik',1]];
function satir(ad,saat){var d=document.createElement('div');d.className='form-grid ders';d.style.marginBottom='8px';d.style.gridTemplateColumns='2fr 1fr 1fr';
 d.innerHTML='<input type="text" placeholder="Ders adı" value="'+(ad||'')+'"><input type="text" inputmode="decimal" placeholder="Not"><input type="text" inputmode="decimal" placeholder="Ders saati" value="'+(saat||'')+'">';el('dersler').appendChild(d);
 d.querySelectorAll('input').forEach(function(i){i.addEventListener('input',function(){if(_last)run(false);});});}
function onReady(){VARSAYILAN.forEach(function(x){satir(x[0],x[1]);});}
function onReset(){el('dersler').innerHTML='';onReady();}
function n(s){s=String(s).trim().replace(',','.');return s===''?NaN:parseFloat(s);}
function hesapla(){
  var top=0, ag=0, say=0, dusuk=false;
  document.querySelectorAll('#dersler .ders').forEach(function(d){var c=d.children, not=n(c[1].value), w=n(c[2].value); if(isNaN(not)||isNaN(w)||w<=0||not<0||not>100) return; top+=not*w; ag+=w; say++; if(not<50) dusuk=true;});
  if(!say) return 'Derslerinize not ve haftalık ders saati girin.';
  var o=top/ag, b=o>=85?'TAKDİR':o>=70?'TEŞEKKÜR':'BELGE YOK', engel=checked('basarisiz')||dusuk||checked('disiplin');
  var rows=[['Ağırlıklı ortalama',num(o,2)],['Toplam haftalık ders saati',num(ag,0)]];
  if(o<85) rows.push([o<70?'Teşekkür için gereken artış':'Takdir için gereken artış','+'+num((o<70?70:85)-o,2)+' puan ortalama']);
  if(o<85) rows.push(['Tüm derslerde ortalama kaç puan artmalı?','+'+num((o<70?70:85)-o,2)+' puan (her derste)']);
  var sonuc=engel&&b!=='BELGE YOK'?'Ortalamanız '+b.toLowerCase()+' aralığında ancak ek şartlar nedeniyle belge verilmeyebilir':(b==='TAKDİR'?'🏆 Takdir belgesi almaya hak kazanıyorsunuz':b==='TEŞEKKÜR'?'🎉 Teşekkür belgesi almaya hak kazanıyorsunuz':'Belge için ortalamanın en az 70 olması gerekir');
  return {main:['Sonuç', b], sub:sonuc, rows:rows, note:engel?'Başarısız ders, disiplin cezası veya özürsüz devamsızlık sınırının aşılması belge verilmesine engel olabilir. Kesin karar okul yönetimi tarafından verilir.':''};
}''',
article='''
<h2 id="kac-puan">Takdir ve teşekkür kaç puanla alınır?</h2>
<p>Milli Eğitim Bakanlığı yönetmeliklerine göre, dönem sonunda tüm derslerin ağırlıklı not ortalaması:</p>
<div class="table-wrap"><table><thead><tr><th>Ağırlıklı ortalama</th><th>Belge</th></tr></thead><tbody>
<tr><td><b>85,00 ve üzeri</b></td><td>🏆 Takdir belgesi</td></tr>
<tr><td><b>70,00 – 84,99</b></td><td>🎉 Teşekkür belgesi</td></tr>
<tr><td>70’in altı</td><td>Belge verilmez</td></tr>
</tbody></table></div>
<p>olan öğrencilere ilgili belge verilir. Ortalama hesabında basit ortalama değil, <b>haftalık ders saatine göre ağırlıklı ortalama</b> kullanılır.</p>

<h2 id="nasil">Takdir teşekkür ortalaması nasıl hesaplanır?</h2>
<div class="formula">Ortalama = Σ(Ders dönem puanı × Haftalık ders saati) ÷ Toplam haftalık ders saati</div>
<div class="example"><p><b>Örnek:</b> Matematik 80 (5 saat), Türkçe 90 (5 saat), Fen 85 (4 saat), İngilizce 75 (3 saat):</p>
<p>(400 + 450 + 340 + 225) ÷ 17 = 1.415 ÷ 17 = <b>83,24 → Teşekkür</b>. Takdir için ortalamanın 1,76 puan artması gerekir.</p></div>
<p>Haftalık ders saati yüksek olan dersler ortalamayı daha fazla etkiler. Bu yüzden 5–6 saatlik ana derslerdeki birkaç puanlık artış, takdire ulaşmada en hızlı yoldur.</p>

<h2 id="sartlar">Takdir ve teşekkür için diğer şartlar</h2>
<ul>
<li><b>Davranış ve disiplin:</b> İlgili dönemde disiplin cezası almış öğrencilere genellikle belge verilmez.</li>
<li><b>Başarısız ders:</b> Lisede başarısız dersi bulunan öğrencinin ortalaması yeterli olsa bile belge verilmeyebilir.</li>
<li><b>Devamsızlık:</b> Özürsüz devamsızlığın yönetmelikte belirtilen sınırı aşmaması gerekir.</li>
</ul>
<p>Şartlar okul türüne (ilkokul, ortaokul, lise) ve yönetmelik değişikliklerine göre farklılık gösterebilir; kesin bilgi için okul idarenize danışın.</p>

<h2 id="karne">Karne notu ve e-Okul</h2>
<p>Dönem puanları e-Okul VBS sisteminde dönem sonunda kesinleşir. e-Okul’da görünen ders notlarınızı ve haftalık ders saatlerini (ders programınızdan) hesaplayıcıya girerek belge durumunuzu önceden görebilirsiniz. Yıl sonu ve diploma notunu hesaplamak için <a href="/not-ortalamasi-hesaplama.html">not ortalaması hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('Takdir kaç puanla alınır?','Ağırlıklı dönem sonu ortalaması 85,00 ve üzeri olan öğrenciler takdir belgesi alır.'),
('Teşekkür kaç puanla alınır?','Ağırlıklı ortalaması 70,00 ile 84,99 arasında olan öğrenciler teşekkür belgesi alır.'),
('84,99 ortalama takdire yuvarlanır mı?','Hayır. Takdir için ortalamanın en az 85,00 olması gerekir; yuvarlama yapılmaz.'),
('Bir dersten zayıfım, teşekkür alabilir miyim?','Lisede başarısız dersi olan öğrenciye ortalaması yeterli olsa da belge verilmeyebilir. Ortaokulda da okul yönetmeliğindeki şartlar uygulanır.'),
('Ortalamaya hangi dersler girer?','Haftalık ders çizelgesindeki tüm zorunlu ve seçmeli dersler, ders saati ağırlığıyla hesaba girer.'),
],
related=['not-ortalamasi-hesaplama','ortalama-hesaplama','tyt-net-hesaplama','yas-hesaplama','yuzde-hesaplama'],
))
