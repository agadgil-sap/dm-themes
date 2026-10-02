(function (DM) {
  'use strict';
  const e = DM.escape;
  const contactOptions = [['phone', 'Phone'], ['email', 'Email']];
  DM.validateMatch = (values, step) => {
    const errors = {};
    if (step === 0 && !DM.treatments.some(t => t.value === values.treatment)) errors.treatment = 'Choose a starting point, including “I’m not sure yet” if that fits.';
    if (step === 1) {
      if (!/^\d{4}$/.test(values.postcode) || Number(values.postcode) < 200) errors.postcode = 'Enter an Australian postcode with four digits, such as 3000 or 0800.';
      if (!['local', 'nearby', 'travel'].includes(values.travel)) errors.travel = 'Choose how far you are comfortable travelling.';
      if (!['exploring', 'soon', 'later'].includes(values.timing)) errors.timing = 'Choose where you are in your decision.';
    }
    if (step === 2) {
      if (!values.name.trim()) errors.name = 'Add your name using sample details for this preview.';
      if (!['phone', 'email'].includes(values.preference)) errors.preference = 'Choose how you would prefer to be contacted.';
      if ((values.preference === 'email' || values.email) && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) errors.email = 'Enter an email address such as alex@example.com.';
      const digits = values.phone.replace(/\D/g, '');
      if ((values.preference === 'phone' || values.phone) && (!/^\+?[\d\s()-]+$/.test(values.phone) || digits.length < 8 || digits.length > 15)) errors.phone = 'Enter a phone number, including the area code or mobile prefix.';
    }
    if (step === 3 && !values.consent) errors.consent = 'Confirm that you understand this is a demo before completing it.';
    return errors;
  };
  DM.validateContact = values => {
    const errors = {};
    if (!values.name.trim()) errors.name = 'Add a sample name for this preview.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) errors.email = 'Enter an email address such as alex@example.com.';
    if (!values.message.trim()) errors.message = 'Add the question you would like to ask.';
    return errors;
  };
  DM.captureForm = form => {
    const data = new FormData(form);
    const target = form.id === 'contact-form' ? DM.state.contact : DM.state.match;
    for (const name of new Set([...form.elements].filter(el => el.name).map(el => el.name))) {
      if (name === 'concerns') target.concerns = data.getAll(name).filter(value => DM.concerns.some(c => c.value === value));
      else if (name === 'consent') target.consent = data.has(name);
      else target[name] = String(data.get(name) || '').trim();
    }
  };
  DM.matchForm = () => {
    const { match: m, errors, formStep: step } = DM.state;
    const titles = ['Where would you like to start?', 'What works for your life?', 'How would you like to hear from us?', 'Take a moment to review.'];
    const descriptions = ['You do not need a treatment plan. Choose the description that feels closest.', 'Your location and preferences help give the conversation useful context.', 'Use sample details. The preview does not send anything or arrange contact.', 'Check your choices before completing the demo enquiry.'];
    if (step === 0 && DM.state.fromHero) {
      titles[0] = 'What would you like the clinic to know?';
      descriptions[0] = 'Your starting point is selected. Add any concerns below, or continue when you’re ready.';
    }
    let fields = '';
    if (step === 0) {
      const treatment = DM.treatments.find(t => t.value === m.treatment);
      const startingPoint = DM.state.fromHero && treatment ? `<div class="selected-starting-point"><span class="icon-disc">${DM.icon(treatment.icon)}</span><div><small>Your starting point</small><strong>${e(treatment.label)}</strong></div><button type="button" class="text-button" data-change-treatment>Change</button></div>` : DM.choiceGroup({ name: 'treatment', legend: 'What are you exploring?', options: DM.treatments, value: m.treatment, error: errors.treatment, required: true });
      fields = startingPoint + DM.choiceGroup({ name: 'concerns', legend: 'What would you like the clinic to understand? (Optional)', options: DM.concerns, value: m.concerns, multiple: true, compact: true });
    }
    if (step === 1) fields = DM.field({ id: 'postcode', label: 'Your postcode', value: m.postcode, hint: 'Four digits, including a leading zero if needed. For example, 3000 or 0800.', required: true, autocomplete: 'postal-code', attrs: 'inputmode="numeric" maxlength="4"', error: errors.postcode }) + DM.choiceGroup({ name: 'travel', legend: 'How far could you travel?', options: [{ value: 'local', label: 'Keep it local' }, { value: 'nearby', label: 'Nearby areas are fine' }, { value: 'travel', label: 'I’m open to travelling' }], value: m.travel, error: errors.travel, compact: true }) + DM.choiceGroup({ name: 'timing', legend: 'Where are you in your decision?', options: [{ value: 'exploring', label: 'I’m exploring and asking questions' }, { value: 'soon', label: 'I’d like to discuss a consultation' }, { value: 'later', label: 'I’m thinking about later' }], value: m.timing, error: errors.timing, compact: true });
    if (step === 2) fields = DM.field({ id: 'name', label: 'Your name', value: m.name, required: true, autocomplete: 'name', attrs: 'maxlength="80"', error: errors.name }) + DM.field({ id: 'preference', label: 'Preferred way to be contacted', value: m.preference, required: true, options: contactOptions, error: errors.preference }) + `<div class="field-pair">${DM.field({ id: 'phone', label: m.preference === 'phone' ? 'Phone number' : 'Phone number (Optional)', type: 'tel', value: m.phone, required: m.preference === 'phone', autocomplete: 'tel', attrs: 'maxlength="25"', error: errors.phone })}${DM.field({ id: 'email', label: m.preference === 'email' ? 'Email address' : 'Email address (Optional)', type: 'email', value: m.email, required: m.preference === 'email', autocomplete: 'email', attrs: 'maxlength="150"', error: errors.email })}</div>` + DM.field({ id: 'contactTime', label: 'A convenient time (Optional)', value: m.contactTime, options: [['any', 'No preference'], ['morning', 'Morning'], ['afternoon', 'Afternoon'], ['evening', 'Evening']], hint: 'A preference to discuss, rather than a promised appointment time.' });
    if (step === 3) {
      const travel = { local: 'Keep it local', nearby: 'Nearby areas are fine', travel: 'Open to travelling' };
      const timing = { exploring: 'Exploring and asking questions', soon: 'Discussing a consultation', later: 'Thinking about later' };
      fields = `<dl class="review-list">${DM.reviewRow('Starting point', DM.treatments.find(t => t.value === m.treatment)?.label, 0)}${DM.reviewRow('Things to understand', m.concerns.map(value => DM.concerns.find(c => c.value === value)?.label).join(', ') || 'No concerns selected', 0)}${DM.reviewRow('Postcode', m.postcode, 1)}${DM.reviewRow('Travel', travel[m.travel], 1)}${DM.reviewRow('Your timing', timing[m.timing], 1)}${DM.reviewRow('Name', m.name, 2)}${DM.reviewRow('Contact preference', m.preference === 'phone' ? 'Phone' : 'Email', 2)}${DM.reviewRow('Contact detail', m.preference === 'phone' ? m.phone : m.email, 2)}</dl><div class="consent-field" id="field-consent"><label><input type="checkbox" name="consent" value="yes"${m.consent ? ' checked' : ''}${errors.consent ? ' aria-invalid="true" aria-describedby="error-consent"' : ''}><span>I understand this is a website preview. No enquiry will be sent and no booking will be made.</span></label>${errors.consent ? `<p class="field-error" id="error-consent">${e(errors.consent)}</p>` : ''}</div>`;
    }
    return `${DM.breadcrumb('Explore my options')}<section class="match-section container"><div class="match-heading"><p class="eyebrow">Your next step starts here</p><h1>Let’s find your<br>starting point.</h1><p>You can be certain, curious or somewhere in between.</p></div><div class="match-layout"><div class="form-shell">${DM.demoNotice()}${DM.progress(step)}<form id="match-form" novalidate><div class="form-heading"><p class="eyebrow">Step ${step + 1} of 4</p><h2>${titles[step]}</h2><p>${descriptions[step]}</p></div>${DM.errorSummary(errors)}${fields}<div class="form-actions">${step > 0 ? `<button class="button button-secondary" type="button" data-back-step>Back</button>` : DM.link('/', 'Back to the website', 'quiet-link')}<button class="button button-primary" type="submit">${step === 3 ? 'Complete demo enquiry' : step === 2 ? 'Review my choices' : 'Continue'}${DM.icon('arrow')}</button></div></form></div><aside class="form-aside"><div class="form-aside-mark">${DM.logo()}</div><h2>A conversation<br>comes first.</h2><p>You’re sharing a starting point, rather than choosing a treatment today.</p><ul class="check-list"><li>${DM.icon('check')}“I’m not sure” is a valid answer.</li><li>${DM.icon('check')}You can go back and change a detail.</li><li>${DM.icon('check')}A dentist assesses clinical suitability.</li></ul><div class="aside-help"><p>Want to read a little first?</p>${DM.link('/implants', 'Understand dental implants')}${DM.link('/questions', 'Read common questions')}</div></aside></div></section>`;
  };
  DM.contactPage = () => {
    const c = DM.state.contact, errors = DM.state.contactErrors;
    return `${DM.breadcrumb('Ask a question')}${DM.pageHero('Start with a question', 'What would help you feel clearer?', 'Try the question form with sample details. It demonstrates how an enquiry could work, without sending a message.')}<section class="section container two-column contact-layout"><div class="section-copy"><p class="eyebrow">You can ask about the first step</p><h2>No question<br>is too small.</h2><p>Perhaps you want to understand how matching works, what an appointment might involve or where to begin with cost questions.</p>${DM.callout('Already exploring implants?', 'The matching enquiry gives you a place to describe your starting point and preferences.', 'chat')}${DM.button('/match')}</div><div class="form-shell">${DM.demoNotice()}<form id="contact-form" novalidate>${DM.errorSummary(errors)}${DM.field({ id: 'name', label: 'Your name', value: c.name, required: true, autocomplete: 'name', attrs: 'maxlength="80"', error: errors.name })}${DM.field({ id: 'email', label: 'Email address', type: 'email', value: c.email, required: true, autocomplete: 'email', attrs: 'maxlength="150"', error: errors.email })}${DM.field({ id: 'message', label: 'Your question', type: 'textarea', value: c.message, hint: 'Use a sample question. Please leave medical records and detailed health information out of this preview.', required: true, attrs: 'maxlength="1500"', error: errors.message })}<button class="button button-primary" type="submit">Complete demo question${DM.icon('arrow')}</button></form></div></section>`;
  };
  DM.confirmationPage = () => {
    const c = DM.state.confirmation;
    if (!c) return `${DM.pageHero('Take a first step', 'There is no completed preview yet.', 'Explore the matching form to see its review and confirmation screens.')}<section class="section container">${DM.button('/match')}</section>`;
    return `<section class="confirmation-section container"><div class="confirmation-card"><span class="confirmation-icon">${DM.icon('check')}</span><p class="eyebrow">Demo completed</p><h1>${c.kind === 'match' ? 'You’ve found a starting point.' : 'You’ve tried the question flow.'}</h1><p class="lead"><strong>No enquiry has been sent.</strong> This confirmation is part of the website preview. No clinic or coordinator will contact you.</p>${c.kind === 'match' ? `<dl class="confirmation-summary">${DM.reviewRow('Starting point', c.treatment)}${DM.reviewRow('Postcode', c.postcode)}${DM.reviewRow('Contact preference', c.preference)}</dl>` : ''}<div class="confirmation-next"><h2>What a live service would do next</h2><p>${c.kind === 'match' ? 'A coordinator or participating clinic would discuss your enquiry, explain the next steps and confirm availability. A dentist would assess treatment suitability.' : 'The team would respond to your question using the contact preference you provided.'}</p></div><div class="confirmation-actions">${DM.button('/', 'Back to the website')}<button class="button button-secondary" type="button" data-start-again>Try another demo enquiry</button></div></div></section>`;
  };
})(window.DentalMatch);
