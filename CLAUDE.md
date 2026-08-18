# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is not a software project — it's a private planning hub (Markdown docs) for Justin Kramer's bachelor weekend, September 10-13, 2026, in Berlin/Ocean City, Maryland. The only code is a small Python script that renders a printable bingo card PDF. Most work here is editing planning documents, not writing code.

## Build command

Generate the bingo card PDF after editing `print/bingo-card.json`:

```powershell
python -m pip install -r requirements-print.txt
python scripts/build_bingo_card.py
```

This reads `print/bingo-card.json` and writes `output/pdf/justins-bachelor-weekend-bingo-card.pdf`. There is no lint/test suite — the only "build" is this script, and the only verification is opening the generated PDF (a preview PNG lives at `output/preview/justins-bachelor-weekend-bingo-card.png`).

`print/bingo-card.json` must contain exactly 25 items (`items` array) plus an integer `free_space_index` (0-24, zero-based) marking the free-space square; `build_bingo_card.py` raises `ValueError` if either constraint is violated.

## Document structure

`README.md` is the entry point and index — it holds the current-plan summary table and links to every other file with a one-line description of each. When adding a new planning file, link it from `README.md`'s "Planning files" table.

Editing conventions used throughout (follow them for consistency):
- Confirmed decisions are bolded inline (e.g. **Casino Pirates**, **8628 Saddlecreek Drive**).
- Each file opens with a one-line **Decision:** or bolded summary before going into detail.
- `CHECKLIST.md` is the single source of truth for open action items — mirror new to-dos there rather than scattering them across files.
- `CONTACTS.md` contains personal phone numbers and must stay private; if this repo is ever made public, remove it first. `promo/INVITE.md` is the only file written for outside/group-chat sharing (no address, no phone numbers).
- `SOURCES.md` tracks research verification dates — update it when re-verifying a price, booking, or schedule claim elsewhere in the docs.

## Key files

| File | Purpose |
| --- | --- |
| `ITINERARY.md` | Day-by-day schedule |
| `GUESTS.md` | Attendance, arrivals, carpools, boat roster |
| `GOLF.md` | Friday golf RSVPs, course, booking steps |
| `FOOD.md` | Meal plan and the one firm dinner reservation |
| `LOGISTICS.md` | Lodging, boat, transportation, costs |
| `THEME.md` | Casino Pirates prop kit and what to avoid |
| `HOUSE-SUPPLIES.md` | Food/drink/prop shopping assignments by car |
| `HOUSE-RULES.md` | House and safety rules |
| `CONTACTS.md` | Internal phone/location directory (private, do not expose) |
| `IDEAS.md` | Researched backup activities |
| `SOURCES.md` | Research sources and verification dates |
| `calendar/justins-ocean-city-weekend.ics` | Importable calendar |
| `print/bingo-card.json` + `scripts/build_bingo_card.py` | Bingo card content and PDF generator |
