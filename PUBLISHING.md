# Replace the portfolio without disturbing project sites

Checked 5 October 2026 against the public repository inventory and forensics deployment workflow.

## Confirmed

- `meenakshisl/meenakshisl.github.io` publishes the root user site.
- `meenakshisl/digital-forensics-notes` is a separate repository with Pages enabled.
- Its `.github/workflows/deploy.yml` builds MkDocs and publishes its own `site` artifact using `actions/deploy-pages`, triggered by pushes to `main`.
- The live URL https://meenakshisl.github.io/digital-forensics-notes/ returned HTTP 200.
- These were the two Pages-enabled repositories in the public inventory. Private repositories and authenticated Pages settings were not accessible.
- The current public root repository contains `css`, `fonts`, `img`, `js`, and two HTML files; it does not contain a `digital-forensics-notes` directory.

## Deployment plan

1. Make a Git snapshot of the existing root repository and record the current Pages source/branch and any custom domain in Settings → Pages.
2. Review any additional old root URLs you want preserved. Files and routes served from the root repository need to be included in the new deployment artifact or redirected; unrelated project sites do not.
3. Copy the new portfolio into the root repository only. Preserve Git history and any CNAME/domain configuration. Do not change the forensics repository or its Pages settings. Do not create a root folder named `digital-forensics-notes`.
4. Disable any old root deployment workflow that would compete with the new workflow, if one has been added since this audit. Choose GitHub Actions as the root repository’s Pages source.
5. Deploy the root repository’s four HTML pages and assets with the provided workflow. It stages only the public files in `_site`.
6. Verify Home, Writing search, Projects, résumé download, and the forensics URL after deployment. Compare additional project URLs against the pre-deployment inventory.
7. If needed, restore the old root files and Pages configuration from the snapshot. No force push or unrelated project changes are necessary.

Changing the root custom domain can also change inherited project-site URLs. Keep the existing domain settings for this replacement.

GitHub documentation: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

Publication is not performed in this session; GitHub write/admin access remains required.
