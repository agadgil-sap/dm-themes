// Run through chrome-devtools-axi run with a real browser session.
const base = 'http://127.0.0.1:4391/index.html';
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const result = [];
for (const variation of ['welcome', 'guided', 'considered']) {
  await page.open(base + '?variation=' + variation);
  for (const route of ['/implants', '/how-it-works', '/costs', '/about', '/questions', '/privacy', '/contact', '/']) {
    await page.click('a[data-route="' + route + '"]');
    await page.wait('main h1');
    const actual = await page.eval(() => window.DentalMatch.state.route);
    assert(actual === route, variation + ': navigation to ' + route);
    assert(await page.eval(() => document.documentElement.scrollWidth <= innerWidth), variation + ': page overflow ' + route);
  }
  if (variation === 'welcome') {
    await page.click('button[data-concern="cost"]');
    assert(await page.eval(() => document.getElementById('concern-response').textContent.includes('payment')), 'Concern response changes');
  }
  if (variation === 'guided') {
    await page.click('#quick-start input[value="single"]');
    await page.click('#quick-start button[type="submit"]');
    await page.wait('.selected-starting-point');
    assert(await page.eval(() => document.querySelectorAll('input[name="concerns"]').length === 4), 'Guided start includes optional concerns');
    await page.click('button[data-change-treatment]');
    assert(await page.eval(() => document.querySelector('input[name="treatment"]:checked').value === 'single'), 'Change treatment preserves hero choice');
    await page.click('a[data-route="/"]');
    await page.wait('#quick-start');
    await page.click('.treatment-grid a[data-treatment="full"]');
    await page.wait('#match-form');
    assert(await page.eval(() => document.querySelector('input[name="treatment"]:checked').value === 'full'), 'Treatment tile overrides earlier quick-start choice');
  } else {
    await page.click('.site-nav a[data-route="/match"]');
    await page.wait('#match-form');
    await page.click('#match-form button[type="submit"]');
    await page.wait('.error-summary');
    assert(await page.eval(() => document.activeElement.classList.contains('error-summary')), 'Error summary receives focus');
    await page.click('input[name="treatment"][value="unsure"]');
  }
  await page.click('input[name="concerns"][value="anxiety"]');
  await page.click('#match-form button[type="submit"]');
  await page.wait('#field-postcode');
  await page.fill('#field-postcode', '800');
  await page.click('#match-form button[type="submit"]');
  await page.wait('.error-summary');
  await page.fill('#field-postcode', '0800');
  await page.click('button[data-variation="considered"]');
  assert(await page.eval(() => document.getElementById('field-postcode').value === '0800'), 'Variation switch retains form answers');
  await page.click('button[data-variation="' + variation + '"]');
  await page.click('#match-form button[type="submit"]');
  await page.wait('#field-name');
  await page.fill('#field-name', 'Alex Sample');
  await page.fill('#field-preference', 'email');
  await page.fill('#field-email', 'alex@example.com');
  await page.click('#match-form button[type="submit"]');
  await page.wait('input[name="consent"]');
  assert(await page.eval(() => document.querySelector('.review-list').textContent.includes('0800')), 'Review preserves leading zero');
  await page.click('button[data-edit-step="1"]');
  await page.wait('#field-postcode');
  await page.fill('#field-postcode', '3000');
  await page.click('#match-form button[type="submit"]');
  await page.wait('#field-name');
  assert(await page.eval(() => document.getElementById('field-email').value === 'alex@example.com'), 'Editing earlier step preserves contact details');
  await page.click('#match-form button[type="submit"]');
  await page.wait('input[name="consent"]');
  await page.click('#match-form button[type="submit"]');
  await page.wait('.error-summary');
  await page.click('input[name="consent"]');
  await page.click('#match-form button[type="submit"]');
  await page.wait('.confirmation-card');
  assert(await page.eval(() => document.querySelector('.confirmation-card').textContent.includes('No enquiry has been sent')), 'Confirmation accurately describes demo');
  assert(await page.eval(() => window.DentalMatch.state.match.email === ''), 'Completed enquiry clears contact fields');
  await page.click('.site-nav a[data-route="/match"]');
  await page.wait('#match-form');
  assert(await page.eval(() => document.querySelector('.form-heading .eyebrow').textContent === 'Step 1 of 4'), 'New enquiry starts at step one after completion');
  await page.click('a[data-route="/contact"]');
  await page.wait('#contact-form');
  await page.click('#contact-form button[type="submit"]');
  await page.wait('.error-summary');
  await page.fill('#field-name', 'Alex Sample');
  await page.fill('#field-email', 'alex@example.com');
  await page.fill('#field-message', 'How does the first appointment work?');
  await page.click('#contact-form button[type="submit"]');
  await page.wait('.confirmation-card');
  assert(await page.eval(() => document.querySelector('h1').textContent.includes('question flow')), 'Question form completes');
  assert(await page.eval(() => localStorage.length === 0 && sessionStorage.length === 0), 'No personal details stored in browser storage');
  result.push({ variation, navigation: 'passed', enquiry: 'passed', questionForm: 'passed', themeSwitch: 'passed', submissionReset: 'passed' });
}
await page.open(base + '?variation=welcome#/costs');
await page.wait('[data-variation=welcome] .nav-current[data-route="/costs"]');
await page.eval(() => document.querySelector('.skip-link').focus());
await page.press('Enter');
assert(await page.eval(() => DentalMatch.state.route === '/costs' && document.activeElement.id === 'page-content'), 'Skip link keeps current route');
await page.click('a[data-route="/implants"]');
await page.wait('.nav-current[data-route="/implants"]');
await page.click('button[data-variation="guided"]');
await page.click('a[data-route="/about"]');
await page.wait('.nav-current[data-route="/about"]');
await page.back();
await page.wait('[data-variation=guided] .nav-current[data-route="/implants"]');
await page.back();
await page.wait('[data-variation=welcome] .nav-current[data-route="/costs"]');
assert(await page.eval(() => DentalMatch.state.route === '/costs' && DentalMatch.state.variation === 'welcome' && document.documentElement.dataset.variation === 'welcome'), 'Browser back restores theme and route');
console.log(JSON.stringify(result));
