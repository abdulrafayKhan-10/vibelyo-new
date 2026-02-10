# Vibelyo.site - Educational Blogging Platform

A complete, production-ready blogging website built with Hugo static site generator, optimized for Google AdSense approval and educational content delivery.

## 🌟 Features

- **Static Site Generator**: Hugo for fast, secure, and SEO-friendly pages
- **5 Content Categories**: Online Earning, Freelancing, Blogging, AI Tools, Digital Skills
- **AdSense Ready**: Mobile-first design, proper page structure, and legal pages
- **AI Content Automation**: Optional Python script for content generation via Ollama
- **GitHub Pages Deployment**: Automated deployment with GitHub Actions
- **Cloudflare Integration**: CDN and DNS management support
- **SEO Optimized**: Meta tags, Open Graph, clean URLs, and semantic HTML

## 📋 Prerequisites

### Required
- **Git**: Version control
- **Hugo Extended**: v0.121.0 or later ([Download](https://gohugo.io/installation/))
- **GitHub Account**: For hosting and deployment

### Optional (for AI content generation)
- **Python 3.8+**: For automation scripts
- **Ollama**: Local LLM for content generation ([Download](https://ollama.ai/))

## 🚀 Quick Start

### 1. Clone or Download

```bash
# If using Git
git clone <your-repo-url>
cd "vibelyo new"

# Or download and extract the ZIP file
```

### 2. Install Hugo

**Windows (using Chocolatey):**
```powershell
choco install hugo-extended
```

**Windows (Manual):**
1. Download from https://github.com/gohugoio/hugo/releases
2. Extract to a folder (e.g., `C:\Hugo\bin`)
3. Add to PATH environment variable

**Verify installation:**
```bash
hugo version
```

### 3. Run Locally

```bash
# Navigate to project directory
cd "c:\Users\rafay\Desktop\vibelyo new"

# Start Hugo development server
hugo server -D

# Open browser to http://localhost:1313
```

## 📁 Project Structure

```
vibelyo new/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment
├── archetypes/
│   └── default.md              # Template for new posts
├── content/
│   ├── _index.md               # Homepage content
│   ├── about.md                # About page
│   ├── contact.md              # Contact page
│   ├── privacy-policy.md       # Privacy policy (required for AdSense)
│   ├── disclaimer.md           # Disclaimer page
│   ├── terms.md                # Terms and conditions
│   ├── online-earning/         # Category 1
│   ├── freelancing/            # Category 2
│   ├── blogging/               # Category 3
│   ├── ai-tools/               # Category 4
│   └── digital-skills/         # Category 5
├── layouts/
│   ├── _default/
│   │   ├── baseof.html         # Base template
│   │   ├── list.html           # Category pages
│   │   └── single.html         # Blog post pages
│   ├── partials/
│   │   ├── header.html         # Site header
│   │   └── footer.html         # Site footer
│   └── index.html              # Homepage template
├── static/
│   ├── css/
│   │   └── style.css           # Main stylesheet
│   └── CNAME                   # Custom domain configuration
├── scripts/
│   ├── generate_content.py     # AI content generator
│   ├── config.json             # AI script configuration
│   └── requirements.txt        # Python dependencies
├── hugo.toml                   # Hugo configuration
└── README.md                   # This file
```

## ✍️ Creating Content

### Method 1: Manual Creation

```bash
# Create a new post in a specific category
hugo new online-earning/my-new-post.md

# Edit the file in content/online-earning/my-new-post.md
# Change draft: true to draft: false when ready to publish
```

### Method 2: AI-Assisted (Optional)

See [AI Content Generation](#-ai-content-generation-optional) section below.

## 🤖 AI Content Generation (Optional)

The project includes a Python script for AI-assisted content generation using Ollama.

### Setup

1. **Install Ollama**
   - Download from https://ollama.ai/
   - Install and start: `ollama serve`

2. **Pull a model**
   ```bash
   ollama pull llama3
   # or
   ollama pull mistral
   ```

3. **Install Python dependencies**
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

4. **Enable the script**
   - Edit `scripts/config.json`
   - Change `"enabled": false` to `"enabled": true`

### Usage

```bash
cd scripts
python generate_content.py
```

Follow the interactive prompts to generate content.

### ⚠️ Important Safety Notes

- **DISABLED BY DEFAULT**: Script requires manual activation
- **CREATES DRAFTS ONLY**: Never auto-publishes
- **REVIEW REQUIRED**: Always review and edit generated content
- **ADD YOUR VOICE**: Personalize AI-generated content
- **VERIFY FACTS**: Check all statistics and claims
- **RATE LIMITED**: Prevents mass content generation
- **ETHICAL USE**: Use responsibly and transparently

## 🌐 Deployment

### GitHub Pages Setup

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings
   - Navigate to Pages section
   - Source: GitHub Actions
   - The workflow will automatically deploy on push to main

3. **Configure Custom Domain** (Optional)
   - In GitHub Pages settings, add custom domain: `vibelyo.site`
   - Ensure `static/CNAME` contains your domain

### Cloudflare Setup

1. **Add Site to Cloudflare**
   - Log in to Cloudflare
   - Add your domain: vibelyo.site
   - Follow DNS setup instructions

2. **Update GoDaddy Nameservers**
   - Log in to GoDaddy
   - Go to domain settings
   - Change nameservers to Cloudflare's nameservers

3. **Configure DNS in Cloudflare**
   ```
   Type: CNAME
   Name: @
   Target: <your-github-username>.github.io
   Proxy status: Proxied (orange cloud)
   
   Type: CNAME
   Name: www
   Target: <your-github-username>.github.io
   Proxy status: Proxied (orange cloud)
   ```

4. **SSL/TLS Settings**
   - Set SSL/TLS encryption mode to "Full"
   - Enable "Always Use HTTPS"

## 💰 Google AdSense Integration

### Prerequisites for Approval

✅ **Content Requirements:**
- 20-30 quality posts (1,500-2,500 words each)
- Original, valuable content
- Regular posting schedule
- 3-6 months of consistent activity

✅ **Technical Requirements:**
- All essential pages (About, Contact, Privacy, Disclaimer, Terms)
- Mobile-friendly design
- Fast loading times
- Clean navigation
- No broken links

✅ **Traffic Requirements:**
- 5,000-10,000 monthly visitors (recommended)
- Organic traffic from search engines
- Engaged audience

### Adding AdSense Code

1. **Apply for AdSense**
   - Visit https://www.google.com/adsense
   - Submit application
   - Wait for approval (1-2 weeks typically)

2. **Add AdSense Code**
   - Edit `layouts/_default/baseof.html`
   - Uncomment AdSense script in `<head>` section
   - Replace `ca-pub-XXXXXXXXXX` with your publisher ID

3. **Add Ad Units**
   - Uncomment ad placeholders in templates
   - Replace data-ad-slot values with your ad unit IDs
   - Test in production environment

## 📊 SEO Best Practices

### On-Page SEO

- ✅ Unique, descriptive titles (50-60 characters)
- ✅ Compelling meta descriptions (150-160 characters)
- ✅ Proper heading hierarchy (H1 → H2 → H3)
- ✅ Keyword optimization (natural placement)
- ✅ Internal linking between related posts
- ✅ Image alt text
- ✅ Clean, readable URLs

### Content Strategy

1. **Keyword Research**
   - Use Google Keyword Planner
   - Target long-tail keywords
   - Focus on search intent

2. **Content Calendar**
   - Post consistently (2-3 times per week minimum)
   - Plan topics in advance
   - Cover topics comprehensively

3. **Quality Over Quantity**
   - In-depth guides (1,500+ words)
   - Actionable advice
   - Original insights
   - Regular updates

## 🔧 Customization

### Changing Colors

Edit `static/css/style.css`:

```css
:root {
    --primary-color: #2563eb;  /* Change to your brand color */
    --secondary-color: #10b981;
    /* ... other variables */
}
```

### Adding a Logo

1. Add logo image to `static/images/logo.png`
2. Edit `layouts/partials/header.html`
3. Replace text logo with image

### Modifying Navigation

Edit `hugo.toml`:

```toml
[[menu.main]]
  name = "New Page"
  url = "/new-page/"
  weight = 9
```

## 📝 Content Topics Reference

See `CONTENT_TOPICS.md` for a pre-configured list of 40 blog topics (8 per category) to guide your content creation.

## 🛠️ Maintenance

### Regular Tasks

**Weekly:**
- Create 2-3 new blog posts
- Respond to comments (if enabled)
- Check analytics

**Monthly:**
- Update old posts with new information
- Check for broken links
- Review SEO performance
- Backup content

**Quarterly:**
- Audit site performance
- Update legal pages if needed
- Review and update content strategy

### Updating Hugo

```bash
# Check current version
hugo version

# Update Hugo (Windows with Chocolatey)
choco upgrade hugo-extended

# Rebuild site
hugo --gc --minify
```

## 🐛 Troubleshooting

### Hugo Server Won't Start

```bash
# Check if Hugo is installed
hugo version

# Check for port conflicts
hugo server -p 1314

# Clear cache
hugo --gc
```

### Build Errors

```bash
# Verbose output
hugo -v

# Check for draft posts
hugo server -D
```

### GitHub Pages Not Updating

- Check GitHub Actions tab for errors
- Verify workflow file syntax
- Ensure main branch is set correctly
- Check repository settings

## 📚 Resources

### Hugo Documentation
- [Hugo Official Docs](https://gohugo.io/documentation/)
- [Hugo Themes](https://themes.gohugo.io/)
- [Hugo Community Forum](https://discourse.gohugo.io/)

### SEO & Content
- [Google Search Central](https://developers.google.com/search)
- [Moz Beginner's Guide to SEO](https://moz.com/beginners-guide-to-seo)
- [Ahrefs Blog](https://ahrefs.com/blog/)

### AdSense
- [AdSense Help Center](https://support.google.com/adsense)
- [AdSense Policies](https://support.google.com/adsense/answer/48182)

## 📄 License

This project is provided as-is for educational purposes. Feel free to use and modify for your own blogging needs.

## 🤝 Support

For issues or questions:
- Review Hugo documentation
- Check GitHub Issues
- Consult Hugo community forums

---

**Built with ❤️ for educational content creators**

*Remember: Quality content and consistency are the keys to blogging success!*
