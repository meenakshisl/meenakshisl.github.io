from pathlib import Path
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StylesheetCacheTests(unittest.TestCase):
    def test_design_changes_refresh_stylesheet_on_every_page(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copy(ROOT / 'build.py', root / 'build.py')
            shutil.copytree(ROOT / 'content', root / 'content')
            (root / 'assets').mkdir()
            css = root / 'assets/style.css'
            css.write_text('body { color: black; }')
            for entry in json.loads((root / 'content/talks.json').read_text()):
                image = root / entry['image']
                image.parent.mkdir(parents=True, exist_ok=True)
                image.touch()

            def build():
                subprocess.run([sys.executable, str(root / 'build.py')], check=True,
                               capture_output=True)
                versions = [re.search(r'assets/style\.css\?v=([a-f0-9]+)',
                                     page.read_text()).group(1)
                            for page in root.glob('*.html')]
                self.assertEqual(len(versions), 5)
                self.assertEqual(len(set(versions)), 1)
                return versions[0]

            first = build()
            self.assertEqual(first, build())
            css.write_text('body { color: green; }')
            self.assertNotEqual(first, build())
            pages = list(root.glob('*.html'))
            for page in pages:
                html = page.read_text()
                self.assertEqual(html.count("gtag('config', 'G-MGVBVXZXQN')"), 1)
                self.assertIn("window.location.hostname !== 'meenakshisl.github.io'", html)
            settings_path = root / 'content/settings.json'
            settings = json.loads(settings_path.read_text())
            settings['google_analytics_measurement_id'] = ''
            settings_path.write_text(json.dumps(settings))
            build()
            for page in pages:
                self.assertNotIn('googletagmanager.com', page.read_text())
            settings['google_analytics_measurement_id'] = 'invalid</script>'
            settings_path.write_text(json.dumps(settings))
            result = subprocess.run([sys.executable, str(root / 'build.py')],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('valid GA4 measurement ID', result.stderr)
