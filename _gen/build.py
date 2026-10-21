"""Kullanım: python3 _gen/build.py  (repo kökünden)"""
import os, re, sys, json, glob, importlib
sys.path.insert(0, os.path.dirname(__file__))
from template import render, BASE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def registry():
    s = open('index.html', encoding='utf-8').read()
    reg = {}
    for m in re.finditer(r"\{ico:'([^']*)',name:'([^']*)',desc:(['\"])(.*?)\3,url:'/([^']+)\.html'", s):
        reg[m.group(5)] = dict(ico=m.group(1), name=m.group(2), desc=m.group(4))
    return reg

MODULES = [m for m in ['tools_diger', 'tools_saglik', 'tools_finans', 'tools_vergi', 'tools_egitim'] if os.path.exists(os.path.join(os.path.dirname(__file__), m + '.py'))]
tools = []
for m in MODULES:
    tools += importlib.import_module(m).TOOLS

reg = registry()
reg.update({k:v for k,v in {
  'yillik-izin-hesaplama': dict(ico='🏖️', name='Yıllık İzin Hesaplama', desc='Kıdeme göre yıllık izin hakkını hesapla.'),
  'asgari-ucret-hesaplama': dict(ico='💵', name='Asgari Ücret Hesaplama', desc='2026 asgari ücret net, brüt ve işveren maliyeti.'),
}.items() if k not in reg})
for t in tools:  # yeni araçlar registry'e
    reg.setdefault(t['slug'], dict(ico=t['ico'], name=t['name'], desc=t['desc'][:60]))
only = set(sys.argv[1:])
for t in tools:
    if only and t['slug'] not in only: continue
    html = render(t, reg)
    open(t['slug'] + '.html', 'w', encoding='utf-8').write(html)
    words = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S)).split())
    print(f"{t['slug']:45s} {words:5d} kelime  title={len(t['title'])} desc={len(t['desc'])}")
json.dump({t['slug']: dict(ico=t['ico'], name=t['name'], cat=t['cat']) for t in tools}, open('_gen/built.json', 'w'), ensure_ascii=False, indent=1)
