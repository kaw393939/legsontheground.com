# Website Images

This folder contains all professionally generated images for the Legs on the Ground website.

## Quick Reference

| Image | Size | Purpose | Location in Website |
|-------|------|---------|---------------------|
| `hero/hero-main.jpg` | 1536x1024 | Main hero banner | Homepage above fold |
| `icons/icon-property-checkin.png` | 1024x1024 | Property check-in service | Services section |
| `icons/icon-translation.png` | 1024x1024 | Translation service | Services section |
| `icons/icon-transportation.png` | 1024x1024 | Transportation service | Services section |
| `icons/icon-preparation.png` | 1024x1024 | Property preparation service | Services section |
| `icons/icon-property-search.png` | 1024x1024 | Property search service | Services section |
| `services/service-property-visit.jpg` | 1024x1024 | Detailed property visit image | Services/detail pages |
| `services/service-translation.jpg` | 1024x1024 | Detailed translation image | Services/detail pages |
| `services/service-transportation.jpg` | 1024x1024 | Detailed transportation image | Services/detail pages |
| `services/service-coordination.jpg` | 1024x1024 | Detailed coordination image | Services/detail pages |
| `about/about-bilingual.jpg` | 1024x1024 | Bilingual services trust factor | About/Why Choose Us |
| `about/about-local-knowledge.jpg` | 1024x1024 | Local knowledge trust factor | About/Why Choose Us |
| `about/about-experience.jpg` | 1024x1024 | Experience trust factor | About/Why Choose Us |
| `social/og-image.jpg` | 1536x1024 | Social media sharing (Facebook/LinkedIn) | Meta tags |
| `social/twitter-card.jpg` | 1536x1024 | Twitter sharing | Meta tags |
| `misc/logo-icon.png` | 1024x1024 | Logo and favicon | Header, footer, browser tab |

## Folder Structure

```
images/
├── hero/          # Hero/banner images
├── icons/         # Service icons (transparent PNG)
├── services/      # Detailed service photos
├── about/         # About/trust section photos
├── social/        # Social media sharing images
└── misc/          # Logo and other assets
```

## Brand Alignment

All images are generated following the brand guidelines:
- **Colors**: Navy Blue (#0A2540), Warm Coral (#FF6B6B), Soft Teal (#4ECDC4)
- **Tone**: Trustworthy, warm, professional, approachable, Caribbean feel
- **Target**: Mainland US property owners in Puerto Rico (age 45-65)

## Image Specifications

### Hero Images
- **Format**: JPEG, 85% quality
- **Dimensions**: 1536x1024px (3:2 landscape)
- **Purpose**: Large, high-impact visuals above the fold

### Service Icons
- **Format**: PNG with transparent background
- **Dimensions**: 1024x1024px (square)
- **Purpose**: Clean, minimal visual indicators for services
- **Style**: Flat design, 2D vector illustration

### Service Detail Photos
- **Format**: JPEG, 85% quality
- **Dimensions**: 1024x1024px (square)
- **Purpose**: Professional photorealistic images for detailed service explanations

### About Section Photos
- **Format**: JPEG, 85% quality
- **Dimensions**: 1024x1024px (square)
- **Purpose**: Support trust factors and "Why Choose Us" messaging

### Social Media Images
- **Format**: JPEG, 90% quality
- **Dimensions**: 1536x1024px (approximates 1200x630 OG standard)
- **Purpose**: Optimized for Facebook, Twitter, LinkedIn sharing

### Logo/Favicon
- **Format**: PNG with transparent background
- **Dimensions**: 1024x1024px (can be resized)
- **Purpose**: Brand identity across website and browser

## Regenerating Images

If you need to regenerate any images:

```bash
cd /home/kwilliams/is373/legsontheground.com/scripts
./venv/bin/python generate_images.py
```

All prompts are defined in `scripts/generate_images.py` and can be customized.

## Usage in HTML

### Hero Image
```html
<section class="hero" style="background-image: url('images/hero/hero-main.jpg')">
```

### Service Icons
```html
<img src="images/icons/icon-property-checkin.png" alt="Property check-in service">
```

### Social Media Meta Tags
```html
<meta property="og:image" content="https://legsontheground.com/images/social/og-image.jpg">
<meta property="twitter:image" content="https://legsontheground.com/images/social/twitter-card.jpg">
```

### Favicon
```html
<link rel="icon" type="image/png" sizes="32x32" href="images/misc/logo-icon.png">
```

## Image Optimization

All images are already optimized:
- ✅ JPEG images use 85-90% quality (good balance of quality vs file size)
- ✅ PNG icons use transparency for flexible placement
- ✅ Dimensions chosen for optimal display without browser scaling
- ✅ Professional AI-generated content aligned with brand

## Copyright & Usage

All images in this folder are generated specifically for Legs on the Ground and are proprietary to the business. Do not use these images for other projects or purposes without permission.

## Report Files

The `report_*.json` files contain generation metadata including:
- Generation timestamp
- Success/failure status
- Image specifications
- Any errors encountered

These files are useful for debugging and tracking image generation history.
