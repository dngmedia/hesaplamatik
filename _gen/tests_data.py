TESTS = {
 'yas-hesaplama': [dict(fill={'dogum': '1995-03-15', 'hedef': '2026-10-21'}, expect='31 yaş 7 ay 6 gün'), dict(fill={}, expect_toast='doğum')],
 'gun-hesaplama': [dict(fill={'t1': '2026-03-01', 't2': '2026-06-15'}, expect='106 gün'),
                   dict(radio={'mod': 'ekle'}, fill={'t1': '2026-01-01', 'gun': '90'}, expect='1 Nisan 2026')],
 'is-gunu-hesaplama': [dict(fill={'t1': '2026-01-01', 't2': '2026-12-31'}, uncheck=['arife']),
                       dict(fill={'t1': '2026-05-25', 't2': '2026-05-31'}),
                       dict(radio={'mod': 'ekle'}, fill={'t1': '2026-05-22', 'n': '3'})],
 'ortalama-hesaplama': [dict(fill={'sayilar': '85 70 92 64 78'}, expect='77,8'),
                        dict(radio={'mod': 'agirlikli'}, fill={'sayilar': '80 90 60', 'agirlik': '4 5 2'}, expect='80,9')],
 'indirim-hesaplama': [dict(fill={'normal': '1500', 'oran': '30'}, expect='1.050,00'),
                       dict(fill={'normal': '100', 'oran': '20', 'oran2': '10'}, expect='72,00'),
                       dict(radio={'mod': 'oran'}, fill={'normal': '1200', 'indirimli': '900'}, expect='%25'),
                       dict(radio={'mod': 'eski'}, fill={'indirimli': '800', 'oran': '20'}, expect='1.000,00')],
 'veri-kullanim-hesaplama': [dict(fill={'video': '60', 'sosyal': '45', 'muzik': '30'})],
 'internet-hizi-donusturucu': [dict(fill={'deger': '100'}, expect='12,50')],
 'yakit-tuketimi-hesaplama': [dict(fill={'km': '520', 'litre': '34,5', 'fiyat': '47,50', 'depo': '50'}, expect='6,63')],
 'yakit-maliyeti-hesaplama': [dict(fill={'km': '450', 'tuketim': '6,5', 'fiyat': '47,50', 'kisi': '3'}, check=['gd'], expect='2.778,75')],
}
TESTS.update({
 'vucut-kitle-indeksi': [dict(fill={'boy': '172', 'kilo': '74'}, expect='25,0')],
 'ideal-kilo-hesaplama': [dict(fill={'boy': '168', 'kilo': '70'})],
 'gunluk-kalori-ihtiyaci-hesaplama': [dict(radio={'cins': 'e'}, fill={'yas': '30', 'boy': '175', 'kilo': '75'}, expect='2.336')],
 'kalori-yakma-hesaplama': [dict(fill={'kilo': '70', 'sure': '45'}, expect='193')],
 'protein-ihtiyaci-hesaplama': [dict(fill={'kilo': '70'})],
 'su-ihtiyaci-hesaplama': [dict(fill={'kilo': '70', 'spor': '30', 'hava': '0.5'}, expect='3,2')],
 'hedef-kilo-suresi-hesaplama': [dict(fill={'boy': '170', 'kilo': '85', 'hedef': '75'}, expect='20 hafta'), dict(fill={'boy': '170', 'kilo': '60', 'hedef': '48'}, expect='VKİ')],
 'vucut-yag-orani-hesaplama': [dict(radio={'cins': 'e'}, fill={'boy': '175', 'kilo': '78', 'boyun': '38', 'bel': '86'}), dict(fill={'boy': '165', 'boyun': '33', 'bel': '75', 'kalca': '98'})],
})
TESTS.update({
 'kredi-erken-kapama-hesaplama': [dict(fill={'tutar': '300.000', 'faiz': '3,49', 'vade': '36', 'odenen': '12'}), dict(fill={'tutar': '2000000', 'faiz': '2,5', 'vade': '120', 'odenen': '24', 'tur': 'konut-sabit'})],
 'roi-hesaplama': [dict(fill={'maliyet': '50000', 'getiri': '68000', 'sure': '18'}, expect='%36,00')],
 'yatirim-geri-donus-suresi-hesaplama': [dict(fill={'yatirim': '1.200.000', 'nakit': '25000'}, expect='4 yıl 0 ay'), dict(fill={'yatirim': '1200000', 'nakit': '25000', 'artis': '25', 'iskonto': '30'})],
 'iskonto-hesaplama': [dict(fill={'fiyat': '10000', 'oranlar': '20 10 5'}, expect='6.840,00'), dict(radio={'mod': 'senet'}, fill={'nominal': '100000', 'gun': '90', 'faiz': '45'})],
 'kira-getirisi-hesaplama': [dict(fill={'fiyat': '4500000', 'kira': '22000', 'masraf': '180000', 'gider': '15000', 'bos': '1', 'artis': '30'})],
 'kira-artis-hesaplama': [dict(fill={'kira': '20000'}, expect='26.298,00'), dict(fill={'kira': '20000', 'anlasma': '25'}, expect='25.000,00')],
 'metrekare-fiyat-hesaplama': [dict(fill={'f1': '3850000', 'm1': '110', 'f2': '4000000', 'm2': '120', 'hedefm': '125'}, expect='35.000')],
 'kar-zarar-hesaplama': [dict(fill={'alis': '750', 'satis': '1000'}, expect='250,00')],
 'kar-marji-hesaplama': [dict(fill={'maliyet': '400', 'satis': '560'}, expect='%28,57'), dict(radio={'mod': 'fiyat'}, fill={'maliyet': '400', 'hedef': '30'}, expect='571,43')],
 'net-kar-hesaplama': [dict(fill={'gelir': '1500000', 'smm': '900000', 'faal': '350000', 'diger': '-20000'}, expect='172.500,00')],
 'stok-karliligi-hesaplama': [dict(fill={'bas': '400000', 'son': '500000', 'satis': '2700000', 'smm': '1800000'}, expect='4,00')],
 'prim-hesaplama': [dict(fill={'satis': '850000', 'oran': '3'}, expect='25.500,00'), dict(radio={'mod': 'kademe'}, fill={'satis': '850000'}, expect='16.500,00'), dict(radio={'mod': 'hedef'}, fill={'satis': '850000', 'oran': '3', 'hedef': '600000'}, expect='7.500,00')],
 'maas-zam-hesaplama': [dict(fill={'maas': '45000', 'oran': '30', 'enf': '29,73'}, expect='58.500,00')],
 'saatlik-ucret-hesaplama': [dict(fill={'tutar': '45000'}, expect='200,00')],
 'mtv-hesaplama': [dict(fill={'cc': '1', 'yas': '0', 'deger': '650000'}, expect='12.028'), dict(fill={'tescil': 'eski', 'cc': '3', 'yas': '2'}, expect='12.624'), dict(fill={'tip': 'moto', 'cc': '1', 'yas': '0'}, expect='2.214')],
 'otv-hesaplama': [dict(fill={'fiyat': '900000', 'otv': '80'}, expect='1.944.000,00'), dict(radio={'mod': 'geri'}, fill={'fiyat': '1944000', 'otv': '80'}, expect='900.000,00')],
 'tapu-harci-hesaplama': [dict(fill={'bedel': '3500000'}, expect='140.000,00')],
 'damga-vergisi-hesaplama': [dict(fill={'tutar': '1000000', 'nusha': '2'}, expect='18.960,00'), dict(fill={'tur': '1.89', 'tutar': '20000', 'ay': '12'}, expect='453,60')],
 'asgari-ucret-hesaplama': [dict(fill={}, expect='28.075,50')],
 'yillik-izin-hesaplama': [dict(fill={'giris': '2019-02-01', 'dogum': '1975-05-10', 'hedef': '2026-10-21', 'kullanilan': '60', 'brut': '45000'}, expect='20 gün'), dict(fill={'giris': '2026-01-01', 'dogum': '1990-01-01'})],
 'emeklilik-yasi-hesaplama': [dict(fill={'dogum': '1975-03-01', 'giris': '1995-06-01', 'prim': '6000'}), dict(fill={'dogum': '1980-03-01', 'giris': '2003-06-01'}), dict(radio={'cins': 'k'}, fill={'dogum': '1990-03-01', 'giris': '2010-06-01'})],
 'enflasyon-hesaplama': [dict(fill={'tutar': '1000', 'y1': '2023', 'y2': '2025'}, expect='1.889'), dict(radio={'mod': 'gelecek'}, fill={'tutar': '1000', 'oran': '25', 'yil': '5'})],
 'elektrik-faturasi-hesaplama': [dict(fill={'kwh': '230', 'birim': '3,2'}, expect='736,00'), dict(radio={'mod': 'cihaz'}, fill={'watt': '1200', 'saat': '6', 'birim': '3,2'}, expect='691,20')],
 'dogalgaz-faturasi-hesaplama': [dict(fill={'m3': '180', 'birim': '1,2'})],
 'su-faturasi-hesaplama': [dict(fill={'m3': '15', 'su': '40', 'atik': '20'}, expect='909,00')],
 'tyt-net-hesaplama': [dict(fill={'trd': '32', 'try': '6', 'matd': '25', 'maty': '8', 'dip': '85'}, expect='53,50')],
 'kpss-net-hesaplama': [dict(fill={'trd': '25', 'try': '4', 'tard': '20', 'tary': '4'}, expect='43,00')],
 'not-ortalamasi-hesaplama': [dict(fill={}, expect_toast='En az bir ders')],
 'takdir-tesekkur-hesaplama': [dict(fill={}, expect_toast='Derslerinize')],
})
TESTS['takdir-tesekkur-hesaplama'].append(dict(fill={}, js="document.querySelectorAll('#dersler .ders').forEach(function(d,i){d.children[1].value=[80,90,85,75,88,95,100,90][i];});", expect='TAKDİR'))
TESTS['memur-emekli-zammi-hesaplama']=[dict(fill={'tur':'emekli','maas':'50.000','aylik':'1'}, expect='54.384'), dict(fill={'tur':'memur','maas':'50000','aylik':'1'}, expect='53.367'), dict(fill={'tur':'memuremekli','maas':'30000','alti':'10'}, expect='32.383')]
TESTS['memur-maaslari']=[dict(fill={'aylik':'1'}, expect='88.897'), dict(fill={'unvan':'0','maas':'100.000','aylik':'1'}, expect='106.73')]
TESTS['ogretmen-maasi']=[dict(fill={'aylik':'1'}, expect='88.897')]
TESTS['polis-maasi']=[dict(fill={'aylik':'1'}, expect='98.89')]
TESTS['hemsire-maasi']=[dict(fill={'aylik':'1'}, expect='90.59')]
TESTS['doktor-maasi']=[dict(fill={'aylik':'1'}, expect='182.266')]
TESTS['issizlik-maasi-hesaplama']=[dict(fill={'brut':'50.000','gun':'180'}, expect='19.848,20'), dict(fill={'brut':'90000','gun':'300'}, expect='26.223,44'), dict(fill={'brut':'40000','gun':'0'}, expect_toast='600 gün')]
TESTS['muhendis-maasi']=[dict(fill={'aylik':'1'}, expect='116.57')]
TESTS['ekonomi-takvimi']=[dict(fill={'grup':'enflasyon'}, expect='gün'), dict(fill={'grup':'faiz'})]
TESTS['maas-siralamasi']=[dict(fill={'maas':'42.000'}, expect='En üst'), dict(fill={'maas':'28075,50'}, expect='46,7'), dict(fill={'maas':'20000'}, expect='Alt %25'), dict(fill={'maas':'150000'}, expect='≈')]
