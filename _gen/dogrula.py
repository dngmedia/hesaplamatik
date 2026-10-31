# -*- coding: utf-8 -*-
"""
Doğruluk denetimi — her build ve testte çalışır.  Kullanım:  python3 _gen/dogrula.py [sayfa.html ...]
Çıkış kodu = hata sayısı (0 ise temiz).  Kurallar ve güncel değerler: _gen/veri.py
"""
import os, re, sys, glob, html, datetime, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import veri

# Hesap doğrulamasından muaf tutulan, bilinçli olarak yuvarlanmış/bağlamlı ifadeler: (dosya, ifade parçası)
MUAF = set()


def gorunur_metin(s):
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'<(?:br|/p|/li|/tr|/h\d|/div|/ul|/ol|/table)\b[^>]*>', ' \n', s)
    s = re.sub(r'</(?:td|th)>', ' | ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s).replace('\xa0', ' ')
    return [re.sub(r'[ \t]+', ' ', l).strip() for l in s.split('\n') if l.strip()]


# ---------- sayı ayrıştırma (Türkçe biçim) ----------
NUM = r'\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?'

def tr2f(t):
    t = t.strip()
    if ',' in t:
        return float(t.replace('.', '').replace(',', '.'))
    if re.fullmatch(r'\d{1,3}(?:\.\d{3})+', t):
        return float(t.replace('.', ''))
    return float(t)

def ondalik(t):
    return len(t.split(',')[1]) if ',' in t else 0


# ---------- ifade hesaplama ----------
TOK = re.compile(r'\s*(%\s*(?:' + NUM + r')|(?:' + NUM + r')\s*%?|[×x\*÷/\+\-−\^\(\)])')

def hesapla(expr):
    toks, pos = [], 0
    expr = expr.strip()
    while pos < len(expr):
        m = TOK.match(expr, pos)
        if not m:
            return None
        toks.append(m.group(1).strip()); pos = m.end()
    py = []
    for t in toks:
        if t in ('×', 'x', '*'): py.append('*')
        elif t in ('÷', '/'): py.append('/')
        elif t in ('-', '−'): py.append('-')
        elif t == '^': py.append('**')
        elif t in '+()': py.append(t)
        else:
            pct = '%' in t
            v = tr2f(t.replace('%', '').strip())
            py.append(repr(v / 100 if pct else v))
    if not any(o in py for o in ('*', '/', '**')):
        return None
    try:
        return eval(''.join(py), {'__builtins__': {}})
    except Exception:
        return None

# "A × B = C" (ve "A = B = C" zinciri) kalıbı: aritmetik parçalar '=' ile ayrılır
ARITH = r'[\d\.,%×÷\+\-−\^\(\)/ ]+'
ZINCIR = re.compile(r'(?<![\w\d])(' + ARITH + r'(?:=\s*(?:≈|~|yaklaşık)?' + ARITH + r')+)')

def _deger(seg):
    seg = seg.strip().rstrip('.,').strip()
    seg = seg.strip().strip('()') if seg.strip().count('(') != seg.strip().count(')') else seg.strip()
    seg = seg.strip()
    if not seg:
        return None, None
    if re.fullmatch(r'\d{1,2}/\d', seg):
        return None, None  # derece/kademe gösterimi (1/4), bölme değil
    if re.fullmatch(r'%?\s*(?:' + NUM + r')\s*%?', seg):
        t = seg.replace('%', '').strip()
        return tr2f(t), t
    return hesapla(seg), None

def hesap_kontrol(dosya, satirlar):
    hatalar = []
    # '=' veya '≈' ile başlayan satır bir öncekinin devamıdır
    birlesik = []
    for l in satirlar:
        if birlesik and re.match(r'^[=≈]', l):
            birlesik[-1] += ' ' + ('= ' + l[1:] if l.startswith('≈') else l)
        else:
            birlesik.append(l)
    for l in birlesik:
        l = l.replace('[', '(').replace(']', ')')
        for m in ZINCIR.finditer(l):
            zincir = m.group(1)
            if not re.search(r'[×÷\^/]', zincir):
                continue
            parcalar = [re.sub(r'^\s*(?:≈|~|yaklaşık)', '', p) for p in zincir.split('=')]
            yakl = bool(re.search(r'=\s*(?:≈|~|yaklaşık)', zincir))
            # "a×b = X + c×d = Y" liste yazımı: X'ten sonra yeni zincir başlar
            duz = []
            for i, p in enumerate(parcalar):
                mm = re.match(r'^\s*(' + NUM + r')\s*[+\-−]\s*(.*\S.*)$', p) if i else None
                if mm and duz and duz[-1][0] is not None and abs(abs(duz[-1][0][0] or 0) - tr2f(mm.group(1))) <= max(1, tr2f(mm.group(1)) * 0.006):
                    duz.append(((tr2f(mm.group(1)), mm.group(1)), p))
                    duz.append((None, None))
                    duz.append((_deger(mm.group(2)), mm.group(2)))
                else:
                    duz.append((_deger(p), p))
            ciftler = [(a, b) for a, b in zip(duz, duz[1:]) if a[0] is not None and b[0] is not None]
            for ((v1, t1), p1), ((v2, t2), _p2) in ciftler:
                if v1 is None or v2 is None or t1 is not None and t2 is not None:
                    continue  # iki düz sayı ya da çözülemeyen parça
                if (dosya, p1.strip()) in MUAF:
                    continue
                birim = 10 ** (-ondalik(t2)) if t2 else 0.01
                tol_abs = max(birim, 1.0) if t2 is not None and ondalik(t2) == 0 else birim
                tol_rel = 0.02 if yakl else 0.006
                ok = any(abs(abs(a) - abs(v2)) <= max(tol_abs, abs(v2) * tol_rel) for a in (v1, v1 * 100, v1 / 100))
                if not ok:
                    hatalar.append(f'{dosya}: HESAP TUTMUYOR → "{zincir.strip()[:120]}" ({p1.strip()} ≈ {v1:,.4g}, yazılan {v2:,.4g})')
    return hatalar


def eski_kontrol(dosya, metin):
    out = []
    for rx, neden in veri.ESKI:
        for m in re.finditer(rx, metin, flags=re.I):
            out.append(f'{dosya}: ESKİ/YANLIŞ İFADE → "{m.group(0)[:90]}" ({neden})')
    return out


def baglam_kontrol(dosya, metin):
    out = []
    for ad, rx, izin in veri.BAGLAM:
        for m in re.finditer(rx, metin):
            if m.group(1) not in izin:
                out.append(f'{dosya}: {ad} beklenmeyen değer {m.group(1)} → "{m.group(0)[:100]}"')
    return out


def tarih_kontrol(bugun=None):
    bugun = bugun or datetime.date.today()
    out = []
    for k, (deger, kaynak, dog, kontrol) in veri.FACTS.items():
        if datetime.date.fromisoformat(kontrol) < bugun:
            out.append(f'veri.py: "{k}" kontrol tarihi geçti ({kontrol}) → resmî kaynaktan yeniden doğrula ({kaynak}), değer/tarih güncelle')
    return out


def sayfalar():
    fs = glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'blog', '*.html'))
    return sorted(f for f in fs if not os.path.basename(f).startswith(('google', '404')))


def run(dosyalar=None, tarih=True):
    hatalar = []
    for f in dosyalar or sayfalar():
        rel = os.path.relpath(f, ROOT)
        s = open(f, encoding='utf-8').read()
        satirlar = gorunur_metin(s)
        metin = ' \n'.join(satirlar)
        hatalar += eski_kontrol(rel, metin)
        hatalar += baglam_kontrol(rel, metin)
        hatalar += hesap_kontrol(rel, satirlar)
    if tarih:
        hatalar += tarih_kontrol()
    return hatalar


if __name__ == '__main__':
    args = [os.path.abspath(a) for a in sys.argv[1:]]
    h = run(args or None)
    for x in h:
        print('✗', x)
    print('DOĞRULUK HATASI:', len(h))
    sys.exit(min(len(h), 100))
