"""Finans, işletme, gayrimenkul ve maaş hesaplamaları."""

TOOLS = []

# ───────────────────────── KREDİ ERKEN KAPAMA ─────────────────────────
TOOLS.append(dict(
slug='kredi-erken-kapama-hesaplama', name='Kredi Erken Kapama Hesaplama', cat='finans', ico='🔓',
title='Kredi Erken Kapama Hesaplama 2026 – Kapatma Tutarı ve Faiz Kazancı | Hesaplarsın',
desc='Kredinizi erken kapatırsanız ne kadar ödeyeceğinizi ve ne kadar faizden kurtulacağınızı hesaplayın. İhtiyaç, taşıt ve konut kredisi; erken ödeme tazminatı dahil.',
h1='🔓 Kredi Erken Kapama Hesaplama',
lead='Kredi tutarı, faiz oranı, vade ve ödediğiniz taksit sayısını girin; bugün kapatırsanız ödeyeceğiniz tutarı, varsa erken ödeme tazminatını ve kazancınızı görün.',
form='''<div class="form-grid">
<div class="field"><label for="tutar">Çekilen Kredi Tutarı (₺)</label><input type="number" id="tutar" placeholder="örn: 300.000" inputmode="decimal"></div>
<div class="field"><label for="faiz">Aylık Akdi Faiz (%)</label><input type="number" id="faiz" placeholder="örn: 3,49" inputmode="decimal"></div>
<div class="field"><label for="vade">Vade (ay)</label><input type="number" id="vade" placeholder="örn: 36" inputmode="numeric"></div>
<div class="field"><label for="odenen">Ödenen Taksit Sayısı</label><input type="number" id="odenen" placeholder="örn: 12" inputmode="numeric"></div>
<div class="field full"><label for="tur">Kredi Türü</label><select id="tur">
<option value="ihtiyac">İhtiyaç / taşıt kredisi (BSMV %15 + KKDF %15)</option>
<option value="konut-sabit">Konut kredisi – sabit faiz (vergi yok, tazminat %1–2)</option>
<option value="konut-degisken">Konut kredisi – değişken faiz (tazminat yok)</option></select></div>
</div>''',
js=r'''
function hesapla(){
  var P=v('tutar'), r0=v('faiz')/100, n=Math.round(v('vade')), k=Math.round(v('odenen')), tur=el('tur').value;
  if(!(P>0)||!(r0>0)||!(n>0)) return 'Kredi tutarı, faiz ve vadeyi girin.'; if(!(k>=0&&k<n)) return 'Ödenen taksit sayısı vadeden küçük olmalı.';
  var vergi=tur==='ihtiyac'?0.30:0, r=r0*(1+vergi);
  var taksit=P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1);
  var kalan=P*(Math.pow(1+r,n)-Math.pow(1+r,k))/(Math.pow(1+r,n)-1);
  var kalanVade=n-k, tazOran=tur==='konut-sabit'?(kalanVade>36?0.02:0.01):0, taz=kalan*tazOran;
  var kapama=kalan+taz, kalanTaksitler=taksit*kalanVade, kazanc=kalanTaksitler-kapama;
  return {main:['Erken kapama tutarı', tl(kapama)], sub:'Kalan '+kalanVade+' taksit yerine tek seferde ödenecek tutar',
    rows:[['Aylık taksit (vergiler dahil)',tl(taksit)],['Kalan anapara',tl(kalan)],['Erken ödeme tazminatı'+(tazOran?' (%'+(tazOran*100)+')':''),tl(taz)],
      ['Kalan taksitlerin toplamı',tl(kalanTaksitler)],['Faizden tasarruf',tl(kazanc),'hl'],['Toplam geri ödeme (kredinin tamamı)',tl(taksit*n)]],
    note:'Tutar, son taksit tarihinde kapatma varsayımıyla hesaplanır. Taksit tarihleri arasında kapatırsanız işlemiş günlük faiz eklenir; kesin tutarı bankanızdan “kapama tutarı” olarak isteyin.'};
}''',
article='''
<h2 id="nedir">Kredi erken kapama nedir?</h2>
<p>Kredi erken kapama, vadesi henüz dolmamış bir kredinin kalan borcunun tek seferde ödenmesidir. Türkiye’de 6502 sayılı Tüketicinin Korunması Hakkında Kanun’a göre tüketiciler kredilerini istedikleri zaman kısmen veya tamamen erken ödeyebilir; banka bunu reddedemez. Erken ödemede banka, ödenmeyen <b>gelecek dönem faizlerini</b> ve bunlara bağlı vergileri tahsil edemez. Yani yalnızca kalan anaparayı ödersiniz.</p>

<h2 id="nasil">Erken kapama tutarı nasıl hesaplanır?</h2>
<p>Eşit taksitli kredilerde her taksit, faiz ve anapara bölümünden oluşur. İlk aylarda taksitlerin büyük kısmı faizdir; vade ilerledikçe anapara payı artar. Erken kapamada ödenecek tutar, son ödenen taksitten sonraki <b>kalan anapara</b>dır.</p>
<div class="formula">Taksit = P × r × (1+r)ⁿ ÷ [(1+r)ⁿ − 1]<br>Kalan anapara (k taksit sonra) = P × [(1+r)ⁿ − (1+r)ᵏ] ÷ [(1+r)ⁿ − 1]</div>
<p>Burada P kredi tutarı, n vade, k ödenen taksit sayısı ve r vergiler dahil aylık faiz oranıdır. İhtiyaç ve taşıt kredilerinde faiz üzerinden %15 BSMV ve %15 KKDF alındığından r = faiz × 1,30’dur. Konut kredileri bu vergilerden muaftır.</p>
<div class="example"><p><b>Örnek:</b> 300.000 ₺, aylık %3,49 faiz, 36 ay vadeli ihtiyaç kredisi; 12 taksit ödendikten sonra kapatılırsa:</p>
<p>Vergili aylık oran %4,537 → Taksit ≈ 17.066 ₺. 12. taksitten sonra kalan anapara ≈ <b>246.464 ₺</b>. Kalan 24 taksitin toplamı ≈ 409.575 ₺ olduğundan erken kapamayla yaklaşık <b>163.000 ₺</b> faiz ve vergi ödenmemiş olur.</p></div>

<h2 id="tazminat">Erken ödeme tazminatı (kapama cezası) var mı?</h2>
<div class="table-wrap"><table><thead><tr><th>Kredi türü</th><th>Erken ödeme tazminatı</th></tr></thead><tbody>
<tr><td>İhtiyaç, taşıt ve diğer tüketici kredileri</td><td>Alınamaz</td></tr>
<tr><td>Konut kredisi – sabit faiz, kalan vade 36 ay veya az</td><td>Erken ödenen tutarın en fazla %1’i</td></tr>
<tr><td>Konut kredisi – sabit faiz, kalan vade 36 aydan fazla</td><td>Erken ödenen tutarın en fazla %2’si</td></tr>
<tr><td>Konut kredisi – değişken faiz</td><td>Alınamaz</td></tr>
<tr><td>Ticari / KOBİ kredileri</td><td>Sözleşmeye göre (6502 kapsamı dışında)</td></tr>
</tbody></table></div>
<p>Konut kredilerinde tazminat ancak sözleşmede hüküm varsa istenebilir ve tüketiciye yapılan toplam faiz indirimini aşamaz.</p>

<h2 id="mantikli-mi">Krediyi erken kapatmak mantıklı mı?</h2>
<ul>
<li><b>Kredinin ilk yarısında</b> kapatmak, faiz tasarrufu açısından en avantajlı dönemdir; son taksitlere yaklaştıkça taksitler çoğunlukla anaparadır ve kazanç azalır.</li>
<li><b>Alternatif getiri:</b> Elinizdeki parayı vadeli mevduatta değerlendirirseniz kazanacağınız net faizi <a href="/mevduat-faizi-hesaplama.html">mevduat faizi hesaplama</a> ile karşılaştırın. Kredi faizi (vergiler dahil) mevduatın net getirisinden yüksekse kapatmak genellikle daha kazançlıdır.</li>
<li><b>Acil durum fonu:</b> Tüm birikiminizi krediye yatırmadan önce birkaç aylık giderinizi kenarda bırakın.</li>
<li><b>Kısmi erken ödeme:</b> Tamamını kapatamıyorsanız ara ödeme yaparak taksit tutarını veya vadeyi düşürebilirsiniz.</li>
</ul>
<p>Yeni bir kredinin taksitlerini hesaplamak için <a href="/kredi-hesaplama.html">kredi hesaplama</a>, birden fazla borcu planlamak için <a href="/borc-kapatma-hesaplama.html">borç kapatma hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('Krediyi erken kapatınca faiz iadesi alınır mı?','Gelecek taksitlerin içindeki faiz hiç tahsil edilmez; yalnızca kalan anaparayı ve kapama gününe kadar işlemiş faizi ödersiniz. Bu nedenle ayrıca bir “iade” süreci yoktur.'),
('İhtiyaç kredisi erken kapatma cezası var mı?','Hayır. 6502 sayılı Kanun kapsamındaki ihtiyaç ve taşıt kredilerinde erken ödeme tazminatı alınamaz.'),
('Konut kredisi erken kapatma cezası ne kadar?','Sabit faizli konut kredilerinde kalan vade 36 ay ve altındaysa en fazla %1, 36 aydan fazlaysa en fazla %2 tazminat alınabilir. Değişken faizlide tazminat alınamaz.'),
('Kredi kapatma tutarını nereden öğrenirim?','Banka şubesi, internet/mobil bankacılık veya müşteri hizmetlerinden kapama tutarını isteyebilirsiniz. Tutar ödeme gününe göre değiştiği için güncel tarihle sorun.'),
('Kısmi erken ödeme yapabilir miyim?','Evet. Kısmi ödemede kalan anapara düşer; banka taksit tutarını azaltır veya vadeyi kısaltır. Hangisinin uygulanacağını bankanızla belirleyin.'),
],
related=['kredi-hesaplama','borc-kapatma-hesaplama','mevduat-faizi-hesaplama','arac-kredisi-hesaplama','kredi-karti-asgari-odeme-hesaplama'],
sources=[('6502 sayılı Tüketicinin Korunması Hakkında Kanun','https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6502.pdf')],
))

# ───────────────────────── ROI ─────────────────────────
TOOLS.append(dict(
slug='roi-hesaplama', name='ROI Hesaplama', cat='finans', ico='🎯',
title='ROI Hesaplama – Yatırım Getirisi Oranı (Yıllık ROI Dahil) | Hesaplarsın',
desc='Yatırım maliyeti ve elde edilen kazançla ROI (yatırım getirisi) oranını, net kârı ve yıllıklandırılmış getiriyi hesaplayın. Reklam ve pazarlama ROI’si için de uygun.',
h1='🎯 ROI Hesaplama – Yatırım Getirisi Oranı',
lead='Bir yatırımın, kampanyanın veya projenin size ne kazandırdığını yüzde olarak görün. Süre girerseniz yıllık getiri (CAGR) de hesaplanır.',
form='''<div class="form-grid">
<div class="field"><label for="maliyet">Yatırım Maliyeti (₺)</label><input type="number" id="maliyet" placeholder="örn: 50.000" inputmode="decimal"></div>
<div class="field"><label for="getiri">Toplam Dönüş / Satış Değeri (₺)</label><input type="number" id="getiri" placeholder="örn: 68.000" inputmode="decimal"></div>
<div class="field"><label for="ek">Ek Masraflar (₺) <small>isteğe bağlı</small></label><input type="number" id="ek" placeholder="komisyon, vergi vb." inputmode="decimal"></div>
<div class="field"><label for="sure">Yatırım Süresi (ay) <small>isteğe bağlı</small></label><input type="number" id="sure" placeholder="örn: 18" inputmode="numeric"></div>
</div>''',
js=r'''
function hesapla(){
  var m=v('maliyet'), g=v('getiri'), e=v('ek')||0, s=v('sure');
  if(!(m>0)||isNaN(g)) return 'Maliyet ve dönüş tutarını girin.';
  var top=m+e, kar=g-top, roi=kar/top*100, rows=[['Toplam yatırım',tl(top)],['Net kâr / zarar',tl(kar),kar>=0?'hl':'neg'],['Kazanç katsayısı',num(g/top,2)+'x']];
  if(s>0){var y=(Math.pow(g/top,12/s)-1)*100; rows.push(['Yıllık getiri (CAGR)',pct(y)]); rows.push(['Aylık ortalama getiri',pct((Math.pow(g/top,1/s)-1)*100)]);}
  return {main:['ROI (yatırım getirisi)', pct(roi)], sub:kar>=0?'Yatırım kârlı':'Yatırım zararda', rows:rows};
}''',
article='''
<h2 id="nedir">ROI nedir?</h2>
<p>ROI (Return on Investment – yatırımın getirisi), bir yatırımdan elde edilen net kazancın yatırım maliyetine oranıdır. Hisse senedi, gayrimenkul, makine alımı, reklam kampanyası veya bir eğitim programı gibi farklı yatırımların verimliliğini karşılaştırmak için kullanılan en yaygın ölçüttür.</p>
<div class="formula">ROI (%) = (Toplam dönüş − Toplam maliyet) ÷ Toplam maliyet × 100</div>
<div class="example"><p><b>Örnek:</b> 50.000 ₺’ye alınan ve 18 ay sonra 68.000 ₺’ye satılan bir yatırım:</p><p>(68.000 − 50.000) ÷ 50.000 × 100 = <b>%36 ROI</b>. Yıllık bazda (CAGR) ≈ %22,8.</p></div>

<h2 id="yillik">Yıllık ROI neden önemli?</h2>
<p>Basit ROI süreyi hesaba katmaz. 3 yılda %36 getiri ile 1 yılda %36 getiri aynı değildir. Farklı sürelerdeki yatırımları karşılaştırmak için yıllıklandırılmış getiri (CAGR) kullanılır:</p>
<div class="formula">Yıllık getiri = (Dönüş ÷ Maliyet)^(12 ÷ ay) − 1</div>
<p>Yüksek enflasyon dönemlerinde getirinizi enflasyonla karşılaştırmayı unutmayın; reel getiriyi görmek için <a href="/enflasyon-hesaplama.html">enflasyon hesaplama</a> aracından yararlanabilirsiniz.</p>

<h2 id="pazarlama">Reklam ve pazarlama ROI’si nasıl hesaplanır?</h2>
<p>Dijital pazarlamada ROI, kampanyanın getirdiği brüt kâr ile reklam harcaması karşılaştırılarak hesaplanır. Ciroyu değil kârı kullanmak önemlidir; aksi halde ürün maliyetleri göz ardı edilir. Reklamlarda sık kullanılan bir başka ölçüt <b>ROAS</b>’tır (reklam harcamasının getirisi = ciro ÷ reklam harcaması).</p>
<div class="table-wrap"><table><thead><tr><th>Ölçüt</th><th>Formül</th><th>Ne gösterir?</th></tr></thead><tbody>
<tr><td>ROI</td><td>(Kâr − Maliyet) ÷ Maliyet</td><td>Yatırımın gerçek kârlılığı</td></tr>
<tr><td>ROAS</td><td>Ciro ÷ Reklam harcaması</td><td>Her 1 ₺ reklamın getirdiği satış</td></tr>
<tr><td>ROE</td><td>Net kâr ÷ Özkaynak</td><td>Ortakların sermayesinin verimi</td></tr>
</tbody></table></div>

<h2 id="sinirlar">ROI’nin sınırları</h2>
<ul>
<li>Riski ölçmez: aynı ROI’ye sahip iki yatırımdan biri çok daha riskli olabilir.</li>
<li>Paranın zaman değerini dikkate almaz; nakit akışlı projelerde net bugünkü değer (NBD) ve iç verim oranı (İVO) daha doğru sonuç verir.</li>
<li>Gizli maliyetler (vergi, komisyon, bakım) eklenmezse ROI olduğundan yüksek görünür.</li>
</ul>
<p>Yatırımın kendini kaç yılda amorti edeceğini görmek için <a href="/yatirim-geri-donus-suresi-hesaplama.html">yatırım geri dönüş süresi hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('İyi bir ROI oranı kaçtır?','Sektöre, riske ve süreye göre değişir. Genel kural olarak getirinin aynı dönemdeki enflasyon ve risksiz mevduat getirisinin üzerinde olması beklenir.'),
('Negatif ROI ne demektir?','Yatırımdan elde edilen dönüşün maliyetten düşük olduğunu, yani zarar edildiğini gösterir.'),
('ROI ile ROAS arasındaki fark nedir?','ROI net kârlılığı ölçer; ROAS ise yalnızca reklam harcamasına karşılık elde edilen ciroyu gösterir ve ürün maliyetlerini hesaba katmaz.'),
('ROI hesaplamasına vergi dahil edilmeli mi?','Evet. Gerçekçi bir sonuç için komisyon, vergi ve diğer masrafları “ek masraflar” alanına girin.'),
],
related=['yatirim-geri-donus-suresi-hesaplama','bilesik-faiz','kar-marji-hesaplama','net-kar-hesaplama','enflasyon-hesaplama'],
))

# ───────────────────────── YATIRIM GERİ DÖNÜŞ ─────────────────────────
TOOLS.append(dict(
slug='yatirim-geri-donus-suresi-hesaplama', name='Yatırım Geri Dönüş Süresi Hesaplama', cat='finans', ico='⏳',
title='Yatırım Geri Dönüş Süresi Hesaplama – Kaç Yılda Kendini Öder? | Hesaplarsın',
desc='1.000.000 TL’lik yatırım ayda 25.000 TL getiriyorsa 40 ayda (3,3 yıl) amorti eder. Dükkân, ev veya makine yatırımınızın geri dönüş süresini hesaplayın.',
h1='⏳ Yatırım Geri Dönüş Süresi Hesaplama',
lead='Bir dükkân, makine, güneş paneli ya da kiralık daire yatırımının kendini ne zaman amorti edeceğini hesaplayın. Yıllık artış oranı girerseniz büyüyen nakit akışı da hesaba katılır.',
form='''<div class="form-grid">
<div class="field"><label for="yatirim">Yatırım Tutarı (₺)</label><input type="number" id="yatirim" placeholder="örn: 1.200.000" inputmode="decimal"></div>
<div class="field"><label for="nakit">Aylık Net Nakit Girişi (₺)</label><input type="number" id="nakit" placeholder="gelir − gider, örn: 25.000" inputmode="decimal"></div>
<div class="field"><label for="artis">Yıllık Nakit Artışı (%) <small>isteğe bağlı</small></label><input type="number" id="artis" placeholder="örn: 25 (kira artışı)" inputmode="decimal"></div>
<div class="field"><label for="iskonto">Yıllık İskonto Oranı (%) <small>isteğe bağlı</small></label><input type="number" id="iskonto" placeholder="örn: 30" inputmode="decimal"></div>
</div>''',
js=r'''
function hesapla(){
  var I=v('yatirim'), c=v('nakit'), g=(v('artis')||0)/100, d=(v('iskonto')||0)/100;
  if(!(I>0)||!(c>0)) return 'Yatırım tutarını ve aylık net nakit girişini girin.';
  var basit=I/c, top=0, disk=0, ay=0, aydisk=null, tablo=[];
  for(var m=1;m<=600;m++){var nak=c*Math.pow(1+g,Math.floor((m-1)/12)); top+=nak; disk+=nak/Math.pow(1+d,m/12);
    if(!ay&&top>=I) ay=m; if(aydisk===null&&disk>=I) aydisk=m; if(m%12===0&&m<=120) tablo.push('<tr><td>'+(m/12)+'. yıl</td><td>'+tl(top,0)+'</td><td>'+(top>=I?'✅':'%'+num(top/I*100,0))+'</td></tr>'); if(ay&&(aydisk||!d)&&m>=120) break;}
  var f=function(x){return x?Math.floor(x/12)+' yıl '+(x%12)+' ay':'50 yıldan uzun';};
  return {main:['Geri dönüş süresi', f(ay)], sub:'Basit hesap (sabit nakit): '+num(basit,1)+' ay ≈ '+num(basit/12,1)+' yıl',
    rows:[['Yıllık nakit girişi (ilk yıl)',tl(c*12)],['Yıllık basit getiri oranı',pct(c*12/I*100)],['Kira çarpanı / amortisman (ay)',num(basit,0)+' ay']].concat(d?[['İskontolu geri dönüş süresi',f(aydisk)]]:[]),
    extra:'<table><thead><tr><th>Yıl</th><th>Birikimli nakit</th><th>Durum</th></tr></thead><tbody>'+tablo.join('')+'</tbody></table>'};
}''',
article='''
<h2 id="nedir">Geri dönüş (geri ödeme) süresi nedir?</h2>
<p>Yatırımın geri dönüş süresi (payback period), başlangıçta harcanan paranın yatırımın ürettiği net nakit girişleriyle ne kadar sürede geri kazanılacağını gösterir. Halk arasında “kendini kaç yılda amorti eder?” sorusunun cevabıdır. Küçük işletmeler, gayrimenkul yatırımcıları ve enerji yatırımları (güneş paneli gibi) için en pratik karar ölçütlerinden biridir.</p>
<div class="formula">Basit geri dönüş süresi = Yatırım tutarı ÷ Dönemlik net nakit girişi</div>
<div class="example"><p><b>Örnek:</b> 1.200.000 ₺’lik bir dükkândan ayda 25.000 ₺ net kira alınıyorsa: 1.200.000 ÷ 25.000 = <b>48 ay (4 yıl)</b>. Kira her yıl %25 artarsa süre yaklaşık 3 yıl 2 aya düşer.</p></div>

<h2 id="net-nakit">Net nakit girişi nasıl bulunur?</h2>
<p>Hesaplamada ciroyu değil, tüm giderler düşüldükten sonra elinize kalan net nakdi kullanın. Gayrimenkulde aidat, bakım, emlak vergisi ve kira gelir vergisi; işletmede personel, kira, enerji ve vergiler düşülmelidir. Net kârınızı <a href="/net-kar-hesaplama.html">net kâr hesaplama</a> aracıyla bulabilirsiniz.</p>

<h2 id="iskontolu">İskontolu geri dönüş süresi</h2>
<p>Yüksek enflasyon ve faiz ortamında bugünkü 1 ₺ ile 3 yıl sonraki 1 ₺ aynı değeri taşımaz. İskontolu geri dönüş süresi, gelecekteki nakit girişlerini belirlediğiniz iskonto oranıyla bugüne indirger. İskonto oranı olarak genellikle alternatif getiri (örneğin mevduat faizi) kullanılır. İskontolu süre her zaman basit süreden uzundur.</p>

<h2 id="yorum">Geri dönüş süresi nasıl yorumlanır?</h2>
<div class="table-wrap"><table><thead><tr><th>Yatırım türü</th><th>Tipik geri dönüş süresi</th></tr></thead><tbody>
<tr><td>Konut (kira getirisi)</td><td>15–25 yıl</td></tr><tr><td>Dükkân / ticari gayrimenkul</td><td>10–18 yıl</td></tr>
<tr><td>Çatı tipi güneş enerjisi</td><td>4–8 yıl</td></tr><tr><td>Küçük işletme / franchise</td><td>2–5 yıl</td></tr><tr><td>Üretim makinesi</td><td>2–6 yıl</td></tr>
</tbody></table></div>
<p>Süre ne kadar kısaysa yatırımın riski o kadar düşük kabul edilir. Ancak bu yöntem geri dönüş sonrasındaki kazançları dikkate almaz; yatırımları tam karşılaştırmak için <a href="/roi-hesaplama.html">ROI hesaplama</a> ile birlikte kullanın. Konut yatırımları için özel olarak <a href="/kira-getirisi-hesaplama.html">kira getirisi hesaplama</a> aracı da mevcuttur.</p>
''',
faq=[
('Geri dönüş süresi kaç yıl olmalı?','Sektöre göre değişir. İşletme yatırımlarında 3–5 yıl, gayrimenkulde 15–20 yıl makul kabul edilir. Daha kısa süre daha düşük risk anlamına gelir.'),
('Amortisman süresi ile geri dönüş süresi aynı mı?','Günlük dilde aynı anlamda kullanılır. Muhasebedeki amortisman ise varlığın değerinin yıllara yayılarak gider yazılmasıdır.'),
('Enflasyon geri dönüş süresini nasıl etkiler?','Gelirler enflasyonla birlikte artıyorsa nominal geri dönüş süresi kısalır. Hesaplayıcıdaki yıllık artış alanı bu etkiyi hesaba katar.'),
('İskonto oranı olarak ne kullanmalıyım?','Paranızı başka bir yere yatırsaydınız elde edeceğiniz getiriyi; örneğin vadeli mevduatın yıllık net faiz oranını kullanabilirsiniz.'),
],
related=['roi-hesaplama','kira-getirisi-hesaplama','basa-bas-noktasi-hesaplama','net-kar-hesaplama','bilesik-faiz'],
))

# ───────────────────────── İSKONTO ─────────────────────────
TOOLS.append(dict(
slug='iskonto-hesaplama', name='İskonto Hesaplama', cat='isletme', ico='📉',
title='İskonto Hesaplama – Ticari İskonto, Zincirleme İskonto, Senet | Hesaplarsın',
desc='Liste fiyatı üzerinden tek veya zincirleme (ardışık) iskonto hesaplayın, toplam iskonto oranını bulun. Senet ve çek için iç iskonto ve dış iskonto hesabı dahil.',
h1='📉 İskonto Hesaplama',
lead='Toptancı ve bayilerin kullandığı zincirleme ticari iskontoyu (%20 + %10 + %5) hesaplayın ya da vadeli senedin bugünkü değerini iç ve dış iskonto yöntemleriyle bulun.',
form='''<div class="field full" style="margin-bottom:14px"><label>İskonto Türü</label>
<div class="seg"><label><input type="radio" name="mod" value="ticari" checked onchange="modSec()">Ticari / zincirleme iskonto</label><label><input type="radio" name="mod" value="senet" onchange="modSec()">Senet / çek iskontosu</label></div></div>
<div class="form-grid">
<div class="field" id="f-fiyat"><label for="fiyat">Liste Fiyatı (₺)</label><input type="number" id="fiyat" placeholder="örn: 10.000" inputmode="decimal"></div>
<div class="field" id="f-oranlar"><label for="oranlar">İskonto Oranları (%) <small>boşlukla ayırın</small></label><input type="text" id="oranlar" placeholder="örn: 20 10 5"></div>
<div class="field" id="f-kdv"><label for="kdv">KDV Oranı</label><select id="kdv"><option value="0">KDV ekleme</option><option value="1">%1</option><option value="10">%10</option><option value="20" selected>%20</option></select></div>
<div class="field" id="f-nominal" style="display:none"><label for="nominal">Senet Tutarı (₺)</label><input type="number" id="nominal" placeholder="örn: 100.000" inputmode="decimal"></div>
<div class="field" id="f-gun" style="display:none"><label for="gun">Vadeye Kalan Gün</label><input type="number" id="gun" placeholder="örn: 90" inputmode="numeric"></div>
<div class="field" id="f-faiz" style="display:none"><label for="faiz">Yıllık İskonto (Faiz) Oranı (%)</label><input type="number" id="faiz" placeholder="örn: 45" inputmode="decimal"></div>
</div>''',
js=r'''
function modSec(){var s=radio('mod')==='senet';['fiyat','oranlar','kdv'].forEach(function(i){el('f-'+i).style.display=s?'none':'';});['nominal','gun','faiz'].forEach(function(i){el('f-'+i).style.display=s?'':'none';});el('result').style.display='none';_last=null;}
function hesapla(){
  if(radio('mod')==='senet'){
    var N=v('nominal'), g=v('gun'), i=v('faiz')/100; if(!(N>0)||!(g>0)||!(i>0)) return 'Senet tutarı, gün ve oranı girin.';
    var dis=N*i*g/365, ic=N*i*g/(365+i*g);
    return {main:['İç iskonto ile bugünkü değer', tl(N-ic)], sub:'Dış iskonto ile: '+tl(N-dis),
      rows:[['Senet tutarı (vade sonu)',tl(N)],['İç iskonto tutarı',tl(ic)],['Dış iskonto tutarı',tl(dis)],['Fark (dış − iç)',tl(dis-ic)]],
      note:'Bankalar senet kırdırmada genellikle dış iskonto uygular ve ayrıca BSMV/komisyon kesebilir. VUK’a göre değerlemede iç iskonto kullanılır.'};
  }
  var p=v('fiyat'); if(!(p>0)) return 'Liste fiyatını girin.';
  var o=raw('oranlar').split(/[\s;+\/]+/).map(function(x){return parseFloat(x.replace(',','.'));}).filter(function(x){return x>0&&x<100;});
  if(!o.length) return 'En az bir iskonto oranı girin (örn: 20 10 5).';
  var f=p, rows=[['Liste fiyatı',tl(p)]];
  o.forEach(function(x,i){var d=f*x/100; f-=d; rows.push([(i+1)+'. iskonto (%'+num(x,x%1?1:0)+')','−'+tl(d),'neg']);});
  var top=(1-f/p)*100, kdv=parseFloat(el('kdv').value);
  rows.push(['Toplam iskonto tutarı',tl(p-f)]); rows.push(['Toplam (eşdeğer) iskonto oranı',pct(top),'hl']);
  if(kdv) rows.push(['KDV dahil net fiyat (%'+kdv+')',tl(f*(1+kdv/100))]);
  return {main:['İskontolu net fiyat', tl(f)], sub:o.map(function(x){return '%'+num(x,x%1?1:0);}).join(' + ')+' = %'+num(top,2)+' tek iskonto', rows:rows};
}''',
article='''
<h2 id="nedir">İskonto nedir?</h2>
<p>İskonto, ticarette satıcının alıcıya liste fiyatı üzerinden yaptığı indirimdir. Günlük dilde “indirim” ile eş anlamlı kullanılsa da iskonto genellikle işletmeler arası (B2B) satışlarda, bayi ve toptancı fiyatlandırmasında kullanılan bir terimdir. Finansta ise vadeli bir alacağın (senet, çek) vadesinden önce tahsil edilmesi karşılığında yapılan kesintiyi ifade eder.</p>

<h2 id="zincirleme">Zincirleme (ardışık) iskonto nasıl hesaplanır?</h2>
<p>Toptan satışlarda “%20 + %10 + %5” şeklinde yazılan iskontolar toplanmaz. Her iskonto, bir önceki iskontodan sonra kalan tutara uygulanır.</p>
<div class="formula">Net fiyat = Liste fiyatı × (1 − i₁) × (1 − i₂) × (1 − i₃) …<br>Eşdeğer iskonto = 1 − (1 − i₁)(1 − i₂)(1 − i₃)</div>
<div class="example"><p><b>Örnek:</b> 10.000 ₺ liste fiyatına %20 + %10 + %5 iskonto:</p>
<p>10.000 × 0,80 = 8.000 → 8.000 × 0,90 = 7.200 → 7.200 × 0,95 = <b>6.840 ₺</b></p>
<p>Toplam iskonto %35 değil, <b>%31,6</b>’dır.</p></div>

<h2 id="turler">Ticari iskonto türleri</h2>
<ul>
<li><b>Miktar iskontosu:</b> Belirli adedin üzerinde alım yapıldığında uygulanır.</li>
<li><b>Peşin ödeme iskontosu:</b> Vadeli yerine peşin ödemede verilen indirimdir (örneğin “2/10 net 30”).</li>
<li><b>Bayi / kanal iskontosu:</b> Dağıtım zincirindeki konuma göre verilen indirimdir.</li>
<li><b>Sezon / kampanya iskontosu:</b> Belirli dönemlerde stok eritmek için uygulanır.</li>
</ul>
<p>Fatura üzerinde gösterilen iskontolar KDV matrahından düşülür; KDV iskontolu tutar üzerinden hesaplanır. Bkz. <a href="/kdv-hesaplama.html">KDV hesaplama</a>.</p>

<h2 id="senet">Senet iskontosu: iç iskonto ve dış iskonto</h2>
<p>Vadesi gelmemiş bir senedi bankaya kırdırdığınızda banka, vadeye kalan gün için faiz keser. İki yöntem vardır:</p>
<div class="formula">Dış iskonto = Senet tutarı × Faiz × Gün ÷ 365<br>İç iskonto = Senet tutarı × Faiz × Gün ÷ (365 + Faiz × Gün)</div>
<p><b>Dış iskonto</b> faizi senedin üzerindeki tutardan hesaplar ve uygulamada bankalarca kullanılır. <b>İç iskonto</b> ise faizi senedin bugünkü değeri üzerinden hesapladığı için matematiksel olarak doğru yöntemdir ve Vergi Usul Kanunu’ndaki reeskont işlemlerinde esas alınır. Dış iskonto her zaman iç iskontodan büyüktür.</p>
<div class="example"><p><b>Örnek:</b> 100.000 ₺, 90 gün vadeli senet, yıllık %45: Dış iskonto = 11.096 ₺, İç iskonto = 9.988 ₺.</p></div>
<p>Perakende ürünlerde basit indirim hesabı için <a href="/indirim-hesaplama.html">indirim hesaplama</a>, kâr marjınızı korumak için <a href="/kar-marji-hesaplama.html">kâr marjı hesaplama</a> araçlarını kullanabilirsiniz.</p>
''',
faq=[
('%20 + %10 iskonto toplam yüzde kaç eder?','%30 değil, %28 eder. İkinci iskonto ilk iskonto sonrası kalan fiyata uygulanır: 1 − 0,8 × 0,9 = 0,28.'),
('İskonto ile indirim aynı şey mi?','Temelde aynıdır. İskonto daha çok ticari ve finansal bağlamda (bayi fiyatı, senet kırdırma) kullanılan terimdir.'),
('İskonto KDV’den önce mi düşülür?','Evet. Faturada gösterilen iskonto matrahtan düşülür ve KDV iskontolu tutar üzerinden hesaplanır.'),
('Senet kırdırma hesabında hangi yöntem kullanılır?','Bankalar genellikle dış iskonto uygular. Muhasebedeki reeskont hesaplarında ise iç iskonto kullanılır.'),
],
related=['indirim-hesaplama','kar-marji-hesaplama','kdv-hesaplama','stok-karliligi-hesaplama','yuzde-hesaplama'],
))

# ───────────────────────── KİRA GETİRİSİ ─────────────────────────
TOOLS.append(dict(
slug='kira-getirisi-hesaplama', name='Kira Getirisi Hesaplama', cat='gayrimenkul', ico='🏠',
title='Kira Getirisi Hesaplama – Brüt, Net Getiri ve Amortisman Süresi | Hesaplarsın',
desc='Ev veya dükkânın fiyatı ve aylık kirasıyla brüt ve net kira getirisi oranını, kira çarpanını ve kaç yılda kendini amorti edeceğini hesaplayın.',
h1='🏠 Kira Getirisi Hesaplama',
lead='Satın almayı düşündüğünüz konutun ya da dükkânın kira getirisini, giderler düşüldükten sonraki net getirisini ve kendini kaç yılda amorti edeceğini hesaplayın.',
form='''<div class="form-grid">
<div class="field"><label for="fiyat">Gayrimenkul Fiyatı (₺)</label><input type="number" id="fiyat" placeholder="örn: 4.500.000" inputmode="decimal"></div>
<div class="field"><label for="kira">Aylık Kira (₺)</label><input type="number" id="kira" placeholder="örn: 22.000" inputmode="decimal"></div>
<div class="field"><label for="masraf">Alım Masrafları (₺) <small>tapu, emlakçı</small></label><input type="number" id="masraf" placeholder="örn: 180.000" inputmode="decimal"></div>
<div class="field"><label for="gider">Yıllık Giderler (₺) <small>bakım, emlak vergisi, DASK</small></label><input type="number" id="gider" placeholder="örn: 15.000" inputmode="decimal"></div>
<div class="field"><label for="bos">Boş Kalma Süresi (ay/yıl)</label><input type="number" id="bos" placeholder="örn: 1" inputmode="decimal"></div>
<div class="field"><label for="artis">Yıllık Kira Artışı (%) <small>isteğe bağlı</small></label><input type="number" id="artis" placeholder="örn: 30" inputmode="decimal"></div>
</div>''',
js=r'''
function hesapla(){
  var F=v('fiyat'), K=v('kira'), M=v('masraf')||0, G=v('gider')||0, B=Math.min(v('bos')||0,11), a=(v('artis')||0)/100;
  if(!(F>0)||!(K>0)) return 'Gayrimenkul fiyatı ve aylık kirayı girin.';
  var top=F+M, brut=K*12/F*100, yillikNet=K*(12-B)-G, net=yillikNet/top*100, carpan=F/K;
  var birikim=0, yil=0; while(birikim<top && yil<100){birikim+=(K*Math.pow(1+a,yil))*(12-B)-G; yil++;}
  return {main:['Net kira getirisi (yıllık)', pct(net)], sub:'Brüt getiri: '+pct(brut),
    rows:[['Toplam yatırım (masraflar dahil)',tl(top)],['Yıllık brüt kira',tl(K*12)],['Yıllık net kira (gider ve boş dönem sonrası)',tl(yillikNet)],
      ['Kira çarpanı (fiyat ÷ aylık kira)',num(carpan,0)+' ay'],['Sabit kirayla amortisman',num(top/yillikNet,1)+' yıl'],[a?'Yıllık %'+num(a*100,0)+' artışla amortisman':'Amortisman süresi',yil>=100?'100 yıldan uzun':yil+' yıl','hl']],
    note:'Kira geliri gelir vergisine tabidir. 2026 yılında elde edilen konut kira gelirinde yıllık 58.000 ₺ istisna uygulanır (diğer gelir durumunuza göre istisnadan yararlanamayabilirsiniz).'};
}''',
article='''
<h2 id="nedir">Kira getirisi nedir?</h2>
<p>Kira getirisi, bir gayrimenkulün yıllık kira gelirinin satın alma bedeline oranıdır ve yatırımın her yıl kendini yüzde kaç oranında geri ödediğini gösterir. Konut yatırımında en çok kullanılan iki ölçüt <b>kira getiri oranı</b> ve <b>amortisman süresi</b>dir (kira çarpanı).</p>

<h2 id="brut">Brüt kira getirisi nasıl hesaplanır?</h2>
<div class="formula">Brüt kira getirisi (%) = Yıllık kira ÷ Gayrimenkul fiyatı × 100<br>Amortisman süresi (yıl) = Gayrimenkul fiyatı ÷ Yıllık kira</div>
<div class="example"><p><b>Örnek:</b> 4.500.000 ₺’lik daireden ayda 22.000 ₺ kira alınıyorsa:</p><p>22.000 × 12 = 264.000 ₺ → 264.000 ÷ 4.500.000 × 100 = <b>%5,87 brüt getiri</b>. Kira sabit kalırsa amortisman süresi 17 yıldır (kira çarpanı 205 ay).</p></div>

<h2 id="net">Net kira getirisi neden daha önemli?</h2>
<p>Brüt getiri, yatırımın gerçek maliyetlerini göstermez. Net getiri hesabında şunlar dikkate alınmalıdır:</p>
<ul>
<li><b>Alım masrafları:</b> %4 tapu harcı (alıcı payı %2), emlakçı komisyonu, döner sermaye ücreti. Bkz. <a href="/tapu-harci-hesaplama.html">tapu harcı hesaplama</a>.</li>
<li><b>Yıllık giderler:</b> Emlak vergisi, DASK, boya-bakım, ev sahibine düşen aidat ve demirbaş giderleri.</li>
<li><b>Boş kalma süresi:</b> Kiracı değişimlerinde dairenin boş kaldığı aylar.</li>
<li><b>Kira gelir vergisi:</b> İstisna tutarını aşan kira geliri beyan edilir.</li>
</ul>
<div class="formula">Net getiri (%) = (Yıllık kira × doluluk − Yıllık giderler) ÷ (Fiyat + Alım masrafları) × 100</div>

<h2 id="karsilastirma">Kira getirisi kaç olmalı?</h2>
<p>Türkiye’de son yıllarda konut fiyatlarının kiralardan hızlı artması nedeniyle büyükşehirlerde brüt kira getirisi çoğunlukla <b>%4–7</b> bandındadır; bu da 15–25 yıllık amortisman süresine karşılık gelir. Ticari gayrimenkullerde getiri genellikle daha yüksek, risk de daha fazladır. Bir yatırımı değerlendirirken getiriyi; mevduat faizi, enflasyon ve konutun değer artış beklentisiyle birlikte düşünmek gerekir.</p>
<div class="table-wrap"><table><thead><tr><th>Brüt getiri</th><th>Amortisman süresi</th><th>Değerlendirme</th></tr></thead><tbody>
<tr><td>%4</td><td>25 yıl</td><td>Düşük – değer artışına dayalı yatırım</td></tr>
<tr><td>%5–6</td><td>17–20 yıl</td><td>Büyükşehir ortalaması</td></tr>
<tr><td>%7–8</td><td>12–14 yıl</td><td>İyi</td></tr>
<tr><td>%9 ve üzeri</td><td>11 yıl ve altı</td><td>Yüksek (öğrenci evleri, ticari)</td></tr>
</tbody></table></div>
<p>Yasal kira artış sınırını görmek için <a href="/kira-artis-hesaplama.html">kira artış hesaplama</a>, metrekare fiyatını karşılaştırmak için <a href="/metrekare-fiyat-hesaplama.html">metrekare fiyatı hesaplama</a> araçlarını kullanabilirsiniz.</p>
''',
faq=[
('Ev kaç yılda kendini amorti eder?','Ev fiyatını yıllık kiraya bölerek bulunur. 3.600.000 ₺’lik ve aylık 15.000 ₺ kira getiren bir ev, kira sabit kalırsa 20 yılda kendini amorti eder.'),
('Kira çarpanı nedir?','Ev fiyatının aylık kiraya bölünmesiyle bulunan sayıdır. Çarpan 200 ise ev 200 ayda (yaklaşık 16,7 yıl) kendini amorti eder. Çarpan düştükçe yatırım daha cazip hale gelir.'),
('Brüt ve net kira getirisi arasındaki fark nedir?','Brüt getiri yalnızca kira ile fiyatı karşılaştırır. Net getiri ise alım masraflarını, yıllık giderleri ve boş kalma sürelerini de hesaba katar.'),
('Kira artışı amortisman süresini nasıl etkiler?','Kiralar her yıl arttığı için gerçek amortisman süresi sabit kira hesabından kısadır. Hesaplayıcıya yıllık artış oranı girerek bu etkiyi görebilirsiniz.'),
],
related=['kira-artis-hesaplama','tapu-harci-hesaplama','metrekare-fiyat-hesaplama','yatirim-geri-donus-suresi-hesaplama','roi-hesaplama'],
))

# ───────────────────────── KİRA ARTIŞ ─────────────────────────
TOOLS.append(dict(
slug='kira-artis-hesaplama', name='Kira Artış Hesaplama', cat='gayrimenkul', ico='📈',
title='Kira Artış Oranı Hesaplama Ekim 2026 – Yasal Kira Zammı (%31,49) | Hesaplarsın',
desc='Ekim 2026 yasal kira artış oranı %31,49 (12 aylık TÜFE ortalaması). Mevcut kiranızı girin, kira sözleşmenizin yenilendiği aya göre yeni kiranızı hesaplayın.',
h1='📈 Kira Artış Hesaplama (Ekim 2026: %31,49)',
lead='Kira sözleşmenizin yenilendiği ayı ve mevcut kiranızı seçin; Türk Borçlar Kanunu’na göre uygulanabilecek en yüksek yasal kira artışını ve yeni kiranızı görün.',
form='''<div class="form-grid">
<div class="field"><label for="kira">Mevcut Aylık Kira (₺)</label><input type="number" id="kira" placeholder="örn: 20.000" inputmode="decimal"></div>
<div class="field"><label for="ay">Sözleşme Yenileme Ayı</label><select id="ay"><option value="31.49" selected>Ekim 2026 – %31,49</option><option value="31.79">Eylül 2026 – %31,79</option><option value="manuel">Diğer ay (oranı kendim gireceğim)</option></select></div>
<div class="field" id="f-oran" style="display:none"><label for="oran">Kira Artış Oranı (%)</label><input type="number" id="oran" placeholder="örn: 32,5" inputmode="decimal"></div>
<div class="field"><label for="anlasma">Sözleşmedeki Artış Oranı (%) <small>isteğe bağlı</small></label><input type="number" id="anlasma" placeholder="örn: 25" inputmode="decimal"></div>
</div>''',
js=r'''
function onReady(){el('ay').addEventListener('change',function(){el('f-oran').style.display=el('ay').value==='manuel'?'':'none';});}
function hesapla(){
  var k=v('kira'); if(!(k>0)) return 'Mevcut kiranızı girin.';
  var o=el('ay').value==='manuel'?v('oran'):parseFloat(el('ay').value); if(!(o>=0)) return 'Kira artış oranını girin.';
  var a=v('anlasma'), uyg=(a>=0&&!isNaN(a))?Math.min(a,o):o, yeni=k*(1+uyg/100);
  var rows=[['Mevcut kira',tl(k)],['Yasal üst sınır (TÜFE 12 ay ort.)',pct(o)],['Uygulanacak oran',pct(uyg)],['Aylık artış tutarı',tl(yeni-k),'hl'],['Yıllık ek ödeme',tl((yeni-k)*12)],['Yeni yıllık kira',tl(yeni*12)]];
  return {main:['Yeni aylık kira', tl(yeni)], sub:'%'+num(uyg,2)+' artışla', rows:rows,
    note:(a>o?'Sözleşmedeki oran (%'+num(a,2)+') yasal sınırı aştığı için yasal sınır uygulanır. ':'')+'Oran, kira döneminin başladığı aydan önceki ayın TÜİK verisine göre belirlenir.'};
}''',
article='''
<h2 id="oran">Ekim 2026 kira artış oranı ne kadar?</h2>
<p>TÜİK’in 5 Ekim 2026’da açıkladığı Eylül ayı enflasyon verisine göre, tüketici fiyat endeksinin (TÜFE) <b>12 aylık ortalama değişimi %31,49</b> olmuştur. Kira sözleşmesi Ekim 2026’da yenilenen konut ve işyeri kiracıları için uygulanabilecek en yüksek kira artış oranı budur. Eylül 2026’da yenilenen sözleşmeler için oran %31,79 idi.</p>
<div class="formula">Yeni kira = Mevcut kira × (1 + Kira artış oranı ÷ 100)</div>
<div class="example"><p><b>Örnek:</b> Ekim 2026’da yenilenen 20.000 ₺’lik kira: 20.000 × 1,3149 = <b>26.298 ₺</b> (aylık artış 6.298 ₺).</p></div>

<h2 id="yasal">Kira artışında yasal sınır nedir?</h2>
<p>Türk Borçlar Kanunu’nun 344. maddesine göre yenilenen kira dönemlerinde kira artışı, bir önceki kira yılındaki <b>TÜFE’nin 12 aylık ortalamalara göre değişim oranını</b> geçemez. Konutlarda 2022–2024 arasında uygulanan %25 sınırı 1 Temmuz 2024’te sona ermiştir; şu an konut ve işyerleri için aynı kural geçerlidir.</p>
<ul>
<li>Sözleşmede daha düşük bir oran (örneğin %20) yazıyorsa sözleşmedeki oran uygulanır.</li>
<li>Sözleşmede yüksek oran veya “piyasa koşulları” yazsa bile yasal sınır aşılamaz.</li>
<li>Sözleşmede artış hükmü yoksa da kiraya veren yasal sınıra kadar artış talep edebilir.</li>
</ul>

<h2 id="tablo">Son aylara ait kira artış oranları</h2>
<div class="table-wrap"><table><thead><tr><th>Kira yenileme ayı</th><th>Yasal üst sınır</th></tr></thead><tbody>
<tr><td>Ekim 2026</td><td>%31,49</td></tr><tr><td>Eylül 2026</td><td>%31,79</td></tr>
</tbody></table></div>
<p>Oranlar her ayın 3’ünde (hafta sonuna denk gelirse sonraki iş günü) TÜİK tarafından açıklanan enflasyon verileriyle güncellenir. Sonraki açıklama tarihleri için <a href="/ekonomi-takvimi.html#enflasyon">ekonomi takvimine</a> bakabilirsiniz. Diğer aylar için hesaplayıcıda “Diğer ay” seçeneğiyle oranı elle girebilirsiniz.</p>

<h2 id="kira-tablosu">Ekim 2026 kira zammı tablosu</h2>
<p>%31,49 yasal üst sınırla yeni kira tutarları:</p>
<div class="table-wrap"><table><thead><tr><th>Mevcut kira</th><th>Yeni kira (en fazla)</th><th>Aylık artış</th><th>Yıllık ek ödeme</th></tr></thead><tbody>
<tr><td>10.000 ₺</td><td>13.149 ₺</td><td>3.149 ₺</td><td>37.788 ₺</td></tr><tr><td>15.000 ₺</td><td>19.724 ₺</td><td>4.724 ₺</td><td>56.682 ₺</td></tr><tr><td>20.000 ₺</td><td>26.298 ₺</td><td>6.298 ₺</td><td>75.576 ₺</td></tr><tr><td>25.000 ₺</td><td>32.872 ₺</td><td>7.872 ₺</td><td>94.470 ₺</td></tr><tr><td>30.000 ₺</td><td>39.447 ₺</td><td>9.447 ₺</td><td>113.364 ₺</td></tr><tr><td>40.000 ₺</td><td>52.596 ₺</td><td>12.596 ₺</td><td>151.152 ₺</td></tr><tr><td>50.000 ₺</td><td>65.745 ₺</td><td>15.745 ₺</td><td>188.940 ₺</td></tr>
</tbody></table></div>

<h2 id="ortalama">Neden yıllık enflasyon değil, 12 aylık ortalama?</h2>
<p>Haberlerde sık geçen “yıllık enflasyon” ile kira artışında kullanılan oran farklıdır. Eylül 2026’da yıllık enflasyon <b>%29,73</b> iken kira artış sınırı <b>%31,49</b> oldu. Çünkü kira artışında son 12 ayın endeks ortalaması, bir önceki 12 ayın ortalamasıyla karşılaştırılır. Enflasyon düşerken 12 aylık ortalama yıllık orandan bir süre daha yüksek kalır; enflasyon yükselirken ise tersi olur. Kira artışında her zaman TÜİK bülteninde “12 aylık ortalamalara göre değişim” başlığındaki oran kullanılır.</p>

<h2 id="ay">Hangi ayın oranı uygulanır?</h2>
<p>Kira yılının başladığı aydan önce açıklanan son oran esas alınır. Sözleşmesi 15 Ekim 2026’da yenilenen kiracı için 5 Ekim’de açıklanan Eylül verisi, yani <b>%31,49</b> kullanılır. Sözleşmesi Kasım’da yenilenecekler için 3 Kasım’da açıklanacak oran geçerli olur; bu oranın yaklaşık %31,2 olması bekleniyor (ayrıntılar: <a href="/blog/kasim-2026-kira-artis-orani.html">Kasım 2026 kira artış oranı</a>).</p>

<h2 id="isyeri">İşyeri kiralarında stopaj ve artış</h2>
<p>Şirket veya şahıs işletmesi olan kiracılar, işyeri kirasında brüt kira üzerinden <b>%20 stopaj</b> keserek vergi dairesine öder; ev sahibine net tutar yatırılır. Kira artışı brüt kira üzerinden hesaplanır.</p>
<div class="example"><p><b>Örnek:</b> Ev sahibine net 20.000 ₺ ödenen bir dükkânın brüt kirası 20.000 ÷ 0,80 = <b>25.000 ₺</b>’dir. %31,49 artışla yeni brüt kira 32.872 ₺, ev sahibine ödenecek yeni net kira 26.298 ₺ olur; kiracı her ay 6.574 ₺ stopajı vergi dairesine yatırır.</p></div>

<h2 id="ara-artis">Kira yılı içinde zam yapılabilir mi?</h2>
<p>Hayır. Kira artışı yalnızca yeni kira yılının başında yapılabilir. Altı ayda bir veya üç ayda bir artış öngören sözleşme hükümleri, yıllık TÜFE sınırını dolanmaya yönelik olduğu ölçüde geçersizdir. Kira bedelinin döviz cinsinden belirlenmesi de konut kiralarında kural olarak mümkün değildir.</p>

<h2 id="bes-yil">5 yılı dolduran kiracılar için durum</h2>
<p>Beş yıldan uzun süren kira ilişkilerinde, yeni kira dönemine ait kira bedeli hakim tarafından; TÜFE’nin 12 aylık ortalaması, kiralananın durumu ve emsal kira bedelleri dikkate alınarak hakkaniyete uygun şekilde belirlenebilir (kira tespit davası). Bu durumda artış yasal TÜFE sınırını aşabilir.</p>

<h2 id="anlasmazlik">Ev sahibi fazla zam isterse ne yapılmalı?</h2>
<ul>
<li>Yasal sınıra göre hesaplanan yeni kirayı banka hesabına “… ayı kirası” açıklamasıyla yatırmaya devam edin.</li>
<li>Kira artışı uyuşmazlıklarında dava açmadan önce <b>arabulucuya</b> başvurmak zorunludur.</li>
<li>Kira sözleşmenizi ve ödeme dekontlarınızı saklayın.</li>
</ul>
<p>Kiraya verenler için yatırımın getirisini <a href="/kira-getirisi-hesaplama.html">kira getirisi hesaplama</a>, genel fiyat değişimini görmek için <a href="/enflasyon-hesaplama.html">enflasyon hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('Ekim 2026 kira zammı yüzde kaç?','Ekim 2026’da kira sözleşmesi yenilenenler için yasal kira artış üst sınırı %31,49’dur.'),
('Kira artışı TÜFE’den fazla olabilir mi?','Hayır. Yenilenen kira dönemlerinde artış, 12 aylık TÜFE ortalamasını geçemez. Yalnızca 5 yılı aşan kira ilişkilerinde hakim hakkaniyete göre yeni bedel belirleyebilir.'),
('İşyeri kiralarında da aynı oran mı uygulanır?','Evet. Konut ve çatılı işyeri kiralarında aynı TÜFE 12 aylık ortalama sınırı geçerlidir.'),
('Kira artış oranı ne zaman açıklanır?','TÜİK her ayın 3’ünde enflasyon verilerini açıklar; aynı gün o ay yenilenecek kira sözleşmeleri için artış oranı da belli olur.'),
('20.000 TL kira Ekim 2026’da ne kadar olur?','Ekim 2026’da yenilenen 20.000 TL’lik kira, %31,49 yasal sınırla en fazla 26.298 TL olur.'),
('Sözleşmede kira artışı yazmıyorsa ne olur?','Kiraya veren yine yasal sınıra kadar artış talep edebilir; uzlaşılamazsa arabuluculuk ve kira tespit davası yoluna gidilebilir.'),
],
related=['kira-getirisi-hesaplama','enflasyon-hesaplama','tapu-harci-hesaplama','metrekare-fiyat-hesaplama','yuzde-hesaplama'],
sources=[('6098 sayılı Türk Borçlar Kanunu m.344','https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6098.pdf'),('TÜİK Enflasyon Verileri','https://data.tuik.gov.tr/')],
))

# ───────────────────────── METREKARE FİYAT ─────────────────────────
TOOLS.append(dict(
slug='metrekare-fiyat-hesaplama', name='Metrekare Fiyatı Hesaplama', cat='gayrimenkul', ico='📐',
title='Metrekare Fiyatı Hesaplama – Evin m² Fiyatı Ne Kadar? | Hesaplarsın',
desc='4.500.000 TL’lik 120 m² ev, m² başına 37.500 TL eder. Ev, arsa ya da dükkânın m² fiyatını hesaplayın, iki ilanı karşılaştırın.',
h1='📐 Metrekare Fiyatı Hesaplama',
lead='İlandaki fiyatı ve metrekareyi girin; metrekare başına fiyatı hesaplayın. İkinci bir ilan girerek hangisinin daha uygun olduğunu karşılaştırın.',
form='''<div class="form-grid">
<div class="field"><label for="f1">1. Gayrimenkul Fiyatı (₺)</label><input type="number" id="f1" placeholder="örn: 3.850.000" inputmode="decimal"></div>
<div class="field"><label for="m1">1. Alan (m²)</label><input type="number" id="m1" placeholder="örn: 110" inputmode="decimal"></div>
<div class="field"><label for="f2">2. Gayrimenkul Fiyatı (₺) <small>karşılaştırma</small></label><input type="number" id="f2" placeholder="isteğe bağlı" inputmode="decimal"></div>
<div class="field"><label for="m2">2. Alan (m²)</label><input type="number" id="m2" placeholder="isteğe bağlı" inputmode="decimal"></div>
<div class="field full"><label for="hedefm">Hedef Alan (m²) <small>bu m² fiyatıyla kaç TL eder?</small></label><input type="number" id="hedefm" placeholder="örn: 125" inputmode="decimal"></div>
</div>''',
js=r'''
function hesapla(){
  var f1=v('f1'), m1=v('m1'); if(!(f1>0)||!(m1>0)) return 'Fiyat ve metrekareyi girin.';
  var b1=f1/m1, rows=[['1. ilan m² fiyatı',tl(b1,0)]], f2=v('f2'), m2=v('m2'), h=v('hedefm'), sub='';
  if(f2>0&&m2>0){var b2=f2/m2; rows.push(['2. ilan m² fiyatı',tl(b2,0)]); var ucuz=b1<b2?1:2, fark=Math.abs(b1-b2)/Math.max(b1,b2)*100;
    rows.push(['Daha uygun olan',ucuz+'. ilan (m² başına %'+num(fark,1)+' ucuz)','hl']); sub='Fark: m² başına '+tl(Math.abs(b1-b2),0);}
  if(h>0) rows.push([num(h,0)+' m² için tahmini fiyat',tl(b1*h,0)]);
  return {main:['Metrekare fiyatı', tl(b1,0)+' / m²'], sub:sub, rows:rows};
}''',
article='''
<h2 id="nasil">Metrekare fiyatı nasıl hesaplanır?</h2>
<p>Bir gayrimenkulün metrekare (m²) fiyatı, toplam satış fiyatının alanına bölünmesiyle bulunur. Farklı büyüklükteki daireleri, arsaları veya dükkânları adil şekilde karşılaştırmanın en pratik yoludur.</p>
<div class="formula">m² fiyatı = Satış fiyatı ÷ Metrekare</div>
<div class="example"><p><b>Örnek:</b> 110 m²’lik daire 3.850.000 ₺ ise: 3.850.000 ÷ 110 = <b>35.000 ₺/m²</b>. Aynı bölgedeki 125 m²’lik bir daire bu birim fiyatla yaklaşık 4.375.000 ₺ eder.</p></div>

<h2 id="brut-net">Brüt ve net metrekare farkı</h2>
<p>İlanlarda verilen metrekare çoğunlukla <b>brüt</b> alandır ve duvarları, balkonları, ortak alanlardan düşen payı (merdiven, asansör boşluğu, giriş holü) içerir. <b>Net</b> metrekare ise duvar içinden ölçülen, fiilen kullanılan alandır. Genellikle net alan, brüt alanın %75–85’i kadardır. İki ilanı karşılaştırırken her ikisinde de aynı ölçütün (brüt veya net) kullanıldığından emin olun.</p>
<div class="table-wrap"><table><thead><tr><th>Terim</th><th>Kapsam</th></tr></thead><tbody>
<tr><td>Net alan</td><td>Odaların, mutfağın, banyonun duvar içi alanları toplamı</td></tr>
<tr><td>Brüt alan</td><td>Net alan + iç ve dış duvarlar + balkon</td></tr>
<tr><td>Brüt (ortak alanlar dahil)</td><td>Brüt alan + bina ortak alanlarından düşen pay</td></tr>
</tbody></table></div>

<h2 id="etkenler">Metrekare fiyatını etkileyen faktörler</h2>
<ul>
<li><b>Konum:</b> Ulaşım, okul, hastane ve sosyal donatılara yakınlık.</li>
<li><b>Bina yaşı ve deprem dayanıklılığı:</b> 2000 sonrası (özellikle 2018 yönetmeliği sonrası) yapılar daha değerlidir.</li>
<li><b>Kat ve cephe:</b> Ara katlar, güney cephe ve manzara fiyatı artırır.</li>
<li><b>Site özellikleri:</b> Otopark, güvenlik, havuz, asansör.</li>
<li><b>İmar durumu (arsalarda):</b> TAKS, KAKS (emsal) ve kat izni arsa m² fiyatını doğrudan belirler.</li>
</ul>

<h2 id="maliyet">Satın alırken toplam maliyeti unutmayın</h2>
<p>Metrekare fiyatı yalnızca başlangıçtır. Tapu harcı (%4), emlakçı komisyonu, döner sermaye, DASK ve taşınma masrafları toplam maliyeti %5–7 artırabilir. Bkz. <a href="/tapu-harci-hesaplama.html">tapu harcı hesaplama</a>. Yatırım amaçlı alımlarda <a href="/kira-getirisi-hesaplama.html">kira getirisi hesaplama</a> ile amortisman süresini de kontrol edin. Duvar boyası gibi tadilat işleri için <a href="/boya-hesaplama.html">boya hesaplama</a> aracı da işinize yarayabilir.</p>
''',
faq=[
('Evin metrekare fiyatı nasıl bulunur?','Satış fiyatını evin metrekaresine bölün. 2.400.000 ₺’lik 80 m² ev için m² fiyatı 30.000 ₺’dir.'),
('İlanlardaki metrekare brüt mü net mi?','Çoğu ilanda brüt metrekare yazılır. Tapu kaydında da genellikle brüt alan yer alır; net alanı ilan detayından veya ekspertiz raporundan kontrol edin.'),
('Net metrekare brütün yüzde kaçıdır?','Genellikle %75–85’i kadardır. Duvar kalınlığı, balkon sayısı ve ortak alan oranı bu oranı değiştirir.'),
('Arsa metrekare fiyatı nasıl hesaplanır?','Arsa fiyatı arsa alanına bölünür. Ancak arsalarda asıl belirleyici olan imar durumudur; aynı m²’de emsali yüksek arsa çok daha değerlidir.'),
],
related=['kira-getirisi-hesaplama','tapu-harci-hesaplama','kira-artis-hesaplama','boya-hesaplama','yuzde-hesaplama'],
))

# ───────────────────────── KAR / ZARAR ─────────────────────────
TOOLS.append(dict(
slug='kar-zarar-hesaplama', name='Kâr / Zarar Hesaplama', cat='isletme', ico='⚖️',
title='Kâr Zarar Hesaplama – Alış Satış Fiyatından Kâr Oranı | Hesaplarsın',
desc='Alış ve satış fiyatına göre kâr veya zarar tutarını, maliyete göre kâr oranını (markup) ve satışa göre kâr marjını hesaplayın. Adet ve masraf desteği.',
h1='⚖️ Kâr / Zarar Hesaplama',
lead='Ürünü kaça alıp kaça sattığınızı girin; kâr veya zarar tutarını, maliyet üzerinden kâr oranını ve satış üzerinden kâr marjını tek ekranda görün.',
form='''<div class="form-grid">
<div class="field"><label for="alis">Alış Fiyatı / Birim Maliyet (₺)</label><input type="number" id="alis" placeholder="örn: 750" inputmode="decimal"></div>
<div class="field"><label for="satis">Satış Fiyatı (₺)</label><input type="number" id="satis" placeholder="örn: 1.000" inputmode="decimal"></div>
<div class="field"><label for="adet">Adet</label><input type="number" id="adet" value="1" inputmode="numeric"></div>
<div class="field"><label for="masraf">Birim Başı Ek Masraf (₺) <small>kargo, komisyon</small></label><input type="number" id="masraf" placeholder="isteğe bağlı" inputmode="decimal"></div>
</div>''',
js=r'''
function hesapla(){
  var a=v('alis'), s=v('satis'), n=Math.max(1,v('adet')||1), m=v('masraf')||0;
  if(!(a>0)||!(s>=0)) return 'Alış ve satış fiyatını girin.';
  var mal=a+m, k=s-mal, top=k*n;
  return {main:[k>=0?'Toplam kâr':'Toplam zarar', tl(Math.abs(top))], sub:k>=0?'Satış kârlı':'Satış zararda – maliyetin altında satılıyor',
    rows:[['Birim maliyet (masraflar dahil)',tl(mal)],['Birim kâr / zarar',tl(k),k>=0?'hl':'neg'],['Kâr oranı (maliyete göre, markup)',pct(k/mal*100)],['Kâr marjı (satışa göre)',s>0?pct(k/s*100):'—'],
      ['Başa baş satış fiyatı',tl(mal)],['Toplam ciro ('+num(n,0)+' adet)',tl(s*n)]]};
}''',
article='''
<h2 id="nasil">Kâr ve zarar nasıl hesaplanır?</h2>
<p>Bir satıştan elde edilen kâr, satış fiyatından ürünün tüm maliyetleri (alış fiyatı, kargo, komisyon, ambalaj) çıkarılarak bulunur. Sonuç pozitifse kâr, negatifse zarar edilmiştir.</p>
<div class="formula">Kâr / Zarar = Satış fiyatı − (Alış fiyatı + Ek masraflar)</div>

<h2 id="oran-marj">Kâr oranı ile kâr marjı arasındaki fark</h2>
<p>Ticarette en sık karıştırılan iki kavramdır ve aynı satış için farklı yüzdeler verir:</p>
<div class="formula">Kâr oranı (markup) = Kâr ÷ Maliyet × 100<br>Kâr marjı = Kâr ÷ Satış fiyatı × 100</div>
<div class="example"><p><b>Örnek:</b> 750 ₺’ye alınıp 1.000 ₺’ye satılan ürün: Kâr = 250 ₺.</p><p>Kâr oranı = 250 ÷ 750 = <b>%33,3</b> · Kâr marjı = 250 ÷ 1.000 = <b>%25</b></p></div>
<p>Esnaf genellikle “maliyetin üzerine %X koydum” der (kâr oranı); finansal tablolarda ise kâr marjı kullanılır. Satış fiyatını hedef marja göre belirlemek için <a href="/kar-marji-hesaplama.html">kâr marjı hesaplama</a> aracını kullanın.</p>

<h2 id="tablo">Kâr oranı ve kâr marjı dönüşüm tablosu</h2>
<div class="table-wrap"><table><thead><tr><th>Kâr oranı (maliyete göre)</th><th>Kâr marjı (satışa göre)</th></tr></thead><tbody>
<tr><td>%10</td><td>%9,1</td></tr><tr><td>%20</td><td>%16,7</td></tr><tr><td>%25</td><td>%20</td></tr><tr><td>%33,3</td><td>%25</td></tr>
<tr><td>%50</td><td>%33,3</td></tr><tr><td>%100</td><td>%50</td></tr>
</tbody></table></div>

<h2 id="zarar">Zarar etmemek için dikkat edilecekler</h2>
<ul>
<li><b>Gizli maliyetler:</b> Pazaryeri komisyonu, ödeme altyapısı ücreti, iade kargoları ve reklam harcaması birim maliyete eklenmelidir.</li>
<li><b>KDV:</b> Alış ve satış fiyatlarını aynı şekilde (ikisi de KDV hariç veya ikisi de KDV dahil) girin. Bkz. <a href="/kdv-hesaplama.html">KDV hesaplama</a>.</li>
<li><b>Sabit giderler:</b> Kira, personel ve fatura gibi sabit giderleri karşılamak için gereken satış adedini <a href="/basa-bas-noktasi-hesaplama.html">başa baş noktası hesaplama</a> ile bulun.</li>
<li><b>Enflasyon:</b> Yerine koyma maliyeti yükseliyorsa eski alış fiyatıyla yapılan kâr hesabı yanıltıcı olabilir.</li>
</ul>
''',
faq=[
('Kâr yüzdesi nasıl hesaplanır?','Maliyete göre kâr oranı için kârı maliyete, satışa göre kâr marjı için kârı satış fiyatına bölüp 100 ile çarpın.'),
('%30 kârla satış fiyatı nasıl bulunur?','Maliyete %30 eklemek için maliyeti 1,30 ile çarpın. 500 ₺ maliyetli ürün 650 ₺’ye satılır. Satış üzerinden %30 marj için ise maliyeti 0,70’e bölün: 714,29 ₺.'),
('Zarar oranı nasıl hesaplanır?','Zarar tutarını maliyete bölüp 100 ile çarpın. 1.000 ₺’ye alınıp 800 ₺’ye satılan üründe zarar oranı %20’dir.'),
('Kâr hesabında KDV dahil mi edilmeli?','KDV işletme için gelir ya da gider değildir. Doğru kâr hesabı için alış ve satış fiyatlarını KDV hariç kullanmak en sağlıklısıdır.'),
],
related=['kar-marji-hesaplama','net-kar-hesaplama','brut-kar-hesaplama','basa-bas-noktasi-hesaplama','stok-karliligi-hesaplama','iskonto-hesaplama'],
))

# ───────────────────────── KAR MARJI ─────────────────────────
TOOLS.append(dict(
slug='kar-marji-hesaplama', name='Kâr Marjı Hesaplama', cat='isletme', ico='📊',
title='Kâr Marjı Hesaplama – Hedef Marja Göre Satış Fiyatı Bulma | Hesaplarsın',
desc='Maliyet ve satış fiyatından kâr marjını hesaplayın ya da hedef kâr marjına göre satış fiyatını belirleyin. Marj ve markup farkı, KDV dahil fiyat ve örnek tablo.',
h1='📊 Kâr Marjı Hesaplama',
lead='Ürününüzün kâr marjını hesaplayın veya “%30 marjla kaça satmalıyım?” sorusunun cevabını bulun. KDV dahil etiket fiyatı da otomatik hesaplanır.',
form='''<div class="field full" style="margin-bottom:14px"><label>Ne hesaplamak istiyorsunuz?</label>
<div class="seg"><label><input type="radio" name="mod" value="marj" checked onchange="modSec()">Kâr marjını bul</label><label><input type="radio" name="mod" value="fiyat" onchange="modSec()">Hedef marja göre satış fiyatı</label></div></div>
<div class="form-grid">
<div class="field"><label for="maliyet">Birim Maliyet (₺, KDV hariç)</label><input type="number" id="maliyet" placeholder="örn: 400" inputmode="decimal"></div>
<div class="field" id="f-satis"><label for="satis">Satış Fiyatı (₺, KDV hariç)</label><input type="number" id="satis" placeholder="örn: 560" inputmode="decimal"></div>
<div class="field" id="f-hedef" style="display:none"><label for="hedef">Hedef Kâr Marjı (%)</label><input type="number" id="hedef" placeholder="örn: 30" inputmode="decimal"></div>
<div class="field"><label for="kdv">KDV Oranı</label><select id="kdv"><option value="0">Yok</option><option value="1">%1</option><option value="10">%10</option><option value="20" selected>%20</option></select></div>
</div>''',
js=r'''
function modSec(){var f=radio('mod')==='fiyat';el('f-satis').style.display=f?'none':'';el('f-hedef').style.display=f?'':'none';el('result').style.display='none';_last=null;}
function hesapla(){
  var c=v('maliyet'), k=parseFloat(el('kdv').value); if(!(c>0)) return 'Birim maliyeti girin.';
  var s;
  if(radio('mod')==='fiyat'){var h=v('hedef'); if(!(h>=0&&h<100)) return 'Hedef marj 0–99 arasında olmalı.'; s=c/(1-h/100);}
  else {s=v('satis'); if(!(s>0)) return 'Satış fiyatını girin.';}
  var p=s-c, marj=p/s*100, mk=p/c*100;
  return {main:[radio('mod')==='fiyat'?'Olması gereken satış fiyatı':'Kâr marjı', radio('mod')==='fiyat'?tl(s):pct(marj)],
    sub:radio('mod')==='fiyat'?'KDV dahil etiket: '+tl(s*(1+k/100)):'Birim kâr: '+tl(p),
    rows:[['Satış fiyatı (KDV hariç)',tl(s)],['Birim kâr',tl(p),p>=0?'hl':'neg'],['Kâr marjı (satışa göre)',pct(marj)],['Markup (maliyete göre)',pct(mk)],['KDV dahil satış fiyatı',tl(s*(1+k/100))],['Satış başına KDV',tl(s*k/100)]]};
}''',
article='''
<h2 id="nedir">Kâr marjı nedir?</h2>
<p>Kâr marjı, satış fiyatının yüzde kaçının kâr olarak işletmede kaldığını gösterir. Her 100 ₺’lik satıştan ne kadar kazandığınızı anlatır ve fiyatlandırma, kampanya ve indirim kararlarının temelini oluşturur.</p>
<div class="formula">Kâr marjı (%) = (Satış fiyatı − Maliyet) ÷ Satış fiyatı × 100</div>
<div class="example"><p><b>Örnek:</b> Maliyeti 400 ₺ olan ürün 560 ₺’ye satılıyorsa: (560 − 400) ÷ 560 × 100 = <b>%28,6 kâr marjı</b>. Aynı satışta markup (maliyete göre kâr) %40’tır.</p></div>

<h2 id="hedef">Hedef kâr marjına göre satış fiyatı nasıl bulunur?</h2>
<p>En yaygın hata, %30 marj için maliyete %30 eklemektir. Bu yöntem gerçekte %23 marj verir. Doğru yöntem maliyeti (1 − marj) değerine bölmektir:</p>
<div class="formula">Satış fiyatı = Maliyet ÷ (1 − Hedef marj ÷ 100)</div>
<div class="example"><p><b>Örnek:</b> 400 ₺ maliyetli ürüne %30 marj: 400 ÷ 0,70 = <b>571,43 ₺</b> (KDV hariç). %20 KDV ile etiket fiyatı 685,71 ₺.</p></div>

<h2 id="turler">Brüt, faaliyet ve net kâr marjı</h2>
<div class="table-wrap"><table><thead><tr><th>Marj türü</th><th>Hesaplama</th></tr></thead><tbody>
<tr><td>Brüt kâr marjı</td><td>(Satışlar − Satılan malın maliyeti) ÷ Satışlar</td></tr>
<tr><td>Faaliyet (FAVÖK) marjı</td><td>Faaliyet kârı ÷ Satışlar</td></tr>
<tr><td>Net kâr marjı</td><td>Vergi sonrası net kâr ÷ Satışlar</td></tr>
</tbody></table></div>
<p>Bu araç ürün bazında brüt marjı hesaplar. İşletmenin tüm giderlerini içeren net marj için <a href="/net-kar-hesaplama.html">net kâr hesaplama</a>, dönemsel brüt kâr için <a href="/brut-kar-hesaplama.html">brüt kâr hesaplama</a> araçlarını kullanabilirsiniz.</p>

<h2 id="sektor">Sektörlere göre tipik brüt kâr marjları</h2>
<div class="table-wrap"><table><thead><tr><th>Sektör</th><th>Tipik brüt marj</th></tr></thead><tbody>
<tr><td>Market / gıda perakende</td><td>%15 – 25</td></tr><tr><td>Elektronik perakende</td><td>%10 – 20</td></tr><tr><td>Giyim / tekstil</td><td>%45 – 60</td></tr>
<tr><td>Restoran / kafe</td><td>%60 – 70 (yemek maliyeti %30–40)</td></tr><tr><td>Yazılım / dijital ürün</td><td>%70 – 90</td></tr><tr><td>Kozmetik</td><td>%50 – 70</td></tr>
</tbody></table></div>
<p>Değerler genel eğilimleri göstermek içindir; işletmenin ölçeği ve kanalına göre değişir.</p>

<h2 id="indirim">İndirim kâr marjını nasıl etkiler?</h2>
<p>%30 marjla satılan bir üründe %10 indirim yapmak kârın üçte birini yok eder. İndirim kararından önce kalan marjı kontrol edin; zincirleme bayi iskontolarını <a href="/iskonto-hesaplama.html">iskonto hesaplama</a> aracıyla hesaplayabilirsiniz.</p>
''',
faq=[
('%30 kâr marjı nasıl hesaplanır?','Satış fiyatını bulmak için maliyeti 0,70’e bölün. 700 ₺ maliyetli bir ürün için satış fiyatı 1.000 ₺ olur; 300 ₺ kâr satışın %30’udur.'),
('Kâr marjı ile kâr oranı (markup) aynı mı?','Hayır. Kâr marjı kârı satış fiyatına, markup ise maliyete böler. Aynı satış için markup her zaman marjdan yüksektir.'),
('Kâr marjı hesaplamasına KDV dahil edilir mi?','Hayır. Maliyet ve satış fiyatını KDV hariç kullanın; KDV müşteriden tahsil edilip devlete ödenir.'),
('İyi bir kâr marjı kaç olmalı?','Sektöre bağlıdır. Perakendede %20–30, hizmet ve dijital ürünlerde %50 ve üzeri yaygındır. Net marjın enflasyon ortamında da pozitif kalması gerekir.'),
],
related=['kar-zarar-hesaplama','net-kar-hesaplama','brut-kar-hesaplama','iskonto-hesaplama','kdv-hesaplama','basa-bas-noktasi-hesaplama'],
))

# ───────────────────────── NET KAR ─────────────────────────
TOOLS.append(dict(
slug='net-kar-hesaplama', name='Net Kâr Hesaplama', cat='isletme', ico='✅',
title='Net Kâr Hesaplama 2026 – Vergi Sonrası Kârım Ne Kadar? | Hesaplarsın',
desc='Satış geliri, maliyet, giderler ve vergiyle brüt kârı, faaliyet kârını, vergi sonrası net kârı ve net kâr marjını hesaplayın. İşletmeler ve şahıs şirketleri için.',
h1='✅ Net Kâr Hesaplama',
lead='Aylık veya yıllık gelir ve giderlerinizi girin; brüt kârdan başlayarak vergi sonrası net kârınızı ve net kâr marjınızı adım adım görün.',
form='''<div class="form-grid">
<div class="field"><label for="gelir">Net Satış Gelirleri (₺)</label><input type="number" id="gelir" placeholder="örn: 1.500.000" inputmode="decimal"></div>
<div class="field"><label for="smm">Satılan Malın Maliyeti (₺)</label><input type="number" id="smm" placeholder="örn: 900.000" inputmode="decimal"></div>
<div class="field"><label for="faal">Faaliyet Giderleri (₺) <small>kira, maaş, pazarlama</small></label><input type="number" id="faal" placeholder="örn: 350.000" inputmode="decimal"></div>
<div class="field"><label for="diger">Diğer Gelir (+) / Gider (−) (₺) <small>faiz vb.</small></label><input type="number" id="diger" placeholder="örn: -20.000" inputmode="decimal"></div>
<div class="field full"><label for="vergi">Vergi Türü</label><select id="vergi"><option value="25">Kurumlar vergisi – %25</option><option value="gv">Şahıs işletmesi – gelir vergisi tarifesi (yıllık)</option><option value="0">Vergi hesaplama</option></select></div>
</div>''',
js=r'''
function gvTarife(m){var d=[[190000,.15],[400000,.20],[1000000,.27],[5300000,.35],[Infinity,.40]],t=0,p=0;for(var i=0;i<d.length;i++){if(m>p)t+=(Math.min(m,d[i][0])-p)*d[i][1];p=d[i][0];}return t;}
function hesapla(){
  var g=v('gelir'), s=v('smm')||0, f=v('faal')||0, o=v('diger')||0; if(!(g>0)) return 'Net satış gelirini girin.';
  var brut=g-s, faaliyet=brut-f, vok=faaliyet+o, tur=el('vergi').value;
  var vergi=vok<=0?0:(tur==='gv'?gvTarife(vok):vok*parseFloat(tur)/100), net=vok-vergi;
  return {main:[net>=0?'Net kâr':'Net zarar', tl(Math.abs(net))], sub:'Net kâr marjı: '+pct(net/g*100),
    rows:[['Brüt kâr',tl(brut)],['Brüt kâr marjı',pct(brut/g*100)],['Faaliyet kârı (FVÖK)',tl(faaliyet)],['Faaliyet kâr marjı',pct(faaliyet/g*100)],['Vergi öncesi kâr',tl(vok)],['Hesaplanan vergi',tl(vergi),'neg'],['Net kâr',tl(net),net>=0?'hl':'neg']],
    note:tur==='gv'?'Şahıs işletmelerinde ücret dışı gelirler için 2026 gelir vergisi tarifesi kullanılmıştır; indirim ve istisnalar dahil değildir.':'Kurumlar vergisi oranı genel oran olan %25 alınmıştır; bankalar ve finans şirketleri için oran farklıdır.'};
}''',
article='''
<h2 id="nedir">Net kâr nedir?</h2>
<p>Net kâr, bir işletmenin belirli bir dönemde elde ettiği tüm gelirlerden; satılan malların maliyeti, faaliyet giderleri, finansman giderleri ve vergiler düşüldükten sonra kalan tutardır. Gelir tablosunun “son satırı” olduğu için İngilizcede <i>bottom line</i> olarak da anılır. İşletmenin gerçekten kazanıp kazanmadığını gösteren en temel göstergedir.</p>

<h2 id="adimlar">Net kâr nasıl hesaplanır? (Adım adım)</h2>
<div class="formula">1) Brüt kâr = Net satışlar − Satılan malın maliyeti<br>2) Faaliyet kârı = Brüt kâr − Faaliyet giderleri<br>3) Vergi öncesi kâr = Faaliyet kârı ± Diğer gelir/giderler<br>4) Net kâr = Vergi öncesi kâr − Vergi</div>
<div class="example"><p><b>Örnek (yıllık, limited şirket):</b> Satışlar 1.500.000 ₺, SMM 900.000 ₺, faaliyet giderleri 350.000 ₺, faiz gideri 20.000 ₺:</p>
<p>Brüt kâr 600.000 → Faaliyet kârı 250.000 → Vergi öncesi 230.000 → %25 kurumlar vergisi 57.500 → <b>Net kâr 172.500 ₺</b> (net marj %11,5).</p></div>

<h2 id="vergi">Hangi vergi oranı kullanılmalı?</h2>
<div class="table-wrap"><table><thead><tr><th>İşletme türü</th><th>Vergi</th></tr></thead><tbody>
<tr><td>Limited / anonim şirket</td><td>Kurumlar vergisi, genel oran %25</td></tr>
<tr><td>Şahıs işletmesi, serbest meslek</td><td>Gelir vergisi, %15–40 artan oranlı tarife</td></tr>
<tr><td>Basit usul esnaf</td><td>Kazancın belirli tutara kadarı istisna</td></tr>
</tbody></table></div>
<p>Şahıs işletmeleri için vergiyi ayrıntılı görmek isterseniz <a href="/gelir-vergisi-hesaplama.html">gelir vergisi hesaplama</a> aracını kullanabilirsiniz. Kesin vergi hesabı için mali müşavirinize danışın.</p>

<h2 id="marj">Net kâr marjı kaç olmalı?</h2>
<p>Net kâr marjı, net kârın satışlara oranıdır. Perakende ve toptan ticarette %2–5, üretimde %5–10, hizmet ve yazılım işletmelerinde %15 ve üzeri sağlıklı kabul edilebilir. Marjınız düşükse önce <a href="/kar-marji-hesaplama.html">ürün bazında kâr marjını</a>, ardından sabit giderleri gözden geçirin.</p>

<h2 id="nakit">Net kâr ile nakit akışı aynı şey mi?</h2>
<p>Hayır. Vadeli satışlar, stok yatırımları, kredi anapara ödemeleri ve amortisman, kâr ile kasadaki nakit arasında fark yaratır. Kâr eden bir işletme nakit sıkıntısı yaşayabilir. Bu nedenle kâr hesabını nakit akışı planıyla birlikte takip edin; sabit giderleri karşılayacak satış seviyesini <a href="/basa-bas-noktasi-hesaplama.html">başa baş noktası</a> ile bulun.</p>
''',
faq=[
('Net kâr ile brüt kâr arasındaki fark nedir?','Brüt kâr yalnızca satılan malın maliyetini düşer. Net kâr ise faaliyet giderleri, finansman giderleri ve vergiler de düşüldükten sonra kalan tutardır.'),
('Net kâr marjı nasıl hesaplanır?','Net kârı net satışlara bölüp 100 ile çarpın. 2.000.000 ₺ satıştan 150.000 ₺ net kâr elde eden işletmenin net marjı %7,5’tir.'),
('Kurumlar vergisi oranı 2026’da kaç?','Genel kurumlar vergisi oranı %25’tir. Bankalar, finansal kiralama ve sigorta şirketleri gibi bazı kurumlar için oran %30’dur.'),
('Amortisman net kârı etkiler mi?','Evet. Amortisman faaliyet gideri olarak kârı azaltır, ancak nakit çıkışı gerektirmez. Bkz. amortisman hesaplama.'),
],
related=['brut-kar-hesaplama','kar-marji-hesaplama','basa-bas-noktasi-hesaplama','gelir-vergisi-hesaplama','amortisman-hesaplama','ciro-hesaplama'],
))

# ───────────────────────── STOK KARLILIĞI ─────────────────────────
TOOLS.append(dict(
slug='stok-karliligi-hesaplama', name='Stok Kârlılığı Hesaplama', cat='isletme', ico='📦',
title='Stok Kârlılığı Hesaplama – Stok Devir Hızı, GMROI | Hesaplarsın',
desc='Ortalama stok maliyeti, satışlar ve brüt kârla stok devir hızını, stokta kalma süresini (gün) ve stok yatırımının getirisini (GMROI) hesaplayın.',
h1='📦 Stok Kârlılığı Hesaplama',
lead='Stoğa bağladığınız paranın size ne kadar kazandırdığını ölçün: stok devir hızı, stokta ortalama kalma süresi ve GMROI tek hesaplamada.',
form='''<div class="form-grid">
<div class="field"><label for="bas">Dönem Başı Stok (₺, maliyet)</label><input type="number" id="bas" placeholder="örn: 400.000" inputmode="decimal"></div>
<div class="field"><label for="son">Dönem Sonu Stok (₺, maliyet)</label><input type="number" id="son" placeholder="örn: 500.000" inputmode="decimal"></div>
<div class="field"><label for="satis">Dönem Net Satışları (₺)</label><input type="number" id="satis" placeholder="örn: 2.700.000" inputmode="decimal"></div>
<div class="field"><label for="smm">Satılan Malın Maliyeti (₺)</label><input type="number" id="smm" placeholder="örn: 1.800.000" inputmode="decimal"></div>
<div class="field full"><label for="gun">Dönem Uzunluğu</label><select id="gun"><option value="365" selected>1 yıl</option><option value="182">6 ay</option><option value="91">3 ay</option><option value="30">1 ay</option></select></div>
</div>''',
js=r'''
function hesapla(){
  var b=v('bas'), s=v('son'), sat=v('satis'), smm=v('smm'), g=parseFloat(el('gun').value);
  if(!(b>=0)||!(s>=0)||!(b+s>0)) return 'Dönem başı ve sonu stok değerlerini girin.'; if(!(smm>0)) return 'Satılan malın maliyetini girin.';
  var ort=(b+s)/2, devir=smm/ort, gun=g/devir, rows=[['Ortalama stok',tl(ort)],['Stok devir hızı',num(devir,2)+' kez'],['Stokta ortalama kalma süresi',num(gun,0)+' gün']];
  if(sat>0){var bk=sat-smm; rows.push(['Brüt kâr',tl(bk)]); rows.push(['Brüt kâr marjı',pct(bk/sat*100)]); rows.push(['GMROI (stok yatırımının brüt getirisi)',num(bk/ort,2)+' ₺ / 1 ₺ stok','hl']);}
  return {main:['Stok devir hızı', num(devir,2)+' kez'], sub:'Stok ortalama '+num(gun,0)+' günde bir yenileniyor', rows:rows};
}''',
article='''
<h2 id="nedir">Stok kârlılığı neden önemli?</h2>
<p>Perakende ve toptan ticarette işletmenin parasının büyük kısmı stokta durur. Raflarda bekleyen her ürün; depolama maliyeti, fire, modası geçme ve enflasyonda değer kaybı riski taşır. Stok kârlılığı, bu yatırımın ne kadar hızlı nakde ve kâra dönüştüğünü gösterir. Üç temel ölçüt kullanılır: stok devir hızı, stokta kalma süresi ve GMROI.</p>

<h2 id="devir">Stok devir hızı nasıl hesaplanır?</h2>
<div class="formula">Ortalama stok = (Dönem başı stok + Dönem sonu stok) ÷ 2<br>Stok devir hızı = Satılan malın maliyeti ÷ Ortalama stok<br>Stokta kalma süresi (gün) = 365 ÷ Stok devir hızı</div>
<div class="example"><p><b>Örnek:</b> Yıllık SMM 1.800.000 ₺, ortalama stok 450.000 ₺ ise devir hızı <b>4</b>’tür; stok yılda 4 kez yenilenir ve ürünler ortalama <b>91 gün</b> depoda kalır.</p></div>

<h2 id="gmroi">GMROI nedir?</h2>
<p>GMROI (Gross Margin Return on Inventory Investment), stoğa yatırılan her 1 ₺’nin bir dönemde kaç ₺ brüt kâr getirdiğini gösterir. Perakendecilerin hangi ürün grubuna daha fazla raf ve sermaye ayıracağına karar vermesinde kullanılır.</p>
<div class="formula">GMROI = Brüt kâr ÷ Ortalama stok maliyeti</div>
<p>GMROI 1’in altındaysa ürün grubu, stokta tutulma maliyetini bile karşılamıyor olabilir. Perakendede 2–3 ve üzeri iyi kabul edilir.</p>

<h2 id="sektor">Sektörlere göre stok devir hızı</h2>
<div class="table-wrap"><table><thead><tr><th>Sektör</th><th>Yıllık devir hızı</th><th>Stokta kalma</th></tr></thead><tbody>
<tr><td>Market / taze gıda</td><td>12 – 24</td><td>15 – 30 gün</td></tr><tr><td>Eczane / kozmetik</td><td>6 – 10</td><td>36 – 60 gün</td></tr>
<tr><td>Giyim</td><td>3 – 5</td><td>73 – 120 gün</td></tr><tr><td>Mobilya / beyaz eşya</td><td>2 – 4</td><td>90 – 180 gün</td></tr><tr><td>Yedek parça / hırdavat</td><td>2 – 3</td><td>120 – 180 gün</td></tr>
</tbody></table></div>

<h2 id="iyilestirme">Stok kârlılığını artırmanın yolları</h2>
<ul>
<li>ABC analiziyle cironun %80’ini getiren ürünlere odaklanın; yavaş dönen ürünleri azaltın.</li>
<li>Uzun süre satılmayan stokları kampanya ile eritin; indirimin marjınıza etkisini <a href="/kar-marji-hesaplama.html">kâr marjı hesaplama</a> ile kontrol edin.</li>
<li>Tedarikçilerle daha sık ve küçük partilerle sipariş anlaşması yapın.</li>
<li>Satış verisine dayalı minimum-maksimum stok seviyeleri belirleyin.</li>
</ul>
''',
faq=[
('Stok devir hızı yüksek olması iyi mi?','Genellikle evet; paranın stokta daha az beklediğini gösterir. Ancak aşırı yüksek devir, sık stok tükenmesi ve kaçan satış anlamına da gelebilir.'),
('Stok devir hızı satışlarla mı maliyetle mi hesaplanır?','Doğru yöntem, stok maliyet değeriyle tutulduğu için satılan malın maliyetini kullanmaktır. Satış tutarı kullanılırsa devir hızı olduğundan yüksek çıkar.'),
('Ortalama stok nasıl bulunur?','En basit yöntem dönem başı ve dönem sonu stokların ortalamasıdır. Daha hassas sonuç için aylık stok değerlerinin ortalaması alınabilir.'),
('GMROI kaç olmalı?','Perakendede 2 ve üzeri iyi, 3 ve üzeri çok iyi kabul edilir. 1’in altı stok yatırımının verimsiz olduğuna işaret eder.'),
],
related=['kar-marji-hesaplama','brut-kar-hesaplama','net-kar-hesaplama','ciro-hesaplama','iskonto-hesaplama'],
))

# ───────────────────────── PRİM ─────────────────────────
TOOLS.append(dict(
slug='prim-hesaplama', name='Satış Primi Hesaplama', cat='maas', ico='🏆',
title='Prim Hesaplama – Satış Primi, Kademeli Prim ve Hedef Primi | Hesaplarsın',
desc='Satış tutarı ve prim oranıyla satış priminizi hesaplayın. Hedef aşımı, kademeli (basamaklı) prim sistemi ve primin bordroda vergiye etkisi açıklamalı.',
h1='🏆 Satış Primi Hesaplama',
lead='Aylık satış tutarınızı, prim oranınızı ve varsa hedefinizi girin; brüt priminizi ve hedef gerçekleşme oranınızı görün. Kademeli prim sistemi de desteklenir.',
form='''<div class="field full" style="margin-bottom:14px"><label>Prim Sistemi</label>
<div class="seg"><label><input type="radio" name="mod" value="sabit" checked onchange="modSec()">Sabit oran</label><label><input type="radio" name="mod" value="hedef" onchange="modSec()">Hedefi aşan kısma</label><label><input type="radio" name="mod" value="kademe" onchange="modSec()">Kademeli</label></div></div>
<div class="form-grid">
<div class="field"><label for="satis">Satış Tutarı (₺)</label><input type="number" id="satis" placeholder="örn: 850.000" inputmode="decimal"></div>
<div class="field" id="f-oran"><label for="oran">Prim Oranı (%)</label><input type="number" id="oran" placeholder="örn: 3" inputmode="decimal"></div>
<div class="field" id="f-hedef" style="display:none"><label for="hedef">Satış Hedefi (₺)</label><input type="number" id="hedef" placeholder="örn: 600.000" inputmode="decimal"></div>
<div class="field full" id="f-kademe" style="display:none"><label for="kademe">Kademeler <small>her satıra “üst sınır oran” yazın, son satır için sınır yerine * kullanın</small></label>
<textarea id="kademe" rows="4">300000 1
600000 2
* 3</textarea></div>
</div>''',
js=r'''
function modSec(){var m=radio('mod');el('f-oran').style.display=m==='kademe'?'none':'';el('f-hedef').style.display=m==='hedef'?'':'none';el('f-kademe').style.display=m==='kademe'?'':'none';el('result').style.display='none';_last=null;}
function hesapla(){
  var s=v('satis'), m=radio('mod'); if(!(s>0)) return 'Satış tutarını girin.';
  if(m==='kademe'){
    var satirlar=raw('kademe').split('\n').map(function(l){return l.trim().split(/\s+/);}).filter(function(x){return x.length>=2;});
    if(!satirlar.length) return 'Kademeleri girin.'; var prev=0, top=0, rows=[];
    for(var i=0;i<satirlar.length;i++){var lim=satirlar[i][0]==='*'?Infinity:parseFloat(satirlar[i][0].replace(/\./g,'').replace(',','.')), o=parseFloat(satirlar[i][1].replace(',','.'));
      if(s>prev){var dil=Math.min(s,lim)-prev, p=dil*o/100; top+=p; rows.push([tl(prev,0)+' – '+(lim===Infinity?'üzeri':tl(lim,0))+' (%'+num(o,o%1?1:0)+')',tl(p)]);} prev=lim;}
    rows.push(['Ortalama prim oranı',pct(top/s*100)]);
    return {main:['Toplam brüt prim', tl(top)], rows:rows, note:'Kademeli sistemde her oran yalnızca kendi dilimine giren satışa uygulanır.'};
  }
  var o=v('oran'); if(!(o>=0)) return 'Prim oranını girin.';
  if(m==='hedef'){var h=v('hedef'); if(!(h>0)) return 'Satış hedefini girin.'; var asim=Math.max(0,s-h), p=asim*o/100;
    return {main:['Brüt prim', tl(p)], sub:'Hedef gerçekleşme: '+pct(s/h*100,1), rows:[['Hedef',tl(h)],['Hedefi aşan satış',tl(asim)],['Prim oranı',pct(o)]], note:s<h?'Hedefe '+tl(h-s)+' kaldı.':''};}
  return {main:['Brüt prim', tl(s*o/100)], rows:[['Satış tutarı',tl(s)],['Prim oranı',pct(o)]]};
}''',
article='''
<h2 id="nedir">Satış primi nedir?</h2>
<p>Satış primi, çalışanın belirli bir dönemde gerçekleştirdiği satış performansına bağlı olarak sabit maaşına ek olarak ödenen değişken ücrettir. Perakende, otomotiv, emlak, sigorta, ilaç ve saha satış ekiplerinde yaygın olarak kullanılır. Prim sistemleri genellikle iş sözleşmesinde veya şirketin prim yönetmeliğinde tanımlanır.</p>

<h2 id="sistemler">Prim sistemleri ve hesaplama yöntemleri</h2>
<h3>1. Sabit oranlı prim</h3>
<div class="formula">Prim = Satış tutarı × Prim oranı ÷ 100</div>
<div class="example"><p>850.000 ₺ satış, %3 prim → <b>25.500 ₺</b></p></div>
<h3>2. Hedefi aşan kısma prim</h3>
<p>Belirlenen hedefe ulaşılana kadar prim ödenmez; hedefin üzerindeki satışa prim oranı uygulanır.</p>
<div class="formula">Prim = (Satış − Hedef) × Prim oranı ÷ 100</div>
<div class="example"><p>Hedef 600.000 ₺, satış 850.000 ₺, %3 → 250.000 × 0,03 = <b>7.500 ₺</b></p></div>
<h3>3. Kademeli (basamaklı) prim</h3>
<p>Satış arttıkça oran yükselir ve her oran yalnızca kendi dilimine uygulanır (gelir vergisi dilimleri gibi).</p>
<div class="example"><p>0–300.000 ₺ %1, 300.000–600.000 ₺ %2, üzeri %3; satış 850.000 ₺:</p><p>3.000 + 6.000 + 7.500 = <b>16.500 ₺</b></p></div>

<h2 id="vergi">Prim maaşa nasıl yansır? (Vergi ve SGK)</h2>
<p>Satış primi ücret niteliğindedir ve ödendiği ayın bordrosuna eklenir. Bu nedenle prim üzerinden <b>%14 SGK işçi payı, %1 işsizlik sigortası, gelir vergisi ve damga vergisi</b> kesilir. Primin eklendiği ay kümülatif vergi matrahı yükseldiği için vergi dilimi atlanabilir ve primin net karşılığı beklenenden düşük olabilir. Primli bir ayın net maaşını görmek için brüt maaş ile brüt primi toplayıp <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> aracına girebilirsiniz.</p>

<h2 id="haklar">Prim hakkında bilmeniz gerekenler</h2>
<ul>
<li>Düzenli ödenen primler, <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı</a> hesabında “giydirilmiş ücrete” dahil edilir (son bir yılın ortalaması).</li>
<li>İş sözleşmesinde tanımlanan prim hakkı işveren tarafından tek taraflı kaldırılamaz.</li>
<li>Prim hesaplamasında iade ve iptal edilen satışların düşülüp düşülmeyeceği yönetmelikte açıkça belirtilmelidir.</li>
</ul>
''',
faq=[
('Satış primi nasıl hesaplanır?','En basit yöntemle satış tutarı prim oranıyla çarpılır. 500.000 ₺ satış ve %2 oranında prim 10.000 ₺’dir.'),
('Primden vergi kesilir mi?','Evet. Prim ücret sayılır; SGK primi, işsizlik sigortası, gelir vergisi ve damga vergisi kesintilerine tabidir.'),
('Kademeli prim sistemi nasıl işler?','Satış tutarı dilimlere ayrılır ve her dilime kendi oranı uygulanır. Üst dilime geçmek, alt dilimlerdeki primi değiştirmez.'),
('Prim kıdem tazminatına dahil mi?','Düzenli ve sürekli ödenen primler son bir yıllık ortalamasıyla kıdem tazminatı hesabına dahil edilir.'),
],
related=['net-maas-hesaplama','komisyon-hesaplama','maas-zam-hesaplama','kidem-tazminati-hesaplama','saatlik-ucret-hesaplama'],
))

# ───────────────────────── MAAŞ ZAM ─────────────────────────
TOOLS.append(dict(
slug='maas-zam-hesaplama', name='Maaş Zam Hesaplama', cat='maas', ico='📊',
title='Maaş Zammı Hesaplama 2026 – Zam Oranı, Yeni Maaş ve Reel Artış | Hesaplarsın',
desc='Mevcut maaşınız ve zam oranınızla yeni maaşınızı hesaplayın ya da eski ve yeni maaş arasındaki zam oranını bulun. Enflasyona göre reel zammınızı da görün.',
h1='📊 Maaş Zam Hesaplama',
lead='Zam oranına göre yeni maaşınızı bulun ya da aldığınız zammın yüzde kaç olduğunu hesaplayın. Enflasyonu girerseniz zammın alım gücünüzü artırıp artırmadığını görün.',
form='''<div class="field full" style="margin-bottom:14px"><label>Ne hesaplamak istiyorsunuz?</label>
<div class="seg"><label><input type="radio" name="mod" value="yeni" checked onchange="modSec()">Zamlı maaş</label><label><input type="radio" name="mod" value="oran" onchange="modSec()">Zam oranı</label></div></div>
<div class="form-grid">
<div class="field"><label for="maas">Mevcut Maaş (₺)</label><input type="number" id="maas" placeholder="örn: 45.000" inputmode="decimal"></div>
<div class="field" id="f-oran"><label for="oran">Zam Oranı (%)</label><input type="number" id="oran" placeholder="örn: 30" inputmode="decimal"></div>
<div class="field" id="f-yeni" style="display:none"><label for="yeni">Yeni Maaş (₺)</label><input type="number" id="yeni" placeholder="örn: 58.500" inputmode="decimal"></div>
<div class="field"><label for="enf">Yıllık Enflasyon (%) <small>reel zam için</small></label><input type="number" id="enf" placeholder="örn: 29,73" inputmode="decimal"></div>
</div>''',
js=r'''
function modSec(){var o=radio('mod')==='oran';el('f-oran').style.display=o?'none':'';el('f-yeni').style.display=o?'':'none';el('result').style.display='none';_last=null;}
function hesapla(){
  var m=v('maas'); if(!(m>0)) return 'Mevcut maaşınızı girin.'; var o, y;
  if(radio('mod')==='oran'){y=v('yeni'); if(!(y>0)) return 'Yeni maaşı girin.'; o=(y/m-1)*100;} else {o=v('oran'); if(isNaN(o)) return 'Zam oranını girin.'; y=m*(1+o/100);}
  var rows=[['Mevcut maaş',tl(m)],['Zam oranı',pct(o)],['Aylık artış',tl(y-m),'hl'],['Yıllık ek kazanç',tl((y-m)*12)]], e=v('enf'), sub='';
  if(e>=0&&!isNaN(e)){var r=((1+o/100)/(1+e/100)-1)*100; rows.push(['Reel zam (enflasyondan arındırılmış)',pct(r),r>=0?'hl':'neg']); rows.push(['Enflasyon kadar zam için gereken maaş',tl(m*(1+e/100))]); sub=r>=0?'Zam enflasyonun üzerinde, alım gücünüz arttı':'Zam enflasyonun altında, alım gücünüz azaldı';}
  return {main:[radio('mod')==='oran'?'Zam oranı':'Yeni maaşınız', radio('mod')==='oran'?pct(o):tl(y)], sub:sub, rows:rows};
}''',
article='''
<h2 id="nasil">Maaş zammı nasıl hesaplanır?</h2>
<p>Zamlı maaşı bulmak için mevcut maaş, (1 + zam oranı) ile çarpılır. Zam oranını bulmak içinse yeni maaş eski maaşa bölünür ve 1 çıkarılır.</p>
<div class="formula">Yeni maaş = Mevcut maaş × (1 + Zam oranı ÷ 100)<br>Zam oranı (%) = (Yeni maaş ÷ Eski maaş − 1) × 100</div>
<div class="example"><p><b>Örnek:</b> 45.000 ₺ maaşa %30 zam: 45.000 × 1,30 = <b>58.500 ₺</b>. Aylık artış 13.500 ₺, yıllık ek kazanç 162.000 ₺.</p></div>

<h2 id="reel">Reel zam nedir?</h2>
<p>Reel zam, enflasyonun etkisi çıkarıldıktan sonra maaşınızın alım gücündeki gerçek değişimdir. %30 zam alırken enflasyon %29,73 ise alım gücünüz neredeyse aynı kalmıştır. Reel zam basitçe zam oranından enflasyonu çıkararak değil, şu formülle hesaplanır:</p>
<div class="formula">Reel zam = (1 + Zam oranı) ÷ (1 + Enflasyon) − 1</div>
<div class="example"><p><b>Örnek:</b> %30 zam, %29,73 enflasyon → 1,30 ÷ 1,2973 − 1 = <b>%0,21 reel artış</b>.</p></div>
<p>TÜİK verilerine göre Eylül 2026 itibarıyla yıllık TÜFE %29,73’tür. Geçmiş yıllara göre paranızın değerini görmek için <a href="/enflasyon-hesaplama.html">enflasyon hesaplama</a> aracını kullanabilirsiniz.</p>

<h2 id="brut-net">Brüt zam mı net zam mı?</h2>
<p>Zam oranı brüt maaşa uygulandığında, gelir vergisi dilimleri nedeniyle net maaştaki artış oranı farklı olabilir. Özellikle yılın ilerleyen aylarında vergi dilimi yükseldiği için net artış brüt artıştan düşük görünebilir. Zamlı brüt maaşınızın net karşılığını <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> ile görebilirsiniz.</p>

<h2 id="pazarlik">Zam görüşmesine nasıl hazırlanılır?</h2>
<ul>
<li>Son zamdan bu yana gerçekleşen enflasyonu hesaplayın; bu, alım gücünü korumak için gereken asgari orandır.</li>
<li>Pozisyonunuzun piyasa ücret aralığını araştırın (maaş anketleri, iş ilanları).</li>
<li>Somut katkılarınızı (satış artışı, maliyet tasarrufu, tamamlanan projeler) rakamlarla hazırlayın.</li>
<li>Zam dışında yan hakları da (yemek, yol, uzaktan çalışma, eğitim desteği) pazarlık masasına koyun.</li>
</ul>
''',
faq=[
('%25 zam ile maaşım ne kadar olur?','Maaşınızı 1,25 ile çarpın. 40.000 ₺ maaş %25 zamla 50.000 ₺ olur.'),
('Zam oranı nasıl bulunur?','Yeni maaşı eski maaşa bölüp 1 çıkarın ve 100 ile çarpın. 40.000 ₺’den 52.000 ₺’ye çıkan maaş için zam oranı %30’dur.'),
('Enflasyon kadar zam ne demek?','Maaşın son zamdan bu yana gerçekleşen enflasyon oranında artırılmasıdır. Bu durumda reel zam sıfırdır, alım gücü korunur.'),
('Zam brüt maaşa mı net maaşa mı yapılır?','İşverenler çoğunlukla brüt maaş üzerinden zam yapar. Sözleşmenizde net ücret tanımlıysa zam net ücrete de uygulanabilir.'),
],
related=['net-maas-hesaplama','enflasyon-hesaplama','saatlik-ucret-hesaplama','asgari-ucret-hesaplama','yuzde-hesaplama'],
))

# ───────────────────────── MEMUR & EMEKLİ ZAMMI ─────────────────────────
TOOLS.append(dict(
slug='memur-emekli-zammi-hesaplama', name='Memur ve Emekli Zammı Hesaplama', cat='kamu', ico='👴',
title='Ocak 2027 Memur ve Emekli Zammı Hesaplama | Hesaplarsın',
desc='Ocak 2027 SSK, Bağ-Kur emeklisi ve memur zammını hesaplayın: 6 aylık enflasyon, %5 toplu sözleşme, enflasyon farkı ve yeni maaşınız tek ekranda.',
h1='👴 Memur ve Emekli Zammı Hesaplama (Ocak 2027)',
lead='Maaşınızı ve kalan ayların enflasyon tahminini girin; Ocak 2027’de SSK/Bağ-Kur emeklisi veya memur olarak alacağınız zammı ve yeni maaşınızı görün.',
form='''<div class="form-grid">
<div class="field"><label for="tur">Kim için hesaplanacak?</label><select id="tur"><option value="emekli">SSK veya Bağ-Kur emeklisi</option><option value="memur">Memur</option><option value="memuremekli">Memur emeklisi (Emekli Sandığı)</option></select></div>
<div class="field"><label for="maas">Mevcut Aylık (₺)</label><input type="number" id="maas" placeholder="örn: 30.000" inputmode="decimal"></div>
<div class="field"><label for="aylik">Ekim–Aralık aylık ortalama enflasyon tahmini (%)</label><input type="number" id="aylik" value="1" inputmode="decimal"></div>
<div class="field"><label for="alti">6 aylık enflasyon (%) <small>biliyorsanız; boş bırakın</small></label><input type="number" id="alti" placeholder="örn: 8,77" inputmode="decimal"></div>
</div>''',
js=r'''
var Q3=0.0557, TS=0.05, TS_ONCEKI=0.07, KIDEM=73729.87;
function hesapla(){
  var m=v('maas'); if(!(m>0)) return 'Mevcut aylığınızı girin.';
  var a=v('aylik'); if(isNaN(a)) a=1; if(a<-2||a>10) return 'Aylık enflasyon tahmini −2 ile 10 arasında olmalı.';
  var h=v('alti'), h2=(h>0)?h/100:(1+Q3)*Math.pow(1+a/100,3)-1, tur=el('tur').value, z, rows=[['Temmuz–Aralık 6 aylık enflasyon',pct(h2*100)]];
  if(tur==='emekli'){ z=h2; rows.push(['Zam yöntemi','6 aylık TÜFE artışı kadar']); }
  else { var fark=Math.max(0,(1+h2)/(1+TS_ONCEKI)-1); z=(1+TS)*(1+fark)-1; rows.push(['Toplu sözleşme zammı (2027 ilk yarı)','%5,00']); rows.push(['Enflasyon farkı',pct(fark*100)]); }
  var y=m*(1+z);
  rows.push(['Toplam zam oranı',pct(z*100),'hl']); rows.push(['Aylık artış',tl(y-m)]); rows.push(['Ocak–Haziran 2027 toplam ek gelir',tl((y-m)*6)]);
  if(tur!=='emekli') rows.push(['Kıdem tazminatı tavanı (Ocak 2027, tahmini)',tl(KIDEM*(1+z))]);
  return {main:['Ocak 2027 tahmini aylık', tl(y)], sub:'%'+num(z*100,2)+' zam ile', rows:rows,
    note:'Temmuz–Eylül 2026 enflasyonu %5,57 olarak gerçekleşti. Kesin zam oranı, Aralık 2026 enflasyonunun açıklandığı Ocak 2027’nin ilk günlerinde belli olur. En düşük emekli aylığı kanunla ayrıca belirlenir.'};
}''',
article='''
<h2 id="nasil">Ocak 2027 zammı nasıl hesaplanır?</h2>
<p><b>SSK ve Bağ-Kur emeklileri</b> (5510 sayılı Kanun) Ocak ayında, önceki Temmuz–Aralık dönemindeki altı aylık TÜFE artışı kadar zam alır. <b>Memurlar ve memur emeklileri</b> ise 8. Dönem Toplu Sözleşme’ye göre 2027’nin ilk yarısı için <b>%5</b> zam alır; 2026’nın ikinci yarısındaki %7’lik toplu sözleşme zammını aşan enflasyon da <b>enflasyon farkı</b> olarak eklenir.</p>
<div class="formula">Emekli zammı = (1 + Temmuz) × (1 + Ağustos) × … × (1 + Aralık) − 1<br>Enflasyon farkı = (1 + 6 aylık enflasyon) ÷ 1,07 − 1<br>Memur zammı = 1,05 × (1 + Enflasyon farkı) − 1</div>
<div class="example"><p><b>Örnek:</b> Temmuz–Eylül enflasyonu %5,57; Ekim, Kasım ve Aralık’ta ayda %1 enflasyon olursa altı aylık enflasyon 1,0557 × 1,01³ − 1 = <b>%8,77</b> olur. SSK/Bağ-Kur emeklisi %8,77 zam alır. Memurun enflasyon farkı 1,0877 ÷ 1,07 − 1 = %1,65, toplam zammı 1,05 × 1,0165 − 1 = <b>%6,74</b> olur.</p></div>

<h2 id="senaryo">Ocak 2027 zam senaryoları</h2>
<div class="table-wrap"><table><thead><tr><th>Ekim–Aralık aylık ort.</th><th>6 aylık enflasyon</th><th>Emekli zammı</th><th>Memur zammı</th></tr></thead><tbody>
<tr><td>%0,6</td><td>%7,48</td><td>%7,48</td><td>%5,47</td></tr>
<tr><td>%1,0</td><td>%8,77</td><td>%8,77</td><td>%6,74</td></tr>
<tr><td>%1,4</td><td>%10,07</td><td>%10,07</td><td>%8,01</td></tr>
</tbody></table></div>
<p>Kurumların yıl sonu enflasyon tahminleri (OVP %28,4, TCMB Piyasa Katılımcıları Anketi %29,61) Ekim–Aralık için aylık ortalama %1–1,4 aralığına işaret ediyor. Ayrıntılı değerlendirme için <a href="/blog/memur-emekli-zammi-ocak-2027.html">Ocak 2027 memur ve emekli zammı</a> yazımıza bakın.</p>

<h2 id="takvim">Zam ne zaman kesinleşir?</h2>
<ul>
<li><b>3 Kasım 2026:</b> Ekim enflasyonu</li>
<li><b>3 Aralık 2026:</b> Kasım enflasyonu</li>
<li><b>Ocak 2027’nin ilk iş günleri:</b> Aralık enflasyonu ve kesin zam oranları</li>
</ul>
<p>Her veri açıklandığında hesaplayıcıdaki gerçekleşen enflasyon değerini güncelliyoruz. Tüm tarihler için <a href="/ekonomi-takvimi.html">ekonomi takvimine</a> bakın.</p>

<h2 id="kidem">Memur zammı kıdem tazminatı tavanını da belirler</h2>
<p>Kıdem tazminatı tavanı memur maaş katsayısına bağlıdır. Temmuz–Aralık 2026 tavanı 73.729,87 ₺’dir ve Ocak 2027’de memur zammıyla aynı oranda artması beklenir. Memur seçeneğinde hesaplayıcı tahmini yeni tavanı da gösterir; tazminatınızı <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı hesaplama</a> aracıyla bulabilirsiniz.</p>

<h2 id="dusuk">En düşük emekli aylığı</h2>
<p>Ekim 2026 itibarıyla en düşük emekli aylığı 23.552 ₺’dir. Bu tutar ayrıca kanunla belirlendiği için Ocak 2027’de yalnızca enflasyon oranında değil, yapılacak yasal düzenlemeye göre artırılabilir.</p>
''',
faq=[
('Ocak 2027 emekli zammı ne kadar olacak?','SSK ve Bağ-Kur emeklilerinin Ocak 2027 zammı Temmuz–Aralık 2026 enflasyonuna eşit olacak. Temmuz–Eylül döneminde enflasyon %5,57 oldu; Ekim–Aralık’ta aylık ortalama %1–1,4 enflasyonla zam yaklaşık %8,8–%10,1 olur.'),
('Ocak 2027 memur zammı ne kadar olacak?','Memurlar %5 toplu sözleşme zammına ek olarak, altı aylık enflasyonun %7’yi aşan kısmı kadar enflasyon farkı alacak. Mevcut tahminlerle toplam memur zammı yaklaşık %6,7–%8 aralığında.'),
('Memur emeklisinin zammı memurla aynı mı?','Evet. Emekli Sandığı’na tabi memur emeklileri, memurlarla aynı oranda (toplu sözleşme zammı + enflasyon farkı) zam alır.'),
('Emekli zammı ne zaman yatar?','Kesin oran Ocak 2027’nin ilk iş günlerinde açıklanır; zamlı aylıklar Ocak ayındaki olağan ödeme günlerinde hesaplara yatırılır.'),
],
related=['memur-maaslari','ogretmen-maasi','maas-zam-hesaplama','kidem-tazminati-hesaplama','emeklilik-yasi-hesaplama'],
sources=[('5510 sayılı Sosyal Sigortalar ve GSS Kanunu','https://www.mevzuat.gov.tr/mevzuatmetin/1.5.5510.pdf'),('TÜİK Tüketici Fiyat Endeksi','https://data.tuik.gov.tr/'),('ÇSGB – Kamu Görevlileri Toplu Sözleşmesi','https://www.csgb.gov.tr/')],
))

# ───────────────────────── İŞSİZLİK MAAŞI ─────────────────────────
TOOLS.append(dict(
slug='issizlik-maasi-hesaplama', name='İşsizlik Maaşı Hesaplama', cat='maas', ico='🧾',
title='İşsizlik Maaşı Hesaplama 2026 – Ne Kadar, Kaç Ay? | Hesaplarsın',
desc='2026 işsizlik maaşı hesaplama: son 4 ay brüt maaşınızın %40’ı, en fazla 26.424 TL. Prim gününe göre 6, 8 veya 10 ay; net tutar ve başvuru şartları.',
h1='🧾 İşsizlik Maaşı Hesaplama 2026',
lead='Son 4 aylık brüt maaş ortalamanızı ve son 3 yıldaki prim gün sayınızı girin; alacağınız aylık işsizlik maaşını, kaç ay ödeneceğini ve toplam tutarı görün.',
button='İşsizlik Maaşını Hesapla',
form='''<div class="form-grid">
<div class="field"><label for="brut">Son 4 Ayın Ortalama Brüt Maaşı (₺)</label><input type="number" id="brut" placeholder="örn: 45.000" inputmode="decimal"></div>
<div class="field"><label for="gun">Son 3 Yılda Ödenen Prim Günü</label><select id="gun"><option value="0">600 günden az</option><option value="180" selected>600 – 899 gün</option><option value="240">900 – 1079 gün</option><option value="300">1080 gün ve üzeri</option></select></div>
<div class="field full"><label class="chk"><input type="checkbox" id="kosul" checked> İşten kendi isteğim ve kusurum dışında çıkarıldım ve son 120 gün kesintisiz çalıştım</label></div>
</div>''',
js=r'''
var BR=33030, TAVAN=BR*0.8, DAMGA=0.00759;
function hesapla(){
  var b=v('brut'), g=+el('gun').value; if(!(b>0)) return 'Son 4 ayın ortalama brüt maaşını girin.';
  if(!el('kosul').checked) return 'İstifa eden, emekli olan veya kusurlu davranış nedeniyle işten çıkarılanlar işsizlik maaşı alamaz.';
  if(g===0) return 'İşsizlik maaşı için son 3 yılda en az 600 gün işsizlik sigortası primi ödenmiş olmalı.';
  var ham=b*0.40, brut=Math.min(ham,TAVAN), damga=brut*DAMGA, net=brut-damga, ay=g/30;
  return {main:['Aylık net işsizlik maaşı', tl(net)], sub:g+' gün ('+ay+' ay) boyunca',
    rows:[['Brüt maaşın %40’ı',tl(ham)],['Üst sınır (brüt asgari ücretin %80’i)',tl(TAVAN)],['Aylık brüt ödenek',tl(brut)],['Damga vergisi (binde 7,59)','−'+tl(damga),'neg'],['Aylık net ödenek',tl(net),'hl'],['Ödeme süresi',g+' gün ('+ay+' ay)'],['Toplam net ödeme',tl(net*ay)]],
    note:(ham>TAVAN?'Hesaplanan tutar üst sınırı aştığı için 2026 üst sınırı (26.424 ₺ brüt) uygulandı. ':'')+'İŞKUR’a işten ayrıldıktan sonraki 30 gün içinde başvurun; geç başvuruda geciken gün sayısı kadar süre kısalır.'};
}''',
article='''
<h2 id="ne-kadar">2026 işsizlik maaşı ne kadar?</h2>
<p>İşsizlik maaşı (işsizlik ödeneği), son 4 aylık brüt kazancınızın ortalamasının <b>%40’ı</b> kadardır. Ancak bu tutar, brüt asgari ücretin <b>%80’ini</b> geçemez. 2026 brüt asgari ücreti 33.030 ₺ olduğundan:</p>
<div class="table-wrap"><table><thead><tr><th></th><th>Brüt</th><th>Damga vergisi</th><th>Net</th></tr></thead><tbody>
<tr><td>En düşük (asgari ücretli)</td><td>13.212,00 ₺</td><td>100,28 ₺</td><td><b>13.111,72 ₺</b></td></tr>
<tr><td>En yüksek (üst sınır)</td><td>26.424,00 ₺</td><td>200,56 ₺</td><td><b>26.223,44 ₺</b></td></tr>
</tbody></table></div>
<p>İşsizlik maaşından gelir vergisi ve SGK primi kesilmez; yalnızca binde 7,59 damga vergisi kesilir. Ödenek alırken genel sağlık sigortanız devlet tarafından ödenir.</p>
<div class="formula">Aylık brüt ödenek = min(Son 4 ay brüt ortalama × %40 ; Brüt asgari ücret × %80)<br>Net ödenek = Brüt ödenek × (1 − 0,00759)</div>

<h2 id="tablo">Maaşa göre işsizlik maaşı tablosu</h2>
<div class="table-wrap"><table><thead><tr><th>Son 4 ay brüt ortalama</th><th>Aylık net işsizlik maaşı</th><th>6 ay toplam</th><th>10 ay toplam</th></tr></thead><tbody>
<tr><td>33.030 ₺ (asgari ücret)</td><td>13.111,72 ₺</td><td>78.670 ₺</td><td>131.117 ₺</td></tr>
<tr><td>40.000 ₺</td><td>15.878,56 ₺</td><td>95.271 ₺</td><td>158.786 ₺</td></tr>
<tr><td>50.000 ₺</td><td>19.848,20 ₺</td><td>119.089 ₺</td><td>198.482 ₺</td></tr>
<tr><td>60.000 ₺</td><td>23.817,84 ₺</td><td>142.907 ₺</td><td>238.178 ₺</td></tr>
<tr><td>66.060 ₺ ve üzeri</td><td>26.223,44 ₺ (tavan)</td><td>157.341 ₺</td><td>262.234 ₺</td></tr>
</tbody></table></div>
<p>66.060 ₺ ve üzerindeki brüt maaşlarda %40 oranı üst sınırı aştığı için herkes aynı tutarı alır.</p>

<h2 id="sure">İşsizlik maaşı kaç ay verilir?</h2>
<p>Ödeme süresi, işten ayrılmadan önceki son 3 yılda ödenen işsizlik sigortası prim gününe göre belirlenir:</p>
<div class="table-wrap"><table><thead><tr><th>Son 3 yılda prim günü</th><th>Ödeme süresi</th></tr></thead><tbody>
<tr><td>600 – 899 gün</td><td>180 gün (6 ay)</td></tr>
<tr><td>900 – 1079 gün</td><td>240 gün (8 ay)</td></tr>
<tr><td>1080 gün ve üzeri</td><td>300 gün (10 ay)</td></tr>
</tbody></table></div>

<h2 id="sartlar">İşsizlik maaşı alma şartları</h2>
<ul>
<li>İş sözleşmesinin <b>kendi isteğiniz ve kusurunuz dışında</b> sona ermesi (işveren feshi, iş yerinin kapanması, haklı nedenle fesih gibi).</li>
<li>İşten ayrılmadan önceki <b>son 120 gün</b> boyunca hizmet akdiyle kesintisiz çalışmış olmak.</li>
<li>Son 3 yılda en az <b>600 gün</b> işsizlik sigortası primi ödenmiş olmak.</li>
<li>İşten ayrıldıktan sonraki <b>30 gün içinde</b> İŞKUR’a başvurmak.</li>
</ul>
<p>İstifa edenler, emekli olanlar, ahlak ve iyi niyet kurallarına aykırı davranış nedeniyle (İş Kanunu m.25/II) işten çıkarılanlar işsizlik maaşı alamaz. Haklı nedenle (örneğin ücretin ödenmemesi) iş sözleşmesini fesheden çalışan ise ödenek alabilir.</p>

<h2 id="basvuru">Başvuru nasıl yapılır?</h2>
<ol>
<li>İşveren, işten çıkışınızı SGK’ya doğru kodla bildirmelidir; işten ayrılış bildirgesinin kodu ödenek hakkını doğrudan belirler.</li>
<li>e-Devlet’te “İŞKUR İşsizlik Ödeneği Başvurusu” hizmetinden veya İŞKUR hizmet merkezinden başvurun.</li>
<li>Başvurunuz onaylanırsa ödenek, hak kazandığınız tarihi izleyen ayın sonundan itibaren her ay banka hesabınıza yatırılır.</li>
</ol>

<h2 id="kesilme">İşsizlik maaşı ne zaman kesilir?</h2>
<p>Yeni bir işe girdiğinizde, emekli olduğunuzda, İŞKUR’un önerdiği uygun bir işi veya eğitimi geçerli neden olmadan reddettiğinizde ya da kurumun çağrılarına uymadığınızda ödenek kesilir. Ödenek alırken kayıt dışı çalıştığınız tespit edilirse aldığınız tutar faiziyle geri istenir.</p>
<p>İşten çıkarıldıysanız <a href="/kidem-tazminati-hesaplama.html">kıdem tazminatı</a> ve <a href="/ihbar-tazminati-hesaplama.html">ihbar tazminatı</a> haklarınızı da hesaplamayı unutmayın.</p>
''',
faq=[
('2026 en yüksek işsizlik maaşı ne kadar?','2026’da en yüksek işsizlik maaşı brüt 26.424 ₺, damga vergisi kesildikten sonra net 26.223,44 ₺’dir. Bu, brüt asgari ücretin %80’idir.'),
('Asgari ücretli ne kadar işsizlik maaşı alır?','Asgari ücretle çalışmış biri, brüt asgari ücretin %40’ı olan 13.212 ₺ brüt, yaklaşık 13.111,72 ₺ net işsizlik maaşı alır.'),
('İstifa eden işsizlik maaşı alabilir mi?','Hayır. Kendi isteğiyle istifa edenler işsizlik maaşı alamaz. Ancak ücretin ödenmemesi gibi haklı nedenlerle iş sözleşmesini fesheden çalışanlar ödenek alabilir.'),
('İşsizlik maaşı kaç ay verilir?','Son 3 yılda 600 gün prim için 6 ay, 900 gün için 8 ay, 1080 gün ve üzeri için 10 ay ödenir.'),
('İşsizlik maaşı başvurusu ne zamana kadar yapılır?','İşten ayrıldıktan sonraki 30 gün içinde İŞKUR’a başvurulmalıdır. Geç başvuruda geciken gün sayısı kadar ödeme süresinden düşülür.'),
],
related=['kidem-tazminati-hesaplama','ihbar-tazminati-hesaplama','net-maas-hesaplama','asgari-ucret-hesaplama','yillik-izin-hesaplama'],
sources=[('4447 sayılı İşsizlik Sigortası Kanunu m.50–51','https://www.mevzuat.gov.tr/mevzuatmetin/1.5.4447.pdf'),('İŞKUR – İşsizlik Ödeneği','https://www.iskur.gov.tr/')],
))

# ───────────────────────── SAATLİK ÜCRET ─────────────────────────
TOOLS.append(dict(
slug='saatlik-ucret-hesaplama', name='Saatlik Ücret Hesaplama', cat='maas', ico='🕐',
title='Saatlik Ücret Hesaplama 2026 – Maaşım Saatte Kaç TL? | Hesaplarsın',
desc='Asgari ücretle saatlik brüt 146,80 TL, net 124,78 TL. Maaşınızı girin; saatlik, günlük ve mesai ücretinizi 2026 kurallarına (225 saat) göre anında görün.',
h1='🕐 Saatlik Ücret Hesaplama',
lead='Aylık maaşınızın saatlik ve günlük karşılığını, ya da saatlik ücretinizle ayda ne kazanacağınızı hesaplayın. Fazla mesai saat ücretiniz de otomatik gösterilir.',
form='''<div class="field full" style="margin-bottom:14px"><label>Hesaplama Yönü</label>
<div class="seg"><label><input type="radio" name="mod" value="aylik" checked onchange="modSec()">Aylık maaştan saatliğe</label><label><input type="radio" name="mod" value="saatlik" onchange="modSec()">Saatlikten aylığa</label></div></div>
<div class="form-grid">
<div class="field"><label for="tutar" id="lbl-tutar">Aylık Maaş (₺)</label><input type="number" id="tutar" placeholder="örn: 45.000" inputmode="decimal"></div>
<div class="field"><label for="saat">Aylık Çalışma Saati</label><select id="saat"><option value="225" selected>225 saat (İş Kanunu – 45 saat/hafta)</option><option value="195">195 saat (Haftada 45 saat × 4,33)</option><option value="173">173 saat (40 saat/hafta)</option><option value="manuel">Kendim gireceğim</option></select></div>
<div class="field" id="f-ozel" style="display:none"><label for="ozel">Aylık Saat</label><input type="number" id="ozel" placeholder="örn: 160" inputmode="decimal"></div>
</div>''',
js=r'''
function onReady(){el('saat').addEventListener('change',function(){el('f-ozel').style.display=el('saat').value==='manuel'?'':'none';});}
function modSec(){el('lbl-tutar').textContent=radio('mod')==='aylik'?'Aylık Maaş (₺)':'Saatlik Ücret (₺)';el('result').style.display='none';_last=null;}
function hesapla(){
  var t=v('tutar'), h=el('saat').value==='manuel'?v('ozel'):parseFloat(el('saat').value);
  if(!(t>0)) return 'Tutarı girin.'; if(!(h>0)) return 'Aylık çalışma saatini girin.';
  var saatlik=radio('mod')==='aylik'?t/h:t, aylik=saatlik*h;
  return {main:[radio('mod')==='aylik'?'Saatlik ücret':'Aylık kazanç', radio('mod')==='aylik'?tl(saatlik):tl(aylik)],
    rows:[['Saatlik ücret',tl(saatlik)],['Günlük ücret (aylık ÷ 30)',tl(aylik/30)],['Haftalık ücret',tl(aylik/30*7)],['Aylık ücret',tl(aylik)],['Yıllık ücret',tl(aylik*12)],
      ['Fazla mesai saat ücreti (%50 zamlı)',tl(saatlik*1.5),'hl'],['Fazla sürelerle çalışma (%25 zamlı)',tl(saatlik*1.25)]],
    note:'İş Kanunu uygulamasında aylık ücretten saatlik ücrete geçişte 225 saat kullanılır. Hesaplamalar brüt ücret üzerinden yapılmalıdır.'};
}''',
article='''
<h2 id="nasil">Saatlik ücret nasıl hesaplanır?</h2>
<p>Aylık maaş alan bir çalışanın saatlik ücreti, aylık brüt ücretin aylık çalışma saatine bölünmesiyle bulunur. Türkiye’de İş Kanunu’na göre haftalık çalışma süresi en fazla 45 saattir ve aylık ücret 30 gün üzerinden hesaplanır. Yargıtay ve uygulamada aylık ücretli çalışanlar için <b>225 saat</b> esas alınır (30 gün × 7,5 saat).</p>
<div class="formula">Saatlik ücret = Aylık brüt ücret ÷ 225<br>Günlük ücret = Aylık brüt ücret ÷ 30</div>
<div class="example"><p><b>Örnek:</b> 45.000 ₺ brüt maaş: 45.000 ÷ 225 = <b>200 ₺/saat</b>, günlük 1.500 ₺. Fazla mesai saat ücreti 200 × 1,5 = 300 ₺.</p></div>

<h2 id="asgari">2026 asgari ücret saatlik ne kadar?</h2>
<div class="table-wrap"><table><thead><tr><th>2026 asgari ücret</th><th>Brüt</th><th>Net</th></tr></thead><tbody>
<tr><td>Aylık</td><td>33.030,00 ₺</td><td>28.075,50 ₺</td></tr>
<tr><td>Günlük (÷30)</td><td>1.101,00 ₺</td><td>935,85 ₺</td></tr>
<tr><td>Saatlik (÷225)</td><td>146,80 ₺</td><td>124,78 ₺</td></tr>
</tbody></table></div>
<p>Asgari ücretin işverene toplam maliyetini ve diğer ayrıntıları <a href="/asgari-ucret-hesaplama.html">asgari ücret hesaplama</a> sayfasında bulabilirsiniz.</p>

<h2 id="225">Neden 225 saat? 195 ve 173 saat ne zaman kullanılır?</h2>
<ul>
<li><b>225 saat:</b> İş Kanunu uygulaması; hafta tatili ücretli olduğu için 30 günün tamamı × 7,5 saat. Fazla mesai ve eksik gün kesintilerinde kullanılır.</li>
<li><b>195 saat:</b> Haftada 45 saat × ayda ortalama 4,33 hafta; fiilen çalışılan saati gösterir.</li>
<li><b>173 saat:</b> Haftada 40 saat çalışılan işyerleri (kamu ve bazı özel sektör).</li>
</ul>
<p>Serbest çalışanlar (freelance) için saatlik ücreti belirlerken ise faturalandırılabilir saatler (genellikle haftada 25–30 saat), vergiler, BAĞ-KUR primi ve izin günleri dikkate alınmalıdır.</p>

<h2 id="mesai">Fazla mesai ücreti nasıl hesaplanır?</h2>
<p>Haftalık 45 saati aşan her saat için saatlik ücretin %50 fazlası ödenir. Haftalık çalışma süresi 45 saatin altında belirlenmiş işyerlerinde, sözleşmedeki süre ile 45 saat arasındaki çalışmalar “fazla sürelerle çalışma” sayılır ve %25 zamlı ödenir. Ayrıntılı hesap için <a href="/fazla-mesai-hesaplama.html">fazla mesai hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('Aylık maaş saatlik ücrete nasıl çevrilir?','Aylık brüt maaşı 225’e bölün. 33.030 ₺ brüt asgari ücretin saatlik karşılığı 146,80 ₺’dir.'),
('Günlük ücret nasıl hesaplanır?','Aylık brüt ücret 30’a bölünür. Ayın kaç gün çektiğine bakılmaksızın 30 gün esas alınır.'),
('Fazla mesai ücreti saatlik ücretin kaç katı?','Haftalık 45 saati aşan çalışmalarda saatlik ücretin 1,5 katı ödenir.'),
('Saatlik ücret brüt mü net mi hesaplanır?','Yasal hesaplamalar (fazla mesai, kesintiler) brüt ücret üzerinden yapılır. Net saatlik ücreti görmek için net maaşı aynı saate bölebilirsiniz.'),
],
related=['fazla-mesai-hesaplama','net-maas-hesaplama','asgari-ucret-hesaplama','maas-zam-hesaplama','is-gunu-hesaplama'],
))
