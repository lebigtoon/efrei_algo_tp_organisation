"""Convertit rapport.md en rapport.pdf (markdown -> HTML -> PDF via weasyprint)."""

from __future__ import annotations

from pathlib import Path

import markdown
from weasyprint import HTML

RACINE = Path(__file__).resolve().parent.parent
CHEMIN_MD = RACINE / "rapport.md"
CHEMIN_PDF = RACINE / "rapport.pdf"

CSS = """
@page { size: A4; margin: 2cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 20pt; border-bottom: 2px solid #333; padding-bottom: 6px; }
h2 { font-size: 15pt; margin-top: 1.4em; border-bottom: 1px solid #999; padding-bottom: 3px; }
h3 { font-size: 12.5pt; margin-top: 1.2em; color: #333; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 9.5pt; }
th, td { border: 1px solid #ccc; padding: 5px 8px; text-align: left; vertical-align: top; }
th { background-color: #e8e8e8; }
code { font-family: "Courier New", monospace; background-color: #f0f0f0; padding: 1px 4px; border-radius: 3px; font-size: 9pt; }
pre { background-color: #f4f4f4; border: 1px solid #ddd; padding: 10px; border-radius: 4px; font-size: 9pt; overflow-x: auto; }
pre code { background-color: transparent; padding: 0; }
"""


def convertir_md_vers_pdf(chemin_md: Path = CHEMIN_MD, chemin_pdf: Path = CHEMIN_PDF) -> None:
    texte_md = chemin_md.read_text(encoding="utf-8")
    html_corps = markdown.markdown(texte_md, extensions=["tables", "fenced_code", "toc"])
    html_complet = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_corps}</body></html>"
    HTML(string=html_complet, base_url=str(RACINE)).write_pdf(str(chemin_pdf))
    print(f"PDF généré : {chemin_pdf}")


if __name__ == "__main__":
    convertir_md_vers_pdf()
