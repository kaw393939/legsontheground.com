#!/usr/bin/env python3
"""
AI Image Manager for Legs on the Ground
Uses OpenAI Vision API to analyze images and generate metadata
"""

import os
import base64
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ImageAnalyzer:
    """Analyzes images using OpenAI Vision API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.images_dir = Path('static/images')
        self.output_file = Path('content/data/images.yaml')
        
    def encode_image(self, image_path: Path) -> str:
        """Encode image to base64"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def get_image_info(self, image_path: Path) -> Dict:
        """Get basic image information"""
        with Image.open(image_path) as img:
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'size_kb': image_path.stat().st_size / 1024
            }
    
    def analyze_image(self, image_path: Path, context: str = "") -> Dict:
        """
        Analyze image using OpenAI Vision API
        
        Args:
            image_path: Path to image file
            context: Optional context about what the image represents
        
        Returns:
            Dictionary with analysis results
        """
        print(f"   🔍 Analyzing {image_path.name}...")
        
        # Get basic image info
        info = self.get_image_info(image_path)
        
        # Encode image
        base64_image = self.encode_image(image_path)
        
        # Determine context based on directory
        category = image_path.parent.name
        context_prompt = self._get_context_prompt(category, image_path.stem)
        
        # Analyze with OpenAI Vision
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert at analyzing website images for accessibility and SEO. 
                        Generate concise, descriptive alt text that:
                        - Describes the key visual elements
                        - Is specific and actionable
                        - Is under 125 characters
                        - Uses natural language
                        - Focuses on what's relevant for the business context"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""{context_prompt}
                                
Please provide:
1. A concise alt text (under 125 characters)
2. A detailed description (2-3 sentences)
3. Key visual elements (comma-separated list)
4. Suggested use cases for this image
5. Any accessibility concerns

Format as JSON:
{{
    "alt_text": "...",
    "description": "...",
    "key_elements": ["...", "..."],
    "use_cases": ["...", "..."],
    "accessibility_notes": "..."
}}"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "low"  # Use low detail to save tokens
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            # Parse response
            content = response.content[0].text if hasattr(response.content[0], 'text') else response.choices[0].message.content
            
            # Try to extract JSON from response
            try:
                # Find JSON in response (might have markdown code blocks)
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    # Fallback: create structured response from text
                    analysis = {
                        "alt_text": content[:125],
                        "description": content,
                        "key_elements": [],
                        "use_cases": [],
                        "accessibility_notes": "Auto-generated"
                    }
            except json.JSONDecodeError:
                analysis = {
                    "alt_text": f"Image for {category}",
                    "description": content[:200],
                    "key_elements": [],
                    "use_cases": [],
                    "accessibility_notes": "Could not parse structured response"
                }
            
            return {
                'file': str(image_path.relative_to('static')),
                'category': category,
                'alt_text': analysis.get('alt_text', ''),
                'description': analysis.get('description', ''),
                'key_elements': analysis.get('key_elements', []),
                'use_cases': analysis.get('use_cases', []),
                'accessibility_notes': analysis.get('accessibility_notes', ''),
                'dimensions': {
                    'width': info['width'],
                    'height': info['height']
                },
                'size_kb': round(info['size_kb'], 2),
                'format': info['format'],
                'analyzed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"      ⚠️  Error analyzing {image_path.name}: {e}")
            return {
                'file': str(image_path.relative_to('static')),
                'category': category,
                'alt_text': f"Image for {category}",
                'description': "Analysis failed",
                'error': str(e),
                'dimensions': {
                    'width': info['width'],
                    'height': info['height']
                },
                'size_kb': round(info['size_kb'], 2),
                'format': info['format']
            }
    
    def _get_context_prompt(self, category: str, filename: str) -> str:
        """Get context-specific prompt based on image category"""
        contexts = {
            'hero': "This is a hero/banner image for a property concierge service website in Puerto Rico. It should convey trust, professionalism, and tropical appeal.",
            'services': "This image represents a specific service offering (property management, translation, transportation, or coordination services) for a Puerto Rico property concierge business.",
            'about': "This image represents a key benefit or team aspect of the property concierge service, likely showing bilingual capability, local expertise, or experience.",
            'testimonials': "This is an avatar or profile image for a customer testimonial.",
            'social': "This is a social media preview image (Open Graph or Twitter Card) for sharing the website.",
            'icons': "This is an icon used for visual navigation or to represent a service feature.",
            'misc': "This is a logo, branding element, or miscellaneous graphic for the website."
        }
        
        return contexts.get(category, f"This is a {category} image for a property concierge service website.")
    
    def analyze_all_images(self) -> List[Dict]:
        """Analyze all images in the images directory"""
        print("\n🖼️  AI Image Analysis Starting...")
        print("=" * 60)
        
        results = []
        image_files = []
        
        # Find all image files
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']:
            image_files.extend(self.images_dir.rglob(ext))
        
        print(f"\nFound {len(image_files)} images to analyze\n")
        
        for i, image_path in enumerate(sorted(image_files), 1):
            print(f"[{i}/{len(image_files)}] {image_path.relative_to('static')}")
            result = self.analyze_image(image_path)
            results.append(result)
            print(f"      ✓ Alt text: {result.get('alt_text', 'N/A')[:80]}...")
        
        return results
    
    def save_results(self, results: List[Dict]):
        """Save analysis results to YAML file"""
        print(f"\n💾 Saving results to {self.output_file}...")
        
        # Create output structure
        output = {
            'images': results,
            'metadata': {
                'total_images': len(results),
                'analyzed_at': datetime.now().isoformat(),
                'categories': list(set(r['category'] for r in results))
            }
        }
        
        # Ensure directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write YAML
        with open(self.output_file, 'w') as f:
            yaml.dump(output, f, default_flow_style=False, sort_keys=False)
        
        print(f"   ✓ Saved {len(results)} image analyses")
    
    def generate_report(self, results: List[Dict]) -> str:
        """Generate a summary report"""
        report = [
            "\n" + "=" * 60,
            "📊 IMAGE ANALYSIS REPORT",
            "=" * 60,
            f"\nTotal Images Analyzed: {len(results)}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n📁 By Category:",
        ]
        
        # Count by category
        categories = {}
        for r in results:
            cat = r.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items()):
            report.append(f"   {cat:15s}: {count} images")
        
        # Size analysis
        total_size = sum(r.get('size_kb', 0) for r in results)
        avg_size = total_size / len(results) if results else 0
        
        report.extend([
            "\n💾 Size Analysis:",
            f"   Total: {total_size:.2f} KB",
            f"   Average: {avg_size:.2f} KB per image",
        ])
        
        # Accessibility check
        missing_alt = [r for r in results if not r.get('alt_text') or r.get('error')]
        if missing_alt:
            report.append(f"\n⚠️  {len(missing_alt)} images need manual review")
        else:
            report.append("\n✅ All images have alt text generated")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Image Analyzer for website images')
    parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
    parser.add_argument('--dry-run', action='store_true', help='Analyze without saving')
    args = parser.parse_args()
    
    try:
        analyzer = ImageAnalyzer(api_key=args.api_key)
        results = analyzer.analyze_all_images()
        
        if not args.dry_run:
            analyzer.save_results(results)
        
        report = analyzer.generate_report(results)
        print(report)
        
        if not args.dry_run:
            print(f"\n✨ Results saved to: {analyzer.output_file}")
            print("\n🎯 Next Steps:")
            print("   1. Review content/data/images.yaml")
            print("   2. Edit alt text if needed")
            print("   3. Update templates to use image data")
            print("   4. Rebuild site with ./build.sh")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nTo use the AI Image Manager:")
        print("   1. Get an OpenAI API key from https://platform.openai.com/api-keys")
        print("   2. Create a .env file with: OPENAI_API_KEY=your-key-here")
        print("   3. Run: python image_manager.py")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
