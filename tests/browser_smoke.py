"""Optional browser checks: pip install -r requirements-web-test.txt; python tests/browser_smoke.py.

Starts a temporary loopback-only server. No submitted link is visited.
Set CHROMIUM_EXECUTABLE if your browser is outside Playwright's managed install.
"""
import functools
import http.server
import os
from pathlib import Path
import shutil
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


class BrowserSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(QuietHandler, directory=str(ROOT / 'web'))
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/'
        cls.playwright = sync_playwright().start()
        executable = os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium') or shutil.which('google-chrome')
        cls.browser = cls.playwright.chromium.launch(headless=True, **({'executable_path': executable} if executable else {}))

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 390, 'height': 844})
        self.page = self.context.new_page()
        self.errors = []
        self.requests = []
        self.page.on('pageerror', lambda err: self.errors.append(str(err)))
        self.page.on('request', lambda req: self.requests.append(req.url))
        self.page.goto(self.url, wait_until='networkidle')
        self.initial_requests = list(self.requests)

    def tearDown(self):
        self.assertEqual(self.errors, [], 'Unexpected browser JavaScript errors')
        self.assertEqual(self.requests, self.initial_requests, 'Checking a link must not make network requests')
        self.context.close()

    def check(self, value):
        self.page.get_by_role('textbox', name='Paste a website link').fill(value)
        self.page.get_by_role('button', name='Check this link', exact=True).click()

    def test_misleading_userinfo_shows_actual_host(self):
        self.check('https://accounts.example.com@signin.example.net/verify')
        self.assertEqual(self.page.locator('#hostname').inner_text(), 'signin.example.net')
        self.assertTrue(self.page.locator('#results').is_visible())
        self.assertIn('@', self.page.locator('#findings').inner_text())
        self.assertIn('not a safety verdict', self.page.locator('#result-summary').inner_text())
        self.assertEqual(self.page.locator('#results a').count(), 0)
        self.assertEqual(self.page.evaluate('document.activeElement.id'), 'results')

    def test_ordinary_link_is_not_a_safety_verdict(self):
        self.page.get_by_role('button', name='Ordinary link', exact=True).click()
        self.assertEqual(self.page.locator('#hostname').inner_text(), 'example.com')
        self.assertEqual(self.page.locator('#connection').inner_text(), 'HTTPS · not proof of trust')
        self.assertEqual(self.page.locator('#port').inner_text(), '443 (default)')
        self.assertIn('No obvious warning signs', self.page.locator('#result-title').inner_text())
        self.page.get_by_text('What this check can—and can’t—tell you', exact=True).click()
        self.assertEqual(self.page.locator('#features > div').count(), 10)
        self.assertIn('5.45%', self.page.locator('details').inner_text())
        self.assertIn('not a measured error rate', self.page.locator('details').inner_text())

    def test_http_and_custom_ports(self):
        self.check('http://example.com/')
        self.assertEqual(self.page.locator('#connection').inner_text(), 'HTTP · not encrypted')
        self.assertEqual(self.page.locator('#port').inner_text(), '80 (default)')
        self.check('example.com:8080/path')
        self.assertEqual(self.page.locator('#connection').inner_text(), 'HTTPS · not proof of trust')
        self.assertEqual(self.page.locator('#port').inner_text(), '8080')

    def test_invalid_input_clear_and_stale_result(self):
        for value in ['', 'javascript:alert(1)', 'https://exa mple.com', 'not-a-domain']:
            self.check(value)
            self.assertTrue(self.page.locator('#input-error').is_visible())
            self.assertTrue(self.page.locator('#results').is_hidden())
            self.assertEqual(self.page.locator('#url-input').get_attribute('aria-invalid'), 'true')
        self.check('https://example.com/')
        self.page.get_by_role('textbox', name='Paste a website link').fill('https://changed.example/')
        self.assertTrue(self.page.locator('#results').is_hidden())
        self.page.get_by_role('button', name='Clear', exact=True).click()
        self.assertEqual(self.page.locator('#url-input').input_value(), '')
        self.assertTrue(self.page.locator('#input-error').is_hidden())

    def test_no_navigation_storage_or_html_injection(self):
        self.check('https://example.com/?next=https://other.example/&x=<img%20src=x%20onerror=alert(1)>')
        self.assertTrue(self.page.url.startswith(self.url))
        self.assertEqual(self.page.locator('img, iframe').count(), 0)
        self.assertEqual(self.page.evaluate('localStorage.length + sessionStorage.length'), 0)
        self.assertEqual(self.context.cookies(), [])

    def test_mobile_and_desktop_no_horizontal_overflow(self):
        for width in [320, 390, 768, 1280]:
            self.page.set_viewport_size({'width': width, 'height': 900})
            self.check('https://' + 'a' * 60 + '.' + 'b' * 60 + '.example.com/a-very-long-path')
            self.assertTrue(self.page.locator('#results').is_visible())
            self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), f'Overflow at {width}px')

    def test_shortened_link_and_unicode_hostname(self):
        self.page.get_by_role('button', name='Shortened link', exact=True).click()
        self.assertEqual(self.page.locator('#hostname').inner_text(), 'bit.ly')
        self.assertIn('short', self.page.locator('#findings').inner_text().lower())
        self.check('https://例え.com/')
        self.assertEqual(self.page.locator('#hostname').inner_text(), 'xn--r8jz45g.com')


if __name__ == '__main__':
    unittest.main(verbosity=2)
