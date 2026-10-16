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
from datetime import date
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
CALENDLY = "https://calendly.com/team-fatmir/30min?hide_gdpr_banner=1&primary_color=c32828"

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

body = body.replace('<img src="assets/fatmir-hero-photo.webp"', '<img fetchpriority="high" src="assets/fatmir-hero-photo.webp"')
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

KNOWS = ["Social Selling", "TikTok Shop", "Live Shopping", "Temu", "Shopify", "Amazon",
         "Performance Marketing", "Meta Ads", "Google Ads", "Personal Branding", "Onlinehandel"]
AWARDS = ["Bester Onlineshop 2023", "Südwestfalenaward 2024",
          "Südwestfalenaward 2025", "Südwestfalenaward 2026"]


def strip_tags(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def faq_pairs(html):
    """Fragen und Antworten aus dem FAQ-Block, damit Seite und Schema gleich bleiben."""
    pat = (r'<button type="button" aria-expanded="false"[^>]*>\s*<span>(.*?)</span>.*?'
           r'<div data-faq-panel[^>]*><div[^>]*><p[^>]*>(.*?)</p>')
    return [(strip_tags(q), strip_tags(a)) for q, a in re.findall(pat, html, re.S)]


def home_ld(html, page_url):
    service = {
        "@type": "ProfessionalService",
        "@id": pg.SITE + "/#fatmir",
        "name": "Fatmir Adzaj",
        "description": ("Offizielle TikTok, Temu, Shopify und Amazon Partneragentur aus Dortmund. "
                        "Social Selling, TikTok Shop und Performance Marketing aus einer Hand."),
        "url": pg.SITE + "/",
        "image": pg.SITE + "/assets/og-fatmir.jpg",
        "logo": pg.SITE + "/assets/logo-ink.png",
        "email": pg.MAIL,
        "telephone": "+49 2331 3442428",
        "priceRange": "ab 1.500 EUR",
        "address": {"@type": "PostalAddress", "streetAddress": pg.STREET, "postalCode": "44319",
                    "addressLocality": "Dortmund", "addressRegion": "Nordrhein-Westfalen",
                    "addressCountry": "DE"},
        "areaServed": [{"@type": "Country", "name": n} for n in ("Deutschland", "Österreich", "Schweiz")],
        "founder": {"@id": pg.SITE + "/#person"},
        "award": AWARDS,
        "knowsAbout": KNOWS,
    }
    person = {
        "@type": "Person",
        "@id": pg.SITE + "/#person",
        "name": "Fatmir Adzaj",
        "jobTitle": "Berater und Unternehmer",
        "image": pg.SITE + "/assets/fatmir-hero-photo.webp",
        "url": pg.SITE + "/",
        "worksFor": {"@id": pg.SITE + "/#fatmir"},
        "knowsAbout": KNOWS,
        "award": AWARDS,
        "address": {"@type": "PostalAddress", "addressLocality": "Dortmund", "addressCountry": "DE"},
    }
    website = {
        "@type": "WebSite",
        "@id": pg.SITE + "/#website",
        "url": pg.SITE + "/",
        "name": "Fatmir Adzaj",
        "inLanguage": "de-DE",
        "publisher": {"@id": pg.SITE + "/#fatmir"},
    }
    webpage = {
        "@type": "WebPage",
        "@id": page_url + "#webpage",
        "url": page_url,
        "name": INDEX_TITLE,
        "description": INDEX_DESC,
        "inLanguage": "de-DE",
        "isPartOf": {"@id": pg.SITE + "/#website"},
        "about": {"@id": pg.SITE + "/#fatmir"},
        "primaryImageOfPage": pg.SITE + "/assets/og-fatmir.jpg",
    }
    graph = [service, person, website, webpage]
    qa = faq_pairs(html)
    if qa:
        graph.append({
            "@type": "FAQPage",
            "@id": page_url + "#faq",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa],
        })
    return {"@context": "https://schema.org", "@graph": graph}


def crumbs_ld(slug, name):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Startseite", "item": pg.SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": pg.SITE + "/" + slug + "/"},
    ]}


def head(title, description, canonical, robots="index, follow", depth=0, extra="", css=None,
         ld=None, preload_img=None):
    up = "../" * depth
    css = style if css is None else css
    ld_tag = ""
    if ld:
        ld_tag = ('\n<script type="application/ld+json">'
                  + json.dumps(ld, ensure_ascii=False, separators=(",", ":"))
                  + "</script>")
    pre = ""
    if preload_img:
        pre = f'\n<link rel="preload" as="image" href="{up}assets/{preload_img}" fetchpriority="high">'
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="Fatmir Adzaj mit dem Award für den besten Onlineshop">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{pg.SITE}/assets/og-fatmir.jpg">
<meta name="twitter:image:alt" content="Fatmir Adzaj mit dem Award für den besten Onlineshop">
<meta name="theme-color" content="#F5F2EC">
<link rel="icon" type="image/png" sizes="64x64" href="{up}assets/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="{up}assets/apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/assets/fonts/BricolageGrotesque-500-latin.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/assets/fonts/Karla-400-latin.woff2">
<style>{fonts_css}{css}</style>{pre}{ld_tag}{extra}"""


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

INDEX_TITLE = "TikTok Shop & Social Selling Partneragentur | Fatmir Adzaj"
INDEX_DESC = ("Fatmir Adzaj aus Dortmund: offizielle TikTok, Temu, Shopify und Amazon "
              "Partneragentur. Social Selling, TikTok Shop und Performance Marketing aus einer Hand.")

index_page = f"""<!DOCTYPE html>
<html lang="de">
<head>
{head(INDEX_TITLE, INDEX_DESC, pg.SITE + "/", depth=0, ld=home_ld(body, pg.SITE + "/"), preload_img="fatmir-hero-photo.webp")}
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


def build_subpage(slug, title, description, main_html, cta_href, extra_js="", robots="index, follow",
                  ld=None):
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
{head(title, description, pg.SITE + "/" + slug + "/", robots=robots, depth=1, ld=ld)}
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
    # iOS füllt Transparenz schwarz, deshalb Creme als Grund und etwas Rand
    touch = Image.new("RGBA", (180, 180), (245, 242, 236, 255))
    mark = sq.resize((140, 140), Image.LANCZOS)
    touch.paste(mark, (20, 20), mark)
    touch.convert("RGB").save(ASSETS / "apple-touch-icon.png")
except Exception as exc:  # pragma: no cover
    print("favicon uebersprungen:", exc)

(OUT / "index.html").write_text(index_page, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")

k = build_subpage(
    "kontakt",
    "Termin mit Fatmir Adzaj buchen | Kostenloses Erstgespräch",
    "Buch dir 30 Minuten mit Fatmir Adzaj, kostenlos und persönlich. Wir klären, wo du stehst "
    "und welcher Hebel dir am schnellsten Sichtbarkeit und Kunden bringt.",
    pg.KONTAKT_MAIN, '"#termin"',
    extra_js=site_consent.CALENDLY_JS.replace("@CALENDLY@", CALENDLY),
    ld=crumbs_ld("kontakt", "Termin buchen"))

i = build_subpage(
    "impressum", "Impressum | Fatmir Adzaj",
    "Impressum von Fatmir Adzaj, Tronjestraße 14, 44319 Dortmund. Angaben nach § 5 DDG.",
    pg.IMPRESSUM_MAIN, '"../kontakt/"', robots="index, follow", ld=crumbs_ld("impressum", "Impressum"))

d = build_subpage(
    "datenschutz", "Datenschutz | Fatmir Adzaj",
    "Wie diese Seite mit deinen Daten umgeht: Hosting, Calendly, Warteliste, deine Rechte. "
    "Kurz und ohne Nebelkerzen.",
    pg.DATENSCHUTZ_MAIN, '"../kontakt/"', robots="index, follow", ld=crumbs_ld("datenschutz", "Datenschutz"))

# Dankeseite: fuer Besucher nach der Buchung, nicht fuer die Suche
t_danke = build_subpage(
    "danke", "Danke, dein Termin steht | Fatmir Adzaj",
    "Termin bestätigt. Was jetzt passiert und wie du das Gespräch vorbereitest.",
    pg.DANKE_MAIN, '"../kontakt/"', robots="noindex, follow")

# Vorschau /neu/: zweite Startseite aus Neu.dc.html, gleiche Logik wie die Startseite
# plus eigenes Skript, nicht in der Sitemap und nicht im Index
NEU_SRC = ROOT / "Neu.dc.html"
t_neu = 0
if NEU_SRC.exists():
    nsrc = NEU_SRC.read_text(encoding="utf-8")
    n_style = re.search(r"<style>(.*?)</style>",
                        re.search(r"<helmet>(.*?)</helmet>", nsrc, re.S).group(1), re.S).group(1)
    n_body = re.search(r"<x-dc>(.*?)</x-dc>", nsrc, re.S).group(1)
    n_body = re.sub(r"<helmet>.*?</helmet>", "", n_body, flags=re.S)
    n_body = re.sub(r"<sc-if[^>]*>", "", n_body).replace("</sc-if>", "")
    n_body = re.sub(r'\s*on(?:Click|Submit)="\{\{[^}]*\}\}"', "", n_body)
    n_body = re.sub(r'src="([^"/:]+\.(?:png|jpe?g|webp|svg))"', r'src="../assets/\1"', n_body)
    n_body = n_body.replace('<img src="../assets/fatmir-hero-photo.webp"', '<img fetchpriority="high" src="../assets/fatmir-hero-photo.webp"')
    for p in ("kontakt/", "impressum/", "datenschutz/"):
        n_body = n_body.replace(f'href="{p}"', f'href="../{p}"')
    n_js = re.search(r"<script data-neu-script[^>]*>(.*?)</script>", nsrc, re.S).group(1)
    n_pre = re.search(r"<script data-neu-before[^>]*>(.*?)</script>", nsrc, re.S)
    start = "(function () {\n  var page = new Component("
    assert INDEX_JS.count(start) == 1
    neu_index_js = INDEX_JS.replace(start, (n_pre.group(1) if n_pre else "") + "\n" + start)
    neu_page = f"""<!DOCTYPE html>
<html lang="de">
<head>
{head(INDEX_TITLE, INDEX_DESC, pg.SITE + "/neu/", robots="noindex, nofollow", depth=1, css=n_style, ld=home_ld(n_body, pg.SITE + "/neu/"), preload_img="fatmir-hero-photo.webp")}
</head>
<body>
{n_body}
{consent_markup(1)}
<script>{neu_index_js}</script>
<script>{n_js}</script>
<script>{consent_script()}</script>
</body>
</html>
"""
    (OUT / "neu").mkdir(parents=True, exist_ok=True)
    (OUT / "neu" / "index.html").write_text(neu_page, encoding="utf-8")
    t_neu = len(neu_page)

# 404: GitHub Pages liefert docs/404.html für jede unbekannte Adresse aus,
# deshalb stehen alle Pfade absolut
build_subpage("404", "Seite nicht gefunden | Fatmir Adzaj",
              "Diese Seite gibt es nicht. Zur Startseite oder direkt einen Termin mit Fatmir buchen.",
              pg.NOTFOUND_MAIN, '"/kontakt/"', robots="noindex, follow")
nf_dir = OUT / "404"
nf = (nf_dir / "index.html").read_text(encoding="utf-8")
nf = nf.replace('src="../', 'src="/').replace('href="../', 'href="/')
nf = re.sub(r'\n<link rel="canonical"[^>]*>', "", nf)
nf = re.sub(r'\n<meta property="og:url"[^>]*>', "", nf)
(OUT / "404.html").write_text(nf, encoding="utf-8")
shutil.rmtree(nf_dir)

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
                f"    <lastmod>{date.today().isoformat()}</lastmod>",
                f"    <changefreq>{freq}</changefreq>",
                f"    <priority>{prio}</priority>", "  </url>"]
sitemap.append("</urlset>")
(OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

size = sum(f.stat().st_size for f in ASSETS.rglob("*") if f.is_file())
print(f"index {len(index_page)//1024} KB | kontakt {k//1024} KB | impressum {i//1024} KB | "
      f"datenschutz {d//1024} KB | danke {t_danke//1024} KB | neu {t_neu//1024} KB | "
      f"{count} Assets, {size//1024} KB")
