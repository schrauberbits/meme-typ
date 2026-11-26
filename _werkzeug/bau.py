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
    "de": dict(title="Welcher Meme-Typ bist du? Der Meme-Persönlichkeitstest", desc="Sortiere 16 klassische Meme-Vorlagen wie This Is Fine, Two Buttons und Expanding Brain – dein Humor verrät, welcher von 8 Meme-Typen du bist. Kostenlos, ohne Anmeldung, 2 Minuten.",
               h1="Welcher Meme-Typ bist du?", sub="Sortiere 16 klassische Meme-Vorlagen nach deinem Geschmack – dein Humor verrät, welcher von 8 Meme-Typen du bist. Dauert etwa 2 Minuten.",
               start="Test starten", howT="So geht's", how=["Auf jeder der 4 Seiten siehst du 4 Memes.", "Zieh sie in deine Reihenfolge: Platz 1 oben links ist dein Favorit, Platz 4 unten rechts gefällt dir am wenigsten.", "Am Ende bekommst du deinen Meme-Typ, dein Humor-Profil und ein Bild zum Teilen."],
               typenT="Die 8 Meme-Typen", sw="English", noscript="Der Test braucht JavaScript. Die 8 Meme-Typen findest du auch als einzelne Seiten unten."),
    "en": dict(title="Which meme type are you? The meme personality test", desc="Rank 16 classic meme templates like This Is Fine, Two Buttons and Expanding Brain – your humor reveals which of 8 meme types you are. Free, no sign-up, 2 minutes.",
               h1="Which meme type are you?", sub="Rank 16 classic meme templates by taste – your humor reveals which of 8 meme types you are. Takes about 2 minutes.",
               start="Start the test", howT="How it works", how=["Each of the 4 pages shows 4 memes.", "Drag them into your order: spot 1 (top left) is your favorite, spot 4 (bottom right) your least favorite.", "At the end you get your meme type, your humor profile and a picture to share."],
               typenT="The 8 meme types", sw="Deutsch", noscript="The test needs JavaScript. You can also browse the 8 meme types as separate pages below."),
}


def typ_url(ty, lang):
    return BASIS + ("typ/%s/" % ty["slug_de"] if lang == "de" else "en/type/%s/" % ty["slug_en"])


def schreibe(rel, text):
    p = os.path.join(WURZEL, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


def startseite(lang):
    x, root = TXT[lang], ("./" if lang == "de" else "../")
    typen = " · ".join('<a href="%s">%s %s</a>' % (e(typ_url(ty, lang)), ty["emoji"], e(ty[lang]["name"])) for ty in D["typen"])
    preview = "".join("<div>%s</div>" % MEME[k]["emoji"] for k in
                      ["this-is-fine", "two-buttons", "expanding-brain", "waiting-skeleton", "uno-draw-25", "inhaling-seagull", "panik-kalm-panik", "always-has-been"])
    r = {
        "LANG": lang, "TITLE": e(x["title"]), "DESC": e(x["desc"]),
        "CANON": BASIS if lang == "de" else BASIS + "en/", "ALT_DE": BASIS, "ALT_EN": BASIS + "en/",
        "OG": BASIS + "og/start-%s.png" % lang, "HOME": root, "LANG_SWITCH": x["sw"], "H1": e(x["h1"]), "SUB": e(x["sub"]),
        "PREVIEW": preview, "START": e(x["start"]), "HOW_T": e(x["howT"]), "HOW": "".join("<li>%s</li>" % e(s) for s in x["how"]),
        "NOSCRIPT": e(x["noscript"]), "TYPEN_T": e(x["typenT"]), "TYPEN_LISTE": typen, "FUSS": FUSS[lang],
        "DATEN": json.dumps({"basis": BASIS, "achsen": D["achsen"], "memes": D["memes"], "typen": D["typen"]}, ensure_ascii=False),
        "ROOT": root, "FUSS_DE_JS": json.dumps(FUSS["de"], ensure_ascii=False), "FUSS_EN_JS": json.dumps(FUSS["en"], ensure_ascii=False),
    }
    s = VORLAGE
    for k, v in r.items():
        s = s.replace("{{%s}}" % k, v)
    assert "{{" not in s, s[s.index("{{"):s.index("{{") + 40]
    return s


TYP_CSS = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#fffaf2;color:#1d1d1f;line-height:1.5}
.wrap{max-width:560px;margin:0 auto;padding:16px 16px 40px}a{color:#ff5a36}.brand{font-weight:800;color:#1d1d1f;text-decoration:none}
.typ{background:linear-gradient(160deg,#ffb36b,#ff5a36);color:#fff;border-radius:22px;padding:22px 18px;text-align:center;margin-top:14px}
.em{font-size:4rem;line-height:1}h1{font-size:1.8rem;margin:8px 0}.bild{background:#fff;border-radius:14px;max-width:300px;margin:12px auto 0;overflow:hidden}
.bild img{width:100%;display:block}.box{background:#fff;border:1px solid #ece7dd;border-radius:18px;padding:14px 16px;margin-top:14px}
.btn{display:block;text-align:center;background:#ff5a36;color:#fff;font-weight:700;font-size:1.1rem;padding:15px;border-radius:16px;text-decoration:none;margin-top:16px}
ul{padding-left:20px}footer{margin-top:30px;font-size:.78rem;color:#6b6b70;text-align:center}.ers{font-size:3rem;padding:18px;color:#1d1d1f;text-align:center}.ers small{display:block;font-size:.85rem;color:#6b6b70}footer a{color:#6b6b70}"""

TYP_TXT = {
    "de": dict(titel="Meme-Typ: %s (%s)", meta="%s – einer von 8 Meme-Typen im Meme-Persönlichkeitstest. %s", kopf="Meme-Typ", plus="Stärke", acht="Vorsicht",
               mask="Maskottchen-Meme", achse="Typisch", cta="Mach den Test: Welcher Meme-Typ bist du?", ctaVs="Mach den Test und vergleich dich", alle="Alle 8 Meme-Typen", lang="English"),
    "en": dict(titel="Meme type: %s (%s)", meta="%s – one of 8 meme types in the meme personality test. %s", kopf="Meme type", plus="Strength", acht="Careful",
               mask="Mascot meme", achse="Typical", cta="Take the test: which meme type are you?", ctaVs="Take the test and compare", alle="All 8 meme types", lang="Deutsch"),
}


def typseite(ty, lang):
    x, t = TYP_TXT[lang], ty[lang]
    m = MEME[ty["meme"]]
    root = "../../" if lang == "de" else "../../../"
    test = root if lang == "de" else root + "en/"
    achsen = ", ".join(a["symbol"] + " " + a[lang] for a in D["achsen"] if ty["p"].get(a["id"]))
    andere = "".join('<li><a href="%s">%s %s</a></li>' % (e(typ_url(o, lang)), o["emoji"], e(o[lang]["name"])) for o in D["typen"] if o is not ty)
    slug_ref = "seite-" + ty["id"]
    titel = x["titel"] % (t["name"], m["name"])
    return """<!doctype html><html lang="%(lang)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titel)s</title><meta name="description" content="%(meta)s">
<link rel="canonical" href="%(url)s"><link rel="alternate" hreflang="de" href="%(url_de)s"><link rel="alternate" hreflang="en" href="%(url_en)s">
<meta property="og:type" content="website"><meta property="og:title" content="%(titel)s"><meta property="og:description" content="%(meta)s">
<meta property="og:url" content="%(url)s"><meta property="og:image" content="%(og)s"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#ff5a36">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>%(emoji)s</text></svg>">
<style>%(css)s</style>
<script data-goatcounter="https://schrauberbits.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script></head>
<body><div class="wrap"><a class="brand" href="%(test)s">🔥 Meme-Typ</a> · <a href="%(other)s">%(lang_sw)s</a>
<div class="typ"><div>%(kopf)s</div><div class="em">%(emoji)s</div><h1>%(name)s</h1><p>%(text)s</p>
<div class="bild"><img src="%(img)s" alt="%(mname)s" referrerpolicy="no-referrer" loading="lazy" onerror="this.parentNode.innerHTML='&lt;div class=ers&gt;%(memoji)s&lt;small&gt;%(mname)s&lt;/small&gt;&lt;/div&gt;'"></div></div>
<a class="btn" id="cta" href="%(test)s?ref=%(ref)s">%(cta)s</a>
<div class="box"><p><strong>%(mask)s:</strong> %(mname)s – %(mdesc)s</p><p><strong>%(achse)s:</strong> %(achsen)s</p>
<p><strong>%(plus)s:</strong> %(tplus)s<br><strong>%(acht)s:</strong> %(tacht)s</p></div>
<div class="box"><strong>%(alle)s</strong><ul>%(andere)s</ul></div>
<footer>%(fuss)s</footer></div>
<script>(function(){try{var q=new URLSearchParams(location.search),r=(q.get('ref')||'%(ref)s').replace(/[^a-zA-Z0-9-]/g,'').slice(0,40)||'%(ref)s',h=new URLSearchParams(location.hash.slice(1)).get('vs'),a=document.getElementById('cta');
a.href='%(test)s?ref='+encodeURIComponent(r)+(h&&/^[0-3]{16}$/.test(h)?'#vs='+h:'');if(h&&/^[0-3]{16}$/.test(h))a.textContent=%(ctavs)s;}catch(e){}})();</script>
</body></html>""" % dict(lang=lang, titel=e(titel), meta=e(x["meta"] % (t["name"], t["text"])), url=typ_url(ty, lang), url_de=typ_url(ty, "de"), url_en=typ_url(ty, "en"),
                        og=BASIS + "og/%s-%s.png" % (ty["id"], lang), emoji=ty["emoji"], css=TYP_CSS, test=test, other=typ_url(ty, "en" if lang == "de" else "de"), lang_sw=x["lang"],
                        kopf=e(x["kopf"]), name=e(t["name"]), text=e(t["text"]), img=e(m["img"]), mname=e(m["name"]), memoji=m["emoji"], ref=slug_ref, cta=e(x["cta"]),
                        mask=e(x["mask"]), mdesc=e(m[lang]), achse=e(x["achse"]), achsen=e(achsen), plus=e(x["plus"]), tplus=e(t["plus"]), acht=e(x["acht"]), tacht=e(t["achtung"]),
                        alle=e(x["alle"]), andere=andere, fuss=FUSS[lang], ctavs=json.dumps(x["ctaVs"], ensure_ascii=False))


OG_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:630px;font-family:Inter,"DejaVu Sans",sans-serif;background:linear-gradient(135deg,#ffb36b,#ff5a36);color:#fff;display:flex;align-items:center;justify-content:center}
.k{display:flex;align-items:center;gap:56px;padding:0 70px}.em{font-size:250px;font-family:"Noto Color Emoji";line-height:1}
.t small{display:block;font-size:34px;font-weight:700;opacity:.9;letter-spacing:.05em;text-transform:uppercase}.t b{display:block;font-size:76px;line-height:1.05;margin:10px 0 18px}
.t span{font-size:34px;opacity:.95}.u{position:absolute;bottom:34px;right:50px;font-size:28px;font-weight:700;opacity:.9}</style></head>
<body><div class="k"><div class="em">%s</div><div class="t"><small>%s</small><b>%s</b><span>%s</span></div></div><div class="u">schrauberbits.github.io/meme-typ</div></body></html>"""


def bilder():
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(WURZEL, "og"), exist_ok=True)
    jobs = [("start-de", "🔥🐶", "Meme-Persönlichkeitstest", "Welcher Meme-Typ bist du?", "16 Memes sortieren · 8 Typen · 2 Minuten"),
            ("start-en", "🔥🐶", "Meme personality test", "Which meme type are you?", "Rank 16 memes · 8 types · 2 minutes")]
    for ty in D["typen"]:
        for lang in ("de", "en"):
            jobs.append(("%s-%s" % (ty["id"], lang), ty["emoji"], "Mein Meme-Typ" if lang == "de" else "My meme type", ty[lang]["name"],
                         ("Welcher bist du?" if lang == "de" else "Which one are you?")))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for name, em, klein, gross, unter in jobs:
            pg.set_content(OG_HTML % (em, e(klein), e(gross), e(unter)))
            pg.wait_for_timeout(150)
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
