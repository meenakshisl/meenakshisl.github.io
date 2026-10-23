"""Fetch the publication's public RSS feed; no API plan or token required."""
import json
import re
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
HOST = 'meenakshisl.hashnode.dev'
FEED_URL = f'https://{HOST}/rss.xml'


def parse_feed(body):
    try:
        root = ElementTree.fromstring(body)
    except ElementTree.ParseError as error:
        raise ValueError('Hashnode did not return a valid RSS XML feed') from error
    channel = root.find('channel') if root.tag == 'rss' else None
    if channel is None:
        raise ValueError('Hashnode response is not an RSS feed')
    posts = []
    for item in channel.findall('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        url = urlparse(link)
        if not title or url.scheme != 'https' or url.hostname != HOST:
            raise ValueError('Hashnode feed contains an invalid title or post URL')
        published = item.findtext('pubDate')
        if not published:
            raise ValueError('Hashnode post is missing its publication date')
        tags = [node.text.strip() for node in item.findall('category') if node.text and node.text.strip()]
        description = unescape(re.sub(r'<[^>]*>', '', item.findtext('description') or ''))
        posts.append({
            'date': parsedate_to_datetime(published).date().isoformat(),
            'title': title, 'url': link,
            'topic': tags[0] if tags else 'Blog',
            'publisher': 'Hashnode', 'description': ' '.join(description.split()),
            'tags': tags or ['Blog'],
        })
    return posts


def fetch_posts():
    request = Request(FEED_URL, headers={
        'Accept': 'application/rss+xml, application/xml, text/xml',
        'User-Agent': 'portfolio-writing-sync',
    })
    with urlopen(request, timeout=30) as response:
        return parse_feed(response.read())


if __name__ == '__main__':
    posts = fetch_posts()
    destination = ROOT / 'content/hashnode.json'
    temporary = destination.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(destination)
    print(f'Fetched {len(posts)} Hashnode posts from {FEED_URL}.')
