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
title='Para Sayma Hesaplama – 225 Tane 200 TL Ne Kadar Eder? | Hesaplarsın',
desc='225 tane 200 TL 45.000 TL eder. Elinizdeki 200, 100, 50, 20, 10 ve 5 TL banknotların adedini girin; toplam tutarı, deste sayısını anında görün.',
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
