"""Lightweight site validator used by build.py.

The repository previously referenced a `validator` module but did not ship it,
so validation silently no-op'd. This implementation focuses on:
- HTML parseability (html5lib + BeautifulSoup)
- Basic accessibility sanity checks (missing <title>, missing alt on <img>)
- CSS parseability (cssutils)

It is intentionally conservative: it reports issues but avoids false positives.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cssutils
from bs4 import BeautifulSoup
import html5lib


@dataclass
class ValidationResult:
    name: str
    errors: list[str]
    warnings: list[str]


class SiteValidator:
    def __init__(self, output_dir: Path | str):
        self.output_dir = Path(output_dir)

        # Keep cssutils quiet unless there's a real problem.
        cssutils.log.setLevel("FATAL")

    def validate_all(self) -> list[ValidationResult]:
        results: list[ValidationResult] = []
        results.append(self._validate_html())
        results.append(self._validate_css())
        return results

    def _validate_html(self) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        html_files = sorted(self.output_dir.glob("*.html"))
        if not html_files:
            errors.append("No HTML files found in output directory")
            return ValidationResult("html", errors, warnings)

        for html_path in html_files:
            raw = html_path.read_text(encoding="utf-8", errors="replace")

            # Parse with html5lib for robustness.
            try:
                document = html5lib.parse(raw, treebuilder="etree")
                if document is None:
                    errors.append(f"{html_path.name}: html5lib returned no document")
            except Exception as exc:  # pragma: no cover
                errors.append(f"{html_path.name}: HTML parse error: {exc}")
                continue

            soup = BeautifulSoup(raw, "html.parser")

            title = soup.find("title")
            if not title or not (title.get_text(strip=True)):
                errors.append(f"{html_path.name}: missing or empty <title>")

            for img in soup.find_all("img"):
                if img.has_attr("alt"):
                    continue
                # Decorative images should still provide alt="".
                warnings.append(f"{html_path.name}: <img> missing alt attribute")

        return ValidationResult("html", errors, warnings)

    def _validate_css(self) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        css_path = self.output_dir / "styles.css"
        if not css_path.exists():
            errors.append("Missing styles.css in output")
            return ValidationResult("css", errors, warnings)

        css_text = css_path.read_text(encoding="utf-8", errors="replace")
        try:
            cssutils.parseString(css_text)
        except Exception as exc:  # pragma: no cover
            errors.append(f"styles.css: CSS parse error: {exc}")

        return ValidationResult("css", errors, warnings)

    def generate_report(self) -> str:
        results = self.validate_all()
        lines: list[str] = []
        total_errors = 0
        total_warnings = 0

        for result in results:
            total_errors += len(result.errors)
            total_warnings += len(result.warnings)

        lines.append(f"Results: {total_errors} errors, {total_warnings} warnings")

        for result in results:
            if result.errors:
                lines.append(f"\n[{result.name}] Errors:")
                lines.extend(f"- {e}" for e in result.errors)
            if result.warnings:
                lines.append(f"\n[{result.name}] Warnings:")
                lines.extend(f"- {w}" for w in result.warnings)

        return "\n".join(lines).strip() + "\n"

    def save_report(self, path: Path | str) -> None:
        path = Path(path)
        results = self.validate_all()
        payload: dict[str, Any] = {
            "output_dir": str(self.output_dir),
            "results": [
                {"name": r.name, "errors": r.errors, "warnings": r.warnings}
                for r in results
            ],
        }
        import json

        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
