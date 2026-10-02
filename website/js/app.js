(function (DM) {
  'use strict';
  const app = document.getElementById('app');
  const state = DM.state;
  const requested = new URLSearchParams(location.search).get('variation');
  if (requested && DM.variations[requested]) state.variation = requested;
  const routeFromUrl = () => location.hash.startsWith('#/') ? location.hash.slice(1).split('?')[0] : '/';
  const renderer = () => ({ '/': DM.home, '/implants': DM.implants, '/how-it-works': DM.how, '/costs': DM.costs, '/about': DM.about, '/questions': DM.questions, '/match': DM.matchForm, '/contact': DM.contactPage, '/privacy': DM.privacy, '/confirmation': DM.confirmationPage }[state.route] || DM.notFound);
  DM.render = (focus = false) => {
    document.documentElement.dataset.variation = state.variation;
    app.innerHTML = DM.header() + `<main id="page-content" tabindex="-1">${renderer()()}</main>` + DM.footer();
    document.title = `${DM.routes[state.route] || 'Page not found'} | Dental Match | ${DM.variations[state.variation].label}`;
    document.getElementById('route-status').textContent = `${DM.routes[state.route] || 'Page not found'}. ${DM.variations[state.variation].label} website variation.`;
    if (focus) {
      const main = document.getElementById('page-content');
      main.focus({ preventScroll: true });
      scrollTo({ top: 0, behavior: 'instant' });
    }
  };
  const captureCurrent = () => { const form = app.querySelector('#match-form,#contact-form,#quick-start'); if (form) DM.captureForm(form); };
  const focusErrors = () => { const summary = app.querySelector('.error-summary'); if (summary) { summary.focus(); summary.scrollIntoView({ block: 'center', behavior: 'instant' }); } else app.querySelector('[aria-invalid=true]')?.focus(); };
  const focusFormHeading = () => { const h = app.querySelector('.form-heading'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); h.scrollIntoView({ block: 'start', behavior: 'instant' }); } };
  DM.navigate = (route, capture = true) => {
    if (capture) captureCurrent();
    if (state.route === route) { DM.render(true); return; }
    location.hash = route;
  };
  const syncFromUrl = () => {
    const variation = new URLSearchParams(location.search).get('variation');
    const nextVariation = variation && DM.variations[variation] ? variation : state.variation;
    const nextRoute = routeFromUrl();
    if (nextRoute === state.route && nextVariation === state.variation) return;
    state.variation = nextVariation; state.route = nextRoute; DM.render(true);
  };
  window.addEventListener('hashchange', syncFromUrl);
  window.addEventListener('popstate', syncFromUrl);
  document.querySelector('.skip-link').addEventListener('click', event => {
    event.preventDefault(); const main = document.getElementById('page-content');
    main.focus({ preventScroll: true }); main.scrollIntoView({ block: 'start' });
  });
  app.addEventListener('input', event => {
    const form = event.target.closest('#match-form,#contact-form,#quick-start');
    if (form) DM.captureForm(form);
  });
  app.addEventListener('change', event => {
    const form = event.target.closest('#match-form,#contact-form,#quick-start');
    if (form) DM.captureForm(form);
    if (form?.id === 'match-form' && event.target.name === 'preference') {
      DM.render();
      document.getElementById('field-preference').focus({ preventScroll: true });
    }
  });
  app.addEventListener('click', event => {
    const button = event.target.closest('button');
    const variant = button?.dataset.variation;
    if (variant && DM.variations[variant]) {
      captureCurrent(); state.variation = variant;
      const url = new URL(location.href); url.searchParams.set('variation', variant); history.replaceState(null, '', url);
      DM.render(); app.querySelector(`button[data-variation="${variant}"]`).focus({ preventScroll: true });
      return;
    }
    if (button?.classList.contains('menu-toggle')) {
      const open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(open)); document.getElementById('site-nav').classList.toggle('is-open', open);
      return;
    }
    if (button?.dataset.concern) {
      state.concern = button.dataset.concern;
      const c = DM.concerns.find(c => c.value === state.concern);
      app.querySelectorAll('[data-concern]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      document.getElementById('concern-response').innerHTML = `<p class="response-heading">${DM.escape(c.title)}</p><p>${DM.escape(c.body)}</p>`;
      return;
    }
    if (button?.hasAttribute('data-back-step')) { captureCurrent(); state.formStep--; state.errors = {}; DM.render(); focusFormHeading(); return; }
    if (button?.hasAttribute('data-edit-step')) { state.formStep = Number(button.dataset.editStep); if (!state.formStep) state.fromHero = false; state.errors = {}; DM.render(); focusFormHeading(); return; }
    if (button?.hasAttribute('data-change-treatment')) { state.fromHero = false; DM.render(); app.querySelector('input[name=treatment]:checked')?.focus(); return; }
    if (button?.hasAttribute('data-start-again')) {
      state.match = DM.newMatch();
      state.formStep = 0; state.fromHero = false; state.errors = {}; state.confirmation = null; DM.navigate('/match'); return;
    }
    const errorLink = event.target.closest('[data-error-link]');
    if (errorLink) { event.preventDefault(); const field = document.getElementById('field-' + errorLink.dataset.errorLink); const target = field.matches('input,select,textarea') ? field : field.querySelector('input') || field; target.focus(); return; }
    const routeLink = event.target.closest('[data-route]');
    if (routeLink && !event.ctrlKey && !event.metaKey && !event.shiftKey && event.button === 0) {
      event.preventDefault();
      captureCurrent();
      if (routeLink.dataset.treatment) { state.match.treatment = routeLink.dataset.treatment; state.formStep = 0; state.fromHero = false; state.errors = {}; }
      DM.navigate(routeLink.dataset.route, false);
    }
  });
  app.addEventListener('submit', event => {
    const form = event.target;
    if (!['quick-start', 'match-form', 'contact-form'].includes(form.id)) return;
    event.preventDefault(); DM.captureForm(form);
    if (form.id === 'quick-start') {
      state.errors = DM.validateMatch(state.match, 0);
      if (Object.keys(state.errors).length) { DM.render(); app.querySelector('[name=treatment]')?.focus(); return; }
      state.formStep = 0; state.fromHero = true; DM.navigate('/match'); return;
    }
    if (form.id === 'match-form') {
      for (let step = 0; step <= state.formStep; step++) {
        state.errors = DM.validateMatch(state.match, step);
        if (Object.keys(state.errors).length) { state.formStep = step; DM.render(); focusErrors(); return; }
      }
      if (state.formStep < 3) { state.formStep++; DM.render(); focusFormHeading(); return; }
      state.confirmation = { kind: 'match', treatment: DM.treatments.find(t => t.value === state.match.treatment).label, postcode: state.match.postcode, preference: state.match.preference === 'phone' ? 'Phone' : 'Email' };
      state.match = DM.newMatch(); state.formStep = 0; state.fromHero = false;
      // Navigate without re-capturing the completed contact fields.
      location.hash = '/confirmation'; return;
    }
    state.contactErrors = DM.validateContact(state.contact);
    if (Object.keys(state.contactErrors).length) { DM.render(); focusErrors(); return; }
    state.confirmation = { kind: 'contact' }; state.contact = { name: '', email: '', message: '' }; location.hash = '/confirmation';
  });
  window.addEventListener('keydown', event => {
    if (event.code === 'Escape') {
      const toggle = app.querySelector('.menu-toggle[aria-expanded=true]');
      if (toggle) { toggle.setAttribute('aria-expanded', 'false'); document.getElementById('site-nav').classList.remove('is-open'); toggle.focus(); }
    }
  });
  state.route = routeFromUrl(); DM.render();
})(window.DentalMatch);
