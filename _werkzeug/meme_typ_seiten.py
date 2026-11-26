#!/usr/bin/env python3
"""Schreibt in meme-typ: bilder/LIESMICH.md, bilder-status/index.html, turnier/index.html.
Aufruf: python3 meme_typ_seiten.py [<pfad zu meme-typ>]"""
import json, os, sys, html

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else "/home/claude/meme-typ"
MD = json.load(open(os.path.join(HIER, "memes.json"), encoding="utf-8"))
e = html.escape
UPLOAD = "https://github.com/schrauberbits/meme-typ/upload/main/bilder"
SYSTEME = [("bigfive", "Big Five", "https://schrauberbits.github.io/meme-bigfive/"), ("mbti", "16 Typen", "https://schrauberbits.github.io/meme-mbti/"),
           ("enneagramm", "Enneagramm", "https://schrauberbits.github.io/meme-enneagramm/")]
MEMES = [{k: m[k] for k in ("id", "name", "datei", "direkt", "img", "quelle", "kopie")} for m in MD["memes"]]

CSS = """:root{--bg:#f6f6f4;--surface:#fff;--ink:#111318;--ink2:#3b3f47;--muted:#6b7079;--line:#e4e4e0;--accent:#e4472b;--ok:#1f7a4d;--warn:#b54708}
*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit}.main{max-width:980px;margin:0 auto;padding:28px 16px 60px}.eyebrow{font-size:.78rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
h1{font-size:clamp(1.6rem,4vw,2.2rem);letter-spacing:-.02em;margin:6px 0 10px}p{color:var(--ink2)}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px;margin:14px 0}
.btn{display:inline-flex;align-items:center;background:var(--accent);color:#fff;font-weight:600;padding:11px 18px;border-radius:10px;text-decoration:none;border:0;font:inherit;cursor:pointer}
.btn.ghost{background:var(--surface);color:var(--ink);border:1px solid var(--line)}
table{width:100%;border-collapse:collapse;font-size:.9rem}th,td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--line);vertical-align:middle}th{font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600}
.th{width:64px;height:48px;border-radius:6px;background:#f1f1ee;overflow:hidden;display:flex;align-items:center;justify-content:center;font-size:.65rem;color:var(--muted)}.th img{width:100%;height:100%;object-fit:cover}
.ok{color:var(--ok);font-weight:600}.fehlt{color:var(--accent);font-weight:600}.frei{color:var(--warn);font-weight:600}
code{font-size:.82rem;background:#f1f1ee;padding:2px 6px;border-radius:5px;word-break:break-all}
.kopieren{font-size:.8rem;padding:5px 9px;border-radius:7px;border:1px solid var(--line);background:var(--surface);cursor:pointer}
.zahlen{display:flex;gap:18px;flex-wrap:wrap}.zahlen div{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px}.zahlen b{display:block;font-size:1.5rem}
.balken{height:8px;background:#ececE8;border-radius:4px;overflow:hidden;min-width:80px}.balken i{display:block;height:8px;background:var(--accent)}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.tabs button{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:6px 12px;font:inherit;font-size:.85rem;cursor:pointer}.tabs button.an{background:var(--ink);color:#fff;border-color:var(--ink)}
.muted{color:var(--muted)}.klein{font-size:.82rem}
@media(max-width:640px){.weg{display:none}td,th{padding:8px 5px}}"""


def seite(titel, rumpf, skript):
    return """<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title><meta name="robots" content="noindex"><style>%s</style></head><body><main class="main">%s</main><script>%s</script></body></html>""" % (e(titel), CSS, rumpf, skript)


STATUS = """<div class="eyebrow">Meme-Tests · Bilder</div><h1>Bilder-Status</h1>
<p>Alle drei Varianten (Big Five, 16 Typen, Enneagramm) laden ihre Bilder aus diesem einen Ordner. Lade jedes fehlende Bild einmal hoch, mit genau dem angezeigten Dateinamen. Der Name stimmt automatisch, wenn du das Bild über den Direktlink speicherst.</p>
<div class="panel"><b>So geht's</b><ol class="klein"><li>Bei jedem fehlenden Bild auf „Speichern“ tippen (oder oben „Alle fehlenden speichern“). Die Datei hat dann schon den richtigen Namen.</li>
<li>„Bilder hochladen“ antippen, auf „choose your files“ tippen, die gespeicherten Dateien auswählen und unten auf „Commit changes“ tippen.</li>
<li>Nach etwa einer Minute diese Seite neu laden. Hochgeladene Bilder stehen dann auf „vorhanden“.</li></ol>
<a class="btn" href="%(upload)s">Bilder hochladen</a> <button class="btn ghost" id="alleSpeichern" type="button">Alle fehlenden speichern</button> <span id="msg" class="klein muted"></span></div>
<div class="zahlen"><div><b id="nVor">–</b>vorhanden</div><div><b id="nFehlt">–</b>fehlen</div><div><b id="nFrei">–</b>laufen ohne Upload</div></div>
<div class="panel"><table><thead><tr><th>Bild</th><th>Meme</th><th>Status</th><th class="weg">Dateiname</th><th>Bild</th></tr></thead><tbody id="liste"></tbody></table></div>
<p class="klein muted"><a href="../turnier/">Turnier-Stand</a> · %(links)s</p>"""

STATUS_JS = """const M=%s;const B='./../bilder/';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let nV=0,nF=0,nFr=0;const fehlend=[];
function zahl(){document.getElementById('nVor').textContent=nV;document.getElementById('nFehlt').textContent=nF;document.getElementById('nFrei').textContent=nFr;}
document.getElementById('liste').innerHTML=M.map((m,k)=>'<tr id="z'+k+'"><td><div class="th">…</div></td><td><b>'+esc(m.name)+'</b><div class="klein"><a href="'+esc(m.quelle)+'">Vorlage auf imgflip</a></div></td><td class="st">prüfe …</td><td class="weg"><code>'+esc(m.datei)+'</code></td><td><button class="kopieren speichern" type="button" data-k="'+k+'">Speichern</button> <a class="klein" href="../kopieren/#'+esc(m.id)+'">kopieren</a></td></tr>').join('');
M.forEach((m,k)=>{const img=new Image();img.referrerPolicy='no-referrer';
  img.onload=()=>{const z=document.getElementById('z'+k);z.querySelector('.th').innerHTML='';z.querySelector('.th').appendChild(img);z.querySelector('.st').innerHTML='<span class=ok>vorhanden</span>';nV++;zahl();};
  img.onerror=()=>{const z=document.getElementById('z'+k);if(m.img){z.querySelector('.st').innerHTML='<span class=frei>läuft über imgflip</span><div class=klein>Upload optional</div>';z.querySelector('.th').innerHTML='<img src="'+esc(m.img)+'" referrerpolicy="no-referrer">';nFr++;}else{z.querySelector('.st').innerHTML='<span class=fehlt>fehlt</span>';z.querySelector('.th').textContent='fehlt';nF++;fehlend.push(m.id);fehlendIdx.push(k);}zahl();};
  img.src=B+encodeURIComponent(m.datei)+'?v='+Date.now();});
async function kopiere(t){try{await navigator.clipboard.writeText(t);return true;}catch(e){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();const ok=document.execCommand('copy');a.remove();return ok;}}
const fehlendIdx=[];
async function speichere(k){const m=M[k];const r=await fetch(m.kopie,{mode:'cors',referrerPolicy:'no-referrer'});if(!r.ok)throw new Error('HTTP '+r.status);const b=await r.blob();const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=m.datei;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},4000);}
document.addEventListener('click',async ev=>{const b=ev.target.closest('.speichern');if(!b)return;const alt=b.textContent;b.textContent='…';try{await speichere(+b.dataset.k);b.textContent='Gespeichert';}catch(e){b.textContent='Fehler';}setTimeout(()=>b.textContent=alt,2500);});
document.getElementById('alleSpeichern').onclick=async()=>{const msg=document.getElementById('msg');if(!fehlendIdx.length){msg.textContent='Es fehlt kein Bild.';return;}let n=0;for(const k of fehlendIdx){msg.textContent='Speichere '+(n+1)+' von '+fehlendIdx.length+' …';try{await speichere(k);n++;}catch(e){}await new Promise(r=>setTimeout(r,700));}msg.textContent=n+' Bilder gespeichert. Fragt der Browser, ob mehrere Downloads erlaubt sind, bitte zulassen.';};"""

TURNIER = """<div class="eyebrow">Meme-Tests · Turnier</div><h1>Welche Memes tragen den Test?</h1>
<p>Jeder Test zieht 20 von %(n)d Memes. Gezählt wird je Meme, in wie vielen begonnenen Tests es vorkam und wie viele davon fertig wurden. Memes mit hoher Fertig-Quote halten die Leute im Test, Memes mit niedriger Quote sind Kandidaten zum Austauschen. Unter 20 begonnenen Tests ist die Quote noch Zufall.</p>
<div class="tabs" id="tabs"></div>
<div class="zahlen"><div><b id="sG">–</b>begonnene Tests</div><div><b id="sF">–</b>fertige Tests</div><div><b id="sQ">–</b>Fertig-Quote gesamt</div></div>
<div class="panel"><table><thead><tr><th>#</th><th>Bild</th><th>Meme</th><th>Fertig-Quote</th><th class="weg">Abweichung</th><th>Begonnen</th></tr></thead><tbody id="liste"><tr><td colspan="6" class="muted">Lade Zählung …</td></tr></tbody></table></div>
<p class="klein muted" id="hinweis"></p>
<p class="klein muted"><a href="../bilder-status/">Bilder-Status</a> · %(links)s</p>"""

TURNIER_JS = """const M=%s;const SYS=%s;const GC='https://schrauberbits.goatcounter.com/counter/';const B='./../bilder/';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const daten={};let fehlerZahl=0,auswahl='alle';
async function holen(pfad){try{const r=await fetch(GC+encodeURIComponent(pfad)+'.json',{cache:'no-store'});if(r.status===404)return 0;if(!r.ok){fehlerZahl++;return 0;}const j=await r.json();return parseInt(String(j.count).replace(/[^0-9]/g,''))||0;}catch(e){fehlerZahl++;return 0;}}
async function laden(){
  const jobs=[];SYS.forEach(s=>M.forEach(m=>['gezeigt','fertig'].forEach(a=>jobs.push([s[0],m.id,a]))));
  let i=0;async function arbeiter(){while(i<jobs.length){const [s,id,a]=jobs[i++];((daten[s]=daten[s]||{})[id]=daten[s][id]||{})[a]=await holen('turnier-'+s+'-'+a+'-'+id);}}
  await Promise.all([1,2,3,4,5,6].map(arbeiter));zeichnen();
}
function werte(id){let g=0,f=0;SYS.forEach(s=>{if(auswahl!=='alle'&&auswahl!==s[0])return;const d=(daten[s[0]]||{})[id]||{};g+=d.gezeigt||0;f+=d.fertig||0;});return {g,f};}
function zeichnen(){
  document.getElementById('tabs').innerHTML=[['alle','Alle Varianten']].concat(SYS.map(s=>[s[0],s[1]])).map(([k,n])=>'<button type="button" data-k="'+k+'" class="'+(k===auswahl?'an':'')+'">'+esc(n)+'</button>').join('');
  const zeilen=M.map(m=>({m,...werte(m.id)}));
  // begonnene Tests: jeder Test zeigt 20 Memes
  const G=zeilen.reduce((s,z)=>s+z.g,0)/20,F=zeilen.reduce((s,z)=>s+z.f,0)/20,Q=G?F/G:0;
  document.getElementById('sG').textContent=Math.round(G);document.getElementById('sF').textContent=Math.round(F);document.getElementById('sQ').textContent=G?Math.round(Q*100)+' %%':'–';
  zeilen.forEach(z=>{z.q=z.g?z.f/z.g:null;z.d=z.q===null?null:z.q-Q;});
  zeilen.sort((a,b)=>((b.g>=20)-(a.g>=20))||((b.q??-1)-(a.q??-1))||(b.g-a.g));
  document.getElementById('liste').innerHTML=zeilen.map((z,k)=>{const q=z.q===null?'–':Math.round(z.q*100)+' %%';const d=z.d===null?'':(z.d>=0?'+':'')+Math.round(z.d*100)+' Pkt.';const wenig=z.g<20;
    return '<tr'+(wenig?' style="opacity:.6"':'')+'><td>'+(k+1)+'</td><td><div class="th"><img src="'+B+encodeURIComponent(z.m.datei)+'" referrerpolicy="no-referrer" onerror="'+(z.m.img?'this.onerror=null;this.src=\\''+esc(z.m.img)+'\\'':'this.remove()')+'"></div></td><td><b>'+esc(z.m.name)+'</b>'+(wenig?'<div class=klein>noch zu wenig Daten</div>':'')+'</td><td>'+q+'<div class="balken"><i style="width:'+(z.q===null?0:Math.round(z.q*100))+'%%"></i></div></td><td class="weg">'+d+'</td><td>'+z.g+'</td></tr>';}).join('');
  document.getElementById('hinweis').textContent=fehlerZahl?('Hinweis: '+fehlerZahl+' Zählwerte ließen sich nicht abrufen. Ist in GoatCounter unter Settings die Option „Allow adding visitor counts on your website“ aktiv?'):'Stand: '+new Date().toLocaleString('de-DE');
}
document.addEventListener('click',ev=>{const b=ev.target.closest('#tabs button');if(b){auswahl=b.dataset.k;zeichnen();}});
laden();"""


KOPIE = """<div class="eyebrow">Meme-Tests · Bild kopieren</div><h1 id="titel">Bild kopieren</h1>
<div class="panel" id="karte" style="text-align:center"><div id="bild" style="min-height:200px;display:flex;align-items:center;justify-content:center;background:#f1f1ee;border-radius:10px;overflow:hidden"></div>
<p id="status" class="klein muted" style="min-height:1.4em;margin:12px 0"></p>
<button class="btn" id="kopieren" type="button" style="font-size:1.1rem;padding:16px 26px">Bild kopieren</button>
<button class="btn ghost" id="speichern" type="button" style="font-size:1.1rem;padding:16px 26px">Bild speichern</button></div>
<div class="panel"><b>Alle Bilder</b><div id="alle" class="klein" style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px"></div></div>
<p class="klein muted"><a href="../bilder-status/">Bilder-Status</a> · <a href="https://github.com/schrauberbits/meme-typ/upload/main/bilder">Bilder hochladen</a></p>"""

KOPIE_JS = """const M=%s;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const $=id=>document.getElementById(id);
let m=null,pngPromise=null,blobRoh=null;
function waehle(){const id=decodeURIComponent(location.hash.slice(1));m=M.find(x=>x.id===id)||M[0];
  document.title=m.name+' kopieren';$('titel').textContent=m.name;$('status').textContent='Lade Bild …';
  $('bild').innerHTML='<img src="'+esc(m.kopie)+'" crossorigin="anonymous" referrerpolicy="no-referrer" style="max-width:100%%;max-height:60vh;display:block">';
  blobRoh=null;pngPromise=fetch(m.kopie,{mode:'cors',referrerPolicy:'no-referrer'}).then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.blob();}).then(b=>{blobRoh=b;return createImageBitmap(b);}).then(bm=>{const c=document.createElement('canvas');c.width=bm.width;c.height=bm.height;c.getContext('2d').drawImage(bm,0,0);return new Promise((ok,nein)=>c.toBlob(x=>x?ok(x):nein(new Error('PNG')),'image/png'));});
  pngPromise.then(()=>{$('status').textContent='Bereit.';versucheAuto();}).catch(e=>{$('status').textContent='Bild ließ sich nicht laden: '+e.message;});
  $('alle').innerHTML=M.map(x=>'<a href="#'+esc(x.id)+'" style="padding:5px 9px;border:1px solid var(--line);border-radius:999px;text-decoration:none;'+(x===m?'background:var(--ink);color:#fff':'')+'">'+esc(x.name)+'</a>').join('');}
async function kopieren(auto){
  try{
    if(!navigator.clipboard||!window.ClipboardItem)throw new Error('Dein Browser kann keine Bilder kopieren – nimm „Bild speichern“.');
    // ClipboardItem sofort im Tipp anlegen (Safari), das PNG kommt als Promise nach
    await navigator.clipboard.write([new ClipboardItem({'image/png':pngPromise})]);
    $('status').innerHTML='<span class=ok>Kopiert</span> – jetzt einfügen, wo du es brauchst.';return true;
  }catch(e){if(!auto)$('status').textContent='Dein Browser hat das Kopieren blockiert. Halte das Bild gedrückt und wähle „Kopieren“ – oder nimm „Bild speichern“.';return false;}
}
async function versucheAuto(){if(document.hasFocus&&document.hasFocus()){const ok=await kopieren(true);if(!ok)$('status').textContent='Tippe auf „Bild kopieren“.';}else $('status').textContent='Tippe auf „Bild kopieren“.';}
$('kopieren').onclick=()=>kopieren(false);
$('speichern').onclick=async()=>{try{await pngPromise;}catch(e){}const b=blobRoh;if(!b){$('status').textContent='Bild noch nicht geladen.';return;}const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=m.datei;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},2000);$('status').innerHTML='Gespeichert als <code>'+esc(m.datei)+'</code>.';};
addEventListener('hashchange',waehle);waehle();"""


def main():
    links = " · ".join('<a href="%s">%s</a>' % (u, n) for _, n, u in SYSTEME)
    os.makedirs(os.path.join(ZIEL, "bilder"), exist_ok=True)
    os.makedirs(os.path.join(ZIEL, "bilder-status"), exist_ok=True)
    os.makedirs(os.path.join(ZIEL, "turnier"), exist_ok=True)
    zeilen = "\n".join("| %s | `%s` | %s |" % (m["name"], m["datei"], m["direkt"]) for m in MEMES)
    open(os.path.join(ZIEL, "bilder", "LIESMICH.md"), "w", encoding="utf-8").write(
        "# Bilder für die Meme-Tests\n\nHier liegen die Meme-Bilder für meme-bigfive, meme-mbti und meme-enneagramm. "
        "Dateinamen genau so lassen, wie sie über den Direktlink heruntergeladen werden.\n\nStatus: https://schrauberbits.github.io/meme-typ/bilder-status/\n\n"
        "| Meme | Dateiname | Direktlink |\n|---|---|---|\n" + zeilen + "\n")
    open(os.path.join(ZIEL, "bilder-status", "index.html"), "w", encoding="utf-8").write(
        seite("Bilder-Status · Meme-Tests", STATUS % dict(upload=UPLOAD, links=links), STATUS_JS % json.dumps(MEMES, ensure_ascii=False)))
    open(os.path.join(ZIEL, "turnier", "index.html"), "w", encoding="utf-8").write(
        seite("Turnier · Meme-Tests", TURNIER % dict(n=len(MEMES), links=links),
              TURNIER_JS % (json.dumps(MEMES, ensure_ascii=False), json.dumps([[s, n] for s, n, _ in SYSTEME], ensure_ascii=False))))
    os.makedirs(os.path.join(ZIEL, "kopieren"), exist_ok=True)
    km = [{k: m[k] for k in ("id", "name", "datei", "kopie")} for m in MD["memes"]]
    open(os.path.join(ZIEL, "kopieren", "index.html"), "w", encoding="utf-8").write(
        seite("Bild kopieren · Meme-Tests", KOPIE, KOPIE_JS % json.dumps(km, ensure_ascii=False)))
    print("OK", ZIEL)


if __name__ == "__main__":
    main()
