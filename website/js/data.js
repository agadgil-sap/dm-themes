window.DentalMatch = {};
(function (DM) {
  'use strict';
  DM.variations = {
    welcome: { label: 'Clear & welcoming', short: 'Welcoming', number: '1', title: 'A clearer path to your next smile.', eyebrow: 'Dental implants. A first step that feels possible.', intro: 'If dental care has had to wait, you’re in the right place. Explore dental implant options and connect with a clinic that can talk through your next step.' },
    guided: { label: 'Your guided first step', short: 'Guided', number: '2', title: 'Big dental decisions. Smaller first steps.', eyebrow: 'Dental implants. Start with where you are.', intro: 'One missing tooth, several, or simply unsure? Tell us what you’re exploring. We’ll help you start a conversation with a participating clinic.' },
    considered: { label: 'Space to decide', short: 'Considered', number: '3', title: 'You don’t need every answer to begin.', eyebrow: 'Dental implants. A little clarity to begin.', intro: 'Dental implants are a decision worth understanding. Take a moment to explore your questions, then find a starting point with a clinic in our network.' }
  };
  DM.routes = {
    '/': 'Home', '/implants': 'Dental implants', '/how-it-works': 'How matching works', '/costs': 'Costs & options', '/about': 'About Dental Match', '/questions': 'Your questions', '/match': 'Explore my options', '/contact': 'Ask a question', '/privacy': 'About this preview', '/confirmation': 'Preview complete'
  };
  DM.treatments = [
    { value: 'single', label: 'One missing tooth', detail: 'Explore a single implant', icon: 'tooth' },
    { value: 'several', label: 'Several missing teeth', detail: 'Explore your replacement options', icon: 'teeth' },
    { value: 'full', label: 'Most or all teeth', detail: 'Explore a larger treatment plan', icon: 'smile' },
    { value: 'unsure', label: 'I’m not sure yet', detail: 'Start with a conversation', icon: 'chat' }
  ];
  DM.concerns = [
    { value: 'anxiety', label: 'I feel anxious', title: 'You can start by saying that.', body: 'Tell the clinic what worries you before your appointment. Ask how they explain treatment, help anxious patients and give you time to decide.', icon: 'heart' },
    { value: 'cost', label: 'I’m worried about cost', title: 'Clear questions before a big decision.', body: 'Ask for an itemised treatment plan and discuss payment arrangements with the clinic. Availability, fees and eligibility need to be confirmed with the provider.', icon: 'wallet' },
    { value: 'time', label: 'Life keeps getting in the way', title: 'Your practical needs belong in the conversation.', body: 'Let the clinic know about work, family and travel. Ask about appointment options, the likely treatment schedule and time you may need away from work.', icon: 'clock' },
    { value: 'shame', label: 'It’s been a long time', title: 'Start from where you are today.', body: 'You do not have to explain everything to take a first step. Share what would help you feel comfortable, then let a dentist talk through your options.', icon: 'leaf' }
  ];
  DM.matchingSteps = [
    { title: 'Tell us where you are', body: 'Share what you’re exploring, your location and anything that would make the first conversation easier.', icon: 'chat' },
    { title: 'Explore a clinic connection', body: 'Your needs help guide a connection with a participating clinic. Availability and the clinic’s services are confirmed with you.', icon: 'match' },
    { title: 'Decide with a dentist', body: 'A dentist assesses your needs and explains treatment, costs and alternatives. You decide whether to take the next step.', icon: 'check' }
  ];
  DM.faqs = [
    { q: 'Do I need to know which implant treatment I want?', a: 'No. “I’m not sure yet” is a useful starting point. The matching enquiry helps you begin a conversation; a dentist assesses which treatments may be suitable.' },
    { q: 'Is Dental Match a dental clinic?', a: 'Dental Match is a matching service that connects patients with participating clinics. The clinic provides clinical advice, assessment and treatment.' },
    { q: 'Can I tell you I’m nervous?', a: 'Yes. You can select anxiety as a concern in the enquiry. Ask the clinic how they support anxious patients and what to expect at the first appointment.' },
    { q: 'Can I ask about costs before committing?', a: 'Yes. Ask the clinic what an initial consultation costs, what a treatment quote includes and which payment arrangements they offer. Any funding application has its own terms and eligibility requirements.' },
    { q: 'Does a match mean I am suitable for implants?', a: 'No. A clinic connection is a starting point. A dentist needs to assess your oral and general health before advising on implants or alternatives.' },
    { q: 'Who will contact me first?', a: 'The live service may start with a Dental Match coordinator or a participating clinic. This website preview demonstrates the enquiry experience; it does not send details or arrange contact.' },
    { q: 'Can I explore options if I need more than one tooth replaced?', a: 'Yes. Choose several missing teeth or most or all teeth in the enquiry. A dentist can explain the options that fit your situation.' },
    { q: 'What happens when I submit this preview form?', a: 'You will see a review and a confirmation screen. The demo sends nothing to a clinic and makes no booking. Use sample contact details while exploring it.' }
  ];
  DM.newMatch = () => ({ treatment: '', concerns: [], postcode: '', travel: 'local', timing: 'exploring', name: '', email: '', phone: '', preference: 'phone', contactTime: 'any', consent: false });
  DM.state = { variation: 'welcome', route: '/', concern: 'anxiety', formStep: 0, fromHero: false, match: DM.newMatch(), errors: {}, confirmation: null, contact: { name: '', email: '', message: '' }, contactErrors: {} };
})(window.DentalMatch);
