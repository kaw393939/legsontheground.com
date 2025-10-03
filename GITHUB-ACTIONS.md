# GitHub Actions CI/CD

Automated build, validation, and deployment using GitHub Actions.

## Overview

This project uses GitHub Actions to automatically:
1. **Build** the site from YAML content
2. **Validate** HTML/CSS/accessibility  
3. **Deploy** to GitHub Pages
4. **Preview** pull requests before merge

## Workflows

### 1. Deploy Workflow (`deploy.yml`)

**Triggers**: Push to `master` or `main` branch  
**Purpose**: Build, validate, and deploy to production

**Steps**:
1. Checkout code
2. Setup Python 3.12
3. Install dependencies (cached)
4. Build site with validation
5. Upload validation report artifact
6. Deploy to GitHub Pages
7. Post deployment summary

**Status Badge**:
```markdown
![Deploy](https://github.com/YOUR-USERNAME/legsontheground.com/actions/workflows/deploy.yml/badge.svg)
```

### 2. Preview Workflow (`preview.yml`)

**Triggers**: Pull requests to `master` or `main`  
**Purpose**: Validate changes before merge

**Steps**:
1. Checkout PR code
2. Setup Python 3.12
3. Install dependencies
4. Build and validate
5. Generate validation report
6. Upload artifacts (site + report)
7. Comment on PR with results
8. Fail if validation errors found

**Features**:
- 🔍 Automatic validation on every PR
- 💬 Bot comments with results
- 📦 Downloadable preview artifacts
- ❌ Blocks merge if errors found

## Setup Instructions

### 1. Enable GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Under "Build and deployment":
   - Source: **GitHub Actions** (not "Deploy from a branch")
3. Save changes

That's it! The workflow handles everything else.

### 2. Add Status Badge

Add to your README.md:

```markdown
## Status

![Deploy Status](https://github.com/YOUR-USERNAME/legsontheground.com/actions/workflows/deploy.yml/badge.svg)
```

Replace `YOUR-USERNAME` with your GitHub username.

### 3. Configure Branch Protection (Optional)

Protect `master` branch:

1. Go to **Settings** → **Branches**
2. Add rule for `master`
3. Enable:
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Select `validate` check
4. Save

This prevents merging PRs with validation errors.

## Usage

### Automatic Deployment

Just push to master:

```bash
git add .
git commit -m "Update content"
git push origin master
```

GitHub Actions will:
1. Build the site
2. Run validation
3. Deploy to Pages (if validation passes)
4. Update site within ~1 minute

### Pull Request Workflow

1. **Create Branch**:
   ```bash
   git checkout -b feature/new-service
   ```

2. **Make Changes**:
   - Edit YAML files
   - Update templates
   - Modify content

3. **Push and Create PR**:
   ```bash
   git push origin feature/new-service
   ```
   Then create PR on GitHub

4. **Review Results**:
   - Bot comments on PR with validation results
   - Download artifacts to preview changes
   - Fix any errors found

5. **Merge**:
   - Once approved and validated, merge PR
   - Auto-deploys to production

### Manual Deployment

Trigger deployment manually:

1. Go to **Actions** tab
2. Select "Deploy to GitHub Pages"
3. Click **Run workflow**
4. Select branch
5. Click **Run workflow**

## Artifacts

### Validation Report

**File**: `validation-report.json`  
**Retention**: 30 days  
**Contains**:
- Detailed validation results
- Error and warning messages
- Timestamps
- Summary statistics

**Download**:
1. Go to **Actions** tab
2. Click on workflow run
3. Scroll to **Artifacts** section
4. Download `validation-report`

### PR Preview Site

**Files**: Complete built site  
**Retention**: 7 days  
**Contains**:
- All generated HTML
- CSS and JavaScript
- Images

**Download**:
1. Go to PR page
2. Scroll to checks
3. Click "Details" on validation
4. Download `pr-preview-site` artifact
5. Extract and open `index.html`

## Monitoring

### Workflow Status

**View All Runs**:
1. Go to **Actions** tab
2. See history of all builds
3. Click any run for details

**Deployment Status**:
1. **Environments** tab shows active deployments
2. Click "github-pages" for deployment history
3. See URLs and timestamps

### Notifications

Get notified of failures:

1. Go to **Settings** → **Notifications**
2. Enable "Actions"
3. Choose email or GitHub notifications

Or watch the repository:
1. Click **Watch** button
2. Select **Custom** → **Actions**

## Troubleshooting

### Build Fails

**Check logs**:
1. Go to failed workflow run
2. Expand failed step
3. Review error messages

**Common issues**:

**Invalid YAML**:
```
Error: while parsing a block mapping
```
→ Fix YAML syntax in content files

**Missing dependencies**:
```
ModuleNotFoundError: No module named 'X'
```
→ Add to `requirements.txt`

**Validation errors**:
```
❌ Found 3 validation errors
```
→ Check validation report artifact

### Deployment Fails

**Permissions issue**:
```
Error: Resource not accessible by integration
```
→ Check repository settings:
1. **Settings** → **Actions** → **General**
2. Set "Workflow permissions" to "Read and write permissions"
3. Enable "Allow GitHub Actions to create and approve pull requests"

**Pages not configured**:
```
Error: GitHub Pages is not enabled
```
→ Enable Pages with "GitHub Actions" source

### Slow Builds

**Python dependencies caching**:
The workflow uses `cache: 'pip'` to cache dependencies.

**First run**: ~2-3 minutes  
**Subsequent runs**: ~30-60 seconds

### Validation Warnings

**Non-blocking warnings**:
Warnings don't fail the build:
- Long meta descriptions
- Many !important in CSS
- Minor SEO suggestions

**Fix warnings** (optional):
1. Download validation report
2. Review specific warnings
3. Update content/styles
4. Push changes

## Performance

### Build Times

**Average workflow duration**:
- Checkout: ~5 seconds
- Setup Python: ~10 seconds (cached)
- Install deps: ~15 seconds (cached) / ~60 seconds (fresh)
- Build + validate: ~5 seconds
- Deploy: ~20 seconds

**Total**: ~1 minute (with cache)

### Resource Usage

**GitHub Actions limits** (free tier):
- 2,000 minutes/month
- Typical build: ~1 minute
- **~2,000 builds/month free**

This site uses:
- ~1 minute per deploy
- ~100 builds/month estimated
- **Well within free tier**

## Security

### Secrets Management

No secrets required for this project!

If you add external APIs (like OpenAI for images):

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add secret (e.g., `OPENAI_API_KEY`)
3. Reference in workflow:
   ```yaml
   env:
     OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
   ```

### Permissions

Workflows use minimal permissions:

```yaml
permissions:
  contents: read      # Read code
  pages: write        # Deploy to Pages
  id-token: write     # OIDC authentication
```

### Dependencies

All dependencies pinned in `requirements.txt`:
```
jinja2>=3.1.0
pyyaml>=6.0.0
# etc.
```

## Advanced Configuration

### Custom Domain

To use custom domain (e.g., `legsontheground.com`):

1. **Add CNAME file**:
   ```bash
   echo "legsontheground.com" > static/CNAME
   ```

2. **Configure DNS**:
   - Add CNAME record pointing to: `USERNAME.github.io`
   - Or A records for apex domain

3. **Update Pages settings**:
   - Go to **Settings** → **Pages**
   - Enter custom domain
   - Wait for DNS check

Workflow handles CNAME automatically.

### Environment Variables

Add build-time variables:

```yaml
- name: 🏗️ Build site
  run: python build.py --validate
  env:
    SITE_ENV: production
    BUILD_NUMBER: ${{ github.run_number }}
```

Access in Python:
```python
import os
env = os.getenv('SITE_ENV', 'development')
```

### Multiple Environments

Deploy to staging and production:

**staging.yml**:
```yaml
on:
  push:
    branches: [develop]

# Deploy to: https://staging.legsontheground.com
```

**deploy.yml**:
```yaml
on:
  push:
    branches: [master]

# Deploy to: https://legsontheground.com
```

### Scheduled Builds

Rebuild nightly to pull fresh data:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
```

### Slack/Discord Notifications

Add notification step:

```yaml
- name: 📢 Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Build failed: ${{ github.event.head_commit.message }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Workflow Diagram

```
┌──────────────┐
│ Push to Main │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│   Checkout   │────▶│ Setup Python │
└──────────────┘     └──────┬───────┘
                            │
                            ▼
                     ┌──────────────┐
                     │Install Deps  │
                     └──────┬───────┘
                            │
                            ▼
                     ┌──────────────┐
                     │Build & Valid.│
                     └──────┬───────┘
                            │
                    ┌───────┴────────┐
                    │                │
                    ▼                ▼
              ┌─────────┐     ┌─────────┐
              │ Errors? │     │  Pass?  │
              └────┬────┘     └────┬────┘
                   │               │
                   │               ▼
                   │        ┌──────────────┐
                   │        │Deploy Pages  │
                   │        └──────┬───────┘
                   │               │
                   │               ▼
                   │        ┌──────────────┐
                   │        │   Success!   │
                   │        └──────────────┘
                   │
                   ▼
              ┌─────────┐
              │  Fail   │
              └─────────┘
```

## Best Practices

### Commit Messages

Use conventional commits:

```bash
git commit -m "feat: add new service"
git commit -m "fix: correct pricing display"
git commit -m "docs: update README"
git commit -m "style: adjust button colors"
```

Benefits:
- Clear PR history
- Easy to track changes
- Potential for auto-changelog

### Branch Strategy

**Simple workflow**:
- `master`: Production
- `feature/*`: New features
- `fix/*`: Bug fixes

**Process**:
1. Create branch from `master`
2. Make changes
3. Push and create PR
4. Wait for validation
5. Review and merge
6. Auto-deploy to production

### Testing Before Push

Always test locally:

```bash
# Build and validate
python build.py --validate

# Preview
cd docs && python -m http.server 8000
```

Catch issues before they reach CI.

## Migration from Manual Deploys

If currently deploying manually:

1. **Remove old workflow**:
   - Delete `.github/workflows/pages.yml` if exists
   
2. **Update Pages source**:
   - Change from "Deploy from branch"
   - To "GitHub Actions"

3. **First deploy**:
   - Push to master
   - Watch Actions tab
   - Verify deployment

4. **Update README**:
   - Remove manual deploy instructions
   - Add status badge

## Support

### GitHub Actions Documentation
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Pages](https://docs.github.com/en/pages)
- [Actions marketplace](https://github.com/marketplace?type=actions)

### Troubleshooting
- Check **Actions** tab for logs
- Review **validation-report.json** artifact
- Open issue if stuck

---

**Phase 4 Complete** - Fully automated CI/CD pipeline with quality gates
