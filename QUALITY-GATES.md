# Quality Gates & Validation

Automated quality validation system that ensures your site meets professional standards before deployment.

## What It Validates

### HTML Validation ✓
- **HTML5 Compliance**: Valid structure and syntax
- **Required Elements**: html, head, title, body tags
- **Meta Tags**: Charset, viewport, description, Open Graph
- **Images**: Alt text, dimensions, proper attributes
- **Links**: Valid hrefs, security attributes for external links
- **Heading Hierarchy**: Proper h1-h6 structure without skips
- **Accessibility**: Lang attribute, skip links, ARIA landmarks, form labels
- **SEO**: Title length, canonical URLs, meta descriptions

### CSS Validation ✓
- **Syntax**: Valid CSS parsing
- **Best Practices**: Vendor prefixes, !important usage
- **Performance**: File size monitoring
- **Color Usage**: Color palette tracking

## Usage

### Run Validation Standalone

```bash
# Validate generated site
python validator.py

# Validate custom directory
python validator.py --docs-dir path/to/site

# Save detailed JSON report
python validator.py --save-report report.json

# Strict mode (fail on warnings)
python validator.py --strict
```

### Integrate with Build

```bash
# Build and validate
python build.py --validate

# Build without validation
python build.py
```

## Validation Levels

### 🔴 Errors (Must Fix)
- Invalid HTML5 structure
- Missing required elements
- Images without alt text
- Empty or broken links
- CSS parsing errors

**Action**: Build fails, must be fixed before deployment

### 🟡 Warnings (Should Fix)
- Meta description length issues
- Title length recommendations
- Missing security attributes
- Excessive !important usage
- Accessibility recommendations

**Action**: Build succeeds but recommendations shown

### ℹ️ Info (For Reference)
- Total image count
- Total link count
- Heading structure overview
- CSS statistics

## Current Site Status

**Last Validation**: All checks passing ✅

```
Tests Passed: 2/2
Total Errors: 0
Total Warnings: 3
```

### Known Warnings
1. **Meta Description**: 194 chars (recommended 50-160)
   - Current: Full business description
   - Action: Consider shortening for better SEO snippet

2. **Page Title**: 65 chars (recommended 30-60)
   - Current: "Legs on the Ground | Property Concierge Services | Washington DC"
   - Action: Optional - works well for branding

3. **CSS !important**: 34 instances
   - Action: Technical debt - consider refactoring utility classes

## Validation Architecture

```
validator.py
├── ValidationResult      # Result container
├── HTMLValidator         # HTML checks
│   ├── _check_required_elements()
│   ├── _check_meta_tags()
│   ├── _check_images()
│   ├── _check_links()
│   ├── _check_headings()
│   ├── _check_accessibility()
│   └── _check_seo()
├── CSSValidator          # CSS checks
│   ├── _check_vendor_prefixes()
│   ├── _check_important_usage()
│   └── _check_color_contrast()
└── SiteValidator         # Orchestrator
    ├── validate_all()
    ├── generate_report()
    └── save_report()
```

## Integration Points

### Build System
- `build.py` includes `--validate` flag
- Runs after successful build
- Can block deployment on errors

### CI/CD Pipeline
```yaml
# In GitHub Actions workflow
- name: Build and Validate
  run: python build.py --validate --strict
```

## Dependencies

```
html5lib>=1.1          # HTML5 parsing
beautifulsoup4>=4.12.0 # HTML analysis
cssutils>=2.9.0        # CSS parsing
```

Install with:
```bash
pip install html5lib beautifulsoup4 cssutils
```

## Output Files

### Console Output
Real-time validation progress with pass/fail indicators

### JSON Report
Detailed machine-readable report saved to `validation-report.json`:

```json
{
  "timestamp": "2025-10-02T23:40:46",
  "results": [
    {
      "name": "HTML: index.html",
      "passed": true,
      "error_count": 0,
      "warning_count": 2,
      "errors": [],
      "warnings": [...]
    }
  ],
  "summary": {
    "total_tests": 2,
    "passed": 2,
    "failed": 0,
    "total_errors": 0,
    "total_warnings": 3
  }
}
```

## Best Practices

### For Developers

1. **Run Validation Locally**: Before pushing changes
   ```bash
   python build.py --validate
   ```

2. **Fix Errors First**: Address all errors before warnings

3. **Review Warnings**: Consider fixing for better quality

4. **Check Reports**: Review JSON reports for trends

### For Content Editors

1. **Image Guidelines**:
   - Always provide meaningful alt text
   - Keep descriptions under 125 characters
   - Use descriptive filenames

2. **Meta Content**:
   - Keep descriptions between 50-160 characters
   - Keep titles between 30-60 characters
   - Include target keywords naturally

3. **Headings**:
   - Use only one h1 per page
   - Don't skip heading levels (h1→h3)
   - Make headings descriptive

## Customization

### Add Custom Checks

Edit `validator.py` to add domain-specific rules:

```python
def _check_custom_rule(self, soup: BeautifulSoup, result: ValidationResult):
    """Your custom validation"""
    # Add your logic
    if condition:
        result.add_error("Your error message")
```

### Adjust Thresholds

Modify warning thresholds in validator classes:

```python
# Title length
if title_len > 70:  # Changed from 60
    result.add_warning(...)
```

## Future Enhancements

- [ ] Performance validation (Core Web Vitals)
- [ ] Link checker (detect broken links)
- [ ] Image optimization checks
- [ ] JavaScript validation
- [ ] Schema.org validation
- [ ] Mobile-friendliness check
- [ ] Security headers validation

## Troubleshooting

### "Module not found" Error
```bash
pip install html5lib beautifulsoup4 cssutils
```

### Validation Takes Too Long
- Use `--docs-dir` to validate specific directories
- Skip validation during development, run before commit

### False Positives
- Review validation logic in `validator.py`
- Customize rules for your needs
- Use JSON report to filter specific warnings

## Learn More

- [HTML5 Validator](https://validator.w3.org/)
- [WCAG Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [CSS Best Practices](https://cssguidelin.es/)
- [SEO Best Practices](https://developers.google.com/search/docs)

---

**Phase 3 Complete** - Quality gates ensure professional standards
