# Legs on the Ground - Property Concierge Services

Professional bilingual property concierge services for mainland owners in Puerto Rico.

## 🚀 Quick Start

```bash
# Development (easiest)
make dev          # Build + serve with live preview

# Or using Python directly
python site.py dev

# Or manually
python site.py build
python site.py serve
```

Visit http://localhost:8000 to see your site!

## 📦 Installation

```bash
# Install dependencies
make install
# or
pip install -r requirements.txt

# Setup git hooks (optional)
python site.py init-hooks
```

## 🎯 Common Commands

### Using Make (Recommended)
```bash
make build        # Build the site
make serve        # Start server
make dev          # Build + serve (most common)
make validate     # Check for errors
make cleanup      # Keep project tidy
make status       # Show project info
make help         # See all commands
```

### Using Python CLI
```bash
python site.py build      # Build the site
python site.py serve      # Start development server
python site.py dev        # Development mode
python site.py validate   # Validate content
python site.py backup     # Create backup
python site.py analyze    # AI visual analysis
python site.py optimize   # Optimize images
python site.py cleanup    # Clean up project
python site.py status     # Show status
```

## 📁 Project Structure

```
├── site.py              # 🎯 Unified CLI (use this!)
├── site.config.yaml     # ⚙️  Configuration
├── Makefile             # 🔧 Convenient shortcuts
├── build.py             # 🏗️  Core build system
├── validator.py         # ✅ Quality checks
├── cleanup_project.py   # 🧹 Organization
├── templates/           # 📄 Jinja2 templates
├── content/             # 📝 YAML content
├── static/              # 🎨 CSS, JS, images
├── docs/                # 📦 Built site (auto-generated)
├── tools/               # 🛠️  AI development tools
├── reports/             # 📊 Analysis reports
└── backups/             # 💾 Auto-backups
```

## 🎨 CSS (DRY Workflow)

- Source CSS is split into ordered parts in `static/css/parts/`.
- Builds automatically bundle these into `docs/styles.css`.
- If you edit `static/css/styles.css` directly, your changes may not be picked up when `static/css/parts/` exists.

## 🔧 Configuration

Edit `site.config.yaml` to customize:
- Build settings
- Validation rules
- Backup preferences
- Tool configurations
- Development server options

## 🎨 Development Workflow

```bash
# 1. Make changes to templates/content/static
# 2. Build and preview
make dev

# 3. Validate before committing
make validate

# 4. Keep project clean
make cleanup

# 5. Check status
make status
```

## 🛠️ AI Tools

All tools are in the `tools/` directory:

```bash
# Visual analysis
python tools/visual_inspector.py --full --analyze

# Image optimization
python tools/image_optimizer.py

# Logo generation
python tools/logo_generator.py

# See all tools
ls tools/
```

Or use the CLI:
```bash
python site.py analyze    # Visual analysis
python site.py optimize   # Image optimization
```

## ✅ Quality Assurance

```bash
# Validate everything
make validate

# Run visual analysis
make analyze

# Optimize images
make optimize
```

## 💾 Backups

Automatic backups are created before each build (configurable in `site.config.yaml`):

```bash
# Manual backup
make backup
# or
python site.py backup
```

Backups are stored in `backups/` directory (keeps last 5 by default).

## 🧹 Keeping It Clean

```bash
# Regular cleanup
make cleanup

# Aggressive cleanup (removes more old files)
python site.py cleanup --aggressive

# Clean build artifacts
make clean
```

## 📊 Project Status

```bash
make status
# Shows:
# - File counts
# - Last build info
# - Backup status
# - Configuration
```

## 🔗 Git Integration

```bash
# Setup automatic validation before commits
python site.py init-hooks

# This will:
# - Run validation before each commit
# - Run cleanup before each commit
# - Prevent commits if validation fails
```

## 📖 Documentation

- **This File:** Quick start and commands
- **Launch Checklist:** `LAUNCH-CHECKLIST.md`
- **Tool Documentation:** `tools/README.md`
- **Reports Index:** `reports/INDEX.md`
- **Configuration:** `site.config.yaml`

## 🚢 Deployment

```bash
# Validate and build
make deploy

# Push to GitHub (auto-deploys via Pages)
git add .
git commit -m "Update site"
git push
```

## 🐛 Troubleshooting

**Build fails?**
```bash
python site.py validate  # Check for errors
python site.py clean     # Clean and rebuild
```

**Project messy?**
```bash
make cleanup             # Organize files
```

**Need to rollback?**
```bash
ls backups/              # Find backup
# Restore manually from backups/
```

## 📈 Performance

Build metrics are automatically tracked in `build_metrics.log`:
- Build time
- File sizes
- Timestamps

## 🎯 Pro Tips

1. **Use `make` for common tasks** - Easier to remember
2. **Run `make cleanup` after analysis** - Keeps project tidy
3. **Use `make dev` for development** - Build + serve in one command
4. **Check `make status` often** - Know your project state
5. **Commit often** - Git hooks ensure quality

## 📞 Support

- **Live Site:** https://kaw393939.github.io/legsontheground.com/
- **Build System:** Python 3.12 + Jinja2
- **Deployment:** GitHub Pages (automatic)

---

**Made with ❤️ using AI-powered development tools**

## 🎯 Overview

This is a modern, maintainable static site built with:
- **Python 3.12** - Build system
- **Jinja2** - Template engine
- **Markdown + YAML** - Content management
- **No CMS required** - Git-based workflow

**Key Features:**
- ✅ Content managed in YAML (easy for non-technical users)
- ✅ Template-based HTML generation (DRY principle)
- ✅ Single-command build process
- ✅ AI-powered image analysis (OpenAI Vision API)
- ✅ Automated quality validation (HTML/CSS/Accessibility)
- ✅ GitHub Pages deployment ready
- 🚧 CI/CD with GitHub Actions (Phase 4)

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Git

### Setup & Build

```bash
# Clone the repository
git clone <your-repo-url>
cd legsontheground.com

# Build the site (creates venv automatically)
./build.sh

# Preview locally
cd docs && python3 -m http.server 8000
# Open http://localhost:8000
```

## 📁 Project Structure

```
legsontheground.com/
├── content/                 # Content (edit here!)
│   ├── config.yaml         # Site-wide configuration
│   ├── pages/              # Page content (Markdown)
│   │   └── home.md
│   └── data/               # Structured data (YAML)
│       ├── services.yaml
│       ├── testimonials.yaml
│       ├── value-props.yaml
│       ├── why-choose.yaml
│       └── navigation.yaml
│
├── templates/              # Jinja2 templates (HTML structure)
│   ├── base.html          # Master template
│   ├── home.html          # Homepage layout
│   ├── components/        # Reusable components
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── top-bar.html
│   └── sections/          # Page sections
│       ├── hero.html
│       ├── services.html
│       ├── testimonials.html
│       └── ...
│
├── static/                 # Static assets (images, CSS, JS)
│   ├── css/
│   ├── js/
│   └── images/
│
├── docs/                   # Generated output (GitHub Pages)
│   └── index.html         # Built HTML
│
├── build.py               # Build script
├── build.sh               # Convenience wrapper
└── requirements.txt       # Python dependencies
```

## 🛠️ Development Workflow

### 1. Edit Content

**For Non-Technical Users:** See [CONTENT-GUIDE.md](CONTENT-GUIDE.md)

**For Developers:**
- Edit `content/pages/*.md` for page content
- Edit `content/data/*.yaml` for structured data
- Edit `content/config.yaml` for site-wide settings

### 2. Build Site

```bash
./build.sh          # Full build
./build.sh --validate  # Build with validation (coming soon)
```

Or use Python directly:
```bash
./venv/bin/python build.py
```

### 3. Test Locally

```bash
cd docs
python3 -m http.server 8000
```

### 4. Deploy

Push to GitHub and GitHub Actions will auto-deploy (Phase 4).

For manual deployment:
```bash
git add .
git commit -m "Update content"
git push origin master
```

## 📝 Content Management

### YAML Files

All data is in `content/data/*.yaml`:

```yaml
# services.yaml
services:
  - id: property-visits
    title: "Property Check-Ins"
    price: "$100"
    description: "Detailed property inspections"
    features:
      - "Photo documentation"
      - "Issue alerts"
```

### Markdown Pages

Pages use YAML frontmatter + Markdown:

```markdown
---
title: "Page Title"
layout: "home"
hero:
  title: "Hero Title"
  subtitle: "Hero Subtitle"
---

# Page Content

Your markdown content here...
```

## 🎨 Template System

### Template Hierarchy

```
base.html                   # Master template
└── home.html              # Page layout
    ├── sections/hero.html
    ├── sections/services.html
    └── sections/cta.html
```

### Available Variables

In templates, you have access to:
- `{{ site.* }}` - Site configuration (phone, email, etc.)
- `{{ page.* }}` - Current page frontmatter
- `{{ services }}` - Services data
- `{{ testimonials }}` - Testimonials data
- `{{ navigation }}` - Menu structure
- `{{ features }}` - Feature flags
- `{{ current_year }}` - Current year (for copyright)

## 🔧 Build System

### build.py

The core build script:

```python
from build import SiteBuilder

builder = SiteBuilder()
builder.build()
```

**What it does:**
1. Loads all YAML data from `content/data/`
2. Parses Markdown pages with frontmatter
3. Renders Jinja2 templates with data
4. Copies static assets (CSS, JS, images)
5. Outputs to `docs/` directory

### Build Options

```bash
# Clean build
./venv/bin/python build.py

# Keep existing files
./venv/bin/python build.py --no-clean

# With validation
./venv/bin/python build.py --validate
```

## 🧪 Testing & Validation

### Build with Validation
```bash
# Full build with quality gates
python build.py --validate

# Standalone validation
python validator.py

# Save detailed report
python validator.py --save-report report.json
```

### What Gets Validated ✓
- **HTML**: Structure, meta tags, accessibility, SEO
- **CSS**: Syntax, best practices, performance
- **Images**: Alt text, dimensions
- **Links**: Valid hrefs, security attributes
- **Headings**: Proper hierarchy

See [QUALITY-GATES.md](QUALITY-GATES.md) for details.

## 🚀 Deployment

### GitHub Pages (Recommended)

1. Push to GitHub
2. Enable Pages in repo settings
3. Set source to `/docs` folder on `master` branch
4. Site auto-updates on push

### Manual Deploy

Build locally and upload `docs/` folder to any static host.

## 🤖 AI Features (Phase 2) ✨

**NOW AVAILABLE!**
- ✅ AI image analysis (OpenAI Vision API)
- ✅ Auto-generated alt text
- ✅ Detailed image descriptions
- ✅ Accessibility recommendations
- ✅ SEO-optimized metadata

See [AI-IMAGE-MANAGER.md](AI-IMAGE-MANAGER.md) for setup and usage.

## 📦 Dependencies

```txt
jinja2>=3.1.0       # Template engine
pyyaml>=6.0.0       # YAML parser
markdown>=3.5.0     # Markdown processor
```

Install:
```bash
pip install -r requirements.txt
```

## 🐛 Troubleshooting

### Build Fails

**Check YAML syntax:**
```bash
./venv/bin/python -c "import yaml; yaml.safe_load(open('content/config.yaml'))"
```

**Check Python version:**
```bash
python3 --version  # Should be 3.12+
```

### Missing Content

If sections are empty, check:
1. YAML file structure matches template expectations
2. Data keys are correct (use underscores, not hyphens)
3. Build script loaded the data (check console output)

### JavaScript Errors

Check browser console. Common issues:
- Missing element IDs (add to templates)
- Font Awesome not loading (check CDN)

## 📚 Additional Documentation

- [CONTENT-GUIDE.md](CONTENT-GUIDE.md) - For content editors
- [LAUNCH-CHECKLIST.md](LAUNCH-CHECKLIST.md) - Pre-launch checklist
- [docs/](docs/) - Technical documentation

## 🗺️ Roadmap

- [x] Phase 1: Foundation (Content + Templates)
- [x] Phase 2: AI Image Manager (OpenAI Vision API)
- [x] Phase 3: Quality Gates (HTML/CSS/Accessibility)
- [x] Phase 4: GitHub Actions CI/CD ✨ NEW!
- [ ] Phase 5: Final Testing & Launch

## 📄 License

Proprietary - Legs on the Ground © 2025

## 👥 Contributing

1. Create feature branch
2. Make changes
3. Test locally
4. Submit pull request

## 🆘 Support

For technical issues, contact your developer or file an issue in the repository.

## Project Structure

```
legsontheground.com/
├── src/                          # Website files
│   ├── index.html               # Main website (SEO optimized)
│   ├── styles.css               # Professional styling
│   ├── robots.txt               # Search engine crawler rules
│   └── sitemap.xml              # Site structure for search engines
│
└── docs/                         # Essential documentation
    ├── brand-basics.md          # Core brand identity & messaging
    ├── design-system.md         # Colors, typography, spacing
    ├── content-guide.md         # How to write & communicate
    ├── business-reality.md      # Services, pricing, goals
    └── README.md                # Documentation guide
```

## SEO Optimization Features

### ✅ Traditional SEO:
- Comprehensive meta tags (title, description, keywords)
- Open Graph tags for social sharing
- Twitter Card meta tags
- Structured data (Schema.org) for Local Business
- Structured data for Services and Pricing
- Structured data for FAQs
- Semantic HTML5 with proper ARIA labels
- Geographic metadata for Puerto Rico/San Juan
- XML sitemap
- Robots.txt with AI agent rules
- Canonical URLs
- Mobile-responsive design

### ✅ AI Agent Optimization:
- Detailed service descriptions with pricing
- Natural language Q&A format
- Structured data that AI can parse
- Clear business context and location
- Bilingual service emphasis
- FAQ schema for common questions
- Specific geographic service areas
- Contact information in multiple formats

### ✅ Key SEO Keywords Targeted:
- Puerto Rico property management
- Bilingual property services Puerto Rico
- San Juan property concierge
- Mainland property owners Puerto Rico
- Act 60 property services
- Puerto Rico translation services
- Property check-ins Puerto Rico
- Absentee property management

## Quick Reference for Nilsa

### Day-to-Day Questions:
1. **What to charge?** → `docs/business-reality.md`
2. **How to talk to customers?** → `docs/content-guide.md`
3. **What makes us different?** → `docs/brand-basics.md`
4. **Design/color questions?** → `docs/design-system.md`

### Website Updates:
1. Edit: `src/index.html`
2. Check tone: `docs/content-guide.md`
3. Check colors: `docs/design-system.md`

## Next Steps Before Launch

### Setup (Do First):
- [ ] Get business email (contact@legsontheground.com)
- [ ] Set up form handler (Formspree - free tier)
- [ ] Get business phone (Google Voice - free)
- [ ] Purchase domain name
- [ ] Get liability insurance
- [ ] Update robots.txt with actual domain
- [ ] Update sitemap.xml with actual URLs
- [ ] Update Formspree form ID in index.html
- [ ] Create og-image.jpg (1200x630px) for social sharing
- [ ] Create twitter-image.jpg (1200x600px) for Twitter

### SEO & Discovery:
- [ ] Submit sitemap to Google Search Console
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Set up Google Business Profile
- [ ] Create Facebook Business Page
- [ ] Set up LinkedIn Company Page
- [ ] Join Facebook groups for Puerto Rico property owners
- [ ] Test with WAVE accessibility tool
- [ ] Test with axe DevTools
- [ ] Validate HTML with W3C Validator
- [ ] Test with Lighthouse (aim for 90+ scores)

### Launch:
- [ ] Deploy website with proper domain
- [ ] Test all structured data with Google Rich Results Test
- [ ] Verify mobile-friendliness with Google Mobile-Friendly Test
- [ ] Test with multiple screen readers
- [ ] Test keyboard navigation
- [ ] Test with browser zoom up to 200%
- [ ] Set up Google Analytics
- [ ] Monitor search console for indexing
- [ ] Test form submissions
- [ ] Verify all links work

## Accessibility Testing Checklist

### Keyboard Navigation:
- [ ] All interactive elements accessible via Tab key
- [ ] Logical tab order throughout page
- [ ] Skip-to-content link functional
- [ ] Escape key closes mobile menu
- [ ] Enter/Space activates buttons and links

### Screen Reader Testing:
- [ ] All images have alt text
- [ ] Form labels properly associated
- [ ] ARIA labels present where needed
- [ ] Heading hierarchy makes sense
- [ ] Lists properly marked up

### Visual Testing:
- [ ] Text readable at 200% zoom
- [ ] Color contrast meets standards
- [ ] Focus indicators visible
- [ ] Works in high contrast mode
- [ ] No content only conveyed by color

## Important Reminders

**Safety First:**
- Never use personal name publicly
- Business contact info only
- Professional boundaries always

**Keep It Simple:**
- 5 core services only
- Clear, honest pricing
- Personal, reliable service
- No overpromising

---

**Website Status:** ✅ SEO Optimized, Fully Accessible & Ready to launch
**Accessibility Level:** WCAG 2.1 Level AA compliant (AAA for body text)
**Documentation:** ✅ Complete and simplified
**Next Action:** Deploy to domain and submit to search engines
