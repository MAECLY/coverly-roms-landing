# Coverly ROMs landing: https://coverly-roms.maecly.com
# Standard library only: python3 and node, no install step.

SHELL := /bin/bash
.DEFAULT_GOAL := help

REPO := MAECLY/coverly-roms
SITE_OUT := target/site
SITE_PORT ?= 8080
# GitHub release JSON to preview (e.g. scripts/site/fixtures/release.json).
RELEASE ?=
# `make covers CONTACT=/tmp/sheet.html`: also write a contact sheet.
CONTACT ?=
# Where `make sync-tokens` reads the app's design tokens.
TOKENS_URL ?= https://raw.githubusercontent.com/$(REPO)/main/design/tokens.json

.PHONY: help
help: ## List the targets.
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

.PHONY: site
site: ## Serve the landing on http://localhost:SITE_PORT, default 8080 (RELEASE=release.json to preview a release).
	node scripts/site/gen_covers.mjs --check
	rm -rf "$(SITE_OUT)"
	@if [ -n "$(RELEASE)" ]; then \
	  python3 -I scripts/site/apply_release.py --release-json "$(RELEASE)" --repo $(REPO) --site site --out "$(SITE_OUT)"; \
	else \
	  python3 -I scripts/site/apply_release.py --no-release --repo $(REPO) --site site --out "$(SITE_OUT)"; \
	fi
	@echo "Serving $(SITE_OUT) on http://localhost:$(SITE_PORT) (Ctrl+C to stop)"
	python3 -m http.server $(SITE_PORT) --bind 127.0.0.1 -d "$(SITE_OUT)"

.PHONY: build
build: ## Build target/site as Vercel does (latest release from the GitHub API).
	bash scripts/site/vercel_build.sh

.PHONY: check
check: ## Every gate: tokens, cover sprite, release.js tests, links, parity, head, budgets, contrast, motion, art, release.
	node scripts/brand/build_tokens.mjs --check
	node scripts/site/gen_covers.mjs --check
	node --test scripts/site/*.test.mjs
	python3 -I scripts/site/check_site.py

.PHONY: covers
covers: ## Regenerate the cover sprite and inks (CONTACT=sheet.html also writes a review sheet).
	node scripts/site/gen_covers.mjs $(if $(CONTACT),--contact "$(CONTACT)")

.PHONY: og
og: ## Render the Open Graph cards site/assets/og.png and og-en.png (needs Chrome or Chromium).
	node scripts/site/og.mjs

.PHONY: tokens
tokens: ## Regenerate site/assets/tokens.css from design/tokens.json.
	node scripts/brand/build_tokens.mjs

.PHONY: sync-tokens
sync-tokens: ## Fetch design/tokens.json from the app repository (main), then regenerate.
	@tmp="$$(mktemp)"; trap 'rm -f "$$tmp"' EXIT; \
	  curl -fsSL "$(TOKENS_URL)" -o "$$tmp" && \
	  python3 -I -c 'import json, sys; json.load(open(sys.argv[1]))' "$$tmp" && \
	  if cmp -s "$$tmp" design/tokens.json; then \
	    echo "design/tokens.json already matches $(REPO)@main"; \
	  else \
	    cp "$$tmp" design/tokens.json && echo "updated design/tokens.json from $(REPO)@main"; \
	  fi
	$(MAKE) --no-print-directory tokens
