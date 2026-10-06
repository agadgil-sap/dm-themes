# Dental Match & Dental Support Network

Published brand explorations, website prototypes and brand-reference assets for the patient-facing Dental Match brand and the B2B Dental Support Network brand.

## Published pages

| Page | Link |
| --- | --- |
| Dental Match website, with three variations | [Open website](https://agadgil-sap.github.io/dm-themes/) |
| Dental Match website critique and visual review | [Open review](https://agadgil-sap.github.io/dm-themes/dental-match-website-review.html) |
| Dental Match original six themes, including Theme C | [Open theme board](https://agadgil-sap.github.io/dm-themes/dental-match-inspiration.html) |
| Dental Match logo exploration, page 1 | [Open first 24 logos](https://agadgil-sap.github.io/dm-themes/dental-match-logo-exploration.html) |
| Dental Match logo exploration, page 2 | [Open next 24 logos](https://agadgil-sap.github.io/dm-themes/dental-match-logo-exploration-page-2.html) |
| Dental Support Network website and logo exploration | [Open three themes and twelve logos](https://agadgil-sap.github.io/dm-themes/dental-support-network-exploration.html) |
| Dental Support Network brand guidelines | [Open brand guide](https://agadgil-sap.github.io/dm-themes/dental-support-network-brand.html) |
| Dental Support Network downloadable brand kit | [Download ZIP](https://agadgil-sap.github.io/dm-themes/dsn-brand/dsn-brand-kit.zip) |

## Dental Support Network

Dental Support Network is a B2B brand for Australian clinic owners and practice managers.
Its core message is: **We find, qualify and book implant patients for clinics.**
The exploration develops original Theme C, Quiet confidence, into three website treatments and twelve logo concepts.
**C1 / Established partner + N01 / The connection** is the working baseline, pending final selection.
The enquiry flow is an interactive demo and sends no enquiries.

The [brand guidelines](https://agadgil-sap.github.io/dm-themes/dental-support-network-brand.html) cover fifteen sections, including identity, colour, typography, spacing, reusable components, forms, messaging, imagery, accessibility and AI agent instructions.
Redbelly was a reference for the guide's structure only; no Redbelly assets or brand rules were copied.

### Downloads and AI references

- [Complete brand kit](https://agadgil-sap.github.io/dm-themes/dsn-brand/dsn-brand-kit.zip): local HTML guide, exploration, 72 SVG variants, font licences and reference files.
- [Standalone offline HTML guide](https://agadgil-sap.github.io/dm-themes/dsn-brand/brand-guide-offline.html): embedded fonts and illustrations, with online links for additional downloads.
- [Brand rules / Markdown](https://agadgil-sap.github.io/dm-themes/dsn-brand/brand-rules.md).
- [Brand specification / JSON](https://agadgil-sap.github.io/dm-themes/dsn-brand/brand-spec.json).
- [Design tokens / CSS](https://agadgil-sap.github.io/dm-themes/dsn-brand/tokens.css).
- [Reusable AI agent brief / text](https://agadgil-sap.github.io/dm-themes/dsn-brand/agent-prompt.txt).

Extract the ZIP and open `dental-support-network-brand.html` in a browser; no server is required.
Keep the `dsn-brand` folder beside the guide for local downloads.
For AI-assisted work, provide the Markdown rules, JSON specification, CSS tokens and relevant SVG assets.
SVG wordmarks use editable live text; install Lora and DM Sans or outline the approved lettering before production use.

### Dental Support Network sources

Edit [.lavish/dental-support-network.html](.lavish/dental-support-network.html) for the exploration.
Edit [scripts/build-dsn-brand.py](scripts/build-dsn-brand.py) and [scripts/dsn-brand-guide.css](scripts/dsn-brand-guide.css) for the brand guide and downloadable kit.
Export the exploration first, then rebuild the guide and ZIP so the kit includes the latest exploration.

```sh
lavish-axi export .lavish/dental-support-network.html --out dental-support-network-exploration.html
python3 scripts/build-dsn-brand.py
```

The published guide, reference files, SVGs and ZIP are generated outputs.
Do not edit them manually.

## Dental Match website variations

The selected identity is **L22, the smile wordmark, with B, Friendly Clarity**.
The current phase is three complete website variations for Australian patients exploring dental implants.

[Open the live website](https://agadgil-sap.github.io/dm-themes/) and use the three-way toggle at the top to compare them.
The existing [refinements URL](https://agadgil-sap.github.io/dm-themes/dental-match-ab-refinements.html) also opens the new website.
The old A+B, B logo and combination controls have been removed from this entry point.

- [1. Clear & welcoming](https://agadgil-sap.github.io/dm-themes/?variation=welcome) leads with patient concerns and a reassuring response.
- [2. Your guided first step](https://agadgil-sap.github.io/dm-themes/?variation=guided) starts the matching journey with a treatment choice in the hero.
- [3. Space to decide](https://agadgil-sap.github.io/dm-themes/?variation=considered) gives patients a quieter, question-led introduction.

Each version includes implant information, how matching works, cost questions, about, FAQs, a matching enquiry, a question form and confirmation pages.
Forms are **interactive demos** and send no enquiries or bookings.
Use sample details.
Form answers stay in page memory, survive a variation switch and are cleared when the demo is completed or the page is reloaded.
No answers are written to browser storage.

[Read the visual critique](https://agadgil-sap.github.io/dm-themes/dental-match-website-review.html) for the recommendation, tradeoffs and verification evidence.
The design direction and component plan are recorded in [website/DESIGN.md](website/DESIGN.md).
The [second visual review](https://agadgil-sap.github.io/dm-themes/dental-match-website-review.html#visual-polish) includes before-and-after examples of card padding and FAQ spacing.
The issues, corrections and verification scope are recorded in [website/VISUAL-REVIEW.md](website/VISUAL-REVIEW.md).

## Website sources and verification

Edit the shared sources in [website](website), then regenerate the portable HTML.
The shared components cover navigation, buttons, cards, accordions, choices, fields, progress, validation, review and confirmation.
The three variations use the same identity and content with distinct layouts and opening interactions.
Hash routes support direct links on GitHub Pages without a server-side router.

```sh
python3 website/build.py
node --test website/tests/forms.test.cjs
```

The build generates `index.html`, `dental-match-website.html`, `dental-match-ab-refinements.html` and the Lavish preview.
Do not edit these outputs manually.
The real-browser journeys in [website/tests/journeys.js](website/tests/journeys.js) run through `chrome-devtools-axi run` against a local server on port 4391.

The editable critique is [.lavish/dental-match-website-review.html](.lavish/dental-match-website-review.html).
Export it after changes:

```sh
lavish-axi export .lavish/dental-match-website-review.html --out dental-match-website-review.html
```

## Earlier brand explorations

Six visual directions for Dental Match, an Australian clinic matching and patient support business focused on dental implants and major dental treatment.
The concepts explore a reassuring, practical identity for patients facing fear, cost concerns, family responsibilities, shame, inconvenience and uncertainty about their options.

## View the board

The logo exploration now has 48 concepts across two pages, with navigation at the top and bottom of each page.
[View page 2 online](https://agadgil-sap.github.io/dm-themes/dental-match-logo-exploration-page-2.html) for three A arch studies, three B smile studies and eighteen further concepts in six different colour and style themes.
The original A and B symbols are included as reference points in those first six.
Open [dental-match-logo-exploration-page-2.html](dental-match-logo-exploration-page-2.html) for the portable version.

![Twenty-four further Dental Match logo concepts](.lavish/assets/dental-match-page-2-logos.png)

[View page 1 online](https://agadgil-sap.github.io/dm-themes/dental-match-logo-exploration.html) for the original 24 concepts across people, connection, letterforms, pathways, dental motifs, conversation, renewal and wordmarks.
Open [dental-match-logo-exploration.html](dental-match-logo-exploration.html) for the portable version.
Both pages support filters, larger previews, palette comparisons and SVG downloads.
The published pages save a combined shortlist and separate notes for each page in the browser.
Lavish review tabs hold their own selections; queue or copy each shortlist before closing the tab.

![Twenty-four broad Dental Match logo concepts](.lavish/assets/dental-match-24-logos.png)

The earlier refinement round developed the selected A and B directions, with three variations of each and twelve logo sketches for B.
Its archived source remains in [.lavish/dental-match-ab-refinements.html](.lavish/dental-match-ab-refinements.html).

![Twelve smile and people logo studies for Dental Match](.lavish/assets/dental-match-b-logos.png)

Download [dental-match-inspiration.html](dental-match-inspiration.html) and open it in a browser.
The portable board includes its reference screenshots, with fonts and styling loaded over the internet.

![Six Dental Match visual directions](.lavish/assets/brand-directions-six.png)

## The six directions

- **A: Warm reassurance** - forest green, sage and peach with rounded typography.
- **B: Friendly clarity** - plum and lilac with bold, modern typography.
- **C: Quiet confidence** - navy, mist blue and brass with refined serif typography.
- **D: Grounded care** - cocoa, ochre and olive with a sturdy, familiar serif.
- **E: Positive momentum** - coral and apricot with energetic condensed typography.
- **F: Clear guidance** - white, slate and teal with structured, practical typography.

Each direction includes a palette, type pairing, exploratory logo sketch, draft messaging and photography guidance.
A and B were the favourites in the earlier round; the final selection is B with L22.
The second round explores a smile that also suggests two people meeting or matching.

## Source and exports

The editable source is [.lavish/dental-match-inspiration.html](.lavish/dental-match-inspiration.html).
Its local assets are in [.lavish/assets](.lavish/assets).
The root HTML file is a generated portable export; regenerate it from the source after edits.

```sh
lavish-axi export .lavish/dental-match-inspiration.html --out dental-match-inspiration.html
python3 .lavish/assets/logo-exploration/build.py
python3 .lavish/assets/logo-exploration/build.py --page 2
lavish-axi export .lavish/dental-match-logo-exploration.html --out dental-match-logo-exploration.html
lavish-axi export .lavish/dental-match-logo-exploration-page-2.html --out dental-match-logo-exploration-page-2.html
```

The archived second-round source is [.lavish/dental-match-ab-refinements.html](.lavish/dental-match-ab-refinements.html).
Do not export it over the current website alias.
The twelve draft B symbols are available as editable SVGs in [.lavish/assets/logos-b](.lavish/assets/logos-b).

For the logo boards, edit the authored page 1 concepts in [.lavish/assets/logo-exploration/concepts.json](.lavish/assets/logo-exploration/concepts.json), page 2 concepts in [.lavish/assets/logo-exploration/concepts-page-2.json](.lavish/assets/logo-exploration/concepts-page-2.json), or their renderer in [.lavish/assets/logo-exploration/build.py](.lavish/assets/logo-exploration/build.py), then run the build and export commands above.
The HTML boards, SVGs and ZIP bundles are generated outputs.
The draft SVGs are in [.lavish/assets/logo-exploration/svg](.lavish/assets/logo-exploration/svg) and [.lavish/assets/logo-exploration/svg-page-2](.lavish/assets/logo-exploration/svg-page-2).
Each board also provides a download of its 24 SVG sketches.

## Visual references

The board includes reference screenshots from [Tend](https://www.hellotend.com/site/home), [HotDoc](https://english.hotdoc.com.au/) and [Dental 99](https://dental99.com.au/), captured on 2 October 2026.
The Dental Match directions are original explorations.
