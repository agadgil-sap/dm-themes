# Dental Match booking site

The site uses the existing L22 smile wordmark and Friendly Clarity brand tokens.
Manrope carries headings and DM Sans carries form text.
The signature visual is a symbolic tooth arch, used only in the visual and card versions.
It illustrates answer categories and is not a clinical tooth chart.

## The four variations

| URL query | Structure | Why it was chosen |
| --- | --- | --- |
| `variation=visual` | Illustrated choices, focused steps, contextual side panel | Make the first treatment question quick to scan on mobile. |
| `variation=conversation` | One question at a time, visible answer history, individual contact questions | Test a slower pace and make sensitive answers easy to reconsider. |
| `variation=planner` | Four complete sections, funding branches unfold in place, sticky summary | Let people see the scope of the enquiry before sharing their details. |
| `variation=card` | Visual enquiry, clinic outcome, appointment, card preview, booking handoff | Test a separate commitment step after qualification rather than adding friction to every lead. |

All variations share one model and one set of rules.
Switching versions preserves the current enquiry in memory so the reviewer can compare experiences.
Switching away from the card version invalidates any simulated card consent.

## Questions and branching

The chosen reference is [Dental Members Australia](https://aus.dentalmembersaustralia.com/#teeth).
The core question data is preserved across all four versions.

1. Missing or broken teeth: All, 6+, 3-5, 2 or less.
2. Super balance: $50k+, $20k-$50k, $10k-$20k, under $10k.
3. For the two lower super bands, ask interest in a payment plan.
4. If interested, ask Australian permanent residency.
5. If residency is Yes, ask whether the person works at least 25 hours per week or full-time.
6. State: WA, VIC, QLD, NSW, SA, TAS.
7. First name, last name, email and Australian phone number.
8. Preview acknowledgement, followed by review and editing.

All paths collect contact details before presenting an outcome.
Changing a parent answer removes any now-inapplicable funding answers.
Changing treatment, contact, funding or location clears the previous appointment and card consent.

## Provisional automatic routing

| Outcome | Demonstration rule | Next step |
| --- | --- | --- |
| Clinic consultation | All / 6+ teeth, $20k+ in super and a listed state | Clinic introduction, example time selection and clinic booking handoff. |
| Internal qualification | Lower super band with finance interest, or 3-5 / 2 or less teeth | Team call and callback preference. |
| Follow-up | Lower super band and no interest in finance | Enquiry acknowledgement without appointment controls. |

Incomplete or unrecognised answers never qualify for a referral.
The person does not choose their outcome.
Reviewer fixture buttons appear only in the review dialog.
Residency and work answers inform the team call; they do not grant or reject finance approval.
All clinic coverage, treatment and funding thresholds need business approval before live use.
A super balance alone does not establish eligibility for release.
The [ATO’s compassionate grounds guidance](https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/super/withdrawing-and-using-your-super/early-access-to-super/access-on-compassionate-grounds) is the authoritative starting point for that separate process.

## Card variation

The card screen follows a qualifying clinic outcome and selected example appointment.
It keeps the earlier arrangement of A$0 payment, no appointment hold and no no-show fee.
The fields are read-only, the setup is simulated, and explicit acknowledgement is required.
Changing the appointment clears the acknowledgement and simulated setup.
“Prefer not to provide a card?” opens a booking-help callback flow without pretending the person is clinically unsuitable.

The live recommendation is provider-hosted setup under the clinic’s merchant account.
[Stripe supports saving a payment method without taking a payment](https://docs.stripe.com/payments/save-and-reuse).
An authorisation hold reserves funds and expires, with online card windows commonly five to seven days depending on network and transaction type, so it is a poor default for consultations booked weeks ahead.
See [Stripe’s authorisation guidance](https://docs.stripe.com/payments/place-a-hold-on-a-payment-method).
Saving a card without an applicable fee offers no financial protection against no-shows.
If the business later chooses a fee, the amount, cancellation window, exceptions, dispute contact and consent must be agreed before integration.

## Routes and state

Hash routes work on GitHub Pages and in the portable HTML.
The query parameter selects the variation; the hash identifies the visible step.
No patient answers appear in the URL.
Examples include `?variation=conversation#/teeth` and `?variation=planner#/planner`.

Question routes are `teeth`, `superBand`, conditional funding keys, `state`, and either `contact` or individual contact fields.
Other routes are `review`, `clinic`, `team`, `followup`, `appointment`, `card`, `handoff`, `booking-help`, `callback-confirmation`, `questions` and `privacy`.
Direct links to later steps are guarded by required answers, current outcome, appointment selection and card consent.
Browser back works within the current enquiry.
Help and preview information return to the last enquiry step.
Reloading or starting again clears the enquiry.

## Live connections still required

This frontend deliberately sends no lead or booking requests.
No card provider, clinic availability or clinic booking URL has been supplied.

For live use, connect a protected enquiry endpoint, validate and recalculate routing on the server, record contact consent, and return the next permitted action.
The server must own referral decisions rather than trust the browser’s result.
It should identify the participating clinic before sharing the enquiry.
The selected clinic’s live calendar or booking link must supply real availability, consultation costs and appointment confirmation.
Calendar confirmation, not opening a booking link, establishes the booking.

Card setup should use the clinic’s provider-hosted flow and verified completion callback.
Never treat a return-page visit as proof that setup succeeded.
The provider should store the payment details; the booking service should store only the necessary provider references and consent record.
No raw card fields should be added to this frontend or lead records.
The current simulation must remain visibly labelled until those connections are tested.

## Build and verification

Edit `shell.html`, `model.js`, `view.js`, `app.js` and `style.css`.
`build.py` imports the website’s shared brand tokens and generates `booking/index.html`, `dental-match-booking.html` and `.lavish/dental-match-booking.html`.
Do not edit those outputs manually.

Run `python3 booking/build.py` and `node --test booking/tests/model.test.cjs website/tests/forms.test.cjs` from the project root.
The model tests cover all 240 valid routing combinations, branch pruning, validation, consent invalidation and future example dates.
The browser journeys exercise all four variations, all three outcomes, editing, back navigation, help, callbacks, card assistance and appointment consent.
Run a local server on port 4392 and use `chrome-devtools-axi run < booking/tests/journeys.js`.
Set `BOOKING_TEST_URL` to another entry point when needed.
