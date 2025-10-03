# AI Image Manager - Phase 2

## Overview

The AI Image Manager uses OpenAI's Vision API to automatically analyze website images and generate:
- Accessibility-friendly alt text
- Detailed descriptions
- SEO-optimized metadata
- Usage recommendations

## Quick Start

### 1. Setup OpenAI API Key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get a key from: https://platform.openai.com/api-keys
nano .env
```

### 2. Run the Image Analyzer

```bash
# Analyze all images and generate images.yaml
./venv/bin/python image_manager.py

# Dry run (analyze without saving)
./venv/bin/python image_manager.py --dry-run
```

### 3. Review Results

Check the generated file:
```bash
cat content/data/images.yaml
```

## What It Does

### Image Analysis
The AI analyzes each image and generates:
- **Alt Text**: Concise, under 125 characters
- **Description**: Detailed 2-3 sentence description
- **Key Elements**: Visual elements list
- **Use Cases**: Suggested usage contexts
- **Accessibility Notes**: Any accessibility concerns

### Categories Analyzed
- `hero/` - Hero banner images
- `services/` - Service offering images
- `about/` - Team/benefit images
- `social/` - Social media preview images
- `icons/` - Icon graphics
- `misc/` - Logos and other graphics

## Output Structure

The generated `content/data/images.yaml` looks like:

```yaml
images:
  - file: images/hero/hero-main.jpg
    category: hero
    alt_text: "Luxury beachfront property at sunset in Puerto Rico"
    description: "Stunning beachfront property with palm trees at golden hour..."
    key_elements:
      - beachfront property
      - palm trees
      - sunset lighting
    use_cases:
      - Hero banner
      - Property showcase
    accessibility_notes: "High contrast, clear subject"
    dimensions:
      width: 1920
      height: 1080
    size_kb: 245.67
    format: JPEG
    analyzed_at: "2025-10-02T20:45:00"

metadata:
  total_images: 16
  analyzed_at: "2025-10-02T20:45:00"
  categories:
    - hero
    - services
    - about
    - social
    - icons
    - misc
```

## Using Image Data in Templates

Once generated, you can use the image data in your templates:

```jinja2
{# Load image metadata #}
{% set hero_image = images|selectattr('file', 'equalto', 'images/hero/hero-main.jpg')|first %}

{# Use AI-generated alt text #}
<img src="{{ hero_image.file }}" 
     alt="{{ hero_image.alt_text }}"
     width="{{ hero_image.dimensions.width }}"
     height="{{ hero_image.dimensions.height }}">
```

## Costs

OpenAI Vision API pricing (as of Oct 2025):
- gpt-4o-mini: ~$0.00015 per image (low detail)
- 16 images ≈ $0.0024 total

**Very affordable for occasional analysis!**

## Advanced Usage

### Custom API Key
```bash
./venv/bin/python image_manager.py --api-key sk-your-key-here
```

### Analyze Specific Images
Edit `image_manager.py` to filter by category or filename.

### Re-analyze After Changes
Run the analyzer again anytime you add or update images.

## Features

### ✅ Implemented
- [x] OpenAI Vision API integration
- [x] Batch image analysis
- [x] Alt text generation (accessibility)
- [x] Detailed descriptions
- [x] Image metadata (size, dimensions)
- [x] Category-aware analysis
- [x] YAML output format
- [x] Error handling
- [x] Progress tracking
- [x] Summary reports

### 🚧 Future Enhancements
- [ ] Image optimization suggestions
- [ ] Duplicate detection
- [ ] Format conversion recommendations
- [ ] WebP conversion
- [ ] Lazy loading suggestions
- [ ] SEO scoring

## Troubleshooting

### API Key Not Found
```
Error: OpenAI API key not found
```
**Solution**: Create `.env` file with `OPENAI_API_KEY=your-key`

### Rate Limiting
If you hit rate limits, the script will show errors. Wait a moment and retry.

### Invalid API Key
```
Error: Incorrect API key provided
```
**Solution**: Check your API key at https://platform.openai.com/api-keys

### Network Issues
If you get connection errors, check your internet connection.

## Integration with Build System

To use AI-generated image data in your build:

1. **Update build.py** to load images.yaml
2. **Pass image data** to templates
3. **Use in templates** for automated alt text

Example update to `build.py`:

```python
# In load_all_data() method
image_data = self.load_yaml('content/data/images.yaml')
data['images'] = image_data.get('images', [])
```

## Best Practices

### When to Re-analyze
- After adding new images
- After major image updates
- Periodically for SEO improvements

### Editing Generated Content
The AI-generated content is a great starting point. Feel free to:
- Edit alt text for better context
- Enhance descriptions
- Add specific business terminology

### Version Control
- Commit `images.yaml` to version control
- Track changes to image metadata
- Review AI suggestions before deploying

## Performance

- **Analysis Speed**: ~2-3 seconds per image
- **Total Time**: ~30-45 seconds for 16 images
- **Token Usage**: ~200-300 tokens per image
- **Cost**: Less than $0.01 total

## Example Report

```
════════════════════════════════════════════════════════════
📊 IMAGE ANALYSIS REPORT
════════════════════════════════════════════════════════════

Total Images Analyzed: 16
Generated: 2025-10-02 20:45:00

📁 By Category:
   about          : 3 images
   hero           : 1 images
   icons          : 5 images
   misc           : 1 images
   services       : 4 images
   social         : 2 images

💾 Size Analysis:
   Total: 1847.34 KB
   Average: 115.46 KB per image

✅ All images have alt text generated

════════════════════════════════════════════════════════════
```

## Next Steps

1. ✅ Run image analysis
2. ✅ Review generated alt text
3. ✅ Edit any descriptions needed
4. 🔄 Update templates to use image data
5. 🔄 Rebuild site with new metadata
6. 🔄 Test accessibility improvements

## Support

For issues or questions:
- Check [README.md](README.md) for general setup
- See [CONTENT-GUIDE.md](CONTENT-GUIDE.md) for content editing
- Review OpenAI API docs: https://platform.openai.com/docs

---

**Phase 2 Status**: Image Manager Complete ✅  
**Next**: Integrate with build system + Quality Gates (Phase 3)
