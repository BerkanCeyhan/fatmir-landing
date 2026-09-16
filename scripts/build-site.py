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

# ---------------------------------------------------------------- Kontaktseite
nav_html = re.search(r"<nav data-nav.*?</nav>", body, re.S).group(0)
footer_html = re.search(r"<footer.*?</footer>", body, re.S).group(0)


def subpage(html):
    """Nav/Footer fuer eine Seite eine Ebene tiefer umbiegen."""
    html = html.replace('src="assets/', 'src="../assets/')
    html = html.replace('href="#', 'href="../#')
    html = html.replace('href="kontakt/"', 'href="./"')
    return html


k_nav = subpage(nav_html)
# Auf der Kontaktseite gibt es kein Hero, die Leiste startet direkt hell
k_nav = k_nav.replace(
    "border:1px solid transparent; background:transparent;",
    "border:1px solid rgba(20,24,26,.1); background:rgba(245,242,236,.86);"
    " box-shadow:0 10px 36px rgba(20,24,26,.08); backdrop-filter:blur(14px);")
k_nav = k_nav.replace("color:#FFFFFF; text-shadow:0 1px 12px rgba(20,24,26,.35);", "color:#4B534F;")
k_nav = k_nav.replace('href="../#top"', 'href="../"')
k_nav = k_nav.replace('href="../#gespraech"', 'href="#termin"')

k_footer = subpage(footer_html)

KONTAKT_JS = """
(function () {
  var apply = function () {
    var w = window.innerWidth;
    document.querySelectorAll('[data-cols3]').forEach(function (el) {
      el.style.gridTemplateColumns = w >= 900 ? 'repeat(3, minmax(0,1fr))'
        : (w >= 620 ? 'repeat(2, minmax(0,1fr))' : '1fr');
    });
    var links = document.querySelector('[data-nav-links]');
    if (links) links.style.display = w >= 900 ? 'flex' : 'none';
  };
  apply();
  window.addEventListener('resize', apply);
  document.querySelectorAll('[data-magnet]').forEach(function (el) {
    el.addEventListener('mouseenter', function () { el.style.transform = 'scale(1.03) translateY(-1px)'; });
    el.addEventListener('mouseleave', function () { el.style.transform = 'none'; });
  });
})();
"""

K_DESC = ("Termin mit Fatmir Adzaj buchen. Kostenloses Erstgespraech zu Sichtbarkeit, "
          "Performance Marketing und Live Shopping.")

kontakt = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kontakt — Fatmir Adzaj</title>
<meta name="description" content="{K_DESC}">
<meta name="robots" content="index, follow">
<meta property="og:title" content="Termin mit Fatmir Adzaj buchen">
<meta property="og:description" content="{K_DESC}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#F5F2EC">
<link rel="icon" href="../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts}
<style>{style}</style>
</head>
<body>
<div style="position:relative; max-width:100%; overflow:hidden; background:#F5F2EC; display:flex; flex-direction:column; min-height:100dvh;">

{k_nav}

  <main id="termin" style="flex:1; padding:clamp(122px,14vw,160px) 22px clamp(56px,7vw,96px);">
    <div style="max-width:960px; margin:0 auto;">
      <h1 style="margin:0; font-size:clamp(2.1rem,5.4vw,3.4rem); line-height:1.12; letter-spacing:-.02em; color:#14181A;">Termin mit Fatmir buchen</h1>
      <p style="margin:18px 0 0; max-width:52ch; font-size:clamp(1.05rem,1.5vw,1.2rem); line-height:1.65; color:#4B534F;">Such dir einen freien Platz im Kalender aus. Im Gespräch klären wir, wo du gerade stehst und welcher Hebel bei dir am schnellsten Sichtbarkeit bringt.</p>

      <!-- Calendly: hier das Inline Widget einsetzen.
           1. Im <head> oben ergänzen:
              <link rel="stylesheet" href="https://assets.calendly.com/assets/external/widget.css">
           2. Den folgenden Platzhalter ersetzen durch:
              <div class="calendly-inline-widget" data-url="https://calendly.com/DEIN-LINK"
                   style="min-width:320px; height:760px;"></div>
              <script src="https://assets.calendly.com/assets/external/widget.js" async></script> -->
      <div data-calendly style="margin-top:clamp(30px,4vw,48px); min-height:640px; display:flex; align-items:center; justify-content:center; padding:32px; border-radius:22px; border:1px solid rgba(20,24,26,.1); background:#FDFBF6; box-shadow:0 18px 48px rgba(20,24,26,.06);">
        <p style="margin:0; max-width:34ch; text-align:center; font-size:1.05rem; line-height:1.6; color:#767D78;">Hier erscheint der Kalender von Calendly, sobald der Terminlink hinterlegt ist.</p>
      </div>
    </div>
  </main>

{k_footer}

</div>
<script>{KONTAKT_JS}</script>
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
(OUT / "kontakt").mkdir(exist_ok=True)
(OUT / "kontakt" / "index.html").write_text(kontakt, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")

size = sum(f.stat().st_size for f in ASSETS.iterdir()) + (OUT / "index.html").stat().st_size
print(f"docs/index.html geschrieben, {len(page)//1024} KB HTML, "
      f"{len(list(ASSETS.iterdir()))} Assets, {size//1024} KB gesamt")
print(f"docs/kontakt/index.html geschrieben, {len(kontakt)//1024} KB HTML")
