const { test } = require('node:test');
const assert = require('node:assert/strict');
const M = require('../model.js');

test('incomplete and unrecognised answers never qualify for a referral', () => {
  assert.equal(M.route(M.empty()), null);
  const v = M.fixture('clinic');
  for (const key of ['teeth', 'superBand', 'state']) {
    assert.equal(M.route({ ...v, [key]: 'unexpected' }), null);
  }
  assert.equal(M.route({ ...M.fixture('team'), work: '' }), null);
});

test('reference funding branches are conditional and stale answers are removed', () => {
  const v = M.fixture('team');
  assert.deepEqual(M.fundingKeys(v), ['finance', 'residency', 'work']);
  M.setAnswer(v, 'residency', 'No');
  assert.equal(v.work, '');
  assert.deepEqual(M.fundingKeys(v), ['finance', 'residency']);
  M.setAnswer(v, 'finance', 'No');
  assert.equal(v.residency, '');
  assert.deepEqual(M.fundingKeys(v), ['finance']);
  M.setAnswer(v, 'superBand', '$50k+ in super');
  assert.equal(v.finance, '');
  assert.deepEqual(M.fundingKeys(v), []);
});

test('all valid combinations route according to the proposed commercial rules', () => {
  let checked = 0;
  for (const teeth of M.groups.teeth) for (const superBand of M.groups.superBand) for (const state of M.groups.state) {
    const base = { ...M.fixture('clinic'), teeth, superBand, state };
    const finances = M.lowSuper(base) ? ['Yes', 'No'] : [''];
    for (const finance of finances) {
      for (const residency of finance === 'Yes' ? ['Yes', 'No'] : ['']) {
        for (const work of residency === 'Yes' ? ['Yes', 'No'] : ['']) {
          const v = { ...base, finance, residency, work };
          const expected = M.lowSuper(v) && finance === 'No' ? 'followup' : M.lowSuper(v) || ['3-5', '2 or less'].includes(teeth) ? 'team' : 'clinic';
          assert.equal(M.route(v).id, expected);
          checked++;
        }
      }
    }
  }
  assert.equal(checked, 240);
});

test('all four experiences ask for the same data and validate contact details', () => {
  for (const variant of Object.keys(M.variants)) {
    const v = M.fixture('team'), keys = M.questionKeys(v, variant);
    assert.deepEqual(M.validate(v, keys), {});
    assert.ok(M.validate({ ...v, email: 'invalid', phone: '1234', consent: false }, keys).email);
    assert.ok(M.validate({ ...v, phone: '+44 20 1234 5678' }, keys).phone);
    assert.deepEqual(M.validate({ ...v, phone: '+61 400 000 000' }, keys), {});
  }
});

test('appointment, treatment and contact changes invalidate previous card consent', () => {
  for (const key of ['slot', 'teeth', 'superBand', 'state', 'phone']) {
    const v = { ...M.fixture('clinic'), slot: 'old-slot', policyConsent: true, demoCard: true };
    const next = { slot: 'new-slot', teeth: '3-5', superBand: 'Under $10k in super', state: 'Queensland (QLD)', phone: '0400 111 111' }[key];
    M.setAnswer(v, key, next);
    assert.equal(v.policyConsent, false);
    assert.equal(v.demoCard, false);
    if (key !== 'slot') assert.equal(v.slot, '');
  }
  const v = { ...M.fixture('clinic'), policyConsent: true, demoCard: true };
  M.setAnswer(v, 'policyConsent', false);
  assert.equal(v.demoCard, false);
});

test('example slots are future weekdays, including across month and year boundaries', () => {
  for (const instant of ['2026-10-09T12:00:00Z', '2026-12-31T12:00:00Z', '2026-10-06T23:55:00Z']) {
    const now = new Date(instant), slots = M.slotOptions(now);
    assert.equal(slots.length, 3);
    assert.equal(new Set(slots.map(x => x.id)).size, 3);
    for (const slot of slots) {
      const date = new Date(slot.date + 'T12:00:00Z');
      assert.ok(date > now);
      assert.ok(![0, 6].includes(date.getUTCDay()));
    }
  }
});
