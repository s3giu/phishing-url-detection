import { analyzeUrl } from './analyzer.js';

const form = document.querySelector('#check-form');
const input = document.querySelector('#url-input');
const error = document.querySelector('#input-error');
const results = document.querySelector('#results');
const text = (selector, value) => { document.querySelector(selector).textContent = value; };

function resetResult() {
  results.hidden = true;
  error.hidden = true;
  error.textContent = '';
  input.removeAttribute('aria-invalid');
}

function check() {
  resetResult();
  let result;
  try {
    result = analyzeUrl(input.value);
    if (!result.hostname) {
      throw new Error(result.findings[0]?.detail || 'Please enter a complete HTTP or HTTPS website link.');
    }
  } catch (err) {
    error.textContent = err.message || 'Please enter a complete HTTP or HTTPS website link.';
    error.hidden = false;
    input.setAttribute('aria-invalid', 'true');
    input.focus();
    return;
  }
  text('#hostname', result.hostname);
  text('#result-title', result.findings.length ? 'A few things deserve a closer look.' : 'No obvious warning signs in the link text.');
  text('#result-summary', 'This is not a safety verdict. Verify independently before sharing information or paying.');
  text('#connection', result.protocol === 'https' ? 'HTTPS · not proof of trust' : 'HTTP · not encrypted');
  text('#port', result.port || (result.protocol === 'https' ? '443 (default)' : '80 (default)'));
  const findings = document.querySelector('#findings');
  findings.replaceChildren();
  const items = result.findings.length ? result.findings : [{ title: 'Nothing obvious is not an all-clear', detail: 'A convincing-looking address can still host a scam. The page, owner, reputation, and redirects have not been checked.' }];
  for (const finding of items) {
    const li = document.createElement('li');
    const title = document.createElement('h4');
    const detail = document.createElement('p');
    title.textContent = finding.title;
    detail.textContent = finding.detail;
    li.append(title, detail);
    findings.append(li);
  }
  text('#verify-title', result.verification.title);
  text('#verification', result.verification.detail);
  const features = document.querySelector('#features');
  features.replaceChildren();
  for (const [name, value] of Object.entries(result.features)) {
    const row = document.createElement('div');
    const label = document.createElement('dt');
    const number = document.createElement('dd');
    label.textContent = name.replaceAll('_', ' ');
    number.textContent = Number.isInteger(value) ? String(value) : value.toFixed(4);
    row.append(label, number);
    features.append(row);
  }
  results.hidden = false;
  results.focus({ preventScroll: true });
  results.scrollIntoView({ behavior: 'instant', block: 'start' });
}

form.addEventListener('submit', (event) => { event.preventDefault(); check(); });
input.addEventListener('input', resetResult);
document.querySelector('#clear-button').addEventListener('click', () => {
  form.reset();
  resetResult();
  document.querySelector('#findings').replaceChildren();
  document.querySelector('#features').replaceChildren();
  text('#hostname', '');
  input.focus();
});
for (const example of document.querySelectorAll('[data-example]')) {
  example.addEventListener('click', () => { input.value = example.dataset.example; check(); });
}
