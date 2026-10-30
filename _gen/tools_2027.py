"""2027 sezon araçları. Asgari ücret açıklandığında: RESMI_BRUT doldurulur, başlık/açıklama 'belli oldu' olarak güncellenir.
Kaynak oranlar blog/asgari-ucret-2027.html ile aynıdır (TÜİK, OVP, TCMB Piyasa Katılımcıları Anketi, Eylül 2026).
"""
TOOLS = []

BRUT26 = 33030.00
NET26 = 28075.50
SC = [('2026 zammıyla aynı', 27.0), ('OVP 2026 yıl sonu enflasyon tahmini', 28.4), ('TCMB Piyasa Katılımcıları Anketi (Eylül)', 29.61),
      ('Finansal Kurumlar Birliği tahmini', 30.39), ('Enflasyonun 5 puan üstü', 35.0)]


def tr(x, d=2):
    s = f"{x:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def row(ad, o):
    b = BRUT26 * (1 + o / 100); n = b * 0.85
    return f'<tr><td>{ad}</td><td>%{tr(o)}</td><td>{tr(b)} ₺</td><td>{tr(n)} ₺</td><td>+{tr(n - NET26)} ₺</td><td>{tr(b * 1.2175)} ₺</td></tr>'


TABLO = ('<div class="table-wrap"><table><thead><tr><th>Senaryo</th><th>Artış</th><th>Brüt</th><th>Net</th><th>Net artış</th><th>İşverene maliyet*</th></tr></thead><tbody>'
         + ''.join(row(a, o) for a, o in SC) + '</tbody></table></div>'
         '<p style="font-size:.82rem;color:var(--muted)">*İşveren maliyeti: brüt + %19,75 SGK işveren payı (2 puanlık prim teşvikiyle) + %2 işsizlik sigortası işveren payı. Teşviksiz maliyet için hesaplayıcıdaki seçeneği kullanın.</p>')

OPTS = ''.join(f'<option value="{o}">{a} (%{tr(o)})</option>' for a, o in SC)

FORM = f'''<div class="form-grid">
<div class="field full"><label for="sen">Artış senaryosu</label><select id="sen" onchange="if(this.value!=='x')el('oran').value=String(this.value).replace('.',',')">{OPTS}<option value="x">Kendi oranımı gireceğim</option></select></div>
<div class="field"><label for="oran">Zam oranı (%)</label><input type="number" id="oran" value="27" inputmode="decimal"></div>
<div class="field"><label for="tesvik">İşveren SGK payı</label><select id="tesvik"><option value="19.75" selected>%19,75 (2 puan prim teşvikiyle)</option><option value="21.75">%21,75 (teşviksiz)</option></select></div>
</div>'''

JS = r'''
var B26=33030, N26=28075.50;
function hesapla(){
  var o=v('oran'); if(isNaN(o)||o<0||o>150) return 'Zam oranını 0 ile 150 arasında girin.';
  var r2=function(x){return Math.round(x*100)/100;}, b=r2(B26*(1+o/100)), sgk=r2(b*0.14), iss=r2(b*0.01), n=r2(b-sgk-iss), isv=+el('tesvik').value/100, mal=b*(1+isv+0.02);
  return {main:['2027 net asgari ücret (tahmini)', tl(n)], sub:'%'+num(o,2)+' zamla · brüt '+tl(b)+' · net artış +'+tl(n-N26),
    rows:[['2027 brüt asgari ücret',tl(b),'hl'],['SGK işçi payı (%14)','−'+tl(sgk),'neg'],['İşsizlik sigortası işçi payı (%1)','−'+tl(iss),'neg'],
          ['Gelir ve damga vergisi','0 ₺ (asgari ücret istisnası)'],['2027 net asgari ücret',tl(n),'hl'],
          ['2026’ya göre net artış','+'+tl(n-N26)+' (aylık)'],['Yıllık net artış','+'+tl((n-N26)*12)],
          ['İşverene toplam maliyet',tl(mal)],['Saatlik brüt ücret (225 saat)',tl(b/225)],['Saatlik net ücret',tl(n/225)],
          ['Fazla mesai saat ücreti (brüt, %50 zamlı)',tl(b/225*1.5)],['Günlük brüt ücret',tl(b/30)],
          ['İşsizlik ödeneği üst sınırı (brütün %80’i)',tl(b*0.8)]],
    note:'Tahmindir: 2027 asgari ücreti henüz açıklanmadı. Hesap, asgari ücrete gelir ve damga vergisi istisnasının 2027’de de süreceği varsayımına dayanır. Rakam açıklandığı gün sayfa güncellenecektir.'};
}
function onReady(){ run(false); }
'''

TOOLS.append(dict(
slug='asgari-ucret-2027-hesaplama', name='Asgari Ücret 2027 Hesaplama', cat='maas', ico='📈',
title='Asgari Ücret 2027 Hesaplama – Zamlı Net Maaş Ne Olur? | Hesaplarsın',
desc='Asgari ücret 2027’de %27, %28,4 veya %30 zamla ne kadar olur? Zam oranını seçin; brüt, net, işveren maliyeti ve saatlik ücreti anında görün.',
h1='📈 Asgari Ücret 2027 Zam Hesaplama',
lead='2027 asgari ücreti Aralık 2026’da açıklanacak. Beklenen zam oranlarından birini seçin ya da kendi tahmininizi girin; yeni brüt ve net asgari ücreti, işverene maliyeti, saatlik ve fazla mesai ücretini hemen görün.',
card_title='2027 Asgari Ücret Senaryo Hesaplayıcı', button='Hesapla',
form=FORM, js=JS,
article=f'''<h2 id="senaryolar">2027 asgari ücret senaryoları</h2>
<p>Asgari ücret artışının sabit bir formülü yoktur, ancak Asgari Ücret Tespit Komisyonu kararlarında yıl sonu enflasyon tahmini temel referanstır. Eylül 2026’da yıllık enflasyon %29,73, yılın ilk 9 ayındaki enflasyon %24,32 oldu. Orta Vadeli Program 2026 yıl sonu enflasyonunu %28,4 olarak öngörüyor. Bu verilere göre farklı artış oranlarında 2027 asgari ücreti:</p>
{TABLO}
<p>Kurumların tahminleri %28 ile %30,4 arasında yoğunlaşıyor; bu aralıkta net asgari ücret yaklaşık <strong>36.000–36.600 ₺</strong> olur.</p>
<h2 id="nasil">Net asgari ücret nasıl hesaplanır?</h2>
<p>Brüt asgari ücretten %14 SGK işçi payı ve %1 işsizlik sigortası primi kesilir. Asgari ücrete isabet eden gelir vergisi ve damga vergisi 2022’den beri istisna olduğundan başka kesinti yapılmaz. Bu yüzden net asgari ücret, brütün tam %85’idir: 2026’da 33.030 ₺ brüt → 28.075,50 ₺ net.</p>
<h2 id="ne-zaman">2027 asgari ücreti ne zaman açıklanacak?</h2>
<p>Komisyonun Aralık 2026’nın ilk haftalarında toplanması ve yeni rakamın Aralık sonunda açıklanması bekleniyor. 2026 asgari ücreti 23 Aralık 2025’te açıklanmıştı. Yeni tutar 1 Ocak 2027’den itibaren geçerli olur. Açıklandığı gün bu sayfadaki hesaplayıcı resmî rakamla güncellenecek. Beklentilerin ayrıntısı için <a href="https://hesaplarsin.com/blog/asgari-ucret-2027.html">Asgari Ücret 2027 Ne Kadar Olacak?</a> yazımıza bakabilirsiniz.</p>
<h2 id="etki">Asgari ücretteki artış başka neleri değiştirir?</h2>
<ul><li><strong>İşsizlik maaşı tavanı:</strong> Brüt asgari ücretin %80’i olduğu için asgari ücretle birlikte artar.</li>
<li><strong>Fazla mesai ve saatlik ücret:</strong> Brüt ücretin 225’e bölünmesiyle bulunur; asgari ücretli çalışanın mesai ücreti doğrudan yükselir.</li>
<li><strong>Gelir vergisi istisnası:</strong> Asgari ücretin üzerindeki maaşlarda da asgari ücrete isabet eden vergi kadar indirim uygulandığından, tüm çalışanların net maaşı etkilenir.</li>
<li><strong>SGK prim tabanı ve tavanı:</strong> Prim tabanı brüt asgari ücrete eşittir, tavan da ona bağlı olarak belirlenir; Bağ-Kur ve isteğe bağlı sigorta primleri de buna göre artar.</li></ul>
<p>Mevcut 2026 rakamlarıyla hesap için <a href="https://hesaplarsin.com/asgari-ucret-hesaplama.html">Asgari Ücret 2026 hesaplama</a>, kendi maaşınızın net karşılığı için <a href="https://hesaplarsin.com/net-maas-hesaplama.html">net maaş hesaplama</a> aracını kullanabilirsiniz.</p>''',
faq=[('2027 asgari ücret ne kadar olacak?', 'Henüz açıklanmadı. Kurumların enflasyon tahminlerine göre zam %28–30,4 aralığında beklenirse net asgari ücret yaklaşık 36.000–36.600 ₺ olur. Kesin rakam Aralık 2026 sonunda açıklanacak.'),
     ('Asgari ücret %30 zam alırsa net ne olur?', 'Brüt asgari ücret 33.030 ₺ × 1,30 = 42.939 ₺ olur; %15 işçi kesintisi sonrası net 36.498,15 ₺ eder.'),
     ('2027’de asgari ücrete ara zam yapılacak mı?', 'Son yıllarda ara zam yapılmadı; 2024, 2025 ve 2026’da asgari ücret yılda bir kez belirlendi. Hükümetin enflasyonla mücadele programı nedeniyle 2027’de de yalnızca Ocak zammı yapılması bekleniyor.'),
     ('Asgari ücretin işverene maliyeti ne kadar?', 'İşveren brüt ücretin üzerine %21,75 SGK payı (prim teşvikiyle %19,75) ve %2 işsizlik sigortası payı öder. 2026’da teşvikli maliyet yaklaşık 40.214 ₺’dir.')],
related=['asgari-ucret-hesaplama', 'net-maas-hesaplama', 'issizlik-maasi-hesaplama', 'fazla-mesai-hesaplama', 'maas-siralamasi'],
sources=[('TÜİK – Tüketici Fiyat Endeksi', 'https://data.tuik.gov.tr/'), ('Çalışma ve Sosyal Güvenlik Bakanlığı – Asgari Ücret', 'https://www.csgb.gov.tr/'),
         ('TCMB – Piyasa Katılımcıları Anketi', 'https://www.tcmb.gov.tr/')],
badges=['✓ Ücretsiz', '2027 Senaryoları', 'Anında Sonuç'],
))


# ───────────────────────── KÂR PAYI (katılım hesabı + temettü) ─────────────────────────
def _kp(tutar, oran, gun):
    brut = tutar * oran / 100 * gun / 365
    st = 0.175 if gun <= 182 else 0.15 if gun <= 365 else 0.10
    return brut, st, brut * (1 - st)

_KP_ROWS = ''.join(f'<tr><td>{g} gün</td><td>{tr(_kp(100000, 40, g)[0])} ₺</td><td>%{tr(_kp(100000, 40, g)[1]*100,1)}</td><td>{tr(_kp(100000, 40, g)[2])} ₺</td></tr>' for g in (32, 92, 181, 365))
KP_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Vade</th><th>Brüt kâr payı</th><th>Stopaj</th><th>Net kâr payı</th></tr></thead><tbody>'
            + _KP_ROWS + '</tbody></table></div><p style="font-size:.82rem;color:var(--muted)">100.000 ₺, yıllık %40 tahmini kâr payı oranıyla. Oran örnek amaçlıdır; bankanızın güncel oranını hesaplayıcıya girin.</p>')

KP_FORM = '''<div class="field full" style="margin-bottom:14px"><label>Hesaplama türü</label><div class="seg"><label><input type="radio" name="tur" value="katilim" checked onchange="kpMod()">Katılım hesabı kâr payı</label><label><input type="radio" name="tur" value="temettu" onchange="kpMod()">Hisse temettüsü (kâr payı)</label></div></div>
<div class="form-grid" id="f-katilim">
<div class="field"><label for="tutar">Yatırılan tutar (₺)</label><input type="number" id="tutar" placeholder="örn: 100.000" inputmode="decimal"></div>
<div class="field"><label for="oran">Yıllık kâr payı oranı (%) <small>bankanın ilan ettiği tahmini oran</small></label><input type="number" id="oran" placeholder="örn: 40" inputmode="decimal"></div>
<div class="field"><label for="gun">Vade (gün)</label><input type="number" id="gun" value="32" inputmode="numeric"></div>
</div>
<div class="form-grid" id="f-temettu" style="display:none">
<div class="field"><label for="adet">Hisse adedi</label><input type="number" id="adet" placeholder="örn: 1.000" inputmode="numeric"></div>
<div class="field"><label for="hbt">Hisse başı brüt temettü (₺)</label><input type="number" id="hbt" placeholder="örn: 2,50" inputmode="decimal"></div>
</div>'''

KP_JS = r'''
function kpMod(){var t=radio('tur');el('f-katilim').style.display=t==='katilim'?'':'none';el('f-temettu').style.display=t==='temettu'?'':'none';}
function hesapla(){
  if(radio('tur')==='temettu'){
    var a=v('adet'),h=v('hbt'); if(!(a>0)||!(h>0)) return 'Hisse adedini ve hisse başı brüt temettüyü girin.';
    var br=a*h, st=br*0.15;
    return {main:['Net temettü',tl(br-st)],sub:num(a,0)+' hisse × '+tl(h)+' brüt',rows:[['Brüt temettü',tl(br)],['Stopaj (%15)','−'+tl(st),'neg'],['Net temettü (hesaba geçen)',tl(br-st),'hl'],['Hisse başı net',tl(h*0.85)]],
      note:'Gerçek kişilere dağıtılan kâr payından şirket %15 stopaj keser (22 Aralık 2024’ten itibaren). Brüt temettünün yarısı gelir vergisinden istisnadır; kalan yarısı yıllık beyan sınırını aşarsa Mart ayında beyan edilir ve kesilen stopaj hesaplanan vergiden düşülür.'};
  }
  var T=v('tutar'),o=v('oran'),g=v('gun'); if(!(T>0)) return 'Yatırılan tutarı girin.'; if(!(o>0)||o>200) return 'Yıllık kâr payı oranını girin.'; if(!(g>0)) return 'Vadeyi gün olarak girin.';
  var br=T*o/100*g/365, s=g<=182?0.175:(g<=365?0.15:0.10), st=br*s, net=br-st, ef=net/T*365/g*100;
  return {main:['Net kâr payı (tahmini)',tl(net)],sub:num(g,0)+' gün · %'+num(o,2)+' yıllık oran · vade sonu '+tl(T+net),
    rows:[['Brüt kâr payı',tl(br)],['Stopaj (%'+num(s*100,1)+')','−'+tl(st),'neg'],['Net kâr payı',tl(net),'hl'],['Vade sonu toplam',tl(T+net)],['Günlük net getiri',tl(net/g)],['Yıllık net getiri oranı',('%'+num(ef,2))]],
    note:'Katılım hesabında kâr payı vade başında kesin değildir: banka tahmini bir oran ilan eder, gerçek tutar havuzun vade sonundaki kârına göre belirlenir. Stopaj, 9 Temmuz 2025’ten itibaren açılan/yenilenen TL hesaplar için 6 aya kadar %17,5, 1 yıla kadar %15, 1 yıldan uzun vadede %10’dur.'};
}
'''

TOOLS.append(dict(
slug='kar-payi-hesaplama', name='Kâr Payı Hesaplama', cat='finans', ico='🌙',
title='Kâr Payı Hesaplama 2026 – Katılım Hesabı ve Temettü | Hesaplarsın',
desc='Katılım bankası kâr payını vade ve stopajla, hisse temettüsünü %15 stopajla hesaplayın. 100.000 ₺ 32 günde ne kadar kâr payı getirir? Net tutarı görün.',
h1='🌙 Kâr Payı Hesaplama',
lead='Katılım (faizsiz) hesabınızın vade sonunda getireceği kâr payını ya da hisse senetlerinizden alacağınız temettüyü hesaplayın. Stopaj kesintisi vadeye göre otomatik uygulanır, net tutarı ve vade sonu bakiyenizi görürsünüz.',
card_title='Kâr Payı Hesaplayıcı', button='Hesapla',
form=KP_FORM, js=KP_JS,
article=f'''<h2 id="nasil">Kâr payı nasıl hesaplanır?</h2>
<div class="kisa-cevap" style="border:2px solid #bfdbfe;background:#eff6ff;border-radius:14px;padding:16px 18px;margin:14px 0 22px;line-height:1.65;font-size:.95rem"><p style="margin:0 0 10px"><strong>Kısa cevap:</strong> Brüt kâr payı, yatırılan tutarın yıllık kâr payı oranıyla ve <strong>vade gününün 365’e oranıyla</strong> çarpılmasıyla bulunur. Net kâr payı için brüt tutardan vadeye göre %17,5, %15 veya %10 stopaj düşülür.</p>
<p style="margin:0 0 8px;font-family:ui-monospace,Menlo,Consolas,monospace;background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:8px 10px;font-size:.88rem">Brüt kâr payı = Tutar × Oran ÷ 100 × Gün ÷ 365 · Net = Brüt × (1 − Stopaj)</p>
<p style="margin:0"><strong>Örnek:</strong> 100.000 ₺, %40, 32 gün: 100.000 × 0,40 × 32 ÷ 365 = <strong>{tr(_kp(100000,40,32)[0])} ₺</strong> brüt; %17,5 stopaj sonrası <strong>{tr(_kp(100000,40,32)[2])} ₺</strong> net</p></div>
<h2 id="tablo">100.000 ₺ ne kadar kâr payı getirir?</h2>
{KP_TABLO}
<h2 id="katilim">Katılım hesabı nasıl çalışır?</h2>
<p>Katılım bankaları faiz yerine <strong>kâr ve zarar ortaklığı</strong> esasıyla çalışır. Yatırdığınız para, bankanın ticari faaliyetlerde kullandığı bir havuza girer; vade sonunda havuzun kârı, hesap açılırken belirlenen <strong>kâr paylaşım oranına</strong> göre (örneğin %80 müşteri, %20 banka) dağıtılır. Banka hesap açılırken tahmini bir kâr payı oranı ilan eder, ancak kesin tutar vade sonunda belli olur. Bu yüzden hesaplayıcıdaki sonuç tahmindir.</p>
<p>Katılım hesapları da mevduat gibi Tasarruf Mevduatı Sigorta Fonu (TMSF) güvencesindedir ve aynı stopaj oranlarına tabidir.</p>
<h2 id="stopaj">Kâr payında stopaj oranları (2026)</h2>
<div class="table-wrap"><table><thead><tr><th>Vade</th><th>Stopaj</th></tr></thead><tbody><tr><td>6 aya kadar</td><td>%17,5</td></tr><tr><td>6 ay – 1 yıl</td><td>%15</td></tr><tr><td>1 yıldan uzun</td><td>%10</td></tr></tbody></table></div>
<p>Oranlar 9 Temmuz 2025’ten itibaren açılan veya yenilenen TL hesaplar için geçerlidir; hesabınıza açılış ya da yenileme tarihindeki oran uygulanır.</p>
<h2 id="temettu">Hisse senedi kâr payı (temettü) nasıl hesaplanır?</h2>
<p>Şirketlerin ortaklarına dağıttığı kâr payına <strong>temettü</strong> denir. Brüt temettü, hisse başı brüt tutarın hisse adedinizle çarpılmasıyla bulunur. 22 Aralık 2024’ten itibaren gerçek kişilere ödenen temettüden şirket <strong>%15 stopaj</strong> keser; örneğin 1.000 hisse × 2,50 ₺ = 2.500 ₺ brüt, 375 ₺ stopaj, <strong>2.125 ₺ net</strong>. Brüt temettünün yarısı gelir vergisinden istisnadır; kalan kısım yıllık beyan sınırını aşarsa beyan edilir.</p>
<p>Klasik vadeli mevduatla karşılaştırmak için <a href="https://hesaplarsin.com/mevduat-faizi-hesaplama.html">mevduat faizi hesaplama</a>, birikiminizin enflasyon karşısındaki durumu için <a href="https://hesaplarsin.com/enflasyon-hesaplama.html">enflasyon hesaplama</a> aracını kullanabilirsiniz.</p>''',
faq=[('100.000 TL 32 günde ne kadar kâr payı getirir?', f'Yıllık %40 kâr payı oranıyla brüt {tr(_kp(100000,40,32)[0])} ₺, %17,5 stopaj sonrası yaklaşık {tr(_kp(100000,40,32)[2])} ₺ net getirir. Kendi bankanızın ilan ettiği oranı hesaplayıcıya girerek güncel tutarı görebilirsiniz.'),
     ('Kâr payı ile faiz arasındaki fark nedir?', 'Faiz, hesap açılırken kesinleşen sabit bir getiridir. Kâr payında ise banka tahmini bir oran ilan eder; gerçek getiri, paranın kullanıldığı havuzun vade sonundaki kârına göre belirlenir ve tahminden biraz farklı olabilir.'),
     ('Kâr payından vergi kesilir mi?', 'Evet. Katılım hesabı kâr payından vadeye göre %17,5 (6 aya kadar), %15 (1 yıla kadar) veya %10 (1 yıldan uzun) stopaj kesilir. Hisse temettüsünden ise %15 stopaj kesilir.'),
     ('Katılım hesabı devlet güvencesinde mi?', 'Evet. Katılım bankalarındaki hesaplar, mevduat gibi TMSF sigortası kapsamındadır.')],
related=['mevduat-faizi-hesaplama', 'bilesik-faiz', 'enflasyon-hesaplama', 'para-deger-kaybi-hesaplama', 'kripto-kar-zarar-hesaplama'],
sources=[('Gelir İdaresi Başkanlığı – Stopaj oranları', 'https://www.gib.gov.tr/'), ('Türkiye Katılım Bankaları Birliği', 'https://www.tkbb.org.tr/'), ('TMSF – Sigortalı mevduat ve katılım fonu', 'https://www.tmsf.org.tr/')],
badges=['✓ Ücretsiz', '2026 Stopaj Oranları', 'Temettü Dahil'],
))


# ───────────────────────── EMEKLİ MAAŞI 2026 / OCAK 2027 ─────────────────────────
# Kaynaklar (24 Ekim 2026 kontrol): Ocak 2026 SSK/Bağ-Kur zammı %12,19; Temmuz 2026 SSK/Bağ-Kur zammı %17,76 (Ocak–Haziran 6 aylık TÜFE);
# memur emeklisi Temmuz 2026 %13,52; en düşük emekli aylığı 20.000 → 23.552 ₺ (7590 sayılı Kanun, Temmuz 2026);
# 65 yaş aylığı 7.257 ₺, engelli aylığı 5.793 / 8.690 ₺ (Temmuz 2026); bayram ikramiyesi 4.000 ₺.
# Temmuz–Eylül 2026 TÜFE: %5,57 (memur-emekli-zammi-hesaplama ile aynı). GÜNCELLEME: Q3_26 → Ekim/Kasım verisiyle.
Q3_26 = 5.57
EN_DUSUK = 23552


def _alti(a):
    return ((1 + Q3_26 / 100) * (1 + a / 100) ** 3 - 1) * 100


def _memur(h):
    fark = max(0.0, (1 + h / 100) / 1.07 - 1)
    return (1.05 * (1 + fark) - 1) * 100


EM_TABLO = ('<div class="table-wrap"><table><thead><tr><th>Şu anki aylık</th>'
            + ''.join(f'<th>Ekim–Aralık ayda %{tr(a, 1)} (zam %{tr(_alti(a))})</th>' for a in (0.6, 1.0, 1.4))
            + '</tr></thead><tbody>'
            + ''.join('<tr><td>' + tr(m, 0) + ' ₺</td>' + ''.join(f'<td>{tr(max(m * (1 + _alti(a) / 100), 0), 0)} ₺</td>' for a in (0.6, 1.0, 1.4)) + '</tr>'
                      for m in (23552, 25000, 30000, 35000, 40000, 50000))
            + '</tbody></table></div>')

EM_FORM = '''<div class="form-grid">
<div class="field"><label for="tur">Emeklilik türü</label><select id="tur"><option value="ssk">SSK emeklisi (4A)</option><option value="bagkur">Bağ-Kur emeklisi (4B)</option><option value="memur">Memur emeklisi (4C, Emekli Sandığı)</option></select></div>
<div class="field"><label for="maas">Şu an aldığınız aylık (₺)</label><input type="number" id="maas" placeholder="örn: 30.000" inputmode="decimal"></div>
<div class="field"><label for="aylik">Ekim–Aralık aylık ortalama enflasyon tahmini (%)</label><input type="number" id="aylik" value="1" inputmode="decimal"></div>
<div class="field full"><label class="chk"><input type="checkbox" id="taban"> En düşük emekli aylığını (23.552 ₺) alıyorum</label></div>
</div>'''

EM_JS = r'''
var Q3=0.0557, EN_DUSUK=23552;
function hesapla(){
  var tur=el('tur').value, taban=checked('taban'), m=taban?EN_DUSUK:v('maas');
  if(!(m>0)) return 'Şu an aldığınız aylığı girin.';
  var a=v('aylik'); if(isNaN(a)) a=1; if(a<-2||a>10) return 'Aylık enflasyon tahmini −2 ile 10 arasında olmalı.';
  var h=(1+Q3)*Math.pow(1+a/100,3)-1, z;
  if(tur==='memur'){ var fark=Math.max(0,(1+h)/1.07-1); z=1.05*(1+fark)-1; } else { z=h; }
  var y=m*(1+z), rows=[['Temmuz–Aralık 2026 enflasyonu (tahmini)',pct(h*100)],['Ocak 2027 zam oranı (tahmini)',pct(z*100),'hl'],
    ['Zam yöntemi',tur==='memur'?'%5 toplu sözleşme + enflasyon farkı':'6 aylık TÜFE artışı kadar'],['Aylık artış',tl(y-m)],['Ocak–Haziran 2027 toplam ek gelir',tl((y-m)*6)],
    ['Bayram ikramiyesi (2026)','4.000 ₺ (her bayram)']];
  var note='Temmuz–Eylül 2026 enflasyonu %5,57 olarak gerçekleşti; kalan aylar sizin tahmininizle hesaplandı. Kesin oran Aralık enflasyonunun açıklandığı Ocak 2027’nin ilk günlerinde belli olur.';
  if(tur!=='memur' && (taban || m<=EN_DUSUK)){
    note='En düşük aylık alanlarda zam, kanunla belirlenen tabana değil kök aylığa uygulanır. Ocak 2027’de taban için yeni bir yasal düzenleme yapılmazsa aylığınız 23.552 ₺ kalabilir; taban zam oranında artırılırsa '+tl(EN_DUSUK*(1+z))+' olur. '+note;
    rows=[rows[0],rows[1],['Taban sabit kalırsa',tl(EN_DUSUK)],['Taban zam oranında artırılırsa',tl(EN_DUSUK*(1+z))],rows[5]];
    return {main:['Ocak 2027 tahmini aylık', tl(EN_DUSUK)+' – '+tl(EN_DUSUK*(1+z))], sub:'Yasal düzenlemeye bağlı', rows:rows, note:note};
  }
  return {main:['Ocak 2027 tahmini aylık', tl(y)], sub:'%'+num(z*100,2)+' zam ile', rows:rows, note:note};
}
function onReady(){ el('taban').addEventListener('change',function(){ el('maas').disabled=this.checked; if(this.checked) el('maas').value=''; }); }
'''

TOOLS.append(dict(
slug='emekli-maasi-hesaplama', name='Emekli Maaşı Hesaplama 2026', cat='maas', ico='👴',
title='Emekli Maaşı Hesaplama 2026 – Ocak 2027 Zammı, En Düşük Aylık | Hesaplarsın',
desc='En düşük emekli maaşı 23.552 ₺. SSK, Bağ-Kur ve memur emeklisi için Ocak 2027 zamlı maaşınızı hesaplayın; 65 yaş aylığı ve bayram ikramiyesi tutarları.',
h1='👴 Emekli Maaşı Hesaplama 2026',
lead='Şu an aldığınız emekli aylığını ve emeklilik türünüzü girin; Ocak 2027 zammıyla yeni aylığınızı tahmin edin. 2026’da kesinleşen zam oranları, en düşük emekli maaşı, 65 yaş aylığı ve bayram ikramiyesi tutarları aşağıda.',
card_title='Emekli Maaşı ve Ocak 2027 Zam Hesaplayıcı', button='Hesapla',
form=EM_FORM, js=EM_JS,
article=f'''<h2 id="2026-rakamlar">2026’da emekli maaşları: kesinleşen rakamlar</h2>
<div class="table-wrap"><table><thead><tr><th>Kalem</th><th>Tutar / oran</th></tr></thead><tbody>
<tr><td>Ocak 2026 SSK ve Bağ-Kur emekli zammı</td><td>%12,19</td></tr>
<tr><td>Temmuz 2026 SSK ve Bağ-Kur emekli zammı</td><td>%17,76</td></tr>
<tr><td>Temmuz 2026 memur emeklisi zammı</td><td>%13,52</td></tr>
<tr><td>En düşük emekli aylığı (Ocak–Haziran 2026)</td><td>20.000 ₺</td></tr>
<tr><td><b>En düşük emekli aylığı (Temmuz 2026’dan itibaren)</b></td><td><b>23.552 ₺</b></td></tr>
<tr><td>Emekli bayram ikramiyesi (2026, her bayram)</td><td>4.000 ₺</td></tr>
<tr><td>65 yaş (yaşlılık) aylığı – Temmuz 2026</td><td>7.257 ₺</td></tr>
<tr><td>Engelli aylığı – %40–69 / %70 ve üzeri (Temmuz 2026)</td><td>5.793 ₺ / 8.690 ₺</td></tr>
</tbody></table></div>
<p>En düşük emekli aylığı Temmuz 2026’da 7590 sayılı Kanun’la 20.000 ₺’den 23.552 ₺’ye yükseltildi. Kanun Temmuz ödemelerinden sonra yürürlüğe girdiği için aradaki <b>3.552 ₺ fark</b> en düşük aylık alan emeklilere sonradan, ayrı bir ödemeyle verildi. 65 yaş ve engelli aylıkları memur maaş katsayısına bağlı olduğundan memur zammıyla aynı dönemlerde artar.</p>

<h2 id="ocak-2027">Ocak 2027 emekli zammı ne kadar olacak?</h2>
<p>SSK (4A) ve Bağ-Kur (4B) emeklileri Ocak’ta, Temmuz–Aralık dönemindeki <b>altı aylık TÜFE artışı</b> kadar zam alır. Temmuz–Eylül 2026 enflasyonu %5,57 olarak gerçekleşti. Memur emeklileri (4C) ise 2027’nin ilk yarısı için toplu sözleşmedeki %5 zamla birlikte, altı aylık enflasyonun %7’yi aşan kısmı kadar enflasyon farkı alır.</p>
<div class="formula">SSK / Bağ-Kur zammı = 1,0557 × (1 + Ekim) × (1 + Kasım) × (1 + Aralık) − 1</div>
<p>Ekim–Aralık için farklı aylık enflasyon varsayımlarıyla SSK ve Bağ-Kur emeklilerinin Ocak 2027 tahmini aylıkları:</p>
{EM_TABLO}
<p style="font-size:.85rem;color:var(--muted)">23.552 ₺ satırı, kök aylığı tabana eşit olan emekliler içindir. Kök aylığı daha düşük olup taban tamamlamasıyla 23.552 ₺ alanlarda Ocak 2027 tutarı yasal düzenlemeye bağlıdır.</p>
<p>Aynı senaryolarda memur emeklisi zammı sırasıyla yaklaşık %{tr(_memur(_alti(0.6)))}, %{tr(_memur(_alti(1.0)))} ve %{tr(_memur(_alti(1.4)))} olur. Memur ve memur emeklisi için ayrıntılı hesap: <a href="https://hesaplarsin.com/memur-emekli-zammi-hesaplama.html">memur ve emekli zammı hesaplama</a>.</p>

<h2 id="en-dusuk">En düşük emekli maaşı nasıl belirlenir?</h2>
<p>En düşük emekli aylığı bir zam oranı değil, <b>kanunla belirlenen bir tabandır</b>. Kök aylığı bu tutarın altında kalan emeklilere aradaki fark Hazine tarafından tamamlanır. Bu nedenle Ocak zammı kök aylığa uygulanır; zamlı kök aylık hâlâ tabanın altında kalıyorsa emekli, yeni bir yasal düzenleme yapılana kadar taban tutarı almaya devam eder. Son yıllarda taban her zam döneminde ayrı bir kanunla yükseltildi.</p>

<h2 id="ogrenme">Emekli maaşımı nereden öğrenirim?</h2>
<ul>
<li><b>e-Devlet:</b> “SGK Emekli Aylık Bilgisi” hizmetinde aylık tutarınızı ve kesintileri görebilirsiniz.</li>
<li><b>Banka:</b> Aylığın yattığı hesabın dökümünde net ödeme görünür; ancak promosyon ve diğer yatırımlar karışabilir.</li>
<li><b>Kök aylık:</b> En düşük aylık alıyorsanız e-Devlet’teki ayrıntılarda “aylık tutarı” ile ödenen tutar arasındaki fark, Hazine’nin tamamladığı kısımdır.</li>
</ul>
<p>Henüz emekli olmadıysanız ne zaman emekli olacağınızı <a href="https://hesaplarsin.com/emeklilik-yasi-hesaplama.html">emeklilik yaşı hesaplama</a> aracıyla bulabilirsiniz.</p>''',
faq=[('En düşük emekli maaşı 2026’da ne kadar?', 'Temmuz 2026’dan itibaren en düşük emekli aylığı 23.552 ₺’dir. Ocak–Haziran 2026 döneminde 20.000 ₺ idi.'),
     ('2026 Temmuz emekli zammı yüzde kaç oldu?', 'SSK ve Bağ-Kur emeklileri Ocak–Haziran 2026 enflasyonu kadar %17,76, memur emeklileri %13,52 zam aldı. Ocak 2026’da SSK ve Bağ-Kur zammı %12,19 idi.'),
     ('Ocak 2027 emekli zammı ne kadar olacak?', 'Temmuz–Eylül enflasyonu %5,57 gerçekleşti. Ekim–Aralık’ta aylık ortalama %1 enflasyonla SSK ve Bağ-Kur emeklilerinin zammı yaklaşık %' + tr(_alti(1.0)) + ' olur. Kesin oran Ocak 2027’nin ilk günlerinde belli olacak.'),
     ('65 yaş aylığı ne kadar?', 'Temmuz 2026’dan itibaren 65 yaş (yaşlılık) aylığı 7.257 ₺’dir. Bu aylık memur maaş katsayısına bağlı olduğundan Ocak 2027’de memur zammı oranında artar.'),
     ('Emekli bayram ikramiyesi ne kadar?', '2026’da emeklilere Ramazan ve Kurban bayramlarında ayrı ayrı 4.000 ₺ bayram ikramiyesi ödendi.')],
related=['memur-emekli-zammi-hesaplama', 'emeklilik-yasi-hesaplama', 'enflasyon-hesaplama', 'asgari-ucret-2027-hesaplama', 'maas-zam-hesaplama'],
sources=[('SGK – Emekli aylıkları', 'https://www.sgk.gov.tr/'), ('TÜİK – Tüketici Fiyat Endeksi', 'https://data.tuik.gov.tr/'),
         ('Resmî Gazete – 7590 sayılı Kanun (en düşük aylık)', 'https://www.resmigazete.gov.tr/'), ('Aile ve Sosyal Hizmetler Bakanlığı – 2022 sayılı Kanun aylıkları', 'https://www.aile.gov.tr/')],
badges=['✓ Ücretsiz', 'Ocak 2027 Tahmini', 'SSK · Bağ-Kur · Memur'],
))
