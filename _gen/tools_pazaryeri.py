"""Pazaryeri komisyon / net kâr hesaplayıcıları: genel (çok platform) + Trendyol, Hepsiburada, Shopier.
Oranlar kategoriye ve satıcı anlaşmasına göre değişir; burada 2026 için yaygın kaynaklardaki yaklaşık
orta değerler kullanılır, kullanıcı oranı her zaman değiştirebilir. GÜNCELLEME: P sözlüğü ve makale tabloları.
Son kontrol: 22 Ekim 2026.
"""
import json
TOOLS = []

# platform -> (görünen ad, sabit hizmet bedeli KDV hariç, kategori listesi [(ad, oran, ürün KDV oranı — yoksa %20)])
P = {
 'trendyol': ('Trendyol', 8.49, [
    ('Giyim, ayakkabı, çanta', 21.5, 10), ('Takı, saat, aksesuar', 22.5), ('Ev tekstili, mobilya, züccaciye', 21.0),
    ('Kozmetik ve kişisel bakım', 18.5), ('Parfüm', 18.0), ('Spor ve outdoor', 17.0), ('Küçük ev aletleri', 16.0),
    ('Kitap ve kırtasiye', 13.5, 10), ('Süpermarket / gıda', 12.5), ('Beyaz eşya', 10.0), ('Bilgisayar ve tablet', 8.5),
    ('Televizyon', 7.5), ('Cep telefonu', 5.5), ('Telefon yedek parça / aksesuar', 26.0)]),
 'hepsiburada': ('Hepsiburada', 10.99, [
    ('Giyim, çanta', 18.0, 10), ('Ev tekstili, züccaciye', 18.0), ('Ayakkabı', 19.49, 10), ('Mobilya', 20.0), ('Kozmetik, parfüm, cilt bakım', 17.0),
    ('Yapı market / hırdavat', 17.0), ('Telefon aksesuarı', 20.0), ('Pet shop', 15.5), ('Ev bakım ürünleri', 15.0),
    ('Anne-bebek', 14.5), ('Bilgisayar', 12.0), ('Oyun konsolu', 10.5), ('Televizyon', 8.34), ('Cep telefonu', 7.75)]),
 'shopier': ('Shopier', 0.49, [
    ('Aylık satış 15.000 ₺ altı / yeni satıcı', 5.99), ('15.000 – 59.999 ₺', 5.49), ('60.000 – 149.999 ₺', 4.99),
    ('150.000 – 299.999 ₺', 4.49), ('300.000 – 749.999 ₺', 3.99), ('750.000 – 1.499.999 ₺', 3.49), ('1.500.000 ₺ ve üzeri', 2.99)]),
 'diger': ('Diğer (kendi oranım)', 0.0, [('Kendi komisyon oranımı gireceğim', 15.0)]),
}

JS_DATA = 'var PZ=' + json.dumps({k: {'ad': a, 'h': h, 'k': [[x[0], x[1], (x[2] if len(x) > 2 else 20)] for x in ks]} for k, (a, h, ks) in P.items()}, ensure_ascii=False) + ';'

JS = JS_DATA + r'''
function pzKat(ilk){var p=el('platform').value,d=PZ[p],s=el('kategori');s.innerHTML='';
  d.k.forEach(function(x,i){var o=document.createElement('option');o.value=i;o.textContent=x[0]+' (%'+num(x[1],2)+')';s.appendChild(o);});
  el('l-kategori').textContent=p==='shopier'?'Aylık toplam satışınız':'Kategori';
  pzOran();el('hizmet').value=String(d.h).replace('.',',');}
function pzOran(){var p=el('platform').value,i=+el('kategori').value||0,x=PZ[p].k[i];el('oran').value=String(x[1]).replace('.',',');if(p!=='shopier'&&p!=='diger')el('kdv').value=String(x[2]);}
function hesapla(){
  var p=el('platform').value,d=PZ[p],F=v('fiyat'),M=v('maliyet')||0,r=v('oran'),H=v('hizmet')||0,K=v('kargo')||0;
  var kdv=+el('kdv').value/100, mat=el('matrah').value, muk=!el('muaf').checked, st=el('stopaj').checked?0.01:0;
  if(!(F>0)) return 'Satış fiyatını (KDV dahil) girin.'; if(!(r>=0)||r>60) return 'Komisyon oranını kontrol edin (0–60).';
  var Fh=F/(1+kdv), C=(mat==='haric'?Fh:F)*r/100, Ck=C*0.2, Hk=H*0.2, Kk=K*0.2, S=Fh*st;
  var kesinti=C+Ck+H+Hk+K+Kk+S, yatan=F-kesinti;
  var net, oKdv=0;
  if(muk){ oKdv=F-Fh-(M-M/(1+kdv))-Ck-Hk-Kk; net=Fh-M/(1+kdv)-C-H-K; }
  else { net=F-M-C-Ck-H-Hk-K-Kk; }
  var marj=net/F*100, top=(C+Ck+H+Hk+K+Kk)/F*100;
  var rows=[['Satış fiyatı (KDV dahil)',tl(F)],['Komisyon (%'+num(r,2)+', '+(mat==='haric'?'KDV hariç':'KDV dahil')+' fiyat üzerinden)','−'+tl(C),'neg'],['Komisyonun KDV’si (%20)','−'+tl(Ck),'neg']];
  if(H>0) rows.push([(p==='shopier'?'Sabit işlem ücreti':'Platform hizmet bedeli')+' (KDV dahil)','−'+tl(H+Hk),'neg']);
  if(K>0) rows.push(['Kargo (KDV dahil)','−'+tl(K+Kk),'neg']);
  if(S>0) rows.push(['E-ticaret stopajı (%1, vergiden mahsup edilir)','−'+tl(S),'neg']);
  rows.push(['Hesabınıza yatan tutar',tl(yatan),'hl']);
  if(M>0) rows.push(['Ürün maliyeti (KDV dahil)','−'+tl(M),'neg']);
  if(muk) rows.push(oKdv>=0?['Bu satıştan ödenecek KDV (yaklaşık)','−'+tl(oKdv),'neg']:['İndirilecek KDV fazlası (devreden KDV)','+'+tl(-oKdv)]);
  rows.push(['Pazaryeri kesintilerinin satışa oranı','%'+num(top,1)]);
  return {main:['Net kârınız',tl(net)],sub:'Kâr marjı %'+num(marj,1)+' · '+d.ad+' · hesabınıza yatan '+tl(yatan),rows:rows,
    note:(muk?'KDV mükellefi varsayımıyla: ödediğiniz KDV’ler (komisyon, kargo, maliyet) indirilir; net kâr KDV hariç tutarlardan hesaplanır. ':'KDV mükellefi değilsiniz: ödediğiniz KDV’ler maliyet sayılır. ')+
      (S>0?'Stopaj, yıllık gelir/kurumlar vergisinden mahsup edildiği için kâra gider olarak yazılmadı. ':'')+
      'Oranlar kategoriye ve satıcı anlaşmasına göre değişir; kesin oranı satıcı panelinizden kontrol edin. Gelir vergisi bu hesaba dahil değildir.'};
}
function onReady(){pzKat(true);}
'''


def form(platform, lock=False):
    opts = ''.join(f'<option value="{k}"{" selected" if k == platform else ""}>{a}</option>' for k, (a, h, ks) in P.items())
    plat = (f'<input type="hidden" id="platform" value="{platform}">' if lock else
            f'<div class="field full"><label for="platform">Pazaryeri / Platform</label><select id="platform" onchange="pzKat()">{opts}</select></div>')
    return plat + '''
<div class="field full"><label for="kategori" id="l-kategori">Kategori</label><select id="kategori" onchange="pzOran()"></select></div>
<div class="form-grid">
<div class="field"><label for="fiyat">Satış Fiyatı (₺) <small>KDV dahil, müşterinin ödediği</small></label><input type="number" id="fiyat" placeholder="örn: 600" inputmode="decimal"></div>
<div class="field"><label for="maliyet">Ürün Maliyeti (₺) <small>KDV dahil alış</small></label><input type="number" id="maliyet" placeholder="örn: 250" inputmode="decimal"></div>
<div class="field"><label for="oran">Komisyon Oranı (%) <small>panelinizdeki oranı yazabilirsiniz</small></label><input type="number" id="oran" inputmode="decimal"></div>
<div class="field"><label for="kargo">Kargo (₺, KDV hariç) <small>siz ödüyorsanız</small></label><input type="number" id="kargo" placeholder="örn: 70" inputmode="decimal"></div>
<div class="field"><label for="hizmet">Sabit Hizmet / İşlem Bedeli (₺, KDV hariç)</label><input type="number" id="hizmet" inputmode="decimal"></div>
<div class="field"><label for="kdv">Ürünün KDV Oranı</label><select id="kdv"><option value="20" selected>%20</option><option value="10">%10</option><option value="1">%1</option><option value="0">%0</option></select></div>
<div class="field full"><label for="matrah">Komisyon matrahı</label><select id="matrah"><option value="dahil" selected>KDV dahil satış fiyatı (yaygın uygulama)</option><option value="haric">KDV hariç satış fiyatı</option></select></div>
<div class="field full"><label class="chk"><input type="checkbox" id="stopaj" checked> %1 e-ticaret stopajını düş</label>
<label class="chk"><input type="checkbox" id="muaf"> KDV mükellefi değilim (esnaf muaflığı vb.)</label></div>
</div>'''


def tablo(platform):
    a, h, ks = P[platform]
    head = 'Aylık satış' if platform == 'shopier' else 'Kategori'
    rows = ''.join(f'<tr><td>{x[0]}</td><td>%{str(x[1]).replace(".", ",")}</td></tr>' for x in ks)
    return f'<div style="overflow-x:auto"><table class="veri-tablo"><thead><tr><th>{head}</th><th>Komisyon (yaklaşık)</th></tr></thead><tbody>{rows}</tbody></table></div>'


def tr(x, d=2):
    s = f"{x:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def ornek(F, M, r, H, K, kdv=0.20, mat='dahil', st=0.01):
    """JS ile aynı formül: (komisyon, kesintiler, hesaba yatan, net kâr, ödenecek KDV)."""
    Fh = F / (1 + kdv); C = (Fh if mat == 'haric' else F) * r / 100
    S = Fh * st; yatan = F - C * 1.2 - H * 1.2 - K * 1.2 - S
    net = Fh - M / (1 + kdv) - C - H - K
    okdv = F - Fh - (M - M / (1 + kdv)) - C * .2 - H * .2 - K * .2
    return C, yatan, net, okdv, S


SOURCES = [('Trendyol Satıcı Merkezi', 'https://partner.trendyol.com/'),
           ('Hepsiburada İş Ortağım', 'https://merchant.hepsiburada.com/'),
           ('Shopier', 'https://www.shopier.com/'),
           ('Kurumlar Vergisi Kanunu md. 15 / Gelir Vergisi Kanunu md. 94 (e-ticaret stopajı)', 'https://www.gib.gov.tr/')]

STOPAJ_P = ('<p><strong>E-ticaret stopajı:</strong> 1 Ocak 2025’ten bu yana pazaryerleri ve aracı ödeme kuruluşları, satıcıya yaptıkları ödemelerden '
            '<strong>KDV hariç satış tutarının %1’i</strong> oranında vergi kesintisi yapar. Bu kesinti kayıp değildir: yıl sonunda ödeyeceğiniz gelir veya '
            'kurumlar vergisinden düşülür (mahsup edilir). Hesaplayıcı bu yüzden stopajı hesabınıza yatan tutardan düşer ama net kârı hesaplarken gider saymaz.</p>')

KDV_P = ('<p><strong>KDV nasıl işler?</strong> Müşterinin ödediği fiyat KDV dahildir. Pazaryeri komisyonu, hizmet bedeli ve kargo faturalarına ayrıca %20 KDV ekler. '
         'KDV mükellefiyseniz bu KDV’leri ve ürünü alırken ödediğiniz KDV’yi, satıştan doğan KDV’den indirirsiniz; aradaki fark devlete ödenir. '
         'Bu yüzden gerçek kârınız KDV hariç tutarlar üzerinden bulunur. Ürününüzün KDV oranını doğru seçin: hazır giyim, ayakkabı ve çanta %10, temel gıda %1, elektronik, kozmetik ve çoğu ürün %20’dir. Esnaf muaflığındaysanız veya KDV mükellefi değilseniz “KDV mükellefi değilim” kutusunu işaretleyin: '
         'ödediğiniz KDV’ler o zaman maliyetinize eklenir.</p>')

# ───────────────────────── ÖRNEKLER (makalelerdeki rakamlar formülden üretilir) ─────────────────────────
tC, tY, tN, tK, tS = ornek(600, 250, 21.5, 8.49, 70, kdv=0.10)
hC, hY, hN, hK, hS = ornek(600, 250, 18.0, 10.99, 70, kdv=0.10)
sC, sY, sN, sK, sS = ornek(600, 250, 5.99, 0.49, 70, kdv=0.10)


def ornek_tablo(ad, F, M, r, H, K):
    C, Y, N, OK, S = ornek(F, M, r, H, K, kdv=0.10)
    rows = [('Satış fiyatı (KDV dahil)', tr(F) + ' ₺'), (f'Komisyon %{tr(r)}', '−' + tr(C) + ' ₺'), ('Komisyonun KDV’si', '−' + tr(C * .2) + ' ₺'),
            ('Hizmet / işlem bedeli (KDV dahil)', '−' + tr(H * 1.2) + ' ₺'), ('Kargo (KDV dahil)', '−' + tr(K * 1.2) + ' ₺'),
            ('E-ticaret stopajı %1', '−' + tr(S) + ' ₺'), ('<strong>Hesaba yatan</strong>', '<strong>' + tr(Y) + ' ₺</strong>'),
            ('Ürün maliyeti (KDV dahil)', '−' + tr(M) + ' ₺'), (('Ödenecek KDV (yaklaşık)', '−' + tr(OK) + ' ₺') if OK >= 0 else ('İndirilecek KDV fazlası (sonraki aya devreder)', '+' + tr(-OK) + ' ₺')),
            ('Stopaj iadesi (vergiden mahsup)', '+' + tr(S) + ' ₺'), ('<strong>Net kâr</strong>', '<strong>' + tr(N) + ' ₺</strong>')]
    b = ''.join(f'<tr><td>{a}</td><td>{x}</td></tr>' for a, x in rows)
    return f'<div style="overflow-x:auto"><table class="veri-tablo" aria-label="{ad} örnek hesap"><thead><tr><th>{ad} · 600 ₺’lik satış</th><th>Tutar</th></tr></thead><tbody>{b}</tbody></table></div>'


# karşılaştırma: aynı ürün, üç platform
KARS = [(n, *ornek(600, 250, r, h, 70, kdv=0.10)) for n, r, h in [('Trendyol (giyim %21,5)', 21.5, 8.49), ('Hepsiburada (giyim %18)', 18.0, 10.99), ('Shopier (%5,99, kendi kargonuz)', 5.99, 0.49)]]
KARS_T = '<div style="overflow-x:auto"><table class="veri-tablo" aria-label="Platform karşılaştırma"><thead><tr><th>Platform</th><th>Komisyon</th><th>Hesaba yatan</th><th>Net kâr</th></tr></thead><tbody>' + ''.join(
    f'<tr><td>{n}</td><td>{tr(C)} ₺</td><td>{tr(Y)} ₺</td><td>{tr(N)} ₺</td></tr>' for n, C, Y, N, OK, S in KARS) + '</tbody></table></div>'

COMMON_FAQ = [
    ('E-ticaret stopajı nedir, kârımdan mı gidiyor?', 'Pazaryerleri 2025’ten beri satıcıya yapılan ödemelerden KDV hariç satış tutarının %1’i kadar vergi keser. Bu tutar yıl sonunda ödeyeceğiniz gelir veya kurumlar vergisinden düşülür; yani kalıcı bir kayıp değil, peşin ödenmiş vergidir.'),
    ('Komisyon KDV dahil fiyattan mı, KDV hariç fiyattan mı hesaplanır?', 'Pazaryerlerinin çoğu komisyon oranını KDV dahil satış fiyatına uygular ve komisyon faturasına ayrıca %20 KDV ekler. Bazı anlaşmalarda matrah farklı olabilir; hesaplayıcıda “Komisyon matrahı” seçeneğiyle iki yöntemi de deneyebilirsiniz.'),
    ('Hesaplamadaki oranlar kesin mi?', 'Hayır. Komisyon oranı alt kategoriye, markaya, kampanyaya ve satıcı anlaşmasına göre değişir. Tablodaki oranlar 2026 için yaygın değerlerin yaklaşık ortasıdır. Kesin oranınızı satıcı panelinizden görüp “Komisyon Oranı” alanına yazın.'),
]

LEAD_SUFFIX = ' Komisyon, komisyonun KDV’si, hizmet bedeli, kargo ve %1 e-ticaret stopajı düşülür; hesabınıza yatan tutarı ve gerçek net kârınızı görürsünüz.'

# ───────────────────────── GENEL ─────────────────────────
TOOLS.append(dict(
slug='pazaryeri-komisyon-hesaplama', name='Pazaryeri Komisyon Hesaplama', cat='isletme', ico='🛒',
title='Pazaryeri Komisyon Hesaplama 2026 – Trendyol, Hepsiburada, Shopier | Hesaplarsın',
desc='Trendyol, Hepsiburada, Shopier’de satıştan elinize ne kalır? Komisyon, KDV, hizmet bedeli, kargo ve %1 stopaj düşülür; net kârınızı görün.',
h1='🛒 Pazaryeri Komisyon ve Net Kâr Hesaplama',
lead='Platformu, kategoriyi ve satış fiyatını seçin.' + LEAD_SUFFIX,
card_title='Pazaryeri Net Kâr Hesaplayıcı', button='Net Kârımı Hesapla',
form=form('trendyol'), js=JS,
article=f'''<h2 id="nasil">Pazaryerinde bir satıştan ne kadar kazanırım?</h2>
<p>Pazaryerinde satış fiyatının tamamı size kalmaz. Müşterinin ödediği tutardan sırasıyla <strong>komisyon</strong>, komisyonun <strong>%20 KDV’si</strong>, platformun sabit <strong>hizmet bedeli</strong>, <strong>kargo</strong> ve <strong>%1 e-ticaret stopajı</strong> düşülür; kalan tutar hesabınıza yatar. Gerçek kârı bulmak için bundan ürün maliyetinizi ve devlete ödeyeceğiniz KDV farkını da çıkarmanız gerekir.</p>
<h2 id="karsilastirma">Aynı ürün üç platformda: hangisi daha kârlı?</h2>
<p>KDV dahil 600 ₺’ye satılan, maliyeti 250 ₺ olan, kargosu 70 ₺ + KDV tutan bir giyim ürünü (ürün KDV’si %10) için yaklaşık hesap:</p>
{KARS_T}
<p>Shopier’de komisyon çok daha düşüktür, ama trafiği siz getirirsiniz: Instagram, WhatsApp veya kendi reklamınız olmadan satış gelmez. Trendyol ve Hepsiburada ise yüksek komisyon karşılığında hazır müşteri sunar. Karar verirken komisyonun yanında reklam harcamanızı da hesaba katın.</p>
<h2 id="kesintiler">Kesinti kalemleri</h2>
<ul><li><strong>Komisyon:</strong> Kategoriye göre genellikle %5 ile %26 arasında. Elektronikte düşük, giyim ve aksesuarda yüksektir.</li>
<li><strong>Hizmet / işlem bedeli:</strong> Sipariş veya gönderi başına sabit ücret. 2026’da Trendyol’da yaklaşık 8,49 ₺ + KDV, Hepsiburada’da 10,99 ₺ + KDV (21 Eylül 2026’dan itibaren), Shopier’de işlem başına 0,49 ₺.</li>
<li><strong>Kargo:</strong> Çoğu pazaryerinde satıcı öder. Düşük tutarlı siparişlerde “barem” denen sabit, indirimli kargo ücretleri uygulanır.</li>
<li><strong>E-ticaret stopajı:</strong> KDV hariç satışın %1’i.</li></ul>
{STOPAJ_P}
{KDV_P}
<h2 id="dusur">Komisyon yükünü azaltmanın yolları</h2>
<ul><li>Satış fiyatını belirlerken önce maliyet + kargo + hedef kâr toplamını çıkarın, sonra komisyon ve KDV’yi üstüne ekleyin. Komisyonu sonradan “yemek” kârı eritir.</li>
<li>Düşük fiyatlı ürünlerde kargo ve sabit hizmet bedeli kârın büyük kısmını alır; ürünleri set halinde satmak sipariş başı sabit giderleri böler.</li>
<li>Platformların kampanya dönemlerinde komisyon indirimleri olur; satıcı panelindeki duyuruları takip edin.</li>
<li>Kendi kitleniz varsa Shopier veya kendi sitenizle düşük komisyonlu kanal açmak ortalama kârınızı yükseltir.</li></ul>
<p>Genel satış komisyonu (emlak, satış temsilcisi, prim) için <a href="https://hesaplarsin.com/komisyon-hesaplama.html">komisyon hesaplama</a>, kâr marjı ve fiyatlama için <a href="https://hesaplarsin.com/kar-marji-hesaplama.html">kâr marjı hesaplama</a> aracını kullanabilirsiniz.</p>''',
faq=[('Trendyol mu Hepsiburada mı daha az komisyon alıyor?', 'Kategoriye göre değişir. Giyimde Hepsiburada’nın oranı (yaklaşık %18) Trendyol’dan (yaklaşık %21,5) düşüktür; elektronikte iki platform birbirine yakındır. Sabit hizmet bedeli ve kargo da sonucu değiştirdiği için ürününüzle iki platformu hesaplayıcıda karşılaştırın.'),
     ('Pazaryerinde net kâr nasıl hesaplanır?', 'Net kâr = KDV hariç satış tutarı − KDV hariç ürün maliyeti − komisyon − hizmet bedeli − kargo (hepsi KDV hariç). KDV mükellefi değilseniz KDV’ler de maliyete eklenir. Stopaj vergiden mahsup edildiği için kâra gider olarak yazılmaz.'),
     ('Hesabıma yatan para neden net kârımdan farklı?', 'Hesaba yatan tutar, ürün maliyetini ve devlete ödeyeceğiniz KDV’yi içermez. Bu paradan ürünün alış bedelini ve aylık KDV beyannamesindeki farkı ödedikten sonra kalan tutar net kârınızdır.')] + COMMON_FAQ,
related=['trendyol-komisyon-hesaplama', 'hepsiburada-komisyon-hesaplama', 'shopier-komisyon-hesaplama', 'komisyon-hesaplama', 'kar-marji-hesaplama'],
sources=SOURCES,
badges=['✓ Ücretsiz', '2026 Oranları', 'Stopaj Dahil'],
))

# ───────────────────────── TRENDYOL ─────────────────────────
TOOLS.append(dict(
slug='trendyol-komisyon-hesaplama', name='Trendyol Komisyon Hesaplama', cat='isletme', ico='🟠',
title='Trendyol Komisyon Hesaplama 2026 – Net Kâr ve Kategori Oranları | Hesaplarsın',
desc='Trendyol’da satıştan elinize ne kalır? Kategori komisyonu, KDV, hizmet bedeli, kargo ve %1 stopajı düşerek hesaba yatan tutarı ve net kârı hesaplayın.',
h1='🟠 Trendyol Komisyon Hesaplama',
lead='Kategorinizi ve satış fiyatınızı girin.' + LEAD_SUFFIX,
card_title='Trendyol Net Kâr Hesaplayıcı', button='Hesapla',
form=form('trendyol', lock=True), js=JS,
article=f'''<h2 id="oranlar">Trendyol komisyon oranları 2026 (yaklaşık)</h2>
<p>Trendyol komisyonu kategoriye, alt kategoriye ve satıcının anlaşmasına göre belirlenir. Aşağıdaki oranlar 2026’da yaygın olarak görülen aralıkların yaklaşık ortasıdır; kesin oranınızı <strong>Satıcı Paneli → Hesabım → Anlaşma Bilgileri</strong> ekranından görebilirsiniz.</p>
{tablo('trendyol')}
<h2 id="ornek">Örnek: 600 ₺’lik bir elbise satışı</h2>
<p>KDV dahil 600 ₺’ye satılan, 250 ₺’ye alınmış, kargosu 70 ₺ + KDV olan bir giyim ürünü (ürün KDV’si %10, %21,5 komisyon, 8,49 ₺ + KDV hizmet bedeli):</p>
{ornek_tablo('Trendyol', 600, 250, 21.5, 8.49, 70)}
<p>Bu satıştan hesabınıza <strong>{tr(tY)} ₺</strong> yatar; maliyet ve KDV farkı ödendikten sonra net kârınız yaklaşık <strong>{tr(tN)} ₺</strong> olur. Yani 600 ₺’lik satışın yaklaşık %{tr(tN / 600 * 100, 1)}’i kâr olarak kalır.</p>
<h2 id="hizmet">Platform hizmet bedeli ve kargo</h2>
<p>Trendyol her siparişten komisyonun yanında sabit bir <strong>platform hizmet bedeli</strong> alır. 2026’da standart tutar yaklaşık 8,49 ₺ + KDV’dir; “Bugün Kargoda” etiketiyle aynı gün kargoya verilen siparişlerde daha düşük tutar uygulanır. Bu bedel satıcı seviyesine ve dönemsel kampanyalara göre değişebildiği için hesaplayıcıda alanı değiştirebilirsiniz.</p>
<p>Kargo ücreti çoğunlukla satıcıya aittir. Düşük tutarlı siparişlerde Trendyol anlaşmalı kargoyla <strong>barem</strong> denen sabit ücretler uygulanır; daha yüksek tutarlı siparişlerde ücret ürünün desisine göre belirlenir. Güncel barem tutarlarını panelinizdeki kargo ekranından kontrol edin.</p>
<p><strong>Stopaj ve KDV:</strong> Trendyol, ödemenizden KDV hariç satış tutarının %1’i kadar e-ticaret stopajı keser; bu tutar yıl sonu vergisinden düşülür. Komisyon ve hizmet bedeli faturalarındaki KDV’yi, KDV mükellefiyseniz indirebilirsiniz. Ayrıntılı anlatım <a href="https://hesaplarsin.com/pazaryeri-komisyon-hesaplama.html#b-kesintiler">pazaryeri kesinti kalemleri</a> bölümünde.</p>

<h2 id="odeme">Trendyol ödemeleri ne zaman yatar?</h2>
<p>Trendyol, teslim edilen siparişlerin tutarını satıcının vade süresine göre haftalık ödeme günlerinde hesaba aktarır. Vade, satıcı puanına ve anlaşmaya göre değişir; cari hesap ekstrenizde her siparişin ödeme tarihi görünür.</p>
<h2 id="fiyat">Trendyol’da fiyat nasıl belirlenir?</h2>
<p>Hedef kârınızdan geriye doğru gidin: ürün maliyeti + kargo + hizmet bedeli + hedef kâr toplamını bulun, sonra komisyon ve KDV’yi ekleyerek satış fiyatını belirleyin. Hesaplayıcıda farklı satış fiyatları deneyerek net kârın sıfırın üzerinde kaldığı en düşük fiyatı bulabilirsiniz. Diğer platformlarla karşılaştırmak için <a href="https://hesaplarsin.com/pazaryeri-komisyon-hesaplama.html">pazaryeri komisyon hesaplama</a> sayfasını kullanın.</p>''',
faq=[('Trendyol giyim komisyonu yüzde kaç?', 'Giyim, ayakkabı ve çanta kategorilerinde 2026’da Trendyol komisyonu genellikle %21,5 ile %22,5 arasındadır. Alt kategori ve marka anlaşmanıza göre farklı olabilir.'),
     ('Trendyol hizmet bedeli ne kadar?', '2026’da standart platform hizmet bedeli sipariş başına yaklaşık 8,49 ₺ + KDV’dir. Aynı gün kargoya verilen “Bugün Kargoda” siparişlerinde daha düşük tutar uygulanır. Güncel tutar satıcı panelinde yer alır.'),
     ('Trendyol’da 100 ₺’lik üründen ne kadar kazanırım?', 'Düşük fiyatlı ürünlerde kargo ve sabit hizmet bedeli satış tutarının büyük kısmını alır. 100 ₺’lik bir üründe barem kargo, hizmet bedeli ve komisyon birlikte satışın yarısını geçebilir. Hesaplayıcıya kendi maliyetinizi girerek zarar edip etmediğinizi görün.')] + COMMON_FAQ[-1:],
related=['pazaryeri-komisyon-hesaplama', 'hepsiburada-komisyon-hesaplama', 'shopier-komisyon-hesaplama', 'kar-marji-hesaplama', 'kdv-hesaplama'],
sources=SOURCES[:1] + SOURCES[3:],
badges=['✓ Ücretsiz', '2026 Oranları', 'Stopaj Dahil'],
))

# ───────────────────────── HEPSİBURADA ─────────────────────────
TOOLS.append(dict(
slug='hepsiburada-komisyon-hesaplama', name='Hepsiburada Komisyon Hesaplama', cat='isletme', ico='🟧',
title='Hepsiburada Komisyon Hesaplama 2026 – Net Kâr ve Oranlar | Hesaplarsın',
desc='Hepsiburada’da satıştan elinize ne kalır? Kategori komisyonu, KDV, 10,99 ₺ hizmet bedeli, kargo ve %1 stopajı düşerek hesaba yatan tutarı ve net kârı görün.',
h1='🟧 Hepsiburada Komisyon Hesaplama',
lead='Kategorinizi ve satış fiyatınızı girin.' + LEAD_SUFFIX,
card_title='Hepsiburada Net Kâr Hesaplayıcı', button='Hesapla',
form=form('hepsiburada', lock=True), js=JS,
article=f'''<h2 id="oranlar">Hepsiburada komisyon oranları 2026 (yaklaşık)</h2>
<p>Hepsiburada komisyonu kategoriye göre yaklaşık %6 ile %25 arasında değişir ve oranlara ayrıca KDV eklenir. Aşağıdaki değerler 2026 için yaygın oranların yaklaşık ortasıdır; kesin oranınız <strong>İş Ortağım</strong> panelinde ve kategori komisyon listesinde yer alır.</p>
{tablo('hepsiburada')}
<h2 id="ornek">Örnek: 600 ₺’lik bir giyim ürünü</h2>
<p>KDV dahil 600 ₺’ye satılan, 250 ₺’ye alınmış, kargosu 70 ₺ + KDV olan bir giyim ürünü (ürün KDV’si %10, %18 komisyon, 10,99 ₺ + KDV hizmet bedeli):</p>
{ornek_tablo('Hepsiburada', 600, 250, 18.0, 10.99, 70)}
<p>Bu satıştan hesabınıza <strong>{tr(hY)} ₺</strong> yatar, net kârınız yaklaşık <strong>{tr(hN)} ₺</strong> olur. Aynı ürün Trendyol’da (%21,5 komisyonla) yaklaşık {tr(tN)} ₺ net kâr bırakır.</p>
<h2 id="hizmet">Hizmet bedeli ve kargo</h2>
<p>Hepsiburada <strong>21 Eylül 2026</strong>’dan itibaren her teslimat için <strong>10,99 ₺ + KDV</strong> hizmet bedeli uygular (önceki tutar 10,50 ₺). Düşük tutarlı siparişlerde barem kargo uygulanır: 0–200 ₺ arası siparişlerde 43,99 ₺ + KDV, 200–400 ₺ arasında 75,99 ₺ + KDV. Daha yüksek tutarlı siparişlerde kargo ücreti desiye göre hesaplanır.</p>
<p><strong>Vergi kesintileri:</strong> Hepsiburada hakedişinizden %1 e-ticaret stopajını (KDV hariç tutar üzerinden) keserek öder; bu peşin ödenmiş vergidir ve yıllık beyannamede mahsup edilir. Komisyon faturasına eklenen %20 KDV ise KDV mükellefleri için indirilebilir. Tüm kalemlerin açıklaması için <a href="https://hesaplarsin.com/pazaryeri-komisyon-hesaplama.html#b-kesintiler">pazaryeri kesinti kalemleri</a> bölümüne bakın.</p>

<h2 id="fiyat">Hepsiburada’da kârlı fiyat</h2>
<p>200 ₺’nin altındaki siparişlerde barem kargo ve hizmet bedeli birlikte yaklaşık 66 ₺ eder (KDV dahil); bu, düşük fiyatlı ürünlerde kârın neredeyse tamamını alabilir. Ürünü set halinde satmak veya fiyatı barem sınırının üstüne taşımak çoğu zaman daha kârlıdır. Farklı fiyatları hesaplayıcıda deneyin; diğer platformlarla karşılaştırmak için <a href="https://hesaplarsin.com/pazaryeri-komisyon-hesaplama.html">pazaryeri komisyon hesaplama</a> sayfasını kullanın.</p>''',
faq=[('Hepsiburada komisyon oranı yüzde kaç?', 'Kategoriye göre yaklaşık %6 ile %25 arasındadır. Giyim, çanta ve ev tekstilinde yaklaşık %18, ayakkabıda %19,49, cep telefonunda %7–8,5 civarındadır. Oranlara ayrıca KDV eklenir.'),
     ('Hepsiburada hizmet bedeli ne kadar?', '21 Eylül 2026’dan itibaren teslimat başına 10,99 ₺ + KDV’dir (KDV dahil yaklaşık 13,19 ₺). Barem kargo desteği olan gönderilerde de uygulanır.'),
     ('Hepsiburada barem kargo ücretleri nedir?', '0–200 ₺ arası siparişlerde 43,99 ₺ + KDV, 200–400 ₺ arası siparişlerde 75,99 ₺ + KDV’dir. 400 ₺ ve üzerinde kargo ücreti ürünün desisine göre belirlenir.')] + COMMON_FAQ[-1:],
related=['pazaryeri-komisyon-hesaplama', 'trendyol-komisyon-hesaplama', 'shopier-komisyon-hesaplama', 'kar-marji-hesaplama', 'kdv-hesaplama'],
sources=SOURCES[1:2] + SOURCES[3:],
badges=['✓ Ücretsiz', 'Eylül 2026 Ücretleri', 'Stopaj Dahil'],
))

# ───────────────────────── SHOPIER ─────────────────────────
TOOLS.append(dict(
slug='shopier-komisyon-hesaplama', name='Shopier Komisyon Hesaplama', cat='isletme', ico='🛍️',
title='Shopier Komisyon Hesaplama 2026 – Oranlar ve Net Kazanç | Hesaplarsın',
desc='Shopier’de satıştan elinize ne kalır? Aylık cironuza göre %2,99–5,99 + 0,49 ₺ komisyon, KDV ve %1 stopajı düşerek net kazancınızı hesaplayın.',
h1='🛍️ Shopier Komisyon Hesaplama',
lead='Aylık satış seviyenizi ve ürün fiyatınızı girin. Komisyon, komisyonun KDV’si, işlem ücreti, kargo ve %1 e-ticaret stopajı düşülür; elinize geçen tutarı ve net kârınızı görürsünüz.',
card_title='Shopier Net Kazanç Hesaplayıcı', button='Hesapla',
form=form('shopier', lock=True), js=JS,
article=f'''<h2 id="oranlar">Shopier komisyon oranları 2026</h2>
<p>Shopier sabit bir kategori komisyonu yerine, <strong>aylık toplam satışınıza göre kademeli</strong> bir oran uygular. Her işleme oranın yanında 0,49 ₺ sabit ücret eklenir; tutarlar KDV hariçtir.</p>
{tablo('shopier')}
<p>Yeni satıcılar ve aylık 15.000 ₺’nin altında satış yapanlar en yüksek kademeden (%5,99 + 0,49 ₺) başlar; satış hacmi arttıkça oran %2,99’a kadar düşer.</p>
<h2 id="ornek">Örnek: 600 ₺’lik bir satış</h2>
<p>KDV dahil 600 ₺’ye satılan, 250 ₺’ye alınmış bir giyim ürünü (ürün KDV’si %10); kargoyu siz ödüyorsunuz (70 ₺ + KDV), en yüksek kademe (%5,99):</p>
{ornek_tablo('Shopier', 600, 250, 5.99, 0.49, 70)}
<p>Bu satıştan hesabınıza <strong>{tr(sY)} ₺</strong> yatar, net kârınız yaklaşık <strong>{tr(sN)} ₺</strong> olur. Aynı ürün Trendyol’da yaklaşık {tr(tN)} ₺, Hepsiburada’da {tr(hN)} ₺ net kâr bırakır. Fark büyük; ancak Shopier’de müşteriyi Instagram, WhatsApp veya reklamla sizin getirmeniz gerekir. Reklam maliyetinizi de hesaba katmayı unutmayın.</p>
<h2 id="nasil">Shopier nasıl çalışır?</h2>
<p>Shopier bir pazaryeri değil, sosyal medyadan satış yapanlar için ödeme ve mağaza altyapısıdır. Ürününüz için bir ödeme linki oluşturur, bunu Instagram profilinizde veya mesajlarda paylaşırsınız; müşteri kartla öder, Shopier komisyonu düşüp kalan tutarı bakiyenize aktarır. Bakiye, Shopier’in belirlediği ödeme dönemlerinde banka hesabınıza geçer.</p>
<p><strong>Shopier’de vergi:</strong> Shopier aracı ödeme kuruluşu olarak çalıştığı için o da ödemelerden %1 stopaj keser. Şahıs olarak, şirket kurmadan satış yapanlar için esnaf muaflığı koşullarını ve KDV durumunu bir mali müşavirle netleştirmek önemlidir; muaflıktaysanız hesaplayıcıda “KDV mükellefi değilim” kutusunu işaretleyin.</p>

<h2 id="vergi">Shopier’de satış yapmak için şirket gerekir mi?</h2>
<p>Düzenli satış yapıyorsanız vergi kaydınız olmalıdır. Evden el emeği ürün satanlar belirli şartlarla esnaf muaflığından yararlanabilir; bu durumda hesaplayıcıda “KDV mükellefi değilim” kutusunu işaretleyin. Şahıs şirketi ve vergi konusunda bir mali müşavirden görüş almanızı öneririz.</p>''',
faq=[('Shopier komisyonu ne kadar?', '2026’da aylık toplam satışınıza göre %5,99 ile %2,99 arasında değişir; her işleme ayrıca 0,49 ₺ eklenir. Tutarlar KDV hariçtir. Yeni satıcılar %5,99 + 0,49 ₺ ile başlar.'),
     ('Shopier mi Trendyol mu daha kârlı?', 'Komisyon açısından Shopier çok daha ucuzdur (yaklaşık %6’ya karşı %20 ve üzeri). Ama Trendyol size hazır müşteri getirir, Shopier’de ise müşteriyi sosyal medya veya reklamla siz bulursunuz. Reklam maliyetiniz satış başına komisyon farkından düşükse Shopier daha kârlıdır.'),
     ('Shopier’de stopaj kesiliyor mu?', 'Evet. Aracı ödeme kuruluşları da 2025’ten itibaren satıcıya yapılan ödemelerden KDV hariç tutarın %1’i oranında stopaj keser. Bu tutar yıllık gelir vergisinden mahsup edilir.')] + COMMON_FAQ[-1:],
related=['pazaryeri-komisyon-hesaplama', 'trendyol-komisyon-hesaplama', 'hepsiburada-komisyon-hesaplama', 'kar-marji-hesaplama', 'komisyon-hesaplama'],
sources=SOURCES[2:],
badges=['✓ Ücretsiz', '2026 Oranları', 'Stopaj Dahil'],
))
