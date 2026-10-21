import test from 'node:test';
import assert from 'node:assert/strict';
import { analyzeUrl, lexicalFeatures } from '../web/analyzer.js';

test('returns canonical HTTPS for a schemeless domain and warns', () => {
  const r = analyzeUrl('Example.com/path');
  assert.equal(r.hostname, 'example.com'); assert.equal(r.protocol, 'https');
  assert.equal(r.normalizedUrl, 'https://example.com/path');
  assert.ok(r.findings.some(f => f.id === 'added-scheme'));
});
test('credentials are surfaced without exposing a link', () => assert.ok(analyzeUrl('https://login:secret@example.com').findings.some(f => f.id === 'credentials')));
test('Unicode dots canonicalize and punycode is flagged', () => {
  const r = analyzeUrl('https://例え。テスト/path');
  assert.equal(r.hostname, 'xn--r8jz45g.xn--zckzah'); assert.ok(r.findings.some(f => f.id === 'unicode-hostname'));
});
test('IP canonicalization catches hexadecimal/octal IPv4 and IPv6', () => {
  assert.equal(analyzeUrl('http://0x7f.0.0.1').hostname, '127.0.0.1');
  assert.ok(analyzeUrl('http://0x7f.0.0.1').findings.some(f => f.id === 'ip-host'));
  assert.ok(analyzeUrl('https://[::1]:8080').findings.some(f => f.id === 'ip-host'));
});
test('rejects unsupported schemes, malformed ports, spaces, and bare words', () => {
  assert.ok(analyzeUrl('javascript:alert(1)').findings.some(f => f.id === 'unsupported-scheme'));
  assert.ok(analyzeUrl('https://example.com:bad').findings.some(f => f.id === 'malformed-url'));
  assert.ok(analyzeUrl('https://example .com').findings.some(f => f.id === 'invalid-characters'));
  assert.ok(analyzeUrl('example').findings.some(f => f.id === 'bare-hostname'));
});
test('trailing dot and shortener are reported', () => {
  const r = analyzeUrl('https://www.bit.ly./x');
  assert.equal(r.hostname, 'www.bit.ly.'); assert.ok(r.findings.some(f => f.id === 'shortener'));
});
test('redirect parameters are noted without fetching or recursion', () => {
  const r = analyzeUrl('https://example.com/?next=https%3A%2F%2Fevil.test');
  assert.ok(r.findings.some(f => f.id === 'redirect-parameter')); assert.equal(r.normalizedUrl.includes('evil.test'), true);
});
test('XSS-like text remains plain JSON data', () => {
  const r = analyzeUrl('https://example.com/%3Cscript%3Ealert(1)%3C/script%3E');
  assert.ok(r.findings.some(f => f.id === 'encoded-chars')); assert.equal(typeof r.verification.detail, 'string');
  assert.equal(JSON.stringify(r).includes('<script>'), false);
});
test('lexical features match the repository formulas on normalized input', () => {
  const r = analyzeUrl('HTTPS://Example.com/a1?x=2');
  assert.deepEqual(r.features, lexicalFeatures(r.normalizedUrl));
  assert.equal(r.features.url_length, r.normalizedUrl.length);
  assert.equal(r.features.digit_count, 2); assert.equal(r.features.dot_count, 1);
});
test('blank, too-long, and control input are rejected', () => {
  assert.ok(analyzeUrl(' ').findings.some(f => f.id === 'blank'));
  assert.ok(analyzeUrl('a'.repeat(8193)).findings.some(f => f.id === 'url-too-long'));
  assert.ok(analyzeUrl('https://example.com/\u0000').findings.some(f => f.id === 'invalid-characters'));
});

test('schemeless domain ports are accepted without accepting executable schemes', () => {
  const result = analyzeUrl('example.com:8080/path');
  assert.equal(result.hostname, 'example.com');
  assert.equal(result.protocol, 'https');
  assert.equal(result.port, '8080');
  assert.ok(result.findings.some(item => item.id === 'added-scheme'));
  assert.equal(analyzeUrl('javascript:8080').hostname, null);
});

test('verification advice gives an independent route rather than asking users to open links', () => {
  for (const url of ['https://example.com/', 'https://bit.ly/test', 'https://example.com/?next=other']) {
    const result = analyzeUrl(url);
    assert.match(result.verification.detail, /official app/);
    assert.match(result.verification.detail, /separately known number/);
  }
  assert.match(analyzeUrl('https://bit.ly/test').verification.detail, /final destination is unknown/);
});

test('IPv6 with a non-default port preserves closing bracket in feature extraction', () => {
  assert.equal(analyzeUrl('https://[2001:db8::1]:8080/path').features.domain_length, '[2001:db8::1]'.length);
});
