# Meenakshi’s portfolio

A small static website for GitHub Pages. No npm packages, framework, or external fonts. Published writing lives in `content/writing.json`; Python generates the homepage.

## Publish to your existing GitHub Pages repository

Repository: https://github.com/meenakshisl/meenakshisl.github.io

Back up your existing repository before replacing its homepage. Copy this folder’s contents into the repository root, including `.github/workflows/pages.yml`. Keep any existing CNAME file if you use a custom domain. In GitHub, choose **Settings → Pages → Source → GitHub Actions**. Commit the files to your default branch. The workflow builds and publishes the site.

The completed homepage is also included, so you can inspect it before deployment.

## Sync Hashnode articles

The Publish portfolio workflow fetches all public posts from
`meenakshisl.hashnode.dev`, merges them with the manual writing list by URL,
and deploys the site. Manual entries take precedence. No API token or automated
commits are needed. A failed fetch stops deployment and leaves the live site intact.

To update immediately: open the repository on GitHub → **Actions → Publish
portfolio → Run workflow**, select the default branch, and click **Run workflow**.
The workflow must first be committed and pushed to the default branch.

Automatic sync runs every other Friday at 08:47 India time (03:17 UTC), starting
30 October 2026. GitHub cron cannot represent a 14-day interval, so a weekly
cadence job skips alternate weeks. GitHub may delay scheduled runs and disables
scheduled workflows in public repositories after 60 days without repository
activity; re-enable the workflow in Actions when needed. Pushes also rebuild and
sync the site, and manual runs always bypass the cadence check.

For local preview with Hashnode posts, run `python3 scripts/fetch_hashnode.py`
before `python3 build.py`. The downloaded `content/hashnode.json` is ignored by Git.

## Add a Medium or other external article

Add an entry to `content/writing.json` (include a comma between entries):

```json
{
  "date": "2026-10-03",
  "title": "Your article title",
  "topic": "AI security",
  "publisher": "Medium",
  "url": "https://medium.com/your-actual-article-url",
  "description": "One short sentence about the article."
}
```

Use the actual publication date. Articles sort newest first automatically. Credit collaborators in the description. For a paywalled article use `"publisher": "Medium · Paywalled"`.

Commit the edit; GitHub Actions updates the homepage. For local preview run `python3 build.py` and `python3 -m http.server 8000` in this folder, then open http://localhost:8000.

## Enable visitor statistics

Create a site in Cloudflare Web Analytics. Copy the public 32-character token from its beacon snippet into `content/settings.json`:

```json
{"cloudflare_analytics_token": "YOUR_ACTUAL_TOKEN"}
```

This is the public analytics token, **not** a Cloudflare API credential. Commit the change. The build adds the Cloudflare beacon automatically. View reports in your Cloudflare dashboard. Analytics are disabled until configured. Visits are approximate; script blockers can prevent recording. No analytics dashboard or tracking token is exposed in the page interface.

## Content and design

Article titles, dates, author credits and links were checked against Endor Labs publications. Bio uses your GitHub profile, previous site, and the interests you described. It does not imply that every analysed vulnerability was discovered by you. No unpublished posts or Medium profile links were invented.

## Pages and résumé

The top navigation opens four separate pages: Home, Writing, Projects, and Résumé. Home presents professional background and selected work. All articles live on Writing; the forensics resource lives on Projects.

Add your actual résumé PDF at `assets/resume.pdf`, then run `python3 build.py` (or commit to trigger GitHub Actions). The Résumé page automatically shows a working download button when the file exists. Until then, it displays an honest availability message. Do not add a placeholder PDF.

## Writing search and tags

Writing supports a keyword search and a tag dropdown, usable together. Search covers titles, descriptions, topics, publishers, and tags; it does not search the full text on external publishers. All entered words must match. Add a `"tags": ["AI security", "LLMs"]` field to an article in `content/writing.json`; the dropdown updates during the build. Existing entries without tags fall back to their topic. Clear filters restores the complete list. With JavaScript disabled, the full article list remains available.
