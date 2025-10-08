# Makefile for Legs on the Ground website
# Provides convenient shortcuts for common tasks

.PHONY: help build serve dev validate clean backup analyze optimize cleanup status install

# Default target
help:
	@echo "╔════════════════════════════════════════════════════════╗"
	@echo "║   Legs on the Ground - Development Commands            ║"
	@echo "╚════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 Setup:"
	@echo "  make install       Install dependencies"
	@echo ""
	@echo "🏗️  Build:"
	@echo "  make build         Build the site"
	@echo "  make serve         Start server (localhost:8000)"
	@echo "  make dev           Build + serve"
	@echo ""
	@echo "✅ Quality:"
	@echo "  make validate      Validate content/images"
	@echo "  make analyze       Run AI visual analysis"
	@echo "  make optimize      Optimize images"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make cleanup       Clean up project files"
	@echo "  make clean         Remove build artifacts"
	@echo "  make backup        Create backup"
	@echo ""
	@echo "📊 Info:"
	@echo "  make status        Show project status"
	@echo ""
	@echo "💡 Examples:"
	@echo "  make dev           # Start development"
	@echo "  make build         # Build for production"
	@echo "  make cleanup       # Keep project tidy"
	@echo ""

# Installation
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Installation complete"

# Build commands
build:
	@python site.py build

serve:
	@python site.py serve

dev:
	@python site.py dev

# Quality commands
validate:
	@python site.py validate

analyze:
	@python site.py analyze

optimize:
	@python site.py optimize

# Maintenance commands
cleanup:
	@python site.py cleanup

clean:
	@python site.py clean

backup:
	@python site.py backup

# Info commands
status:
	@python site.py status

# Git setup
init-hooks:
	@python site.py init-hooks

# Combined workflows
deploy: validate build
	@echo "✅ Ready for deployment"

full-clean: clean cleanup
	@echo "✅ Deep clean complete"

quick: build serve
	@echo "🚀 Quick preview"
