# -*- coding: utf-8 -*-
"""Gömülebilir hesaplayıcılar (20 Kas 2026).

embed/<slug>.html : başka sitelerin iframe ile ekleyebileceği sade araç sayfası (noindex, follow)
Araç sayfasına   : "Bu hesaplayıcıyı sitenize ekleyin" kutusu (<!-- EMBED --> ... <!-- /EMBED -->, idempotent)
Gömme kodu iframe'in DIŞINDA bir kaynak linki içerir: asıl amaç doğal geri bağlantı.
"""
import os, re, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://hesaplarsin.com'
# (slug, iframe yüksekliği px, kimler için)
EMBEDS = [
    ('kira-artis-hesaplama', 620, 'emlak ofisleri ve kira blogları'),
    ('tapu-harci-hesaplama', 640, 'emlak ofisleri'),
    ('kira-stopaji-hesaplama', 620, 'muhasebe ve emlak siteleri'),
    ('konut-kredisi-hesaplama', 700, 'emlak ve inşaat firmaları'),
    ('deger-artis-kazanci-hesaplama', 700, 'emlak ofisleri ve mali müşavirler'),
    ('yillik-izin-hesaplama', 700, 'İK ve muhasebe siteleri'),
    ('asgari-ucret-2027-hesaplama', 660, 'İK, muhasebe ve haber siteleri'),
    ('kar-marji-hesaplama', 600, 'e-ticaret ve esnaf siteleri'),
    ('yas-hesaplama', 620, 'okul, kreş ve blog siteleri'),
    ('kac-gun-kaldi', 640, 'okul, haber ve blog siteleri'),
]
SLUGS = [e[0] for e in EMBEDS]


def kod(slug, name, h):
    """Kullanıcıya verilecek gömme kodu (HTML)."""
    return (f'<iframe src="{BASE}/embed/{slug}.html" title="{name}" width="100%" height="{h}" style="border:0;max-width:680px;width:100%" loading="lazy"></iframe>\n'
            f'<p style="font:13px/1.4 sans-serif;margin:4px 0 0">Kaynak: <a href="{BASE}/{slug}.html">{name} – Hesaplarsın</a></p>\n'
            '<script>addEventListener("message",function(e){if(e.origin!=="' + BASE + '"||!e.data||!e.data.hsH)return;'
            'document.querySelectorAll(\'iframe[src^="' + BASE + '/embed/"]\').forEach(function(f){if(f.contentWindow===e.source)f.style.height=e.data.hsH+"px";});});</script>')


def sayfa(spec, CSS, RUNTIME):
    name = spec['name']
    form = re.sub(r'type="number"', 'type="text" autocomplete="off"', spec['form'])
    rt = RUNTIME
    # menü (hamburger) bağımlılıklarını çıkar: gömülü sayfada menü yok
    rt = re.sub(r"\n  var hb=el\('hamBtn'\).*?\n  document\.addEventListener\('click'.*?\n", '\n', rt, flags=re.S)
    rt = rt.replace("h+='<div class=\"res-actions\"><button type=\"button\" onclick=\"kopyala()\">📋 Sonucu Kopyala</button><button type=\"button\" onclick=\"paylas()\">💬 WhatsApp’ta Paylaş</button></div>';", '')
    assert "hamBtn" not in rt, 'embed runtime: menü kodu ayıklanamadı'
    e = lambda s: html.escape(s, quote=True)
    return f'''<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE}/{spec['slug']}.html">
<title>{e(name)} – Hesaplarsın</title>
<style>{CSS}
body{{background:transparent}}.emb{{max-width:680px;margin:0 auto;padding:8px}}.emb .card{{margin:0}}
.emb-foot{{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:10px;font-size:.8rem;color:var(--muted)}}
.emb-foot a{{color:var(--brand);font-weight:700;text-decoration:none}}#toast{{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);background:#111827;color:#fff;padding:10px 16px;border-radius:8px;display:none;font-size:.9rem}}</style>
</head><body><div class="emb">
<section class="card" aria-label="{e(name)}">
  <div class="card-title">{e(spec.get('card_title', name))}</div>
  {form}
  <button class="btn-calc" type="button" onclick="run()">{e(spec.get('button', 'Hesapla'))}</button>
  <div id="result" aria-live="polite"></div>
  <div class="emb-foot"><span>Bilgi amaçlıdır.</span><a href="{BASE}/{spec['slug']}.html" target="_blank" rel="noopener">{e(name)} · Hesaplarsın</a></div>
</section></div><div id="toast"></div>
<script>{rt}
{spec['js']}
(function(){{var s=0;function h(){{var y=document.documentElement.scrollHeight;if(y!==s&&window.parent!==window){{s=y;parent.postMessage({{hsH:y}},'*');}}}}
new ResizeObserver(h).observe(document.body);addEventListener('load',h);}})();</script>
</body></html>'''


def kutu(spec, h):
    k = html.escape(kod(spec['slug'], spec['name'], h))
    return (f'<!-- EMBED --><div class="card"><div class="side-title">Bu hesaplayıcıyı sitenize ekleyin</div>'
            f'<p style="font-size:.85rem;color:var(--muted);margin:6px 0 8px">Ücretsiz. Kodu sitenize yapıştırın; rakamlar her ay burada güncellenir.</p>'
            f'<textarea readonly rows="4" style="width:100%;font:12px/1.4 monospace;padding:8px;border:1px solid var(--border);border-radius:8px" onclick="this.select()">{k}</textarea>'
            f'<a href="/sitene-hesaplayici-ekle.html" style="display:inline-block;margin-top:6px;font-size:.85rem">Diğer hesaplayıcılar ve önizleme →</a></div><!-- /EMBED -->')


def run(tools):
    import template as T
    by = {t['slug']: t for t in tools}
    os.makedirs(os.path.join(ROOT, 'embed'), exist_ok=True)
    n = 0
    for slug, h, _ in EMBEDS:
        spec = by[slug]
        open(os.path.join(ROOT, 'embed', slug + '.html'), 'w', encoding='utf-8').write(sayfa(spec, T.CSS, T.RUNTIME))
        p = os.path.join(ROOT, slug + '.html')
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<!-- EMBED -->.*?<!-- /EMBED -->', '', s, flags=re.S)
        assert s.count('<aside class="sidebar">') == 1, slug
        s = s.replace('<aside class="sidebar">', '<aside class="sidebar">\n    ' + kutu(spec, h), 1)
        open(p, 'w', encoding='utf-8').write(s)
        n += 1
    return n
