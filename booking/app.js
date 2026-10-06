(function (root) {
  'use strict';
  const M = root.BookingModel, V = root.BookingView;
  const app = document.getElementById('app');
  const initialVariant = new URLSearchParams(location.search).get('variation');
  const s = { variant: M.variants[initialVariant] ? initialVariant : 'visual', v: M.empty(), route: '', resume: '', errors: {}, submitted: false, editing: false, assisted: false, callbackDone: false, slots: M.slotOptions() };
  const first = () => s.variant === 'planner' ? 'planner' : 'teeth';
  const path = () => location.hash.startsWith('#/') ? location.hash.slice(2).split('?')[0] : first();
  const missingStep = () => M.questionKeys(s.v, s.variant).find(key => Object.keys(M.validate(s.v, [key])).length);
  const qualifiedRoute = () => M.route(s.v)?.id || first();
  const validSlot = () => s.slots.some(slot => slot.id === s.v.slot);
  function guard(route) {
    if (route === 'resume') return s.resume || first();
    if (['questions', 'privacy'].includes(route)) return route;
    if (route === 'planner') return s.variant === 'planner' ? route : first();
    const keys = M.questionKeys(s.v, s.variant);
    if (keys.includes(route)) {
      if (s.variant === 'planner') return 'planner';
      const earlier = keys.slice(0, keys.indexOf(route)).find(key => Object.keys(M.validate(s.v, [key])).length);
      return earlier || route;
    }
    if (route === 'review') return missingStep() ? (s.variant === 'planner' ? 'planner' : missingStep()) : route;
    const known = ['clinic', 'team', 'followup', 'appointment', 'card', 'handoff', 'booking-help', 'callback-confirmation'];
    if (!known.includes(route)) return first();
    if (!s.submitted || missingStep()) return guard('review');
    const outcome = qualifiedRoute();
    if (['clinic', 'team', 'followup'].includes(route)) return route === outcome ? route : outcome;
    if (['appointment', 'card', 'handoff', 'booking-help'].includes(route)) {
      if (outcome !== 'clinic') return outcome;
      if (route === 'appointment') return route;
      if (!validSlot()) return 'appointment';
      if (['card', 'booking-help'].includes(route)) return s.variant === 'card' ? route : 'handoff';
      if (s.variant === 'card' && (!s.v.policyConsent || !s.v.demoCard)) return 'card';
      return route;
    }
    if (route === 'callback-confirmation') return s.callbackDone ? route : s.assisted ? 'booking-help' : outcome;
    return first();
  }
  function render(focus = false, preserveScroll = false) {
    const scroll = window.scrollY;
    document.documentElement.dataset.variation = s.variant;
    app.innerHTML = V.shell(s);
    document.title = `${M.questions[s.route] || ({ clinic: 'Your clinic consultation', team: 'A call with our team', followup: 'Enquiry follow-up', planner: 'Consultation planner', handoff: 'Clinic booking handoff', 'callback-confirmation': 'Callback request preview' })[s.route] || 'Dental Match'} | ${M.variants[s.variant].label}`;
    document.getElementById('route-status').textContent = `${M.variants[s.variant].label}. ${M.questions[s.route] || s.route}.`;
    if (focus) {
      document.getElementById('main').focus({ preventScroll: true });
      if (!preserveScroll) window.scrollTo({ top: 0, behavior: 'instant' });
    }
    if (preserveScroll) window.scrollTo({ top: scroll, behavior: 'instant' });
  }
  function go(requested, { replace = false, focus = true } = {}) {
    if (['questions', 'privacy'].includes(requested) && !['questions', 'privacy'].includes(s.route)) s.resume = s.route || first();
    const route = guard(requested);
    s.route = route; s.errors = {};
    if (!['questions', 'privacy'].includes(route)) s.resume = route;
    const url = new URL(location.href);
    url.searchParams.set('variation', s.variant); url.hash = '/' + route;
    if (replace) history.replaceState(null, '', url);
    else if (url.href !== location.href) history.pushState(null, '', url);
    render(focus);
  }
  function capture(form) {
    const data = new FormData(form);
    for (const name of new Set([...form.elements].filter(el => el.name && !el.disabled).map(el => el.name))) {
      const input = form.querySelector(`[name="${name}"]`);
      const value = input.type === 'checkbox' ? data.has(name) : String(data.get(name) || '').trim();
      if (s.v[name] !== value && !['slot', 'callback', 'policyConsent', 'demoCard'].includes(name)) { s.submitted = false; s.callbackDone = false; }
      M.setAnswer(s.v, name, value);
    }
  }
  function showErrors(errors) {
    s.errors = errors; render(false, true);
    const summary = document.querySelector('.error-summary');
    summary?.focus(); summary?.scrollIntoView({ block: 'center', behavior: 'instant' });
  }
  function reset() {
    s.v = M.empty(); s.submitted = false; s.editing = false; s.callbackDone = false; s.assisted = false;
    go(first());
  }
  function switchVariant(variant) {
    if (!M.variants[variant]) return;
    const form = document.querySelector('#booking-form,#appointment-form,#card-form,#callback-form');
    if (form) capture(form);
    s.variant = variant;
    let next = s.route;
    if (variant === 'planner' && M.questionKeys(s.v, 'conversation').includes(next)) next = 'planner';
    else if (next === 'planner') next = 'teeth';
    else if (next === 'contact' && variant === 'conversation') next = 'firstName';
    else if (['firstName', 'lastName', 'email', 'phone', 'consent'].includes(next) && variant !== 'conversation') next = 'contact';
    if (['card', 'booking-help'].includes(next) && variant !== 'card') next = 'appointment';
    // A variant switch is not authorisation for a card or a booking.
    s.v.policyConsent = false; s.v.demoCard = false;
    go(next, { replace: true });
  }
  app.addEventListener('input', ev => {
    const form = ev.target.closest('form');
    if (form) capture(form);
    if (s.route === 'planner') document.getElementById('planner-summary').innerHTML = V.miniSummary(s);
  });
  app.addEventListener('change', ev => {
    const form = ev.target.closest('form');
    if (!form) return;
    capture(form);
    if (s.route === 'planner' && ['superBand', 'finance', 'residency'].includes(ev.target.name)) {
      const name = ev.target.name, value = ev.target.value;
      render(false, true);
      [...app.querySelectorAll(`[name="${name}"]`)].find(el => el.value === value)?.focus({ preventScroll: true });
    }
    if (s.route === 'card' && ev.target.name === 'policyConsent' && !s.v.policyConsent) {
      document.getElementById('card-status').textContent = 'Accept the example terms again to try card setup.';
      app.querySelector('[data-simulate-card]').textContent = 'Try the card setup preview';
    }
  });
  app.addEventListener('submit', ev => {
    ev.preventDefault(); const form = ev.target; capture(form);
    if (form.id === 'booking-form') {
      const all = M.questionKeys(s.v, s.variant);
      const keys = s.route === 'planner' || s.route === 'review' ? all : all.slice(0, all.indexOf(s.route) + 1);
      const errors = M.validate(s.v, keys);
      if (Object.keys(errors).length) { showErrors(errors); return; }
      if (s.route === 'review') {
        s.submitted = true; s.editing = false; s.assisted = false; s.callbackDone = false;
        go(qualifiedRoute());
      } else if (s.route === 'planner' || s.editing) go('review');
      else go(all[all.indexOf(s.route) + 1] || 'review');
    }
    if (form.id === 'appointment-form') {
      if (!validSlot()) { showErrors({ slot: 'Choose an example consultation time.' }); return; }
      go(s.variant === 'card' ? 'card' : 'handoff');
    }
    if (form.id === 'card-form') {
      if (!s.v.policyConsent || !s.v.demoCard) { showErrors({ policyConsent: 'Accept the example terms and try the card setup preview before continuing.' }); return; }
      go('handoff');
    }
    if (form.id === 'callback-form') {
      if (!['Morning · 9 am-12 pm', 'Afternoon · 12 pm-5 pm', 'No preference'].includes(s.v.callback)) { showErrors({ callback: 'Choose a callback preference.' }); return; }
      s.callbackDone = true; s.assisted = s.route === 'booking-help'; go('callback-confirmation');
    }
  });
  app.addEventListener('click', ev => {
    const target = ev.target.closest('button,a');
    if (!target) return;
    if (target.dataset.variant) { switchVariant(target.dataset.variant); return; }
    if (target.hasAttribute('data-review')) { document.getElementById('review-dialog').showModal(); return; }
    if (target.hasAttribute('data-close')) { document.getElementById('review-dialog').close(); return; }
    if (target.dataset.fixture) {
      s.v = M.fixture(target.dataset.fixture); s.submitted = false; s.callbackDone = false; s.editing = false; go('review'); return;
    }
    if (target.hasAttribute('data-reset')) { reset(); return; }
    if (target.hasAttribute('data-back')) {
      const form = document.getElementById('booking-form'); if (form) capture(form);
      if (s.route === 'review') go(s.variant === 'planner' ? 'planner' : M.questionKeys(s.v, s.variant).at(-1));
      else { const keys = M.questionKeys(s.v, s.variant); go(keys[Math.max(0, keys.indexOf(s.route) - 1)]); }
      return;
    }
    if (target.dataset.edit) {
      s.editing = true; s.submitted = false; s.callbackDone = false;
      let key = target.dataset.edit;
      if (key === 'contact' && s.variant === 'conversation') key = 'firstName';
      go(s.variant === 'planner' ? 'planner' : key); return;
    }
    if (target.dataset.go) { go(target.dataset.go); return; }
    if (target.hasAttribute('data-simulate-card')) {
      capture(document.getElementById('card-form'));
      if (!s.v.policyConsent) { showErrors({ policyConsent: 'Accept the example card terms first.' }); return; }
      s.v.demoCard = true; s.errors = {}; render(false, true);
      document.getElementById('card-status').textContent = 'Example complete. No card has been saved and no funds are held.'; return;
    }
    if (target.hasAttribute('data-demo-handoff')) {
      document.getElementById('handoff-status').textContent = 'Handoff preview complete. A live clinic link must be connected. No appointment is booked.'; return;
    }
    if (target.dataset.error) {
      ev.preventDefault(); const el = document.getElementById('field-' + target.dataset.error);
      const field = el?.matches('input') ? el : el?.querySelector('input'); field?.focus(); return;
    }
    if (target.tagName === 'A' && target.getAttribute('href')?.startsWith('#/')) {
      if (ev.ctrlKey || ev.metaKey || ev.shiftKey || ev.button !== 0) return;
      ev.preventDefault(); go(target.getAttribute('href').slice(2));
    }
  });
  document.querySelector('.skip-link').addEventListener('click', ev => { ev.preventDefault(); document.getElementById('main').focus(); });
  function fromUrl() {
    const variant = new URLSearchParams(location.search).get('variation');
    if (M.variants[variant]) s.variant = variant;
    go(path(), { replace: true });
  }
  window.addEventListener('popstate', fromUrl);
  window.addEventListener('hashchange', fromUrl);
  go(path(), { replace: true, focus: false });
})(window);
