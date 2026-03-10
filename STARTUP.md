# Vibelyo — Startup & Operations Guide

**Your site:** [https://vibelyo.site](https://vibelyo.site)  
**Repository:** [github.com/abdulrafayKhan-10/vibelyo-new](https://github.com/abdulrafayKhan-10/vibelyo-new)  
**Stack:** Hugo → GitHub Actions → GitHub Pages → Cloudflare → GoDaddy

---

## Table of Contents

1. [One-Time Setup Checklist](#1-one-time-setup-checklist)
2. [Weekly Content Workflow](#2-weekly-content-workflow)
3. [How to Write and Publish a Post Manually](#3-how-to-write-and-publish-a-post-manually)
4. [How to Use the AI Draft Generator](#4-how-to-use-the-ai-draft-generator)
5. [Monetisation Roadmap](#5-monetisation-roadmap)
6. [Site Configuration Reference](#6-site-configuration-reference)
7. [Adding Affiliate Links](#7-adding-affiliate-links)
8. [Troubleshooting](#8-troubleshooting)
9. [Content Topics Queue (Ready to Use)](#9-content-topics-queue)

---

## 1. One-Time Setup Checklist

Complete these before pushing content. Tick each off when done.

### Step 1 — Add GitHub Secrets (enables AI content generation)

> Repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret Name | Where to get it | Priority |
|---|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — free, no credit card | 🔴 Do this first |
| `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) — free signup credits | 🟡 Optional backup |
| `DASHSCOPE_API_KEY` | [dashscope.aliyuncs.com](https://dashscope.aliyuncs.com) — Qwen, has free quota | 🟡 Optional backup |

### Step 2 — Connect Google Search Console

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add property → **URL prefix** → `https://vibelyo.site`
3. Choose **HTML tag** verification method
4. Copy the `content="..."` value from the meta tag they give you
5. Open `hugo.toml` and set:
   ```toml
   googleSiteVerification = "paste-your-code-here"
   ```
6. Commit and push — verification passes automatically

### Step 3 — Submit Your Sitemap

After GSC verification:
1. In Google Search Console → **Sitemaps**
2. Enter: `https://vibelyo.site/sitemap.xml`
3. Submit

### Step 4 — Set Up Google Analytics 4

1. Go to [analytics.google.com](https://analytics.google.com) → Create new property
2. Platform: **Web** → Enter `vibelyo.site`
3. Copy your **Measurement ID** (looks like `G-XXXXXXXXXX`)
4. Open `hugo.toml` and set:
   ```toml
   googleAnalyticsID = "G-XXXXXXXXXX"
   ```
5. Commit and push

### Step 5 — Set Up Social Media Profiles

Create accounts on these platforms with the username **vibelyo** (or closest available):

- [ ] Twitter/X — share new posts, engage with niches
- [ ] Pinterest — best for blogging/online earning content (drives real traffic)
- [ ] LinkedIn — for digital skills and freelancing content

Update the social links in `layouts/partials/footer.html` once created.

---

## 2. Weekly Content Workflow

**Target: 3 posts per week** (roughly 1 per category rotation)

### The weekly routine:

**Monday:** Pick 1 topic from the [Content Topics Queue](#9-content-topics-queue). Run the AI generator (takes 2–3 minutes).

**Tuesday:** Review the AI-drafted PR. Edit for your voice, verify facts, add personal insight.

**Wednesday:** Merge the PR → post goes live automatically.

**Repeat** for posts 2 and 3 across the week.

### Month-by-month milestones:

| Month | Posts live | Expected monthly visitors |
|---|---|---|
| Month 1 | 5 (already done) | < 100 |
| Month 2 | 15 | 100–500 |
| Month 3 | 25 | 500–2,000 |
| Month 4–6 | 40+ | 2,000–10,000 |
| Month 6+ | ongoing | Apply for AdSense |

---

## 3. How to Write and Publish a Post Manually

### Folder structure for a new post:

```
content/
  blogging/
    your-new-post.md    ← create this
```

### Frontmatter template (copy this for every new post):

```yaml
---
title: "Your Post Title Here"
description: "One sentence describing the post — used in Google search results."
date: 2026-03-11T10:00:00+05:00
draft: false
featured: false
categories: ["blogging"]
tags: ["tag one", "tag two", "tag three"]
keywords: "primary keyword, secondary keyword, related term"
showReadingTime: true
---
```

**Category options:** `online-earning` · `freelancing` · `blogging` · `ai-tools` · `digital-skills`

### Publish a post:

```powershell
# In the vibelyo new folder
git add -A
git commit -m "Add: your post title here"
git push origin main
```

GitHub Actions builds and deploys automatically within 2–3 minutes.

### To preview locally before pushing:

```powershell
hugo server
# Open http://localhost:1313 in your browser
```

---

## 4. How to Use the AI Draft Generator

This generates a full draft post and opens a Pull Request for your review automatically.

### Steps:

1. Go to your repository → **Actions** tab
2. Click **"Generate AI Content Draft"** in the left sidebar
3. Click **"Run workflow"** (top right)
4. Fill in the form:

| Field | Example |
|---|---|
| **Category** | `blogging` |
| **Topic** | `how to grow blog traffic to 10k visitors per month` |
| **Title** | `How to Grow Your Blog Traffic to 10,000 Monthly Visitors` |
| **Description** | `Step-by-step guide to growing blog traffic with SEO, Pinterest, and email list building.` |
| **Keywords** | `grow blog traffic, increase blog visitors, SEO for blogs` |
| **Tags** | `blogging tips, SEO, traffic growth` |

5. Click **"Run workflow"** — takes about 2 minutes
6. A Pull Request appears in your repository with the draft post
7. Review the PR → edit directly in GitHub if needed → **Merge**
8. Post goes live within 2–3 minutes

### AI provider used:

The generator tries providers in this order:  
**Groq (llama-3.3-70b)** → **DeepSeek** → **Qwen**

As long as `GROQ_API_KEY` is set, it uses Groq's completely free tier.

---

## 5. Monetisation Roadmap

### Stage 1 — Foundation (now → 25 posts)

- [ ] Complete one-time setup checklist above
- [ ] Publish 3 posts per week consistently
- [ ] Add affiliate links to recommended-tools sections (see section 7)
- [ ] Begin building email list with a free [ConvertKit](https://convertkit.com) account

**Income at this stage:** Minimal to zero. This is the building phase.

### Stage 2 — Early Revenue (25–50 posts, ~month 3–6)

- [ ] Apply for **Google AdSense** at [adsense.google.com](https://adsense.google.com)
  - Requirement: original content, About/Privacy/Contact pages, real traffic
  - After approval, open `hugo.toml` and set:
    ```toml
    adsensePublisherID = "ca-pub-XXXXXXXXXXXXXXXXX"
    adsenseAutoAdsEnabled = true
    ```
- [ ] Join affiliate programs:
  - [Canva Affiliate](https://www.canva.com/affiliates/) — recurring commissions
  - [ConvertKit](https://convertkit.com/affiliate) — 30% recurring
  - [Bluehost](https://www.bluehost.com/affiliates) — $65+ per referral
  - [Semrush](https://www.semrush.com/partner/affiliate) — $200 per sale

**Income at this stage:** $50–$500/month once ads and affiliate links are in place.

### Stage 3 — Scaling (50+ posts, 10k+ monthly visitors)

- [ ] Upgrade from AdSense to [Ezoic](https://www.ezoic.com) (higher RPM)
- [ ] Create a simple digital product (ebook, template, email course)
- [ ] At 50k monthly visitors → apply to [Mediavine](https://www.mediavine.com) for premium ad rates

**Income at this stage:** $500–$5,000/month depending on traffic and niche engagement.

---

## 6. Site Configuration Reference

All site-wide settings live in **`hugo.toml`**.

```toml
# Analytics — set before growing traffic, so you have data from day one
googleSiteVerification = ""    # paste GSC verification code
googleAnalyticsID = ""         # paste GA4 measurement ID (G-XXXXXXXXXX)

# Ads — set ONLY after AdSense approves you
adsensePublisherID = ""        # paste your ca-pub-XXXXXXXXXXXXXXXXX ID
adsenseAutoAdsEnabled = false  # change to true after AdSense approval

# Site info — already configured, no changes needed unless you rebrand
author = "Abdul Rafay Khan"
email = "rafaykhan.biz@gmail.com"
```

---

## 7. Adding Affiliate Links

All recommended tool links live in one file: **`layouts/partials/recommended-tools.html`**

This partial renders at the bottom of every blog post, automatically showing the right tools for each category.

### How to swap a regular link for an affiliate link:

1. Open `layouts/partials/recommended-tools.html`
2. Find the tool entry (e.g., Canva)
3. Replace the URL:

```html
<!-- Before -->
(dict "name" "Canva" "url" "https://www.canva.com" ...)

<!-- After (with affiliate ref) -->
(dict "name" "Canva" "url" "https://www.canva.com/join/your-affiliate-ref" ...)
```

4. Save, commit, push — every post using that tool now sends affiliate traffic

> **The affiliate disclosure note** already appears below the tools grid on every post — you are legally covered.

---

## 8. Troubleshooting

### Site not updating after a push?

1. Go to your repository → **Actions** tab
2. Check if the "Hugo" workflow ran successfully (green tick)
3. If it failed, click on the run to see the error message
4. Most common cause: a markdown file with a syntax error in the frontmatter (check `draft:`, `date:` formatting)

### AI workflow not generating a post?

1. Check that `GROQ_API_KEY` secret is set in GitHub Settings → Secrets
2. Go to Actions → "Generate AI Content Draft" → click the failed run → read the error
3. If Groq fails, add `DEEPSEEK_API_KEY` as a fallback

### Hugo server not starting locally?

```powershell
# Make sure you are in the right folder
Set-Location 'c:\Users\rafay\Desktop\vibelyo new'
hugo version    # should show hugo v0.155+
hugo server
```

### Post showing as draft (not visible on live site)?

Check the frontmatter. It must have:
```yaml
draft: false
```

### Reading time not showing?

The post frontmatter must include:
```yaml
showReadingTime: true
```
Or confirm `showReadingTime = true` is set in `hugo.toml` under `[params]` (it already is).

---

## 9. Content Topics Queue

Ready-to-use topics from `CONTENT_TOPICS.md` — paste directly into the AI generator form.

### Online Earning (7 remaining)

| # | Title to use | Keywords |
|---|---|---|
| 1 | Passive Income Ideas That Actually Work in 2026 | passive income, make money while you sleep, income streams |
| 2 | How to Make Money with Print on Demand | print on demand, Printful, Redbubble, sell merch online |
| 3 | Complete Affiliate Marketing Guide for Beginners | affiliate marketing, how to start affiliate marketing |
| 4 | How to Earn Money from YouTube in 2026 | YouTube monetization, make money YouTube |
| 5 | Dropshipping Guide: Start with Zero Inventory | dropshipping for beginners, Shopify dropshipping |
| 6 | How to Sell Digital Products Online | sell digital products, Gumroad, digital downloads |
| 7 | Best High-Paying Freelance Skills in 2026 | high paying freelance skills, best skills to learn |

### Freelancing (7 remaining)

| # | Title to use | Keywords |
|---|---|---|
| 1 | How to Write a Freelance Proposal That Wins Every Time | freelance proposal, how to write proposals, win clients |
| 2 | Freelance Pricing Guide: How Much to Charge in 2026 | freelance rates, how much to charge, freelance pricing |
| 3 | Best Freelance Platforms Compared: Upwork vs Fiverr vs Toptal | Upwork vs Fiverr, best freelance platforms |
| 4 | How to Build a Freelance Portfolio with No Experience | freelance portfolio, portfolio with no clients |
| 5 | From Side Hustle to Full-Time Freelancer: A Realistic Timeline | go full time freelance, quit job freelancing |
| 6 | How to Get Your First 5 Clients on Upwork | first Upwork client, Upwork for beginners |
| 7 | Freelance Contract Template: What to Include | freelance contract, client agreements |

### Blogging (7 remaining)

| # | Title to use | Keywords |
|---|---|---|
| 1 | How to Do Keyword Research for Free | keyword research free, find keywords, SEO keywords |
| 2 | On-Page SEO Checklist for Blog Posts in 2026 | on-page SEO, SEO checklist, optimize blog post |
| 3 | How to Write Blog Posts That Rank on Google | rank on Google, write SEO blog posts |
| 4 | Best Free Blogging Tools You Should Be Using | free blogging tools, tools for bloggers |
| 5 | How to Build an Email List from Zero | build email list, email list growth, ConvertKit |
| 6 | Blog Monetization: 6 Ways to Make Money from Your Blog | blog monetization, make money blogging |
| 7 | How to Increase Blog Traffic Using Pinterest | Pinterest traffic, Pinterest for bloggers |

### AI Tools (7 remaining)

| # | Title to use | Keywords |
|---|---|---|
| 1 | Best Free AI Writing Tools in 2026 | free AI writing tools, AI content creation |
| 2 | How to Use Claude AI: A Complete Beginner's Guide | Claude AI, Anthropic Claude, AI assistant |
| 3 | Google Gemini vs ChatGPT: Which Is Better? | Gemini vs ChatGPT, best AI chatbot |
| 4 | How to Use AI to Write Blog Posts 10x Faster | AI for blogging, write blog posts with AI |
| 5 | Best AI Tools for Designers and Creatives | AI design tools, Canva AI, Adobe Firefly |
| 6 | Prompt Engineering 101: Write Better AI Prompts | prompt engineering, how to write AI prompts |
| 7 | How to Automate Your Work with AI in 2026 | AI automation, automate with ChatGPT |

### Digital Skills (7 remaining)

| # | Title to use | Keywords |
|---|---|---|
| 1 | How to Learn SEO for Free: A Complete Roadmap | learn SEO free, SEO beginner guide |
| 2 | Canva Tutorial for Beginners: Design Like a Pro | Canva tutorial, Canva for beginners |
| 3 | Google Analytics 4 Explained for Beginners | Google Analytics 4, GA4 tutorial |
| 4 | Excel for Beginners: Most Useful Formulas and Functions | Excel basics, Excel formulas for beginners |
| 5 | How to Start Learning to Code in 2026 | learn to code, coding for beginners |
| 6 | Digital Marketing for Beginners: A Complete Overview | digital marketing beginner, learn digital marketing |
| 7 | How to Build Your Personal Brand Online | personal brand, build personal brand online |

---

## Quick Reference Commands

```powershell
# Preview site locally
hugo server

# Build for production (check for errors)
hugo --minify

# Publish a new or edited post
git add -A
git commit -m "Add: post title here"
git push origin main

# Check build status
# → GitHub → Actions tab → latest run
```

---

*Last updated: March 11, 2026 — Site fully operational at vibelyo.site*
