"""Build DSN's own brand guide and local reference kit from authored content."""
from pathlib import Path
import re, html, json, zipfile, base64
R=Path(__file__).resolve().parents[1]; O=R/'dsn-brand'; O.mkdir(exist_ok=True)
shapes=re.findall(r"^\['(N\d+)','([^']+)','(.*?)','(.*?)'\],?$",(R/'.lavish/dental-support-network.html').read_text(),re.M)
assert len(shapes)==12
colours={'navy':'#1E3549','mist':'#B9CFD8','brass':'#BCA57A','ice':'#EDF3F6','slate':'#526879','line':'#D2DDE3','white':'#FFFFFF','error':'#A42E2E','success':'#246548'}
# Preserve licence text while normalising line endings for the repository.
for licence in O.glob('*-font-licence.txt'):
 licence.write_text('\n'.join(line.rstrip() for line in licence.read_text().splitlines())+'\n')
files=[]
for code,name,description,path in shapes:
 for variant,ink,accent in [('colour','#1E3549','#BCA57A'),('reverse','#FFFFFF','#BCA57A'),('mono','#1E3549','#1E3549')]:
  geom=path.replace('class="accent"',f'stroke="{accent}"')
  group=f'<g fill="none" stroke="{ink}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="square">{geom}</g>'
  mark=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" role="img"><title>{html.escape(name)}</title>{group}</svg>'
  lock=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 90" role="img"><title>Dental Support Network</title><g transform="translate(0 5)">{group}</g><text x="102" y="40" fill="{ink}" font-family="Lora,Georgia,serif" font-size="27" font-weight="500" letter-spacing="-.7">Dental Support</text><text x="103" y="66" fill="{ink}" font-family="DM Sans,Arial,sans-serif" font-size="12" font-weight="500" letter-spacing="4">NETWORK</text></svg>'
  for typ,value in [('mark',mark),('lockup',lock)]:
   f=f'{code.lower()}-{typ}-{variant}.svg'; (O/f).write_text(value); files.append(f)
S=[]
def add(id,title,intro,blocks):S.append({'id':id,'title':title,'intro':intro,'blocks':blocks})
def prose(title,text):return {'type':'prose','title':title,'text':text}
def rows(head,items):return {'type':'table','head':head,'rows':items}
def bullets(items):return {'type':'list','items':items}
add('foundation','01 / Brand foundation','Quiet confidence, developed for a clinic audience.',[
prose('The business','Dental Support Network is a B2B brand for Australian clinic owners and practice managers. Its starting proposition is finding, qualifying and booking implant patients for clinics.'),
prose('Positioning','A considered patient acquisition partner, supporting clear conversations, a useful handover and a coordinated next step into a clinic consultation.'),
prose('Character','Composed, human, precise and dependable. Explain the work in concrete terms. Earn confidence with evidence and useful detail.'),
prose('Relationship to Dental Match','Dental Match speaks to patients; Dental Support Network speaks to clinics. Keep each brand’s name, lead journey, contact details and audience clear.'),
rows(['Status','Meaning'],[('Established inputs','Dental Support Network; B2B; Australia; original Theme C; founder-supplied hero message.'),('Working baseline','C1 / Established partner and N01 / The connection. A documented default pending final selection.'),('Explorations','C2, C3 and N02–N12 remain alternatives. Do not combine logo families in one experience.'),('Needs business input','Qualification criteria, service scope, prices, integrations, hours, response times, contact details and results claims.')])])
add('identity','02 / Logo & identity','Two open brackets. One considered connection.',[
{'type':'logos'},prose('N01 / The connection','The brackets translate original Theme C into a compact signature. Two sides share a small brass connection. This suggests support and coordination without a literal tooth.'),
prose('Primary lockup','Use the supplied horizontal logo for navigation, proposals and partner materials. Display the full name on first contact. Use a symbol-only asset after the brand name is established.'),
prose('Artwork status','The supplied SVGs are concept assets. Symbols use vector paths; wordmarks use editable live text with Lora and DM Sans fallbacks. Final production masters need approved geometry and outlined lettering.'),
rows(['Use','Asset'],[('Light background','n01-lockup-colour.svg'),('Navy background','n01-lockup-reverse.svg'),('One ink','n01-lockup-mono.svg'),('Avatar / favicon','n01-mark-colour.svg')])])
add('logo-rules','03 / Logo application','Keep the signature stable and give it room.',[
{'type':'clearspace'},rows(['Rule','Working specification'],[
('Clear space','Reserve 20 units around the 80-unit symbol frame, one quarter of the symbol frame on every side. Around a lockup use one quarter of its rendered symbol size.'),
('Digital minimum','Symbol: 24 px frame, preferably 32–48 px in UI. Full lockup: 240 px wide. Smaller headers should use the symbol beside readable HTML text.'),
('Print minimum','Proposed lockup minimum 45 mm wide; symbol minimum 8 mm. Proof on the actual material before production.'),
('Colour / background','Colour on white or ice; reverse on navy; monochrome for single-ink output. Use a solid quiet panel on photography.'),
('Scaling','Preserve aspect ratio and viewBox. Do not stretch, rotate, crop, redraw, change stroke proportions, add effects or recolour the connection.'),
('Alternatives','N02–N12 are review options. A final selection requires updating the guide, master assets, favicon, specification and defaults together.')]),
prose('Do','Use the supplied asset, a readable full name, consistent clear space and a restrained background. Check at the real display size.'),
prose('Avoid','Mixing concepts, gradients within the mark, decorative shadows, low-contrast placement and replacing the full name with DSN on first contact.')])
def lum(h):
 c=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 return sum(w*(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for v,w in zip(c,[.2126,.7152,.0722]))
def contrast(a,b):
 lo,hi=sorted([lum(a),lum(b)]); return (hi+.05)/(lo+.05)
add('colour','04 / Colour system','Navy carries the brand. Brass adds a measured accent.',[
{'type':'swatches'},rows(['Role','Use'],[
('Navy','Headlines, primary buttons, core logo ink and C1 hero backgrounds.'),('White / ice','Readable page backgrounds, cards and alternate surfaces.'),('Mist','Secondary text on navy, quiet diagram lines and accent surfaces. Avoid mist body text on white.'),('Brass','Small decorative details and the connection line. Suggested accent area below 5%. Do not use for normal text on light backgrounds.'),('Slate','Secondary body text on white and ice. Do not reduce opacity until small text becomes faint.'),('Line','Card borders and dividers. Use slate for form boundaries that need sufficient contrast.'),('Error / success','Proposed functional extensions, with explicit wording and an icon where useful. Do not rely on colour alone.')]),
rows(['Text / background','Contrast','Normal text'],[(a+' / '+b,f'{contrast(colours[a],colours[b]):.2f}:1','Passes 4.5:1' if contrast(colours[a],colours[b])>=4.5 else 'Does not pass 4.5:1') for a,b in [('navy','white'),('navy','ice'),('slate','white'),('slate','ice'),('mist','navy'),('brass','navy'),('brass','white'),('error','white'),('success','white')]])])
add('type','05 / Typography','Editorial headlines. Practical interfaces.',[
{'type':'type'},rows(['Role','Specification','Behaviour'],[
('Hero','Lora 400, 48–60 px desktop, 30–38 px phone.','Line height 1.14, tracking -0.02em. One dominant heading.'),('Section heading','Lora 500, 32–40 px desktop, 28–32 px phone.','Line height 1.2. Avoid long all-caps text.'),('Card heading','Lora 500, 22–26 px.','Line height 1.25. Keep concise.'),('Body','DM Sans 400, 16 px.','Line height 1.6, approximately 45–75 characters per line.'),('Buttons / fields','DM Sans 500–600, 14–16 px.','Sentence case; essential form text at least 16 px.'),('Eyebrows','DM Sans 600, 11–12 px.','Short uppercase text, tracking 0.12–0.16em. No critical long copy.'),('Fallbacks','Lora → Georgia → serif; DM Sans → Arial → sans-serif.','Load only needed weights with font-display: swap.')]),
prose('Font distribution','Fonts are referenced through their official Google Fonts distributions. The local HTML uses embedded fonts when available, otherwise named fallbacks. SVG wordmarks require installed fonts until lettering is outlined. Preserve font licences when distributing font files.')])
add('layout','06 / Layout & spacing','One consistent rhythm across websites and documents.',[
rows(['Pattern','Working standard'],[
('Spacing','4, 8, 12, 16, 24, 32, 48, 64 and 80 px. Use this scale for gaps and padding.'),('Container','Maximum content width 1200 px; gutters 48 px desktop, 32 px tablet, 20–24 px phone.'),('Sections','64–80 px vertical desktop, 40–48 px mobile. Related elements should sit closer than separate sections.'),('Cards','24–32 px desktop padding, 20–24 px mobile. Keep padding identical in a repeated group.'),('Grids','Use minmax(0, 1fr) and min-width: 0 on nested children. Collapse three columns to two and one as content requires.'),('Corners','3 px buttons, 6 px cards, 8–10 px framed views. Avoid rounded pills as the dominant layout style.'),('Borders / shadow','1 px line borders; soft low-opacity navy shadow only where useful. Hierarchy must work without shadow.'),('Breakpoints','Mobile first; proposed thresholds 700 and 1000 px. Check real content at 320, 390, 820 and 1440 px.'),('Hero','Default C1: navy split hero, a clear headline, one primary CTA and an explanatory process illustration. Stack on mobile.'),('Motion','120–180 ms understated transitions. Honour reduced motion. Avoid parallax, autoplay and decorative movement.')]),
prose('Content order','Explain the service first, show Find / Qualify / Book, describe the clinic handover, answer questions and offer one clear next step.'),prose('Mobile','Allow natural heading wraps. Remove forced desktop line breaks on phones. Check the longest field labels, headings and buttons.')])
add('components','07 / Reusable components','Use one component family, with deliberate states.',[
{'type':'components'},rows(['Component','Rules'],[
('Header','Full brand name, compact symbol, 3–5 links maximum and one enquiry action. A mobile menu needs keyboard support and aria-expanded.'),('Primary button','Navy/white on light; ice/navy on dark. At least 44×44 px target, preferably 48 px high. Use a clear action, such as Discuss your clinic.'),('Secondary action','Transparent, navy text and slate border on light. Distinct hover and visible focus.'),('Links','Underline links in body copy. Navigation can omit underline. Never use colour as the only indicator.'),('Cards','Concise title, useful support text, 24 px padding and a 1 px line border. Avoid redundant actions in every card.'),('Process','Number, short verb, explanation and handover/output. Use Find → Qualify → Book consistently.'),('FAQ','Use native details/summary or an accessible disclosure. Keep qualification wording accessible and easy to find.'),('Statuses','Plain-language message and next step. Announce dynamic results appropriately; do not rely on a colour change.'),('Icons','Simple line icons, 1.5–2 px stroke at 24 px. Hide decorative icons and label meaningful icon-only controls.'),('Footer','Full brand, actual approved contact/legal links. Do not fabricate an ABN, phone number, address or accreditation.')])])
add('forms','08 / Forms & journeys','Make the next step clear and collect only useful information.',[
{'type':'form'},bullets([
'Use visible labels, required/optional wording and relevant examples. Placeholders never replace labels.',
'Start with clinic name, contact name, work email and topic. Add phone only when needed and explain why. Do not collect patient medical information in a clinic partnership form.',
'Production autocomplete tokens should reflect name, organisation, email and telephone. Inputs should be at least 48 px high with 16 px text.',
'Use a slate boundary and a 3 px focus outline. Explain errors in text, associate hints/errors using aria-describedby and apply aria-invalid where needed.',
'Validate on submit and after relevant interaction. Preserve answers on failure. Focus an error summary or the first invalid field.',
'Include idle, editing, invalid, submitting, confirmed success and failure-with-retry states. Prevent duplicate submission.',
'Show success only after the server confirms receipt. State the real next step and an approved response expectation.',
'For multiple steps, show progress, support back navigation and preserve entries in memory. Keep marketing consent separate where applicable.',
'Never send names, emails, phone numbers, health details or field contents to analytics or session replay. Track start, step complete, error and confirmed receipt as distinct non-sensitive events.',
'Label interactive demos honestly. A demo confirmation must state that no enquiry or booking was sent.'
])])
add('voice','09 / Voice & messaging','Calm authority. Specific actions. Human conversations.',[
prose('Core proposition','We find, qualify and book implant patients for clinics.'),
prose('Supporting message','From the first enquiry to a booked consultation, we handle the conversations that help patients take the next step with your clinic.'),
prose('Writing style','Clear, measured and practical. Use Australian English: enquiry, colour, organisation. Speak to clinic owners and practice managers. Reassure through useful detail and clear next actions.'),
rows(['Prefer','Avoid'],[
('We coordinate the next step with your clinic.','We guarantee a full appointment book.'),('Understand the patient’s goals and readiness.','Every lead is clinically qualified.'),('Give your team useful context for the consultation.','Fully vetted implant candidates.'),('Discuss your clinic.','Unlock explosive growth now.'),('Find, qualify and book.','Vague end-to-end solutions or leads, leads, leads.'),('Your dentist assesses clinical suitability.','Marketing copy that diagnoses, guarantees eligibility or promises treatment outcomes.')]),
prose('What qualify means','Qualification means an agreed enquiry and booking process. It is not a clinical diagnosis. The clinic’s dentist determines treatment suitability. Explain this near the process and in FAQs.')])
add('imagery','10 / Imagery & graphics','Show people and process with restraint.',[
prose('Photography','Prefer real clinic teams, calm consultation conversations and credible clinical environments. Use natural light and grounded expressions. Obtain permission for identifiable people and patient imagery.'),
prose('Avoid','Graphic procedures, exaggerated perfect smiles, generic handshake stock, fabricated case studies, synthetic testimonials and unapproved before-and-after photographs.'),
prose('Illustration','Use simple SVG lines in navy, mist and brass. Explain enquiry, conversation and appointment. Keep meaningful diagrams labelled and accessible.'),
prose('Composition','One clear subject and generous negative space. Place text on a solid panel when contrast is uncertain. Avoid heavy gradients, ornamental 3D graphics and busy backgrounds.'),{'type':'process'}])
add('applications','11 / Applications','Keep the identity consistent across channels.',[
rows(['Medium','Specification'],[
('Website / landing page','C1 default, full name in header, focused hero and one primary CTA. Show process, scope, FAQs and an approved enquiry path.'),('Social profile','N01 symbol on navy or ice with safe space for circular cropping. Full profile name: Dental Support Network.'),('Social / paid creative','One message, one visual, one CTA. Suggested 1080×1080 and 1080×1350 templates. Check current platform safe areas. Lead with the clinic proposition.'),('Presentation','16:9 canvas. Navy title slide and ice content slides. Lora headings, DM Sans body. One central message per slide; source evidence and label sample numbers.'),('Proposal / one-pager','A4 format, headline, Find / Qualify / Book, agreed scope and next action. Navy text and readable type; avoid tiny brass copy.'),('Email','Important content as live text, compact linked logo and one clear next action. Georgia / Arial fallback where custom fonts are not supported.'),('Email signature','Name, role, approved contact details and compact logo. No fabricated awards, accreditations or banners.'),('Forms','Reuse input, label, focus, error and success components. Separate clinic enquiries from Dental Match patient journeys.'),('Print','Approved vector masters with outlined type. Convert colours for the print process and proof the result; hex is not a certified print specification.')])])
add('accessibility','12 / Accessibility & claims','A brand should work for everyone who uses it.',[
bullets([
'Aim for WCAG 2.2 AA in production. Normal text needs 4.5:1 contrast, large text 3:1, and meaningful UI boundaries/focus at least 3:1 against adjacent colours.',
'Use one H1, logical heading order, landmarks, a skip link, useful alt text and accessible names for icon-only controls.',
'Check keyboard navigation. Dialogs need an accessible name, sensible focus, Escape support and restored focus on close.',
'Check 200% zoom and 320 CSS px reflow. Only deliberate, labelled data regions should scroll horizontally.',
'Prefer 44×44 px targets and 16 px essential body/form text. Do not hide important copy in small captions.',
'Honour reduced motion. Avoid autoplay audio, flashing and unnecessary animation.',
'Publish results, prices, endorsements, certifications and clinic/patient counts only with approved evidence and permission.',
'Do not imply clinical credentials, treatment eligibility, funding access, partnerships, performance guarantees or response-time commitments without support.',
'Label prototypes and sample content conspicuously. A live form needs real receipt handling, an approved privacy notice and an agreed follow-up owner.'
])])
prompt='''Create an asset for Dental Support Network, an Australian B2B patient acquisition brand for clinic owners and practice managers.
Read brand-rules.md, brand-spec.json and tokens.css before designing.
Use C1 / Established partner and N01 / The connection as the working baseline, pending final selection.
Use supplied SVG assets; do not redraw or mix logo families.
Use Lora headlines and DM Sans body/UI.
Use navy #1E3549, ice #EDF3F6, white #FFFFFF, mist #B9CFD8 and restrained brass #BCA57A.
Use navy or slate body text on light backgrounds; avoid light-background brass/mist body text.
Core message: We find, qualify and book implant patients for clinics.
Qualification is enquiry and booking qualification; clinical suitability belongs to the clinic’s dentist.
Use Australian English, concrete actions, 24 px card padding, consistent spacing and responsive layouts.
Reuse existing components and tokens.
Do not invent prices, metrics, testimonials, contact details or service commitments.
Label sample data and demos honestly.
Check contrast, keyboard use, focus, labels, 320 px reflow and all form states.
Return the artifact with validation performed and business inputs still needing approval.
Task: [asset, audience, channel, dimensions, content and interactions].'''
add('agents','13 / AI agent reference','Readable rules, structured tokens and a reusable brief.',[
prose('Read before creating','Read the Markdown rules, JSON specification and CSS tokens from the same version. Check the working status and asset paths before creating pages, assets, forms or presentations.'),
rows(['Sequence','Requirement'],[
('1 / Read','Confirm the name, audience, default theme, logo and version.'),('2 / Reuse','Prefer existing UI components. Map colours, typography and spacing to the documented tokens.'),('3 / Implement','Use semantic HTML and complete interaction states. Do not silently change the brand default.'),('4 / Verify','Inspect desktop and phone output, keyboard use and contrast. Check copy against verified business facts.'),('5 / Report','List validation, departures from the guide and unresolved business details.'),('Conflicts','Current explicit human instructions take priority. Identify conflicts rather than inventing a compromise or replacing approved artwork.')]),{'type':'prompt','text':prompt}])
add('downloads','14 / Downloads & local use','A portable reference for designers, developers and AI tools.',[
{'type':'downloads'},prose('How to use locally','Download and extract the ZIP. Open dental-support-network-brand.html in any browser. Keep the dsn-brand folder beside it for downloads. The standalone guide embeds its illustrations and fonts when available; no server is required.'),
prose('For an AI agent','Provide dsn-brand/brand-rules.md and brand-spec.json, plus tokens.css and the relevant SVG assets. The kit contains no API credentials or lead data. A Markdown-aware tool can use the rules directly.'),
prose('Asset limitations','72 SVG files cover 12 concepts, two formats and three colour variants. Logos are vector sketches with editable live wordmark text. Install the specified fonts or refine and outline approved artwork before external production.'),{'type':'library'}])
add('governance','15 / Governance & checklist','Maintain one working reference.',[
prose('Version & approval','v0.1, 6 October 2026. C1 and N01 are a working baseline, not a final logo decision. The colour/type foundation comes from the original Theme C; detailed application rules are proposed standards.'),
prose('Source ownership','Edit scripts/build-dsn-brand.py for the guide and kit. Edit .lavish/dental-support-network.html for the exploration. Rebuild generated outputs instead of editing generated files manually.'),
prose('Next decisions','Choose the final direction and logo. Refine and outline wordmark masters, verify service wording, and approve real contact, privacy and operating details before launch.'),
bullets(['Correct name, audience, core message and Australian English.','One logo family, correct colours and sufficient clear space.','Readable typography, aligned padding and consistent spacing.','Clear CTA, functional navigation and complete form states.','Accessible focus, contrast, labels and mobile reflow.','Evidence for claims; sample content and demos labelled.','Guide, JSON, CSS and downloadable kit all match.'])])
# Markdown derives from the same authored blocks, with complete sentences on separate lines.
md='# Dental Support Network brand rules\n\nv0.1 / Working reference / 6 October 2026\n\nC1 and N01 are proposed defaults pending final selection.\n'
for s in S:
 md+='\n## '+s['title']+'\n\n'+s['intro']+'\n\n'
 for b in s['blocks']:
  if b['type']=='prose':md+='### '+b['title']+'\n\n'+'\n'.join(re.split(r'(?<=[.!?])\s+(?=[A-Z])',b['text']))+'\n\n'
  elif b['type']=='list':md+='\n'.join('- '+x for x in b['items'])+'\n\n'
  elif b['type']=='table':
   md+='| '+' | '.join(b['head'])+' |\n| '+' | '.join('---' for _ in b['head'])+' |\n'
   md+=''.join('| '+' | '.join(x)+' |\n' for x in b['rows'])+'\n'
  elif b['type']=='prompt':md+='### Reusable agent brief\n\n'+b['text']+'\n'
md+='\n## Asset paths\n\nUse dsn-brand/n01-lockup-colour.svg, n01-lockup-reverse.svg and n01-mark-colour.svg for the working default.\nThe alternative concepts remain exploration-only.\n'
(O/'brand-rules.md').write_text(md); (O/'agent-prompt.txt').write_text(prompt+'\n')
spec={'version':'0.1','date':'2026-10-06','status':'working-reference-pending-final-selection','brand':'Dental Support Network','audience':['Australian clinic owners','practice managers'],'business_type':'B2B','proposition':'We find, qualify and book implant patients for clinics.','working_default':{'direction':'C1','logo':'N01','final_approved':False},'palette':colours,'typography':{'display':{'family':'Lora','weights':[400,500],'fallback':'Georgia,serif'},'body':{'family':'DM Sans','weights':[400,500,600],'fallback':'Arial,sans-serif','size_px':16,'line_height':1.6}},'spacing_px':[4,8,12,16,24,32,48,64,80],'layout':{'max_width_px':1200,'gutter_px':{'desktop':48,'tablet':32,'mobile':24},'card_padding_px':24,'breakpoints_px':[700,1000]},'radius_px':{'button':3,'card':6,'frame':9},'accessibility':{'normal_text_contrast':4.5,'large_text_contrast':3,'non_text_contrast':3,'target_px':44,'test_widths_px':[320,390,820,1440]},'qualification':'Enquiry and booking qualification, not clinical diagnosis.','clinical_suitability_owner':'Clinic dentist','form_states':['idle','editing','invalid','submitting','confirmed-success','failure-with-retry'],'claims_require_evidence':True,'never_invent':['metrics','prices','testimonials','clinical eligibility','response times','contact details','service commitments'],'assets':{'path':'dsn-brand/','lockup':'n01-lockup-colour.svg','reverse':'n01-lockup-reverse.svg','mark':'n01-mark-colour.svg','wordmarks':'editable SVG text; not outlined','concepts':[x[0] for x in shapes]},'sections':S}
(O/'brand-spec.json').write_text(json.JSONEncoder(indent=2,ensure_ascii=False).encode(spec)+'\n')
css_tokens='/* Generated by scripts/build-dsn-brand.py. DSN working v0.1. */\n:root {\n'+''.join(f'  --dsn-{k}: {v};\n' for k,v in colours.items())+'''  --dsn-font-display: "Lora", Georgia, serif;
  --dsn-font-body: "DM Sans", Arial, sans-serif;
  --dsn-body-size: 16px;
  --dsn-body-line-height: 1.6;
  --dsn-content-width: 1200px;
  --dsn-gutter: 24px;
  --dsn-card-padding: 24px;
  --dsn-radius-button: 3px;
  --dsn-radius-card: 6px;
  --dsn-radius-frame: 9px;
  --dsn-focus: #337590;
'''+''.join(f'  --dsn-space-{n}: {n}px;\n' for n in [4,8,12,16,24,32,48,64,80])+'''}
@media (min-width:700px) { :root { --dsn-gutter:32px; } }
@media (min-width:1000px) { :root { --dsn-gutter:48px; } }
'''
(O/'tokens.css').write_text(css_tokens)
E=html.escape
def tbl(b):
 return '<div class="table-scroll" tabindex="0" role="region" aria-label="'+E(b['head'][0])+' table"><table><thead><tr>'+''.join('<th scope="col">'+E(x)+'</th>' for x in b['head'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+('<a href="dsn-brand/'+x+'" download>Download SVG</a>' if x.endswith('.svg') else E(x))+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>'
def render(b):
 t=b['type']
 if t=='prose':return '<article class="card"><h3>'+E(b['title'])+'</h3><p>'+E(b['text'])+'</p></article>'
 if t=='table':return tbl(b)
 if t=='list':return '<ul>'+''.join('<li>'+E(x)+'</li>' for x in b['items'])+'</ul>'
 if t=='logos':return '<div class="pair"><div class="logo-display"><img src="dsn-brand/n01-lockup-colour.svg" alt="Dental Support Network colour logo"></div><div class="logo-display dark"><img src="dsn-brand/n01-lockup-reverse.svg" alt="Dental Support Network reverse logo"></div></div>'
 if t=='clearspace':return '<div class="clearspace"><img src="dsn-brand/n01-mark-colour.svg" alt="N01 with clear space"><p>Minimum clear space: ¼ of the symbol’s 80-unit frame on all sides.</p></div>'
 if t=='swatches':return '<div class="swatches">'+''.join(f'<article class="swatch"><div style="background:{v}"></div><h3>{k.title()}</h3><button data-copy="{v}" class="copy-code" aria-label="Copy {k} colour">{v} <span>Copy</span></button></article>' for k,v in colours.items())+'</div>'
 if t=='type':return '<div class="type-specimen"><p class="eyebrow">Lora / 400–500</p><p class="display">A considered partner.<br>A clearer next step.</p><p class="eyebrow">DM Sans / 400–600</p><p>From first enquiry to booked consultation, make the next action clear.</p></div>'
 if t=='components':return '<div class="component-demo"><p class="eyebrow">Action styles</p><button class="button" data-toast="Primary action style sample">Discuss your clinic ↗</button><button class="button outline" data-toast="Secondary action style sample">See how we work</button><p class="note">Style samples only. No enquiry is opened or sent.</p></div>'
 if t=='form':return '<div class="form-sample"><h3>Tell us about your clinic.</h3><p class="note">Styling sample only. Nothing is sent or saved.</p><label for="sample-clinic">Clinic name (required)</label><input id="sample-clinic" placeholder="Example Dental Clinic" autocomplete="off"><label for="sample-email">Work email (required)</label><input id="sample-email" type="email" placeholder="you@example.com" autocomplete="off" aria-describedby="sample-hint"><p id="sample-hint" class="note">Use an address where your team can be reached.</p><p class="error-example">Example error: enter a valid work email.</p></div>'
 if t=='process':return '<div class="process" role="img" aria-label="Find an enquiry, qualify through conversation, book a consultation"><svg viewBox="0 0 720 180" aria-hidden="true"><path d="M100 70h520" stroke="#B9CFD8" stroke-width="2"/><g fill="#EDF3F6" stroke="#1E3549"><circle cx="100" cy="70" r="32"/><circle cx="360" cy="70" r="32"/><circle cx="620" cy="70" r="32"/></g><g fill="#1E3549" font-family="Lora,Georgia,serif" font-size="23" text-anchor="middle"><text x="100" y="78">01</text><text x="360" y="78">02</text><text x="620" y="78">03</text></g><g fill="#1E3549" font-family="DM Sans,Arial,sans-serif" font-size="17" text-anchor="middle"><text x="100" y="137">Find</text><text x="360" y="137">Qualify</text><text x="620" y="137">Book</text></g></svg></div>'
 if t=='prompt':return '<div class="agent-panel"><h3>A reusable agent brief.</h3><div class="links"><a href="dsn-brand/brand-rules.md" download>Markdown rules</a><a href="dsn-brand/brand-spec.json" download>JSON specification</a><a href="dsn-brand/tokens.css" download>CSS tokens</a></div><button class="button light" data-copy="'+E(b['text'],quote=True)+'">Copy agent brief</button><pre tabindex="0" aria-label="Agent brief">'+E(b['text'])+'</pre><a href="dsn-brand/agent-prompt.txt" download>Download brief</a></div>'
 if t=='downloads':return '<div class="download-feature"><div><h3>A complete local kit.</h3><p>Extract, open and reference. Includes the local guide, 72 SVGs, rules, specification and tokens.</p></div><a class="button" href="dsn-brand/dsn-brand-kit.zip" download>Download ZIP ↗</a></div><div class="links"><a href="dsn-brand/brand-guide-offline.html" download>Standalone HTML guide</a><a href="dsn-brand/brand-rules.md" download>Rules / Markdown</a><a href="dsn-brand/brand-spec.json" download>Specification / JSON</a><a href="dsn-brand/tokens.css" download>Tokens / CSS</a></div>'
 if t=='library':return '<div class="asset-grid">'+''.join(f'<article class="card"><div class="asset-preview"><img src="dsn-brand/{code.lower()}-lockup-colour.svg" alt="{E(name)} concept"></div><h3>{code} / {E(name)}</h3><p>{"Working default" if code=="N01" else "Exploration only"}</p><div class="links">'+''.join(f'<a href="dsn-brand/{code.lower()}-{typ}-{variant}.svg" download>{label}</a>' for typ,variant,label in [('lockup','colour','Colour'),('lockup','reverse','Reverse'),('lockup','mono','Mono'),('mark','colour','Mark')])+'</div></article>' for code,name,desc,p in shapes)+'</div>'
 raise ValueError(t)
nav=''.join(f'<a href="#{s["id"]}">{E(s["title"])}</a>' for s in S)
body=''
for s in S:
 body+=f'<section id="{s["id"]}"><h2>{E(s["title"])}</h2><p class="intro">{E(s["intro"])}</p>'
 blocks=s['blocks']; i=0
 while i<len(blocks):
  if blocks[i]['type']=='prose':
   body+='<div class="cards">'
   while i<len(blocks) and blocks[i]['type']=='prose':body+=render(blocks[i]);i+=1
   body+='</div>'
  else:body+=render(blocks[i]);i+=1
 body+='</section>'
style=(R/'scripts/dsn-brand-guide.css').read_text()
font_css=(O/'fonts.css').read_text() if (O/'fonts.css').exists() else ''
font_link='' if font_css else '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Lora:wght@400;500&display=swap" rel="stylesheet">'
page='''<!doctype html>
<!-- Generated by scripts/build-dsn-brand.py. Edit the source, not this output. -->
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Dental Support Network | Brand guidelines</title><meta name="description" content="Dental Support Network working brand guide, logo assets and AI agent reference."><link rel="icon" href="dsn-brand/n01-mark-colour.svg">'''+font_link+'<style>'+font_css+style+'''</style></head><body><a class="skip" href="#foundation">Skip to guidelines</a><header><div class="top"><a href="#" aria-label="Dental Support Network brand guide home"><img src="dsn-brand/n01-lockup-colour.svg" alt="Dental Support Network"></a><nav aria-label="Brand guide"><a href="dental-support-network-exploration.html">Website & logos ↗</a><a href="#downloads">Downloads</a><button onclick="window.print()" class="print-button">Print / PDF</button></nav></div></header><div class="hero"><p class="eyebrow">Theme C / Quiet confidence / Brand reference</p><h1>A considered identity.<br>A shared standard.</h1><p>Guidelines for people and AI agents creating Dental Support Network websites, forms, presentations and partner materials.</p><div class="hero-actions"><a class="button light" href="dsn-brand/dsn-brand-kit.zip" download>Download brand kit ↗</a><a class="button outline" href="#agents">AI agent reference</a></div><div class="status">v0.1 / Working reference / 6 October 2026. C1 + N01 is the working baseline, pending final selection.</div></div><div class="shell"><aside aria-label="Guideline sections"><details id="contents" open><summary>Contents / 15 sections</summary><div class="toc-links">'''+nav+'</div></details></aside><main>'+body+'''</main></div><footer><span>Dental Support Network / Original Theme C foundation</span><span>Structure reference: <a href="https://redbelly.network/brand">Redbelly brand library</a>. No Redbelly assets or brand rules used.</span></footer><div class="toast" role="status" aria-live="polite"></div><script>
const contents=document.getElementById('contents');if(matchMedia('(max-width:800px)').matches)contents.open=false;
let timer;function toast(x){document.querySelector('.toast').textContent=x;clearTimeout(timer);timer=setTimeout(()=>document.querySelector('.toast').textContent='',4000)}
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(b.dataset.copy);toast(b.classList.contains('copy-code')?'Colour copied.':'Agent brief copied.')}catch{toast('Clipboard unavailable. Select the text or download the reference file.')}}));document.querySelectorAll('[data-toast]').forEach(b=>b.addEventListener('click',()=>toast(b.dataset.toast)));
const links=[...document.querySelectorAll('aside a')];const observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting)links.forEach(a=>{const active=a.hash==='#'+e.target.id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')})},{rootMargin:'-15% 0px -70% 0px'});document.querySelectorAll('main section').forEach(s=>observer.observe(s));
</script></body></html>'''
# Inline illustrations so the local HTML does not need sibling images.
def inline_image(m):
 f=R/m.group(1); svg=f.read_text();svg=svg.replace('<svg ',f'<svg class="embedded-logo" aria-label="{m.group(2)}" ');return svg
page=re.sub(r'<img src="(dsn-brand/[^\"]+\.svg)" alt="([^\"]+)">',inline_image,page)
page=page.replace('<link rel="icon" href="dsn-brand/n01-mark-colour.svg">','<link rel="icon" href="data:image/svg+xml;base64,'+base64.b64encode((O/'n01-mark-colour.svg').read_bytes()).decode()+'">')
(R/'dental-support-network-brand.html').write_text(page)
# The single-file export links to the hosted files; the extracted kit keeps local links.
base='https://agadgil-sap.github.io/dm-themes/'
offline=page.replace('href="dsn-brand/','href="'+base+'dsn-brand/').replace('href="dental-support-network-exploration.html"','href="'+base+'dental-support-network-exploration.html"')
(O/'brand-guide-offline.html').write_text(offline)
readme='''# Dental Support Network local brand kit

Extract the ZIP, then open dental-support-network-brand.html in a browser.
No server is required.
The guide embeds its illustrations and any bundled fonts.
Keep the dsn-brand directory beside the HTML for local downloads.
The standalone HTML uses online links for additional downloads, but its reference content renders offline.

For an AI agent, provide dsn-brand/brand-rules.md, brand-spec.json, tokens.css and the relevant SVG assets.
C1 and N01 are working defaults, pending final selection.
SVG wordmarks use live text, not outlined lettering.
Install Lora and DM Sans for editable wordmarks or outline approved artwork before production.
These original DSN concepts and rules use the original Theme C foundation.
Redbelly informed section structure only; no assets or brand rules were copied.
'''
(O/'README.md').write_text(readme)
with zipfile.ZipFile(O/'dsn-brand-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(R/'dental-support-network-brand.html',arcname='dental-support-network-brand.html')
 exploration=(R/'dental-support-network-exploration.html').read_text()
 exploration=re.sub(r'<link href="https://fonts.googleapis.com/[^"]+" rel="stylesheet">', '<style>'+font_css+'</style>', exploration)
 exploration=exploration.replace('href="dental-match-inspiration.html#route-c"','href="https://agadgil-sap.github.io/dm-themes/dental-match-inspiration.html#route-c"')
 z.writestr('dental-support-network-exploration.html',exploration)
 for f in O.iterdir():
  if f.name!='dsn-brand-kit.zip':z.write(f,arcname='dsn-brand/'+f.name)
print('Built 15 guide sections, 72 SVG variants, offline HTML and ZIP kit.')
