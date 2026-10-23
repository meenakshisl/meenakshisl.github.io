"""Fetch public Hashnode writing for the deployment; no credentials required."""
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
HOST = 'meenakshisl.hashnode.dev'
QUERY = '''query Posts($host: String!, $after: String) {
  publication(host: $host) {
    posts(first: 50, after: $after) {
      edges { node { title url publishedAt brief tags { name } } }
      pageInfo { hasNextPage endCursor }
    }
  }
}'''


def fetch_posts():
    posts, cursors = [], set()
    after = None
    while True:
        request = Request('https://gql.hashnode.com/', data=json.dumps({
            'query': QUERY, 'variables': {'host': HOST, 'after': after}
        }).encode(), headers={'Content-Type': 'application/json',
                              'User-Agent': 'portfolio-writing-sync'})
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
        if payload.get('errors'):
            raise ValueError(f'Hashnode query failed: {payload["errors"]}')
        publication = payload['data']['publication']
        if publication is None:
            raise ValueError(f'Hashnode publication not found: {HOST}')
        connection = publication['posts']
        for edge in connection['edges']:
            post = edge['node']
            url = urlparse(post['url'])
            if url.scheme != 'https' or url.hostname != HOST:
                raise ValueError('Unexpected Hashnode post URL')
            tags = [tag['name'] for tag in post['tags']]
            posts.append({
                'date': datetime.fromisoformat(post['publishedAt'].replace('Z', '+00:00')).date().isoformat(),
                'title': post['title'], 'url': post['url'],
                'topic': tags[0] if tags else 'Blog',
                'publisher': 'Hashnode', 'description': post.get('brief') or '',
                'tags': tags or ['Blog'],
            })
        page = connection['pageInfo']
        if not page['hasNextPage']:
            return posts
        after = page['endCursor']
        if not after or after in cursors:
            raise ValueError('Hashnode pagination did not advance')
        cursors.add(after)


if __name__ == '__main__':
    posts = fetch_posts()
    destination = ROOT / 'content/hashnode.json'
    destination.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + '\n')
    print(f'Fetched {len(posts)} Hashnode posts.')
