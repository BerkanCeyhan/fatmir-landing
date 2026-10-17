# Fatmir Adzaj Landing Page

Statische Landing Page für Fatmir Adzaj (Consulting und Personal Branding).
Live über GitHub Pages aus dem Ordner `docs/`.

## Aufbau

- `Neu.dc.html` — Quelle der Startseite (Design-Canvas-Format), live seit 17.10.2026
- `Main.dc.html` / `Mobile.dc.html` — alte Startseite, archiviert unter fatmir.de/alt/
  (noindex). Main liefert weiter die Seitenlogik und Navigation/Fuß der Unterseiten.
  Stand vor dem Wechsel: Git-Tag `alte-startseite`
- `scripts/build-site.py` — baut daraus `docs/` (Startseite, Unterseiten, `/alt/`,
  `/neu/` als Weiterleitung auf `/`, `docs/assets/`)
- `scripts/gen-fatmir-bilder.mjs` — erzeugt Iconset, Illustrationen und Hero über Gemini
- `scripts/remove-bg.py` — stellt generierte Bilder und Partnerlogos frei
- `img2/` — fertige Bildassets der Seite

## Neu bauen

```bash
uv run --with pillow python scripts/build-site.py
```

Bildgenerierung braucht `GEMINI_API_KEY` in einer lokalen `.env` (nicht im Repo).

## Offen

- Kontaktdaten (Instagram, LinkedIn, Mail) fehlen noch
- Terminlink für den CTA fehlt noch
- Testimonials sind Beispieltexte und müssen durch echte Zitate ersetzt werden
