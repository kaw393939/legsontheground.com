#!/usr/bin/env python3
"""
Quality Validation System for Legs on the Ground
Validates HTML, CSS, and checks accessibility
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import html5lib
from bs4 import BeautifulSoup
import cssutils
import logging

# Suppress cssutils warnings
cssutils.log.setLevel(logging.CRITICAL)


class ValidationResult:
    """Container for validation results"""
    
    def __init__(self, name: str):
        self.name = name
        self.errors = []
        self.warnings = []
        self.info = []
        self.passed = True
    
    def add_error(self, message: str, location: str = None):
        """Add an error"""
        self.errors.append({'message': message, 'location': location})
        self.passed = False
    
    def add_warning(self, message: str, location: str = None):
        """Add a warning"""
        self.warnings.append({'message': message, 'location': location})
    
    def add_info(self, message: str):
        """Add info message"""
        self.info.append(message)
    
    def get_summary(self) -> Dict:
        """Get result summary"""
        return {
            'name': self.name,
            'passed': self.passed,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }


class HTMLValidator:
    """Validates HTML files"""
    
    def __init__(self):
        self.parser = html5lib.HTMLParser(strict=True)
    
    def validate_file(self, html_path: Path) -> ValidationResult:
        """Validate an HTML file"""
        result = ValidationResult(f"HTML: {html_path.name}")
        
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse with html5lib
            try:
                doc = html5lib.parse(content, treebuilder='etree')
                result.add_info(f"Valid HTML5 structure")
            except Exception as e:
                result.add_error(f"HTML5 parsing error: {e}")
                return result
            
            # Parse with BeautifulSoup for detailed checks
            soup = BeautifulSoup(content, 'html5lib')
            
            # Check for basic required elements
            self._check_required_elements(soup, result)
            
            # Check meta tags
            self._check_meta_tags(soup, result)
            
            # Check images
            self._check_images(soup, result)
            
            # Check links
            self._check_links(soup, result)
            
            # Check headings hierarchy
            self._check_headings(soup, result)
            
            # Check accessibility
            self._check_accessibility(soup, result)
            
            # Check SEO basics
            self._check_seo(soup, result)
            
        except Exception as e:
            result.add_error(f"Failed to validate: {e}")
        
        return result
    
    def _check_required_elements(self, soup: BeautifulSoup, result: ValidationResult):
        """Check for required HTML elements"""
        required = {
            'html': 'root element',
            'head': 'head section',
            'title': 'page title',
            'body': 'body section'
        }
        
        for tag, desc in required.items():
            if not soup.find(tag):
                result.add_error(f"Missing required {desc}: <{tag}>")
    
    def _check_meta_tags(self, soup: BeautifulSoup, result: ValidationResult):
        """Check meta tags"""
        # Charset
        charset = soup.find('meta', charset=True) or soup.find('meta', {'http-equiv': 'Content-Type'})
        if not charset:
            result.add_warning("Missing charset declaration")
        
        # Viewport
        viewport = soup.find('meta', {'name': 'viewport'})
        if not viewport:
            result.add_warning("Missing viewport meta tag for responsive design")
        
        # Description
        description = soup.find('meta', {'name': 'description'})
        if not description:
            result.add_warning("Missing meta description for SEO")
        elif description.get('content'):
            desc_len = len(description['content'])
            if desc_len < 50:
                result.add_warning(f"Meta description too short ({desc_len} chars, recommended 50-160)")
            elif desc_len > 160:
                result.add_warning(f"Meta description too long ({desc_len} chars, recommended 50-160)")
    
    def _check_images(self, soup: BeautifulSoup, result: ValidationResult):
        """Check images for alt text and proper attributes"""
        images = soup.find_all('img')
        
        if not images:
            result.add_info("No images found")
            return
        
        missing_alt = []
        missing_dimensions = []
        
        for img in images:
            src = img.get('src', 'unknown')
            
            # Check alt text
            if not img.get('alt'):
                missing_alt.append(src)
            
            # Check dimensions (good for performance)
            if not (img.get('width') and img.get('height')):
                missing_dimensions.append(src)
        
        if missing_alt:
            result.add_error(f"{len(missing_alt)} images missing alt text", 
                           f"Images: {', '.join(missing_alt[:3])}")
        
        if missing_dimensions:
            result.add_warning(f"{len(missing_dimensions)} images missing width/height attributes")
        
        result.add_info(f"Total images: {len(images)}")
    
    def _check_links(self, soup: BeautifulSoup, result: ValidationResult):
        """Check links"""
        links = soup.find_all('a')
        
        empty_links = []
        missing_title = []
        
        for link in links:
            href = link.get('href', '')
            
            # Check for empty href
            if not href:
                empty_links.append(link.get_text()[:30])
            
            # Check external links for security
            if href.startswith('http') and not href.startswith(('http://localhost', 'https://legsontheground.com')):
                # Should have rel="noopener noreferrer"
                rel = link.get('rel', [])
                if 'noopener' not in rel or 'noreferrer' not in rel:
                    result.add_warning(f"External link missing security attributes: {href[:50]}")
        
        if empty_links:
            result.add_warning(f"{len(empty_links)} links with empty href")
        
        result.add_info(f"Total links: {len(links)}")
    
    def _check_headings(self, soup: BeautifulSoup, result: ValidationResult):
        """Check heading hierarchy"""
        headings = []
        for i in range(1, 7):
            for h in soup.find_all(f'h{i}'):
                headings.append((i, h.get_text()[:50]))
        
        if not headings:
            result.add_warning("No headings found")
            return
        
        # Check if starts with h1
        if headings[0][0] != 1:
            result.add_warning(f"Page should start with h1, found h{headings[0][0]}")
        
        # Check for skipped levels
        prev_level = 0
        for level, text in headings:
            if level > prev_level + 1:
                result.add_warning(f"Heading hierarchy skip: h{prev_level} to h{level}")
            prev_level = level
        
        # Count h1s
        h1_count = sum(1 for level, _ in headings if level == 1)
        if h1_count > 1:
            result.add_warning(f"Multiple h1 tags found ({h1_count}), should have only one")
        
        result.add_info(f"Heading structure: {' -> '.join(f'h{l}' for l, _ in headings[:5])}")
    
    def _check_accessibility(self, soup: BeautifulSoup, result: ValidationResult):
        """Check basic accessibility features"""
        # Check for lang attribute
        html_tag = soup.find('html')
        if html_tag and not html_tag.get('lang'):
            result.add_warning("Missing lang attribute on <html> tag")
        
        # Check for skip link
        skip_link = soup.find('a', {'class': 'skip-link'}) or soup.find('a', href='#main-content')
        if not skip_link:
            result.add_warning("Missing skip-to-content link for keyboard navigation")
        
        # Check for ARIA landmarks
        main = soup.find('main')
        if not main:
            result.add_warning("Missing <main> landmark for screen readers")
        
        # Check forms for labels
        inputs = soup.find_all(['input', 'textarea', 'select'])
        for inp in inputs:
            if inp.get('type') not in ['submit', 'button', 'hidden']:
                inp_id = inp.get('id')
                if not inp_id or not soup.find('label', {'for': inp_id}):
                    result.add_warning(f"Form input missing associated label: {inp.get('name', 'unknown')}")
    
    def _check_seo(self, soup: BeautifulSoup, result: ValidationResult):
        """Check SEO basics"""
        # Title length
        title = soup.find('title')
        if title:
            title_text = title.get_text()
            title_len = len(title_text)
            if title_len < 30:
                result.add_warning(f"Title too short ({title_len} chars, recommended 30-60)")
            elif title_len > 60:
                result.add_warning(f"Title too long ({title_len} chars, recommended 30-60)")
            result.add_info(f"Title: {title_text[:60]}")
        
        # Canonical URL
        canonical = soup.find('link', {'rel': 'canonical'})
        if not canonical:
            result.add_warning("Missing canonical URL")
        
        # Open Graph
        og_title = soup.find('meta', {'property': 'og:title'})
        og_desc = soup.find('meta', {'property': 'og:description'})
        og_image = soup.find('meta', {'property': 'og:image'})
        
        if not (og_title and og_desc and og_image):
            result.add_warning("Incomplete Open Graph tags (missing title, description, or image)")


class CSSValidator:
    """Validates CSS files"""
    
    def validate_file(self, css_path: Path) -> ValidationResult:
        """Validate a CSS file"""
        result = ValidationResult(f"CSS: {css_path.name}")
        
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Parse CSS
            sheet = cssutils.parseString(css_content)
            
            # Basic stats
            rule_count = len([r for r in sheet if r.type == r.STYLE_RULE])
            result.add_info(f"Total CSS rules: {rule_count}")
            
            # Check for common issues
            self._check_vendor_prefixes(sheet, result)
            self._check_important_usage(css_content, result)
            self._check_color_contrast(sheet, result)
            
            # File size check
            size_kb = len(css_content.encode('utf-8')) / 1024
            result.add_info(f"File size: {size_kb:.2f} KB")
            
            if size_kb > 100:
                result.add_warning(f"CSS file is large ({size_kb:.2f} KB), consider splitting or minifying")
            
        except Exception as e:
            result.add_error(f"CSS parsing error: {e}")
        
        return result
    
    def _check_vendor_prefixes(self, sheet, result: ValidationResult):
        """Check for outdated vendor prefixes"""
        outdated_prefixes = ['-moz-border-radius', '-webkit-border-radius', '-moz-box-shadow']
        
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for prop in rule.style:
                    if prop.name in outdated_prefixes:
                        result.add_warning(f"Outdated vendor prefix: {prop.name}")
    
    def _check_important_usage(self, css_content: str, result: ValidationResult):
        """Check for excessive !important usage"""
        important_count = css_content.count('!important')
        
        if important_count > 10:
            result.add_warning(f"Excessive use of !important ({important_count} instances)")
        elif important_count > 0:
            result.add_info(f"!important used {important_count} times")
    
    def _check_color_contrast(self, sheet, result: ValidationResult):
        """Basic color usage check"""
        colors_used = set()
        
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for prop in rule.style:
                    if 'color' in prop.name or 'background' in prop.name:
                        colors_used.add(prop.value)
        
        result.add_info(f"Unique colors used: {len(colors_used)}")


class SiteValidator:
    """Main validator for the entire site"""
    
    def __init__(self, docs_dir: Path = Path('docs')):
        self.docs_dir = docs_dir
        self.html_validator = HTMLValidator()
        self.css_validator = CSSValidator()
        self.results = []
    
    def validate_all(self) -> List[ValidationResult]:
        """Validate all files"""
        print("\n🔍 Running Quality Validation...")
        print("=" * 60)
        
        # Validate HTML files
        html_files = list(self.docs_dir.glob('**/*.html'))
        print(f"\n📄 Validating {len(html_files)} HTML files...")
        
        for html_file in html_files:
            print(f"   Checking {html_file.name}...", end=" ")
            result = self.html_validator.validate_file(html_file)
            self.results.append(result)
            
            if result.passed:
                print("✓")
            else:
                print(f"✗ ({len(result.errors)} errors)")
        
        # Validate CSS files
        css_files = list(self.docs_dir.glob('**/*.css'))
        print(f"\n🎨 Validating {len(css_files)} CSS files...")
        
        for css_file in css_files:
            print(f"   Checking {css_file.name}...", end=" ")
            result = self.css_validator.validate_file(css_file)
            self.results.append(result)
            
            if result.passed:
                print("✓")
            else:
                print(f"✗ ({len(result.errors)} errors)")
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate validation report"""
        lines = [
            "\n" + "=" * 60,
            "📊 VALIDATION REPORT",
            "=" * 60,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        
        total_errors = sum(len(r.errors) for r in self.results)
        total_warnings = sum(len(r.warnings) for r in self.results)
        passed_count = sum(1 for r in self.results if r.passed)
        
        lines.extend([
            f"\n📈 Overall Status:",
            f"   Tests Passed: {passed_count}/{len(self.results)}",
            f"   Total Errors: {total_errors}",
            f"   Total Warnings: {total_warnings}",
        ])
        
        # Show details for each validation
        for result in self.results:
            summary = result.get_summary()
            status = "✅" if summary['passed'] else "❌"
            
            lines.append(f"\n{status} {summary['name']}")
            
            if summary['errors']:
                lines.append(f"   Errors ({len(summary['errors'])}):")
                for err in summary['errors'][:3]:  # Show first 3
                    lines.append(f"      • {err['message']}")
                if len(summary['errors']) > 3:
                    lines.append(f"      ... and {len(summary['errors']) - 3} more")
            
            if summary['warnings']:
                lines.append(f"   Warnings ({len(summary['warnings'])}):")
                for warn in summary['warnings'][:3]:
                    lines.append(f"      • {warn['message']}")
                if len(summary['warnings']) > 3:
                    lines.append(f"      ... and {len(summary['warnings']) - 3} more")
            
            if summary['info']:
                for info in summary['info'][:2]:
                    lines.append(f"   ℹ  {info}")
        
        # Overall verdict
        lines.append("\n" + "=" * 60)
        if total_errors == 0:
            lines.append("✅ ALL VALIDATIONS PASSED!")
        else:
            lines.append(f"⚠️  {total_errors} ERRORS NEED ATTENTION")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def save_report(self, output_path: Path):
        """Save validation report to file"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'results': [r.get_summary() for r in self.results],
            'summary': {
                'total_tests': len(self.results),
                'passed': sum(1 for r in self.results if r.passed),
                'failed': sum(1 for r in self.results if not r.passed),
                'total_errors': sum(len(r.errors) for r in self.results),
                'total_warnings': sum(len(r.warnings) for r in self.results),
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {output_path}")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate HTML and CSS quality')
    parser.add_argument('--docs-dir', default='docs', help='Directory to validate')
    parser.add_argument('--save-report', help='Save JSON report to file')
    parser.add_argument('--strict', action='store_true', help='Fail on warnings')
    args = parser.parse_args()
    
    validator = SiteValidator(Path(args.docs_dir))
    results = validator.validate_all()
    
    report = validator.generate_report()
    print(report)
    
    if args.save_report:
        validator.save_report(Path(args.save_report))
    
    # Exit code
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)
    
    if total_errors > 0:
        return 1
    elif args.strict and total_warnings > 0:
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
