"""Mevcut blog düzenini (blog/kidem-tazminati-2027.html) şablon alarak yeni yazı üretir."""
import re, json, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, 'blog/kidem-tazminati-2027.html'), encoding='utf-8').read()


def tl(x, d=2):
    s = f"{x:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def table(head, rows, label=''):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return (f'<div style="overflow-x:auto"><table class="veri-tablo" aria-label="{label}">'
            f'<thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')


def hero(icon, badge, l1, v1, l2, v2, c1, c2):
    return f'''<div class="article-hero">
    <svg viewBox="0 0 760 340" xmlns="http://www.w3.org/2000/svg">
      <defs><linearGradient id="hg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:{c1}"/><stop offset="100%" style="stop-color:{c2}"/></linearGradient></defs>
      <rect width="760" height="340" fill="url(#hg)" rx="16"/>
      <circle cx="650" cy="60" r="120" fill="rgba(255,255,255,0.04)"/>
      <circle cx="100" cy="280" r="90" fill="rgba(255,255,255,0.04)"/>
      <circle cx="560" cy="150" r="80" fill="rgba(255,255,255,0.08)"/>
      <circle cx="560" cy="150" r="58" fill="rgba(255,255,255,0.12)"/>
      <text x="560" y="173" text-anchor="middle" font-size="56" fill="white" opacity="0.95">{icon}</text>
      <rect x="60" y="255" width="340" height="44" rx="22" fill="rgba(245,158,11,0.92)"/>
      <text x="230" y="282" text-anchor="middle" font-size="16" font-weight="bold" fill="white">{badge}</text>
      <text x="60" y="100" font-size="13" fill="rgba(255,255,255,0.6)" font-family="monospace">{l1}</text>
      <text x="60" y="126" font-size="24" font-weight="bold" fill="white">{v1}</text>
      <text x="60" y="165" font-size="13" fill="rgba(255,255,255,0.6)" font-family="monospace">{l2}</text>
      <text x="60" y="191" font-size="20" font-weight="bold" fill="white">{v2}</text>
      <text x="700" y="318" text-anchor="end" font-size="11" fill="rgba(255,255,255,0.4)">hesaplarsin.com • Ekim 2026</text>
    </svg>
  </div>'''


def make(slug, title, desc, keywords, crumb, h1, hero_html, badges, body, faq, related, date='2026-10-21', date_tr='21 Ekim 2026'):
    s = TPL
    url = f'https://hesaplarsin.com/blog/{slug}.html'
    words = len(re.sub(r'<[^>]+>', ' ', body + ' '.join(q + a for q, a in faq)).split())
    mins = max(3, round(words / 200))
    e = lambda t: html.escape(t, quote=True)
    s = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', s, count=1)
    for pat, val in [(r'(<meta name="description" content=")[^"]*', desc), (r'(<meta name="keywords" content=")[^"]*', keywords),
                     (r'(<meta property="og:title" content=")[^"]*', title.replace(' | Hesaplarsın', '')),
                     (r'(<meta property="og:description" content=")[^"]*', desc),
                     (r'(<meta property="article:published_time" content=")[^"]*', date)]:
        s = re.sub(pat, lambda m: m.group(1) + e(val), s, count=1)
    s = s.replace('https://hesaplarsin.com/blog/kidem-tazminati-2027.html', url)
    for m in re.findall(r'(<meta name="twitter:(?:title|description)" content=")[^"]*', s):
        pass
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + e(title.replace(' | Hesaplarsın', '')), s, count=1)
    s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + e(desc), s, count=1)
    # şemalar
    art = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "datePublished": date, "dateModified": date,
           "inLanguage": "tr", "mainEntityOfPage": url, "image": "https://hesaplarsin.com/assets/og-image.png",
           "author": {"@type": "Person", "name": "Duran Gönülalan", "jobTitle": "Hesaplarsın Kurucusu", "url": "https://hesaplarsin.com/hakkimizda.html#kurucu"},
           "publisher": {"@type": "Organization", "name": "Hesaplarsın", "url": "https://hesaplarsin.com", "logo": {"@type": "ImageObject", "url": "https://hesaplarsin.com/assets/icon-512.png"}}}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in faq]}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://hesaplarsin.com"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://hesaplarsin.com/blog.html"},
        {"@type": "ListItem", "position": 3, "name": crumb, "item": url}]}
    lds = re.findall(r'<script type="application/ld\+json">.*?</script>', s, re.S)
    new_ld = [json.dumps(x, ensure_ascii=False) for x in (art, fq, bc)]
    for old, new in zip(lds, new_ld):
        s = s.replace(old, f'<script type="application/ld+json">{new}</script>', 1)
    s = re.sub(r'<span>Kıdem Tazminatı 2027</span>\n</nav>', f'<span>{e(crumb)}</span>\n</nav>', s, count=1)
    # makale gövdesi
    a = s.index('<article class="article-wrap">') + len('<article class="article-wrap">')
    b = s.index('</article>')
    badge_html = ''.join(f'<span class="meta-badge{" meta-badge-hot" if i == 0 else ""}">{x}</span>\n    ' for i, x in enumerate(badges))
    faq_html = ''.join(f'''  <div class="faq-item">
    <button class="faq-q" onclick="toggleFaq(this)" aria-expanded="false">{q} <span class="ico">+</span></button>
    <div class="faq-a">{a_}</div>
  </div>
''' for q, a_ in faq)
    rel_html = ''.join(f'    <a class="related-card" href="{u}"><span class="rc-icon">{i}</span><div><h4>{t}</h4><p>{d}</p></div></a>\n' for i, t, d, u in related)
    art_html = f'''
  {hero_html}
  <div class="article-meta">
    {badge_html}<span>📅 {date_tr}</span>
    <span>⏱️ {mins} dk okuma</span>
  </div>
  <h1>{h1}</h1>
{body}
  <h2>Sık Sorulan Sorular</h2>
{faq_html}
  <p style="font-size:.8rem;color:var(--muted);margin-top:18px">Hazırlayan: <a href="https://hesaplarsin.com/hakkimizda.html#kurucu">Duran Gönülalan</a>, Hesaplarsın kurucusu · Son güncelleme: {date_tr} · Rakamların kaynakları ve güncelleme takvimi için <a href="https://hesaplarsin.com/yontem-ve-kaynaklar.html">Yöntem ve Kaynaklar</a>.</p>

  <h2>İlgili Araçlar ve Yazılar</h2>
  <div class="related-grid">
{rel_html}  </div>
'''
    s = s[:a] + art_html + s[b:]
    open(os.path.join(ROOT, f'blog/{slug}.html'), 'w', encoding='utf-8').write(s)
    import subprocess
    subprocess.run(['python3', '_gen/covers.py', slug], cwd=ROOT, check=True)
    return words, mins
