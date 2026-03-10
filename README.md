# Vibelyo.site - Educational Blogging Platform

A complete, production-ready blogging website built with Hugo static site generator, optimized for Google AdSense approval and educational content delivery.

## AI Draft Generation Workflow

You can generate new draft posts directly from GitHub Actions via:

- `.github/workflows/ai-content-draft.yml`

### Required GitHub Secrets

- `DEEPSEEK_API_KEY` (recommended)
- `DASHSCOPE_API_KEY` (optional fallback for Qwen)

The generator script uses provider fallback order from `scripts/config.json`:

1. `deepseek`
2. `qwen`
3. `ollama`

### What It Does

1. Generates a markdown post draft in `content/<category>/`
2. Adds Hugo frontmatter with `draft: true`
3. Runs basic quality checks (word count, headings, FAQ, keyword hits)
4. Opens a pull request for human review

Script: `scripts/generate_ai_post.py`

## SEO and Monetization Settings

The following are now configurable in `hugo.toml` under `[params]`:

- `googleSiteVerification`
- `googleAnalyticsID`
- `adsensePublisherID`
- `adsenseAutoAdsEnabled`

Set real values, then push to deploy.
