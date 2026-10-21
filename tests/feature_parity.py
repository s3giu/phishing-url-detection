"""Run with original research dependencies installed: python tests/feature_parity.py."""
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pandas as pd
from src.features.lexical_features import extract_features_dataframe


class OriginalFeatureParity(unittest.TestCase):
    def test_normalized_urls_match_original_extractor(self):
        urls = [
            'HTTPS://Example.com/a1?x=2',
            'https://user:password@example.com:8080/a-b/c?next=2#x',
            'https://[2001:db8::1]:8080/path',
            'http://0x7f.0.0.1/',
            'https://例え.com/パス?q=✓',
            'example.com:8080/path',
            'https://example.com/?url=https%3A%2F%2Fother.test',
            'https://example.com/',
        ]
        script = "import {analyzeUrl} from './web/analyzer.js'; console.log(JSON.stringify(" + json.dumps(urls) + ".map(analyzeUrl)))"
        output = subprocess.check_output(['node', '--input-type=module', '-e', script], cwd=ROOT, text=True)
        analyzed = json.loads(output)
        original = extract_features_dataframe(pd.DataFrame({'url': [r['normalizedUrl'] for r in analyzed]}))
        for index, result in enumerate(analyzed):
            for name, value in result['features'].items():
                with self.subTest(url=urls[index], feature=name):
                    self.assertTrue(math.isclose(value, float(original.iloc[index][name]), rel_tol=1e-12, abs_tol=1e-12))


if __name__ == '__main__':
    unittest.main(verbosity=2)
