# -*- coding: utf-8 -*-
"""
TEK DOĞRULUK KAYNAĞI (veri sicili)
==================================
Sitede geçen resmî rakamların güncel değeri, kaynağı ve bir sonraki kontrol tarihi burada durur.
`_gen/dogrula.py` her build/test'te:
  1) ESKI listesindeki eski/yanlış ifadeleri bütün sayfalarda arar  → bulursa HATA
  2) BAGLAM kurallarıyla, belli bir bağlamda geçen rakamın izinli değerlerden biri olup olmadığına bakar → değilse HATA
  3) Sayfalardaki "A × B = C" tipi örnek hesapları yeniden hesaplar → tutmuyorsa HATA
  4) KONTROL tarihi geçmiş veriyi listeler → HATA (veri yeniden doğrulanıp tarih ileri alınmadan build temiz geçmez)

Bir rakam değiştiğinde yapılacak:
  - FACTS içindeki değeri, kaynağı ve 'dogrulandi' / 'kontrol' tarihini güncelle,
  - eski değeri ESKI'ye ekle (sayfalarda kalmışsa dogrula.py yakalar),
  - build + test.
"""

# key: (değer, kaynak, doğrulandığı tarih, bir sonraki kontrol tarihi)
FACTS = {
    'asgari_brut_2026':   ('33.030,00 TL', 'ÇSGB / Resmî Gazete 24.12.2025', '2026-10-30', '2027-01-05'),
    'asgari_net_2026':    ('28.075,50 TL', 'ÇSGB', '2026-10-30', '2027-01-05'),
    'sgk_tavan_2026':     ('297.270 TL (asgari ücret × 9)', '5510 m.82, 7555 s.K.', '2026-10-30', '2027-01-05'),
    'isveren_sgk_2026':   ('%21,75 (MYÖ %12 + GSS %7,5 + KVSK %2,25); teşvikle %19,75, imalatta %16,75', 'SGK 2026 prim oranları', '2026-10-30', '2027-01-05'),
    'bagkur_4b_2026':     ('%35,75; 5 puan indirimle %30,75', 'Alomaliye 18.08.2026 / SGK', '2026-10-30', '2027-01-05'),
    'kidem_tavan':        ('64.948,77 TL (Oca–Haz 2026), 73.729,87 TL (Tem–Ara 2026)', 'HMB katsayı genelgesi', '2026-10-30', '2027-01-05'),
    'memur_katsayi':      ('1,575512 (Tem–Ara 2026)', 'HMB', '2026-10-30', '2027-01-05'),
    'bedelli':            ('472.653,60 TL; ek bedel 5.514,29 TL/ay', 'MSB / 1111 s.K. m.10, katsayı 1,575512', '2026-10-30', '2027-01-05'),
    'en_dusuk_emekli':    ('23.552 TL (Tem 2026–)', '7590 s.K.', '2026-10-30', '2027-01-05'),
    'damga_ucret':        ('binde 7,59; asgari ücrete isabet eden kısım istisna', '488 s.K. (1) s.tablo', '2026-10-30', '2027-01-05'),
    'gv_dilim_2026':      ('190.000 / 400.000 / 1.500.000 (ücret) / 5.300.000', 'GİB 2026 tarifesi', '2026-10-30', '2027-01-05'),
    'konut_kira_istisna': ('58.000 TL (2026 gelirleri)', 'GVK m.21', '2026-10-30', '2027-01-05'),
    'tufe_yillik':        ('Eylül 2026 %29,73', 'TÜİK', '2026-10-30', '2026-11-03'),
    'kira_artis':         ('Ekim 2026 %31,49', 'TÜİK 12 aylık ortalama', '2026-10-30', '2026-11-03'),
    'politika_faizi':     ('%36 (22.10.2026)', 'TCMB PPK', '2026-10-30', '2026-12-12'),
    'konut_faiz':         ('aylık %2,87–2,99 (16.10.2026)', 'banka web siteleri', '2026-10-30', '2026-11-30'),
    'dask':               ('betonarme 11.053 TL/m², diğer 7.369 TL/m², azami teminat 2.343.283 TL (01.06.2026)', 'dask.gov.tr tarife ve primler', '2026-10-30', '2026-11-30'),
    'taksi_tarife':       ('İstanbul 71,94 açılış / 47,92 km; Ankara 65 / 40', 'İBB UKOME 20.07.2026, ABB 1.3.2026', '2026-10-30', '2027-01-04'),
    'ihtiyac_kredisi_vade': ('≤125 bin 36 ay; 125–250 bin 24 ay; üzeri 12 ay', 'BDDK Şubat 2025', '2026-10-30', '2027-01-05'),
    'erken_odeme':        ('tüketici kredisinde tazminat yok (6502 m.27); sabit faizli konutta kalan vade <36 ay %1, üzeri %2 (m.37)', '6502 s.K.', '2026-10-30', '2027-06-30'),
    'temettu_stopaj':     ('%15 (22.12.2024–)', 'CB Kararı 2024/9286', '2026-10-30', '2027-06-30'),
    'kobi_siniri':       ('250 çalışan; net satış veya bilanço 1 milyar TL', 'KOBİ Yönetmeliği değişikliği 7.8.2025', '2026-10-30', '2027-06-30'),
    'tmsf_limit':        ('1.200.000 TL / kişi (2026)', 'TMSF', '2026-10-30', '2027-01-05'),
    'mevduat_stopaj':     ('%17,5 / %15 / %10 (9.7.2025–)', 'CB Kararı', '2026-10-30', '2027-01-05'),
}

# Eski / yanlış olduğu kesinleşmiş ifadeler (regex, açıklama). Sayfada görünen metinde geçerse HATA.
ESKI = [
    (r'[İi]şveren (?:SGK )?[Pp]ay[ıi][^.<]{0,40}%15,5', 'işveren SGK payı %15,5 değil, %21,75'),
    (r'SGK İşveren Payı \(%15,5\)', 'işveren SGK payı %15,5 değil, %21,75'),
    (r'%34,5[^.<]{0,60}(?:uzun vade|Bağ-?Kur|4/b)', '4/b prim oranı %35,75'),
    (r'(?:Bağ-?Kur|4/b)[^.<]{0,80}%34,5', '4/b prim oranı %35,75'),
    (r'63\.949', 'eski kıdem tavanı'),
    (r'22\.000\s*[–-]\s*28\.000 TL', 'DASK m² maliyeti uydurma aralık'),
    (r'5 deprem risk bölgesi', 'DASK 7 risk grubu kullanır'),
    (r'587 sayılı (?:KHK|Kanun Hükmünde Kararname) ile tüm konutlar', 'DASK artık 6305 s.K. ile düzenleniyor'),
    (r'net gelirin %25[–-]33', 'nafakada kanuni yüzde yok'),
    (r'%2 \(6 ay içinde\)', 'erken ödeme kuralı yanlış'),
    (r'6 aydan (?:önce|sonra)[^.<]{0,60}erken ödeme', 'erken ödeme kuralı yanlış'),
    (r'(?:ihtiyaç kredisi|İhtiyaç Kredisi)[^.<]{0,60}max 60 ay', 'ihtiyaç kredisi en çok 36 ay'),
    (r'Aylık %1,89', 'eski konut faizi'),
    (r'(?:vergi matrahı|matrahının) %0,759', 'damga vergisi brüt ücretten alınır'),
    (r'temettü[^.<]{0,40}stopaj \(%10\)', 'temettü stopajı %15'),
    (r'ilk 10 yıl[^.<]{0,40}%2[^.<]{0,60}%1,5', 'bağlama oranı her 360 gün %2'),
    (r'25 yılda toplam bağlama oranı', 'bağlama oranı her 360 gün %2'),
    (r'vergi aslının %25[–-]100', 'vergi ziyaı cezası kural olarak 1 kat'),
    (r'enflasyonun yaklaşık %36 seyrettiği', 'TÜFE Eylül 2026 %29,73'),
    (r'1,0 üzeri yüksek risk', 'DSÖ böyle bir eşik tanımlamaz'),
    (r'551\.845', 'bileşik faiz örneği yanlıştı (doğrusu 715.198)'),
    (r'KOBİ[^.<]{0,80}500 milyon', 'KOBİ sınırı 7.8.2025 itibarıyla 1 milyar TL'),
    (r'17\.815 ₺', 'araç kredisi örnek taksiti yanlıştı'),
    (r'~29\.500–31\.000', 'araç kredisi banka taksitleri vergisiz/yanlış hesaplanmıştı'),
    (r"ÖSYM'nin açıkladığı resmi katsayı", 'ÖSYM sabit katsayı yayımlamaz'),
    (r'ÖSYM katsayıları her yıl', 'ÖSYM sabit katsayı yayımlamaz'),
]

# Bağlam kuralları: (ad, regex — ilk grup rakamı yakalar, izinli değerler kümesi)
BAGLAM = [
    ('işveren SGK oranı',
     r'[İi]şveren (?:SGK |[Ss]igorta )?[Pp]ay[ıi][^.<%]{0,25}%(\d+,\d+)',
     {'21,75', '19,75', '16,75', '20,75', '22,75', '23,75'}),
    ('kıdem tavanı (kuruşlu)',
     r'(?:[Kk]ıdem (?:tazminatı )?tavan[ıi]|[Tt]avan (?:tutarı)?)[^.<]{0,60}?(\d{2}\.\d{3},\d{2}) TL',
     {'64.948,77', '73.729,87', '53.919,68', '46.655,43', '41.828,42', '35.058,58', '23.489,83', '19.982,83'}),
    ('SGK prim tavanı 2026',
     r'2026[^.<]{0,40}prim tavan[ıi][^.<]{0,30}?(\d{3}\.\d{3}(?:,\d{2})?) TL',
     {'297.270', '297.270,00'}),
]
