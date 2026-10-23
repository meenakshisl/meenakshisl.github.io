import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('sync', Path(__file__).resolve().parents[1] / 'scripts/fetch_hashnode.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class FeedTests(unittest.TestCase):
    def test_realistic_rss(self):
        posts = sync.parse_feed(b'''<rss><channel><item>
        <title><![CDATA[Security & testing]]></title>
        <link>https://meenakshisl.hashnode.dev/test</link>
        <pubDate>Fri, 23 Oct 2026 09:55:43 GMT</pubDate>
        <description><![CDATA[<p>A &amp; B</p>]]></description>
        <category>Security</category></item></channel></rss>''')
        self.assertEqual(posts[0]['date'], '2026-10-23')
        self.assertEqual(posts[0]['description'], 'A & B')
        self.assertEqual(posts[0]['tags'], ['Security'])

    def test_html_response_is_reported_clearly(self):
        with self.assertRaisesRegex(ValueError, 'not an RSS feed'):
            sync.parse_feed(b'<html><body>API retired</body></html>')

    def test_malformed_response(self):
        with self.assertRaisesRegex(ValueError, 'valid RSS XML'):
            sync.parse_feed(b'')

    def test_unexpected_post_url(self):
        with self.assertRaisesRegex(ValueError, 'post URL'):
            sync.parse_feed(b'<rss><channel><item><title>Test</title><link>javascript:alert(1)</link></item></channel></rss>')


if __name__ == '__main__':
    unittest.main()
