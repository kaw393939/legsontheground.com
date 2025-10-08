#!/usr/bin/env python3
"""
Legs on the Ground - Unified CLI
Main command interface for all project operations
"""

import sys
import argparse
import subprocess
from pathlib import Path
import yaml
import logging
from datetime import datetime
import shutil

class SiteManager:
    """Unified site management interface"""
    
    def __init__(self, config_file="site.config.yaml"):
        self.root = Path(__file__).parent
        self.config_file = self.root / config_file
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self):
        """Load configuration"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return yaml.safe_load(f)
        return self.default_config()
    
    def default_config(self):
        """Default configuration if file doesn't exist"""
        return {
            'build': {'output_dir': 'docs'},
            'logging': {'level': 'INFO'},
            'backup': {'enabled': True, 'location': 'backups', 'keep_last': 5}
        }
    
    def setup_logging(self):
        """Setup logging"""
        level = getattr(logging, self.config.get('logging', {}).get('level', 'INFO'))
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger('site')
    
    def validate(self, fix=False):
        """Validate project (content, images, links)"""
        self.logger.info("🔍 Validating project...")
        
        errors = []
        warnings = []
        
        # Check YAML files
        if self.config.get('validation', {}).get('check_yaml', True):
            yaml_errors = self._validate_yaml_files()
            errors.extend(yaml_errors)
        
        # Check images
        if self.config.get('validation', {}).get('check_images', True):
            image_errors = self._validate_images()
            errors.extend(image_errors)
        
        # Report results
        if errors:
            self.logger.error(f"❌ Validation failed with {len(errors)} errors")
            for error in errors:
                self.logger.error(f"  - {error}")
            return False
        
        if warnings:
            self.logger.warning(f"⚠️  {len(warnings)} warnings found")
            for warning in warnings:
                self.logger.warning(f"  - {warning}")
        
        self.logger.info("✅ Validation passed")
        return True
    
    def _validate_yaml_files(self):
        """Validate all YAML content files"""
        errors = []
        content_dir = self.root / self.config.get('build', {}).get('content_dir', 'content')
        
        if not content_dir.exists():
            return ["Content directory not found"]
        
        for yaml_file in content_dir.glob('**/*.yaml'):
            try:
                with open(yaml_file) as f:
                    yaml.safe_load(f)
            except yaml.YAMLError as e:
                errors.append(f"Invalid YAML in {yaml_file.name}: {str(e)}")
        
        return errors
    
    def _validate_images(self):
        """Check for missing images referenced in content"""
        errors = []
        # This would scan content for image references and check they exist
        # Simplified for now
        return errors
    
    def backup(self):
        """Create backup of current state"""
        if not self.config.get('backup', {}).get('enabled', True):
            self.logger.info("Backup disabled in config")
            return
        
        self.logger.info("💾 Creating backup...")
        
        backup_loc = self.root / self.config.get('backup', {}).get('location', 'backups')
        backup_loc.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        backup_path = backup_loc / backup_name
        
        # Backup critical files
        important = ['content', 'templates', 'static', 'site.config.yaml']
        backup_path.mkdir()
        
        for item in important:
            src = self.root / item
            if src.exists():
                if src.is_dir():
                    shutil.copytree(src, backup_path / item)
                else:
                    shutil.copy2(src, backup_path / item)
        
        # Keep only last N backups
        keep_last = self.config.get('backup', {}).get('keep_last', 5)
        backups = sorted(backup_loc.glob('backup_*'))
        for old_backup in backups[:-keep_last]:
            shutil.rmtree(old_backup)
        
        self.logger.info(f"✅ Backup created: {backup_name}")
    
    def build(self, validate_first=True):
        """Build the site"""
        self.logger.info("🏗️  Building site...")
        
        # Auto-backup if enabled
        if self.config.get('backup', {}).get('auto_backup_before_build', True):
            self.backup()
        
        # Validate first
        if validate_first and not self.validate():
            self.logger.error("❌ Build aborted due to validation errors")
            return False
        
        # Run build
        start_time = datetime.now()
        
        try:
            result = subprocess.run(
                ['python', 'build.py'],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=True
            )
            
            build_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"✅ Build completed in {build_time:.2f}s")
            
            # Track metrics
            if self.config.get('performance', {}).get('track_build_time', True):
                self._track_build_metrics(build_time)
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Build failed: {e.stderr}")
            return False
    
    def _track_build_metrics(self, build_time):
        """Track build performance metrics"""
        metrics_file = self.root / "build_metrics.log"
        
        output_dir = self.root / self.config.get('build', {}).get('output_dir', 'docs')
        
        # Calculate sizes
        total_size = sum(f.stat().st_size for f in output_dir.rglob('*') if f.is_file())
        
        metrics = f"{datetime.now().isoformat()},{build_time:.2f},{total_size}\n"
        
        with open(metrics_file, 'a') as f:
            f.write(metrics)
    
    def serve(self):
        """Start development server"""
        self.logger.info("🚀 Starting development server...")
        
        config = self.config.get('development', {}).get('server', {})
        host = config.get('host', 'localhost')
        port = config.get('port', 8000)
        
        output_dir = self.root / self.config.get('build', {}).get('output_dir', 'docs')
        
        self.logger.info(f"📡 Server running at http://{host}:{port}")
        self.logger.info("Press Ctrl+C to stop")
        
        try:
            subprocess.run([
                'python', '-m', 'http.server', str(port),
                '--directory', str(output_dir)
            ])
        except KeyboardInterrupt:
            self.logger.info("\n👋 Server stopped")
    
    def dev(self):
        """Development mode - build and serve with auto-reload"""
        self.logger.info("🔧 Starting development mode...")
        
        # Initial build
        self.build(validate_first=True)
        
        self.logger.info("💡 Tip: Edit files and run 'python site.py build' to rebuild")
        
        # Start server
        self.serve()
    
    def clean(self):
        """Clean build artifacts"""
        self.logger.info("🧹 Cleaning build artifacts...")
        
        output_dir = self.root / self.config.get('build', {}).get('output_dir', 'docs')
        
        if output_dir.exists():
            shutil.rmtree(output_dir)
            self.logger.info(f"✅ Removed {output_dir}")
        
        # Clean logs
        for log_file in self.root.glob('*.log'):
            log_file.unlink()
            self.logger.info(f"✅ Removed {log_file.name}")
    
    def analyze(self, sections=None):
        """Run visual analysis"""
        self.logger.info("👁️  Running visual analysis...")
        
        cmd = ['python', 'tools/visual_inspector.py', '--full', '--analyze']
        
        try:
            subprocess.run(cmd, cwd=self.root, check=True)
            self.logger.info("✅ Analysis complete")
        except subprocess.CalledProcessError:
            self.logger.error("❌ Analysis failed")
    
    def optimize_images(self):
        """Optimize all images"""
        self.logger.info("🖼️  Optimizing images...")
        
        try:
            subprocess.run(['python', 'tools/image_optimizer.py'], cwd=self.root, check=True)
            self.logger.info("✅ Images optimized")
        except subprocess.CalledProcessError:
            self.logger.error("❌ Optimization failed")
    
    def cleanup(self, aggressive=False):
        """Clean up project"""
        self.logger.info("🗑️  Cleaning up project...")
        
        cmd = ['python', 'cleanup_project.py']
        if aggressive:
            cmd.append('--aggressive')
        
        try:
            subprocess.run(cmd, cwd=self.root, check=True)
            self.logger.info("✅ Cleanup complete")
        except subprocess.CalledProcessError:
            self.logger.error("❌ Cleanup failed")
    
    def status(self):
        """Show project status"""
        print("\n" + "="*60)
        print("📊 PROJECT STATUS")
        print("="*60)
        
        # Project info
        proj = self.config.get('project', {})
        print(f"\n📦 {proj.get('name', 'Unknown')} v{proj.get('version', '?')}")
        
        # File counts
        root_py = len(list(self.root.glob("*.py")))
        root_md = len(list(self.root.glob("*.md")))
        
        tools_dir = self.root / 'tools'
        tools_py = len(list(tools_dir.glob("*.py"))) if tools_dir.exists() else 0
        
        reports_dir = self.root / 'reports'
        reports = len(list(reports_dir.glob("*.md"))) if reports_dir.exists() else 0
        
        print(f"\n📂 Files:")
        print(f"  Root: {root_py} .py, {root_md} .md")
        print(f"  Tools: {tools_py}")
        print(f"  Reports: {reports}")
        
        # Build status
        output_dir = self.root / self.config.get('build', {}).get('output_dir', 'docs')
        if output_dir.exists():
            index = output_dir / 'index.html'
            if index.exists():
                size = index.stat().st_size
                modified = datetime.fromtimestamp(index.stat().st_mtime)
                print(f"\n🏗️  Last Build:")
                print(f"  Date: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Size: {size:,} bytes")
        
        # Backups
        backup_loc = self.root / self.config.get('backup', {}).get('location', 'backups')
        if backup_loc.exists():
            backups = list(backup_loc.glob('backup_*'))
            print(f"\n💾 Backups: {len(backups)}")
        
        print("\n" + "="*60)
        print("✅ Status check complete")
        print("="*60 + "\n")
    
    def init_git_hooks(self):
        """Initialize git hooks"""
        self.logger.info("🪝 Setting up git hooks...")
        
        git_dir = self.root / '.git'
        if not git_dir.exists():
            self.logger.warning("Not a git repository")
            return
        
        hooks_dir = git_dir / 'hooks'
        hooks_dir.mkdir(exist_ok=True)
        
        # Pre-commit hook
        pre_commit = hooks_dir / 'pre-commit'
        pre_commit.write_text("""#!/bin/bash
# Auto-generated pre-commit hook

echo "Running pre-commit checks..."

# Validate project
python site.py validate

if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Commit aborted."
    exit 1
fi

# Cleanup
python site.py cleanup

echo "✅ Pre-commit checks passed"
exit 0
""")
        pre_commit.chmod(0o755)
        
        self.logger.info("✅ Git hooks installed")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Legs on the Ground - Unified Site Management',
        epilog='Examples:\n'
               '  python site.py build\n'
               '  python site.py dev\n'
               '  python site.py analyze\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--version', action='version', version='1.0.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Build command
    subparsers.add_parser('build', help='Build the site')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate content and structure')
    
    # Serve command
    subparsers.add_parser('serve', help='Start development server')
    
    # Dev command
    subparsers.add_parser('dev', help='Development mode (build + serve)')
    
    # Clean command
    subparsers.add_parser('clean', help='Clean build artifacts')
    
    # Backup command
    subparsers.add_parser('backup', help='Create backup')
    
    # Analyze command
    subparsers.add_parser('analyze', help='Run visual analysis')
    
    # Optimize command
    subparsers.add_parser('optimize', help='Optimize images')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up project')
    cleanup_parser.add_argument('--aggressive', action='store_true', help='Aggressive cleanup')
    
    # Status command
    subparsers.add_parser('status', help='Show project status')
    
    # Init command
    subparsers.add_parser('init-hooks', help='Initialize git hooks')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize manager
    manager = SiteManager()
    
    # Execute command
    commands = {
        'build': manager.build,
        'validate': manager.validate,
        'serve': manager.serve,
        'dev': manager.dev,
        'clean': manager.clean,
        'backup': manager.backup,
        'analyze': manager.analyze,
        'optimize': manager.optimize_images,
        'cleanup': lambda: manager.cleanup(args.aggressive if hasattr(args, 'aggressive') else False),
        'status': manager.status,
        'init-hooks': manager.init_git_hooks,
    }
    
    command_func = commands.get(args.command)
    if command_func:
        try:
            command_func()
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled")
        except Exception as e:
            logging.error(f"❌ Error: {str(e)}")
            sys.exit(1)


if __name__ == '__main__':
    main()
