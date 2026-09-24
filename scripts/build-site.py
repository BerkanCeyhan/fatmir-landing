#!/usr/bin/env python3
"""Baut aus Main.dc.html die statische Seite fuer GitHub Pages.

    python3 scripts/build-site.py

Ausgabe: docs/index.html, docs/kontakt/, docs/impressum/, docs/datenschutz/,
docs/assets/, robots.txt und sitemap.xml.

Die Startseite kommt aus Main.dc.html (Canvas-Syntax wird dabei uebersetzt),
Navigation und Fuss werden fuer die Unterseiten daraus uebernommen, damit es
keine zweite Quelle gibt. Rechtstexte stehen in scripts/site_pages.py,
die Einwilligungsleiste in scripts/site_consent.py.
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_consent
import site_pages as pg

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Main.dc.html"
OUT = ROOT / "docs"
ASSETS = OUT / "assets"
CALENDLY = "https://calendly.com/team-fatmir/30min?primary_color=c32828"

src = SRC.read_text(encoding="utf-8")

helmet = re.search(r"<helmet>(.*?)</helmet>", src, re.S).group(1)
style = re.search(r"<style>(.*?)</style>", helmet, re.S).group(1)
fonts_css = (ROOT / "img2" / "fonts" / "fonts.css").read_text(encoding="utf-8")

body = re.search(r"<x-dc>(.*?)</x-dc>", src, re.S).group(1)
body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)
body = re.sub(r"<sc-if[^>]*>", "", body)
body = body.replace("</sc-if>", "")
body = re.sub(r'\s*on(?:Click|Submit)="\{\{[^}]*\}\}"', "", body)
body = re.sub(r'src="([^"/:]+\.(?:png|jpe?g|webp|svg))"', r'src="assets/\1"', body)

logic = re.search(r"<script data-dc-script[^>]*>(.*?)</script>", src, re.S).group(1).strip()

nav_html = re.search(r"<nav data-nav.*?</nav>", body, re.S).group(0)
footer_html = re.search(r"<footer.*?</footer>", body, re.S).group(0)


def subpage_chrome(html):
    """Navigation und Fuss eine Ebene tiefer haengen."""
    html = html.replace('src="assets/', 'src="../assets/')
    html = html.replace('href="#', 'href="../#')
    html = html.replace('href="kontakt/"', 'href="../kontakt/"')
    html = html.replace('href="impressum/"', 'href="../impressum/"')
    html = html.replace('href="datenschutz/"', 'href="../datenschutz/"')
    return html


# --------------------------------------------------------------------- Kopfteil

PERSON_LD = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "@id": pg.SITE + "/#fatmir",
    "name": "Fatmir Adzaj",
    "description": ("Consulting und Personal Branding für Unternehmer. TikTok Shop, Live Shopping, "
                    "Temu, Shopify und Performance Marketing aus einer Hand."),
    "url": pg.SITE + "/",
    "image": pg.SITE + "/assets/og-fatmir.jpg",
    "logo": pg.SITE + "/assets/logo-ink.png",
    "email": pg.MAIL,
    "telephone": "+49 2331 3442428",
    "priceRange": "ab 1.500 EUR",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": pg.STREET,
        "postalCode": "44319",
        "addressLocality": "Dortmund",
        "addressCountry": "DE",
    },
    "areaServed": [{"@type": "Country", "name": "Deutschland"},
                   {"@type": "Country", "name": "Österreich"},
                   {"@type": "Country", "name": "Schweiz"}],
    "founder": {"@type": "Person", "name": "Fatmir Adzaj", "jobTitle": "Berater und Unternehmer"},
    "award": ["Bester Onlineshop 2023", "Südwestfalenaward 2024",
              "Südwestfalenaward 2025", "Südwestfalenaward 2026"],
    "knowsAbout": ["TikTok Shop", "Live Shopping", "Temu", "Shopify", "Amazon",
                   "Performance Marketing", "Personal Branding", "Onlinehandel"],
    "sameAs": [],
}


def head(title, description, canonical, robots="index, follow", depth=0, extra=""):
    up = "../" * depth
    ld = ""
    if depth == 0:
        ld = ('\n<script type="application/ld+json">'
              + json.dumps(PERSON_LD, ensure_ascii=False, separators=(",", ":"))
              + "</script>")
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="{robots}">
<meta name="author" content="Fatmir Adzaj">
<meta name="google-site-verification" content="qk1YUyTHfSH1Y-FbTKsXqTsB9fAA26CSWS--cHBqVJo">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Fatmir Adzaj">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{pg.SITE}/assets/og-fatmir.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Fatmir Adzaj mit dem Award für den besten Onlineshop">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{pg.SITE}/assets/og-fatmir.jpg">
<meta name="theme-color" content="#F5F2EC">
<link rel="icon" href="{up}assets/favicon.png">
<link rel="apple-touch-icon" href="{up}assets/favicon.png">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/assets/fonts/BricolageGrotesque-700-latin.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/assets/fonts/Karla-400-latin.woff2">
<style>{fonts_css}{style}</style>{ld}{extra}"""


def consent_markup(depth):
    return site_consent.BANNER.replace("@ROOT@", "../" * depth if depth else "")


def consent_script():
    return site_consent.JS.replace("@GA4@", pg.GA4_ID)


# ------------------------------------------------------------------ Startseite

INDEX_JS = """
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

INDEX_TITLE = "Fatmir Adzaj — Wer dich nicht kennt, kauft woanders."
INDEX_DESC = ("Keine Agentur, keine Theorie. Fatmir macht Marken sichtbar: TikTok Shop, Live Shopping, "
              "Temu, Shopify, Performance Marketing. Nicht lange schnacken. Machen.")

index_page = f"""<!DOCTYPE html>
<html lang="de">
<head>
{head(INDEX_TITLE, INDEX_DESC, pg.SITE + "/", depth=0)}
</head>
<body>
{body}
{consent_markup(0)}
<script>{INDEX_JS}</script>
<script>{consent_script()}</script>
</body>
</html>
"""

# ------------------------------------------------------------------ Unterseiten

SUB_JS = """
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


def build_subpage(slug, title, description, main_html, cta_href, extra_js="", robots="index, follow"):
    nav = subpage_chrome(nav_html)
    nav = nav.replace(
        "border:1px solid transparent; background:transparent;",
        "border:1px solid rgba(20,24,26,.1); background:rgba(245,242,236,.86);"
        " box-shadow:0 10px 36px rgba(20,24,26,.08); backdrop-filter:blur(14px);")
    nav = nav.replace("color:#4B534F; transition:color .45s ease;", "color:#4B534F;")
    nav = nav.replace('href="../#top"', 'href="../"')
    nav = nav.replace('href="../kontakt/"', cta_href)
    foot = subpage_chrome(footer_html)
    page = f"""<!DOCTYPE html>
<html lang="de">
<head>
{head(title, description, pg.SITE + "/" + slug + "/", robots=robots, depth=1)}
</head>
<body>
<div style="position:relative; max-width:100%; overflow:hidden; background:#F5F2EC; display:flex; flex-direction:column; min-height:100dvh;">

{nav}

{main_html}
{foot}

</div>
{consent_markup(1)}
<script>{SUB_JS}</script>
<script>{consent_script()}</script>
<script>{extra_js}</script>
</body>
</html>
"""
    target = OUT / slug
    target.mkdir(parents=True, exist_ok=True)
    (target / "index.html").write_text(page, encoding="utf-8")
    return len(page)


# ----------------------------------------------------------------------- Bauen

if ASSETS.exists():
    shutil.rmtree(ASSETS)
ASSETS.mkdir(parents=True)
count = 0
for f in sorted((ROOT / "img2").rglob("*")):
    if f.is_file():
        rel = f.relative_to(ROOT / "img2")
        dest = ASSETS / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        count += 1

try:
    from PIL import Image
    logo = Image.open(ROOT / "img2" / "logo-ink.png").convert("RGBA")
    side = max(logo.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
    sq.resize((64, 64), Image.LANCZOS).save(ASSETS / "favicon.png")
except Exception as exc:  # pragma: no cover
    print("favicon uebersprungen:", exc)

(OUT / "index.html").write_text(index_page, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")

k = build_subpage(
    "kontakt",
    "Termin mit Fatmir buchen — 30 Minuten, kostenlos",
    "30 Minuten, kostenlos, persönlich mit Fatmir. Kein Callcenter, kein Fragebogen. "
    "Such dir einen Platz im Kalender und wir schauen, welcher Hebel bei dir zieht.",
    pg.KONTAKT_MAIN, '"#termin"',
    extra_js=site_consent.CALENDLY_JS.replace("@CALENDLY@", CALENDLY))

i = build_subpage(
    "impressum", "Impressum — Fatmir Adzaj",
    "Impressum von Fatmir Adzaj, Tronjestraße 14, 44319 Dortmund. Angaben nach § 5 TMG.",
    pg.IMPRESSUM_MAIN, '"../kontakt/"', robots="index, follow")

d = build_subpage(
    "datenschutz", "Datenschutz — Fatmir Adzaj",
    "Wie diese Seite mit deinen Daten umgeht: Hosting, Calendly, Warteliste, deine Rechte. "
    "Kurz und ohne Nebelkerzen.",
    pg.DATENSCHUTZ_MAIN, '"../kontakt/"', robots="index, follow")

(OUT / "robots.txt").write_text(
    "User-agent: *\n"
    "Allow: /\n\n"
    f"Sitemap: {pg.SITE}/sitemap.xml\n", encoding="utf-8")

urls = [("/", "1.0", "weekly"), ("/kontakt/", "0.8", "monthly"),
        ("/impressum/", "0.2", "yearly"), ("/datenschutz/", "0.2", "yearly")]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, prio, freq in urls:
    sitemap += ["  <url>", f"    <loc>{pg.SITE}{path}</loc>",
                f"    <changefreq>{freq}</changefreq>",
                f"    <priority>{prio}</priority>", "  </url>"]
sitemap.append("</urlset>")
(OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

size = sum(f.stat().st_size for f in ASSETS.rglob("*") if f.is_file())
print(f"index {len(index_page)//1024} KB | kontakt {k//1024} KB | impressum {i//1024} KB | "
      f"datenschutz {d//1024} KB | {count} Assets, {size//1024} KB")
