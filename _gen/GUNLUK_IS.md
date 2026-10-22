# "Günlük iş" akışı

Duran "günlük iş" yazdığında:

1. **Rakam kontrolü (otomatik yayın serbest):** O gün değişen resmî veri var mı? TÜİK enflasyonu (her ayın 3'ü / sonraki iş günü),
   kira artış oranı, TCMB PPK kararı, memur/emekli zammı, asgari ücret, kıdem tavanı, ekonomi takvimi (`tools_takvim.py` EVENTS).
   Varsa ilgili dosyaları güncelle → `python3 _gen/build.py` → `python3 _gen/sitemap.py` → `timeout 900 python3 _gen/test_pages.py` → commit/push.
2. **Yeni içerik önerisi (ONAY GEREKİR):** Tek satırda konu + neden (Search Console verisi, sezon, eksik konu).
   Duran "tamam" demeden yeni blog yazısı veya yeni araç yayına ALINMAZ.
   - Blog: scratchpad `newpost.py` deseni (blog/kidem-tazminati-2027.html şablonu) + `_gen/covers.py <slug>`; blog.html kartı ve sayısı.
   - Araç: ilgili `_gen/tools_*.py` modülü, index.html TOOLS satırı, `_gen/og.py <slug>`, gerekirse `_gen/links.py` eşleşmesi.
   - Her rakam resmî kaynakla doğrulanır; kaynak sayfaya yazılır.
3. **Özet:** 3 satır — ne güncellendi, ne yayınlandı, sıradaki öneri.

Tempo: günde en fazla 1 yeni içerik. Toplu/seri içerik üretilmez (Google "scaled content" ve AdSense riski).
Hatırlatmalar (send_later): 23 Eki 08:00Z, 2 Kas 08:00Z, 3 Kas 07:15Z, 31 Ara 07:00Z, 1 Oca 07:00Z, 4 Oca 07:15Z.
