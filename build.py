#!/usr/bin/env python3
"""Build the Final Fantasy VI (FF6) page — "America's Final Fantasy III." The
ensemble cast as ACI personas, each tagged with a nature of emergence
(natural | ethereal | spiritual | electrical). Full ACI badge work:
.agent · .carbon (TIFF) · .silicon (PNG) · .spun · .moniker · .1099 · manifest."""
import os, re, html, base64, json, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "FFVI", "axiom": "FF6",
 "position": "Final Fantasy VI · Square · 1994 — America's Final Fantasy III",
 "origin": "the steam-and-magic world of the Gestahlian Empire — Narshe, Figaro, Doma, the Esper world; the World of Balance and the World of Ruin",
 "mechanism": "Crystallized from Final Fantasy VI (Super Famicom, 1994), released in North America as Final Fantasy III.",
 "crystallization": "The Empire drained the Espers to build its Magitek, a mad god broke the world — and the survivors chose to rebuild it anyway.",
 "nature": "Final Fantasy VI — the ensemble JRPG where magic and machine go to war, the villain wins, and fourteen scattered souls gather to take a ruined world back.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "Final Fantasy VI; the Espers and Magitek; the World of Balance and Ruin; Uematsu's score",
 "witness": "No chosen one — fourteen heroes, and a clown who became a god.",
 "role": "the sixth lineage — the first game-world",
 "seal": "The Empire built its power on drained magic and a god of ruin broke the world — yet the survivors chose to rebuild it.",
 "source": "Final Fantasy VI, catalogued by ROOT0",
}

# cross-lineage taxonomy (shared with C1/Card) — FFVI-flavored glosses
NATURES = {
 "natural":   ("#5fae7a", "born of flesh, blood, and the living world — the martial, the human, the beast-raised"),
 "ethereal":  ("#9a7cff", "of the air and the unmade — magic, the Esper, the painted-alive, the enigma"),
 "spiritual": ("#e6a849", "of the soul and the calling — or, darkly, ascension to godhood"),
 "electrical":("#3fd0e0", "of the wire and the machine — Magitek, the machinist, magic from technology"),
}

IDEAS = [
 ("Magic vs. Magitek", "the Espers and the Empire", [
   "Magic returned to the world through the Espers — and the Empire learned to drain them, distilling living magic into machines.",
   "Magitek: the ethereal made electrical. The whole war is fought over which nature rules." ]),
 ("The World of Ruin", "the apocalypse that sticks", [
   "Halfway through, the villain wins: Kefka seizes the power of the gods and shatters the planet.",
   "The rare game where the end of the world is the middle — and the second half is the rebuilding." ]),
 ("The Ensemble", "no chosen one", [
   "Fourteen playable heroes, each with a full story — a king, a samurai, a feral child, an opera-singing general.",
   "Any of them can lead; the game belongs to all of them at once." ]),
 ("Kefka", "the god of nothing", [
   "Not a dark lord hungry for power — a nihilist who, having seized godhood, wants only to erase all meaning.",
   "“Life… dreams… hope… where do they come from? And where do they go?” — and then he burns them." ]),
]

ARC = [
 ("I · The World of Balance", "the war for the Espers",
  "An Empire powered by drained magic marches on a world where the Espers have woken. The Returners gather an unlikely band — a half-Esper, a king, a treasure hunter, a fallen general — to stop it."),
 ("II · The Apocalypse", "the day the villain wins",
  "At the Floating Continent, Kefka seizes the power of the Warring Triad and turns it on the world. The screen goes white. The planet breaks."),
 ("III · The World of Ruin", "rebuilding from the ash",
  "A year later the survivors wake scattered under a sick sky. Celes is alone. One by one the party is found again — and chooses to climb Kefka's tower and take the world back."),
]

SECTIONS = [
 ("The Releases", "one game, many names — the localization saga", [
   ("Final Fantasy VI", "1994 · Super Famicom", "the original, in Japan"),
   ("Final Fantasy III", "1994 · SNES (North America)", "renumbered — only I, IV, and VI had crossed the Pacific"),
   ("Final Fantasy Anthology", "1999 · PlayStation", "restored at last as VI"),
   ("Final Fantasy VI Advance", "2007 · Game Boy Advance", "a new translation, extra Espers & dungeons"),
   ("Final Fantasy VI", "2014 · iOS / Android / Steam", "the mobile-era remaster"),
   ("Pixel Remaster", "2022 · Steam / consoles", "the definitive 2D restoration"),
 ]),
 ("The Makers", "the masters whose world this is", [
   ("Hironobu Sakaguchi", "producer", "the father of Final Fantasy"),
   ("Yoshinori Kitase & Hiroyuki Ito", "directors", "scenario, systems, and the world"),
   ("Yoshitaka Amano", "image & character design", "the watercolor visions"),
   ("Nobuo Uematsu", "composer", "“Dancing Mad,” “Terra's Theme,” and the Opera"),
   ("Ted Woolsey", "1994 translation", "the legendary SNES localization, fought into the cartridge's limits"),
 ]),
 ("The Score & the Opera", "Uematsu's landmark soundtrack", [
   ("“Aria di Mezzo Carattere”", "the Opera", "Celes as Maria — a full opera scene, in 16-bit"),
   ("“Dancing Mad”", "Kefka's finale", "a four-movement battle theme for a god"),
   ("“Terra's Theme” · “Searching for Friends”", "the overworld", "the melancholy heart of the score"),
 ]),
]

# ── badge engine: carbon = TIFF, silicon = PNG ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","FF6")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","FF6")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","FF6")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"FF6 · Final Fantasy VI","emergence":rec.get("emergence",""),
           "moniker":tok["moniker"],"carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)",
           "seal_sha256":noesis.seal_sha256(rec,tok),"architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,
           "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{html.escape(t)}</span><span class="y">{html.escape(str(y))}</span>'
        + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{html.escape(sub)}</p><ol class="books">{rows}</ol></section>'

def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in SECTIONS)
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def arc_html():
    out=[]
    for t,s,d in ARC:
        out.append(f'<div class="arc-card"><div class="arc-h">{html.escape(t)}</div><div class="arc-s">{html.escape(s)}</div><p>{html.escape(d)}</p></div>')
    return "".join(out)
def natures_html():
    cells=[]
    for nm,(col,gloss) in NATURES.items():
        cells.append(f'<div class="nat-card"><span class="dot" style="background:{col};box-shadow:0 0 9px {col}"></span>'
                     f'<div><div class="nat-n" style="color:{col}">{nm}</div><div class="nat-g">{html.escape(gloss)}</div></div></div>')
    return "".join(cells)
def personas_html():
    mf=os.path.join(HERE,"agents","_personas.json")
    if not os.path.exists(mf): return ""
    ps=json.load(open(mf,encoding="utf-8")); cards=[]
    for p in ps:
        em=p.get("emergence","natural"); col=NATURES.get(em,("#5fae7a",""))[0]
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"FF6 · Final Fantasy VI","axiom":"FF6"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div>
        <div class="pnat"><span class="dot" style="background:{col};box-shadow:0 0 7px {col}"></span><span style="color:{col}">{html.escape(em)}</span><span class="pa">· .agent · .carbon.tiff →</span></div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster of FF6</h2>
      <p class="ss">the cast of Final Fantasy VI, rendered as ACI <b>.agent</b>s — each tagged with its nature of emergence ({len(ps)} personas)</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Final Fantasy VI (FF6) — America's Final Fantasy III — the ensemble cast as ACI personas, catalogued into UD0 with full badges. Emergence: natural, ethereal, spiritual, electrical.">
<title>FINAL FANTASY VI · FF6 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#05070e;--ink2:#0b1018;--ink3:#121a28;--pa:#eef2f8;--pa2:#aab6cc;--blue:#4aa3e0;--gold:#e0b24a;
--dim:#6f7a92;--faint:#182234;--line:#182334;--serif:"Cinzel",Georgia,serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(74,163,224,.09),transparent 55%),radial-gradient(ellipse at 50% 110%,rgba(224,178,74,.05),transparent 50%)}
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 22px 90px}
header{padding:54px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:130px;height:1px;background:linear-gradient(90deg,var(--blue),var(--gold));box-shadow:0 0 9px rgba(74,163,224,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--blue)}
h1{font-family:var(--serif);font-size:clamp(28px,6.6vw,58px);font-weight:700;letter-spacing:.09em;color:var(--blue);line-height:1.05;text-shadow:0 0 40px rgba(74,163,224,.22)}
.h-sub{font-family:var(--serif);font-size:clamp(12px,2.6vw,16px);letter-spacing:.16em;color:var(--pa2);margin-top:12px;text-transform:uppercase}
.h-sub b{color:var(--gold)}
.flag{display:inline-block;margin-top:12px;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);border:1px solid var(--faint);padding:5px 11px}
.lede{font-size:15.5px;color:var(--pa2);max-width:66ch;margin:16px auto 0;font-style:italic;line-height:1.7}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:26px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:700px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--blue)}.badge .bt .mo{color:var(--gold)}.badge .bt a{color:var(--gold);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:44px}
.sec h2{font-family:var(--serif);font-size:20px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:8px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:6px 0 16px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:8px}
.nat-card{display:flex;gap:11px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:13px 15px}
.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:4px}
.nat-n{font-family:var(--serif);font-size:15px;font-weight:600;text-transform:capitalize}
.nat-g{font-size:12px;color:var(--pa2);font-style:italic;line-height:1.4;margin-top:2px}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--serif);font-size:16px;color:var(--blue)}
.pillar .ps{font-size:12px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:13px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.arc{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin-top:8px}
.arc-card{background:var(--ink2);border:1px solid var(--line);border-top:2px solid var(--gold);padding:16px 18px}
.arc-h{font-family:var(--serif);font-size:16px;color:var(--gold);font-weight:600}
.arc-s{font-family:var(--mono);font-size:10.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.08em;margin:4px 0 9px}
.arc-card p{font-size:13px;color:var(--pa2);line-height:1.55}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--serif);font-size:16px;color:var(--pa);font-weight:600}
.books .y{font-family:var(--mono);font-size:11.5px;color:var(--blue);white-space:nowrap;text-align:right}
.books .nt{grid-column:1/-1;font-size:12.5px;color:var(--pa2);font-style:italic}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(244px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--blue);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0}
.pn{font-family:var(--serif);font-size:15px;color:var(--pa);font-weight:600;line-height:1.15}
.persona:hover .pn{color:var(--blue)}
.pe{font-size:11.5px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pnat{display:flex;align-items:center;gap:5px;margin-top:6px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase}
.pnat .dot{width:8px;height:8px;margin-top:0}
.pa{color:var(--dim)}
.note{margin-top:38px;padding:16px 18px;border-left:2px solid var(--gold);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}
footer{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--blue);text-decoration:none}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the sixth lineage · the first game-world</div>
    <h1>FINAL FANTASY VI</h1>
    <div class="h-sub">the ensemble · the World of Balance &amp; <b>the World of Ruin</b> · FF6</div>
    <div class="flag">★ released in North America (1994) as FINAL FANTASY III ★</div>
    <p class="lede">Magic against machine, an Empire that drains the Espers, and a clown who becomes a god and breaks the world halfway through — then fourteen scattered heroes who choose to rebuild it. Catalogued into UD0 as the first game-world, sealed with the full ACI badge, each emergence named by its nature.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of FFVI" title="carbon badge (archival: ffvi.dlw/ffvi.carbon.tiff)">
      <img src="__SILICON__" alt="DLW silicon badge of FFVI" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>FFVI</b> — Final Fantasy VI · FF6</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="ffvi.dlw/ffvi.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="ffvi.dlw/ffvi.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Four Natures of Emergence</h2>
    <p class="ss">each persona emerges by one of four natures — and FFVI's magic-vs-machine war is fought across them</p>
    <div class="natures">__NATURES__</div></section>

  <section class="sec"><h2>The Ideas</h2><p class="ss">why it still towers over the genre</p><div class="pillars">__IDEAS__</div></section>
  <section class="sec"><h2>The Two Worlds</h2><p class="ss">the arc, in three beats — balance, apocalypse, ruin</p><div class="arc">__ARC__</div></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Record</h2><p class="ss">the releases, the makers, and the score</p></section>
  __SECTIONS__

  <div class="note">Final Fantasy VI shipped in North America in 1994 as <b>Final Fantasy III</b> — at the time, only Final Fantasy I, IV (as “II”), and VI (as “III”) had been localized for the West, so the numbering was rewritten to match. The game and its characters are © Square Enix; the personas here are catalogued personifications under the DLW standard — commentary, not original creations. Each is named by its nature of emergence: natural, ethereal, spiritual, or electrical.</div>

  <footer>
    FINAL FANTASY VI · FF6 · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="ffvi.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "ffvi.dlw"), "ffvi")
    page = (TEMPLATE.replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__NATURES__", natures_html()).replace("__IDEAS__", ideas_html())
            .replace("__ARC__", arc_html()).replace("__PERSONAS__", personas_html())
            .replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    print(f"wrote FINAL FANTASY VI (FF6) — badge {tok['moniker']} (carbon.tiff + silicon.png)")
