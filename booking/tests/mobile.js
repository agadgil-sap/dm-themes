// Run at each desired viewport using chrome-devtools-axi emulate first.
const base = process.env.BOOKING_TEST_URL || 'http://127.0.0.1:4392/booking/index.html';
let checks = 0;
async function check(label) {
  const size = await page.eval(() => ({ width: innerWidth, content: document.documentElement.scrollWidth, route: document.querySelector('main').dataset.route }));
  if (size.content > size.width) throw new Error(`${label}: horizontal overflow ${JSON.stringify(size)}`);
  checks++;
}
async function fixture(id) {
  await page.click('[data-review]'); await check('Review notes');
  await page.click(`[data-fixture="${id}"]`); await check('Review enquiry');
  await page.click('main form button[type="submit"]'); await check('Outcome ' + id);
}
for (const variant of ['visual', 'conversation', 'planner', 'card']) {
  await page.open(base + '?variation=' + variant);
  await check(variant + ' opening');
  for (const outcome of ['clinic', 'team', 'followup']) {
    await fixture(outcome);
    if (outcome === 'clinic') {
      await page.click('[data-go="appointment"]'); await check('Appointment');
      await page.click('main .slot:first-of-type'); await page.click('main form button[type="submit"]');
      await check(variant === 'card' ? 'Card' : 'Handoff');
    }
  }
}
await page.open(base + '?variation=planner');
await page.click('main label:has(input[name="superBand"][value="Under $10k in super"])');
await page.click('main label:has(input[name="finance"][value="Yes"])');
await page.click('main label:has(input[name="residency"][value="Yes"])');
await check('Planner with all funding questions');
console.log(`PASS: ${checks} overflow checks at ${await page.eval(() => innerWidth)}px.`);
