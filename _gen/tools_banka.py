"""Banka komisyon hesaplama: (1) havale/EFT/FAST ücret üst sınırları (2026, TCMB), (2) POS / kredi kartı komisyonu.
GÜNCELLEME: EFT ücret dilimleri her yıl başında (önceki yıl enflasyonu oranında) güncellenir → DILIM listesi + makale.
Kaynak: 2026 tarifesi 5 Şubat 2026'dan itibaren; 8.300 ₺'ye kadar 8,37 ₺; 8.300–399.000 ₺ 16,76 ₺; üzeri 209,38 ₺ (mobil/internet üst sınır).
"""
TOOLS = []
DILIM = [(8300, 8.37), (399000, 16.76), (None, 209.38)]


def tr(x, d=2):
    s = f"{x:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


FORM = '''<div class="field full" style="margin-bottom:14px"><label>Hesaplama türü</label><div class="seg"><label><input type="radio" name="tur" value="eft" checked onchange="bkMod()">Havale / EFT / FAST ücreti</label><label><input type="radio" name="tur" value="pos" onchange="bkMod()">POS / kredi kartı komisyonu</label></div></div>
<div class="form-grid" id="f-eft">
<div class="field"><label for="tutar">Gönderilecek tutar (₺)</label><input type="number" id="tutar" placeholder="örn: 50.000" inputmode="decimal"></div>
<div class="field"><label for="islem">Aylık işlem sayısı <small>isteğe bağlı</small></label><input type="number" id="islem" value="1" inputmode="numeric"></div>
</div>
<div class="form-grid" id="f-pos" style="display:none">
<div class="field"><label for="satis">Satış tutarı (₺)</label><input type="number" id="satis" placeholder="örn: 10.000" inputmode="decimal"></div>
<div class="field"><label for="poran">Peşin komisyon oranı (%) <small>bankanızla anlaşmanız</small></label><input type="number" id="poran" placeholder="örn: 2,5" inputmode="decimal"></div>
<div class="field"><label for="taksit">Taksit sayısı</label><input type="number" id="taksit" value="1" inputmode="numeric"></div>
<div class="field"><label for="tek">Taksit başına ek komisyon (%) <small>taksitli satışta</small></label><input type="number" id="tek" placeholder="örn: 1,5" inputmode="decimal"></div>
<div class="field"><label for="sabit">İşlem başı sabit ücret (₺)</label><input type="number" id="sabit" placeholder="0" inputmode="decimal"></div>
<div class="field"><label class="chk" style="margin-top:28px"><input type="checkbox" id="bsmv"> Komisyona %5 BSMV ekle</label></div>
</div>'''

JS = r'''
function bkMod(){var t=radio('tur');el('f-eft').style.display=t==='eft'?'':'none';el('f-pos').style.display=t==='pos'?'':'none';}
function hesapla(){
  if(radio('tur')==='pos'){
    var S=v('satis'),o=v('poran'),n=Math.max(1,Math.round(v('taksit')||1)),te=v('tek')||0,sb=v('sabit')||0,b=el('bsmv').checked;
    if(!(S>0)) return 'Satış tutarını girin.'; if(!(o>=0)||o>30) return 'Komisyon oranını kontrol edin.';
    var top=o+(n>1?te*(n-1):0), k=S*top/100, bs=b?k*0.05:0, kes=k+bs+sb, net=S-kes;
    return {main:['Hesabınıza geçecek net tutar',tl(net)],sub:'Toplam kesinti '+tl(kes)+' · etkin oran %'+num(kes/S*100,2),
      rows:[['Satış tutarı',tl(S)],['Toplam komisyon oranı','%'+num(top,2)+(n>1?' ('+n+' taksit)':' (peşin)')],['Komisyon','−'+tl(k),'neg']].concat(b?[['BSMV (%5)','−'+tl(bs),'neg']]:[]).concat(sb>0?[['Sabit işlem ücreti','−'+tl(sb),'neg']]:[]).concat([['Net tutar',tl(net),'hl'],['Kesintiyi karşılamak için gereken satış fiyatı',tl((S+sb)/(1-top/100*(b?1.05:1)))]]),
      note:'Komisyon oranları bankaya, sektöre, ciroya ve paranın hesaba geçiş süresine (valör/bloke) göre değişir. Taksitli satışta ek oranlar bankadan bankaya farklıdır; kendi POS sözleşmenizdeki oranları girin.'};
  }
  var T=v('tutar'), m=Math.max(1,Math.round(v('islem')||1)); if(!(T>0)) return 'Gönderilecek tutarı girin.';
  var f=T<=8300?8.37:(T<=399000?16.76:209.38), d=T<=8300?'8.300 ₺’ye kadar':(T<=399000?'8.300 – 399.000 ₺':'399.000 ₺ üzeri');
  var fast=T<=100000;
  return {main:['En fazla kesilebilecek EFT ücreti',tl(f)],sub:'Tutar dilimi: '+d+' · mobil/internet bankacılığı üst sınırı',
    rows:[['Gönderilen tutar',tl(T)],['Ücret dilimi',d],['Azami EFT ücreti',tl(f),'hl'],['Havale ücreti (aynı banka içi)','Genellikle EFT’den düşük veya ücretsiz'],
      ['FAST ile gönderilebilir mi?',fast?'Evet (tek seferde 100.000 ₺’ye kadar)':'Hayır, 100.000 ₺ FAST sınırını aşıyor; EFT kullanılır'],
      ['Aylık '+m+' işlemde azami toplam',tl(f*m)],['Yıllık azami toplam',tl(f*m*12)]],
    note:'Tutarlar 2026 için mobil ve internet bankacılığında alınabilecek üst sınırlardır; bankalar daha düşük ücret alabilir, bazı dijital bankalar ücret almaz. Şube işlemlerinde ücretler daha yüksek olabilir. Kesin ücret için bankanızın ücret tarifesine bakın.'};
}
'''

_d = '<div class="table-wrap"><table><thead><tr><th>Gönderilen tutar</th><th>Azami ücret (mobil/internet)</th></tr></thead><tbody><tr><td>8.300 ₺’ye kadar</td><td>8,37 ₺</td></tr><tr><td>8.300 – 399.000 ₺</td><td>16,76 ₺</td></tr><tr><td>399.000 ₺ üzeri</td><td>209,38 ₺</td></tr></tbody></table></div>'

TOOLS.append(dict(
slug='banka-komisyon-hesaplama', name='Banka Komisyon Hesaplama', cat='finans', ico='🏦',
title='Banka Komisyon Hesaplama 2026 – EFT, Havale, FAST ve POS Ücreti | Hesaplarsın',
desc='EFT ve havale ücreti ne kadar? 2026 tutar dilimlerine göre azami ücreti, FAST sınırını ve POS/kredi kartı komisyonu sonrası hesabınıza geçecek tutarı görün.',
h1='🏦 Banka Komisyon Hesaplama',
lead='Para transferinde bankanın en fazla ne kadar ücret kesebileceğini ya da işletmenizin POS cihazından kartla yapılan satışta komisyon sonrası eline ne kalacağını hesaplayın. 2026 EFT ücret dilimleri ve FAST sınırı dahildir.',
card_title='Banka Komisyonu Hesaplayıcı', button='Hesapla',
form=FORM, js=JS,
article=f'''<h2 id="nasil">Banka komisyonu nasıl hesaplanır?</h2>
<div class="kisa-cevap" style="border:2px solid #bfdbfe;background:#eff6ff;border-radius:14px;padding:16px 18px;margin:14px 0 22px;line-height:1.65;font-size:.95rem"><p style="margin:0 0 10px"><strong>Kısa cevap:</strong> EFT ve havalede ücret yüzdeyle değil, gönderilen tutarın düştüğü <strong>sabit dilime</strong> göre alınır; 2026’da mobil ve internet bankacılığında üst sınır 8,37 ₺, 16,76 ₺ veya 209,38 ₺’dir. POS ve kredi kartı satışlarında ise komisyon, satış tutarının bankayla anlaşılan oranla çarpılmasıyla bulunur.</p>
<p style="margin:0 0 8px;font-family:ui-monospace,Menlo,Consolas,monospace;background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:8px 10px;font-size:.88rem">POS komisyonu = Satış × Oran ÷ 100 · Net = Satış − Komisyon − Sabit ücret</p>
<p style="margin:0"><strong>Örnek:</strong> 50.000 ₺ EFT → en fazla <strong>16,76 ₺</strong> · 10.000 ₺ kartla satış, %2,5 komisyon → <strong>250 ₺</strong> kesinti, hesaba <strong>9.750 ₺</strong></p></div>
<h2 id="eft">2026 EFT ve havale ücretleri</h2>
<p>Bankaların para transferinde alabileceği ücretlerin üst sınırı Türkiye Cumhuriyet Merkez Bankası düzenlemeleriyle belirlenir ve her yıl bir önceki yılın enflasyonu oranında güncellenir. 2026 tarifesi 5 Şubat 2026’dan itibaren uygulanıyor; tutarlar bir önceki yıla göre yaklaşık %30,9 arttı.</p>
{_d}
<p>Bunlar <strong>üst sınırdır</strong>: bankalar daha az ücret alabilir, bazı dijital bankalar ve kampanyalar ücretsizdir. Aynı banka içindeki havaleler genellikle daha ucuz ya da ücretsizdir. Şubeden yapılan işlemlerde ücretler daha yüksek olabilir.</p>
<h2 id="fast">FAST nedir, sınırı ne kadar?</h2>
<p>FAST, Merkez Bankası’nın 7/24 anlık para transferi sistemidir; hafta sonu ve gece de para saniyeler içinde karşıya geçer. 2026’da tek seferde FAST ile gönderilebilecek tutar <strong>100.000 ₺</strong>’dir. Daha yüksek tutarlar EFT ile, mesai saatlerinde gönderilir.</p>
<h2 id="pos">POS ve kredi kartı komisyonu</h2>
<p>İşletmeler kartla yapılan satışlarda bankaya komisyon öder. Oran; bankaya, sektöre, aylık ciroya ve paranın hesaba ne zaman geçeceğine (ertesi gün mü, belirli bir bloke süresinden sonra mı) göre değişir. Taksitli satışlarda her taksit için ek komisyon alınır; bu yüzden taksitli satışın maliyeti peşinden belirgin şekilde yüksektir. Komisyonu müşteriye yansıtmak istiyorsanız hesaplayıcıdaki “gereken satış fiyatı” satırı, kesinti sonrası aynı tutarı almanız için fiyatın ne olması gerektiğini gösterir.</p>
<p>Pazaryerinde satış yapıyorsanız komisyon, kargo ve stopajı birlikte hesaplayan <a href="https://hesaplarsin.com/pazaryeri-komisyon-hesaplama.html">pazaryeri komisyon hesaplama</a>, genel satış komisyonu için <a href="https://hesaplarsin.com/komisyon-hesaplama.html">komisyon hesaplama</a> aracını kullanabilirsiniz.</p>''',
faq=[('EFT ücreti ne kadar 2026?', 'Mobil ve internet bankacılığında 2026 üst sınırları: 8.300 ₺’ye kadar 8,37 ₺, 8.300–399.000 ₺ arası 16,76 ₺, 399.000 ₺ üzeri 209,38 ₺. Bankalar daha düşük ücret alabilir.'),
     ('FAST ile en fazla ne kadar gönderilebilir?', '2026’da FAST ile tek seferde en fazla 100.000 ₺ gönderilebilir. Daha yüksek tutarlar EFT ile mesai saatlerinde gönderilir.'),
     ('Havale ile EFT arasındaki fark nedir?', 'Havale aynı bankadaki hesaplar arasında, EFT farklı bankalar arasında yapılan transferdir. Havale genellikle ücretsiz veya EFT’den ucuzdur.'),
     ('POS komisyonu nasıl hesaplanır?', 'Satış tutarı, bankayla anlaştığınız komisyon oranıyla çarpılır. 10.000 ₺’lik peşin satışta %2,5 komisyon 250 ₺ eder; taksitli satışta her taksit için ek oran eklenir.')],
related=['komisyon-hesaplama', 'pazaryeri-komisyon-hesaplama', 'kredi-hesaplama', 'kredi-karti-asgari-odeme-hesaplama', 'doviz-cevirici'],
sources=[('Türkiye Cumhuriyet Merkez Bankası', 'https://www.tcmb.gov.tr/'), ('Gazete Oksijen – 2026 EFT ve havale ücretleri', 'https://gazeteoksijen.com/turkiye/eft-ve-havale-ucretlerine-zam-2026-tarifesi-belli-oldu-261730')],
badges=['✓ Ücretsiz', '2026 Ücret Dilimleri', 'POS Dahil'],
))
