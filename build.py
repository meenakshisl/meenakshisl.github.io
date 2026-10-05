"""Generate the portfolio from its writing list. Python standard library only."""
from pathlib import Path
from datetime import date
from html import escape
from urllib.parse import urlparse
import json, re
ROOT=Path(__file__).resolve().parent
posts=json.loads((ROOT/'content/writing.json').read_text())
settings=json.loads((ROOT/'content/settings.json').read_text())
rows=[]
for post in sorted(posts,key=lambda p:p['date'],reverse=True):
    published=date.fromisoformat(post['date']) if post['date'] else None
    date_markup=f'<time class="date" datetime="{escape(post["date"])}">{published.strftime("%d %b %Y")}</time>' if published else '<span class="date">Notes</span>'
    if urlparse(post['url']).scheme != 'https':
        raise ValueError('Article URLs must use HTTPS')
    e=lambda key: escape(post[key],quote=True)
    tags=post.get('tags', [post['topic']])
    tag_data=escape(json.dumps(tags),quote=True)
    search_data=escape(' '.join([post['title'],post['description'],post['publisher'],post['topic'],*tags]).casefold(),quote=True)
    tag_labels=''.join(f'<span class="tag">{escape(tag)}</span>' for tag in tags)
    rows.append(f'''<li class="post" data-tags="{tag_data}" data-search="{search_data}">{date_markup}<div><h3><a href="{e('url')}">{e('title')} <span class="arrow" aria-label="external publication">↗</span></a></h3><div class="meta">{e('topic')} &nbsp;·&nbsp; {e('publisher')}</div><p>{e('description')}</p><div class="post-tags">{tag_labels}</div></div></li>''')
token=settings.get('cloudflare_analytics_token','').strip()
if token and not re.fullmatch(r'[a-fA-F0-9]{32}',token):
    raise ValueError('Enter the 32-character Cloudflare Web Analytics token')
analytics=''
if token:
    beacon=escape(json.dumps({'token':token}),quote=True)
    analytics=f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon="{beacon}"></script>'

NAV=[('index.html','Home'),('writing.html','Writing'),('projects.html','Projects'),('resume.html','Résumé')]
def section(title, body):
    return f'<section><h2>{title}</h2><div class="section-body">{body}</div></section>'
resume=ROOT/'assets/resume.pdf'
resume_link='<a class="button" href="assets/resume.pdf" download="Meenakshi-S-L-Resume.pdf">Download résumé ↓</a>' if resume.exists() else '<p class="section-note">My résumé will be available here soon. In the meantime, get in touch through LinkedIn.</p>'
social='<div class="social"><a href="https://github.com/meenakshisl">GitHub ↗</a><a href="https://www.linkedin.com/in/meenakshisl/">LinkedIn ↗</a></div>'
home='<div class="hero"><div class="eyebrow">Security researcher</div><div class="identity"><h1>Meenakshi S L<span>.</span></h1><img class="profile-image" src="assets/profile.jpeg" width="120" height="120" alt="ph03n1x illustrated profile avatar"></div><p class="intro">I’m a Senior Security Engineer at Endor Labs, working on application security, open-source vulnerability research, and static analysis. Previously at VMware; Team bi0s alumna.</p><div class="actions"><a class="button" href="resume.html">View résumé ↗</a><a href="https://www.linkedin.com/in/meenakshisl/">Get in touch ↗</a></div>'+social+'</div>'
home+=section('Background','<div class="experience"><div><span class="label">Industry</span><h3>Endor Labs &amp; VMware</h3><p>At Endor Labs, I work on vulnerability research, AI-assisted static analysis, and security automation. At VMware, I conducted application security testing and contributed to threat modeling and secure design reviews.</p></div><div><span class="label">Community</span><h3>Team bi0s &amp; Team Shakti</h3><p>A background in capture-the-flag competitions and collaborative security learning.</p></div></div>')
home+=section('Focus','<p class="section-note">Vulnerability analysis · Security research · Technical communication</p><p class="section-note">Currently building my penetration testing skills and studying AI security through research papers and hands-on learning.</p>')
home+=section('Freelance &amp; contract work','<p class="section-note">I’m open to freelance and contract engagements in application security, vulnerability analysis, SAST rule development, and security automation.</p><p class="section-note">Have a project in mind? Send a brief outline of the scope, timeline, and expected deliverables.</p><a class="button" href="mailto:meenakshi.sl@protonmail.com">Discuss a project ↗</a>')
all_tags=sorted({tag for post in posts for tag in post.get('tags',[post['topic']])},key=str.casefold)
options=''.join(f'<option value="{escape(tag,quote=True)}">{escape(tag)}</option>' for tag in all_tags)
filters=f'''<form class="writing-filters" role="search" hidden><div><label for="keyword">Search writing</label><input id="keyword" type="search" placeholder="Keyword, title, or CVE…" autocomplete="off"></div><div><label for="tag-filter">Tag</label><select id="tag-filter"><option value="">All tags</option>{options}</select></div><button class="reset-filters" type="reset">Clear filters</button></form><p id="result-count" class="section-note result-count" role="status" aria-live="polite" hidden></p>'''
writing='<div class="hero page-hero"><div class="eyebrow">Articles &amp; analysis</div><h1>Writing<span>.</span></h1><p class="intro">Published work, alongside future notes on pentesting and AI security papers.</p></div><section>'+filters+'<ul class="posts" id="writing-list">'+''.join(rows)+'</ul><p id="no-results" class="section-note" hidden>No articles match those filters. Try another keyword or choose a different tag.</p></section><script src="assets/writing.js" defer></script>'
project_entries=[
('DevSecret','Python · Developer tooling','A command-line tool for a local encrypted vault containing API keys and recovery codes.','https://github.com/meenakshisl/devsecret'),
('pgAdmin vulnerability proof of concept','Python · Vulnerability research','Reproduction code and test files for CVE-2025-13780, accompanying my published pgAdmin research.','https://github.com/meenakshisl/PoC-CVE-2025-13780'),
('Multics protection rings','C · Educational implementation','An exploration of ring-based access control, privilege transitions, and access logging inspired by Multics.','https://github.com/meenakshisl/multics'),
('Stateless password manager','Go · Earlier academic project','A client-server prototype exploring deterministic password generation using a master secret and site details.','https://github.com/meenakshisl/Network-Project'),
('Digital forensics notes','Reference collection · Earlier exploration','Course notes covering acquisition, memory and mobile forensics, and operating-system artifacts. Also listed under Writing.','https://meenakshisl.github.io/digital-forensics-notes/')]
project_sections=''.join(section(escape(title),f'<span class="label">{escape(label)}</span><p class="section-note">{escape(description)}</p><a href="{escape(url)}">'+('Read the notes' if title=='Digital forensics notes' else 'View repository')+' ↗</a>') for title,label,description,url in project_entries)
projects='<div class="hero page-hero"><div class="eyebrow">Code &amp; experiments</div><h1>Projects<span>.</span></h1><p class="intro">Security tools, research reproductions, and earlier explorations.</p></div>'+project_sections

resume_page='<div class="hero page-hero"><div class="eyebrow">Experience &amp; qualifications</div><h1>Résumé<span>.</span></h1><p class="intro">My professional background and experience.</p></div>'+section('Résumé',resume_link+'<p class="section-note"><a href="assets/resume.pdf" target="_blank" rel="noopener">Open PDF in browser ↗</a></p>')+social
for filename,label,body in [('index.html','Home',home),('writing.html','Writing',writing),('projects.html','Projects',projects),('resume.html','Résumé',resume_page)]:
    nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if url==filename else '')+f'>{name}</a>' for url,name in NAV)
    title=escape('Meenakshi S L · '+('Security researcher' if label=='Home' else label))
    html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="Meenakshi S L’s security portfolio, published writing, projects, and professional experience."><meta name="theme-color" content="#f7f6f2"><meta property="og:title" content="{title}"><meta property="og:type" content="website"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css">{analytics}</head><body><a class="skip" href="#main">Skip to content</a><div class="wrap"><header class="top"><a class="brand" href="index.html">Meenakshi / ph03n1x</a><nav aria-label="Main navigation">{nav}</nav></header><main id="main">{body}</main><footer><span>Meenakshi S L / ph03n1x</span><a href="https://www.linkedin.com/in/meenakshisl/">Get in touch ↗</a></footer></div></body></html>"""
    (ROOT/filename).write_text(html)
print(f'Built four pages with {len(rows)} articles. Résumé: {"available" if resume.exists() else "awaiting PDF"}.')
