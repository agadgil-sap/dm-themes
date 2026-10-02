"""Render either logo exploration page and its SVG downloads from authored concepts."""
from pathlib import Path
import argparse
import base64
import html
import io
import json
import zipfile

here = Path(__file__).resolve().parent
root = here.parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--page', type=int, choices=(1, 2), default=1)
page = parser.parse_args().page
source = 'concepts.json' if page == 1 else 'concepts-page-2.json'
board_filename = 'dental-match-logo-exploration' + ('-page-2' if page == 2 else '') + '.html'
bundle = 'dental-match-24-logo-sketches' + ('-page-2' if page == 2 else '') + '.zip'
concepts = json.loads((here / source).read_text())
all_concepts = sum((json.loads((here / name).read_text()) for name in ('concepts.json', 'concepts-page-2.json')), [])
families = list(dict.fromkeys(c['family'] for c in concepts))
assert len(concepts) == 24
assert len({c['id'] for c in concepts}) == 24
assert all(sum(c['family'] == f for c in concepts) == 3 for f in families)
default_id = 'L07' if page == 1 else 'L25'

def is_wordmark(c):
    return c['family'] == 'Wordmarks' or c.get('kind') == 'wordmark'

def palette(c):
    return c.get('palette', {'ink': '#463276', 'soft': '#C7B7EC', 'accent': '#F5D894', 'paper': '#F4F0FB'})

def theme_style(c):
    return ';'.join(f'--{key}:{value}' for key, value in palette(c).items())

def svg(c, cls='', accessible=False):
    semantics = f'role="img" aria-label="{c["id"]}: {html.escape(c["name"])}"' if accessible else 'aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="{c["viewBox"]}" {semantics}><use href="#mark-{c["id"].lower()}"></use></svg>'

def asset(c):
    p = palette(c)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{c["viewBox"]}" color="{p["ink"]}" fill="{p["ink"]}" style="--accent:{p["accent"]}"><title>Dental Match draft {c["id"]}: {html.escape(c["name"])}</title>{c["art"]}</svg>\n'

svg_dir = here / ('svg' if page == 1 else 'svg-page-2')
svg_dir.mkdir(exist_ok=True)
zip_bytes = io.BytesIO()
with zipfile.ZipFile(zip_bytes, 'w', zipfile.ZIP_DEFLATED) as archive:
    for c in concepts:
        filename = c['id'].lower() + '.svg'
        content = asset(c).encode()
        (svg_dir / filename).write_bytes(content)
        entry = zipfile.ZipInfo('dental-match-' + filename, date_time=(1980, 1, 1, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(entry, content)
(here / bundle).write_bytes(zip_bytes.getvalue())
zip_uri = 'data:application/zip;base64,' + base64.b64encode(zip_bytes.getvalue()).decode()

css = '''
*,:before,:after{box-sizing:border-box}
:root{color-scheme:light;--color-primary:#463276;--color-primary-content:#fff;--ink:#463276;--paper:#F4F0FB;--soft:#C7B7EC;--frame:#302D3C;--muted:#696174;--line:#DED8E7}
body{margin:0;background:#F8F7FA;color:var(--frame);font-family:'DM Sans',sans-serif}
h1,h2,h3,p,figure{margin:0}p{line-height:1.65}a{color:inherit;text-underline-offset:4px}button,input,select,textarea{font:inherit}button{cursor:pointer}svg{display:block;fill:currentColor;max-width:100%}button,a,input,select,textarea{touch-action:manipulation}:focus-visible{outline:3px solid #8464B5;outline-offset:4px}[hidden]{display:none!important}
.shell{max-width:1380px;padding-inline:36px;margin:auto}.topbar{background:#fff;border-bottom:1px solid var(--line)}.bar{display:flex;justify-content:space-between;align-items:center;gap:24px;min-height:76px}.studio{font:800 17px Manrope,sans-serif;letter-spacing:-.5px}.studio small{display:block;font:400 11px 'DM Sans',sans-serif;letter-spacing:0;margin-top:4px;color:var(--muted)}nav{display:flex;gap:25px;font-size:12px;flex-wrap:wrap}nav a{text-decoration:none}nav a:hover{text-decoration:underline}
.intro{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);align-items:center;gap:60px;padding-block:48px 35px}.eyebrow{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted)}h1{font:700 clamp(35px,4vw,56px)/1.12 Manrope,sans-serif;letter-spacing:-2px;max-width:660px;margin-top:16px}.intro p{font-size:14px;color:var(--muted);max-width:550px;margin-top:22px}.hero-mosaic{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.hero-mosaic figure{background:#EAE3F5;color:var(--ink);border-radius:17px;min-height:145px;display:flex;align-items:center;justify-content:center;position:relative}.hero-mosaic figure:nth-child(2),.hero-mosaic figure:nth-child(3){background:#fff;border:1px solid var(--line)}.hero-mosaic svg{width:84px;height:84px}.hero-mosaic figcaption{position:absolute;left:13px;bottom:10px;font-size:9px;opacity:.7}
.scope{border-top:1px solid var(--line);border-bottom:1px solid var(--line);display:flex;gap:20px;justify-content:space-between;align-items:center;padding-block:17px;font-size:12px;line-height:1.6}.scope strong{color:var(--ink)}.scope a{flex-shrink:0;font-weight:600;color:var(--ink)}.section-head{display:flex;justify-content:space-between;align-items:end;gap:30px;margin-bottom:22px}h2{font:700 29px/1.2 Manrope,sans-serif;letter-spacing:-.9px}.section-head p{font-size:12px;color:var(--muted);max-width:440px}.gallery-section{padding-top:38px;scroll-margin-top:22px}.filter-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:15px}.filter{border:1px solid var(--line);background:#fff;padding:9px 14px;min-height:40px;border-radius:100px;font-size:11px;color:var(--frame)}.filter[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:#fff}.gallery-count{font-size:11px;color:var(--muted);margin-bottom:20px}
.logo-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}.logo-card{min-width:0;border:1px solid var(--line);border-radius:14px;background:#fff;overflow:hidden;display:flex;flex-direction:column}.logo-card:has(input:checked){outline:2px solid #7B629F;outline-offset:2px}.card-meta{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:13px 16px 0;font-size:9px;color:var(--muted)}.card-meta strong{border:1px solid var(--line);border-radius:5px;padding:5px 7px;font-size:10px;color:var(--ink);font-weight:700}.mark-preview{display:flex;width:100%;align-items:center;justify-content:center;border:0;background:#fff;color:var(--ink);min-height:166px;padding:20px;position:relative}.mark-preview:hover{background:#F8F5FD}.mark-preview svg{width:112px;height:112px}.wordmark-card .mark-preview svg{width:230px;height:110px}.card-body{padding:8px 18px 18px;display:flex;flex-direction:column;flex:1;gap:0}.card-body h3{font:700 16px Manrope,sans-serif;letter-spacing:-.35px;line-height:1.3;min-height:21px}.card-body p{font-size:11px;color:var(--muted);margin-top:8px;min-height:57px;line-height:1.65}.card-actions{display:flex;gap:13px;font-size:10px;margin-top:14px;margin-bottom:13px}.text-button{padding:0;border:0;background:transparent;color:var(--ink);font-size:10px;font-weight:600;text-decoration:underline;text-underline-offset:3px}.pick{display:flex;align-items:center;gap:9px;padding:10px 11px;border:1px solid var(--line);border-radius:7px;font-size:11px;font-weight:600;cursor:pointer;margin-top:auto}.pick input{accent-color:var(--ink);width:16px;height:16px;flex:0 0 16px}.pick:has(input:checked){background:#F0EAF8;border-color:#7B629F}.gallery-note{margin-top:17px;font-size:11px;color:var(--muted)}
.proof-section{margin-top:56px;scroll-margin-top:22px}.proof-controls{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:20px}.field{display:grid;gap:7px;font-size:11px;font-weight:600}.field select{min-height:43px;min-width:220px;border:1px solid #CEC5DC;background:#fff;color:var(--frame);border-radius:7px;padding:9px 32px 9px 12px}.proof-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:20px}.primary-proof{min-height:358px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--paper);color:var(--ink);border:1px solid var(--soft);border-radius:15px;padding:35px;gap:20px}.big-mark{width:152px;height:152px}.primary-proof .brand-name{font:800 28px Manrope,sans-serif;letter-spacing:-1px}.primary-proof .proof-label{font-size:11px;opacity:.8}.primary-proof.is-wordmark .big-mark{width:340px;height:152px}.proof-side{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.proof-tile{min-height:164px;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);padding:16px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:15px}.proof-tile svg{width:70px;height:70px}.proof-tile figcaption{font-size:10px;text-align:center;line-height:1.6}.proof-tile.dark{color:#fff;background:var(--ink);border-color:var(--ink)}.proof-tile.mono{color:#242128}.proof-tile .avatar{border:1px solid var(--soft);background:var(--paper);color:var(--ink);border-radius:17px;padding:8px;width:73px;height:73px}.small-marks{display:flex;align-items:end;gap:19px}.small-marks>span{display:flex;flex-direction:column;align-items:center;gap:8px;flex-shrink:0;font-size:9px}.small-marks svg{width:24px;height:24px}.small-marks>span:nth-child(2) svg{width:48px;height:48px}.proof-tile.is-wordmark svg{width:125px;height:65px}.proof-tile.is-wordmark .small-marks{flex-direction:column;align-items:center;gap:8px}.proof-tile.is-wordmark .small-marks>span svg{width:130px;height:50px}.proof-tile.is-wordmark .small-marks>span:nth-child(2) svg{width:160px;height:61px}.proof-tile.is-wordmark .avatar{width:160px;height:83px;border-radius:7px}.proof-tile.is-wordmark .avatar svg{width:140px;height:65px}.preview-description{margin-top:16px;font-size:12px;line-height:1.7;color:var(--muted);max-width:760px}.read-tip{margin-top:12px;font-size:11px;color:var(--muted)}
.feedback{margin-top:45px;border:1px solid var(--line);border-radius:15px;background:#fff;padding:32px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:45px;scroll-margin-top:22px}.feedback p{font-size:13px;color:var(--muted);margin-top:14px}.feedback label{font-size:12px;font-weight:600}.selection-status{padding:15px;border-radius:8px;background:#F4F0FA;font-size:12px;line-height:1.7;margin-bottom:20px;overflow-wrap:anywhere}.feedback textarea{width:100%;border:1px solid #CEC5DC;border-radius:8px;padding:12px;min-height:104px;font-size:12px;line-height:1.7;background:#fff;margin-top:8px;resize:vertical}.feedback-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:17px}.feedback-actions .btn{font-size:12px;min-height:43px}.form-message{font-size:11px;min-height:22px;line-height:1.6;margin-top:13px}.hint{font-size:10px!important;margin-top:8px!important}.reply-preview{font-size:12px;line-height:1.7;white-space:pre-wrap;overflow-wrap:anywhere;background:#F5F2F9;border-radius:8px;padding:15px;margin-top:13px}footer{padding-block:27px 34px;display:flex;justify-content:space-between;gap:20px;font-size:10px;color:var(--muted)}.symbols{position:absolute;width:0;height:0;overflow:hidden}.intro>*,.logo-grid>*,.proof-grid>*,.proof-side>*,.feedback>*{min-width:0}h1,h2,h3,p,label{overflow-wrap:break-word}
@media(max-width:1150px){.shell{padding-inline:25px}.logo-grid{gap:13px}.card-meta{padding-inline:14px}.card-body{padding-inline:14px}.card-body p{min-height:74px}.mark-preview{min-height:160px}.card-body h3{font-size:15px;min-height:39px}.intro{gap:35px}.primary-proof .brand-name{font-size:25px}.proof-tile.is-wordmark .small-marks>span:nth-child(2) svg{width:130px;height:50px}.proof-tile.is-wordmark .avatar{width:132px;height:74px}.proof-tile.is-wordmark .avatar svg{width:112px;height:56px}}
@media(max-width:900px){.logo-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.intro{gap:25px}.hero-mosaic figure{min-height:125px}.hero-mosaic svg{width:73px;height:73px}.section-head{flex-direction:column;align-items:start;gap:10px}.proof-grid{grid-template-columns:minmax(0,1fr)}.primary-proof{min-height:330px}.proof-side{grid-template-columns:repeat(2,minmax(0,1fr))}.feedback{grid-template-columns:minmax(0,1fr);gap:25px}.proof-tile.is-wordmark .small-marks{flex-direction:row;gap:15px}.proof-tile.is-wordmark .small-marks>span svg{width:110px;height:42px}.proof-tile.is-wordmark .small-marks>span:nth-child(2) svg{width:130px;height:50px}}
@media(max-width:680px){.shell{padding-inline:20px}.bar{align-items:start;flex-direction:column;gap:13px;padding-block:17px}nav{font-size:11px;gap:19px}.intro{grid-template-columns:minmax(0,1fr);padding-block:33px 27px;gap:25px}h1{font-size:40px;letter-spacing:-1.4px}.intro p{font-size:13px;margin-top:17px}.hero-mosaic figure{min-height:126px}.hero-mosaic svg{width:77px;height:77px}.scope{align-items:start;flex-direction:column;gap:10px;font-size:11px}.scope a{flex-shrink:1}.logo-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}.mark-preview{min-height:147px;padding:16px}.mark-preview svg{width:98px;height:98px}.wordmark-card .mark-preview svg{width:190px;height:90px}.card-meta{padding:11px 12px 0;font-size:8px}.card-meta strong{font-size:9px;padding:4px 6px}.card-body{padding:6px 13px 14px}.card-body h3{font-size:14px;min-height:37px}.card-body p{font-size:10px;min-height:83px}.card-actions{font-size:9px;gap:10px}.text-button{font-size:9px}.pick{padding:10px 8px;font-size:10px;gap:7px}h2{font-size:26px}.filter{font-size:10px;padding:9px 12px}.field{width:100%}.field select{width:100%;min-width:0}.proof-section{margin-top:42px}.primary-proof{padding:28px 20px;min-height:340px}.primary-proof .brand-name{font-size:25px}.primary-proof.is-wordmark .big-mark{width:100%;height:150px}.proof-tile{padding:15px 10px}.proof-tile.is-wordmark .small-marks{flex-direction:column}.proof-tile.is-wordmark .small-marks>span svg{width:110px;height:42px}.proof-tile.is-wordmark .small-marks>span:nth-child(2) svg{width:130px;height:50px}.proof-tile.is-wordmark .avatar{width:130px}.proof-tile.is-wordmark .avatar svg{width:108px}.feedback{padding:25px 20px}.feedback-actions{flex-direction:column;align-items:stretch}footer{flex-direction:column;gap:8px}.gallery-section{padding-top:30px}}
@media(max-width:370px){.shell{padding-inline:16px}h1{font-size:35px}.logo-grid{grid-template-columns:minmax(0,1fr)}.mark-preview{min-height:172px}.mark-preview svg{width:115px;height:115px}.wordmark-card .mark-preview svg{width:230px;height:110px}.card-body h3{min-height:0;font-size:16px}.card-body p{min-height:0;font-size:11px}.pick{font-size:11px}.proof-tile.is-wordmark .small-marks>span:nth-child(2) svg{width:112px;height:43px}.proof-tile.is-wordmark .avatar{width:110px;height:67px}.proof-tile.is-wordmark .avatar svg{width:88px;height:47px}.card-meta{font-size:9px}.card-actions,.text-button{font-size:10px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
'''
css += """
.pagination{display:flex;justify-content:space-between;align-items:center;gap:18px;padding-block:20px;border-bottom:1px solid var(--line);font-size:12px}.page-links{display:flex;gap:8px;flex-wrap:wrap}.pagination a{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:9px 16px;border:1px solid var(--line);border-radius:8px;text-decoration:none;background:#fff;font-weight:600}.pagination a[aria-current=page]{background:var(--ink);color:white;border-color:var(--ink)}.pagination.bottom{margin-top:28px;border-top:1px solid var(--line)}.page-two .mark-preview{background:var(--paper)}.page-two .mark-preview:hover{background:var(--soft)}.palette-row{display:flex;align-items:center;gap:5px;margin-top:12px;min-height:17px}.swatch{width:16px;height:16px;border-radius:50%;border:1px solid #00000014;flex-shrink:0}.palette-row small{margin-left:4px;font-size:9px;color:var(--muted)}.primary-proof .brand-name{font-family:var(--brand-font,Manrope),sans-serif}.proof-tile.dark,.proof-tile.mono{--accent:currentColor}
@media(max-width:680px){.pagination{align-items:start;flex-direction:column;gap:10px}.pagination a{padding:9px 13px;font-size:11px}.palette-row{gap:4px;flex-wrap:wrap}.palette-row small{flex-basis:100%;margin:3px 0 0}.swatch{width:14px;height:14px}}
"""
page_meta = {
    1: {
        'title': '24 broad logo concepts / Page 1',
        'description': 'Twenty-four distinct logo concepts for Dental Match across eight creative directions.',
        'eyebrow': 'Go broad. Go creative.',
        'heading': 'Let’s open up<br>the logo.',
        'intro': 'Twenty-four concepts across eight different directions. People, connections, letters, paths and fresh starts all have a place in this round.',
        'hero': ['L02', 'L07', 'L20', 'L13'],
        'scope': '<strong>B’s plum and lilac anchor this round.</strong> Keeping the colour consistent makes the different ideas and silhouettes easier to compare.',
        'gallery_heading': 'Eight directions. Twenty-four possibilities.',
        'note': 'L01-L21 are symbols. L22-L24 explore the name itself as the logo. All are first-round sketches for this broader exploration.',
        'tip': 'Symbols can pair with the friendly B wordmark. Lettering-led concepts show a different typographic personality; their final spacing and letter shapes come after a shortlist.',
        'feedback': 'A useful next choice is the territory: people, a matching symbol, a monogram, a dental clue, or the name itself.',
        'placeholder': 'For example: L02’s profiles, L06’s matching idea and L23’s lettering. Can we make one more warm and less geometric?',
    },
    2: {
        'title': '24 more logo concepts / Page 2',
        'description': 'Three A arch studies, three B smile studies and eighteen new logo concepts in different colours and themes for Dental Match.',
        'eyebrow': 'Your favourites. And fresh possibilities.',
        'heading': 'Familiar shapes.<br>New possibilities.',
        'intro': 'Three studies of A’s arches. Three studies of B’s smile. Then eighteen fresh concepts, with new shapes, colours and personalities to explore.',
        'hero': ['L25', 'L28', 'L41', 'L38'],
        'scope': '<strong>3 arches + 3 smiles + 18 new directions.</strong> The original A and B marks sit alongside their new interpretations. Six further themes broaden the colour and character.',
        'gallery_heading': 'A little familiar. A lot to explore.',
        'note': 'L25 and L28 preserve the original A and B symbols as reference points. L26-L27 and L29-L30 extend them. L31-L48 explore six further themes, with three concepts each.',
        'tip': 'Each concept has its own palette and suggested wordmark style. Try its original colours first, then compare it with A or B. These are draft identities to refine after a shortlist.',
        'feedback': 'You can keep the shape from one concept and the colour or lettering from another. Browse both pages to compare all 48 ideas.',
        'placeholder': 'For example: L26’s arches with L38’s colours, or L29’s people and smile with L45’s lettering.',
    },
}[page]

def pagination(position='top'):
    links = []
    for number, file in ((1, 'dental-match-logo-exploration.html'), (2, 'dental-match-logo-exploration-page-2.html')):
        current = ' aria-current="page"' if number == page else ''
        links.append(f'<a href="{file}" data-logo-page="{number}" data-lavish-action{current}>Page {number} / {"L01-L24" if number == 1 else "L25-L48"}</a>')
    neighbour = 2 if page == 1 else 1
    file = 'dental-match-logo-exploration-page-2.html' if neighbour == 2 else 'dental-match-logo-exploration.html'
    direction = 'Next 24 →' if page == 1 else '← Previous 24'
    return f'<nav class="pagination {position}" aria-label="Logo pages"><div class="page-links">'+''.join(links)+f'</div><a href="{file}" data-logo-page="{neighbour}" data-lavish-action>{direction}</a></nav>'

parts = [f'''<!doctype html>
<!-- Generated from assets/logo-exploration/{source} by assets/logo-exploration/build.py. Edit those sources, then rebuild. -->
<html lang="en-AU" data-theme="winter"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dental Match | {page_meta['title']}</title><meta name="description" content="{page_meta['description']}"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/daisyui.css"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/themes.css"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Lora:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"><style>''', css, f'</style></head><body class="page-{("one" if page == 1 else "two")}">']
parts.append('<svg class="symbols" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs>')
for c in concepts:
    parts.append(f'<symbol id="mark-{c["id"].lower()}" viewBox="{c["viewBox"]}">{c["art"]}</symbol>')
parts.append('</defs></svg>')
parts.append(f'''<header class="topbar"><div class="shell bar"><div class="studio">Dental Match <small>Logo exploration / Page {page} of 2</small></div><nav aria-label="Logo exploration"><a href="#gallery">All 24 logos</a><a href="#proof">Look closer</a><a href="dental-match-ab-refinements.html">A + B styles ↗</a></nav></div></header><main class="shell">''')
parts.append(pagination())
parts.append(f'''<section class="intro" aria-labelledby="page-title"><div><div class="eyebrow">{page_meta['eyebrow']}</div><h1 id="page-title">{page_meta['heading']}</h1><p>{page_meta['intro']}</p></div><div class="hero-mosaic">''')
for id in page_meta['hero']:
    c = next(c for c in concepts if c['id'] == id)
    style = f' style="{theme_style(c)};color:var(--ink);background:var(--paper)"' if page == 2 else ''
    parts.append(f'<figure{style}>{svg(c)}<figcaption>{id} / {html.escape(c["family"])}</figcaption></figure>')
parts.append(f'''</div></section><div class="scope"><p>{page_meta['scope']}</p><a href="{zip_uri}" download="{bundle}">Download these 24 SVG sketches ↓</a></div><form id="logo-form" data-lavish-question="dental-match-logo-shortlist"><section id="gallery" class="gallery-section" aria-labelledby="gallery-title"><div class="section-head"><div><div class="eyebrow">Choose the idea before polishing the details</div><h2 id="gallery-title" style="margin-top:9px">{page_meta['gallery_heading']}</h2></div><p>Tap any symbol to see it larger. Shortlist the ideas you want to develop, including unexpected ones.</p></div><div class="filter-bar" role="group" aria-label="Filter logo concepts">''')
for family in ['All', *families]:
    pressed = 'true' if family == 'All' else 'false'
    parts.append(f'<button class="filter" type="button" data-filter="{html.escape(family)}" aria-pressed="{pressed}">{html.escape(family)}</button>')
parts.append('</div><p class="gallery-count" id="gallery-count" aria-live="polite">Showing all 24 concepts.</p><div class="logo-grid">')
for c in concepts:
    id, name, family = c['id'], c['name'], c['family']
    cls = ' wordmark-card' if is_wordmark(c) else ''
    uri = 'data:image/svg+xml;base64,' + base64.b64encode(asset(c).encode()).decode()
    style = f' style="{theme_style(c)}"' if page == 2 else ''
    swatches = ''
    if page == 2:
        swatches = '<div class="palette-row" aria-label="Suggested palette and lettering">'+''.join(f'<span class="swatch" style="background:{colour}" title="{key}: {colour}"></span>' for key, colour in palette(c).items())+f'<small>{html.escape(c["font"])}</small></div>'
    parts.append(f'<article class="logo-card{cls}" id="logo-{id.lower()}" data-family="{html.escape(family)}"{style}><div class="card-meta"><strong>{id}</strong><span>{html.escape(family)}</span></div><button type="button" class="mark-preview" data-preview="{id}" aria-label="Enlarge {id}: {html.escape(name)}">{svg(c)}</button><div class="card-body"><h3>{html.escape(name)}</h3><p>{html.escape(c["idea"])}</p>{swatches}<div class="card-actions"><button type="button" class="text-button" data-preview="{id}">Look closer</button><a href="{uri}" data-download="{id}" download="dental-match-{id.lower()}-draft.svg">Save SVG</a></div><label class="pick"><input type="checkbox" name="logos" value="{id}">Shortlist {id}</label></div></article>')
parts.append(f'''</div><p class="gallery-note">{page_meta['note']}</p></section>''')
parts.append(pagination('bottom'))
parts.append('''<section id="proof" class="proof-section" aria-labelledby="proof-title"><div class="section-head"><div><div class="eyebrow">Look at the shape in use</div><h2 id="proof-title" style="margin-top:9px">Give an idea a closer look.</h2></div><p>Compare the full identity, a dark background, one-colour use and smaller sizes.</p></div><div class="proof-controls"><label class="field" for="preview-logo">Logo to preview<select id="preview-logo">''')
for c in concepts:
    selected = 'selected' if c['id'] == default_id else ''
    parts.append(f'<option value="{c["id"]}" {selected}>{c["id"]} / {html.escape(c["name"])}</option>')
parts.append('</select></label><label class="field" for="preview-palette">Colour to preview<select id="preview-palette">')
if page == 2:
    parts.append('<option value="original">Concept’s own palette</option>')
parts.append('''<option value="B1">B1 / Plum + lilac</option><option value="B3">B3 / Plum + peach</option><option value="A1">A1 / Forest + sage</option></select></label></div><div class="proof-grid" id="proof-grid"><figure class="primary-proof" id="primary-proof">''')
c = next(c for c in concepts if c['id'] == default_id)
parts.append(svg(c, 'big-mark live-mark') + f'<div class="brand-name" id="brand-name">Dental Match</div><figcaption class="proof-label" id="proof-label">{c["id"]} / {html.escape(c["name"])}</figcaption></figure><div class="proof-side">')
parts.append('<figure class="proof-tile dark">'+svg(c, 'live-mark')+'<figcaption>Reversed on dark colour</figcaption></figure><figure class="proof-tile mono">'+svg(c, 'live-mark')+'<figcaption>One colour</figcaption></figure><figure class="proof-tile"><div class="small-marks"><span>'+svg(c, 'live-mark')+'<span class="size-label">24 px</span></span><span>'+svg(c, 'live-mark')+'<span class="size-label">48 px</span></span></div><figcaption id="size-caption">At icon size</figcaption></figure><figure class="proof-tile"><div class="avatar">'+svg(c, 'live-mark')+'</div><figcaption id="avatar-caption">Social profile sketch</figcaption></figure></div></div><p class="preview-description" id="preview-description"></p>')
parts.append(f'''<p class="read-tip">{page_meta['tip']}</p></section><section class="feedback" id="feedback" aria-labelledby="feedback-title"><div><div class="eyebrow">Keep a few doors open</div><h2 id="feedback-title" style="margin-top:10px">Which ideas have something?</h2><p>Shortlist three to five logos, even if you only like one part of a concept. We can combine an idea from one with the shape or lettering of another.</p><p>{page_meta['feedback']}</p></div><div><div class="selection-status" id="selection-status" aria-live="polite"><div>No logos shortlisted yet.</div><div>Your shortlist includes both pages.</div></div><label for="logo-notes">What catches your eye, and what should change?</label><textarea id="logo-notes" name="notes" placeholder="{page_meta['placeholder']}"></textarea><div class="feedback-actions"><button type="submit" class="btn btn-primary">Queue my shortlist</button><button type="button" class="btn btn-outline" id="copy-feedback">Copy my shortlist</button></div><div class="form-message" id="form-message" role="status"></div><p class="hint">In Lavish, queue your shortlist, then press Send to Agent. On the published page, copy your shortlist into the chat.</p><pre class="reply-preview" id="reply-preview" hidden></pre></div></section></form></main><footer class="shell"><span>Dental Match / Logo exploration / Page {page} of 2 / Draft vector concepts</span><span>The review layout follows B’s palette and typography.</span></footer><script>''')
encoder = json.JSONEncoder(ensure_ascii=False)
parts.append('const pageNumber = '+str(page)+';')
parts.append('const concepts = '+encoder.encode([{**{k:c[k] for k in ['id','name','family','idea','viewBox']}, 'palette':palette(c), 'font':c.get('font', 'Manrope'), 'wordmark':is_wordmark(c)} for c in concepts])+';')
parts.append('const allConcepts = '+encoder.encode([{k:c[k] for k in ['id','name']} for c in all_concepts])+';')
parts.append(r"""
const palettes={B1:{ink:'#463276',soft:'#C7B7EC',accent:'#F5D894',paper:'#F4F0FB'},B3:{ink:'#4F3563',soft:'#E5D9EF',accent:'#E9AD8E',paper:'#FBF5F2'},A1:{ink:'#254B43',soft:'#D9E6DB',accent:'#F1C4AA',paper:'#F1F6F1'}};
const form=document.getElementById('logo-form');
const logoSelect=document.getElementById('preview-logo');
const paletteSelect=document.getElementById('preview-palette');
const proof=document.getElementById('proof-grid');
const summary=document.getElementById('selection-status');
const message=document.getElementById('form-message');
const preview=document.getElementById('reply-preview');
const notes=document.getElementById('logo-notes');
function renderProof(){
  const c=concepts.find(c=>c.id===logoSelect.value),p=paletteSelect.value==='original'?c.palette:palettes[paletteSelect.value];
  for(const key of ['ink','soft','accent','paper'])proof.style.setProperty('--'+key,p[key]);
  proof.style.setProperty('--brand-font',c.font);
  proof.querySelectorAll('.live-mark').forEach(svg=>{svg.setAttribute('viewBox',c.viewBox);svg.querySelector('use').setAttribute('href','#mark-'+c.id.toLowerCase());});
  proof.querySelectorAll('.primary-proof,.proof-tile').forEach(el=>el.classList.toggle('is-wordmark',c.wordmark));
  document.getElementById('brand-name').hidden=c.wordmark;
  document.getElementById('proof-label').textContent=c.id+' / '+c.name;
  document.getElementById('preview-description').textContent=c.idea;
  document.getElementById('size-caption').textContent=c.wordmark?'At compact header width':'At icon size';
  const labels=proof.querySelectorAll('.size-label');
  labels[0].textContent=c.wordmark?'Compact':'24 px';labels[1].textContent=c.wordmark?'Wider':'48 px';
  document.getElementById('avatar-caption').textContent=c.wordmark?'Compact nameplate':'Social profile sketch';
}
logoSelect.addEventListener('change',renderProof);paletteSelect.addEventListener('change',renderProof);renderProof();
document.querySelectorAll('[data-preview]').forEach(button=>button.addEventListener('click',()=>{logoSelect.value=button.dataset.preview;renderProof();document.getElementById('proof').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});}));
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{const family=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));let count=0;document.querySelectorAll('.logo-card').forEach(card=>{card.hidden=family!=='All'&&card.dataset.family!==family;if(!card.hidden)count++;});document.getElementById('gallery-count').textContent=family==='All'?'Showing all 24 concepts.':'Showing '+count+' '+family.toLowerCase()+' concepts. Shortlists from other directions stay selected.';}));
const storageKey='dental-match-logo-shortlist-v1';
function readState(){try{const raw=JSON.parse(localStorage.getItem(storageKey)||'{}');return{logos:Array.isArray(raw.logos)?raw.logos.filter(id=>allConcepts.some(c=>c.id===id)):[],notes:raw.notes&&typeof raw.notes==='object'?raw.notes:{}};}catch{return{logos:[],notes:{}};}}
let state=readState(),saved=true;
function persist(){try{localStorage.setItem(storageKey,JSON.stringify(state));saved=true;}catch{saved=false;}}
function updateSummary(){summary.firstElementChild.textContent=state.logos.length?(saved?'Shortlisted across both pages: ':'Shortlisted on this page: ')+state.logos.join(', ')+'.':'No logos shortlisted yet.';summary.lastElementChild.textContent=saved?'Selections are saved in this browser. Changes have not been queued.':'Keep this review tab open. Queue or copy your shortlist before closing it.';message.textContent='';preview.hidden=true;}
function restore(){form.querySelectorAll('input[name=logos]').forEach(input=>input.checked=state.logos.includes(input.value));notes.value=typeof state.notes[pageNumber]==='string'?state.notes[pageNumber]:'';updateSummary();}
persist();restore();
form.addEventListener('change',event=>{if(event.target.name!=='logos')return;const id=event.target.value;state.logos=state.logos.filter(value=>value!==id);if(event.target.checked)state.logos.push(id);state.logos.sort();persist();updateSummary();});
notes.addEventListener('input',()=>{state.notes[pageNumber]=notes.value;persist();updateSummary();});
window.addEventListener('storage',event=>{if(event.key===storageKey){state=readState();restore();}});
function feedback(){const notesText=[1,2].map(page=>typeof state.notes[page]==='string'&&state.notes[page].trim()?'Page '+page+': '+state.notes[page].trim():'').filter(Boolean).join('\n');if(!state.logos.length&&!notesText)return null;return{logos:state.logos,notes:notesText,text:'Dental Match logo exploration / Pages 1 + 2\nShortlist: '+(state.logos.length?state.logos.map(id=>{const c=allConcepts.find(c=>c.id===id);return id+' / '+c.name;}).join(', '):'Undecided')+'\nPreferences: '+(notesText||'Develop these ideas further.')};}
form.addEventListener('submit',event=>{event.preventDefault();const f=feedback();if(!f){message.textContent='Shortlist a logo or add a note first.';return;}if(window.lavish&&typeof window.lavish.queuePrompt==='function'){window.lavish.queuePrompt(f.text,{tag:'logo-exploration',text:'Dental Match: logo shortlist',element:document.getElementById('feedback'),selector:'#feedback',queueKey:'dental-match-logo-shortlist',data:{question:'dental-match-logo-shortlist',logos:f.logos,notes:f.notes}});summary.lastElementChild.textContent='Shortlist queued.';message.textContent='Shortlist queued. Press Send to Agent in the review bar when ready.';}else{preview.textContent=f.text;preview.hidden=false;message.textContent='Your shortlist is ready below. Copy it into the chat.';}});
document.getElementById('copy-feedback').addEventListener('click',async()=>{const f=feedback();if(!f){message.textContent='Shortlist a logo or add a note first.';return;}try{await navigator.clipboard.writeText(f.text);message.textContent='Shortlist copied. Paste it into the chat.';}catch{preview.textContent=f.text;preview.hidden=false;message.textContent='Select and copy the shortlist below.';}});
// Use the review sessions only inside Lavish; static exports keep relative page links.
document.addEventListener('DOMContentLoaded',()=>{
  if(!window.lavish)return;
  const sessions={1:'f57bb11908b3a723',2:'65cb7bdd23e94d85'};
  document.querySelectorAll('[data-logo-page]').forEach(link=>{
    link.href=new URL('/session/'+sessions[link.dataset.logoPage],location.href).href;
    link.target='_blank';link.rel='noopener';
  });
});
</script></body></html>
""")
board='\n'.join(parts)
assert chr(0x2014) not in board
(root / '.lavish' / board_filename).write_text(board)
print(f'Built logo exploration page {page}, 24 draft SVGs and a downloadable bundle.')
