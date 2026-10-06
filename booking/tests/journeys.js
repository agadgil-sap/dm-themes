// Run with chrome-devtools-axi run < booking/tests/journeys.js.
const base = process.env.BOOKING_TEST_URL || 'http://127.0.0.1:4392/booking/index.html';
let checks = 0;
async function assert(condition, message) {
  if (!condition) throw new Error(message);
  checks++;
}
const route = () => page.eval(() => document.querySelector('main').dataset.route);
const submit = () => page.click('main form button[type="submit"]');
const answer = (key, value) => page.click(`main label:has(input[name="${key}"][value="${value}"])`);
async function fixture(id) {
  await page.click('[data-review]');
  await page.click(`[data-fixture="${id}"]`);
  await assert(await route() === 'review', `Fixture ${id} should open at review`);
}
async function open(variant = 'visual', hash = 'teeth') {
  await page.open(base + '?variation=' + variant + '#/' + hash);
}

await open('visual', 'card');
await assert(await route() === 'teeth', 'Deep links cannot bypass missing answers');
await submit();
await assert(await page.eval(() => !!document.querySelector('.error-summary')), 'Empty first question is blocked');
await answer('teeth', 'All'); await submit();
await answer('superBand', 'Under $10k in super'); await submit();
await assert(await route() === 'finance', 'Lower super opens finance question');
await answer('finance', 'Yes'); await submit();
await answer('residency', 'Yes'); await submit();
await answer('work', 'No'); await submit();
await answer('state', 'Victoria (VIC)'); await submit();
await page.fill('[name="firstName"]', 'Alex'); await page.fill('[name="lastName"]', 'Example');
await page.fill('[name="email"]', 'invalid'); await page.fill('[name="phone"]', '123');
await submit();
await assert(await page.eval(() => document.querySelectorAll('[aria-invalid="true"]').length >= 3), 'Contact errors identify invalid fields');
await page.fill('[name="email"]', 'alex@example.com'); await page.fill('[name="phone"]', '0400 000 000');
await page.click('label:has([name="consent"])'); await submit();
await assert(await route() === 'review', 'Complete enquiry reaches review');
await page.click('[data-edit="superBand"]');
await answer('superBand', '$50k+ in super'); await submit();
await assert(await route() === 'review', 'Edit returns to review when remaining answers are valid');
await assert(!(await page.eval(() => document.querySelector('main').innerText)).includes('Payment plan'), 'Hidden funding answers removed from review');
await submit();
await assert(await route() === 'clinic', 'Funding edit recalculates the outcome');
await page.back(); await page.wait('main[data-route="review"]');
await assert(await route() === 'review', 'Browser back returns to review');

for (const variant of ['visual', 'conversation', 'planner', 'card']) {
  for (const outcome of ['clinic', 'team', 'followup']) {
    await open(variant, variant === 'planner' ? 'planner' : 'teeth');
    await fixture(outcome); await submit();
    await assert(await route() === outcome, `${variant} routes to ${outcome}`);
    if (outcome === 'clinic') {
      await page.click('[data-go="appointment"]'); await submit();
      await assert(await route() === 'appointment', 'An appointment must be selected');
      await page.click('main .slot:first-of-type'); await submit();
      if (variant === 'card') {
        await assert(await route() === 'card', 'Fourth version adds card after appointment');
        await assert(await page.eval(() => !document.querySelector('[name="cardNumber"], [name="cvc"]')), 'Preview never accepts raw card data');
        await submit();
        await assert(await route() === 'card', 'Card stage cannot be bypassed');
        await page.click('label:has([name="policyConsent"])');
        await page.click('[data-simulate-card]');
        await page.click('[data-go="appointment"]');
        await page.click('main .slot:nth-of-type(2)'); await submit();
        await assert(await page.eval(() => !document.querySelector('[name="policyConsent"]').checked), 'Changing appointment invalidates consent');
        await page.click('label:has([name="policyConsent"])'); await page.click('[data-simulate-card]'); await submit();
      }
      await assert(await route() === 'handoff', 'Clinic journey reaches booking handoff');
      await page.click('[data-demo-handoff]');
      await assert((await page.eval(() => document.getElementById('handoff-status').textContent)).includes('No appointment is booked'), 'Handoff does not claim a booking');
    }
    if (outcome === 'team') {
      await submit();
      await assert(await route() === 'team', 'Callback needs a preference');
      await answer('callback', 'No preference'); await submit();
      await assert(await route() === 'callback-confirmation', 'Callback preference reaches confirmation');
    }
    if (outcome === 'followup') {
      await assert(await page.eval(() => !document.querySelector('[data-go="appointment"],#card-form')), 'Follow-up offers no appointment or card');
    }
  }
}

await open('planner', 'planner');
await answer('superBand', 'Under $10k in super'); await answer('finance', 'Yes'); await answer('residency', 'Yes'); await answer('work', 'Yes');
await answer('finance', 'No');
await assert(await page.eval(() => !document.querySelector('[name="residency"],[name="work"]')), 'Planner removes inapplicable branches');
await answer('superBand', '$50k+ in super');
await assert(await page.eval(() => !document.querySelector('[name="finance"]')), 'Planner clears funding branch at higher super');

await open('conversation'); await answer('teeth', '6+'); await submit();
await assert((await page.eval(() => document.querySelector('.answer-history').innerText)).includes('6+'), 'Conversation displays previous answer');
await page.click('.answer-history [data-edit="teeth"]');
await assert(await route() === 'teeth', 'Conversation history answer is editable');
await fixture('clinic');
await page.click('[data-edit="email"]');
await assert(await route() === 'email', 'Review email edit opens the email question');
await page.fill('[name="email"]', 'edited@example.com'); await submit();
await assert(await route() === 'review', 'Editing a contact field returns to review');
await page.click('[data-edit="lastName"]');
await assert(await route() === 'lastName', 'Review last name edit opens its question');

await open('card'); await fixture('clinic'); await submit(); await page.click('[data-go="appointment"]'); await page.click('main .slot:first-of-type'); await submit();
await page.click('[data-go="booking-help"]');
await answer('callback', 'Afternoon · 12 pm-5 pm'); await submit();
await assert(await route() === 'callback-confirmation', 'Card assistance supports a callback');

await open('visual');
await answer('teeth', '6+'); await submit(); await page.click('a[href="#/questions"]');
await page.click('main a[href="#/resume"]');
await assert(await route() === 'superBand', 'Help page returns to the current question');
await page.open(base + '?variation=visual#/handoff');
await page.eval(() => location.reload()); await page.wait('main[data-route="teeth"]');
await assert(await route() === 'teeth', 'Reload clears details and guards outcome routes');
console.log(`PASS: ${checks} browser checks across all four variations and three outcomes.`);
