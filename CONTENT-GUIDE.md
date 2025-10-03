# Content Editing Guide for Legs on the Ground

## Quick Start

This guide helps non-technical users edit website content without touching code.

## How to Edit Content

### 1. **Site-wide Settings** (`content/config.yaml`)
Edit your contact information, social media links, and business details:

```yaml
site:
  title: "Legs on the Ground"
  phone: "+1 (787) 555-1234"
  email: "contact@legsontheground.com"
  whatsapp: "17875551234"
```

### 2. **Services** (`content/data/services.yaml`)
Add or edit your service offerings:

```yaml
services:
  - id: property-visits
    title: "Property Check-Ins"
    price: "$100"
    badge: "Most Popular"
    description: "We visit your property and send detailed reports"
    features:
      - "Detailed photo & video documentation"
      - "Immediate issue alerts"
```

**To add a new service:** Copy an existing service block and change the details.

### 3. **Testimonials** (`content/data/testimonials.yaml`)
Add customer reviews:

```yaml
testimonials:
  - name: "Michael R."
    location: "Florida → San Juan"
    rating: 5
    quote: "Finally found someone I can trust!"
```

### 4. **Homepage Content** (`content/pages/home.md`)
Edit the hero section, call-to-action text:

```yaml
---
hero:
  title: "Your Trusted Eyes, Ears & Legs in Puerto Rico"
  subtitle: "Professional bilingual property concierge services"
---
```

## Building the Site

After making changes, rebuild the site:

```bash
./build.sh
```

The generated site will be in the `docs/` folder.

## Preview Your Changes

```bash
cd docs
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## What NOT to Edit

- Don't edit files in `docs/` - they're auto-generated
- Don't edit files in `templates/` unless you know HTML
- Don't edit `build.py` unless you know Python

## Getting Help

If something breaks:
1. Check your YAML syntax (indentation matters!)
2. Run `./build.sh` to see error messages
3. Revert your changes using git: `git checkout content/`

## Common Tasks

### Change Phone Number
Edit `content/config.yaml`, find `phone:` and update it.

### Add a New Service
1. Open `content/data/services.yaml`
2. Copy an existing service block
3. Change the `id`, `title`, `description`, etc.
4. Run `./build.sh`

### Update Testimonial
1. Open `content/data/testimonials.yaml`
2. Find the testimonial you want to edit
3. Update the `quote`, `name`, or `location`
4. Run `./build.sh`

### Change Hero Image
1. Add your new image to `static/images/hero/`
2. Open `content/pages/home.md`
3. Change `hero.image:` to your new filename
4. Run `./build.sh`

## YAML Syntax Rules

1. **Indentation matters** - Use 2 spaces (not tabs)
2. **Quotes** - Use quotes around text with special characters: `title: "Welcome to the site!"`
3. **Lists** - Start with a dash:
   ```yaml
   features:
     - First feature
     - Second feature
   ```
4. **Multi-line text** - Use `|`:
   ```yaml
   description: |
     This is a long description
     that spans multiple lines.
   ```

## File Structure

```
content/
├── config.yaml          # Site-wide settings
├── pages/
│   └── home.md         # Homepage content
└── data/
    ├── services.yaml   # Service offerings
    ├── testimonials.yaml  # Customer reviews
    ├── value-props.yaml   # Value propositions
    ├── why-choose.yaml    # Why choose us section
    └── navigation.yaml    # Menu items
```

## Questions?

Contact your developer or check the main README.md for technical details.
