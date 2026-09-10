#!/usr/bin/env python3
"""
Baut aus Main.dc.html eine eigenstaendige statische Seite fuer GitHub Pages.

    python3 scripts/build-site.py

Ausgabe: site/index.html plus site/assets/ mit allen Bildern.
Die Canvas-Eigenheiten (x-dc, helmet, sc-if, {{ }}-Handler, DCLogic) werden
dabei in normales HTML plus Vanilla JS uebersetzt.
"""
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Main.dc.html"
OUT = ROOT / "docs"
ASSETS = OUT / "assets"

src = SRC.read_text(encoding="utf-8")

helmet = re.search(r"<helmet>(.*?)</helmet>", src, re.S).group(1)
style = re.search(r"<style>(.*?)</style>", helmet, re.S).group(1)
fonts = "\n".join(re.findall(r'<link [^>]*>', helmet))

body = re.search(r"<x-dc>(.*?)</x-dc>", src, re.S).group(1)
body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)

# Canvas-Syntax herausnehmen: sc-if rendert hier immer, Handler haengen wir in JS an
body = re.sub(r"<sc-if[^>]*>", "", body)
body = body.replace("</sc-if>", "")
body = re.sub(r'\s*on(?:Click|Submit)="\{\{[^}]*\}\}"', "", body)

# Bildpfade in den Assets-Ordner umbiegen
body = re.sub(r'src="([^"/:]+\.(?:png|jpe?g|webp|svg))"', r'src="assets/\1"', body)

logic = re.search(r"<script data-dc-script[^>]*>(.*?)</script>", src, re.S).group(1).strip()

JS = """
class DCLogic {
  constructor(props) { this.props = props; }
}

%s

(function () {
  var page = new Component({ showKurs: true, showLab: false, faqSingleOpen: true, spiralSpeed: 0.55 });
  var vals = page.renderVals();
  document.querySelectorAll('[data-faq] button[aria-expanded]').forEach(function (b) {
    b.addEventListener('click', vals.toggleFaq);
  });
  var form = document.querySelector('form');
  if (form) form.addEventListener('submit', vals.joinWaitlist);
  var close = document.querySelector('[data-mobile-cta] button');
  if (close) close.addEventListener('click', vals.dismissMobileCta);
  page.componentDidMount();
})();
""" % logic

DESC = ("Fatmir Adzaj: Consulting und Personal Branding fuer Unternehmer. "
        "Performance Marketing, Live Shopping und Onlinehandel mit System.")

page = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fatmir Adzaj — Sichtbar werden. Und verkaufen.</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="Fatmir Adzaj — Sichtbar werden. Und verkaufen.">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/fatmir-hero-wide.webp">
<meta name="theme-color" content="#FBF8F4">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts}
<style>{style}</style>
</head>
<body>
{body}
<script>{JS}</script>
</body>
</html>
"""

if ASSETS.exists():
    shutil.rmtree(ASSETS)
ASSETS.mkdir(parents=True)
for f in sorted((ROOT / "img2").iterdir()):
    if f.is_file():
        shutil.copy2(f, ASSETS / f.name)

# Favicon aus dem Signatur-Logo
try:
    from PIL import Image
    logo = Image.open(ROOT / "img2" / "logo-ink.png").convert("RGBA")
    side = max(logo.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
    sq.resize((64, 64), Image.LANCZOS).save(ASSETS / "favicon.png")
except Exception as exc:  # pragma: no cover
    print("favicon uebersprungen:", exc)

(OUT / "index.html").write_text(page, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")

size = sum(f.stat().st_size for f in ASSETS.iterdir()) + (OUT / "index.html").stat().st_size
print(f"docs/index.html geschrieben, {len(page)//1024} KB HTML, "
      f"{len(list(ASSETS.iterdir()))} Assets, {size//1024} KB gesamt")
