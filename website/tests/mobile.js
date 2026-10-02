// Run through chrome-devtools-axi run after emulating a 390px or 320px mobile viewport.
const assert = (condition, message) => { if (!condition) throw new Error(message); };
for (const variation of ['welcome', 'guided', 'considered']) {
  await page.open('http://127.0.0.1:4391/index.html?variation=' + variation);
  assert(await page.eval(() => document.documentElement.scrollWidth <= innerWidth), variation + ': home overflow');
  await page.click('.menu-toggle');
  assert(await page.eval(() => document.querySelector('.menu-toggle').getAttribute('aria-expanded') === 'true'), 'Menu opens');
  await page.press('Escape');
  assert(await page.eval(() => document.activeElement.classList.contains('menu-toggle') && document.querySelector('.menu-toggle').getAttribute('aria-expanded') === 'false'), 'Escape closes menu and restores focus');
  await page.click('.menu-toggle');
  await page.click('.site-nav a[data-route="/implants"]');
  await page.wait('main h1');
  assert(await page.eval(() => DentalMatch.state.route === '/implants'), 'Mobile navigation works');
  for (const route of ['/how-it-works', '/costs', '/about', '/questions', '/privacy', '/contact', '/match']) {
    await page.eval('location.hash = ' + JSON.stringify(route));
    await page.wait('main h1');
    assert(await page.eval(() => DentalMatch.state.route) === route, variation + ': route opens');
    assert(await page.eval(() => document.documentElement.scrollWidth <= innerWidth), variation + ': overflow on ' + route);
  }
  await page.click('input[name=treatment][value=unsure]');
  await page.click('#match-form button[type=submit]');
  await page.wait('#field-postcode');
  await page.fill('#field-postcode', '0800');
  await page.click('#match-form button[type=submit]');
  await page.wait('#field-name');
  await page.fill('#field-name', 'Alex Sample');
  await page.fill('#field-phone', '0400 123 456');
  await page.click('#match-form button[type=submit]');
  await page.wait('input[name=consent]');
  assert(await page.eval(() => document.documentElement.scrollWidth <= innerWidth), variation + ': review overflow');
  await page.click('input[name=consent]');
  await page.click('#match-form button[type=submit]');
  await page.wait('.confirmation-card');
  assert(await page.eval(() => document.documentElement.scrollWidth <= innerWidth), variation + ': confirmation overflow');
}
console.log('Mobile menu, routes and enquiry steps passed for all three variations.');
