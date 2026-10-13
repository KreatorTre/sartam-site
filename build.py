#!/usr/bin/env python3
"""Render ../lore/*.md into static HTML. Run: python3 build.py"""
import re, html, json, pathlib
L = pathlib.Path(__file__).parent.parent/'lore'; O = pathlib.Path(__file__).parent

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)\*(?!\w)', r'<em>\1</em>', t)
    t = re.sub(r'\[?(Provisional[^\]|<]*?)\]?(?=[\s|;,.)<]|$)', r'<span class="badge prov" title="Provisional, may change">\1 · may change</span>', t)
    t = re.sub(r'\[Locked[^\]]*\]', lambda m: f'<span class="badge lock">{m.group(0)[1:-1]}</span>', t)
    return t

def spoil(inner, tag='div'):
    return f'<{tag} class="spoiler" tabindex="0" role="button" aria-label="Spoiler, click to reveal"><span class="sp-label">⚠ Spoiler: click to reveal</span><span class="sp-body">{inner}</span></{tag}>'

def render(md):
    out=[]; lines=md.split('\n'); i=0
    while i<len(lines):
        l=lines[i]
        if l.startswith('#'):
            n=len(l)-len(l.lstrip('#')); txt=l[n:].strip()
            sid=re.sub(r'[^a-z0-9]+','-',txt.lower()).strip('-')
            out.append(f'<h{n} id="{sid}">{inline(txt)}</h{n}>')
        elif l.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'): rows.append(lines[i]); i+=1
            i-=1
            cells=lambda r:[c.strip() for c in r.strip().strip('|').split('|')]
            h=cells(rows[0]); t='<div class="tw"><table><thead><tr>'+''.join(f'<th>{inline(c)}</th>' for c in h)+'</tr></thead><tbody>'
            for r in rows[2:]:
                cs=cells(r); tds=[]
                for c in cs:
                    v=inline(c)
                    if '⚠' in c and len(cs)>1: v=spoil(v,'span')
                    tds.append(f'<td>{v}</td>')
                t+='<tr>'+''.join(tds)+'</tr>'
            out.append(t+'</tbody></table></div>')
        elif re.match(r'\s*(-|\d+\.)\s',l):
            ordered=bool(re.match(r'\s*\d',l)); items=[]
            while i<len(lines) and re.match(r'\s*(-|\d+\.)\s',lines[i]):
                x=re.sub(r'^\s*(-|\d+\.)\s','',lines[i]); items.append(spoil(inline(x),'span') if '⚠' in x else inline(x)); i+=1
            i-=1; tg='ol' if ordered else 'ul'
            out.append(f'<{tg}>'+''.join(f'<li>{x}</li>' for x in items)+f'</{tg}>')
        elif l.strip()=='---': out.append('<hr>')
        elif l.strip():
            out.append(spoil(inline(l)) if '⚠' in l and 'SPOILER' in l and not l.startswith('Tags') else f'<p>{inline(l)}</p>')
        i+=1
    return '\n'.join(out)

def page(title, active, body, extra=''):
    nav=''.join(f'<a href="{h}" class="{"on" if n==active else ""}">{n}</a>' for n,h in [('Home','index.html'),('Wiki','wiki.html'),('Trivia','trivia.html')])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · SARTAM</title><meta name="description" content="SARTAM: a dark, gritty sci-fi saga by Kreator Tre"><link rel="stylesheet" href="style.css"></head>
<body><canvas id="veins" aria-hidden="true"></canvas><header><a class="logo" href="index.html">SARTAM</a><nav>{nav}</nav></header>
<main>{body}</main><footer>SARTAM © Kreator Tre · <a href="https://getinkspired.com" rel="noopener">Read on Inkspired</a></footer>
<script src="veins.js"></script><script src="app.js"></script>{extra}</body></html>'''

wiki=(L/'wiki.md').read_text()
wiki=re.sub(r'^## 6\. Gaps.*$', '## 6. Open Questions (unresolved in canon)', wiki, flags=re.M)
wiki=wiki.replace('# SARTAM Wiki Source Pack','# SARTAM Wiki',1)
heads=re.findall(r'^## (.+)$',wiki,re.M)
toc='<nav class="toc">'+''.join(f'<a href="#{re.sub(r"[^a-z0-9]+","-",h.lower()).strip("-")}">{inline(h)}</a>' for h in heads)+'</nav>'
legend='<p class="legend"><span class="badge lock">Locked</span> canon · <span class="badge prov">Provisional · may change</span> working draft · <span class="spoiler-demo">⚠</span> spoilers hidden until clicked. Cited paths refer to the author\'s source files.</p>'
(O/'wiki.html').write_text(page('Wiki','Wiki',legend+toc+'<article class="md">'+render(wiki)+'</article>'))

qs=[]
for m in re.finditer(r'\*\*Q:\*\*\s*(.+?)\n\s*\*\*A:\*\*\s*(.+?)(?:\s+—\s+`[^`]*`)?\s*$',(L/'trivia.md').read_text(),re.M):
    qs.append({'q':m.group(1).strip(),'a':m.group(2).strip()})
(O/'trivia.html').write_text(page('Trivia','Trivia','<h1>SARTAM Trivia</h1><p>Think of your answer, reveal it, then mark yourself honestly.</p><div id="score" class="score">Score: 0 / 0</div><div id="quiz"></div><button id="reset" class="btn">Restart</button>',
 '<script>const QS='+json.dumps(qs,ensure_ascii=False)+';initQuiz(QS);</script>'))

brief=re.search(r'Universe tagline \[Locked\]: "(.+?)"',wiki).group(1)
home=f'''<section class="hero"><h1 class="glow">SARTAM</h1><p class="tag">{html.escape(brief)}</p>
<p>A mature, anime-inspired saga. The main story is <em>SARTAM: The Novel Series</em> on Inkspired, with eight side stories including <em>SARTAM: The Story of Paulena Pollux</em>.</p>
<div class="cta"><a class="btn" href="wiki.html">Explore the Wiki</a><a class="btn ghost" href="trivia.html">Take the Trivia</a></div></section>
<section class="cards"><div class="card"><h3>F.L.A.W.S. Of Nature</h3><p>Fire, Lightning, Air, Water, Spirit: the five Paths of power.</p></div>
<div class="card"><h3>Five Worlds</h3><p>Cinthyatar, Rijilar, Frigidis, Rhuhun and Zorexon IX.</p></div>
<div class="card"><h3>The Architeks</h3><p>A machine race born from the Katskev, and the shadow over every world.</p></div></section>'''
(O/'index.html').write_text(page('Home','Home',home))
print('built', len(qs), 'questions')
