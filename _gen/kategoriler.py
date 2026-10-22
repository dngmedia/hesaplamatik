"""Kategori (hub) sayfaları: her kategori için rehber metni + araç listesi + ilgili yazılar + SSS.
Araç listesi index.html'deki TOOLS dizisinden okunur; yeni araç eklendiğinde kategori sayfası kendiliğinden güncellenir.
build.py sonunda çalışır. Kabuk (üst menü, CSS, footer) olarak oluşturulmuş bir araç sayfası kullanılır.
"""
import os, re, json, html
from kategori_rehber import R as REH

BASE = 'https://hesaplarsin.com'
E = lambda t: html.escape(t, quote=True)

# kategori anahtarı (index cat) -> sayfa tanımı
K = {
'maas': dict(slug='maas-hesaplamalari', ad='Maaş ve SGK Hesaplamaları', ico='💼',
  title='Maaş Hesaplama Araçları 2026 – Net Maaş, Tazminat, Emeklilik | Hesaplarsın',
  desc='2026 net maaş, kıdem ve ihbar tazminatı, fazla mesai, işsizlik maaşı ve emeklilik hesaplamaları tek sayfada. Güncel asgari ücret ve SGK oranlarıyla.',
  intro=['Çalışan hayatındaki bütün temel hesaplar burada: brüt maaştan net maaşa geçiş, fazla mesai ücreti, işten ayrılınca alınacak kıdem ve ihbar tazminatı, işsizlik maaşı ve ne zaman emekli olacağınız.',
         'Tüm araçlar 2026 parametreleriyle çalışır: brüt asgari ücret 33.030 ₺, net asgari ücret 28.075,50 ₺; işçi SGK primi %14, işsizlik sigortası primi %1; Temmuz–Aralık 2026 kıdem tazminatı tavanı 73.729,87 ₺. Rakamlar Resmî Gazete’de değiştiği gün güncellenir.'],
  extra=[], blogs=['net-maas-nasil-hesaplanir', 'brutten-nete-maas-tablosu-2026', 'kidem-tazminati-2027', 'asgari-ucret-2027', 'fazla-mesai-haklari-2026', 'emeklilik-hesaplama-2026', 'sgk-primi-hesaplama-rehberi'],
  faq=[('Brüt maaştan net maaş nasıl hesaplanır?', 'Brüt maaştan %14 SGK işçi payı ve %1 işsizlik sigortası primi düşülür; kalan matrah üzerinden gelir vergisi ve damga vergisi hesaplanır. 2026’da asgari ücrete isabet eden vergiler istisna olduğundan, asgari ücretli çalışanın net maaşı 28.075,50 ₺’dir.'),
       ('Kıdem tazminatı tavanı 2026’da ne kadar?', 'Temmuz–Aralık 2026 döneminde kıdem tazminatı tavanı 73.729,87 ₺’dir. Tavan, memur maaş katsayısındaki değişime göre her yıl Ocak ve Temmuz’da güncellenir.'),
       ('İşsizlik maaşı ne kadar?', 'Son 4 aylık brüt kazancın ortalamasının %40’ı kadardır; ancak brüt asgari ücretin %80’ini (2026’da 26.424 ₺) geçemez. Yalnızca damga vergisi kesilir.')]),
'kamu': dict(slug='memur-hesaplamalari', ad='Kamu ve Memur Hesaplamaları', ico='🏛️',
  title='Memur Maaş Hesaplama 2026–2027 – Unvanlara Göre Maaşlar | Hesaplarsın',
  desc='Öğretmen, polis, hemşire, doktor ve mühendis maaşları, Ocak 2027 memur ve emekli zammı tahmini. Temmuz 2026 katsayılarıyla güncel tablolar.',
  intro=['Memur ve kamu çalışanları için maaş tabloları ve zam hesaplamaları. Her meslek sayfasında Temmuz 2026 maaşı, Ocak 2027 için farklı enflasyon senaryolarına göre tahmini yeni maaş ve unvan/kademe farkları yer alır.',
         'Temmuz–Aralık 2026 memur maaş katsayısı 1,575512, taban aylık katsayısı 25,794915, yan ödeme katsayısı 0,499649’dur. Ocak 2027 zammı, toplu sözleşmedeki %5 artış ile ilk 6 aylık enflasyonun %7’yi aşan kısmı (enflasyon farkı) birlikte uygulanarak belirlenir.'],
  extra=['emeklilik-yasi-hesaplama'], blogs=['memur-emekli-zammi-ocak-2027', 'kidem-tazminati-2027', 'emeklilik-hesaplama-2026'],
  faq=[('Ocak 2027 memur zammı ne kadar olacak?', 'Toplu sözleşmeyle belirlenen %5 zam ile Temmuz–Aralık 2026 enflasyonunun %7’yi aşan kısmı birleşik olarak uygulanır. Kesin oran, Aralık 2026 enflasyonunun açıklandığı Ocak 2027’nin ilk iş gününde (4 Ocak) belli olur.'),
       ('Memur maaşımı nasıl öğrenirim?', 'Maaş; unvan, derece-kademe, hizmet yılı, eş ve çocuk durumu gibi bilgilere göre değişir. Memur maaşları sayfasındaki tablodan unvanınızın Temmuz 2026 maaşını ve Ocak 2027 tahminini görebilirsiniz; kesin tutar maaş bordronuzda yer alır.'),
       ('Memur maaşı ne zaman yatar?', 'Memur maaşları her ayın 15’inde, peşin olarak ödenir. 15’i hafta sonuna denk gelirse genellikle bir önceki iş günü yatırılır.')]),
'vergi': dict(slug='vergi-hesaplamalari', ad='Vergi Hesaplamaları', ico='🧾',
  title='Vergi Hesaplama Araçları 2026 – KDV, Gelir Vergisi, Tapu Harcı | Hesaplarsın',
  desc='KDV, KDV hariç, gelir vergisi, ÖTV, MTV, tapu harcı, damga vergisi ve amortisman hesaplamaları. 2026 oranları ve vergi dilimleriyle.',
  intro=['Bireylerin ve işletmelerin en sık yaptığı vergi hesapları: fiyata KDV ekleme ve çıkarma, yıllık gelir vergisi, araç alırken ÖTV, her yıl ödenen MTV, ev alırken tapu harcı ve sözleşmelerdeki damga vergisi.',
         'Türkiye’de 2026’da üç KDV oranı uygulanır: %1 (temel gıda), %10 (hazır giyim, konut elektriği, lokanta, ilaç) ve %20 (genel oran). Gelir vergisi dilimleri %15’ten %40’a kadar artan oranlıdır; tapu harcı alıcı ve satıcı için ayrı ayrı %2’dir.'],
  extra=[], blogs=['kdv-oranlari-2026', 'vergi-dilimleri-2027', 'yeniden-degerleme-orani-2026', 'tapu-harci-hesaplama', 'kira-geliri-vergisi-hesaplama'],
  faq=[('KDV nasıl hesaplanır?', 'KDV hariç fiyatı KDV oranıyla çarparsınız: 1.000 ₺ × %20 = 200 ₺ KDV, KDV dahil fiyat 1.200 ₺. KDV dahil fiyattan KDV’yi bulmak için fiyatı 1,20’ye bölersiniz.'),
       ('Tapu harcı kaç TL?', 'Tapu harcı, satış bedeli (beyan edilen değer emlak vergi değerinin altında olamaz) üzerinden alıcı için %2, satıcı için %2 olmak üzere toplam %4’tür. Ayrıca döner sermaye ücreti ödenir.'),
       ('2026 gelir vergisi dilimleri nelerdir?', 'Ücretliler için 2026’da gelir vergisi %15, %20, %27, %35 ve %40 olmak üzere beş dilimlidir. Dilim sınırları her yıl yeniden değerleme oranında artırılır.')]),
'finans': dict(slug='finans-hesaplamalari', ad='Finans ve Kredi Hesaplamaları', ico='💰',
  title='Finans Hesaplama Araçları 2026 – Kredi, Faiz, Döviz, Enflasyon | Hesaplarsın',
  desc='Kredi taksiti, mevduat faizi, bileşik faiz, enflasyon, döviz, kredi kartı asgari ödeme ve yatırım getirisi hesaplamaları tek yerde.',
  intro=['Paranızla ilgili kararlar için temel hesaplar: ihtiyaç, taşıt ve konut kredisi taksiti, kredi erken kapama, mevduat faizi getirisi, bileşik faiz, enflasyon karşısında paranın değeri, döviz çevirisi ve yatırımların geri dönüş süresi.',
         'Kredi hesaplarında BSMV ve KKDF (ihtiyaç kredilerinde %15 + %15) dahil edilir; mevduat hesaplarında stopaj düşülür. Enflasyon ve kira hesapları TÜİK’in açıkladığı TÜFE verileriyle her ay güncellenir; açıklama tarihlerini Ekonomi Takvimi’nden takip edebilirsiniz.'],
  extra=[], blogs=['banka-kredisi-taksit-hesaplama', 'enflasyon-etkisi-2026', 'yeniden-degerleme-orani-2026'],
  faq=[('Kredi taksiti nasıl hesaplanır?', 'Aylık taksit, anapara, aylık faiz oranı ve vadeye göre eşit taksit (annüite) formülüyle bulunur. İhtiyaç kredilerinde faize ayrıca %15 BSMV ve %15 KKDF eklenir; bu yüzden gerçek maliyet ilan edilen faizden yüksektir.'),
       ('Mevduat faizinden ne kadar vergi kesilir?', 'Mevduat faizi gelirinden vadeye göre değişen oranda stopaj kesilir. Hesaplayıcı, güncel stopaj oranını düşerek elinize geçecek net getiriyi gösterir.'),
       ('Paranın değer kaybı nasıl hesaplanır?', 'İki tarih arasındaki kümülatif enflasyon bulunur ve tutar buna bölünür. Örneğin %50 kümülatif enflasyonda 1.000 ₺’nin alım gücü yaklaşık 667 ₺’ye düşer.')]),
'isletme': dict(slug='isletme-hesaplamalari', ad='İşletme ve Ticaret Hesaplamaları', ico='📊',
  title='İşletme Hesaplama Araçları – Kâr Marjı, Komisyon, Pazaryeri | Hesaplarsın',
  desc='Kâr marjı, kâr/zarar, indirim, iskonto, komisyon, Trendyol ve Hepsiburada pazaryeri komisyonu, ciro, başa baş noktası hesaplamaları.',
  intro=['Esnaf, e-ticaret satıcıları ve küçük işletmeler için günlük ticari hesaplar: satış fiyatı ve kâr marjı, indirim ve iskonto, satış komisyonu, Trendyol, Hepsiburada ve Shopier’de bir satıştan elinize ne kalacağı, ciro, net kâr ve başa baş noktası.',
         'Pazaryeri hesaplayıcıları komisyonun yanında komisyonun %20 KDV’sini, sabit hizmet bedelini, kargoyu ve 2025’ten beri uygulanan %1 e-ticaret stopajını da düşer; böylece hesabınıza yatan tutarı ve gerçek net kârınızı ayrı ayrı görürsünüz.'],
  extra=['kdv-hesaplama'], blogs=['komisyon-hesaplama-rehberi', 'kdv-oranlari-2026'],
  faq=[('Kâr marjı nasıl hesaplanır?', 'Kâr marjı = (Satış fiyatı − Maliyet) ÷ Satış fiyatı × 100. Maliyete göre hesaplanan orana ise kâr oranı (markup) denir; 100 ₺’ye alınıp 150 ₺’ye satılan üründe kâr marjı %33,3, kâr oranı %50’dir.'),
       ('Trendyol ne kadar komisyon alıyor?', 'Kategoriye göre değişir; 2026’da giyimde yaklaşık %21,5, elektronikte %5–10 civarındadır. Komisyona ayrıca KDV ve sipariş başına hizmet bedeli eklenir.'),
       ('Başa baş noktası nedir?', 'İşletmenin ne kâr ne zarar ettiği satış miktarıdır: Sabit giderler ÷ (Birim satış fiyatı − Birim değişken maliyet).')]),
'gayrimenkul': dict(slug='emlak-hesaplamalari', ad='Emlak ve Kira Hesaplamaları', ico='🏠',
  title='Emlak ve Kira Hesaplama Araçları 2026 – Kira Artışı, Tapu Harcı | Hesaplarsın',
  desc='Kira artış oranı, kira getirisi, metrekare fiyatı, tapu harcı, damga vergisi ve boya hesaplamaları. TÜİK verisiyle aylık güncel.',
  intro=['Ev kiralayanlar, ev sahipleri ve alım-satım yapanlar için hesaplar: yasal kira artış oranı, bir evin kira getirisi ve amortisman süresi, metrekare birim fiyatı, tapu harcı ve taşınmadan önce kaç litre boya gerektiği.',
         'Konut kiralarında yıllık artış, TÜİK’in açıkladığı 12 aylık TÜFE ortalamasını aşamaz; oran her ayın 3’ünde yeni enflasyon verisiyle güncellenir. Tapu harcı alıcı ve satıcı için ayrı ayrı %2’dir.'],
  extra=['tapu-harci-hesaplama', 'damga-vergisi-hesaplama', 'boya-hesaplama'], blogs=['kasim-2026-kira-artis-orani', 'kira-artisi-2027', 'tapu-harci-hesaplama', 'kira-geliri-vergisi-hesaplama', 'dask-sigortasi-hesaplama'],
  faq=[('Kira artış oranı nasıl belirlenir?', 'Konut kiralarında artış, kira döneminin bittiği aydan önceki 12 aylık TÜFE ortalamasıyla sınırlıdır. Bu oran her ay TÜİK enflasyon açıklamasıyla birlikte belli olur.'),
       ('Kira getirisi nasıl hesaplanır?', 'Yıllık kira geliri ev fiyatına bölünür: yılda 240.000 ₺ kira getiren 6.000.000 ₺’lik evin brüt kira getirisi %4’tür; ev kendini yaklaşık 25 yılda amorti eder.'),
       ('Metrekare fiyatı nasıl bulunur?', 'Satış fiyatı metrekareye bölünür: 4.500.000 ₺’lik 120 m² ev, metrekare başına 37.500 ₺ eder. İlanlarda brüt ve net m² farkına dikkat edin.')]),
'arac': dict(slug='arac-hesaplamalari', ad='Araç ve Yakıt Hesaplamaları', ico='🚗',
  title='Araç Hesaplama Araçları 2026 – MTV, ÖTV, Yakıt, Taşıt Kredisi | Hesaplarsın',
  desc='Taşıt kredisi, MTV, ÖTV, yakıt maliyeti, 100 km yakıt tüketimi, araç değer kaybı ve muayene gecikme cezası hesaplamaları.',
  intro=['Araç sahipleri ve araç almayı düşünenler için hesaplar: taşıt kredisi taksiti, yıllık motorlu taşıtlar vergisi (MTV), sıfır araçta ÖTV, yol için yakıt maliyeti, aracınızın 100 km’de kaç litre yaktığı, ikinci elde değer kaybı ve gecikmiş muayene cezası.',
         'MTV her yıl Ocak ve Temmuz’da iki taksitte ödenir ve tutarı aracın motor hacmine, yaşına ve değerine göre belirlenir. 2026’da MTV tutarları %18,95 oranında artırılmıştır.'],
  extra=['mtv-hesaplama', 'otv-hesaplama'], blogs=[],
  faq=[('MTV ne zaman ödenir?', 'Motorlu taşıtlar vergisi her yıl Ocak ve Temmuz aylarında olmak üzere iki eşit taksitte ödenir. Süresinde ödenmeyen MTV’ye gecikme zammı uygulanır.'),
       ('100 km’de kaç litre yakıyor nasıl hesaplanır?', 'Aldığınız yakıt litresini gidilen kilometreye bölüp 100 ile çarpın: 45 litreyle 600 km gittiyseniz tüketim 45 ÷ 600 × 100 = 7,5 L/100 km’dir.'),
       ('Araç muayenesi geç yapılırsa ne olur?', 'Muayene süresi geçen araçlara her ay için gecikme ücreti eklenir ve trafikte muayenesiz araç kullanmak ayrıca para cezasına tabidir.')]),
'saglik': dict(slug='saglik-hesaplamalari', ad='Sağlık ve Beslenme Hesaplamaları', ico='❤️',
  title='Sağlık Hesaplama Araçları – BMI, Kalori, İdeal Kilo, Su İhtiyacı | Hesaplarsın',
  desc='Vücut kitle indeksi, bazal metabolizma, günlük kalori ve protein ihtiyacı, ideal kilo, vücut yağ oranı ve su ihtiyacı hesaplamaları.',
  intro=['Sağlıklı yaşam için temel ölçümler: vücut kitle indeksi (BMI), bazal metabolizma hızı, günlük kalori ve protein ihtiyacı, ideal kilo aralığı, vücut yağ oranı, bel-kalça oranı ve günlük su ihtiyacı.',
         'Hesaplamalar Dünya Sağlık Örgütü sınıflandırmaları ve Mifflin-St Jeor gibi yaygın kabul gören formüllere dayanır. Sonuçlar bilgilendirme amaçlıdır; tıbbi bir durumunuz varsa doktorunuza danışın.'],
  extra=[], blogs=[],
  faq=[('BMI nasıl hesaplanır?', 'Kilonuzu (kg) boyunuzun (m) karesine bölün: 70 kg ve 1,75 m için 70 ÷ (1,75 × 1,75) = 22,9. Dünya Sağlık Örgütü’ne göre 18,5–24,9 arası normal kilo kabul edilir.'),
       ('Günde kaç kalori almalıyım?', 'Bazal metabolizma hızınız aktivite düzeyinize göre bir katsayıyla çarpılarak bulunur. Hareketsiz bir yetişkinde bu genellikle 1.800–2.400 kalori arasındadır; kişiye göre değişir.'),
       ('Günde ne kadar su içmeliyim?', 'Yaygın yaklaşım, vücut ağırlığının her kilogramı için yaklaşık 30–35 ml sudur; 70 kg bir yetişkin için bu yaklaşık 2,1–2,5 litre eder. Sıcak hava ve egzersizde ihtiyaç artar.')]),
'egitim': dict(slug='egitim-hesaplamalari', ad='Eğitim ve Sınav Hesaplamaları', ico='🎓',
  title='Sınav ve Not Hesaplama Araçları – TYT, AYT, KPSS Net, Ortalama | Hesaplarsın',
  desc='TYT, AYT ve KPSS net hesaplama, lise not ortalaması ve takdir-teşekkür hesaplamaları. Güncel sınav puan kurallarıyla.',
  intro=['Öğrenciler ve adaylar için hesaplar: TYT ve AYT netleri, KPSS neti, dönem ve yıl sonu not ortalaması, takdir veya teşekkür belgesi alıp alamayacağınız.',
         'Sınav netleri, yanlış cevapların doğrulardan düşülmesiyle bulunur: TYT, AYT ve KPSS’de 4 yanlış 1 doğruyu götürür. Lisede takdir için 85, teşekkür için 70 ve üzeri ağırlıklı ortalama gerekir (kırık not olmaması şartıyla).'],
  extra=[], blogs=[],
  faq=[('Net nasıl hesaplanır?', 'Doğru sayısından yanlış sayısının dörtte biri çıkarılır: 30 doğru, 8 yanlış = 30 − 2 = 28 net.'),
       ('Takdir belgesi için kaç ortalama gerekir?', 'Lisede takdir belgesi için 85,00 ve üzeri, teşekkür belgesi için 70,00–84,99 arası ağırlıklı ortalama gerekir; ayrıca başarısız (kırık) dersinizin olmaması gerekir.'),
       ('Not ortalaması nasıl hesaplanır?', 'Her dersin notu haftalık ders saatiyle çarpılır, toplam, toplam ders saatine bölünür. Böylece ders saati fazla olan derslerin ortalamaya etkisi daha büyük olur.')]),
'diger': dict(slug='gunluk-hesaplamalar', ad='Günlük Hesaplamalar', ico='🧮',
  title='Günlük Hesaplama Araçları – Gün, Yaş, Fatura, Ortalama | Hesaplarsın',
  desc='İki tarih arası gün, yaş, iş günü, ortalama, elektrik, doğalgaz ve su faturası, boya, internet hızı ve veri kullanımı hesaplamaları.',
  intro=['Gündelik hayatta sık ihtiyaç duyulan pratik hesaplar: iki tarih arasında kaç gün olduğu, yaşınızın gün ve ay olarak karşılığı, iş günü sayısı, sayıların ortalaması, elektrik, doğalgaz ve su faturası tahmini, boya ihtiyacı, internet hızı ve dosya indirme süresi.',
         'Tarih hesaplamalarında resmî tatiller ve arife günleri dikkate alınabilir; fatura hesaplayıcıları güncel tarife birim fiyatlarını kullanır ve vergileri ayrı ayrı gösterir.'],
  extra=['para-sayma-hesaplama', 'yuzde-hesaplama'], blogs=['elektrik-faturasi-neden-yuksek'],
  faq=[('İki tarih arası kaç gün nasıl hesaplanır?', 'Bitiş tarihinden başlangıç tarihi çıkarılır. Başlangıç gününü de saymak istiyorsanız sonuca 1 eklenir. Hesaplayıcı ayrıca hafta, ay ve iş günü karşılığını da gösterir.'),
       ('Ortalama nasıl hesaplanır?', 'Sayıların toplamı sayı adedine bölünür: 70, 85 ve 90’ın ortalaması 245 ÷ 3 = 81,67.'),
       ('Elektrik faturası nasıl hesaplanır?', 'Tüketilen kWh, tarifedeki birim enerji ve dağıtım bedeliyle çarpılır; üzerine elektrik tüketim vergisi ve KDV (konutta %10) eklenir.')]),
}

ORDER = ['maas', 'kamu', 'vergi', 'finans', 'isletme', 'gayrimenkul', 'arac', 'saglik', 'egitim', 'diger']
CATPAGE = {k: v['slug'] for k, v in K.items()}


def tools_from_index():
    s = open('index.html', encoding='utf-8').read()
    T = re.findall(r"\{ico:'([^']*)',name:'([^']*)',desc:(?:'([^']*)'|\"([^\"]*)\"),url:'([^']*)',cat:'([^']*)',badge:'([^']*)'", s)
    out = {}
    for ico, n, d1, d2, u, cat, b in T:
        out[u.strip('/').replace('.html', '')] = dict(ico=ico, name=n, desc=d1 or d2, cat=cat, badge=b)
    return out


def blog_title(slug):
    p = f'blog/{slug}.html'
    if not os.path.exists(p):
        return None
    m = re.search(r'<h1[^>]*>(.*?)</h1>', open(p, encoding='utf-8').read(), re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else slug


def shell():
    s = open('memur-maaslari.html', encoding='utf-8').read()
    head_end = s.index('<nav class="breadcrumb"')
    foot = s.index('<footer'); foot_end = s.index('</footer>') + len('</footer>')
    return s[:head_end], s[foot:foot_end]


def card(slug, t):
    b = ' <span style="font-size:.68rem;background:#dcfce7;color:#047857;border-radius:6px;padding:1px 6px;margin-left:4px">Yeni</span>' if t['badge'] == 'new' else ''
    return (f'<a class="kcard" href="{BASE}/{slug}.html"><span class="kico">{t["ico"]}</span><span><strong>{E(t["name"])}</strong>{b}'
            f'<small>{E(t["desc"])}</small></span></a>')


CSS = '''<style>.kgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin:14px 0 6px}
.kcard{display:flex;gap:12px;align-items:flex-start;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:14px;text-decoration:none;color:var(--text);transition:border-color .15s,box-shadow .15s}
.kcard:hover{border-color:var(--brand);box-shadow:0 4px 14px rgba(26,86,219,.12)}.kico{font-size:1.5rem;line-height:1}.kcard strong{display:block;font-size:.95rem}.kcard small{display:block;color:var(--muted);font-size:.8rem;margin-top:3px;line-height:1.45}
.kcats{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.kcats a{border:1px solid var(--border);border-radius:999px;padding:6px 12px;font-size:.82rem;text-decoration:none;color:var(--text);background:var(--card)}.kcats a:hover{border-color:var(--brand);color:var(--brand)}
.kblog{margin:8px 0 0;padding-left:18px}.kblog li{margin:6px 0}</style>'''


def render_cat(key, tools, head, foot):
    d = K[key]; slug = d['slug']; url = f'{BASE}/{slug}.html'
    rh = REH.get(key, {}); faqs = d['faq'] + rh.get('faq', [])
    items = [(s, t) for s, t in tools.items() if t['cat'] == key]
    for x in d['extra']:
        if x in tools and all(x != s for s, _ in items):
            items.append((x, tools[x]))
    blogs = [(b, blog_title(b)) for b in d['blogs'] if blog_title(b)]
    lds = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": d['ad'], "description": d['desc'], "url": url, "inLanguage": "tr",
         "isPartOf": {"@type": "WebSite", "name": "Hesaplarsın", "url": BASE + '/'},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f'{BASE}/{s}.html', "name": t['name']} for i, (s, t) in enumerate(items)]}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": BASE + '/'},
            {"@type": "ListItem", "position": 2, "name": d['ad'], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{E(d["title"] if len(d["title"]) <= 62 else d["title"].replace(" | Hesaplarsın", ""))}</title>', h, 1, re.S)
    for pat, val in [(r'(<meta name="description" content=")[^"]*', d['desc']), (r'(<meta property="og:description" content=")[^"]*', d['desc']),
                     (r'(<meta name="twitter:description" content=")[^"]*', d['desc']),
                     (r'(<meta property="og:title" content=")[^"]*', d['title'].replace(' | Hesaplarsın', '')),
                     (r'(<meta name="twitter:title" content=")[^"]*', d['title'].replace(' | Hesaplarsın', '')),
                     (r'(<link rel="canonical" href=")[^"]*', url), (r'(<meta property="og:url" content=")[^"]*', url)]:
        h = re.sub(pat, lambda m: m.group(1) + E(val), h, 1)
    h = re.sub(r'<meta property="og:type" content="[^"]*"', '<meta property="og:type" content="website"', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    h = re.sub(r'<meta property="og:image" content="[^"]*"', f'<meta property="og:image" content="{BASE}/assets/og-image.png"', h)
    h = re.sub(r'<meta name="twitter:image" content="[^"]*"', f'<meta name="twitter:image" content="{BASE}/assets/og-image.png"', h)
    h = h.replace('</head>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in lds) + CSS + '\n</head>', 1)
    h = re.sub(r'<body data-tool="[^"]*">', f'<body data-tool="kategori-{slug}">', h)
    others = ''.join(f'<a href="{BASE}/{K[k]["slug"]}.html">{K[k]["ico"]} {K[k]["ad"]}</a>' for k in ORDER if k != key)
    blog_html = ('<h2>İlgili Rehberler</h2><ul class="kblog">' + ''.join(f'<li><a href="{BASE}/blog/{b}.html">{E(t)}</a></li>' for b, t in blogs) + '</ul>') if blogs else ''
    gl = [(t, x, ac) for t, x, ac in rh.get('rehber', []) if x in tools or os.path.exists(x + '.html')]
    guide_html = ''
    if gl:
        guide_html += '<h2>Hangi durumda hangi araç?</h2><ul class="kblog">' + ''.join(
            f'<li><strong>{E(t)}:</strong> <a href="{BASE}/{x}.html">{E(tools[x]["name"] if x in tools else x)}</a> — {E(ac)}</li>' for t, x, ac in gl) + '</ul>'
    if rh.get('tablo'):
        guide_html += ('<h2>2026 için temel rakamlar</h2><div style="overflow-x:auto"><table class="veri-tablo"><thead><tr><th>Kalem</th><th>Değer</th></tr></thead><tbody>'
                       + ''.join(f'<tr><td>{E(k_)}</td><td>{E(v_)}</td></tr>' for k_, v_ in rh['tablo']) + '</tbody></table></div>')
    faq_html = ''.join(f'<div class="faq-item"><button class="faq-q" type="button" aria-expanded="false">{E(q)}</button><div class="faq-a"><p>{a}</p></div></div>' for q, a in faqs)
    body = f'''<nav class="breadcrumb" aria-label="Breadcrumb">
  <a href="{BASE}/">Ana Sayfa</a><span aria-hidden="true">›</span><span aria-current="page">{E(d["ad"])}</span>
</nav>
<header class="hero">
  <div class="hero-inner">
    <span class="hero-tag">{d["ico"]} Kategori</span>
    <h1>{E(d["ad"])}</h1>
    <p>{d["intro"][0]}</p>
    <div class="hero-badges"><span class="hbadge">{len(items)} araç</span><span class="hbadge">✓ Ücretsiz</span><span class="hbadge">2026 Güncel</span></div>
  </div>
</header>
<div class="article"><div class="article-inner" style="max-width:1100px">
  <h2>Tüm {E(d["ad"])}</h2>
  <div class="kgrid">{''.join(card(s, t) for s, t in items)}</div>
  {guide_html}
  <h2>Bu kategorideki hesaplamalar hakkında</h2>
  <p>{d["intro"][1]}</p>
  <p style="font-size:.88rem;color:var(--muted)">Tüm oranların kaynakları ve güncellenme takvimi: <a href="{BASE}/yontem-ve-kaynaklar.html">Yöntem ve Kaynaklar</a>. Hazırlayan: <a href="{BASE}/hakkimizda.html#kurucu">Duran Gönülalan</a>, Hesaplarsın kurucusu.</p>
  {blog_html}
  <h2>Sık Sorulan Sorular</h2>
  {faq_html}
  <h2>Diğer Kategoriler</h2>
  <div class="kcats">{others}</div>
</div></div>
'''
    script = '''<script>(function(){var hb=document.getElementById('hamBtn'),nl=document.getElementById('navLinks');if(hb&&nl){hb.addEventListener('click',function(){var o=nl.classList.toggle('open');hb.setAttribute('aria-expanded',o);});}
document.querySelectorAll('.faq-q').forEach(function(b){b.addEventListener('click',function(){var a=b.nextElementSibling;var o=a.classList.toggle('open');b.classList.toggle('open',o);b.setAttribute('aria-expanded',o);});});})();</script>'''
    open(f'{slug}.html', 'w', encoding='utf-8').write(h + body + foot + '\n' + script + '\n</body>\n</html>\n')
    return slug, len(items)


def fix_links():
    """Breadcrumb ve footer'daki /#kategori bağlantılarını kategori sayfalarına çevirir (tüm sayfalarda)."""
    import glob
    anch = {'finans': 'finans', 'vergi': 'vergi', 'maas': 'maas', 'kamu': 'kamu', 'gayrimenkul': 'gayrimenkul', 'saglik': 'saglik',
            'arac': 'arac', 'isletme': 'isletme', 'egitim': 'egitim', 'diger': 'diger'}
    n = 0
    for p in glob.glob('*.html') + glob.glob('blog/*.html'):
        s = open(p, encoding='utf-8').read(); o = s
        for k, a in anch.items():
            s = s.replace(f'href="{BASE}/#{a}"', f'href="{BASE}/{CATPAGE[k]}.html"').replace(f'"item": "{BASE}/#{a}"', f'"item": "{BASE}/{CATPAGE[k]}.html"')
        if s != o:
            open(p, 'w', encoding='utf-8').write(s); n += 1
    return n


def run():
    tools = tools_from_index()
    head, foot = shell()
    res = [render_cat(k, tools, head, foot) for k in ORDER]
    return res, fix_links()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(run())
