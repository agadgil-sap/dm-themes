const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const context = vm.createContext({ window: {} });
for (const name of ['data.js', 'components.js', 'forms.js']) {
  vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'js', name), 'utf8'), context);
}
const DM = context.window.DentalMatch;

test('uncertainty is a valid treatment starting point', () => {
  const values = DM.newMatch();
  assert.ok(DM.validateMatch(values, 0).treatment);
  values.treatment = 'unsure';
  assert.equal(Object.keys(DM.validateMatch(values, 0)).length, 0);
});
test('postcodes preserve leading zeroes and reject incomplete formats', () => {
  const values = DM.newMatch();
  for (const code of ['0800', '0200', '3000', '6000']) {
    values.postcode = code;
    assert.equal(Object.keys(DM.validateMatch(values, 1)).length, 0);
  }
  for (const code of ['', '800', '30ab', '0000', '30000']) {
    values.postcode = code;
    assert.ok(DM.validateMatch(values, 1).postcode);
  }
});
test('email contact does not require a phone number', () => {
  const values = { ...DM.newMatch(), name: 'Alex Sample', preference: 'email', email: 'alex+preview@example.com' };
  assert.equal(Object.keys(DM.validateMatch(values, 2)).length, 0);
  values.email = 'not-an-email';
  assert.ok(DM.validateMatch(values, 2).email);
});
test('phone contact accepts readable Australian formats without requiring email', () => {
  const values = { ...DM.newMatch(), name: 'Alex Sample' };
  for (const number of ['0412 345 678', '(03) 9123 4567', '+61 412 345 678']) {
    values.phone = number;
    assert.equal(Object.keys(DM.validateMatch(values, 2)).length, 0);
  }
  values.phone = '123';
  assert.ok(DM.validateMatch(values, 2).phone);
});
test('optional contact fields are checked when provided', () => {
  const values = { ...DM.newMatch(), name: 'Alex Sample', preference: 'email', email: 'alex@example.com', phone: 'wrong' };
  assert.ok(DM.validateMatch(values, 2).phone);
});
test('demo acknowledgement is explicit rather than preselected', () => {
  const values = DM.newMatch();
  assert.equal(values.consent, false);
  assert.ok(DM.validateMatch(values, 3).consent);
  values.consent = true;
  assert.equal(Object.keys(DM.validateMatch(values, 3)).length, 0);
});
test('a fresh enquiry has no personal details or shared concern array', () => {
  const previous = DM.newMatch();
  previous.name = 'Alex';
  previous.concerns.push('anxiety');
  const fresh = DM.newMatch();
  assert.equal(fresh.name, '');
  assert.equal(fresh.concerns.length, 0);
});
test('user-entered text is escaped before inclusion in review markup', () => {
  const markup = DM.reviewRow('Name', '<img src=x onerror=alert(1)>');
  assert.ok(markup.includes('&lt;img'));
  assert.equal(markup.includes('<img'), false);
});
test('question forms require a name, usable email and a question', () => {
  assert.equal(Object.keys(DM.validateContact({ name: '', email: '', message: '' })).length, 3);
  assert.equal(Object.keys(DM.validateContact({ name: 'Alex', email: 'alex@example.com', message: 'How does the first appointment work?' })).length, 0);
});
