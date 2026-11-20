# -*- coding: utf-8 -*-
"""Sayfanın ASIL İÇERİĞİ en son ne zaman değişti?  (sitemap <lastmod> için)

Menü, footer, iç link kutuları ve "Diğer araçlar" bölümü her yeni sayfada bütün sitede değiştiği için
git'in dosya tarihi lastmod olarak kullanılamaz (17 Kas 2026'da 72 sayfa aynı gün "güncellenmiş" görünüyordu;
Google böyle bir lastmod'a güvenmeyi bırakır). Burada yalnızca görünen içerik metninin özeti tutulur.
_gen/icerik_tarih.json: {sayfa: [özet, tarih]}  — özet değişirse tarih bugüne alınır.
"""
import re, html, hashlib, json, os, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, '_gen', 'icerik_tarih.json')


def icerik(s):
    i = s.find('<h1')
    if i < 0:
        i = 0
    for son in ('<!--HZ-FOOT-->', '<footer'):
        j = s.find(son, i)
        if j > 0:
            s = s[i:j]; break
    else:
        s = s[i:]
    s = re.sub(r'<!-- ICLINK -->.*?<!-- /ICLINK -->', ' ', s, flags=re.S)
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', ' ', s, flags=re.S)
    s = re.split(r'<h2[^>]*>\s*(?:Diğer Hesaplama Araçları|İlgili Araçlar ve Yazılar|İlgili Hesaplamalar)', s)[0]
    t = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    t = re.sub(r'\s+', ' ', t).strip()
    return hashlib.sha1(t.encode()).hexdigest()[:16]


def tarihten_kur(f, limit=80):
    """git geçmişinden içeriğin son değiştiği commit tarihini bulur (ilk kurulum için)."""
    out = subprocess.run(['git', 'log', f'-{limit}', '--format=%H %cs', '--', f], cwd=ROOT, capture_output=True, text=True).stdout
    revs = [r.split() for r in out.split('\n') if r.strip()]
    if not revs:
        return None
    simdi = icerik(open(os.path.join(ROOT, f), encoding='utf-8').read())
    son_ayni = revs[0][1]
    for h, d in revs:
        eski = subprocess.run(['git', 'show', f'{h}:{f}'], cwd=ROOT, capture_output=True, text=True).stdout
        if not eski or icerik(eski) != simdi:
            return son_ayni
        son_ayni = d
    return son_ayni


def guncelle(dosyalar, bugun=None):
    bugun = bugun or datetime.date.today().isoformat()
    db = json.load(open(DB, encoding='utf-8')) if os.path.exists(DB) else {}
    for f in dosyalar:
        oz = icerik(open(os.path.join(ROOT, f), encoding='utf-8').read())
        if f not in db:
            db[f] = [oz, tarihten_kur(f) or bugun]
        elif db[f][0] != oz:
            db[f] = [oz, bugun]
    json.dump(db, open(DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    return {f: db[f][1] for f in dosyalar}
