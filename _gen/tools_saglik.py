"""Sağlık hesaplamaları. Not: tüm sağlık sayfalarında tıbbi uyarı ve sağlıklı aralık vurgusu bulunur."""

UYARI = '<div class="info-box" style="margin-top:14px">⚕️ Bu araç genel bilgilendirme amaçlıdır; tıbbi tanı veya tedavi yerine geçmez. Hamilelik, kronik hastalık veya özel beslenme ihtiyacı durumunda hekiminize ya da diyetisyeninize danışın.</div>'
SIDE_VKI = '''<div class="card"><div class="side-title">📊 VKİ Sınıflandırması (DSÖ)</div>
<div class="res-rows" style="font-size:.84rem">
<div class="res-row"><span>18,5 altı</span><b>Zayıf</b></div><div class="res-row"><span>18,5 – 24,9</span><b style="color:var(--success)">Normal</b></div>
<div class="res-row"><span>25 – 29,9</span><b>Fazla kilolu</b></div><div class="res-row"><span>30 – 34,9</span><b>1. derece obez</b></div>
<div class="res-row"><span>35 – 39,9</span><b>2. derece obez</b></div><div class="res-row"><span>40 ve üzeri</span><b>3. derece (morbid) obez</b></div></div></div>'''

CINSIYET = '''<div class="field"><label>Cinsiyet</label><div class="seg"><label><input type="radio" name="cins" value="k" checked>Kadın</label><label><input type="radio" name="cins" value="e">Erkek</label></div></div>'''
AKTIVITE = '''<div class="field full"><label for="akt">Fiziksel Aktivite Düzeyi</label><select id="akt">
<option value="1.2">Hareketsiz (masa başı, egzersiz yok)</option><option value="1.375" selected>Az hareketli (haftada 1–3 gün hafif egzersiz)</option>
<option value="1.55">Orta hareketli (haftada 3–5 gün egzersiz)</option><option value="1.725">Çok hareketli (haftada 6–7 gün yoğun egzersiz)</option>
<option value="1.9">Aşırı hareketli (ağır fiziksel iş / günde 2 antrenman)</option></select></div>'''

TOOLS = []

# ───────────────────────── VKİ ─────────────────────────
TOOLS.append(dict(
slug='vucut-kitle-indeksi', name='Vücut Kitle İndeksi (VKİ) Hesaplama', cat='saglik', ico='⚖️',
title='Vücut Kitle İndeksi Hesaplama (VKİ / BMI) – Boy Kilo Endeksi | Hesaplarsın',
desc='Boy ve kilonuzla vücut kitle indeksinizi (VKİ / BMI) hesaplayın; DSÖ sınıflandırmasına göre durumunuzu ve boyunuza uygun sağlıklı kilo aralığını öğrenin.',
h1='⚖️ Vücut Kitle İndeksi (VKİ) Hesaplama',
lead='Boyunuzu ve kilonuzu girin; boy kilo endeksinizi (BMI), Dünya Sağlık Örgütü sınıflandırmasındaki yerinizi ve boyunuza göre sağlıklı kilo aralığını hemen görün.',
form='''<div class="form-grid">
<div class="field"><label for="boy">Boy (cm)</label><input type="number" id="boy" placeholder="örn: 172" inputmode="decimal"></div>
<div class="field"><label for="kilo">Kilo (kg)</label><input type="number" id="kilo" placeholder="örn: 74" inputmode="decimal"></div>
</div>''' + UYARI,
side=SIDE_VKI,
js=r'''
function hesapla(){
  var b=v('boy'), k=v('kilo'); if(!(b>=100&&b<=250)) return 'Boyunuzu santimetre olarak girin (örn: 172).'; if(!(k>=20&&k<=350)) return 'Kilonuzu kilogram olarak girin.';
  var m=b/100, vki=k/(m*m), alt=18.5*m*m, ust=24.9*m*m;
  var s=vki<18.5?['Zayıf','#3b82f6']:vki<25?['Normal kilolu','#10b981']:vki<30?['Fazla kilolu','#f59e0b']:vki<35?['1. derece obez','#ef4444']:vki<40?['2. derece obez','#dc2626']:['3. derece (morbid) obez','#991b1b'];
  var fark=k<alt?'Sağlıklı aralığın alt sınırına '+num(alt-k,1)+' kg uzaktasınız.':k>ust?'Sağlıklı aralığın üst sınırına '+num(k-ust,1)+' kg uzaktasınız.':'Kilonuz boyunuza göre sağlıklı aralıkta.';
  var pos=Math.max(0,Math.min(100,(vki-15)/(40-15)*100));
  return {main:['Vücut kitle indeksiniz', num(vki,1)], sub:'<b>'+s[0]+'</b> · '+fark,
    rows:[['Sınıflandırma',s[0]],['Boyunuza göre sağlıklı kilo aralığı',num(alt,1)+' – '+num(ust,1)+' kg','hl'],['Boy',num(b,0)+' cm'],['Kilo',num(k,1)+' kg']],
    extra:'<div style="position:relative;height:14px;border-radius:7px;background:linear-gradient(90deg,#3b82f6 0 14%,#10b981 14% 40%,#f59e0b 40% 60%,#ef4444 60% 80%,#991b1b 80%)"><span style="position:absolute;left:calc('+pos+'% - 7px);top:-4px;width:14px;height:22px;border-radius:4px;background:#111;border:2px solid #fff"></span></div><div style="display:flex;justify-content:space-between;font-size:.72rem;color:var(--muted);margin-top:4px"><span>15</span><span>18,5</span><span>25</span><span>30</span><span>35</span><span>40</span></div>',
    note:b&&vki<18.5?'VKİ değeriniz zayıf aralığında. Sağlıklı kilo kazanımı için bir hekim veya diyetisyenle görüşmeniz önerilir.':''};
}''',
article='''
<h2 id="nedir">Vücut kitle indeksi (VKİ) nedir?</h2>
<p>Vücut kitle indeksi (VKİ), İngilizce kısaltmasıyla BMI (Body Mass Index), kilonun boyun karesine bölünmesiyle elde edilen ve bir kişinin boyuna göre zayıf, normal ya da fazla kilolu olup olmadığını gösteren basit bir ölçüttür. Türkiye’de “boy kilo endeksi” veya “beden kitle indeksi” olarak da bilinir. Dünya Sağlık Örgütü (DSÖ) tarafından yetişkinlerde obeziteyi tanımlamak için kullanılır.</p>

<h2 id="nasil">Vücut kitle indeksi nasıl hesaplanır?</h2>
<p>VKİ hesaplamak için kilo (kg), metre cinsinden boyun karesine bölünür. Boyunuz santimetre olarak biliniyorsa önce 100’e bölerek metreye çevirin.</p>
<div class="formula">VKİ = Kilo (kg) ÷ [Boy (m) × Boy (m)]</div>
<div class="example"><p><b>Örnek:</b> 172 cm boyunda ve 74 kg ağırlığındaki biri için:</p><p>1,72 × 1,72 = 2,958 → 74 ÷ 2,958 = <b>25,0</b> (sınırda fazla kilolu)</p></div>

<h2 id="degerler">Boy kilo endeksi değerleri nelerdir?</h2>
<div class="table-wrap"><table><thead><tr><th>VKİ (kg/m²)</th><th>Sınıflandırma</th><th>Sağlık riski</th></tr></thead><tbody>
<tr><td>18,5’in altı</td><td>Zayıf</td><td>Besin eksikliği, kemik erimesi riski</td></tr>
<tr><td>18,5 – 24,9</td><td>Normal kilolu</td><td>En düşük risk</td></tr>
<tr><td>25,0 – 29,9</td><td>Fazla kilolu</td><td>Artmış risk</td></tr>
<tr><td>30,0 – 34,9</td><td>1. derece obezite</td><td>Yüksek risk</td></tr>
<tr><td>35,0 – 39,9</td><td>2. derece obezite</td><td>Çok yüksek risk</td></tr>
<tr><td>40 ve üzeri</td><td>3. derece (morbid) obezite</td><td>Aşırı yüksek risk</td></tr>
</tbody></table></div>

<h2 id="boy-tablosu">Boya göre sağlıklı kilo aralığı tablosu</h2>
<div class="table-wrap"><table><thead><tr><th>Boy</th><th>Sağlıklı kilo aralığı (VKİ 18,5–24,9)</th></tr></thead><tbody>
<tr><td>155 cm</td><td>44,4 – 59,8 kg</td></tr><tr><td>160 cm</td><td>47,4 – 63,7 kg</td></tr><tr><td>165 cm</td><td>50,4 – 67,8 kg</td></tr>
<tr><td>170 cm</td><td>53,5 – 72,0 kg</td></tr><tr><td>175 cm</td><td>56,7 – 76,3 kg</td></tr><tr><td>180 cm</td><td>59,9 – 80,7 kg</td></tr>
<tr><td>185 cm</td><td>63,3 – 85,2 kg</td></tr><tr><td>190 cm</td><td>66,8 – 89,9 kg</td></tr>
</tbody></table></div>

<h2 id="yas-cinsiyet">VKİ yaşa ve cinsiyete göre değişir mi?</h2>
<p>Yetişkinlerde (18 yaş üstü) VKİ sınıflandırması kadın ve erkek için aynıdır. Ancak aynı VKİ değerinde kadınların vücut yağ oranı erkeklere göre genellikle daha yüksektir. 65 yaş üstü bireylerde hafif yüksek VKİ değerleri (yaklaşık 23–28) bazı çalışmalarda daha koruyucu bulunmuştur. <b>Çocuk ve ergenlerde</b> VKİ, yaş ve cinsiyete özel persentil eğrileriyle değerlendirilir; bu hesaplayıcı 18 yaş altı için uygun değildir.</p>

<h2 id="sinirlar">VKİ tek başına yeterli mi?</h2>
<p>VKİ kas ile yağı birbirinden ayırt etmez. Bu nedenle kas kütlesi yüksek sporcular “fazla kilolu” görünebilirken, kas kütlesi düşük kişiler normal VKİ’ye rağmen yüksek yağ oranına sahip olabilir. Daha doğru bir değerlendirme için VKİ’yi bel çevresi, <a href="/bel-kalca-orani-hesaplama.html">bel-kalça oranı</a> ve <a href="/vucut-yag-orani-hesaplama.html">vücut yağ oranı</a> ölçümleriyle birlikte yorumlamak gerekir. Erkeklerde 94 cm, kadınlarda 80 cm üzerindeki bel çevresi artmış riski gösterir.</p>
<p>Boyunuza göre hedeflemeniz gereken kiloyu farklı formüllerle görmek için <a href="/ideal-kilo-hesaplama.html">ideal kilo hesaplama</a> aracını kullanabilirsiniz.</p>
''',
faq=[
('Boy kilo endeksi ile vücut kitle indeksi aynı şey mi?','Evet. Boy kilo endeksi (BKİ), beden kitle indeksi ve vücut kitle indeksi (VKİ) aynı ölçümü ifade eder; İngilizcesi BMI’dır.'),
('İdeal vücut kitle indeksi kaç olmalı?','Yetişkinler için sağlıklı aralık 18,5 ile 24,9 arasıdır. Bu aralıktaki değerler kiloya bağlı hastalık riskinin en düşük olduğu bölgeyi gösterir.'),
('VKİ 25 fazla kilolu mu?','Evet, 25,0 ve üzeri DSÖ sınıflandırmasında fazla kilolu kabul edilir. Ancak kas kütlesi yüksek kişilerde bel çevresi ile birlikte değerlendirilmelidir.'),
('Kadınlar için ideal VKİ farklı mı?','Hayır, yetişkin kadın ve erkekler için aynı aralıklar kullanılır. Hamilelikte VKİ hesaplaması anlamlı değildir; gebelik öncesi kilo esas alınır.'),
('Çocuklarda VKİ nasıl değerlendirilir?','2–18 yaş arasında VKİ yaş ve cinsiyete göre persentil eğrileriyle yorumlanır. Çocuğunuzun durumunu çocuk doktorunuzla değerlendirmeniz önerilir.'),
],
related=['ideal-kilo-hesaplama','vucut-yag-orani-hesaplama','bel-kalca-orani-hesaplama','gunluk-kalori-ihtiyaci-hesaplama','bazal-metabolizma-hesaplama','su-ihtiyaci-hesaplama'],
sources=[('Dünya Sağlık Örgütü – Obezite','https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight'),('T.C. Sağlık Bakanlığı','https://hsgm.saglik.gov.tr/tr/obezite/')],
howto=('Vücut kitle indeksi nasıl hesaplanır?',['Boyunuzu santimetre olarak girin.','Kilonuzu kilogram olarak girin.','Hesapla’ya basın; VKİ değeriniz ve sınıflandırmanız gösterilir.']),
))

# ───────────────────────── İDEAL KİLO ─────────────────────────
TOOLS.append(dict(
slug='ideal-kilo-hesaplama', name='İdeal Kilo Hesaplama', cat='saglik', ico='🎯',
title='İdeal Kilo Hesaplama – Boyuma Göre Kaç Kilo Olmalıyım? | Hesaplarsın',
desc='Boy, cinsiyet ve yaşınıza göre ideal kilonuzu Devine, Robinson, Miller ve Hamwi formülleriyle hesaplayın. Sağlıklı kilo aralığınızı (VKİ 18,5–24,9) da öğrenin.',
h1='🎯 İdeal Kilo Hesaplama',
lead='Boyunuza ve cinsiyetinize göre ideal kilonuzu dört farklı bilimsel formülle hesaplayın; sağlıklı kilo aralığınızı ve mevcut kilonuzla farkı görün.',
form='''<div class="form-grid">''' + CINSIYET + '''
<div class="field"><label for="boy">Boy (cm)</label><input type="number" id="boy" placeholder="örn: 168" inputmode="decimal"></div>
<div class="field"><label for="kilo">Mevcut Kilo (kg) <small>isteğe bağlı</small></label><input type="number" id="kilo" placeholder="örn: 70" inputmode="decimal"></div>
</div>''' + UYARI,
side=SIDE_VKI,
js=r'''
function hesapla(){
  var b=v('boy'), k=v('kilo'), e=radio('cins')==='e'; if(!(b>=130&&b<=230)) return 'Boyunuzu 130–230 cm arasında girin.';
  var inc=b/2.54, d=inc-60;
  var f={Devine:e?50+2.3*d:45.5+2.3*d, Robinson:e?52+1.9*d:49+1.7*d, Miller:e?56.2+1.41*d:53.1+1.36*d, Hamwi:e?48+2.7*d:45.5+2.2*d};
  var vals=Object.keys(f).map(function(x){return f[x];}), ort=vals.reduce(function(t,x){return t+x;},0)/4;
  var m=b/100, alt=18.5*m*m, ust=24.9*m*m;
  var rows=Object.keys(f).map(function(x){return [x+' formülü',num(f[x],1)+' kg'];});
  rows.push(['Sağlıklı kilo aralığı (VKİ)',num(alt,1)+' – '+num(ust,1)+' kg','hl']);
  if(k>0){var vki=k/(m*m); rows.push(['Mevcut VKİ',num(vki,1)]); rows.push(['Formül ortalamasına fark',(k>ort?'+':'')+num(k-ort,1)+' kg']);}
  return {main:['İdeal kilonuz (formül ortalaması)', num(ort,1)+' kg'], sub:'Sağlıklı aralık: '+num(alt,1)+' – '+num(ust,1)+' kg', rows:rows,
    note:b<152?'Formüller 152 cm (5 feet) altındaki boylar için daha az güvenilirdir; VKİ aralığını esas alın.':''};
}''',
article='''
<h2 id="nedir">İdeal kilo nedir?</h2>
<p>İdeal kilo, bir kişinin boyuna, cinsiyetine ve vücut yapısına göre sağlık açısından en düşük risk taşıdığı kabul edilen ağırlıktır. Tek bir “doğru” rakam değil, bir aralıktır. Bu araç hem tıpta yaygın kullanılan dört formülün sonuçlarını hem de Dünya Sağlık Örgütü’nün vücut kitle indeksine dayalı <b>sağlıklı kilo aralığını</b> birlikte gösterir.</p>

<h2 id="formuller">İdeal kilo hesaplama formülleri</h2>
<p>Formüllerde boy inç cinsinden kullanılır (1 inç = 2,54 cm). 152,4 cm (60 inç) temel boy kabul edilir ve bu boyun üzerindeki her inç için belirli bir kilo eklenir.</p>
<div class="table-wrap"><table><thead><tr><th>Formül</th><th>Erkek</th><th>Kadın</th></tr></thead><tbody>
<tr><td>Devine (1974)</td><td>50 + 2,3 × (inç − 60)</td><td>45,5 + 2,3 × (inç − 60)</td></tr>
<tr><td>Robinson (1983)</td><td>52 + 1,9 × (inç − 60)</td><td>49 + 1,7 × (inç − 60)</td></tr>
<tr><td>Miller (1983)</td><td>56,2 + 1,41 × (inç − 60)</td><td>53,1 + 1,36 × (inç − 60)</td></tr>
<tr><td>Hamwi (1964)</td><td>48 + 2,7 × (inç − 60)</td><td>45,5 + 2,2 × (inç − 60)</td></tr>
</tbody></table></div>
<div class="example"><p><b>Örnek:</b> 168 cm boyunda bir kadın: 168 ÷ 2,54 = 66,1 inç → 66,1 − 60 = 6,1</p>
<p>Devine: 45,5 + 2,3 × 6,1 = <b>59,6 kg</b> · Robinson: 49 + 1,7 × 6,1 = <b>59,4 kg</b></p></div>
<p>Devine formülü ilaç dozu hesaplarında da kullanıldığı için tıpta en yaygın olanıdır. Hamwi formülü daha yüksek, Miller formülü ise kısa boylularda daha yüksek sonuç verir.</p>

<h2 id="tablo">Boya göre ideal kilo tablosu</h2>
<div class="table-wrap"><table><thead><tr><th>Boy</th><th>Kadın (Devine)</th><th>Erkek (Devine)</th><th>Sağlıklı aralık</th></tr></thead><tbody>
<tr><td>155 cm</td><td>47,8 kg</td><td>52,3 kg</td><td>44,4 – 59,8 kg</td></tr>
<tr><td>160 cm</td><td>52,4 kg</td><td>56,9 kg</td><td>47,4 – 63,7 kg</td></tr>
<tr><td>165 cm</td><td>56,9 kg</td><td>61,4 kg</td><td>50,4 – 67,8 kg</td></tr>
<tr><td>170 cm</td><td>61,4 kg</td><td>65,9 kg</td><td>53,5 – 72,0 kg</td></tr>
<tr><td>175 cm</td><td>65,9 kg</td><td>70,5 kg</td><td>56,7 – 76,3 kg</td></tr>
<tr><td>180 cm</td><td>70,5 kg</td><td>75,0 kg</td><td>59,9 – 80,7 kg</td></tr>
<tr><td>185 cm</td><td>75,0 kg</td><td>79,5 kg</td><td>63,3 – 85,2 kg</td></tr>
</tbody></table></div>

<h2 id="yas">Yaşa göre ideal kilo değişir mi?</h2>
<p>Klasik formüller yaşı dikkate almaz. Yaş ilerledikçe kas kütlesi azalıp yağ oranı arttığı için aynı kilo farklı bir vücut kompozisyonunu temsil edebilir. Bu nedenle 50 yaş sonrasında kilodan çok bel çevresi, kas gücü ve <a href="/vucut-yag-orani-hesaplama.html">vücut yağ oranı</a> takibi önem kazanır. Yaşlılarda sağlıklı aralığın üst bölümünde olmak genellikle sakınca yaratmaz.</p>

<h2 id="ulasmak">İdeal kiloya nasıl ulaşılır?</h2>
<ul>
<li>Haftada 0,5–1 kg’dan hızlı kilo kaybını hedeflemeyin; hızlı kilo kaybı kas kaybına ve geri alıma yol açar.</li>
<li>Günlük enerji ihtiyacınızı <a href="/gunluk-kalori-ihtiyaci-hesaplama.html">günlük kalori ihtiyacı</a> aracıyla öğrenin ve ihtiyacın çok altına inmeyin.</li>
<li>Yeterli protein alın (<a href="/protein-ihtiyaci-hesaplama.html">protein ihtiyacı hesaplama</a>) ve haftada en az 150 dakika orta yoğunlukta egzersiz yapın.</li>
<li>Uyku düzeni ve su tüketimi kilo yönetiminde göz ardı edilmemelidir.</li>
</ul>
''',
faq=[
('Boyuma göre kaç kilo olmalıyım?','Sağlıklı kilo aralığınız boyunuzun (metre) karesinin 18,5 ve 24,9 ile çarpılmasıyla bulunur. Örneğin 170 cm için 53,5–72 kg arası sağlıklı kabul edilir.'),
('İdeal kilo formülleri neden farklı sonuç veriyor?','Her formül farklı dönemde, farklı bir veri setinden türetilmiştir. Sonuçlar birkaç kilo farklılık gösterebilir; bu yüzden tek bir değer yerine ortalama ve aralık kullanmak daha doğrudur.'),
('Kadınlar için ideal kilo nasıl hesaplanır?','Kadın formüllerinde başlangıç değeri daha düşüktür. Devine’a göre: 45,5 + 2,3 × (inç cinsinden boy − 60).'),
('İdeal kilo ile sağlıklı kilo aynı mı?','Tam olarak değil. İdeal kilo formüllerin verdiği tek bir değerdir; sağlıklı kilo ise VKİ’ye göre daha geniş bir aralıktır. Bu aralıkta olmak çoğu kişi için yeterlidir.'),
('Kas kütlem yüksekse ideal kilo formülleri geçerli mi?','Formüller vücut kompozisyonunu dikkate almaz. Kas kütlesi yüksek kişilerde vücut yağ oranı ve bel çevresi daha anlamlı ölçütlerdir.'),
],
related=['vucut-kitle-indeksi','vucut-yag-orani-hesaplama','gunluk-kalori-ihtiyaci-hesaplama','hedef-kilo-suresi-hesaplama','bel-kalca-orani-hesaplama'],
sources=[('Dünya Sağlık Örgütü – VKİ sınıflandırması','https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight')],
))

# ───────────────────────── GÜNLÜK KALORİ ─────────────────────────
TOOLS.append(dict(
slug='gunluk-kalori-ihtiyaci-hesaplama', name='Günlük Kalori İhtiyacı Hesaplama', cat='saglik', ico='🥗',
title='Günlük Kalori İhtiyacı Hesaplama – Günde Kaç Kalori Almalıyım? | Hesaplarsın',
desc='Yaş, boy, kilo, cinsiyet ve aktivite düzeyinize göre günlük kalori ihtiyacınızı Mifflin-St Jeor formülüyle hesaplayın. Kilo korumak, vermek ve almak için öneriler.',
h1='🥗 Günlük Kalori İhtiyacı Hesaplama',
lead='Bazal metabolizma hızınızı ve aktivite düzeyinizi hesaba katarak kilonuzu korumak için günde kaç kalori almanız gerektiğini öğrenin.',
form='''<div class="form-grid">''' + CINSIYET + '''
<div class="field"><label for="yas">Yaş</label><input type="number" id="yas" placeholder="örn: 30" inputmode="numeric"></div>
<div class="field"><label for="boy">Boy (cm)</label><input type="number" id="boy" placeholder="örn: 175" inputmode="decimal"></div>
<div class="field"><label for="kilo">Kilo (kg)</label><input type="number" id="kilo" placeholder="örn: 75" inputmode="decimal"></div>
''' + AKTIVITE + '''</div>''' + UYARI,
js=r'''
function hesapla(){
  var y=v('yas'), b=v('boy'), k=v('kilo'), e=radio('cins')==='e', a=parseFloat(el('akt').value);
  if(!(y>=18&&y<=100)) return 'Bu hesaplama 18 yaş ve üzeri yetişkinler içindir.'; if(!(b>=130&&b<=230)||!(k>=35&&k<=300)) return 'Boy ve kilonuzu kontrol edin.';
  var bmr=10*k+6.25*b-5*y+(e?5:-161), tdee=bmr*a, taban=e?1500:1200;
  var ver=Math.max(tdee-500,taban), al=tdee+300;
  return {main:['Kilonuzu korumak için', num(tdee,0)+' kcal / gün'], sub:'Bazal metabolizma hızınız: '+num(bmr,0)+' kcal',
    rows:[['Kilo korumak',num(tdee,0)+' kcal'],['Sağlıklı kilo vermek (~0,5 kg/hafta)',num(ver,0)+' kcal'],['Kilo almak (~0,25–0,5 kg/hafta)',num(al,0)+' kcal'],
      ['Önerilen günlük protein',num(k*0.8,0)+' – '+num(k*1.2,0)+' g'],['Önerilen günlük su',num(k*0.033,1)+' litre']],
    note:'Kalori alımının kadınlarda 1.200, erkeklerde 1.500 kcal’nin altına düşmesi uzman gözetimi olmadan önerilmez.'};
}''',
article='''
<h2 id="nedir">Günlük kalori ihtiyacı nedir?</h2>
<p>Günlük kalori ihtiyacı, vücudunuzun bir günde harcadığı toplam enerji miktarıdır (TDEE – Total Daily Energy Expenditure). Bu miktar üç bileşenden oluşur: dinlenme halinde yaşamsal fonksiyonlar için harcanan <b>bazal metabolizma</b> (%60–70), sindirim için harcanan enerji (%10) ve günlük hareket ile egzersiz (%20–30). Bu kadar kalori aldığınızda kilonuz sabit kalır.</p>

<h2 id="nasil">Günlük kalori ihtiyacı nasıl hesaplanır?</h2>
<p>Hesaplayıcı, Amerikan Diyetisyenler Derneği’nin de önerdiği <b>Mifflin-St Jeor</b> denklemiyle önce bazal metabolizma hızını (BMH) bulur, ardından aktivite katsayısıyla çarpar.</p>
<div class="formula">Erkek BMH = 10 × kilo + 6,25 × boy − 5 × yaş + 5<br>Kadın BMH = 10 × kilo + 6,25 × boy − 5 × yaş − 161<br>Günlük ihtiyaç = BMH × Aktivite katsayısı</div>
<div class="example"><p><b>Örnek:</b> 30 yaşında, 175 cm, 75 kg, haftada 1–3 gün spor yapan bir erkek:</p>
<p>BMH = 750 + 1.093,75 − 150 + 5 = 1.698,75 kcal → 1.698,75 × 1,375 = <b>2.336 kcal/gün</b></p></div>

<h2 id="aktivite">Aktivite katsayıları</h2>
<div class="table-wrap"><table><thead><tr><th>Aktivite düzeyi</th><th>Katsayı</th><th>Örnek</th></tr></thead><tbody>
<tr><td>Hareketsiz</td><td>1,2</td><td>Masa başı iş, düzenli egzersiz yok</td></tr>
<tr><td>Az hareketli</td><td>1,375</td><td>Haftada 1–3 gün hafif egzersiz</td></tr>
<tr><td>Orta hareketli</td><td>1,55</td><td>Haftada 3–5 gün orta yoğunlukta spor</td></tr>
<tr><td>Çok hareketli</td><td>1,725</td><td>Haftada 6–7 gün yoğun antrenman</td></tr>
<tr><td>Aşırı hareketli</td><td>1,9</td><td>Ağır bedensel iş, profesyonel sporcu</td></tr>
</tbody></table></div>

<h2 id="kilo-verme">Kilo vermek için kaç kalori almalıyım?</h2>
<p>Yaklaşık 7.700 kcal’lik enerji açığı 1 kg yağ kaybına karşılık gelir. Günlük ihtiyacınızdan 500 kcal eksik almak haftada yaklaşık 0,5 kg kayıp sağlar. Daha büyük açıklar kas kaybına, yorgunluğa ve metabolizmanın yavaşlamasına neden olabilir. Hedef kilonuza ne kadar sürede ulaşacağınızı <a href="/hedef-kilo-suresi-hesaplama.html">hedef kilo süresi hesaplama</a> aracıyla görebilirsiniz.</p>

<h2 id="ortalama">Kadın ve erkek ortalama kalori ihtiyacı</h2>
<div class="table-wrap"><table><thead><tr><th>Yaş grubu</th><th>Kadın (orta aktif)</th><th>Erkek (orta aktif)</th></tr></thead><tbody>
<tr><td>19–30</td><td>2.000 – 2.200 kcal</td><td>2.600 – 2.800 kcal</td></tr>
<tr><td>31–50</td><td>1.800 – 2.000 kcal</td><td>2.400 – 2.600 kcal</td></tr>
<tr><td>51 ve üzeri</td><td>1.600 – 1.800 kcal</td><td>2.200 – 2.400 kcal</td></tr>
</tbody></table></div>
<p>Kalori kadar kalorinin kaynağı da önemlidir: tabağın yarısını sebze-meyve, dörtte birini tam tahıl, dörtte birini protein kaynağı oluşturmalıdır. Spor sırasında harcadığınız enerjiyi <a href="/kalori-yakma-hesaplama.html">kalori yakma hesaplama</a> ile öğrenebilirsiniz.</p>
''',
faq=[
('Günde kaç kalori almalıyım?','Yaş, cinsiyet, kilo, boy ve aktivite düzeyinize bağlıdır. Ortalama yetişkin kadınlar 1.800–2.200, erkekler 2.200–2.800 kcal’ye ihtiyaç duyar. Kişisel değeriniz için hesaplayıcıyı kullanın.'),
('Bazal metabolizma ile günlük kalori ihtiyacı arasındaki fark nedir?','Bazal metabolizma tam dinlenme halinde harcanan enerjidir. Günlük kalori ihtiyacı ise buna günlük hareket ve egzersizi de ekler.'),
('Kilo vermek için kalori ne kadar azaltılmalı?','Genellikle günlük ihtiyaçtan 300–500 kcal eksik almak önerilir. Bu, haftada yaklaşık 0,25–0,5 kg sağlıklı kilo kaybı sağlar.'),
('Mifflin-St Jeor formülü ne kadar doğru?','Sağlıklı yetişkinlerde gerçek ölçümlere en yakın sonucu veren formüllerden biridir; yine de bireysel farklılıklar ±%10 olabilir.'),
],
related=['bazal-metabolizma-hesaplama','kalori-yakma-hesaplama','protein-ihtiyaci-hesaplama','hedef-kilo-suresi-hesaplama','vucut-kitle-indeksi','su-ihtiyaci-hesaplama'],
sources=[('Mifflin MD ve ark., Am J Clin Nutr 1990','https://pubmed.ncbi.nlm.nih.gov/2305711/'),('Türkiye Beslenme Rehberi (TÜBER) 2022','https://hsgm.saglik.gov.tr/tr/web-uygulamalarimiz/357.html')],
))

# ───────────────────────── KALORİ YAKMA ─────────────────────────
TOOLS.append(dict(
slug='kalori-yakma-hesaplama', name='Kalori Yakma Hesaplama', cat='saglik', ico='🏃',
title='Kalori Yakma Hesaplama – Yürüyüş, Koşu, Bisiklet Kaç Kalori? | Hesaplarsın',
desc='Kilonuza ve egzersiz sürenize göre yürüyüş, koşu, bisiklet, yüzme, fitness ve daha fazla aktivitede kaç kalori yaktığınızı MET değerleriyle hesaplayın.',
h1='🏃 Kalori Yakma Hesaplama',
lead='Yaptığınız aktiviteyi, sürenizi ve kilonuzu seçin; egzersiz sırasında kaç kalori yaktığınızı bilimsel MET değerleriyle hesaplayın.',
form='''<div class="form-grid">
<div class="field full"><label for="akt">Aktivite</label><select id="akt">
<optgroup label="Yürüyüş"><option value="3.0">Yavaş yürüyüş (4 km/s)</option><option value="3.5" selected>Normal yürüyüş (5 km/s)</option><option value="4.3">Tempolu yürüyüş (6 km/s)</option><option value="6.0">Yokuş yukarı yürüyüş</option></optgroup>
<optgroup label="Koşu"><option value="8.3">Koşu (8 km/s)</option><option value="9.8">Koşu (10 km/s)</option><option value="11.0">Koşu (11 km/s)</option><option value="11.8">Koşu (12 km/s)</option></optgroup>
<optgroup label="Bisiklet"><option value="4.0">Bisiklet – yavaş (16 km/s altı)</option><option value="8.0">Bisiklet – orta (19–22 km/s)</option><option value="6.8">Kondisyon bisikleti – orta</option></optgroup>
<optgroup label="Spor salonu"><option value="5.0">Ağırlık antrenmanı – orta</option><option value="6.0">Ağırlık antrenmanı – yoğun</option><option value="8.0">HIIT / devre antrenmanı</option><option value="5.0">Eliptik bisiklet – orta</option><option value="3.0">Pilates</option><option value="2.5">Yoga (hatha)</option></optgroup>
<optgroup label="Spor"><option value="7.0">Futbol (amatör)</option><option value="6.5">Basketbol</option><option value="7.3">Tenis</option><option value="5.8">Yüzme – serbest, yavaş</option><option value="9.8">Yüzme – serbest, hızlı</option><option value="11.8">İp atlama</option><option value="5.0">Dans (aerobik)</option></optgroup>
<optgroup label="Günlük işler"><option value="3.3">Ev temizliği</option><option value="4.0">Merdiven çıkma (yavaş)</option><option value="3.5">Bahçe işleri</option></optgroup>
</select></div>
<div class="field"><label for="kilo">Kilo (kg)</label><input type="number" id="kilo" placeholder="örn: 70" inputmode="decimal"></div>
<div class="field"><label for="sure">Süre (dakika)</label><input type="number" id="sure" placeholder="örn: 45" inputmode="numeric"></div>
</div>''',
js=r'''
function hesapla(){
  var met=parseFloat(el('akt').value), k=v('kilo'), d=v('sure'); if(!(k>=30&&k<=300)) return 'Kilonuzu girin.'; if(!(d>0&&d<=600)) return 'Süreyi dakika olarak girin.';
  var kcal=met*3.5*k/200*d, ad=el('akt').options[el('akt').selectedIndex].text;
  return {main:['Yakılan kalori', num(kcal,0)+' kcal'], sub:ad+' · '+num(d,0)+' dakika',
    rows:[['Dakikada yakılan',num(kcal/d,1)+' kcal'],['Saatlik tempo',num(kcal/d*60,0)+' kcal'],['MET değeri',num(met,1)],['Yağ karşılığı (yaklaşık)',num(kcal/7.7,0)+' g'],
      ['Eşdeğer: 1 dilim ekmek (~70 kcal)',num(kcal/70,1)+' dilim'],['Eşdeğer: 1 kutu kola (~140 kcal)',num(kcal/140,1)+' kutu']]};
}''',
article='''
<h2 id="nasil">Egzersizde yakılan kalori nasıl hesaplanır?</h2>
<p>Fiziksel aktivitelerde harcanan enerji, <b>MET</b> (metabolik eşdeğer) değeriyle hesaplanır. 1 MET, oturur haldeyken harcanan enerjiyi ifade eder ve kilogram başına dakikada yaklaşık 3,5 ml oksijen tüketimine karşılık gelir. Bir aktivitenin MET değeri, o aktivitenin dinlenmeye göre kaç kat enerji harcattığını gösterir. MET değerleri, bilimsel çalışmalarda kullanılan <i>Compendium of Physical Activities</i> kaynağından alınmıştır.</p>
<div class="formula">Yakılan kalori = MET × 3,5 × Kilo (kg) ÷ 200 × Süre (dk)</div>
<div class="example"><p><b>Örnek:</b> 70 kg ağırlığındaki biri 45 dakika normal tempoda (5 km/s) yürürse:</p><p>3,5 × 3,5 × 70 ÷ 200 × 45 = <b>193 kcal</b></p></div>

<h2 id="tablo">Aktivitelere göre yakılan kalori tablosu (70 kg, 30 dakika)</h2>
<div class="table-wrap"><table><thead><tr><th>Aktivite</th><th>MET</th><th>30 dakikada</th></tr></thead><tbody>
<tr><td>Yoga</td><td>2,5</td><td>~92 kcal</td></tr><tr><td>Normal yürüyüş (5 km/s)</td><td>3,5</td><td>~129 kcal</td></tr><tr><td>Tempolu yürüyüş (6 km/s)</td><td>4,3</td><td>~158 kcal</td></tr>
<tr><td>Ağırlık antrenmanı (orta)</td><td>5,0</td><td>~184 kcal</td></tr><tr><td>Yüzme (yavaş)</td><td>5,8</td><td>~213 kcal</td></tr><tr><td>Bisiklet (orta)</td><td>8,0</td><td>~294 kcal</td></tr>
<tr><td>Koşu (10 km/s)</td><td>9,8</td><td>~360 kcal</td></tr><tr><td>İp atlama</td><td>11,8</td><td>~434 kcal</td></tr>
</tbody></table></div>

<h2 id="kilo">Kilo, yakılan kaloriyi nasıl etkiler?</h2>
<p>Aynı aktiviteyi yapan daha ağır bir kişi, vücudunu hareket ettirmek için daha fazla enerji harcar. Bu yüzden 90 kg’lık biri 30 dakikalık koşuda 60 kg’lık birinden yaklaşık %50 daha fazla kalori yakar. Kondisyon arttıkça vücut aynı işi daha verimli yaptığı için aynı aktivitede harcanan kalori bir miktar azalabilir.</p>

<h2 id="adim">10.000 adım kaç kalori yakar?</h2>
<p>Ortalama adım uzunluğu 70–80 cm kabul edildiğinde 10.000 adım yaklaşık 7–8 km yürüyüşe karşılık gelir. 70 kg’lık bir yetişkin bu mesafeyi normal tempoda yaklaşık 90 dakikada yürür ve <b>350–400 kcal</b> harcar.</p>

<h2 id="ipuclari">Daha fazla kalori yakmak için ipuçları</h2>
<ul>
<li>Haftada en az 150 dakika orta veya 75 dakika yüksek yoğunlukta aerobik egzersiz yapın (DSÖ önerisi).</li>
<li>Kas kütlesini artıran ağırlık antrenmanları dinlenme halindeki enerji harcamasını da yükseltir; bkz. <a href="/bazal-metabolizma-hesaplama.html">bazal metabolizma hesaplama</a>.</li>
<li>Günlük hareketi artırın: asansör yerine merdiven, kısa mesafelerde yürüyüş.</li>
<li>Egzersizle harcadığınız kaloriyi <a href="/gunluk-kalori-ihtiyaci-hesaplama.html">günlük kalori ihtiyacınızla</a> birlikte değerlendirin.</li>
</ul>
''',
faq=[
('1 saat yürüyüş kaç kalori yakar?','70 kg’lık bir kişi normal tempoda (5 km/s) 1 saat yürüyüşte yaklaşık 257 kcal, tempolu yürüyüşte (6 km/s) yaklaşık 316 kcal yakar.'),
('30 dakika koşu kaç kalori yakar?','10 km/s hızla koşan 70 kg’lık bir kişi 30 dakikada yaklaşık 360 kcal yakar.'),
('1 kilo yağ yakmak için kaç kalori harcamak gerekir?','Yaklaşık 7.700 kcal enerji açığı 1 kg yağ kaybına karşılık gelir.'),
('Akıllı saatlerin kalori ölçümü doğru mu?','Akıllı saatler nabız ve hareket verisiyle tahmin yapar; özellikle ağırlık antrenmanlarında %20–40 sapma görülebilir. MET hesaplaması da bir tahmindir.'),
],
related=['gunluk-kalori-ihtiyaci-hesaplama','bazal-metabolizma-hesaplama','hedef-kilo-suresi-hesaplama','vucut-kitle-indeksi','su-ihtiyaci-hesaplama'],
sources=[('Compendium of Physical Activities','https://pacompendium.com/'),('DSÖ Fiziksel Aktivite Önerileri','https://www.who.int/news-room/fact-sheets/detail/physical-activity')],
))

# ───────────────────────── PROTEİN ─────────────────────────
TOOLS.append(dict(
slug='protein-ihtiyaci-hesaplama', name='Protein İhtiyacı Hesaplama', cat='saglik', ico='🥩',
title='Günlük Protein İhtiyacı Hesaplama – Kaç Gram Protein Almalıyım? | Hesaplarsın',
desc='Kilonuza, aktivite düzeyinize ve hedefinize (kas yapma, kilo verme, koruma) göre günlük protein ihtiyacınızı gram olarak hesaplayın. Öğün başı dağılım dahil.',
h1='🥩 Günlük Protein İhtiyacı Hesaplama',
lead='Kilonuzu, hareket düzeyinizi ve hedefinizi seçin; günde kaç gram protein almanız gerektiğini ve bunu öğünlere nasıl dağıtabileceğinizi görün.',
form='''<div class="form-grid">
<div class="field"><label for="kilo">Kilo (kg)</label><input type="number" id="kilo" placeholder="örn: 70" inputmode="decimal"></div>
<div class="field"><label for="ogun">Günlük Öğün Sayısı</label><select id="ogun"><option>3</option><option selected>4</option><option>5</option></select></div>
<div class="field full"><label for="hedef">Durum / Hedef</label><select id="hedef">
<option value="0.8|1.0">Hareketsiz yetişkin (genel sağlık)</option>
<option value="1.0|1.2" selected>Düzenli hafif egzersiz yapan</option>
<option value="1.2|1.6">Dayanıklılık sporcusu (koşu, bisiklet)</option>
<option value="1.6|2.2">Kas kazanımı (ağırlık antrenmanı)</option>
<option value="1.2|1.6">Kilo verme sürecinde (kas korumak için)</option>
<option value="1.0|1.2">65 yaş üstü</option>
</select></div></div>''' + UYARI,
js=r'''
function hesapla(){
  var k=v('kilo'); if(!(k>=30&&k<=300)) return 'Kilonuzu girin.';
  var r=el('hedef').value.split('|').map(parseFloat), lo=k*r[0], hi=k*r[1], o=parseInt(el('ogun').value), mid=(lo+hi)/2;
  return {main:['Günlük protein ihtiyacınız', num(lo,0)+' – '+num(hi,0)+' g'], sub:'Kilogram başına '+num(r[0],1)+' – '+num(r[1],1)+' g',
    rows:[['Öğün başına ('+o+' öğün)',num(lo/o,0)+' – '+num(hi/o,0)+' g'],['Proteinden gelen enerji',num(lo*4,0)+' – '+num(hi*4,0)+' kcal'],
      ['Örnek: tavuk göğsü (100 g ≈ 31 g protein)',num(mid/31*100,0)+' g’a eşdeğer'],['Örnek: yumurta (1 adet ≈ 6 g)',num(mid/6,0)+' adete eşdeğer']],
    note:'Böbrek hastalığı olanlarda protein alımı hekim kontrolünde belirlenmelidir.'};
}''',
article='''
<h2 id="ne-kadar">Günde ne kadar protein almalıyım?</h2>
<p>Sağlıklı ve hareketsiz bir yetişkinin günlük protein ihtiyacı, Dünya Sağlık Örgütü ve Türkiye Beslenme Rehberi’ne göre <b>kilogram başına 0,8 gram</b>dır. Düzenli spor yapanlarda, kas kazanmak isteyenlerde, kilo verme sürecinde olanlarda ve yaşlılarda bu ihtiyaç artar.</p>
<div class="formula">Günlük protein (g) = Vücut ağırlığı (kg) × Katsayı (g/kg)</div>
<div class="example"><p><b>Örnek:</b> Ağırlık antrenmanı yapan 70 kg’lık biri için: 70 × 1,6 = 112 g ile 70 × 2,2 = 154 g arası. Günde 4 öğünle öğün başına yaklaşık <b>28–38 g</b> protein.</p></div>

<h2 id="tablo">Duruma göre protein ihtiyacı</h2>
<div class="table-wrap"><table><thead><tr><th>Durum</th><th>g / kg / gün</th><th>70 kg için</th></tr></thead><tbody>
<tr><td>Hareketsiz yetişkin</td><td>0,8 – 1,0</td><td>56 – 70 g</td></tr>
<tr><td>Düzenli hafif egzersiz</td><td>1,0 – 1,2</td><td>70 – 84 g</td></tr>
<tr><td>Dayanıklılık sporcusu</td><td>1,2 – 1,6</td><td>84 – 112 g</td></tr>
<tr><td>Kas kazanımı</td><td>1,6 – 2,2</td><td>112 – 154 g</td></tr>
<tr><td>65 yaş üstü</td><td>1,0 – 1,2</td><td>70 – 84 g</td></tr>
</tbody></table></div>

<h2 id="kaynaklar">Protein kaynakları ve miktarları</h2>
<div class="table-wrap"><table><thead><tr><th>Besin (100 g)</th><th>Protein</th></tr></thead><tbody>
<tr><td>Tavuk göğsü (pişmiş)</td><td>~31 g</td></tr><tr><td>Ton balığı (konserve, süzülmüş)</td><td>~26 g</td></tr><tr><td>Dana kıyma (az yağlı, pişmiş)</td><td>~26 g</td></tr>
<tr><td>Beyaz peynir</td><td>~17 g</td></tr><tr><td>Mercimek (pişmiş)</td><td>~9 g</td></tr><tr><td>Nohut (pişmiş)</td><td>~9 g</td></tr>
<tr><td>Yoğurt (süzme)</td><td>~10 g</td></tr><tr><td>Yumurta (1 adet, ~50 g)</td><td>~6 g</td></tr><tr><td>Badem</td><td>~21 g</td></tr>
</tbody></table></div>
<p>Hayvansal kaynaklar tüm temel amino asitleri içerir. Bitkisel beslenenler baklagilleri tahıllarla (örneğin mercimek + bulgur) birleştirerek protein kalitesini artırabilir.</p>

<h2 id="dagitim">Protein öğünlere nasıl dağıtılmalı?</h2>
<p>Araştırmalar, kas protein sentezi için proteinin gün içine yayılmasının tek öğünde alınmasından daha etkili olduğunu göstermektedir. Her ana öğünde 20–40 g protein hedeflemek pratik bir yaklaşımdır. Egzersiz sonrası 2 saat içinde protein içeren bir öğün almak toparlanmayı destekler.</p>

<h2 id="fazlasi">Fazla protein zararlı mı?</h2>
<p>Sağlıklı bireylerde 2 g/kg’a kadar protein alımının güvenli olduğu kabul edilir. Ancak böbrek hastalığı olanlar protein alımını mutlaka hekimleriyle belirlemelidir. Protein ağırlıklı beslenirken yeterli su içmeyi unutmayın; günlük ihtiyacınızı <a href="/su-ihtiyaci-hesaplama.html">su ihtiyacı hesaplama</a> ile öğrenebilirsiniz.</p>
''',
faq=[
('Kas yapmak için günde kaç gram protein almalıyım?','Ağırlık antrenmanı yapanlar için kilogram başına 1,6–2,2 g önerilir. 75 kg’lık biri için bu günde 120–165 g’a karşılık gelir.'),
('Kilo verirken protein ihtiyacı artar mı?','Evet. Kalori açığında kas kaybını önlemek için kilogram başına 1,2–1,6 g protein alınması önerilir.'),
('Tek öğünde ne kadar protein emilir?','Vücut aldığınız proteinin tamamını sindirir; ancak kas yapımı açısından öğün başına 20–40 g en verimli aralık kabul edilir.'),
('Protein tozu gerekli mi?','Gerekli değildir. Günlük ihtiyaç besinlerden karşılanabiliyorsa takviye şart değildir; yalnızca pratiklik sağlar.'),
],
related=['gunluk-kalori-ihtiyaci-hesaplama','kalori-yakma-hesaplama','ideal-kilo-hesaplama','su-ihtiyaci-hesaplama','vucut-yag-orani-hesaplama'],
sources=[('Türkiye Beslenme Rehberi (TÜBER)','https://hsgm.saglik.gov.tr/tr/web-uygulamalarimiz/357.html'),('ISSN Protein ve Egzersiz Bildirgesi','https://jissn.biomedcentral.com/articles/10.1186/s12970-017-0177-8')],
))

# ───────────────────────── SU İHTİYACI ─────────────────────────
TOOLS.append(dict(
slug='su-ihtiyaci-hesaplama', name='Su İhtiyacı Hesaplama', cat='saglik', ico='💧',
title='Günlük Su İhtiyacı Hesaplama – Günde Kaç Litre Su İçmeliyim? | Hesaplarsın',
desc='Kilonuza, egzersiz sürenize ve hava sıcaklığına göre günde kaç litre su içmeniz gerektiğini hesaplayın. Bardak sayısı ve gün içine dağılım önerisi dahil.',
h1='💧 Günlük Su İhtiyacı Hesaplama',
lead='Kilonuzu, günlük egzersiz sürenizi ve hava durumunu girin; günde kaç litre (kaç bardak) su içmeniz gerektiğini öğrenin.',
form='''<div class="form-grid">
<div class="field"><label for="kilo">Kilo (kg)</label><input type="number" id="kilo" placeholder="örn: 70" inputmode="decimal"></div>
<div class="field"><label for="spor">Günlük Egzersiz (dakika)</label><input type="number" id="spor" placeholder="örn: 30" inputmode="numeric"></div>
<div class="field full"><label for="hava">Hava / Ortam</label><select id="hava"><option value="0">Normal / serin</option><option value="0.5">Sıcak (30°C üzeri)</option><option value="0.75">Çok sıcak ve nemli / ağır fiziksel iş</option></select></div>
<div class="field full"><label class="chk"><input type="checkbox" id="emzirme"> Emziriyorum</label></div>
</div>''' + UYARI,
js=r'''
function hesapla(){
  var k=v('kilo'), s=v('spor')||0; if(!(k>=20&&k<=300)) return 'Kilonuzu girin.';
  var taban=k*0.033, egz=s/30*0.35, hava=parseFloat(el('hava').value), em=checked('emzirme')?0.7:0, top=taban+egz+hava+em;
  return {main:['Günlük su ihtiyacınız', num(top,1)+' litre'], sub:'Yaklaşık '+num(top/0.2,0)+' su bardağı (200 ml)',
    rows:[['Temel ihtiyaç (33 ml × kg)',num(taban,2)+' L'],['Egzersiz ilavesi',num(egz,2)+' L'],['Sıcak hava ilavesi',num(hava,2)+' L'],['Emzirme ilavesi',num(em,2)+' L'],
      ['Uyanık olduğunuz her saat için',num(top/16*1000,0)+' ml']],
    note:'Bu miktar içecekler ve besinlerle alınan toplam sıvıyı ifade eder; yaklaşık %20’si yiyeceklerden karşılanır. Kalp veya böbrek hastalığı olanlar hekimlerine danışmalıdır.'};
}''',
article='''
<h2 id="ne-kadar">Günde kaç litre su içmeliyim?</h2>
<p>Genel kabul gören hesaplama, yetişkinler için <b>kilogram başına 30–35 ml</b> sıvıdır. 70 kg’lık bir yetişkin için bu yaklaşık 2,3 litreye karşılık gelir. Avrupa Gıda Güvenliği Otoritesi (EFSA), içecek ve yiyeceklerden gelen toplam sıvı için kadınlarda günde 2 litre, erkeklerde 2,5 litre önermektedir. Egzersiz, sıcak hava ve emzirme bu ihtiyacı artırır.</p>
<div class="formula">Temel su ihtiyacı (L) = Kilo (kg) × 0,033<br>+ her 30 dk egzersiz için ~0,35 L<br>+ sıcak havada 0,5–0,75 L</div>
<div class="example"><p><b>Örnek:</b> 70 kg, günde 30 dakika spor yapan ve sıcak bir yazda yaşayan biri:</p><p>70 × 0,033 = 2,31 L + 0,35 L + 0,5 L = <b>3,16 litre</b> (yaklaşık 16 bardak)</p></div>

<h2 id="tablo">Kiloya göre günlük su ihtiyacı tablosu</h2>
<div class="table-wrap"><table><thead><tr><th>Kilo</th><th>Günlük su</th><th>Bardak (200 ml)</th></tr></thead><tbody>
<tr><td>50 kg</td><td>1,65 L</td><td>8</td></tr><tr><td>60 kg</td><td>1,98 L</td><td>10</td></tr><tr><td>70 kg</td><td>2,31 L</td><td>12</td></tr>
<tr><td>80 kg</td><td>2,64 L</td><td>13</td></tr><tr><td>90 kg</td><td>2,97 L</td><td>15</td></tr><tr><td>100 kg</td><td>3,30 L</td><td>17</td></tr>
</tbody></table></div>

<h2 id="belirtiler">Susuzluğun belirtileri nelerdir?</h2>
<ul>
<li>Koyu sarı renkli idrar ve seyrek idrara çıkma</li><li>Ağız kuruluğu, baş ağrısı ve yorgunluk</li><li>Konsantrasyon güçlüğü ve baş dönmesi</li><li>Kabızlık ve kuru cilt</li>
</ul>
<p>İdrar renginin açık saman sarısı olması, yeterli sıvı aldığınızın pratik bir göstergesidir.</p>

<h2 id="ipuclari">Daha fazla su içmek için ipuçları</h2>
<ul>
<li>Güne bir bardak suyla başlayın ve her öğünle birlikte bir bardak su için.</li>
<li>Yanınızda ölçekli bir şişe taşıyın; telefonunuza hatırlatıcı kurun.</li>
<li>Salatalık, karpuz ve portakal gibi suyu bol besinleri tüketin.</li>
<li>Çay ve kahve de sıvı alımına katkı sağlar; ancak şekerli ve gazlı içecekler su yerine geçmemelidir.</li>
</ul>
<p>Spor yaptığınız günlerde ek su ihtiyacınızı belirlemek için harcadığınız enerjiyi <a href="/kalori-yakma-hesaplama.html">kalori yakma hesaplama</a> ile de görebilirsiniz.</p>
''',
faq=[
('Günde 2 litre su yeterli mi?','Pek çok yetişkin için başlangıç noktası olarak yeterlidir; ancak kilonuz, aktiviteniz ve hava sıcaklığı arttıkça ihtiyacınız da artar.'),
('Çay ve kahve su yerine geçer mi?','Kısmen. Ilımlı miktarda tüketilen çay ve kahve günlük sıvı alımına katkı sağlar, ancak ana sıvı kaynağınız su olmalıdır.'),
('Fazla su içmek zararlı mı?','Çok kısa sürede aşırı miktarda su içmek kandaki sodyum seviyesini düşürebilir (hiponatremi). Saatte 1 litreyi aşmamaya dikkat edin.'),
('Spor yaparken ne kadar su içmeliyim?','Egzersizden 2 saat önce yaklaşık 500 ml, egzersiz sırasında her 15–20 dakikada 150–250 ml su içmek önerilir.'),
],
related=['gunluk-kalori-ihtiyaci-hesaplama','protein-ihtiyaci-hesaplama','kalori-yakma-hesaplama','vucut-kitle-indeksi','bazal-metabolizma-hesaplama'],
sources=[('EFSA – Dietary reference values for water','https://www.efsa.europa.eu/en/efsajournal/pub/1459')],
))

# ───────────────────────── HEDEF KİLO SÜRESİ ─────────────────────────
TOOLS.append(dict(
slug='hedef-kilo-suresi-hesaplama', name='Hedef Kilo Süresi Hesaplama', cat='saglik', ico='📅',
title='Hedef Kilo Süresi Hesaplama – Kaç Haftada Kilo Veririm? | Hesaplarsın',
desc='Mevcut ve hedef kilonuza göre sağlıklı bir tempoda hedefinize kaç haftada ulaşacağınızı, tahmini tarihi ve önerilen günlük kalori açığını hesaplayın.',
h1='📅 Hedef Kilo Süresi Hesaplama',
lead='Mevcut kilonuzu, hedef kilonuzu ve haftalık tempoyu seçin; sağlıklı bir şekilde hedefinize ne zaman ulaşabileceğinizi görün.',
form='''<div class="form-grid">
<div class="field"><label for="boy">Boy (cm)</label><input type="number" id="boy" placeholder="örn: 170" inputmode="decimal"></div>
<div class="field"><label for="kilo">Mevcut Kilo (kg)</label><input type="number" id="kilo" placeholder="örn: 85" inputmode="decimal"></div>
<div class="field"><label for="hedef">Hedef Kilo (kg)</label><input type="number" id="hedef" placeholder="örn: 75" inputmode="decimal"></div>
<div class="field"><label for="tempo">Haftalık Tempo</label><select id="tempo"><option value="0.25">0,25 kg / hafta (yavaş)</option><option value="0.5" selected>0,5 kg / hafta (önerilen)</option><option value="0.75">0,75 kg / hafta</option><option value="1">1 kg / hafta (üst sınır)</option></select></div>
</div>''' + UYARI,
js=r'''
function hesapla(){
  var b=v('boy'), k=v('kilo'), h=v('hedef'), t=parseFloat(el('tempo').value);
  if(!(b>=130&&b<=230)) return 'Boyunuzu girin.'; if(!(k>=30&&k<=300)||!(h>=30&&h<=300)) return 'Mevcut ve hedef kilonuzu girin.';
  var m=b/100, hv=h/(m*m), alt=18.5*m*m;
  if(hv<18.5) return {main:['Hedef sağlıklı aralığın altında', 'VKİ '+num(hv,1)], sub:'Boyunuz için sağlıklı kilo alt sınırı yaklaşık '+num(alt,1)+' kg’dır.',
    rows:[['Sağlıklı kilo aralığı',num(alt,1)+' – '+num(24.9*m*m,1)+' kg']], note:'Bu hedefe yönelik bir plan oluşturmuyoruz. Kilo hedefinizi bir hekim veya diyetisyenle birlikte belirlemenizi öneririz.'};
  var fark=Math.abs(k-h); if(fark<0.1) return 'Mevcut ve hedef kilonuz aynı.';
  var al=h>k, tt=al?Math.min(t,0.5):t, hafta=fark/tt, tarih=new Date(); tarih.setDate(tarih.getDate()+Math.ceil(hafta*7));
  var gunluk=tt*7700/7;
  return {main:[(al?'Kilo almak':'Kilo vermek')+' için tahmini süre', num(Math.ceil(hafta),0)+' hafta'], sub:'Yaklaşık '+num(hafta/4.345,1)+' ay · Tahmini tarih: '+tarih.toLocaleDateString('tr-TR',{day:'numeric',month:'long',year:'numeric'}),
    rows:[['Hedeflenen değişim',num(fark,1)+' kg'],['Haftalık tempo',num(tt,2)+' kg'],['Gereken günlük enerji '+(al?'fazlası':'açığı'),'~'+num(gunluk,0)+' kcal'],['Hedef kilodaki VKİ',num(hv,1)]],
    note:al&&t>0.5?'Sağlıklı kilo alımı için tempo haftada 0,5 kg ile sınırlandırıldı.':'Kilo değişimi doğrusal ilerlemez; ilk haftalardaki hızlı düşüş çoğunlukla su kaybıdır. Plato dönemleri normaldir.'};
}''',
article='''
<h2 id="nasil">Hedef kiloya ulaşma süresi nasıl hesaplanır?</h2>
<p>Vücut yağının yaklaşık 1 kilogramı 7.700 kilokalori enerji depolar. Bu nedenle 1 kg vermek için toplamda yaklaşık 7.700 kcal enerji açığı oluşturmak gerekir. Hesaplayıcı, hedeflenen kilo farkını seçtiğiniz haftalık tempoya bölerek süreyi ve gereken günlük kalori açığını bulur.</p>
<div class="formula">Süre (hafta) = |Mevcut kilo − Hedef kilo| ÷ Haftalık tempo<br>Günlük kalori açığı = Haftalık tempo × 7.700 ÷ 7</div>
<div class="example"><p><b>Örnek:</b> 85 kg’dan 75 kg’a haftada 0,5 kg tempoyla: 10 ÷ 0,5 = <b>20 hafta</b> (yaklaşık 4,6 ay). Gereken günlük açık ≈ 550 kcal.</p></div>

<h2 id="tempo">Haftada kaç kilo vermek sağlıklıdır?</h2>
<p>Sağlık otoriteleri haftada <b>0,5–1 kg</b> kilo kaybını güvenli kabul eder. Daha hızlı kilo kaybı; kas kaybı, safra kesesi taşı riski, saç dökülmesi, halsizlik ve “yo-yo etkisi” denilen geri kilo alımı ile ilişkilidir. Yavaş ve istikrarlı ilerlemek, verilen kilonun korunma ihtimalini artırır.</p>
<div class="table-wrap"><table><thead><tr><th>Tempo</th><th>Günlük açık</th><th>10 kg için süre</th></tr></thead><tbody>
<tr><td>0,25 kg/hafta</td><td>~275 kcal</td><td>40 hafta</td></tr><tr><td>0,5 kg/hafta</td><td>~550 kcal</td><td>20 hafta</td></tr>
<tr><td>0,75 kg/hafta</td><td>~825 kcal</td><td>~14 hafta</td></tr><tr><td>1 kg/hafta</td><td>~1.100 kcal</td><td>10 hafta</td></tr>
</tbody></table></div>

<h2 id="hedef">Gerçekçi bir hedef nasıl belirlenir?</h2>
<p>İlk hedef olarak mevcut kilonuzun <b>%5–10’unu</b> vermek, kan şekeri, kan basıncı ve kolesterol üzerinde belirgin olumlu etkiler sağlar. Uzun vadeli hedefin <a href="/vucut-kitle-indeksi.html">vücut kitle indeksi</a> 18,5–24,9 aralığında olması önerilir. Boyunuza uygun aralığı <a href="/ideal-kilo-hesaplama.html">ideal kilo hesaplama</a> aracında görebilirsiniz.</p>

<h2 id="plato">Neden kilo vermeyi bıraktım? (Plato dönemi)</h2>
<p>Kilo verdikçe vücudunuzun enerji ihtiyacı da azalır; bu yüzden başlangıçtaki kalori açığı zamanla küçülür. Ayrıca su tutulumu, hormonal döngü ve kas kazanımı tartıdaki sayıyı haftalarca sabit gösterebilir. Plato döneminde <a href="/gunluk-kalori-ihtiyaci-hesaplama.html">günlük kalori ihtiyacınızı</a> yeni kilonuza göre yeniden hesaplamak ve hareketi artırmak faydalı olur.</p>
''',
faq=[
('1 ayda kaç kilo vermek sağlıklı?','Haftada 0,5–1 kg tempoyla ayda yaklaşık 2–4 kg kilo vermek sağlıklı kabul edilir.'),
('10 kilo kaç haftada verilir?','Önerilen haftada 0,5 kg tempoyla yaklaşık 20 hafta, haftada 1 kg ile yaklaşık 10 haftada verilebilir.'),
('İlk hafta neden çok kilo verdim?','Diyetin ilk günlerinde glikojen depolarıyla birlikte su kaybedilir; bu nedenle ilk haftadaki hızlı düşüş büyük oranda yağ değil sudur.'),
('Kilo almak için de kullanılabilir mi?','Evet. Hedef kilonuz mevcut kilonuzdan yüksekse hesaplayıcı sağlıklı kilo alımı için süreyi haftada en fazla 0,5 kg tempoyla hesaplar.'),
],
related=['gunluk-kalori-ihtiyaci-hesaplama','ideal-kilo-hesaplama','vucut-kitle-indeksi','kalori-yakma-hesaplama','protein-ihtiyaci-hesaplama'],
))

# ───────────────────────── VÜCUT YAĞ ORANI ─────────────────────────
TOOLS.append(dict(
slug='vucut-yag-orani-hesaplama', name='Vücut Yağ Oranı Hesaplama', cat='saglik', ico='💪',
title='Vücut Yağ Oranı Hesaplama – Mezura ile (US Navy Yöntemi) | Hesaplarsın',
desc='Boy, boyun, bel (ve kadınlarda kalça) ölçülerinizle vücut yağ oranınızı ABD Donanması (US Navy) yöntemiyle hesaplayın. Yağ kütlesi, yağsız kütle ve kategori.',
h1='💪 Vücut Yağ Oranı Hesaplama',
lead='Bir mezura ile ölçeceğiniz boyun, bel ve kalça çevrenizi girin; vücut yağ yüzdenizi, yağ ve yağsız kütlenizi ve fitness kategorinizi öğrenin.',
form='''<div class="form-grid">''' + CINSIYET + '''
<div class="field"><label for="boy">Boy (cm)</label><input type="number" id="boy" placeholder="örn: 175" inputmode="decimal"></div>
<div class="field"><label for="kilo">Kilo (kg) <small>kütle hesabı için</small></label><input type="number" id="kilo" placeholder="örn: 78" inputmode="decimal"></div>
<div class="field"><label for="boyun">Boyun Çevresi (cm)</label><input type="number" id="boyun" placeholder="örn: 38" inputmode="decimal"></div>
<div class="field"><label for="bel">Bel Çevresi (cm) <small>göbek hizası</small></label><input type="number" id="bel" placeholder="örn: 86" inputmode="decimal"></div>
<div class="field" id="f-kalca"><label for="kalca">Kalça Çevresi (cm) <small>kadınlar için</small></label><input type="number" id="kalca" placeholder="örn: 98" inputmode="decimal"></div>
</div>''' + UYARI,
js=r'''
function hesapla(){
  var e=radio('cins')==='e', b=v('boy'), k=v('kilo'), n=v('boyun'), w=v('bel'), h=v('kalca');
  if(!(b>=130&&b<=230)||!(n>20)||!(w>40)) return 'Boy, boyun ve bel ölçülerinizi girin.'; if(!e&&!(h>50)) return 'Kadınlar için kalça çevresi gereklidir.';
  if(w-n<=0||(!e&&w+h-n<=0)) return 'Ölçüleri kontrol edin (bel, boyundan büyük olmalı).';
  var y=e?495/(1.0324-0.19077*Math.log10(w-n)+0.15456*Math.log10(b))-450 : 495/(1.29579-0.35004*Math.log10(w+h-n)+0.221*Math.log10(b))-450;
  if(!(y>2&&y<70)) return 'Ölçüler gerçekçi bir sonuç vermedi; lütfen tekrar ölçün.';
  var kat=e?(y<6?'Temel yağ':y<14?'Atlet':y<18?'Fit':y<25?'Ortalama':'Yüksek'):(y<14?'Temel yağ':y<21?'Atlet':y<25?'Fit':y<32?'Ortalama':'Yüksek');
  var rows=[['Kategori',kat]]; if(k>0){rows.push(['Yağ kütlesi',num(k*y/100,1)+' kg']);rows.push(['Yağsız vücut kütlesi',num(k*(1-y/100),1)+' kg']);}
  rows.push(['Bel / boy oranı',num(w/b,2)+(w/b>0.5?' (0,5 üzeri risk göstergesi)':' (sağlıklı)')]);
  return {main:['Vücut yağ oranınız', '%'+num(y,1)], sub:'US Navy yöntemi · '+(e?'Erkek':'Kadın'), rows:rows};
}''',
article='''
<h2 id="nedir">Vücut yağ oranı nedir?</h2>
<p>Vücut yağ oranı, toplam vücut ağırlığınızın yüzde kaçının yağ dokusundan oluştuğunu gösterir. Kilo ve <a href="/vucut-kitle-indeksi.html">vücut kitle indeksi</a> kas ile yağı ayırt edemezken, yağ oranı vücut kompozisyonu hakkında çok daha anlamlı bilgi verir. Aynı kiloda iki kişiden kas kütlesi yüksek olanın yağ oranı daha düşüktür.</p>

<h2 id="nasil">Vücut yağ oranı nasıl hesaplanır? (US Navy yöntemi)</h2>
<p>Bu araç, ABD Donanması tarafından geliştirilen ve yalnızca bir mezura ile uygulanabilen çevre ölçümü yöntemini kullanır. Yöntem, DEXA gibi laboratuvar ölçümlerine göre genellikle ±%3–4 sapma ile tahmin yapar.</p>
<div class="formula">Erkek: %Yağ = 495 ÷ (1,0324 − 0,19077 × log₁₀(bel − boyun) + 0,15456 × log₁₀(boy)) − 450<br>Kadın: %Yağ = 495 ÷ (1,29579 − 0,35004 × log₁₀(bel + kalça − boyun) + 0,221 × log₁₀(boy)) − 450</div>

<h2 id="olcum">Ölçümler nasıl yapılmalı?</h2>
<ul>
<li><b>Boyun:</b> Gırtlak çıkıntısının hemen altından, mezura hafifçe aşağı eğimli olacak şekilde ölçün.</li>
<li><b>Bel:</b> Erkeklerde göbek deliği hizasından, kadınlarda belin en ince yerinden; nefesi normal şekilde verdikten sonra ölçün.</li>
<li><b>Kalça (kadınlar):</b> Kalçanın en geniş noktasından ölçün.</li>
<li>Ölçümleri sabah, aç karnına ve mezurayı sıkmadan yapın; en doğru sonuç için üç ölçümün ortalamasını alın.</li>
</ul>

<h2 id="degerler">Vücut yağ oranı kaç olmalı?</h2>
<div class="table-wrap"><table><thead><tr><th>Kategori</th><th>Erkek</th><th>Kadın</th></tr></thead><tbody>
<tr><td>Temel (yaşamsal) yağ</td><td>%2 – 5</td><td>%10 – 13</td></tr><tr><td>Atlet</td><td>%6 – 13</td><td>%14 – 20</td></tr>
<tr><td>Fit</td><td>%14 – 17</td><td>%21 – 24</td></tr><tr><td>Ortalama</td><td>%18 – 24</td><td>%25 – 31</td></tr><tr><td>Yüksek</td><td>%25 ve üzeri</td><td>%32 ve üzeri</td></tr>
</tbody></table></div>
<p>Kaynak: American Council on Exercise (ACE). Kadınlarda hormonal sağlık ve doğurganlık için daha yüksek temel yağ oranı gereklidir; temel yağın altına inmek sağlık için tehlikelidir.</p>

<h2 id="bel">Bel çevresi neden önemli?</h2>
<p>Karın bölgesinde biriken iç organ (visseral) yağı, tip 2 diyabet ve kalp-damar hastalıkları ile en güçlü ilişkiyi gösteren yağ türüdür. Bel çevrenizin boyunuzun yarısını aşmaması (bel/boy oranı &lt; 0,5) basit ve güçlü bir sağlık göstergesidir. <a href="/bel-kalca-orani-hesaplama.html">Bel-kalça oranı hesaplama</a> aracıyla da yağ dağılımınızı değerlendirebilirsiniz.</p>
''',
faq=[
('Vücut yağ oranı evde nasıl ölçülür?','Bir mezura ile boyun, bel ve (kadınlarda) kalça çevresini ölçüp bu hesaplayıcıya girmek en pratik yöntemdir. Tartıların biyoelektrik (BIA) ölçümleri ise su durumuna göre değişkenlik gösterir.'),
('Erkekler için ideal yağ oranı kaç?','Sağlıklı erkeklerde %14–24, fit görünüm için %14–17 arası iyi kabul edilir.'),
('Kadınlar için ideal yağ oranı kaç?','Sağlıklı kadınlarda %21–31, fit görünüm için %21–24 arası iyi kabul edilir.'),
('US Navy yöntemi ne kadar doğru?','Çoğu kişi için ±%3–4 hata payıyla tutarlı bir tahmin verir. Çok kaslı veya çok yüksek kilolu kişilerde sapma artabilir.'),
],
related=['bel-kalca-orani-hesaplama','vucut-kitle-indeksi','ideal-kilo-hesaplama','bazal-metabolizma-hesaplama','protein-ihtiyaci-hesaplama'],
sources=[('ACE – Body Fat Percentage','https://www.acefitness.org/'),('Hodgdon & Beckett, Naval Health Research Center (1984)','https://apps.dtic.mil/sti/citations/ADA143890')],
))
