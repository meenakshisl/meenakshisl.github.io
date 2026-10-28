"""Generate the portfolio from its writing list. Python standard library only."""
from pathlib import Path
from datetime import date
from html import escape
from urllib.parse import urlparse
import json, re
ROOT=Path(__file__).resolve().parent
posts=json.loads((ROOT/'content/writing.json').read_text())
hashnode=ROOT/'content/hashnode.json'
if hashnode.exists():
    known_urls={post['url'].rstrip('/') for post in posts}
    for post in json.loads(hashnode.read_text()):
        if post['url'].rstrip('/') not in known_urls:
            posts.append(post)
            known_urls.add(post['url'].rstrip('/'))
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

NAV=[('index.html','Home'),('writing.html','Writing'),('projects.html','Projects'),('talks.html','Talks'),('resume.html','Résumé')]
def section(title, body):
    return f'<section><h2>{title}</h2><div class="section-body">{body}</div></section>'
resume=ROOT/'assets/resume.pdf'
resume_link='<a class="button" href="assets/resume.pdf" download="Meenakshi-S-L-Resume.pdf">Download résumé ↓</a>' if resume.exists() else '<p class="section-note">My résumé will be available here soon. In the meantime, get in touch through LinkedIn.</p>'
social='<div class="social"><a href="https://github.com/meenakshisl">GitHub ↗</a><a href="https://www.linkedin.com/in/meenakshisl/">LinkedIn ↗</a></div>'
home='<div class="hero home-hero"><div class="home-intro"><div class="eyebrow">Independent Security Researcher</div><h1>Meenakshi S L<span>.</span></h1><p class="intro">I find and investigate vulnerabilities in open-source software, with a focus on application security and static analysis. I build tools and detections to make security research more effective, and share what I learn through writing, talks, and hands-on workshops.</p><p class="home-background">Previously at Endor Labs and VMware.<br>Team bi0s and Team Shakti alumna.</p><div class="actions"><a class="button" href="#research">Explore my research ↗</a><a href="#work">Work with me ↗</a></div></div><img class="profile-image" src="assets/profile.jpeg" width="140" height="140" alt="ph03n1x illustrated avatar"></div>\n<section id="research"><div class="home-section-head"><h2>Selected research</h2><a href="writing.html">More writing ↗</a></div><p class="section-note">Vulnerabilities discovered during my work at Endor Labs.</p><div class="research-grid"><article class="research-card"><span class="label">CVE-2025-13780 · pgAdmin</span><h3>When regex isn’t enough</h3><p>Whitespace handling bypassed a database restore filter, allowing shell commands to execute on the pgAdmin host.</p><div class="research-links"><a href="https://www.endorlabs.com/learn/when-regex-isnt-enough-how-we-discovered-cve-2025-13780-in-pgadmin">Read the research ↗</a><a href="https://github.com/meenakshisl/PoC-CVE-2025-13780">View PoC ↗</a></div></article><article class="research-card"><span class="label">CVE-2025-66626 · Argo Workflows</span><h3>A broken fix, a path to RCE</h3><p>A symlink validation bypass in artifact extraction enabled arbitrary file writes and a path to remote code execution.</p><p class="research-credit">Research and write-up with Cris Staicu.</p><div class="research-links"><a href="https://www.endorlabs.com/learn/when-a-broken-fix-leads-to-rce-how-we-found-cve-2025-66626-in-argo">Read the research ↗</a></div></article></div></section>\n<section id="work"><h2>How I can help</h2><p class="section-note home-section-intro">Available for freelance and contract engagements in:</p><div class="service-grid"><div><span class="label">01 / Application security</span><h3>Test how applications behave</h3><p>Application security testing, source code review, and investigation of security weaknesses, with clear findings and remediation guidance.</p></div><div><span class="label">02 / Vulnerability research</span><h3>Understand the root cause</h3><p>Vulnerability analysis, patch review, and proof-of-concept development to establish how an issue works and what it affects.</p></div><div><span class="label">03 / Static analysis &amp; automation</span><h3>Turn findings into detections</h3><p>Custom Semgrep rules and security automation that turn recurring vulnerability patterns into repeatable checks.</p></div></div><a class="button" href="mailto:meenakshi.sl@protonmail.com">Discuss a project ↗</a></section>\n<section><h2>Writing &amp; tools</h2><div class="home-feature-grid"><article><span class="label">Writing / Vulnerability analysis</span><h3>Host header validation bypass in Undertow</h3><p>An analysis of CVE-2025-12543 and the gap in host header validation.</p><a href="https://www.endorlabs.com/learn/cve-2025-12543-host-header-validation-bypass-in-undertow">Read the article ↗</a><a class="home-more" href="writing.html">All writing ↗</a></article><article><span class="label">Tool / Python</span><h3>DevSecret</h3><p>A command-line tool for a local encrypted vault containing API keys and recovery codes.</p><a href="https://github.com/meenakshisl/devsecret">Explore DevSecret ↗</a><a class="home-more" href="projects.html">All projects ↗</a></article></div></section>\n<section><div class="home-section-head"><h2>Talks &amp; community</h2><a href="talks.html">All talks ↗</a></div><p class="section-note">Some of my best learning has come from people willing to share what they know. Talks and hands-on workshops are one way I pass that on.</p><div class="home-talk-grid"><a class="home-talk" href="talks.html"><img src="assets/talks/inctf-2026.jpg" width="100" height="120" alt="InCTF 2026 speaker poster" loading="lazy"><div><span class="label">InCTF · April 2026</span><h3>AI Security 101</h3><p>Conference talk</p></div></a><a class="home-talk" href="talks.html"><img src="assets/talks/iiit-kottayam-december-2026.jpeg" width="100" height="120" alt="IIIT Kottayam workshop poster" loading="lazy"><div><span class="label">IIIT Kottayam · 7–11 Dec 2026</span><h3>Emerging Frontiers in AI-Driven Cybersecurity</h3><p>Workshop / Faculty Development Program</p></div></a></div></section>\n<section class="home-about"><h2>Background &amp; contact</h2><div class="section-body"><p>My experience spans open-source vulnerability research, static analysis, and security automation at Endor Labs, and application security testing, threat modeling, and secure design reviews at VMware. My roots in Team bi0s and Team Shakti continue to shape how I learn and share knowledge.</p><p class="section-note">I’m currently exploring AI security through research papers and hands-on learning.</p><p>Have a question, a topic to discuss, or a project in mind? Feel free to <a href="https://www.linkedin.com/in/meenakshisl/">reach out on LinkedIn</a> — I’m always happy to connect and exchange ideas.</p><div class="social"><a href="mailto:meenakshi.sl@protonmail.com">Email ↗</a><a href="https://github.com/meenakshisl">GitHub ↗</a><a href="resume.html">Résumé ↗</a></div></div></section>'
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
project_tiles=''.join(f'<li><a class="project-tile" href="{escape(url,quote=True)}"><span class="label">{escape(label)}</span><h2>{escape(title)}</h2><p>{escape(description)}</p><span class="project-tile-link">'+('Read the notes' if title=='Digital forensics notes' else 'View repository')+' <span aria-hidden="true">↗</span></span></a></li>' for title,label,description,url in project_entries)
github_preview='<div class="github-panel"><a class="github-preview" href="https://github.com/meenakshisl" aria-label="Visit meenakshisl on GitHub"><img src="assets/github-avatar.png" alt="" width="72" height="72"><div class="github-preview-text"><span class="label">On GitHub</span><h2>ph03n1x <span>@meenakshisl</span></h2><p>Explore my repositories, security tools, and experiments.</p></div><span class="github-preview-arrow" aria-hidden="true">↗</span></a><div class="contribution-preview"><div class="contribution-heading"><h3>Contributions</h3><a href="https://github.com/meenakshisl?tab=overview">View on GitHub ↗</a></div><div class="contribution-scroll" role="region" aria-label="GitHub contribution graph" tabindex="0"><img src="https://ghchart.rshah.org/244f46/meenakshisl" alt="GitHub contribution activity for meenakshisl over the past year. View on GitHub for details." width="663" height="104"></div><p class="contribution-note">Past year · Graph provided by ghchart</p></div></div>'
projects='<div class="hero page-hero"><div class="eyebrow">Code &amp; experiments</div><h1>Projects<span>.</span></h1><p class="intro">Security tools, research reproductions, and earlier explorations.</p></div>'+github_preview+'<ul class="project-grid" aria-label="Projects">'+project_tiles+'</ul>'

resume_page='<div class="hero page-hero"><div class="eyebrow">Experience &amp; qualifications</div><h1>Résumé<span>.</span></h1><p class="intro">My professional background and experience.</p></div>'+section('Résumé',resume_link+'<p class="section-note"><a href="assets/resume.pdf" target="_blank" rel="noopener">Open PDF in browser ↗</a></p>')+social
talk_entries=json.loads((ROOT/'content/talks.json').read_text())
def talk_row(entry):
    e=lambda key: escape(entry.get(key,''),quote=True)
    stamp=entry['date']
    display=(date.fromisoformat(stamp).strftime('%d %b %Y') if len(stamp)==10 else stamp)
    if entry.get('end_date'):
        display=date.fromisoformat(stamp).strftime('%d')+'–'+date.fromisoformat(entry['end_date']).strftime('%d %b %Y')
    links=[]
    for key,label in [('event_url','Event'),('slides_url','Slides')]:
        url=entry.get(key,'')
        if url:
            if urlparse(url).scheme != 'https' and not url.startswith('assets/talks/'):
                raise ValueError('Talk links must use HTTPS or local talk assets')
            links.append(f'<a href="{escape(url,quote=True)}" aria-label="{label} for {e("title")}">{label} ↗</a>')
    link='<div class="talk-links">'+''.join(links)+'</div>' if links else ''
    description=f'<p>{e("description")}</p>' if entry.get('description') else ''
    image_path=entry['image']
    if not image_path.startswith('assets/talks/') or not (ROOT/image_path).is_file():
        raise ValueError('Each talk needs an existing local image')
    image=f'<a class="talk-image" href="{e("image")}" aria-label="View image for {e("title")}"><img src="{e("image")}" alt="{e("image_alt")}" loading="lazy" width="640" height="360"></a>'
    note=f'<p class="image-note">{e("image_note")}</p>' if entry.get('image_note') else ''
    return f'<li class="post talk-post"><time class="date" datetime="{e("date")}">{escape(display)}</time><div class="talk-content">{image}{note}<h3>{e("title")}</h3><div class="meta">{e("event")} · {e("kind")}</div>{description}{link}</div></li>'

upcoming=[]
past=[]
for entry in sorted(talk_entries,key=lambda x:x['date'],reverse=True):
    (upcoming if entry.get('upcoming') and date.fromisoformat(entry.get('end_date',entry['date'])) >= date.today() else past).append(talk_row(entry))
talks='<div class="hero page-hero"><div class="eyebrow">Sharing knowledge</div><h1>Talks<span>.</span></h1><p class="intro">Some of my best learning has come from people willing to share what they know. I hope to pass that on through talks, trainings, and workshops that make security approachable and encourage people to explore, experiment, and ask questions.</p><p class="intro talk-contact">Have a question, a topic to discuss, or a session in mind? Feel free to <a href="https://www.linkedin.com/in/meenakshisl/">reach out on LinkedIn</a> — I’m always happy to connect and exchange ideas.</p></div>'
if upcoming:
    talks+=section('Upcoming','<ul class="posts">'+''.join(upcoming)+'</ul>')
talks+=section('Past sessions','<ul class="posts">'+''.join(past)+'</ul>')

for filename,label,body in [('index.html','Home',home),('writing.html','Writing',writing),('projects.html','Projects',projects),('resume.html','Résumé',resume_page),('talks.html','Talks',talks)]:
    nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if url==filename else '')+f'>{name}</a>' for url,name in NAV)
    title=escape('Meenakshi S L · '+('Independent Security Researcher' if label=='Home' else label))
    description="Meenakshi S L, independent security researcher focused on open-source vulnerability research, application security, and static analysis." if label=="Home" else "Meenakshi S L’s security portfolio, published writing, projects, and professional experience."
    html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{escape(description,quote=True)}"><meta name="theme-color" content="#f7f6f2"><meta property="og:title" content="{title}"><meta property="og:type" content="website"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css">{analytics}</head><body><a class="skip" href="#main">Skip to content</a><div class="wrap"><header class="top"><a class="brand" href="index.html">Meenakshi / ph03n1x</a><nav aria-label="Main navigation">{nav}</nav></header><main id="main">{body}</main><footer><span>Meenakshi S L / ph03n1x</span><a href="https://www.linkedin.com/in/meenakshisl/">Get in touch ↗</a></footer></div></body></html>"""
    (ROOT/filename).write_text(html)
print(f'Built five pages with {len(rows)} articles. Résumé: {"available" if resume.exists() else "awaiting PDF"}.')
