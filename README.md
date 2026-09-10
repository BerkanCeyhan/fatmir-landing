# Fatmir Adzaj Landing Page

Statische Landing Page für Fatmir Adzaj (Consulting und Personal Branding).
Live über GitHub Pages aus dem Ordner `docs/`.

## Aufbau

- `Main.dc.html` / `Mobile.dc.html` — Quelle der Seite (Design-Canvas-Format)
- `scripts/build-site.py` — baut daraus `docs/index.html` plus `docs/assets/`
- `scripts/gen-fatmir-bilder.mjs` — erzeugt Iconset, Illustrationen und Hero über Gemini
- `scripts/remove-bg.py` — stellt generierte Bilder und Partnerlogos frei
- `img2/` — fertige Bildassets der Seite

## Neu bauen

```bash
python3 scripts/build-site.py
```

Bildgenerierung braucht `GEMINI_API_KEY` in einer lokalen `.env` (nicht im Repo).

## Offen

- Kontaktdaten (Instagram, LinkedIn, Mail) fehlen noch
- Terminlink für den CTA fehlt noch
- Testimonials sind Beispieltexte und müssen durch echte Zitate ersetzt werden
