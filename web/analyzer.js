/** Browser-only, network-free Check Before You Click analyzer. */

const MAX_LENGTH = 8192;
const REDIRECT_KEYS = new Set(['url', 'redirect', 'redirect_uri', 'next', 'continue', 'target', 'dest', 'destination']);
const SHORTENERS = ['bit.ly', 't.co', 'tinyurl.com', 'goo.gl', 'is.gd', 'ow.ly', 'rb.gy'];
const SPECIAL_CHARS = /[-_.~:/?#\[\]@!$&'()*+,;=%]/g;

function entropy(s) {
  if (!s.length) return 0;
  const counts = new Map();
  for (const c of s) counts.set(c, (counts.get(c) || 0) + 1);
  let result = 0;
  for (const count of counts.values()) {
    const p = count / s.length;
    result -= p * Math.log2(p);
  }
  return result;
}

/** Reproduces src/features/lexical_features.py against the analyzer's normalized URL. */
export function lexicalFeatures(value) {
  const s = String(value ?? '').trim().toLowerCase();
  const noScheme = s.replace(/^[a-z][a-z0-9+.-]*:\/\//, '');
  const netloc = (noScheme.split('/', 1)[0] || '').split('@').at(-1)
    .replace(/\]:\d+$/, ']').replace(/:\d+$/, '');
  const pathPlus = noScheme.includes('/') ? noScheme.split(/\/(.*)/s)[1] : '';
  const path = (pathPlus || '').split(/[?#]/, 1)[0];
  const digitCount = (s.match(/\d/g) || []).length;
  const length = s.length;
  return {
    url_length: length,
    domain_length: netloc.length,
    path_length: path.length,
    digit_count: digitCount,
    letter_count: (s.match(/[a-z]/g) || []).length,
    special_char_count: (s.match(SPECIAL_CHARS) || []).length,
    digit_ratio: length ? digitCount / length : 0,
    dot_count: (s.match(/\./g) || []).length,
    slash_count: (s.match(/\//g) || []).length,
    entropy: entropy(s),
  };
}

function finding(id, title, detail) { return { id, title, detail }; }
function baseResult(raw) {
  return {
    hostname: null, protocol: null, port: null, normalizedUrl: null,
    findings: [], features: lexicalFeatures(raw),
    verification: { title: 'Verify before opening', detail: 'This is a lexical, offline inspection of the submitted URL; it does not visit the address.' },
    status: 'limited',
    limitations: ['No network request, redirect follow, reputation lookup, or machine-learning prediction is performed.'],
  };
}

/** Analyze a URL without fetching it. Returns plain JSON data and never an anchor/link. */
export function analyzeUrl(raw) {
  const result = baseResult(raw);
  const text = typeof raw === 'string' ? raw : String(raw ?? '');
  if (!text.trim()) {
    result.findings.push(finding('blank', 'URL is blank', 'Enter an HTTP or HTTPS URL to inspect.'));
    result.status = 'review';
    return result;
  }
  if (text.length > MAX_LENGTH) {
    result.findings.push(finding('url-too-long', 'URL exceeds the 8192-character limit', 'The input is rejected before parsing.'));
    result.status = 'review';
    return result;
  }
  if (/[\s\\\u0000-\u001f\u007f]/.test(text)) {
    result.findings.push(finding('invalid-characters', 'URL contains disallowed characters', 'Spaces, control characters, and backslashes are rejected rather than interpreted.'));
    result.status = 'review';
    return result;
  }

  let candidate = text.trim();
  let addedScheme = false;
  const schemelessPort = /^(?:[a-z0-9-]+(?:\.[a-z0-9-]+)+|localhost):\d+(?:[/?#]|$)/i.test(candidate);
  if (schemelessPort || !/^[a-z][a-z0-9+.-]*:/i.test(candidate)) {
    candidate = `https://${candidate}`;
    addedScheme = true;
  }
  let parsed;
  try { parsed = new URL(candidate); } catch {
    result.findings.push(finding('malformed-url', 'URL could not be parsed', 'The hostname, port, or URL syntax is malformed.'));
    result.status = 'review';
    return result;
  }
  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
    result.findings.push(finding('unsupported-scheme', 'Unsupported URL scheme', 'Only HTTP and HTTPS addresses are analyzed.'));
    result.status = 'review';
    return result;
  }
  if (!parsed.hostname) {
    result.findings.push(finding('missing-hostname', 'Hostname is missing', 'An HTTP(S) URL must contain a hostname.'));
    result.status = 'review';
    return result;
  }
  if (!parsed.hostname.includes('.') && parsed.hostname !== 'localhost' && !/^\[[0-9a-f:]+\]$/i.test(parsed.hostname) && !/^\d+(?:\.\d+){3}$/.test(parsed.hostname)) {
    result.findings.push(finding('bare-hostname', 'Hostname is not a domain or IP', 'Bare words are rejected, except for localhost.'));
    result.status = 'review';
    return result;
  }
  const asciiDomain = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.?$/i;
  const validSpecialHost = parsed.hostname === 'localhost' || /^\[[0-9a-f:]+\]$/i.test(parsed.hostname) || /^\d+(?:\.\d+){3}$/.test(parsed.hostname);
  if (!validSpecialHost && !asciiDomain.test(parsed.hostname)) {
    result.findings.push(finding('malformed-hostname', 'Hostname is malformed', 'Hostname labels must use valid ASCII domain syntax after WHATWG canonicalization.'));
    result.status = 'review';
    return result;
  }

  result.hostname = parsed.hostname;
  result.protocol = parsed.protocol.slice(0, -1);
  result.port = parsed.port || null;
  result.normalizedUrl = parsed.href;
  result.features = lexicalFeatures(result.normalizedUrl);
  if (addedScheme) result.findings.push(finding('added-scheme', 'Scheme was added', 'No scheme was supplied, so HTTPS was used for analysis.'));
  if (parsed.protocol === 'http:') result.findings.push(finding('http', 'Unencrypted HTTP', 'HTTP does not provide transport encryption; HTTPS is not guaranteed.'));
  if (parsed.username || parsed.password) result.findings.push(finding('credentials', 'A name before @ is not the destination', `The text before “@” is a username or password, not the website you are visiting. The actual starting hostname is ${parsed.hostname}.`));
  const rawAuthority = candidate.slice(candidate.indexOf('//') + 2).split(/[/?#]/, 1)[0];
  if (/[^\x00-\x7f]/.test(rawAuthority) || /xn--/i.test(parsed.hostname)) result.findings.push(finding('unicode-hostname', 'An internationalized hostname needs a closer look', 'Some letters from different alphabets look alike. Internationalized domains can be legitimate too; the xn-- spelling shown above is how the browser represents them. Compare it with an address you already trust.'));
  const isIp = parsed.hostname.startsWith('[') || /^\d+(?:\.\d+){3}$/.test(parsed.hostname);
  if (isIp) result.findings.push(finding('ip-host', 'IP address used as hostname', 'This URL uses a canonical IP host rather than a named domain; no claim about whether it is private or public is made.'));
  const defaultPort = (parsed.protocol === 'http:' && parsed.port === '80') || (parsed.protocol === 'https:' && parsed.port === '443');
  if (parsed.port && !defaultPort) result.findings.push(finding('unusual-port', 'Non-default port', `The URL explicitly uses port ${parsed.port}.`));
  const labels = parsed.hostname.replace(/^\[|\]$/g, '').split('.');
  if (!isIp && labels.length >= 5) result.findings.push(finding('many-subdomains', 'A hostname with many parts', 'Several dots can make a familiar name appear inside a different address. Compare the full hostname with an address you already know; the number of parts alone does not prove a scam.'));
  if (result.normalizedUrl.length > 200) result.findings.push(finding('long-url', 'Long URL', `The normalized URL is ${result.normalizedUrl.length} characters long.`));
  if (/%[0-9a-f]{2}/i.test(candidate)) result.findings.push(finding('encoded-chars', 'Encoded characters present', 'Percent-encoded bytes can obscure text in the URL and deserve inspection.'));
  const host = parsed.hostname.toLowerCase().replace(/\.$/, '');
  if (SHORTENERS.some(domain => host === domain || host.endsWith(`.${domain}`))) result.findings.push(finding('shortener', 'Known URL-shortener hostname', 'The address uses a recognized shortener domain; this analyzer does not expand it or follow it.'));
  const redirectParams = [...parsed.searchParams.keys()].filter(key => REDIRECT_KEYS.has(key.toLowerCase()));
  if (redirectParams.length) result.findings.push(finding('redirect-parameter', 'Redirect parameter present', `Query parameter${redirectParams.length > 1 ? 's' : ''} ${redirectParams.join(', ')} may point elsewhere; no network request or recursive analysis is performed.`));
  const hiddenDestination = result.findings.some(item => item.id === 'shortener' || item.id === 'redirect-parameter');
  result.verification = hiddenDestination
    ? { title: 'Take a route you already trust', detail: 'The final destination is unknown. Instead of opening or expanding this link, use the organisation’s official app, a saved bookmark, or an address you already know. Confirm the request there, or contact the sender through a separately known number.' }
    : { title: 'Check the request somewhere independent', detail: 'Open the organisation’s official app, use a saved bookmark, or type a website address you already know—not an address suggested by this link. Check whether the same request appears there. For a personal message, contact the sender through a separately known number.' };
  result.status = result.findings.length ? 'review' : 'limited';
  return result;
}
