(function (root) {
  'use strict';
  const variants = {
    visual: { number: '01', label: 'Visual smile selector', short: 'Visual', rationale: 'Pictures make the treatment question easier to scan. One question per screen keeps the funding branch manageable on a phone.' },
    conversation: { number: '02', label: 'A conversation in the form', short: 'Conversation', rationale: 'Previous answers stay visible and editable. This tests whether a quieter, conversational pace helps people finish sensitive funding questions.' },
    planner: { number: '03', label: 'Consultation planner', short: 'Planner', rationale: 'The whole enquiry is visible in four sections. This suits people who want to see what is being asked before sharing their details.' },
    card: { number: '04', label: 'Optional secure card', short: 'With card', rationale: 'A separate appointment commitment step tests its effect on completion and attendance. It appears only on the clinic route, after an appointment is selected.' }
  };
  const groups = {
    teeth: ['All', '6+', '3-5', '2 or less'],
    superBand: ['$50k+ in super', '$20k-$50k in super', '$10k-$20k in super', 'Under $10k in super'],
    finance: ['Yes', 'No'], residency: ['Yes', 'No'], work: ['Yes', 'No'],
    state: ['Western Australia (WA)', 'Victoria (VIC)', 'Queensland (QLD)', 'New South Wales (NSW)', 'South Australia (SA)', 'Tasmania (TAS)']
  };
  const questions = {
    teeth: 'How many missing or broken teeth do you have?',
    superBand: 'How much do you have in super?',
    finance: 'Are you interested in a payment plan to fund treatment?',
    residency: 'Are you an Australian permanent resident?',
    work: 'Are you working at least 25 hours per week or employed full-time?',
    state: 'Which state are you in?',
    firstName: 'What is your first name?', lastName: 'And your last name?',
    email: 'What is your email address?', phone: 'What number can we reach you on?',
    contact: 'Where can we reach you?', consent: 'Before we finish', review: 'Check your details',
    appointment: 'Choose a consultation time', card: 'A card for your appointment'
  };
  const empty = () => ({ teeth: '', superBand: '', finance: '', residency: '', work: '', state: '', firstName: '', lastName: '', email: '', phone: '', consent: false, slot: '', policyConsent: false, demoCard: false, callback: '' });
  const lowSuper = v => groups.superBand.slice(2).includes(v.superBand);
  const fundingKeys = v => lowSuper(v) ? ['finance', ...(v.finance === 'Yes' ? ['residency', ...(v.residency === 'Yes' ? ['work'] : [])] : [])] : [];
  const questionKeys = (v, variant) => ['teeth', 'superBand', ...fundingKeys(v), 'state', ...(variant === 'conversation' ? ['firstName', 'lastName', 'email', 'phone', 'consent'] : ['contact'])];
  const prune = v => {
    if (!lowSuper(v)) { v.finance = ''; v.residency = ''; v.work = ''; }
    else if (v.finance !== 'Yes') { v.residency = ''; v.work = ''; }
    else if (v.residency !== 'Yes') v.work = '';
    return v;
  };
  const validate = (v, keys) => {
    const errors = {};
    for (const key of keys) {
      if (groups[key] && !groups[key].includes(v[key])) errors[key] = 'Choose an answer to continue.';
      if (key === 'contact') Object.assign(errors, validate(v, ['firstName', 'lastName', 'email', 'phone', 'consent']));
      if (['firstName', 'lastName'].includes(key) && (!v[key].trim() || v[key].length > 80)) errors[key] = 'Enter a name using up to 80 characters.';
      if (key === 'email' && (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email) || v.email.length > 150)) errors.email = 'Enter an email address, such as alex@example.com.';
      if (key === 'phone' && !/^(?:0[23478]\d{8}|61[23478]\d{8})$/.test(v.phone.replace(/[\s()+-]/g, ''))) errors.phone = 'Enter an Australian mobile or landline number, including its prefix.';
      if (key === 'consent' && !v.consent) errors.consent = 'Confirm that you are using sample details for this preview.';
    }
    return errors;
  };
  // Commercial demonstration rules. These must be approved before live use.
  // They do not assess clinical suitability, lending or access to super.
  const route = v => {
    if (Object.keys(validate(v, ['teeth', 'superBand', ...fundingKeys(v), 'state'])).length) return null;
    if (lowSuper(v) && v.finance === 'No') return { id: 'followup', reason: 'Lower super band and no interest in a payment plan. Send for follow-up without reserving a consultation.' };
    if (lowSuper(v) || ['3-5', '2 or less'].includes(v.teeth)) return { id: 'team', reason: 'Funding or treatment scope needs a team conversation before a clinic referral.' };
    return { id: 'clinic', reason: 'All / 6+ teeth, a $20k+ super band and a listed state meet the example referral rule. A dentist still assesses treatment suitability.' };
  };
  const invalidateAppointment = v => { v.slot = ''; v.policyConsent = false; v.demoCard = false; v.callback = ''; };
  const setAnswer = (v, key, value) => {
    if (!(key in v)) return;
    if (v[key] !== value && !['policyConsent', 'demoCard', 'callback'].includes(key)) {
      if (key === 'slot') { v.policyConsent = false; v.demoCard = false; }
      else invalidateAppointment(v);
    }
    v[key] = value;
    if (key === 'policyConsent' && !value) v.demoCard = false;
    prune(v);
  };
  const slotOptions = (now = new Date()) => {
    const options = [];
    const current = new Intl.DateTimeFormat('en-CA', { timeZone: 'Australia/Melbourne', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(now);
    const part = key => current.find(p => p.type === key).value;
    const day = new Date(Date.UTC(Number(part('year')), Number(part('month')) - 1, Number(part('day')), 12));
    while (options.length < 3) {
      day.setUTCDate(day.getUTCDate() + 1);
      if ([0, 6].includes(day.getUTCDay())) continue;
      const date = day.toISOString().slice(0, 10);
      const label = new Intl.DateTimeFormat('en-AU', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(day);
      options.push({ id: date + 'T' + (options.length === 1 ? '14:30' : '11:00'), date, label, time: options.length === 1 ? '2:30 pm' : '11:00 am' });
    }
    return options;
  };
  const fixtures = {
    clinic: { teeth: 'All', superBand: '$50k+ in super', state: 'Victoria (VIC)' },
    team: { teeth: '6+', superBand: 'Under $10k in super', finance: 'Yes', residency: 'Yes', work: 'Yes', state: 'Victoria (VIC)' },
    followup: { teeth: 'All', superBand: 'Under $10k in super', finance: 'No', state: 'Victoria (VIC)' }
  };
  const fixture = id => ({ ...empty(), ...fixtures[id], firstName: 'Alex', lastName: 'Example', email: 'alex@example.com', phone: '0400 000 000', consent: true });
  const api = { variants, groups, questions, empty, lowSuper, fundingKeys, questionKeys, prune, validate, route, setAnswer, slotOptions, fixture };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.BookingModel = api;
})(typeof window === 'undefined' ? globalThis : window);
