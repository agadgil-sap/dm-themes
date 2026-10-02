# Dental Match website variations

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
