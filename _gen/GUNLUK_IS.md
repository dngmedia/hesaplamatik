# "Günlük iş" akışı

> **ÖNCE BUNU OKU — AdSense durumu (Duran'ın kalıcı talimatı: her işte göz önünde bulundur)**
> AdSense 2 kez reddedildi (ilki Ekim başı, ikincisi 31 Eki 2026), sebep: **"Düşük değere sahip içerik"**.
> Google'ın istediği üç şey ve bizdeki eksik:
> 1. *Özgün ve yüksek kaliteli bilgi/araç* → kopyası her yerde olan genel araçlar yerine kimsede olmayan veri ve araç; her rakam kaynaklı ve doğru.
> 2. *Sürekli içerik seçimi ve yapısal istikrar* → 9–30 Eki arası 98 commit, sayfa sayısı ~70'ten 148'e çıktı. Artık büyük yapı değişikliği ve toplu sayfa yok; haftada en fazla 2–3 seçilmiş yeni sayfa.
> 3. *Gerçek kullanıcı ilgisi* → Ekim'de Google'dan günde 2–5 tıklama. Asıl eksik trafik ve marka varlığı (dizin kayıtları, basın bülteni, dış link).
> Yeniden başvuru: en erken Aralık ortası, şu şartlar oturunca — günlük organik kullanıcı düzenli 100+ (kendi hedefimiz, resmî eşik değil), sayfaların neredeyse tamamı dizinde, 3–4 hafta yapısal değişiklik yok.
> Her iş seçilirken sor: bu, üç maddeden hangisini iyileştiriyor? Hiçbirini değilse önceliği düşük.


Duran "günlük iş" yazdığında:

1. **Rakam kontrolü (otomatik yayın serbest):** O gün değişen resmî veri var mı? TÜİK enflasyonu (her ayın 3'ü / sonraki iş günü),
   kira artış oranı, TCMB PPK kararı, memur/emekli zammı, asgari ücret, kıdem tavanı, ekonomi takvimi (`tools_takvim.py` EVENTS).
   Varsa ilgili dosyaları güncelle → `python3 _gen/build.py` → `python3 _gen/sitemap.py` → `timeout 900 python3 _gen/test_pages.py` → commit/push.
2. **Yeni içerik (onay gerekmez — Duran 24 Eki 2026'da onay şartını kaldırdı):** Search Console (Composio google_search_console) ve
   OpenSEO (proje 5f618f92…, anahtar kelime hacmi/zorluk; krediyi idareli kullan) verisine göre en değerli konuyu seç, yap, yayınla, özette nedenini yaz.
   - Blog: scratchpad `newpost.py` deseni (blog/kidem-tazminati-2027.html şablonu) + `_gen/covers.py <slug>`; blog.html kartı ve sayısı.
   - Araç: ilgili `_gen/tools_*.py` modülü, index.html TOOLS satırı, `_gen/og.py <slug>`, gerekirse `_gen/links.py` eşleşmesi.
   - Her rakam resmî kaynakla doğrulanır; kaynak sayfaya yazılır.
3. **Özet:** 3 satır — ne güncellendi, ne yayınlandı, sıradaki öneri.

Tempo: günde en fazla 1 yeni içerik. Toplu/seri içerik üretilmez (Google "scaled content" ve AdSense riski).
Hatırlatmalar (send_later): 23 Eki 08:00Z, 2 Kas 08:00Z, 3 Kas 07:15Z, 31 Ara 07:00Z, 1 Oca 07:00Z, 4 Oca 07:15Z.

## Doğruluk kuralları (30 Eki 2026'dan itibaren zorunlu)

- **Tek doğruluk kaynağı:** `_gen/veri.py`. Resmî rakam (asgari ücret, SGK oranları, kıdem tavanı, katsayı, DASK, faiz, TÜFE…) değişince önce burası güncellenir: değer, kaynak, `dogrulandi`, `kontrol` tarihi. Eski değer `ESKI` listesine eklenir.
- **Otomatik denetim:** `python3 _gen/dogrula.py` — build sonunda ve `test_pages.py` içinde çalışır; `.githooks/pre-push` hata varken push'u engeller (yeni klonda `git config core.hooksPath .githooks`). GitHub Actions `dogruluk.yml` her push'ta ve her sabah çalışır.
  1. ESKI: bilinen eski/yanlış ifade sayfada kalmışsa hata.
  2. BAGLAM: işveren SGK oranı, kıdem tavanı, prim tavanı gibi rakamlar izinli değer dışındaysa hata.
  3. HESAP: sayfadaki "A × B = C" ve "A = B = C" zincirleri yeniden hesaplanır; tutmazsa hata.
  4. TARİH: `kontrol` tarihi geçen veri hata verir → resmî kaynaktan yeniden doğrula, tarihi ileri al.
- **Yeni içerik yazarken:** örnek tablo/hesap elle yazılmaz, Python ile hesaplanıp sayfaya basılır. Örnek hesabı mümkünse "A × B = C" biçiminde de yaz ki denetim yakalayabilsin. Kaynaksız oran (sektör ortalaması, "yaygın oran") yazılmaz; yazılırsa "resmî değildir" notu düşülür.
- **"Bu ay" bilgisi** (faiz, kur, tarife) her zaman tarihle yazılır ve `veri.py`'de kontrol tarihi olur.
