# Dental Match website explorations

The agreed identity is L22, the stacked wordmark with a smile under “match”, and B, Friendly Clarity.
The audience is Australian adults exploring dental implants, often with anxiety, cost concerns or a long gap in dental care.
The primary job is to help someone take a manageable first step towards a conversation with a participating clinic.
This phase demonstrates navigation, form validation, review and confirmation without sending an enquiry.

## Shared foundation

- Plum: `#463276`.
- Lilac: `#C7B7EC`.
- Warm gold: `#F5D894`.
- Ink: `#302D3C`.
- Muted text: `#665F74`.
- Paper: `#FAF8FD`.
- Display and identity: Manrope.
- Body and controls: DM Sans.

The L22 lettering remains consistent in all three versions.
Each version shares accessible navigation, buttons, choice cards, form fields, accordions, callouts, step lists, review rows and confirmation components.
The variants preserve the current page and in-memory form answers when switched.
No personal details are saved in browser storage or sent to a server.

## 1. Clear & welcoming

Use a light lilac canvas, generous rounded shapes and a strong but calm Manrope headline.
The signature is a patient concern selector that changes the explanation before asking for contact details.

```text
Headline and first step | What is on your mind?
Service explanation    | A small, useful response
Three matching steps
Implant choices | Practical support
Questions | Final invitation
```

## 2. Your guided first step

Use a plum opening panel, lilac section transitions and compact, structured components.
The signature is a treatment choice in the hero that carries directly into the matching flow.

```text
Plum headline | First question of the matching flow
              | Treatment choices + continue
Matching sequence across the page
Implant overview | Cost questions
Support by concern | FAQs | Invitation
```

## 3. Space to decide

Use white, plum rules, restrained gold accents and quieter components with less rounding.
The signature is a question-led reading panel beside a spacious headline.

```text
Spacious headline | The questions you can start with
                  | Open a question to read
Wide service explanation
Editorial implant and cost sections
Detailed process | FAQs | Invitation
```

## Plan critique before implementation

Three recoloured landing pages would make it hard to judge the patient experience.
The layouts therefore differ in how they introduce the first decision: concern, treatment, or questions.
All retain the same identity and core information so the differences stay comparable.
Generic trust statistics, fabricated patient testimonials and invented clinic credentials are excluded.
The matching role is explained separately from a dentist’s clinical assessment.
The website preview notice is explicit, especially before contact fields and on confirmation.
Clinical overview wording is checked against [healthdirect’s dental implant information](https://www.healthdirect.gov.au/dental-implant).

## Critique after implementation

Clear & welcoming is the recommended starting point because it directly addresses the audience’s concern and delayed-care barriers.
The guided version gives a useful first question to patients ready to act, while Space to decide gives more room to read before enquiring.
This recommendation is a design judgement rather than a measured conversion result.
The screenshot comparison and complete critique are in [.lavish/dental-match-website-review.html](../.lavish/dental-match-website-review.html).

Real-browser review led to a compact guided choice grid, correct treatment carryover, an optional concern step after the hero, and a fresh form after completion.
The delayed-care copy now acknowledges circumstances without blame.
Keyboard checks corrected the skip link, mobile Escape handling and style state during browser history navigation.

Desktop checks passed the full enquiry and question-form journeys for all three variations.
Mobile checks passed all pages and enquiry steps at 320px and 390px without horizontal overflow.
Nine focused tests cover validation, explicit demo acknowledgement, fresh state and escaping.
The demo remains disconnected from any lead destination, with no storage of form answers in the browser.
