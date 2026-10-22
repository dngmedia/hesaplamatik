"""Maaş Sıralaması: "Maaşın Türkiye'de kaçıncı sırada?"
Veri: DİSK-AR Asgari Ücret Araştırması 2026 (Aralık 2025), TÜİK Hanehalkı İşgücü Anketi 2024 mikro verisinden;
özel sektör ücretli çalışanların asgari ücrete göre kümülatif dağılımı. 2×'in üstü için Pareto kuyruk varsayımı (α=2) — tahmini.
Güncelleme: yeni asgari ücret (NET) ve yeni dağılım noktaları geldiğinde CDF ve NET değerlerini değiştirin.
"""
TOOLS = []

NET = 28075.50  # 2026 net asgari ücret
CDF = [(0.0, 0.0), (0.5, 9.0), (1.0, 46.7), (1.05, 49.6), (1.10, 53.2), (1.20, 62.5), (2.0, 87.3)]

JS = r'''
var NET=28075.50, CDF=[[0,0],[0.5,9.0],[1.0,46.7],[1.05,49.6],[1.10,53.2],[1.20,62.5],[2.0,87.3]], MEMUR=73103;
function altPay(x){ // x = maaş / net asgari ücret; dönüş: bu maaşın altında kazananların yüzdesi
  if(x<=0) return 0;
  for(var i=1;i<CDF.length;i++){ if(x<=CDF[i][0]){ var a=CDF[i-1],b=CDF[i]; return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]); } }
  return 100-12.7*Math.pow(x/2,-2);
}
function ustEsik(p){ // en üst p% için gereken kat (kuyruk)
  return 2*Math.sqrt(12.7/p);
}
function hesapla(){
  var m=v('maas'); if(!(m>0)) return 'Aylık net maaşınızı girin.'; if(m>5e6) return 'Lütfen aylık net tutar girin.';
  var x=m/NET, p=altPay(x), tah=x>2, asg=Math.abs(x-1)<0.01, ust=Math.max(0.1,100-p);
  var pr=num(p,p>=99?1:0), ana;
  if(asg){ ana='Asgari ücretle çalışıyorsun'; } else if(x<1){ ana='Çalışanların %'+pr+'’i senden az kazanıyor'; } else { ana='Çalışanların %'+pr+'’inden fazla kazanıyorsun'; }
  var med=NET*1.0556;
  window._kart={p:p, x:x, asg:asg, tah:tah};
  return {main:[ana, asg?'Çalışanların %46,7’si gibi':(x<1?'Alt %'+num(p,0):(tah?'≈ ':'')+'En üst %'+num(ust,ust<10?1:0))], sub:'Net asgari ücretin '+num(x,2)+' katı · özel sektör ücretli çalışanlar',
    rows:[['Net asgari ücret (2026)',tl(NET)],['Senin maaşın / asgari ücret',num(x,2)+' kat'],
          ['Medyan maaş (tahmini, çalışanların yarısı bunun altında)',tl(med)],['Medyana göre',(m>=med?'+':'')+tl(m-med),m>=med?'hl':'neg'],
          ['9/1 derecede memur maaşı (Temmuz 2026)',tl(MEMUR)],['En üst %10’a girmek için (tahmini)',tl(NET*ustEsik(10))],['En üst %1’e girmek için (tahmini)',tl(NET*ustEsik(1))]],
    extra:'<div class="kart-btns"><button type="button" class="btn-kart" onclick="kartIndir()">🖼️ Sonuç kartını indir</button><button type="button" class="btn-kart" onclick="kartPaylas()">📲 Hikâyede paylaş</button></div><p class="kart-not">Kartta maaş tutarın yer almaz, yalnızca sıralaman görünür.</p>',
    note:(tah?'Asgari ücretin 2 katının üzerindeki sıralamalar resmî kırılım olmadığından tahminidir. ':'')+'Dağılım: TÜİK Hanehalkı İşgücü Anketi 2024 (DİSK-AR derlemesi), özel sektör ücretli çalışanlar; asgari ücrete oranla 2026’ya uyarlanmıştır.'};
}
function kartCiz(){
  var k=window._kart; if(!k) return null; var c=document.createElement('canvas'); c.width=1080; c.height=1920; var g=c.getContext('2d');
  var gr=g.createLinearGradient(0,0,1080,1920); gr.addColorStop(0,'#0f307a'); gr.addColorStop(0.55,'#1341b0'); gr.addColorStop(1,'#1a56db'); g.fillStyle=gr; g.fillRect(0,0,1080,1920);
  g.fillStyle='rgba(255,255,255,.06)'; g.beginPath(); g.arc(940,260,360,0,7); g.fill(); g.beginPath(); g.arc(120,1700,300,0,7); g.fill();
  g.fillStyle='#fff'; g.textAlign='center'; var F='-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif';
  g.font='700 54px '+F; g.fillText('Maaşım Türkiye’de', 540, 560);
  var big, alt;
  if(k.asg){ big='%46,7'; alt=['Asgari ücretle çalışan','%46,7’lik kesimdeyim']; }
  else if(k.x<1){ big='%'+Math.round(k.p); alt=['çalışan benden','az kazanıyor']; }
  else { big='%'+(k.p>=99?num(k.p,1):Math.round(k.p)); alt=['çalışandan fazla','kazanıyorum']; }
  g.fillStyle='#fbbf24'; g.font='900 300px '+F; g.fillText(big, 540, 900);
  g.fillStyle='#fff'; g.font='800 76px '+F; g.fillText(alt[0], 540, 1050); g.fillText(alt[1], 540, 1145);
  g.font='500 46px '+F; g.globalAlpha=.85; g.fillText('Net asgari ücretin '+num(k.x,2)+' katı'+(k.tah?' (tahmini)':''), 540, 1260); g.globalAlpha=1;
  g.fillStyle='#fff'; g.beginPath(); if(g.roundRect){g.roundRect(120,1470,840,160,44);}else{g.rect(120,1470,840,160);} g.fill();
  g.fillStyle='#1341b0'; g.font='800 46px '+F; g.fillText('Sen de hesapla 👉', 540, 1530); g.font='700 38px '+F; g.fillText('hesaplarsin.com/maas-siralamasi', 540, 1590);
  g.fillStyle='rgba(255,255,255,.7)'; g.font='500 30px '+F; g.fillText('Özel sektör ücretli çalışanlar · TÜİK HİA 2024 verisiyle', 540, 1760);
  return c;
}
function kartIndir(){var c=kartCiz(); if(!c) return; var a=document.createElement('a'); a.download='maas-siralamam.png'; a.href=c.toDataURL('image/png'); a.click();}
function kartPaylas(){var c=kartCiz(); if(!c) return; c.toBlob(function(b){var f=new File([b],'maas-siralamam.png',{type:'image/png'});
  if(navigator.canShare&&navigator.canShare({files:[f]})){navigator.share({files:[f],text:'Maaşım Türkiye’de kaçıncı sırada? Sen de hesapla: https://hesaplarsin.com/maas-siralamasi.html'}).catch(function(){});}
  else{kartIndir(); toast('Görsel indirildi; hikâyene ekleyebilirsin.');}});}
'''

FORM = '''<div class="form-grid"><div class="field full"><label for="maas">Aylık Net Maaşın (₺) <small>elinize geçen tutar; prim/ikramiye hariç</small></label>
<input type="number" id="maas" placeholder="örn: 42.000" inputmode="decimal"></div></div>
<style>.kart-btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}.btn-kart{flex:1;min-width:180px;background:#f59e0b;color:#fff;border:0;border-radius:10px;padding:13px 16px;font-weight:800;font-size:.92rem;cursor:pointer}.btn-kart:hover{filter:brightness(.95)}.kart-not{font-size:.76rem;color:var(--muted);margin-top:6px}</style>'''

ART = '''
<p><b>Kısa cevap:</b> Türkiye’de özel sektörde çalışanların yaklaşık <b>yarısı asgari ücret veya hemen üzerinde</b> kazanıyor. TÜİK verilerine göre ücretli çalışanların %46,7’si asgari ücret veya altında, %62,5’i asgari ücretin 1,2 katına kadar ücret alıyor; asgari ücretin 2 katından fazla kazananların oranı ise yalnızca <b>%12,7</b>. 2026 net asgari ücretiyle bu, ayda yaklaşık <b>56.150 ₺</b> ve üzeri net maaşın çalışanların en üst %13’üne girdiği anlamına geliyor.</p>

<h2 id="dagilim">Türkiye’de maaş dağılımı (özel sektör)</h2>
<div class="table-wrap"><table><thead><tr><th>Net maaş (2026 karşılığı)</th><th>Asgari ücrete oranı</th><th>Bu tutar ve altında kazananlar</th></tr></thead><tbody>
<tr><td>14.038 ₺ ve altı</td><td>0,5 kat</td><td>%9,0</td></tr>
<tr><td>28.075,50 ₺ (asgari ücret) ve altı</td><td>1,0 kat</td><td>%46,7</td></tr>
<tr><td>29.479 ₺ ve altı</td><td>1,05 kat</td><td>%49,6</td></tr>
<tr><td>30.883 ₺ ve altı</td><td>1,10 kat</td><td>%53,2</td></tr>
<tr><td>33.691 ₺ ve altı</td><td>1,20 kat</td><td>%62,5</td></tr>
<tr><td>56.151 ₺ ve altı</td><td>2,0 kat</td><td>%87,3</td></tr>
<tr><td>56.151 ₺’nin üzeri</td><td>2 kattan fazla</td><td>%12,7 (en üst dilim)</td></tr>
</tbody></table></div>
<p><small>Kaynak: TÜİK Hanehalkı İşgücü Anketi 2024 mikro verisinden DİSK-AR’ın derlediği özel sektör ücretli çalışan dağılımı (Asgari Ücret Araştırması 2026). Oranlar asgari ücretin katları olarak verildiği için 2026 net asgari ücretiyle TL’ye çevrilmiştir.</small></p>

<h2 id="medyan">Türkiye’de medyan maaş ne kadar?</h2>
<p>Medyan maaş, çalışanların yarısının altında, yarısının üstünde kaldığı tutardır. Dağılıma göre özel sektörde medyan, asgari ücretin yaklaşık <b>1,06 katı</b>dır; 2026 rakamlarıyla bu ayda yaklaşık <b>29.640 ₺ net</b> eder. Yani asgari ücretin yalnızca %5–6 üzerinde bir maaş, çalışanların yarısından fazla kazanmak için yeterli. Ortalama maaş ise medyandan yüksektir; çünkü az sayıdaki yüksek maaş ortalamayı yukarı çeker. TÜİK’e göre ücretli çalışanların ortalama ücret geliri asgari ücretin yaklaşık 1,8 katıdır (2023).</p>

<h2 id="kadin">Kadın ve erkek çalışanlar arasındaki fark</h2>
<p>Kadın çalışanlarda düşük ücret oranı daha yüksek: kadınların <b>%60,1</b>’i asgari ücret veya altında ücret alırken bu oran tüm çalışanlarda %46,7’dir. Asgari ücretin yarısı veya altında ücret alanların oranı kadınlarda %15,3, tüm çalışanlarda %9’dur. Kayıt dışı çalışanlarda ise tablo çok daha ağır: kayıt dışı çalışanların yaklaşık %40’ı asgari ücretin yarısı kadar veya daha az kazanıyor.</p>

<h2 id="bolge">Bölgelere göre gelir</h2>
<p>TÜİK Gelir ve Yaşam Koşulları Araştırması 2025’e göre (2024 gelirleri) kişi başına yıllık eşdeğer hanehalkı kullanılabilir geliri en yüksek bölge <b>Ankara</b> (449.618 ₺), ardından <b>İstanbul</b> (434.929 ₺) ve <b>İzmir</b> (405.896 ₺); en düşük bölge ise Van, Muş, Bitlis ve Hakkari’dir (172.552 ₺). Türkiye ortalaması 332.882 ₺’dir. Bu rakamlar maaş değil, hanedeki tüm gelirlerin kişi başına düşen payıdır; yine de yaşadığınız bölgenin gelir seviyesi hakkında fikir verir.</p>

<h2 id="yontem">Hesaplama nasıl yapılıyor?</h2>
<ol>
<li>Girdiğiniz net maaş, 2026 net asgari ücretine (28.075,50 ₺) bölünür.</li>
<li>Bulunan oran, TÜİK verisindeki asgari ücrete göre dağılımda yerine konur; ara değerler doğrusal olarak hesaplanır.</li>
<li>Asgari ücretin 2 katının üzerindeki maaşlar için resmî kırılım bulunmadığından, üst kesimdeki dağılım gelir araştırmalarında yaygın kullanılan Pareto yaklaşımıyla <b>tahmin</b> edilir. Bu bölgedeki sonuçlar yaklaşık değerlerdir.</li>
</ol>
<p>Hesaplama yalnızca <b>özel sektör ücretli çalışanları</b> kapsar; memurlar, işverenler ve kendi hesabına çalışanlar dahil değildir. Girdiğiniz tutar kaydedilmez, hesaplama tarayıcınızda yapılır. Paylaşım kartında maaş tutarınız yer almaz.</p>

<h2 id="artir">Maaşını nasıl karşılaştırmalısın?</h2>
<ul>
<li>Brüt maaşınızı biliyorsanız önce <a href="/net-maas-hesaplama.html">net maaş hesaplama</a> ile netini bulun; yıl içinde vergi dilimi nedeniyle net değişebileceği için yıllık ortalamayı kullanmak daha doğrudur.</li>
<li>Kamuda çalışıyorsanız <a href="/memur-maaslari.html">memur maaşları tablosuyla</a> unvanınıza göre karşılaştırın.</li>
<li>Zam teklifini değerlendirirken <a href="/maas-zam-hesaplama.html">maaş zam hesaplama</a> ile reel artışı görün.</li>
<li>Ocak 2027’de asgari ücret artacağı için sıralamanız değişmese bile TL karşılıkları güncellenecek. Tahminler için <a href="/blog/asgari-ucret-2027.html">Asgari Ücret 2027</a>.</li>
</ul>
'''

TOOLS.append(dict(
slug='maas-siralamasi', name='Maaş Sıralaması: Türkiye’de Kaçıncı Sıradasın?', cat='maas', ico='🏆',
title='Maaşın Türkiye’de Kaçıncı Sırada? Maaş Sıralaması 2026',
desc='Maaşın yüksek mi? Net maaşını gir, Türkiye’deki çalışanların yüzde kaçından fazla kazandığını gör. TÜİK verisiyle 2026 maaş sıralaması ve paylaşılabilir kart.',
h1='🏆 Maaşın Türkiye’de Kaçıncı Sırada?',
lead='Aylık net maaşını gir; Türkiye’de özel sektörde çalışanların yüzde kaçından fazla kazandığını, medyan maaşa ve asgari ücrete göre durumunu gör. Sonucu kart olarak paylaş.',
card_title='Maaş sıralamanı öğren', button='Sıralamamı Göster',
badges=['✓ Ücretsiz', 'TÜİK verisi', 'Maaşın kaydedilmez'],
form=FORM, js=JS, article=ART,
faq=[
('Türkiye’de çalışanların yüzde kaçı asgari ücret alıyor?', 'TÜİK Hanehalkı İşgücü Anketi 2024 verisine göre özel sektör ücretli çalışanların %46,7’si asgari ücret veya altında ücret alıyor. Asgari ücretin %10 fazlasına kadar kazananlar dahil edildiğinde oran %53,2’ye çıkıyor.'),
('Türkiye’de medyan maaş ne kadar?', 'Özel sektörde medyan maaş asgari ücretin yaklaşık 1,06 katıdır. 2026 net asgari ücretiyle bu, ayda yaklaşık 29.640 TL net eder.'),
('Ne kadar kazanan Türkiye’de en üst %10’a girer?', 'Asgari ücretin 2 katından fazla kazananlar özel sektör çalışanlarının en üst %12,7’sini oluşturuyor; bu 2026’da yaklaşık 56.150 TL net maaşa karşılık gelir. En üst %10 için tahmini eşik yaklaşık 63.300 TL nettir.'),
('Maaşım yüksek mi?', 'Net maaşınız 29.640 TL’nin üzerindeyse özel sektör çalışanlarının yarısından fazla, 56.150 TL’nin üzerindeyse yaklaşık %87’sinden fazla kazanıyorsunuz. Kesin sıralamanızı hesaplayıcıya maaşınızı girerek görebilirsiniz.'),
('Girdiğim maaş kaydediliyor mu?', 'Hayır. Hesaplama tamamen tarayıcınızda yapılır, tutar sunucuya gönderilmez. Paylaşım kartında da maaş tutarınız yer almaz.'),
],
related=['net-maas-hesaplama', 'asgari-ucret-hesaplama', 'maas-zam-hesaplama', 'memur-maaslari', 'issizlik-maasi-hesaplama'],
sources=[('DİSK-AR – Asgari Ücret Araştırması 2026 (TÜİK HİA 2024 mikro verisi)', 'https://arastirma.disk.org.tr/'),
         ('TÜİK – Gelir ve Yaşam Koşulları Araştırması 2025', 'https://data.tuik.gov.tr/'),
         ('ÇSGB – 2026 asgari ücret', 'https://www.csgb.gov.tr/')],
))
