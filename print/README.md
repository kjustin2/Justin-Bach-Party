# Bachelor Weekend Bingo

The card is a one-page, US Letter, 5-by-5 bingo layout designed for printing at Staples. It uses 25 custom moments and marks one configured moment as the free space.

## Add the final bingo moments

Edit `bingo-card.json`:

- Keep exactly 25 items. Every item appears once, including the center square.
- `free_space_index` selects the free-space item using zero-based numbering; `12` is the center square.
- Short phrases work best; the builder wraps longer phrases and reduces their type size automatically.

## Build the print PDF

From the repository root, run:

```powershell
python -m pip install -r requirements-print.txt
python scripts/build_bingo_card.py
```

The generated file is `output/pdf/justins-bachelor-weekend-bingo-card.pdf`.

Staples settings: US Letter, portrait, actual size or 100% scale, single-sided, and color. The important content stays at least 0.5 inches from every page edge.
