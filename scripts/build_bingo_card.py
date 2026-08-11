#!/usr/bin/env python3
"""Build the printable bachelor-weekend bingo card from JSON content."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


PAGE_WIDTH, PAGE_HEIGHT = letter
NAVY = HexColor("#15324A")
TEAL = HexColor("#197C80")
CORAL = HexColor("#E96B5B")
PALE_TEAL = HexColor("#EAF5F3")
PALE_SAND = HexColor("#FFF8E8")
INK = HexColor("#17242D")
MUTED = HexColor("#53636D")


def wrap_lines(text: str, font: str, size: float, max_width: float) -> list[str]:
    """Wrap text to fit a cell, preserving explicit line breaks."""
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if stringWidth(candidate, font, size) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def fit_cell_text(text: str, max_width: float, max_height: float) -> tuple[float, list[str]]:
    """Choose the largest readable font size that fits inside one square."""
    for size in (10.5, 10, 9.5, 9, 8.5, 8, 7.5):
        lines = wrap_lines(text, "Helvetica-Bold", size, max_width)
        leading = size * 1.22
        if len(lines) * leading <= max_height:
            return size, lines
    return 7.5, wrap_lines(text, "Helvetica-Bold", 7.5, max_width)


def draw_centered_lines(
    pdf: canvas.Canvas,
    text: str,
    center_x: float,
    center_y: float,
    max_width: float,
    max_height: float,
    color=INK,
) -> None:
    size, lines = fit_cell_text(text, max_width, max_height)
    leading = size * 1.22
    first_baseline = center_y + ((len(lines) - 1) * leading / 2) - (size * 0.34)
    pdf.setFillColor(color)
    pdf.setFont("Helvetica-Bold", size)
    for index, line in enumerate(lines):
        pdf.drawCentredString(center_x, first_baseline - (index * leading), line)


def build_card(config_path: Path, output_path: Path) -> None:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    items = config.get("items", [])
    if len(items) != 25:
        raise ValueError(f"Expected exactly 25 bingo items, found {len(items)}")
    free_space_index = config.get("free_space_index")
    if not isinstance(free_space_index, int) or not 0 <= free_space_index < 25:
        raise ValueError("free_space_index must be an integer from 0 through 24")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output_path), pagesize=letter)
    pdf.setTitle(config["title"])
    pdf.setAuthor("Justin's Ocean City Bachelor Weekend")
    pdf.setSubject("Printable 5x5 bachelor weekend bingo card")

    # Header
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 23)
    pdf.drawCentredString(PAGE_WIDTH / 2, 748, config["title"])
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(PAGE_WIDTH / 2, 724, config["subtitle"])
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2, 706, config["instructions"])

    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(0.9)
    pdf.line(36, 681, 210, 681)
    pdf.line(402, 681, 576, 681)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(36, 686, "PLAYER")
    pdf.drawString(402, 686, "WINNING MOMENT")

    # B-I-N-G-O column tabs
    grid_x = 36
    grid_width = 540
    cell = grid_width / 5
    tab_y = 649
    tab_height = 25
    tab_colors = (NAVY, TEAL, CORAL, TEAL, NAVY)
    for column, letter_value in enumerate("BINGO"):
        x = grid_x + column * cell
        pdf.setFillColor(tab_colors[column])
        pdf.rect(x, tab_y, cell, tab_height, stroke=0, fill=1)
        pdf.setFillColor(white)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(x + cell / 2, tab_y + 6.5, letter_value)

    # Five-by-five board with one supplied moment in every square.
    grid_top = tab_y
    for row in range(5):
        for column in range(5):
            x = grid_x + column * cell
            y = grid_top - (row + 1) * cell
            item_index = (row * 5) + column
            is_free_space = item_index == free_space_index
            pdf.setFillColor(PALE_SAND if is_free_space else (PALE_TEAL if (row + column) % 2 else white))
            pdf.setStrokeColor(CORAL if is_free_space else NAVY)
            pdf.setLineWidth(2.4 if is_free_space else 1.35)
            pdf.rect(x, y, cell, cell, stroke=1, fill=1)

            if is_free_space:
                pdf.setFillColor(CORAL)
                pdf.setFont("Helvetica-Bold", 9)
                pdf.drawCentredString(x + cell / 2, y + 79, "FREE SPACE")
                pdf.setStrokeColor(CORAL)
                pdf.setLineWidth(1.4)
                pdf.line(x + 29, y + 72, x + cell - 29, y + 72)
                draw_centered_lines(
                    pdf,
                    str(items[item_index]),
                    x + cell / 2,
                    y + 43,
                    cell - 16,
                    54,
                    NAVY,
                )
            else:
                draw_centered_lines(
                    pdf,
                    str(items[item_index]),
                    x + cell / 2,
                    y + cell / 2,
                    cell - 16,
                    cell - 18,
                    INK,
                )

    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 7.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 62, "B, I, N, G, O - horizontal, vertical, or diagonal. Look out for each other.")
    pdf.setStrokeColor(CORAL)
    pdf.setLineWidth(2)
    pdf.line(230, 50, 382, 50)

    pdf.showPage()
    pdf.save()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("print/bingo-card.json"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/pdf/justins-bachelor-weekend-bingo-card.pdf"),
    )
    args = parser.parse_args()
    build_card(args.config, args.output)


if __name__ == "__main__":
    main()
