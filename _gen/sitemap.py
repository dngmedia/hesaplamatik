"""sitemap.xml'i dosyalardan yeniden üretir. Yönlendirme sayfaları hariç tutulur."""
import os, glob, subprocess, datetime
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE='https://hesaplarsin.com/'
POP={'kdv-hesaplama.html','net-maas-hesaplama.html','kredi-hesaplama.html','yuzde-hesaplama.html','asgari-ucret-hesaplama.html','kidem-tazminati-hesaplama.html','enflasyon-hesaplama.html','kira-artis-hesaplama.html','tyt-net-hesaplama.html','yas-hesaplama.html','vucut-kitle-indeksi.html','gelir-vergisi-hesaplama.html'}
LEGAL={'gizlilik-politikasi.html','kullanim-sartlari.html','hakkimizda.html','iletisim.html'}
def lastmod(f):
    d=subprocess.run(['git','log','-1','--format=%cs','--',f],capture_output=True,text=True).stdout.strip()
    if subprocess.run(['git','diff','--quiet','HEAD','--',f]).returncode: d=datetime.date.today().isoformat()
    return d or datetime.date.today().isoformat()
urls=[]
for f in sorted(glob.glob('*.html')+glob.glob('blog/*.html')):
    s=open(f,encoding='utf-8').read()
    if 'http-equiv="refresh"' in s or 'noindex' in s or f.startswith(('yandex_','google')): continue
    loc=BASE+('' if f=='index.html' else f)
    pr='1.0' if f=='index.html' else '0.9' if f in POP else '0.3' if f in LEGAL else '0.7' if f.startswith('blog') else '0.8'
    cf='weekly' if f in ('index.html','blog.html') or f in POP else 'monthly'
    urls.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod(f)}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>')
open('sitemap.xml','w',encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(urls)+'\n</urlset>\n')
print(len(urls),'URL')
