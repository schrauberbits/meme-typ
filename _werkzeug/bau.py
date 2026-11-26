#!/usr/bin/env python3
"""Baut den Meme-Typ-Test: index.html (de), en/index.html, 8+8 Typ-Seiten, Vorschaubilder,
sitemap.xml, robots.txt, urls.txt.  Aufruf: python3 _werkzeug/bau.py [--ohne-bilder]"""
import html, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)
D = json.load(open(os.path.join(HIER, "daten.json"), encoding="utf-8"))
VORLAGE = open(os.path.join(HIER, "vorlage.html"), encoding="utf-8").read()
BASIS = D["basis"]
INDEXNOW = "04fadd290f4b124950e8f09ef381b6ff"
e = html.escape
MEME = {m["id"]: m for m in D["memes"]}
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23111318'/%3E"
           "%3Ctext x='32' y='44' font-family='Arial,Helvetica,sans-serif' font-size='34' font-weight='700' fill='%23fff' text-anchor='middle'%3EM%3C/text%3E%3C/svg%3E")

FUSS = {
    "de": ('Ein Spaßtest, kein psychologischer Test. Meme-Vorlagen © ihre jeweiligen Urheber; die Bilder werden von '
           '<a href="https://imgflip.com/memetemplates">imgflip.com</a> geladen. Bewusst ohne Fotos von Prominenten und ohne Figuren aus Filmen und Serien.<br>'
           'Kostenlos, ohne Anmeldung, ohne Werbung; deine Reihenfolge bleibt auf deinem Gerät (nur im Link, wenn du teilst). '
           'Aufrufe werden anonym und ohne Cookies gezählt (GoatCounter). Ein Hobbyprojekt, mit KI-Hilfe erstellt; das Programm selbst nutzt keine KI.<br>'
           'Mehr Helfer: <a href="https://schrauberbits.github.io/pro-person/">Mengen pro Person</a> · <a href="https://schrauberbits.github.io/feuerwerk-helfer/">Feuerwerk-Helfer</a>'),
    "en": ('Just for fun, not a psychological test. Meme templates © their respective creators; images are loaded from '
           '<a href="https://imgflip.com/memetemplates">imgflip.com</a>. Deliberately without photos of celebrities and without characters from films or TV shows.<br>'
           'Free, no sign-up, no ads; your ranking stays on your device (only in the link if you share). '
           'Visits are counted anonymously without cookies (GoatCounter). A hobby project made with AI help; the test itself uses no AI.'),
}
TXT = {
    "de": dict(title="Welcher Meme-Typ bist du? Der Meme-Persönlichkeitstest", desc="Ordne 16 klassische Meme-Vorlagen wie This Is Fine, Two Buttons und Expanding Brain nach deinem Geschmack – deine Rangfolge verrät, welcher von 8 Meme-Typen du bist. Kostenlos, ohne Anmeldung, 2 Minuten.",
               eyebrow="Meme-Persönlichkeitstest", h1="Welcher Meme-Typ bist du?", sub="Zieh die Memes von links nach rechts in deine Reihenfolge – 4 Runden, etwa 2 Minuten. Aus deiner Rangfolge ergibt sich dein Humor-Profil.",
               runde1="Runde 1 von 4", pool="Memes", ziel="Deine Reihenfolge", hint="Antippen oder nach rechts ziehen", weiter="Weiter",
               facts=["Ohne Anmeldung", "Kostenlos", "Deine Auswahl bleibt auf deinem Gerät"],
               howE="Ablauf", howT="So funktioniert der Test", how=["In jeder der 4 Runden siehst du links 4 klassische Memes.", "Ordne sie rechts in deine Reihenfolge – Platz 1 ist dein Favorit.", "Aus allen Rangfolgen ergeben sich dein Humor-Profil auf 4 Achsen und einer von 8 Meme-Typen."],
               typenE="Ergebnisse", typenT="Die 8 Meme-Typen", sw="English", noscript="Der Test braucht JavaScript. Die 8 Meme-Typen findest du weiter unten als einzelne Seiten."),
    "en": dict(title="Which meme type are you? The meme personality test", desc="Rank 16 classic meme templates like This Is Fine, Two Buttons and Expanding Brain by taste – your ranking reveals which of 8 meme types you are. Free, no sign-up, 2 minutes.",
               eyebrow="Meme personality test", h1="Which meme type are you?", sub="Move the memes from left to right in your order – 4 rounds, about 2 minutes. Your ranking reveals your humor profile.",
               runde1="Round 1 of 4", pool="Memes", ziel="Your order", hint="Tap or drag to the right", weiter="Next",
               facts=["No sign-up", "Free", "Your choices stay on your device"],
               howE="How it works", howT="How the test works", how=["In each of the 4 rounds you see 4 classic memes on the left.", "Put them in your order on the right – spot 1 is your favorite.", "All your rankings add up to a humor profile on 4 axes and one of 8 meme types."],
               typenE="Results", typenT="The 8 meme types", sw="Deutsch", noscript="The test needs JavaScript. You can browse the 8 meme types as separate pages below."),
}


def typ_url(ty, lang):
    return BASIS + ("typ/%s/" % ty["slug_de"] if lang == "de" else "en/type/%s/" % ty["slug_en"])


def schreibe(rel, text):
    p = os.path.join(WURZEL, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


def bild(m, cover=True):
    return '<img src="%s" alt="%s" referrerpolicy="no-referrer" loading="lazy" decoding="async"%s>' % (e(m["img"]), e(m["name"]), ' style="object-fit:cover"' if cover else "")


def typkarten(lang, ohne=None):
    return "".join('<a class="tcard" href="%s"><div class="th">%s</div><div class="t">%s<small>%s</small></div></a>' % (
        e(typ_url(ty, lang)), bild(MEME[ty["meme"]]), e(ty[lang]["name"]), e(MEME[ty["meme"]]["name"])) for ty in D["typen"] if ty is not ohne)


def startseite(lang):
    x = TXT[lang]
    r = {
        "LANG": lang, "TITLE": e(x["title"]), "DESC": e(x["desc"]), "FAVICON": FAVICON,
        "CANON": BASIS if lang == "de" else BASIS + "en/", "ALT_DE": BASIS, "ALT_EN": BASIS + "en/",
        "OG": BASIS + "og/start-%s.png" % lang, "HOME": "./", "LANG_SWITCH": x["sw"],
        "EYEBROW": e(x["eyebrow"]), "H1": e(x["h1"]), "SUB": e(x["sub"]), "RUNDE1": e(x["runde1"]), "POOL": e(x["pool"]), "ZIEL": e(x["ziel"]),
        "HINT": e(x["hint"]), "WEITER": e(x["weiter"]), "FACTS": "".join("<span>%s</span>" % e(s) for s in x["facts"]),
        "NOSCRIPT": e(x["noscript"]), "HOW_E": e(x["howE"]), "HOW_T": e(x["howT"]),
        "HOW": "".join('<div class="step"><b>%d</b><p>%s</p></div>' % (k + 1, e(s)) for k, s in enumerate(x["how"])),
        "TYPEN_E": e(x["typenE"]), "TYPEN_T": e(x["typenT"]), "TYPEN_KARTEN": typkarten(lang), "FUSS": FUSS[lang],
        "DATEN": json.dumps({"basis": BASIS, "achsen": D["achsen"], "memes": D["memes"], "typen": D["typen"]}, ensure_ascii=False),
        "FUSS_DE_JS": json.dumps(FUSS["de"], ensure_ascii=False), "FUSS_EN_JS": json.dumps(FUSS["en"], ensure_ascii=False),
    }
    s = VORLAGE
    for k, v in r.items():
        s = s.replace("{{%s}}" % k, v)
    assert "{{" not in s, s[s.index("{{"):s.index("{{") + 40]
    return s


TYP_CSS = """:root{--bg:#f6f6f4;--surface:#fff;--ink:#111318;--ink2:#3b3f47;--muted:#6b7079;--line:#e4e4e0;--accent:#e4472b;--shadow:0 1px 2px rgba(16,18,24,.06),0 4px 16px rgba(16,18,24,.06)}
*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit}.bar{background:var(--surface);border-bottom:1px solid var(--line)}.bar .in{max-width:1080px;margin:0 auto;padding:12px 20px;display:flex;justify-content:space-between;align-items:center}
.logo{display:flex;align-items:center;gap:10px;font-weight:700;text-decoration:none}.logo i{width:28px;height:28px;border-radius:8px;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:.9rem;font-weight:800}
.sw{font-size:.85rem;color:var(--ink2);border:1px solid var(--line);border-radius:8px;padding:6px 12px;text-decoration:none;background:var(--surface)}
.main{max-width:1080px;margin:0 auto;padding:32px 20px 56px}.eyebrow{font-size:.78rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.kopf{display:grid;grid-template-columns:300px 1fr;gap:32px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:26px;box-shadow:var(--shadow)}
.mask{border-radius:12px;overflow:hidden;background:#f3f3f0;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center}.mask img{width:100%;height:100%;object-fit:contain}
h1{font-size:clamp(1.8rem,4vw,2.6rem);letter-spacing:-.022em;line-height:1.1;margin:6px 0 12px}.kopf p{color:var(--ink2);margin:0 0 16px}
dl{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;margin:0 0 20px;font-size:.95rem}dt{color:var(--muted)}dd{margin:0}
.btn{display:inline-flex;align-items:center;justify-content:center;background:var(--accent);color:#fff;font-weight:600;padding:13px 22px;border-radius:10px;text-decoration:none}.btn:hover{background:#c93a20}
.section{margin-top:44px;padding-top:32px;border-top:1px solid var(--line)}.section h2{font-size:1.4rem;letter-spacing:-.015em;margin:6px 0 18px}
.types{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.tcard{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;transition:box-shadow .15s,transform .15s}
.tcard:hover{box-shadow:var(--shadow);transform:translateY(-2px)}.tcard .th{aspect-ratio:4/3;background:#f1f1ee;overflow:hidden}.tcard .th img{width:100%;height:100%;display:block}
.tcard .t{padding:12px 14px;font-weight:600;font-size:.95rem}.tcard .t small{display:block;font-weight:400;color:var(--muted);font-size:.8rem}
.ersatz{font-size:.85rem;color:var(--muted);text-align:center;padding:10px}
footer{border-top:1px solid var(--line);background:var(--surface);margin-top:40px}footer .in{max-width:1080px;margin:0 auto;padding:24px 20px;font-size:.8rem;color:var(--muted);line-height:1.6}footer a{color:var(--ink2)}
@media(max-width:820px){.kopf{grid-template-columns:1fr}.mask{max-width:320px;width:100%;margin:0 auto}.types{grid-template-columns:repeat(2,1fr)}}"""

TYP_TXT = {
    "de": dict(titel="Meme-Typ: %s (%s)", meta="%s – einer von 8 Meme-Typen im Meme-Persönlichkeitstest. %s", kopf="Meme-Typ", plus="Stärke", acht="Vorsicht",
               mask="Typisches Meme", achse="Humor", cta="Test machen", ctaVs="Test machen und vergleichen", alle="Die anderen Meme-Typen", lang="English"),
    "en": dict(titel="Meme type: %s (%s)", meta="%s – one of 8 meme types in the meme personality test. %s", kopf="Meme type", plus="Strength", acht="Careful",
               mask="Typical meme", achse="Humor", cta="Take the test", ctaVs="Take the test and compare", alle="The other meme types", lang="Deutsch"),
}


def typseite(ty, lang):
    x, t = TYP_TXT[lang], ty[lang]
    m = MEME[ty["meme"]]
    test = "../../" if lang == "de" else "../../../en/"
    achsen = ", ".join(a[lang] for a in D["achsen"] if ty["p"].get(a["id"]))
    ref = "seite-" + ty["id"]
    titel = x["titel"] % (t["name"], m["name"])
    return """<!doctype html><html lang="%(lang)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titel)s</title><meta name="description" content="%(meta)s">
<link rel="canonical" href="%(url)s"><link rel="alternate" hreflang="de" href="%(url_de)s"><link rel="alternate" hreflang="en" href="%(url_en)s">
<meta property="og:type" content="website"><meta property="og:title" content="%(titel)s"><meta property="og:description" content="%(meta)s">
<meta property="og:url" content="%(url)s"><meta property="og:image" content="%(og)s"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#ffffff"><link rel="icon" href="%(fav)s">
<style>%(css)s</style>
<script data-goatcounter="https://schrauberbits.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script></head>
<body><header class="bar"><div class="in"><a class="logo" href="%(test)s"><i>M</i><span>Meme-Typ</span></a><a class="sw" href="%(other)s">%(lang_sw)s</a></div></header>
<main class="main"><div class="kopf"><div class="mask"><img src="%(img)s" alt="%(mname)s" referrerpolicy="no-referrer" onerror="this.outerHTML='&lt;div class=ersatz&gt;%(mname)s&lt;/div&gt;'"></div>
<div><div class="eyebrow">%(kopf)s</div><h1>%(name)s</h1><p>%(text)s</p>
<dl><dt>%(mask)s</dt><dd>%(mname)s – %(mdesc)s</dd><dt>%(achse)s</dt><dd>%(achsen)s</dd><dt>%(plus)s</dt><dd>%(tplus)s</dd><dt>%(acht)s</dt><dd>%(tacht)s</dd></dl>
<a class="btn" id="cta" href="%(test)s?ref=%(ref)s">%(cta)s</a></div></div>
<div class="section"><div class="eyebrow">Meme-Typ</div><h2>%(alle)s</h2><div class="types">%(andere)s</div></div></main>
<footer><div class="in">%(fuss)s</div></footer>
<script>(function(){try{var q=new URLSearchParams(location.search),r=(q.get('ref')||'%(ref)s').replace(/[^a-zA-Z0-9-]/g,'').slice(0,40)||'%(ref)s',h=new URLSearchParams(location.hash.slice(1)).get('vs'),ok=h&&/^[0-3]{16}$/.test(h),a=document.getElementById('cta');
a.href='%(test)s?ref='+encodeURIComponent(r)+(ok?'#vs='+h:'');if(ok)a.textContent=%(ctavs)s;}catch(e){}})();</script>
</body></html>""" % dict(lang=lang, titel=e(titel), meta=e(x["meta"] % (t["name"], t["text"])), url=typ_url(ty, lang), url_de=typ_url(ty, "de"), url_en=typ_url(ty, "en"),
                        og=BASIS + "og/%s-%s.png" % (ty["id"], lang), fav=FAVICON, css=TYP_CSS, test=test, other=typ_url(ty, "en" if lang == "de" else "de"), lang_sw=x["lang"],
                        kopf=e(x["kopf"]), name=e(t["name"]), text=e(t["text"]), img=e(m["img"]), mname=e(m["name"]), ref=ref, cta=e(x["cta"]),
                        mask=e(x["mask"]), mdesc=e(m[lang]), achse=e(x["achse"]), achsen=e(achsen), plus=e(x["plus"]), tplus=e(t["plus"]), acht=e(x["acht"]), tacht=e(t["achtung"]),
                        alle=e(x["alle"]), andere=typkarten(lang, ty), fuss=FUSS[lang], ctavs=json.dumps(x["ctaVs"], ensure_ascii=False))


OG_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:630px;font-family:Inter,"DejaVu Sans",sans-serif;background:#111318;color:#fff;position:relative;overflow:hidden}
.k{position:absolute;left:90px;top:120px;right:90px}.bar{width:80px;height:8px;background:#e4472b;margin-bottom:30px}
small{display:block;font-size:30px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#c8cbd1}
b{display:block;font-size:82px;line-height:1.05;letter-spacing:-.02em;margin:14px 0 22px}span{font-size:32px;color:#e9eaec}
.u{position:absolute;left:90px;bottom:56px;font-size:26px;font-weight:600;color:#9ea2a9}.m{position:absolute;right:90px;bottom:44px;width:52px;height:52px;border-radius:12px;background:#fff;color:#111318;font-weight:800;font-size:30px;display:flex;align-items:center;justify-content:center}</style></head>
<body><div class="k"><div class="bar"></div><small>%s</small><b>%s</b><span>%s</span></div><div class="u">schrauberbits.github.io/meme-typ</div><div class="m">M</div></body></html>"""


def bilder():
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(WURZEL, "og"), exist_ok=True)
    jobs = [("start-de", "Meme-Persönlichkeitstest", "Welcher Meme-Typ bist du?", "16 Memes ordnen · 8 Typen · 2 Minuten"),
            ("start-en", "Meme personality test", "Which meme type are you?", "Rank 16 memes · 8 types · 2 minutes")]
    for ty in D["typen"]:
        for lang in ("de", "en"):
            jobs.append(("%s-%s" % (ty["id"], lang), "Mein Meme-Typ" if lang == "de" else "My meme type", ty[lang]["name"],
                         "Welcher bist du?" if lang == "de" else "Which one are you?"))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for name, klein, gross, unter in jobs:
            pg.set_content(OG_HTML % (e(klein), e(gross), e(unter)))
            pg.wait_for_timeout(120)
            pg.screenshot(path=os.path.join(WURZEL, "og", name + ".png"))
        b.close()


def main():
    schreibe("index.html", startseite("de"))
    schreibe("en/index.html", startseite("en"))
    urls = [BASIS, BASIS + "en/"]
    for ty in D["typen"]:
        schreibe("typ/%s/index.html" % ty["slug_de"], typseite(ty, "de"))
        schreibe("en/type/%s/index.html" % ty["slug_en"], typseite(ty, "en"))
        urls += [typ_url(ty, "de"), typ_url(ty, "en")]
    schreibe("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
             "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (u, D["stand"]) for u in urls) + "</urlset>\n")
    schreibe("robots.txt", "User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % BASIS)
    schreibe("urls.txt", "\n".join(urls) + "\n")
    schreibe(INDEXNOW + ".txt", INDEXNOW)
    schreibe(".nojekyll", "")
    if "--ohne-bilder" not in sys.argv:
        bilder()
    print("OK", len(urls), "Seiten")


if __name__ == "__main__":
    main()
