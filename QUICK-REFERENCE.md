# 🔧 Quick Reference - Making Changes

## Common Updates

### Change Service Content
1. Edit: `content/data/services.yaml`
2. Build: `python build.py`
3. Test: `python -m http.server 8002 --directory docs`
4. Deploy: `git add . && git commit -m "Updated services" && git push`

### Change Testimonials
1. Edit: `content/data/testimonials.yaml`
2. Build: `python build.py`
3. Deploy: `git add . && git commit -m "Updated testimonials" && git push`

### Update Styling
1. Edit: `static/css/styles.css`
2. Build: `python build.py` (copies to docs/)
3. Test locally
4. Deploy: `git add . && git commit -m "Style updates" && git push`

### Update Hero Section
1. Edit: `templates/sections/hero.html`
2. Build: `python build.py`
3. Deploy: `git add . && git commit -m "Hero update" && git push`

### Add New Section
1. Create: `templates/sections/newsection.html`
2. Include in: `templates/home.html`
3. Add CSS to: `static/css/styles.css`
4. Build and deploy

---

## Fortune 100 Spacing Standards

**Use these values for professional spacing:**

```css
/* Section Padding (tight) */
padding: clamp(2.5rem, 6vh, 3.5rem) 0;

/* Grid Gaps (efficient) */
gap: var(--space-lg);  /* Primary grid spacing */

/* Card Padding (compact) */
padding: var(--space-lg);  /* Not xl, not md - lg is sweet spot */

/* Element Spacing */
margin-bottom: var(--space-sm);  /* Between related items */
margin-bottom: var(--space-md);  /* Between sections */

/* Feature Lists */
padding: 0.375rem 0;  /* Tight item spacing */
gap: var(--space-sm);  /* Icon to text gap */
```

**Don't Use:**
- `var(--space-3xl)` or `var(--space-5xl)` - TOO MUCH SPACE
- Large fixed heights - Use clamp() for responsive
- Excessive margins - Keep it tight and professional

---

## File Structure Quick Reference

```
legsontheground.com/
├── content/
│   ├── config.yaml           # Site-wide config
│   ├── data/
│   │   ├── services.yaml     # Service offerings
│   │   ├── testimonials.yaml # Customer reviews
│   │   ├── why-choose.yaml   # Benefit cards
│   │   └── value-props.yaml  # Value propositions
│   └── pages/
│       └── home.md           # Homepage content
│
├── templates/
│   ├── base.html             # Main layout
│   ├── home.html             # Homepage template
│   ├── components/           # Reusable parts
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── top-bar.html
│   └── sections/             # Page sections
│       ├── hero.html
│       ├── services.html
│       ├── testimonials.html
│       └── ...
│
├── static/                   # Source files
│   ├── css/styles.css        # Main stylesheet
│   ├── js/main.js           # JavaScript
│   ├── images/              # Original images
│   ├── robots.txt           # SEO
│   ├── sitemap.xml          # SEO
│   └── CNAME                # Custom domain
│
├── docs/                     # ⚠️ GENERATED - Don't edit directly!
│   ├── index.html
│   ├── styles.css
│   ├── main.js
│   ├── images/
│   ├── robots.txt
│   ├── sitemap.xml
│   └── CNAME
│
├── build.py                  # Build script
└── .gitignore               # Git ignore rules
```

---

## Git Workflow

```bash
# Check status
git status

# Build site
python build.py

# Test locally
python -m http.server 8002 --directory docs

# Stage changes
git add .

# Commit with good message
git commit -m "Brief description of changes"

# Push to deploy
git push origin main

# Check deployment
# Go to: GitHub → Actions tab
```

---

## Troubleshooting

**Changes not appearing on live site?**
1. Check GitHub Actions completed successfully
2. Wait 1-2 minutes after push
3. Clear browser cache (Ctrl+Shift+R)
4. Check you edited source files, not docs/

**Build fails?**
1. Check YAML syntax in content files
2. Verify template syntax
3. Run: `python build.py` to see errors

**Styling not applying?**
1. Edit `static/css/styles.css` (not docs/)
2. Run `python build.py`
3. Clear cache and refresh

**Images not loading?**
1. Check files in `static/images/`
2. Verify paths in HTML templates
3. Run build to copy to docs/

---

## Maintenance Schedule

**Weekly**:
- Check GitHub Actions for failed deployments
- Review Google Analytics for traffic
- Test site on mobile devices

**Monthly**:
- Update testimonials if new ones available
- Review and update service prices
- Check for broken links
- Run Lighthouse audit

**Quarterly**:
- Review SEO performance (Search Console)
- Update sitemap lastmod dates
- Refresh hero images if needed
- Consider adding new sections

---

## Support Commands

```bash
# Full rebuild
python build.py

# Serve locally
python -m http.server 8002 --directory docs

# Check git status
git status

# View recent commits
git log --oneline -10

# See file changes
git diff

# Undo unstaged changes
git restore <file>

# View docs size
du -sh docs/
```

---

## Design Principles to Maintain

1. **Spacing**: Always use Fortune 100 tight spacing (lg, not xl)
2. **Typography**: Maintain clear hierarchy with bold weights
3. **Colors**: Stick to established color palette
4. **Contrast**: Keep WCAG AAA ratios (12:1 minimum)
5. **Responsive**: Use clamp() for fluid sizing
6. **Performance**: Optimize images before adding

---

**Need Help?** Refer to:
- `DEPLOYMENT-CHECKLIST.md` - Full deployment guide
- `READY-TO-DEPLOY.md` - Deployment summary
- `README.md` - Project overview
