# Visual review and corrections

Reviewed the published website first, then verified the corrections against the local build.
The agreed L22 identity and Friendly Clarity palette are retained across all three variations.

## Reproduced issues

- The considered theme gave white cards `27px 0px` padding, leaving icons and text against the sides.
- The guided hero combined a 28px fieldset margin and a 22px button margin into a 50px gap.
- The FAQ help callout touched the accordion because the gap was 0px.
- Standalone callouts added an unnecessary 33px bottom margin inside an already padded section.
- The fallback page placed two buttons beside each other with a 0px gap.
- Mobile review Edit buttons began in the second grid row and created an extra empty row.
- Several mobile descriptions were reduced to 10px or 11px, and the form actions used small text in narrow buttons.

## Corrections

Cards and panels now share responsive padding tokens, with room around both text and icons.
The considered theme retains its restrained rules and small corners while inheriting the card padding.
Card actions align at the bottom when neighbouring descriptions wrap differently.
The guided hero uses a single 24px gap before its action.
The FAQ callout has 32px separation on desktop and 24px on phones.
Callout spacing avoids redundant margins, and fallback buttons use a reusable action row with a 16px gap.
Concern responses size to their content instead of reserving a large blank area.
Mobile descriptions and review values are larger, and form actions use the available width.
Mobile review Edit buttons align centrally with their label and value.
On phones, footer links, Edit buttons and preview toggles have touch targets at least 44px high.
At the narrowest width, guided choices use one column so their descriptions stay readable.

## Verification

Page captures covered 1440px desktop, 820px tablet and 390px phone layouts.
The primary pages, privacy information and fallback route were checked, including the three home-page directions and theme-specific inner pages.
Each matching form was exercised through errors, location, contact details, review and confirmation in all three themes at 1440px, 820px, 390px and 320px.
These captures had no horizontal overflow.
Additional geometry checks covered 27 page and theme combinations at each of the four widths, verifying no horizontal overflow or missing card side padding.
The mobile journey checks also verify review action alignment and usable form action heights.
The complete desktop journeys and the nine focused form validation checks pass.

The [visual critique](../.lavish/dental-match-website-review.html) includes current home-page screenshots and before-and-after examples of the FAQ spacing and card padding corrections.
