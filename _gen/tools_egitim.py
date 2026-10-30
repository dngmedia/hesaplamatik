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
<p>KPSS’de netler doğrudan puan değildir. Netlerinizden tahmini P3, P93 veya P94 puanınızı görmek için <a href="https://hesaplarsin.com/kpss-puan-hesaplama.html">KPSS puan hesaplama</a> aracını kullanabilirsiniz. Her testin neti, o sınava giren tüm adayların ortalaması ve standart sapması kullanılarak standart puana dönüştürülür; ardından puan türüne göre ağırlıklandırılır.</p>
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
related=['kpss-puan-hesaplama','tyt-net-hesaplama','ayt-net-hesaplama','not-ortalamasi-hesaplama','ortalama-hesaplama'],
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
function modSec(){var uni=radio('mod')==='uni';el('dersler').innerHTML='<div class="form-grid" style="grid-template-columns:2fr 1fr 1fr;margin-bottom:4px;font-size:.75rem;font-weight:700;color:var(--muted)"><span>Ders</span><span>'+(uni?'Harf notu':'Not (0–100)')+'</span><span>'+(uni?'Kredi / AKTS':'Haftalık saat')+'</span></div>';
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
function onReady(){el('dersler').innerHTML='<div class="form-grid" style="grid-template-columns:2fr 1fr 1fr;margin-bottom:4px;font-size:.75rem;font-weight:700;color:var(--muted)"><span>Ders</span><span>Not (0–100)</span><span>Haftalık saat</span></div>';VARSAYILAN.forEach(function(x){satir(x[0],x[1]);});}
function onReset(){onReady();}
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


# ───────────────────────── OBP (ORTAÖĞRETİM BAŞARI PUANI) ─────────────────────────
# Kurallar (ÖSYM YKS kılavuzu, kamuya açık rehberlerle 24 Ekim 2026 kontrol): OBP = diploma notu × 5 (250–500; 50 altı not 50 sayılır).
# Yerleştirme katkısı OBP × 0,12; önceki yıl bir programa yerleştirilenlerde yarıya iner (× 0,06).
# Meslek lisesi mezunları alanlarıyla ilgili, kılavuzda belirtilen önlisans programlarında ek puan: OBP × 0,06 (ilgili puan türünde en az 150).
def _tr(x, d=2):
    s = f"{x:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


_OBP_ROWS = ''.join(f'<tr><td>{_tr(n, 0)}</td><td>{_tr(max(n, 50) * 5, 0)}</td><td>+{_tr(max(n, 50) * 5 * 0.12)}</td><td>+{_tr(max(n, 50) * 5 * 0.06)}</td></tr>'
                    for n in (50, 60, 70, 75, 80, 85, 90, 95, 100))
OBP_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Diploma notu</th><th>OBP</th><th>YKS’ye katkı (× 0,12)</th><th>Önceki yıl yerleşenler (× 0,06)</th></tr></thead>'
             f'<tbody>{_OBP_ROWS}</tbody></table></div>')

TOOLS.append(dict(
slug='obp-hesaplama', name='OBP Hesaplama', cat='egitim', ico='🎓',
title='OBP Hesaplama 2026 – Diploma Notundan OBP ve YKS Puanına Katkı | Hesaplarsın',
desc='Diploma notunuzu girin; OBP’nizi (250–500) ve YKS yerleştirme puanınıza ekleneceği puanı (× 0,12 veya × 0,06) görün. Meslek lisesi ek puanı dahil.',
h1='🎓 OBP Hesaplama 2026',
lead='Ortaöğretim Başarı Puanı (OBP), lise diploma notunuzun 5 katıdır ve 0,12 ile çarpılarak YKS yerleştirme puanınıza eklenir. Diploma notunuzu girin; OBP’nizi, puanınıza katkısını ve isterseniz ham puanınızla yerleştirme puanınızı görün.',
card_title='OBP ve Yerleştirme Puanı Hesaplayıcı', button='Hesapla',
form='''<div class="form-grid">
<div class="field"><label for="dip">Diploma notu (100 üzerinden)</label><input type="number" id="dip" placeholder="örn: 85,40" inputmode="decimal"></div>
<div class="field"><label for="ham">YKS ham puanınız <small>isteğe bağlı (TYT, SAY, EA, SÖZ veya DİL)</small></label><input type="number" id="ham" placeholder="örn: 380" inputmode="decimal"></div>
<div class="field full"><label class="chk"><input type="checkbox" id="once"> Geçen yıl bir yükseköğretim programına yerleştirildim</label>
<label class="chk"><input type="checkbox" id="meslek"> Meslek lisesi mezunuyum, alanımla ilgili önlisans programı tercih edeceğim</label></div>
</div>''',
js=r'''
function hesapla(){
  var d=v('dip'); if(!(d>0&&d<=100)) return 'Diploma notunuzu 0 ile 100 arasında girin.';
  var dn=Math.max(d,50), obp=dn*5, once=checked('once'), mes=checked('meslek');
  var k=once?0.06:0.12, katki=obp*k, ek=(mes&&!once)?obp*0.06:0, h=v('ham');
  var rows=[['Diploma notu (hesapta)',num(dn,2)+(d<50?' (50’nin altı 50 sayılır)':'')],['OBP (diploma notu × 5)',num(obp,2),'hl'],
    ['Katsayı',once?'0,06 (geçen yıl yerleştiğiniz için yarıya iner)':'0,12'],['Yerleştirme puanına katkı','+'+num(katki,3)]];
  if(mes) rows.push(['Meslek lisesi ek puanı (alanınızdaki önlisans programlarında)', once?'Kılavuzdan kontrol edin':'+'+num(ek,3)]);
  if(h>0){ rows.push(['YKS ham puan',num(h,3)]); rows.push(['Yerleştirme puanı',num(h+katki,3),'hl']); if(ek>0) rows.push(['Alanınızdaki önlisans programlarında',num(h+katki+ek,3)]); }
  return {main:['OBP’niz', num(obp,2)], sub:'YKS puanınıza +'+num(katki,2)+' puan ekler', rows:rows,
    note:'Ek puan, ilgili puan türünde en az 150 puan alan meslek lisesi mezunlarına ÖSYM kılavuzunda belirtilen programlarda uygulanır. Kesin bilgi için o yılın YKS kılavuzunu kontrol edin.'};
}''',
article=f'''<h2 id="nedir">OBP nedir, nasıl hesaplanır?</h2>
<p>Ortaöğretim Başarı Puanı (OBP), lise diploma notunuzun ÖSYM tarafından 500’lük sisteme çevrilmiş hâlidir. Hesaplaması basittir:</p>
<div class="formula">OBP = Diploma notu × 5<br>YKS’ye katkı = OBP × 0,12</div>
<p>OBP en az 250, en fazla 500 olur; diploma notu 50’nin altında olan adayların notu 50 kabul edilir. Bu nedenle OBP, yerleştirme puanınıza <b>en az 30, en fazla 60 puan</b> ekler. Diploma notunuz e-Okul ve e-Devlet’te görünen lise mezuniyet notudur; dönem ortalamalarınızdan hesaplamak için <a href="https://hesaplarsin.com/not-ortalamasi-hesaplama.html">not ortalaması hesaplama</a> aracını kullanabilirsiniz.</p>

<h2 id="tablo">Diploma notuna göre OBP tablosu</h2>
{OBP_TABLO}
<p>İki aday arasındaki 10 puanlık diploma notu farkı, yerleştirme puanında 6 puanlık fark yaratır. Sıralamanın sıkıştığı puan aralıklarında bu fark binlerce sıra değiştirebilir.</p>

<h2 id="yariya">OBP ne zaman yarıya düşer?</h2>
<p>Bir önceki yıl ÖSYM tarafından bir yükseköğretim programına yerleştirilen adayların OBP katsayısı <b>0,12 yerine 0,06</b> olur; yani OBP katkısı yarıya iner. Yerleştiği programa kayıt yaptırmamış olmak bu kuralı değiştirmez. Bu yüzden yerleşip kayıt yaptırmadan ertesi yıl tekrar sınava girmeyi düşünen adaylar, 15–30 puanlık kaybı hesaba katmalıdır.</p>

<h2 id="meslek">Meslek lisesi mezunlarına ek puan</h2>
<p>Meslek lisesi mezunları, mezun oldukları alanla ilgili ve YKS kılavuzunda belirtilen önlisans programlarını tercih ettiklerinde, OBP’lerinin <b>0,06 katı</b> kadar ek puan alır. Bunun için ilgili puan türünde en az 150 puan almak gerekir. Örneğin diploma notu 80 olan bir meslek lisesi mezununun OBP’si 400’dür; normal katkısı 48 puan, alanındaki önlisans programlarında ek puanla birlikte toplam katkısı 72 puan olur.</p>

<h2 id="yerlestirme">Yerleştirme puanı nasıl oluşur?</h2>
<p>Yerleştirme puanı, sınavdaki ham puanınıza OBP katkısının eklenmesiyle bulunur. Önlisans programlarına TYT puan türüyle, lisans programlarına SAY, EA, SÖZ veya DİL puan türleriyle yerleştirme yapılır. Netlerinizi hesaplamak için <a href="https://hesaplarsin.com/tyt-net-hesaplama.html">TYT net</a> ve <a href="https://hesaplarsin.com/ayt-net-hesaplama.html">AYT net ve puan</a> hesaplama araçlarını kullanabilirsiniz.</p>''',
faq=[('OBP nasıl hesaplanır?', 'Lise diploma notunuz 5 ile çarpılır. Örneğin 85 diploma notu 425 OBP eder. YKS yerleştirme puanınıza OBP’nin 0,12 katı, yani 51 puan eklenir.'),
     ('OBP en az ve en fazla kaç puan ekler?', 'OBP 250 ile 500 arasında olduğundan YKS yerleştirme puanına en az 30, en fazla 60 puan ekler. Geçen yıl bir programa yerleştirilenlerde bu katkı 15–30 puana iner.'),
     ('Diploma notu 70 olanın OBP’si kaç?', 'Diploma notu 70 olan adayın OBP’si 350’dir ve YKS puanına 42 puan ekler (350 × 0,12).'),
     ('Geçen yıl yerleştim ama kayıt yaptırmadım, OBP’m düşer mi?', 'Evet. Bir önceki yıl bir programa yerleştirilen adayların OBP katsayısı, kayıt yaptırmamış olsalar da 0,06’ya düşer.'),
     ('Meslek lisesi ek puanı nasıl hesaplanır?', 'Alanınızla ilgili, kılavuzda belirtilen önlisans programlarında OBP’nizin 0,06 katı kadar ek puan alırsınız. İlgili puan türünde en az 150 puan şartı vardır.')],
related=['tyt-net-hesaplama', 'ayt-net-hesaplama', 'not-ortalamasi-hesaplama', 'takdir-tesekkur-hesaplama', 'kpss-net-hesaplama'],
sources=[('ÖSYM – YKS Kılavuzu', 'https://www.osym.gov.tr/'), ('YÖK Atlas – Program taban puanları', 'https://yokatlas.yok.gov.tr/')],
badges=['✓ Ücretsiz', '2027 YKS', 'Meslek Lisesi Ek Puanı'],
))


# ═════════════════════════ LGS PUAN ═════════════════════════
def _tr(x, d=2):
    s = f'{x:,.{d}f}'
    return s.replace(',', '§').replace('.', ',').replace('§', '.')

# Yıllara göre net → puan katsayıları (MEB sonuçlarından türetilmiş yaklaşık doğrusal model; tam net ≈ 500)
LGS_K = {  # yıl: (taban, Türkçe, Matematik, Fen, İnkılap, Din, Yabancı dil)
    2024: (196.619, 4.107, 4.632, 3.889, 1.729, 1.818, 1.531),
    2023: (194.752, 4.348, 4.253, 4.123, 1.666, 1.899, 1.507),
    2022: (200.013, 3.920, 4.929, 3.703, 1.752, 1.660, 1.478),
    2021: (200.004, 3.446, 5.787, 3.562, 1.475, 1.592, 1.339),
    2020: (200.264, 3.797, 5.623, 3.341, 1.411, 1.532, 1.505),
}
LGS_D = [('tr', 'Türkçe', 20), ('ink', 'T.C. İnkılap Tarihi ve Atatürkçülük', 10), ('din', 'Din Kültürü ve Ahlak Bilgisi', 10),
         ('ing', 'Yabancı Dil', 10), ('mat', 'Matematik', 20), ('fen', 'Fen Bilimleri', 20)]
_SIRA = ('tr', 'mat', 'fen', 'ink', 'din', 'ing')
_SORU = dict(tr=20, mat=20, fen=20, ink=10, din=10, ing=10)

def _lgs(netler, yil=2024):
    k = LGS_K[yil]
    p = k[0] + sum(c * netler[d] for c, d in zip(k[1:], _SIRA))
    return min(500, max(100, p))

def _profil(top):  # toplam neti soru sayısına orantılı dağıt
    return {d: top * s / 90 for d, s in _SORU.items()}

_LGS_KN = ''.join(f'<tr><td>{t} net</td>' + ''.join(f'<td>{_tr(_lgs(_profil(t), y), 1)}</td>' for y in (2024, 2023, 2022, 2021, 2020)) + '</tr>'
                  for t in (90, 85, 80, 75, 70, 65, 60, 50, 40, 30))
LGS_KN_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Toplam net (90 soruda)</th><th>2024 modeli</th><th>2023</th><th>2022</th><th>2021</th><th>2020</th></tr></thead>'
                f'<tbody>{_LGS_KN}</tbody></table></div>')
_ADLAR = dict(tr='Türkçe', mat='Matematik', fen='Fen Bilimleri', ink='İnkılap Tarihi', din='Din Kültürü', ing='Yabancı Dil')
LGS_KAT_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Yıl</th><th>Sabit</th><th>Türkçe</th><th>Matematik</th><th>Fen</th><th>İnkılap</th><th>Din</th><th>Yab. dil</th></tr></thead><tbody>'
                 + ''.join(f'<tr><td>{y}</td>' + ''.join(f'<td>{_tr(x, 3)}</td>' for x in k) + '</tr>' for y, k in LGS_K.items()) + '</tbody></table></div>')
_k24 = LGS_K[2024]
LGS_NET_DEGER = ('<div class="table-wrap"><table><thead><tr><th>Ders</th><th>Soru</th><th>1 netin puan değeri (2024)</th><th>Dersin tamamı (tam net)</th></tr></thead><tbody>'
                 + ''.join(f'<tr><td>{_ADLAR[d]}</td><td>{_SORU[d]}</td><td>+{_tr(c, 2)}</td><td>+{_tr(c * _SORU[d], 1)}</td></tr>' for c, d in zip(_k24[1:], _SIRA))
                 + '</tbody></table></div>')
_ORNEK = dict(tr=17, mat=15, fen=16, ink=9, din=9, ing=8)
_ORNEK_P = _lgs(_ORNEK)
LGS_JS_K = 'var LK=' + str({y: list(k) for y, k in LGS_K.items()}).replace("'", '') + ';'

TOOLS.append(dict(
slug='lgs-puan-hesaplama', name='LGS Puan Hesaplama', cat='egitim', ico='🎒',
title='LGS Puan Hesaplama 2027 – Netten Puana, Yıllara Göre Karşılaştırma | Hesaplarsın',
desc='LGS doğru ve yanlışlarını girin; ders netlerinizi, ağırlıklı netinizi ve 2020–2024 sonuçlarına göre tahmini LGS puanınızı (100–500) görün. 3 yanlış 1 doğruyu götürür.',
h1='🎒 LGS Puan Hesaplama 2027',
lead='Deneme veya sınav sonuçlarınızdaki doğru ve yanlış sayılarını girin; ders netlerinizi ve geçmiş yılların sonuçlarına göre tahmini LGS puanınızı (merkezi sınav puanı) anında görün. Aynı netin farklı yıllarda kaç puana karşılık geldiğini de karşılaştırın.',
card_title='LGS Net ve Puan Hesaplayıcı', button='Puanımı Hesapla',
form='<p style="font-weight:700;margin:0 0 6px">Sözel bölüm (50 soru, 75 dakika)</p>' + net_satirlari(LGS_D[:4])
     + '<p style="font-weight:700;margin:14px 0 6px">Sayısal bölüm (40 soru, 80 dakika)</p>' + net_satirlari(LGS_D[4:])
     + '''<div class="form-grid" style="margin-top:10px"><div class="field full"><label for="yil">Puan modeli</label><select id="yil">
<option value="2024" selected>2024 sonuçlarına göre (önerilen)</option><option value="2023">2023 sonuçlarına göre</option><option value="2022">2022 sonuçlarına göre</option><option value="2021">2021 sonuçlarına göre</option><option value="2020">2020 sonuçlarına göre</option><option value="ort">5 yılın ortalaması</option></select></div></div>''',
js=NET_JS + LGS_JS_K + r'''
var SOZ=[["tr","Türkçe",20],["ink","İnkılap Tarihi",10],["din","Din Kültürü",10],["ing","Yabancı Dil",10]], SAY=[["mat","Matematik",20],["fen","Fen Bilimleri",20]];
function nt(id,s){var d=v(id+'d')||0,y=v(id+'y')||0;return d-y/3;}
function puan(n,y){var k=LK[y];var p=k[0]+k[1]*n.tr+k[2]*n.mat+k[3]*n.fen+k[4]*n.ink+k[5]*n.din+k[6]*n.ing;return Math.min(500,Math.max(100,p));}
function hesapla(){
  var a=netHesap(SOZ,3), b=netHesap(SAY,3); if(a.hata||b.hata) return a.hata||b.hata;
  var n={tr:nt('tr'),ink:nt('ink'),din:nt('din'),ing:nt('ing'),mat:nt('mat'),fen:nt('fen')};
  var dol=0; ['tr','ink','din','ing','mat','fen'].forEach(function(k){dol+=(v(k+'d')||0)+(v(k+'y')||0);}); if(!dol) return 'En az bir dersin doğru veya yanlış sayısını girin.';
  var top=n.tr+n.ink+n.din+n.ing+n.mat+n.fen, ag=4*(n.tr+n.mat+n.fen)+n.ink+n.din+n.ing;
  var yy=[2024,2023,2022,2021,2020], ps=yy.map(function(y){return puan(n,y);}), sec=el('yil').value;
  var p=sec==='ort'?ps.reduce(function(s,x){return s+x;},0)/5:puan(n,+sec);
  var mn=Math.min.apply(null,ps), mx=Math.max.apply(null,ps);
  var rows=a.rows.concat(b.rows).concat([['<b>Toplam net</b>','<b>'+num(top,2)+' / 90</b>'],['Ağırlıklı net (Türkçe, Mat, Fen × 4)',num(ag,2)+' / 270'],
    ['Tahmini puan','<b>'+num(p,3)+'</b>','hl'],['Aynı netle 2020–2024 aralığı',num(mn,1)+' – '+num(mx,1)]]);
  var tab='<table><thead><tr><th>Model yılı</th><th>Tahmini puan</th></tr></thead><tbody>'+yy.map(function(y,i){return '<tr><td>'+y+'</td><td>'+num(ps[i],2)+'</td></tr>';}).join('')+'</tbody></table>';
  return {main:['Tahmini LGS puanı', num(p,2)], sub:num(top,2)+' net · '+(sec==='ort'?'5 yılın ortalaması':sec+' modeli'), rows:rows, extra:tab,
    note:'Gerçek LGS puanı, o yıl sınava giren tüm öğrencilerin ortalaması ve standart sapmasıyla hesaplanır; bu nedenle sonuç tahminidir. Yüzdelik diliminizi MEB sonuç belgenizden öğrenebilirsiniz.'};
}''',
article=f'''<h2 id="nasil">LGS puanı nasıl hesaplanır?</h2>
<p>Liselere Geçiş Sistemi (LGS) kapsamındaki merkezi sınavda her testin neti, <b>doğru sayısından yanlış sayısının üçte birinin</b> çıkarılmasıyla bulunur; yani 3 yanlış 1 doğruyu götürür. Boş bırakılan sorular nete etki etmez.</p>
<div class="formula">Net = Doğru − (Yanlış ÷ 3)</div>
<p>Netler doğrudan toplanmaz. MEB her testin netini, o yıl sınava giren tüm öğrencilerin ortalaması ve standart sapmasıyla <b>standart puana</b> çevirir; ardından Türkçe, Matematik ve Fen Bilimleri testlerini <b>4</b>, T.C. İnkılap Tarihi ve Atatürkçülük, Din Kültürü ve Ahlak Bilgisi ve Yabancı Dil testlerini <b>1</b> katsayısıyla ağırlıklandırır. Sonuç 100 ile 500 arasındaki merkezi sınav puanına dönüştürülür.</p>
<div class="example"><p><b>Örnek:</b> Türkçe 17, Matematik 15, Fen 16, İnkılap 9, Din 9 ve Yabancı Dil 8 net yapan bir öğrencinin toplam neti 74, ağırlıklı neti 4 × 48 + 26 = 218’dir. 2024 sonuçlarına göre tahmini puanı <b>{_tr(_ORNEK_P, 1)}</b> olur.</p></div>

<h2 id="dagilim">LGS soru dağılımı ve süreler</h2>
<div class="table-wrap"><table><thead><tr><th>Oturum</th><th>Test</th><th>Soru</th><th>Katsayı</th></tr></thead><tbody>
<tr><td rowspan="4">Sözel bölüm<br><small>50 soru · 75 dakika</small></td><td>Türkçe</td><td>20</td><td>4</td></tr>
<tr><td>T.C. İnkılap Tarihi ve Atatürkçülük</td><td>10</td><td>1</td></tr><tr><td>Din Kültürü ve Ahlak Bilgisi</td><td>10</td><td>1</td></tr><tr><td>Yabancı Dil</td><td>10</td><td>1</td></tr>
<tr><td rowspan="2">Sayısal bölüm<br><small>40 soru · 80 dakika</small></td><td>Matematik</td><td>20</td><td>4</td></tr><tr><td>Fen Bilimleri</td><td>20</td><td>4</td></tr>
</tbody></table></div>
<p>Sınav toplam 90 sorudan oluşur ve aynı gün iki oturumda yapılır. Ağırlıklı netin üst sınırı 4 × 60 + 30 = <b>270</b>’tir.</p>

<h2 id="kac-net">LGS’de kaç net kaç puan? (2020–2024 karşılaştırması)</h2>
<p>Aşağıdaki tablo, toplam netin derslere soru sayısıyla orantılı dağıldığı varsayımıyla her yılın sonuçlarına göre tahmini puanı gösterir. Aynı netin yıldan yıla 5–15 puan farklı sonuç verebildiğine dikkat edin; sınav zorlaştıkça aynı net daha yüksek puana karşılık gelir.</p>
{LGS_KN_TABLO}
<p>Netleriniz bir derste yoğunlaşıyorsa puanınız tablodan farklı olabilir; kesin tahmin için yukarıdaki hesaplayıcıya ders bazında doğru ve yanlışlarınızı girin.</p>

<h2 id="net-degeri">Hangi dersin neti daha çok puan getirir?</h2>
<p>Katsayısı 4 olan dersler toplam puanın yaklaşık %80’ini belirler. 2024 modeline göre bir dersteki <b>1 netlik artışın</b> puana etkisi:</p>
{LGS_NET_DEGER}
<p>Yani bir Matematik neti, yaklaşık üç Yabancı Dil netine eşdeğerdir. Hazırlık sürecinde Türkçe, Matematik ve Fen’deki boşlukları kapatmak puanı en hızlı yükselten yoldur; ancak 1 katsayılı derslerdeki kolay netleri kaçırmak da üst dilimlerde sıralamayı belirgin şekilde düşürür.</p>

<h2 id="katsayilar">Yıllara göre net katsayıları</h2>
<p>Hesaplayıcı, MEB’in açıkladığı sonuçlardan türetilen ve her yıl için ayrı hesaplanan doğrusal katsayıları kullanır. Katsayılar, o yıl ilgili testin ne kadar zor geçtiğine (standart sapmasına) göre değişir:</p>
{LGS_KAT_TABLO}
<p>Her yılın satırında tüm sorular doğru yanıtlandığında puan yaklaşık 500’e ulaşır. Matematik katsayısının 2021’de 5,79’a çıkması, o yıl matematik testinin öğrenciler arasında daha ayırt edici olduğunu gösterir.</p>

<h2 id="yuzdelik">Yüzdelik dilim nedir, nasıl hesaplanır?</h2>
<p>Yüzdelik dilim, sıralamanızın sınava giren toplam öğrenci sayısına oranıdır: <b>Yüzdelik dilim = Sıralama ÷ Katılan öğrenci × 100</b>. 2026 LGS’ye <b>994.358</b> öğrenci katıldığına göre ilk %1’lik dilim yaklaşık ilk {_tr(994358 / 100, 0)} öğrenciye, %5’lik dilim ilk {_tr(994358 * 5 / 100, 0)} öğrenciye karşılık gelir. Lise tercihlerinde okulların taban puanı yerine çoğu zaman <b>taban yüzdelik dilimi</b> karşılaştırılır; çünkü yüzdelik dilim, sınavın zorluğundan daha az etkilenir.</p>
<p>2026 LGS’de tam puan (500) alan öğrenci sayısı 452 olarak açıklandı. Bu sayı 2025’te 719, 2024’te 413’tü.</p>

<h2 id="2027">2027 LGS ne zaman?</h2>
<p>LGS her yıl Haziran ayının ilk yarısında, Cumartesi veya Pazar günü tek gün ve iki oturumda yapılır; 2026 sınavı 13 Haziran’da yapıldı ve sonuçlar 10 Temmuz’da açıklandı. 2027 sınav tarihi MEB’in yayımlayacağı “Ortaöğretim Kurumlarına İlişkin Merkezi Sınav Başvuru ve Uygulama Kılavuzu” ile kesinleşecek; Bakanlık sınav sisteminde bir değişiklik olmadığını açıkladı. Sınava kaç gün kaldığını <a href="https://hesaplarsin.com/gun-hesaplama.html">gün hesaplama</a> aracıyla takip edebilirsiniz.</p>

<h2 id="taktik">Deneme sonuçlarını doğru yorumlamak</h2>
<ul>
<li>Tek bir denemeye değil, son 4–5 denemenin ortalamasına bakın; ortalamayı <a href="https://hesaplarsin.com/ortalama-hesaplama.html">ortalama hesaplama</a> ile kolayca bulabilirsiniz.</li>
<li>Yanlış sayınızı düşürmek, yeni doğru eklemek kadar değerlidir: 3 yanlış bir doğruyu götürdüğü için emin olmadığınız soruyu boş bırakmak bazen daha kârlıdır.</li>
<li>Deneme yayınlarının zorluğu MEB sınavından farklı olabilir; puan yerine net gelişiminizi takip edin.</li>
<li>Okul başarı puanı (OBP) LGS yerleştirmesinde kullanılmaz; ancak sınavsız yerleştirmede (adrese dayalı) devamsızlık ve okul puanı önem kazanır.</li>
</ul>''',
faq=[('LGS’de kaç yanlış bir doğruyu götürür?', 'LGS’de 3 yanlış 1 doğruyu götürür. Net, doğru sayısından yanlış sayısının üçte biri çıkarılarak bulunur.'),
     ('LGS puanı en az ve en fazla kaç olur?', 'LGS merkezi sınav puanı 100 ile 500 arasındadır. Tüm soruları doğru yanıtlayan öğrenci 500 puan alır.'),
     ('LGS’de 80 net kaç puan eder?', f'Netlerin derslere orantılı dağıldığı varsayımıyla 80 net, 2024 sonuçlarına göre yaklaşık {_tr(_lgs(_profil(80)), 0)} puana karşılık gelir. Puan, yılın zorluğuna ve netlerin hangi derslerde olduğuna göre değişir.'),
     ('LGS katsayıları nedir?', 'Türkçe, Matematik ve Fen Bilimleri testleri 4; İnkılap Tarihi, Din Kültürü ve Yabancı Dil testleri 1 katsayısıyla ağırlıklandırılır.'),
     ('Aynı net neden farklı yıllarda farklı puan getiriyor?', 'Netler, o yıl sınava giren tüm öğrencilerin ortalaması ve standart sapmasıyla standart puana çevrilir. Sınav zor geçtiğinde ortalama düştüğü için aynı net daha yüksek puana karşılık gelir.'),
     ('2027 LGS ne zaman yapılacak?', 'Kesin tarih MEB’in 2027 kılavuzuyla açıklanacak. LGS geleneksel olarak Haziran ayının ilk yarısında yapılır; 2026 sınavı 13 Haziran’daydı.')],
related=['obp-hesaplama', 'not-ortalamasi-hesaplama', 'takdir-tesekkur-hesaplama', 'tyt-net-hesaplama', 'gun-hesaplama'],
sources=[('MEB ODSGM – Ortaöğretime geçiş', 'https://odsgm.meb.gov.tr/'), ('MEB – 2026 LGS merkezî sınav raporu', 'https://www.meb.gov.tr/2026-lgs-kapsaminda-merkezi-sinav-raporu-yayimlandi/haber/41333/tr')],
badges=['✓ Ücretsiz', '2020–2024 Karşılaştırma', '3 Yanlış 1 Doğru'],
))


# ═════════════════════════ KPSS PUAN ═════════════════════════
# Standart puan zinciri: SP = 50 + 10·(net − ort)/ss ; ASP = 0,5·SP_GY + 0,5·SP_GK ; Puan ≈ a + b·(ASP − 50)
# Lisans: 2026 ÖSYM test ortalamaları (GY 19,43 · GK 20,07 net), 2026 sonuçlarına kalibre. Önlisans/ortaöğretim: 2018 ÖSYM istatistikleri.
KPSS_M = {
    'lisans':   dict(ad='Lisans (P3)', pt='P3', mg=19.43, sg=8.863, mk=20.07, sk=9.5, a=65.595, b=0.78097),
    'onlisans': dict(ad='Önlisans (P93)', pt='P93', mg=15.69, sg=8.24, mk=17.11, sk=9.98, a=66.891, b=0.72496),
    'orta':     dict(ad='Ortaöğretim (P94)', pt='P94', mg=16.23, sg=10.83, mk=16.40, sk=8.51, a=65.474, b=0.78123),
}
def _kp(gy, gk, m):
    m = KPSS_M[m]
    asp = 0.5 * (50 + 10 * (gy - m['mg']) / m['sg']) + 0.5 * (50 + 10 * (gk - m['mk']) / m['sk'])
    return min(100, m['a'] + m['b'] * (asp - 50))
def _kp_ters(hedef, m):
    lo, hi = 0.0, 120.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if _kp(mid / 2, mid / 2, m) < hedef: lo = mid
        else: hi = mid
    return hi
KPSS_KN_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Toplam net (GY + GK)</th><th>P3 (lisans)</th><th>P93 (önlisans)</th><th>P94 (ortaöğretim)</th></tr></thead><tbody>'
                 + ''.join(f'<tr><td>{t} net</td>' + ''.join(f'<td>{_tr(_kp(t / 2, t / 2, m), 1)}</td>' for m in ('lisans', 'onlisans', 'orta')) + '</tr>'
                           for t in (110, 100, 90, 80, 70, 60, 50, 40, 30)) + '</tbody></table></div>')
KPSS_HEDEF_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Hedef puan</th><th>P3 için gereken net</th><th>P93 için</th><th>P94 için</th></tr></thead><tbody>'
                    + ''.join(f'<tr><td>{h}</td>' + ''.join(f'<td>≈ {_tr(_kp_ters(h, m), 0)}</td>' for m in ('lisans', 'onlisans', 'orta')) + '</tr>'
                              for h in (70, 75, 80, 85, 90, 95)) + '</tbody></table></div>')
KPSS_P93_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Toplam net (GY + GK)</th><th>Tahmini P93 (önlisans)</th></tr></thead><tbody>'
                   + ''.join(f'<tr><td>{t} net</td><td>{_tr(_kp(t / 2, t / 2, "onlisans"), 1)}</td></tr>' for t in (110, 100, 90, 85, 80, 75, 70, 65, 60, 50, 40, 30)) + '</tbody></table></div>')
KPSS_JS_M = 'var KM=' + str({k: [v['mg'], v['sg'], v['mk'], v['sk'], v['a'], v['b']] for k, v in KPSS_M.items()}).replace("'", '"') + ';'

TOOLS.append(dict(
slug='kpss-puan-hesaplama', name='KPSS Puan Hesaplama', cat='egitim', ico='🏛️',
title='KPSS Önlisans Puan Hesaplama 2026 (P93) – Lisans P3, Ortaöğretim P94 | Hesaplarsın',
desc=f'KPSS önlisans sonuçları 30 Ekim’de açıklanıyor. Doğru-yanlışlarınızı girin, tahmini P93 puanınızı görün: 80 net ≈ {_tr(_kp(40, 40, "onlisans"), 0)} puan. Lisans (P3) ve ortaöğretim (P94) de hesaplanır.',
h1='🏛️ KPSS Puan Hesaplama 2026 – Önlisans, Lisans, Ortaöğretim',
lead='Genel Yetenek ve Genel Kültür testlerindeki doğru ve yanlış sayılarınızı girin; netlerinizi ve ÖSYM’nin standart puan yöntemiyle tahmini KPSS puanınızı önlisans (P93), lisans (P3) ve ortaöğretim (P94) için anında görün. KPSS önlisans sonuçları 30 Ekim 2026’da açıklanıyor.',
card_title='KPSS Net ve Puan Hesaplayıcı', button='Puanımı Hesapla',
form='''<div class="field full" style="margin-bottom:14px"><label>Sınav düzeyi</label>
<div class="seg"><label><input type="radio" name="duz" value="onlisans" checked>Önlisans (P93)</label><label><input type="radio" name="duz" value="lisans">Lisans (P3)</label><label><input type="radio" name="duz" value="orta">Ortaöğretim (P94)</label></div></div>''' + net_satirlari([('gy', 'Genel Yetenek (Türkçe + Matematik)', 60), ('gk', 'Genel Kültür (Tarih, Coğrafya, Vatandaşlık, Güncel)', 60)]),
js=NET_JS + KPSS_JS_M + r'''
var AD={lisans:['Lisans','P3'],onlisans:['Önlisans','P93'],orta:['Ortaöğretim','P94']};
function kp(gy,gk,m){var k=KM[m];var a=0.5*(50+10*(gy-k[0])/k[1])+0.5*(50+10*(gk-k[2])/k[3]);return Math.min(100,k[4]+k[5]*(a-50));}
function hesapla(){
  var r=netHesap([["gy","Genel Yetenek",60],["gk","Genel Kültür",60]],4); if(r.hata) return r.hata;
  var gy=(v('gyd')||0)-(v('gyy')||0)/4, gk=(v('gkd')||0)-(v('gky')||0)/4, m=radio('duz')||'lisans';
  if(!(v('gyd')||v('gyy')||v('gkd')||v('gky'))) return 'Genel Yetenek ve Genel Kültür doğru-yanlış sayılarınızı girin.';
  if(gy<=0||gk<=0) return 'Puanın hesaplanabilmesi için her iki testte de netinizin 0’dan büyük olması gerekir.';
  var p=kp(gy,gk,m), lo=Math.max(50,p-2), hi=Math.min(100,p+2);
  var rows=r.rows.concat([['<b>Toplam net</b>','<b>'+num(gy+gk,2)+' / 120</b>'],['Tahmini '+AD[m][1]+' puanı','<b>'+num(p,3)+'</b>','hl'],['Olası aralık (±2 puan)',num(lo,1)+' – '+num(hi,1)]]);
  var diger=Object.keys(AD).filter(function(x){return x!==m;}).map(function(x){return [AD[x][0]+' ('+AD[x][1]+') ile aynı net',num(kp(gy,gk,x),2)];});
  return {main:['Tahmini '+AD[m][1]+' puanı', num(p,2)], sub:AD[m][0]+' · '+num(gy+gk,2)+' net (GY '+num(gy,2)+' · GK '+num(gk,2)+')', rows:rows.concat(diger),
    note:'KPSS puanı, o yıl sınava giren tüm adayların test ortalamaları ve standart sapmalarına göre ÖSYM tarafından hesaplanır. Sonuç tahminidir; resmî puanınız ÖSYM sonuç belgenizde yer alır.'};
}''',
article=f'''<h2 id="onlisans">KPSS önlisans puan hesaplama (P93)</h2>
<p>4 Ekim 2026’da yapılan KPSS Önlisans sınavının sonuçları <b>30 Ekim 2026</b>’da açıklanıyor. Önlisans mezunlarının kullandığı puan türü <b>P93</b>’tür; Genel Yetenek ve Genel Kültür testleri %50’şer ağırlıkla hesaba katılır. Yukarıdaki hesaplayıcı önlisans seçili açılır; doğru ve yanlış sayılarınızı girmeniz yeterli.</p>
<p>Netlerin iki teste eşit dağıldığı varsayımıyla tahmini P93 puanları:</p>
{KPSS_P93_TABLO}
<p>Önlisans tahminleri ÖSYM’nin önceki yıllarda yayımladığı önlisans test istatistiklerine dayanır. ÖSYM 2026 önlisans sayısal bilgilerini sonuçlarla birlikte yayımladığında hesaplayıcıyı bu verilerle güncelleyeceğiz; gerçek puanınız birkaç puan farklı çıkabilir.</p>
<h3>KPSS önlisans sonuçları nasıl öğrenilir?</h3>
<p>Sonuçlar ÖSYM’nin <b>sonuc.osym.gov.tr</b> adresinde T.C. kimlik numarası ve aday şifresiyle sorgulanır. Sonuç belgesinde Genel Yetenek ve Genel Kültür netleriniz ile P93 puanınız yer alır. Belgede gördüğünüz netleri buraya girerek hesaplayıcının tahminini kendi gerçek puanınızla karşılaştırabilirsiniz.</p>

<h2 id="nasil">KPSS puanı nasıl hesaplanır?</h2>
<p>KPSS’de her testte <b>4 yanlış 1 doğruyu götürür</b>; net (ham puan) doğru sayısından yanlış sayısının dörtte biri çıkarılarak bulunur. ÖSYM bu netleri doğrudan toplamaz, üç aşamada puana çevirir:</p>
<ol>
<li><b>Standart puan:</b> Her testin neti, o testin Türkiye ortalaması ve standart sapması kullanılarak ortalaması 50, standart sapması 10 olan standart puana dönüştürülür.</li>
<li><b>Ağırlıklı standart puan (ASP):</b> Genel Yetenek ve Genel Kültür standart puanları puan türünün ağırlıklarıyla toplanır. P3, P93 ve P94’te iki test de <b>%50</b> ağırlığa sahiptir.</li>
<li><b>KPSS puanı:</b> ASP, aşağıdaki formülle 100’lük ölçeğe taşınır.</li>
</ol>
<div class="formula">KPSS puanı = 70 + 30 × [2 × (ASP − X) − S] ÷ [2 × (B − X) − S]</div>
<p>Formülde X tüm adayların ASP ortalaması, S standart sapması, B ise en yüksek ASP’dir. Bu değerler sınav bitmeden bilinemediği için sınav öncesi ve sonrası yapılan her hesaplama tahmindir. Hesaplayıcımız 2026 KPSS Lisans test ortalamalarını kullanır ve 2026 sonuçlarına göre ayarlanmıştır.</p>
<div class="example"><p><b>Örnek:</b> Genel Yetenek’te 45 doğru 12 yanlış (42 net), Genel Kültür’de 40 doğru 16 yanlış (36 net) yapan lisans mezunu bir adayın toplam neti 78, tahmini P3 puanı yaklaşık <b>{_tr(_kp(42, 36, 'lisans'), 1)}</b>’dir.</p></div>

<h2 id="kac-net">KPSS’de kaç net kaç puan? (2026 tahmini)</h2>
<p>Netlerin Genel Yetenek ve Genel Kültür’e eşit dağıldığı varsayımıyla tahmini puanlar:</p>
{KPSS_KN_TABLO}
<p>Tablo yaklaşık değerler verir; gerçek puan ±2 puan sapabilir. Netiniz testlerden birinde yoğunlaşıyorsa puanınız biraz farklı çıkar; kendi netlerinizle hesaplamak için yukarıdaki aracı kullanın.</p>

<h2 id="hedef">Hedef puan için kaç net gerekir?</h2>
{KPSS_HEDEF_TABLO}
<p>Atanma için gereken puan kadroya, kuruma, şehre ve ilan edilen kontenjana göre her tercih döneminde değişir. Hedefinizi belirlerken bir önceki tercih döneminin taban puanlarına bakmak en sağlıklı yoldur.</p>

<h2 id="turler">KPSS puan türleri ve ağırlıkları</h2>
<div class="table-wrap"><table><thead><tr><th>Puan türü</th><th>Kimler için</th><th>Genel Yetenek</th><th>Genel Kültür</th></tr></thead><tbody>
<tr><td>P1</td><td>Lisans – bazı özel kadrolar</td><td>%70</td><td>%30</td></tr>
<tr><td>P2</td><td>Lisans – bazı özel kadrolar</td><td>%60</td><td>%40</td></tr>
<tr><td>P3</td><td>Lisans mezunları – B grubu kadroların çoğu</td><td>%50</td><td>%50</td></tr>
<tr><td>P93</td><td>Önlisans mezunları</td><td>%50</td><td>%50</td></tr>
<tr><td>P94</td><td>Ortaöğretim (lise) mezunları</td><td>%50</td><td>%50</td></tr>
</tbody></table></div>
<p>Öğretmen adayları için P10 ve P121 gibi puan türlerinde Eğitim Bilimleri ve Öğretmenlik Alan Bilgisi testleri de hesaba katılır. A grubu kadrolarda ise alan bilgisi testleri kullanılır.</p>

<h2 id="dagilim">Soru dağılımı ve süre</h2>
<p>Lisans, önlisans ve ortaöğretim düzeylerinde Genel Yetenek–Genel Kültür oturumunun yapısı aynıdır; düzeyler arasındaki fark soruların zorluğundadır.</p>
<div class="table-wrap"><table><thead><tr><th>Test</th><th>Ders</th><th>Soru</th></tr></thead><tbody>
<tr><td rowspan="2">Genel Yetenek (60)</td><td>Türkçe</td><td>30</td></tr><tr><td>Matematik (geometri dahil)</td><td>30</td></tr>
<tr><td rowspan="4">Genel Kültür (60)</td><td>Tarih</td><td>27</td></tr><tr><td>Coğrafya</td><td>18</td></tr><tr><td>Vatandaşlık</td><td>9</td></tr><tr><td>Güncel Bilgiler</td><td>6</td></tr>
</tbody></table></div>
<p>Oturum toplam 120 soru ve 130 dakikadır. Ders bazında netlerinizi ayrı ayrı görmek için <a href="https://hesaplarsin.com/kpss-net-hesaplama.html">KPSS net hesaplama</a> aracını kullanabilirsiniz.</p>

<h2 id="2026">2026 KPSS istatistikleri ve takvimi</h2>
<p>6 Eylül 2026’da yapılan KPSS Lisans Genel Yetenek–Genel Kültür oturumuna <b>1.595.476</b> aday katıldı. ÖSYM’nin açıkladığı sayısal bilgilere göre Genel Yetenek ortalaması <b>19,43</b>, Genel Kültür ortalaması <b>20,07</b> net oldu. 2024’te bu ortalamalar 16,73 ve 18,86 netti; ortalamanın yükselmesi, 2026’da aynı netin 2024’e göre biraz daha düşük puana karşılık geldiği anlamına gelir.</p>
<div class="table-wrap"><table><thead><tr><th>Sınav</th><th>Sınav tarihi</th><th>Sonuç tarihi</th></tr></thead><tbody>
<tr><td>KPSS Lisans (GY-GK)</td><td>6 Eylül 2026</td><td>7 Ekim 2026</td></tr>
<tr><td>KPSS Önlisans</td><td>4 Ekim 2026</td><td>30 Ekim 2026</td></tr>
<tr><td>KPSS Ortaöğretim</td><td>25 Ekim 2026</td><td>19 Kasım 2026</td></tr>
<tr><td>KPSS DHBT</td><td>1 Kasım 2026</td><td>25 Kasım 2026</td></tr>
</tbody></table></div>
<p>Tarihler ÖSYM 2026 sınav takvimine göredir. KPSS sonuçları iki yıl geçerlidir; bu nedenle 2026 puanınızla 2028 sınavına kadar yapılan tercihlerde başvurabilirsiniz.</p>
<p><b>2027 KPSS:</b> ÖSYM’nin 2027 takvimine göre A Grubu Genel Yetenek–Genel Kültür oturumu <b>12 Eylül 2027</b>’de, Alan Bilgisi oturumları 18–19 Eylül 2027’de yapılacak; başvurular 8–19 Temmuz 2027, sonuçlar 13 Ekim 2027’de. KPSS önlisans ve ortaöğretim sınavları iki yılda bir yapıldığı için 2027 takviminde yer almıyor; bir sonraki oturumlar 2028’de.</p>''',
faq=[('KPSS’de kaç yanlış bir doğruyu götürür?', 'KPSS’de 4 yanlış 1 doğruyu götürür. Net, doğru sayısından yanlış sayısının dörtte biri çıkarılarak hesaplanır.'),
     ('KPSS önlisansta 70 net kaç puan eder?', f'Netlerin Genel Yetenek ve Genel Kültür’e eşit dağıldığı varsayımıyla 70 net yaklaşık {_tr(_kp(35, 35, "onlisans"), 0)}, 60 net yaklaşık {_tr(_kp(30, 30, "onlisans"), 0)} P93 puanına karşılık gelir. Kesin puanı ÖSYM 30 Ekim 2026’da açıklayacak.'),
     ('KPSS önlisans sonuçları nereden öğrenilir?', 'Sonuçlar ÖSYM’nin sonuc.osym.gov.tr adresinde T.C. kimlik numarası ve aday şifresiyle sorgulanır. Sonuç belgesinde netleriniz ve P93 puanınız yer alır.'),
     ('KPSS’de 80 net kaç puan eder?', f'Netlerin iki teste eşit dağıldığı varsayımıyla 80 net, 2026 verilerine göre yaklaşık {_tr(_kp(40, 40, "lisans"), 0)} P3 puanına karşılık gelir. Önlisansta (P93) yaklaşık {_tr(_kp(40, 40, "onlisans"), 0)}, ortaöğretimde (P94) yaklaşık {_tr(_kp(40, 40, "orta"), 0)} puandır.'),
     ('P3 puanı nasıl hesaplanır?', 'Genel Yetenek ve Genel Kültür netleri standart puana çevrilir, %50–%50 ağırlıkla toplanır ve ÖSYM formülüyle 100’lük ölçeğe taşınır. Tüm adayların sonuçları kullanıldığı için kesin puanı ancak ÖSYM açıklar.'),
     ('KPSS önlisans sonuçları ne zaman açıklanacak?', '4 Ekim 2026’da yapılan KPSS Önlisans sınavının sonuçları ÖSYM takvimine göre 30 Ekim 2026’da açıklanacak.'),
     ('KPSS ortaöğretim sonuçları ne zaman açıklanacak?', '25 Ekim 2026’da yapılan KPSS Ortaöğretim sınavının sonuçları ÖSYM takvimine göre 19 Kasım 2026’da açıklanacak.'),
     ('KPSS puanı kaç yıl geçerli?', 'KPSS sonuçları iki yıl geçerlidir ve bu süre içindeki tercih dönemlerinde kullanılabilir.')],
related=['kpss-net-hesaplama', 'memur-maaslari', 'yas-hesaplama', 'ortalama-hesaplama', 'memur-emekli-zammi-hesaplama'],
sources=[('ÖSYM – KPSS', 'https://www.osym.gov.tr/'), ('ÖSYM – Sınav takvimi', 'https://www.osym.gov.tr/TR,8797/takvim.html')],
badges=['✓ Ücretsiz', 'P3 · P93 · P94', '2026 Verileri'],
))


# ═════════════════════════ ALES PUAN ═════════════════════════
# Net başına katsayılar 2025/2 oturumu sonuçlarından türetilmiştir (sayısal, sözel). Sabit, tam netin 100 puana
# karşılık geldiği varsayımıyla bulunur. 2017 ÖSYM test istatistikleriyle standart puan zinciri bu modelle 1–4 puan içinde örtüşür.
ALES_K = {'SAY': (0.80251, 0.33159), 'SOZ': (0.27064, 1.00642), 'EA': (0.52294, 0.64822)}
ALES_S = {k: 100 - 50 * (a + b) for k, (a, b) in ALES_K.items()}
def _ales(say, soz, t):
    a, b = ALES_K[t]
    return max(0, min(100, ALES_S[t] + a * say + b * soz))
def _ales_ters(h, t):  # iki teste eşit dağıtılmış toplam net
    lo, hi = 0.0, 100.0
    for _ in range(60):
        m = (lo + hi) / 2
        if _ales(m / 2, m / 2, t) < h: lo = m
        else: hi = m
    return hi
ALES_KN = ('<div class="table-wrap"><table><thead><tr><th>Sayısal net</th><th>Sözel net</th><th>SAY</th><th>SÖZ</th><th>EA</th></tr></thead><tbody>'
           + ''.join(f'<tr><td>{s}</td><td>{z}</td>' + ''.join(f'<td>{_tr(_ales(s, z, t), 1)}</td>' for t in ('SAY', 'SOZ', 'EA')) + '</tr>'
                     for s, z in ((10, 15), (15, 15), (15, 25), (20, 20), (20, 30), (25, 25), (30, 20), (30, 30), (35, 35), (40, 40), (45, 45)))
           + '</tbody></table></div>')
ALES_HEDEF = ('<div class="table-wrap"><table><thead><tr><th>Hedef puan</th><th>Ne için gerekir?</th><th>SAY için toplam net</th><th>SÖZ için</th><th>EA için</th></tr></thead><tbody>'
              + ''.join(f'<tr><td>{h}</td><td>{d}</td>' + ''.join(f'<td>≈ {_tr(_ales_ters(h, t), 0)}</td>' for t in ('SAY', 'SOZ', 'EA')) + '</tr>'
                        for h, d in ((55, 'Tezli yüksek lisans ve doktora (asgari)'), (70, 'Araştırma ve öğretim görevlisi kadroları'), (80, 'Lisans derecesiyle doktora'), (90, 'Rekabetçi programlar ve burslar')))
              + '</tbody></table></div>')
ALES_JS = 'var AK=' + str({k: [ALES_S[k], *v] for k, v in ALES_K.items()}).replace("'", '"') + ';'

TOOLS.append(dict(
slug='ales-puan-hesaplama', name='ALES Puan Hesaplama', cat='egitim', ico='🎓',
title='ALES Puan Hesaplama 2026 – Sayısal, Sözel, Eşit Ağırlık Puanı | Hesaplarsın',
desc='ALES sayısal ve sözel doğru-yanlışlarınızı girin; netlerinizi ve tahmini SAY, SÖZ, EA puanlarınızı görün. Yüksek lisans (55), araştırma görevlisi (70) ve doktora barajlarıyla karşılaştırın.',
h1='🎓 ALES Puan Hesaplama 2026',
lead='Akademik Personel ve Lisansüstü Eğitime Giriş Sınavı (ALES) sayısal ve sözel testlerindeki doğru ve yanlış sayılarınızı girin; netlerinizi, tahmini sayısal (SAY), sözel (SÖZ) ve eşit ağırlık (EA) puanlarınızı ve hangi başvurular için yeterli olduğunu anında görün.',
card_title='ALES Net ve Puan Hesaplayıcı', button='Puanımı Hesapla',
form=net_satirlari([('say', 'Sayısal test', 50), ('soz', 'Sözel test', 50)]),
js=NET_JS + ALES_JS + r'''
function ap(s,z,t){var k=AK[t];return Math.max(0,Math.min(100,k[0]+k[1]*s+k[2]*z));}
function hesapla(){
  var r=netHesap([["say","Sayısal",50],["soz","Sözel",50]],4); if(r.hata) return r.hata;
  if(!(v('sayd')||v('sayy')||v('sozd')||v('sozy'))) return 'Sayısal ve sözel doğru-yanlış sayılarınızı girin.';
  var s=(v('sayd')||0)-(v('sayy')||0)/4, z=(v('sozd')||0)-(v('sozy')||0)/4;
  var p={SAY:ap(s,z,'SAY'),SOZ:ap(s,z,'SOZ'),EA:ap(s,z,'EA')}, best=['SAY','SOZ','EA'].sort(function(a,b){return p[b]-p[a];})[0];
  var ad={SAY:'Sayısal (SAY)',SOZ:'Sözel (SÖZ)',EA:'Eşit ağırlık (EA)'};
  function dur(x){return x>=80?'Lisans derecesiyle doktora dahil tüm eşikleri geçiyor':x>=70?'Araştırma görevlisi (70) eşiğini geçiyor':x>=55?'Yüksek lisans ve doktora (55) eşiğini geçiyor':'55 eşiğinin altında';}
  var rows=r.rows.concat([['<b>Toplam net</b>','<b>'+num(s+z,2)+' / 100</b>']]);
  ['SAY','SOZ','EA'].forEach(function(t){rows.push([ad[t]+' puanı','<b>'+num(p[t],2)+'</b> <small style="color:var(--muted)">('+num(Math.max(0,p[t]-4),1)+'–'+num(Math.min(100,p[t]+4),1)+')</small>',t===best?'hl':'']);});
  rows.push(['En yüksek puan türünüze göre',dur(p[best])]);
  return {main:['Tahmini '+ad[best]+' puanı', num(p[best],2)], sub:'Sayısal '+num(s,2)+' · Sözel '+num(z,2)+' net', rows:rows,
    note:'ALES puanı, o oturuma giren tüm adayların ortalaması ve standart sapmasıyla hesaplanır; sonuç tahminidir ve ±4 puan sapabilir. Başvuracağınız programın istediği puan türünü ilandan kontrol edin.'};
}''',
article=f'''<h2 id="nasil">ALES puanı nasıl hesaplanır?</h2>
<p>ALES, ÖSYM tarafından yılda üç kez yapılan, <b>50 sayısal ve 50 sözel</b> sorudan oluşan bir sınavdır. Her testte <b>4 yanlış 1 doğruyu götürür</b>. Netler doğrudan toplanmaz; ÖSYM her testin netini o oturumun ortalaması ve standart sapmasıyla ortalaması 50, standart sapması 10 olan standart puana çevirir. Ardından puan türüne göre ağırlıklandırır:</p>
<div class="table-wrap"><table><thead><tr><th>Puan türü</th><th>Sayısal testin ağırlığı</th><th>Sözel testin ağırlığı</th><th>Genellikle istenen alanlar</th></tr></thead><tbody>
<tr><td>Sayısal (SAY)</td><td>%75</td><td>%25</td><td>Mühendislik, fen bilimleri, tıp temel bilimleri</td></tr>
<tr><td>Sözel (SÖZ)</td><td>%25</td><td>%75</td><td>Edebiyat, tarih, dil, hukuk ve ilahiyat programları</td></tr>
<tr><td>Eşit ağırlık (EA)</td><td>%50</td><td>%50</td><td>İşletme, iktisat, eğitim, psikoloji, sosyal bilimler</td></tr>
</tbody></table></div>
<p>Son olarak ağırlıklı puan, KPSS ve diğer ÖSYM sınavlarındaki yöntemle 100 üzerinden puana dönüştürülür:</p>
<div class="formula">ALES puanı = 70 + 30 × [2 × (AP − X) − S] ÷ [2 × (B − X) − S]</div>
<p>Formülde AP adayın ağırlıklı puanı, X tüm adayların ortalaması, S standart sapması, B ise en yüksek ağırlıklı puandır. Bu değerler sınavdan sonra belli olduğu için her hesaplama tahmindir. Hesaplayıcımız, geçmiş oturum sonuçlarından türetilen net katsayılarını kullanır.</p>

<h2 id="kac-net">ALES’te kaç net kaç puan?</h2>
{ALES_KN}
<p>Aynı toplam nette, ağırlığı yüksek testteki net puanı daha çok artırır: sayısal ağırlıklı puanda 1 sayısal net yaklaşık {_tr(ALES_K['SAY'][0], 2)}, 1 sözel net yaklaşık {_tr(ALES_K['SAY'][1], 2)} puan getirir. Sözel puanda ise 1 sözel net yaklaşık {_tr(ALES_K['SOZ'][1], 2)} puan değerindedir.</p>

<h2 id="baraj">ALES’te kaç puan gerekir?</h2>
{ALES_HEDEF}
<p>Lisansüstü Eğitim ve Öğretim Yönetmeliği’ne göre tezli yüksek lisans ve doktora programlarına başvuruda ilgili puan türünde en az <b>55</b>, lisans derecesiyle doktoraya başvuruda en az <b>80</b> puan aranır; tezsiz yüksek lisansta ALES şartı yoktur. Araştırma görevlisi ve öğretim görevlisi kadrolarında ise en az <b>70</b> puan istenir. Üniversiteler bu eşiklerin üzerinde puan isteyebilir ve programa göre puan türü belirler; başvurmadan önce ilanı kontrol edin. Tablodaki net değerleri iki teste eşit dağıtılmış toplam netlerdir.</p>

<h2 id="tarih">2026 ALES/3 ne zaman?</h2>
<div class="table-wrap"><table><thead><tr><th>Aşama</th><th>Tarih</th></tr></thead><tbody>
<tr><td>Başvuru</td><td>7–15 Ekim 2026 (geç başvuru 21 Ekim)</td></tr>
<tr><td>Sınav</td><td>29 Kasım 2026, Pazar</td></tr>
<tr><td>Sonuç</td><td>17 Aralık 2026</td></tr>
</tbody></table></div>
<h3>2027 ALES tarihleri</h3>
<div class="table-wrap"><table><thead><tr><th>Oturum</th><th>Başvuru</th><th>Sınav</th><th>Sonuç</th></tr></thead><tbody>
<tr><td>ALES/1</td><td>24 Şubat – 4 Mart 2027</td><td>18 Nisan 2027</td><td>7 Mayıs 2027</td></tr>
<tr><td>ALES/2</td><td>25 Mayıs – 2 Haziran 2027</td><td>11 Temmuz 2027</td><td>30 Temmuz 2027</td></tr>
<tr><td>ALES/3</td><td>12–20 Ekim 2027</td><td>28 Kasım 2027</td><td>17 Aralık 2027</td></tr>
</tbody></table></div>
<p>2027 tarihleri ÖSYM’nin 28 Ekim 2026’da yayımladığı 2027 sınav takvimine göredir; ÖSYM takvimde değişiklik yapabilir. ALES sonuçları açıklandığı tarihten itibaren <b>5 yıl</b> geçerlidir. Birden fazla oturuma girdiyseniz başvuruda en yüksek geçerli puanınızı kullanabilirsiniz. Sınava kaç gün kaldığını <a href="https://hesaplarsin.com/gun-hesaplama.html">gün hesaplama</a> aracıyla takip edebilirsiniz.</p>

<h2 id="taktik">ALES’e hazırlanırken</h2>
<ul>
<li>Hedef programınızın puan türünü önce öğrenin: EA isteyen bir programa başvuracaksanız sayısal ve sözel testlere eşit zaman ayırın.</li>
<li>Sayısal testte sayısal mantık ve problem soruları, sözel testte paragraf ve sözel mantık soruları belirleyicidir.</li>
<li>4 yanlış 1 doğruyu götürdüğü için emin olmadığınız soruları boş bırakmak çoğu zaman daha kârlıdır.</li>
<li>Yabancı dil şartı için YDS veya YÖKDİL puanınızı da kontrol edin; doktora ve kadro ilanlarında genellikle ayrıca aranır.</li>
</ul>''',
faq=[('ALES’te kaç yanlış bir doğruyu götürür?', 'ALES’te 4 yanlış 1 doğruyu götürür. Net, doğru sayısından yanlış sayısının dörtte biri çıkarılarak bulunur.'),
     ('ALES’te 60 net kaç puan eder?', f'Netlerin iki teste eşit dağıldığı varsayımıyla 60 net (30 sayısal + 30 sözel) yaklaşık {_tr(_ales(30, 30, "SAY"), 0)} SAY, {_tr(_ales(30, 30, "SOZ"), 0)} SÖZ ve {_tr(_ales(30, 30, "EA"), 0)} EA puanına karşılık gelir. Gerçek puan oturumun zorluğuna göre ±4 puan değişebilir.'),
     ('Yüksek lisans için ALES kaç olmalı?', 'Tezli yüksek lisansta ilgili puan türünde en az 55 puan aranır. Tezsiz yüksek lisans programlarında ALES şartı yoktur. Üniversiteler daha yüksek puan isteyebilir.'),
     ('Araştırma görevlisi olmak için ALES kaç gerekir?', 'Araştırma görevlisi ve öğretim görevlisi kadrolarında ilgili puan türünde en az 70 ALES puanı aranır.'),
     ('2027’de ALES ne zaman?', 'ÖSYM’nin 2027 takvimine göre ALES/1 18 Nisan, ALES/2 11 Temmuz, ALES/3 28 Kasım 2027’de yapılacak.'),
     ('2026 ALES/3 sonuçları ne zaman açıklanacak?', '29 Kasım 2026’da yapılacak ALES/3 sınavının sonuçları ÖSYM takvimine göre 17 Aralık 2026’da açıklanacak.'),
     ('ALES puanı kaç yıl geçerli?', 'ALES sonuçları açıklandığı tarihten itibaren 5 yıl geçerlidir.')],
related=['kpss-puan-hesaplama', 'kpss-net-hesaplama', 'not-ortalamasi-hesaplama', 'gun-hesaplama', 'obp-hesaplama'],
sources=[('ÖSYM – ALES', 'https://www.osym.gov.tr/'), ('YÖK – Lisansüstü Eğitim ve Öğretim Yönetmeliği', 'https://www.mevzuat.gov.tr/')],
badges=['✓ Ücretsiz', 'SAY · SÖZ · EA', 'ALES/3 29 Kasım'],
))
