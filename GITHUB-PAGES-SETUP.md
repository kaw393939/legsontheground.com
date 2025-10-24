# GitHub Pages Deployment Guide

## Current Setup ✅

Your site is configured for GitHub Pages deployment with a custom domain:

- **Repository**: `kaw393939/legsontheground.com`
- **Branch**: `main` 
- **Source Folder**: `/docs` 
- **Custom Domain**: `legsontheground.com`
- **CNAME**: Already configured

## GitHub Pages Configuration

1. **Repository Settings**:
   - Go to `Settings` → `Pages`
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
   - Custom domain: `legsontheground.com` (should be pre-filled)

2. **DNS Configuration** (if not already done):
   ```
   Type: CNAME
   Name: www
   Value: kaw393939.github.io
   
   Type: A (for apex domain)
   Name: @
   Values: 
     185.199.108.153
     185.199.109.153  
     185.199.110.153
     185.199.111.153
   ```

## Deployment Workflow

### Automatic Deployment
Every time you push to the `main` branch, GitHub Pages will automatically serve the latest version from the `/docs` folder.

### Manual Deployment Process

1. **Make Content Changes**:
   ```bash
   # Edit files in content/, templates/, or static/
   ```

2. **Build the Site**:
   ```bash
   make build
   # or
   python site.py build
   ```

3. **Test Locally** (optional):
   ```bash
   cd docs && python3 -m http.server 3000
   # Visit http://localhost:3000
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Update site content"
   git push origin main
   ```

5. **Verify**: Visit https://legsontheground.com (may take 1-2 minutes)

## File Structure for GitHub Pages

```
/docs/                    # GitHub Pages serves from here
├── index.html           # Homepage
├── styles.css           # Styles
├── main.js              # JavaScript
├── images/              # All images
├── CNAME                # Custom domain config
├── robots.txt           # SEO
└── sitemap.xml          # SEO
```

## URLs and SEO

- **Live Site**: https://legsontheground.com
- **Sitemap**: https://legsontheground.com/sitemap.xml
- **Robots**: https://legsontheground.com/robots.txt

## Monitoring

- **GitHub Pages Status**: Repository Settings → Pages
- **Build Logs**: Repository → Actions (if using Actions)
- **Domain Status**: Settings → Pages → Custom domain section

## Quick Commands

```bash
# Development workflow
make dev              # Build + serve locally

# Production deployment  
make build            # Build for production
git add .
git commit -m "Deploy update"
git push origin main

# Validate before deploy
make validate         # Check for issues
```

## Troubleshooting

### Site Not Updating
1. Check GitHub Pages build status in repository settings
2. Verify the `/docs` folder contains latest files
3. Clear browser cache
4. Check domain DNS settings

### 404 Errors
1. Ensure `index.html` exists in `/docs` folder
2. Check file paths are relative (no leading `/`)
3. Verify CNAME file contains correct domain

### SSL/HTTPS Issues
1. GitHub Pages automatically provides SSL for custom domains
2. May take 24-48 hours for initial SSL certificate provisioning
3. Check "Enforce HTTPS" is enabled in Pages settings

## Performance

- ✅ Static files served via GitHub's CDN
- ✅ Automatic compression (gzip)
- ✅ Global edge network
- ✅ SSL/HTTPS included
- ✅ 99.9% uptime SLA

---

**Status**: ✅ Ready for deployment  
**Last Updated**: October 24, 2025