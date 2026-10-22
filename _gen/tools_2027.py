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
