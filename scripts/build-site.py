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

JS = r"""
(function () {
  var doc = document;
  var FAQ_SINGLE_OPEN = true;
  var MARQUEE_SECONDS = 46;

  function toggleFaq(e) {
    var btn = e.currentTarget;
    var item = btn.parentElement;
    var panel = item.querySelector('[data-faq-panel]');
    var icon = btn.querySelector('[data-faq-icon]');
    var open = panel.style.gridTemplateRows === '1fr';
    var list = btn.closest('[data-faq]');
    if (FAQ_SINGLE_OPEN) {
      list.querySelectorAll('[data-faq-panel]').forEach(function (p) { p.style.gridTemplateRows = '0fr'; });
      list.querySelectorAll('[data-faq-icon]').forEach(function (ic) { ic.style.transform = 'none'; });
      list.querySelectorAll('button[aria-expanded]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    } else if (open) {
      panel.style.gridTemplateRows = '0fr';
      if (icon) icon.style.transform = 'none';
    }
    if (!open) {
      panel.style.gridTemplateRows = '1fr';
      if (icon) icon.style.transform = 'rotate(45deg)';
    }
    btn.setAttribute('aria-expanded', open ? 'false' : 'true');
  }
  doc.querySelectorAll('[data-faq] button[aria-expanded]').forEach(function (b) {
    b.addEventListener('click', toggleFaq);
  });

  var form = doc.querySelector('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = form.querySelector('[data-waitlist]');
      var msg = form.querySelector('[data-waitlist-msg]');
      if (msg) msg.textContent = 'Danke, du stehst auf der Warteliste. Fatmir meldet sich vor dem Start.';
      if (input) input.value = '';
    });
  }

  var bar = doc.querySelector('[data-mobile-cta]');
  var dismissed = false;
  var close = bar && bar.querySelector('button');
  if (close) {
    close.addEventListener('click', function () {
      dismissed = true;
      bar.style.transform = 'translateY(120%)';
    });
  }

  var reveals = Array.prototype.slice.call(doc.querySelectorAll('[data-reveal]')).filter(function (el) {
    return !el.closest('[data-hero]');
  });
  var vh = window.innerHeight;
  reveals.forEach(function (el) {
    if (el.getBoundingClientRect().top > vh * 0.9) el.style.opacity = '0';
  });
  var ro = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target;
      var sibs = Array.prototype.slice.call(el.parentElement ? el.parentElement.children : []).filter(function (c) {
        return c.hasAttribute && c.hasAttribute('data-reveal');
      });
      var idx = Math.max(0, sibs.indexOf(el));
      el.style.animation = 'rise .75s cubic-bezier(.22,.9,.3,1) ' + (idx * 0.08) + 's both';
      ro.unobserve(el);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  reveals.forEach(function (el) { ro.observe(el); });

  doc.querySelectorAll('[data-hero] [data-reveal]').forEach(function (el, i) {
    el.style.opacity = '0';
    el.style.animation = 'rise .85s cubic-bezier(.22,.9,.3,1) ' + (0.15 + i * 0.1) + 's both';
  });

  var nav = doc.querySelector('[data-nav]');
  var hero = doc.querySelector('[data-hero]');
  function setNav(solid) {
    if (!nav) return;
    nav.style.background = solid ? 'rgba(251,248,244,.86)' : 'transparent';
    nav.style.borderColor = solid ? 'rgba(23,20,15,.1)' : 'transparent';
    nav.style.boxShadow = solid ? '0 10px 36px rgba(23,20,15,.08)' : 'none';
    nav.style.backdropFilter = solid ? 'blur(14px)' : 'none';
  }
  if (hero) {
    var no = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var past = en.intersectionRatio < 0.2;
        setNav(past);
        if (bar && !dismissed && window.innerWidth < 768) {
          bar.style.display = 'flex';
          bar.style.transform = past ? 'translateY(0)' : 'translateY(120%)';
        }
      });
    }, { threshold: [0, 0.2, 0.6] });
    no.observe(hero);
  }

  function applyResponsive() {
    var w = window.innerWidth;
    var wide = w >= 900;
    doc.querySelectorAll('[data-cols2]').forEach(function (el) {
      el.style.gridTemplateColumns = wide ? 'repeat(2, minmax(0,1fr))' : '1fr';
    });
    doc.querySelectorAll('[data-cols3]').forEach(function (el) {
      el.style.gridTemplateColumns = wide ? 'repeat(3, minmax(0,1fr))' : (w >= 620 ? 'repeat(2, minmax(0,1fr))' : '1fr');
    });
    doc.querySelectorAll('[data-cols4]').forEach(function (el) {
      el.style.gridTemplateColumns = wide ? 'repeat(4, minmax(0,1fr))' : 'repeat(2, minmax(0,1fr))';
    });
    var heroWideLayout = w >= 980;
    var heroGrid = doc.querySelector('[data-hero-grid]');
    var heroWide = doc.querySelector('[data-hero-wide]');
    var heroPortrait = doc.querySelector('[data-hero-portrait]');
    var heroBlob = doc.querySelector('[data-hero-blob]');
    if (heroGrid) {
      heroGrid.style.gridTemplateColumns = heroWideLayout ? '1.05fr .95fr' : '1fr';
      heroGrid.style.position = heroWideLayout ? 'absolute' : 'relative';
      heroGrid.style.inset = heroWideLayout ? '0' : '';
      heroGrid.style.paddingTop = heroWideLayout ? '110px' : '132px';
    }
    if (heroWide) heroWide.style.display = heroWideLayout ? 'block' : 'none';
    if (heroPortrait) heroPortrait.style.display = heroWideLayout ? 'none' : 'block';
    if (heroBlob) heroBlob.style.display = heroWideLayout ? 'none' : 'block';
    doc.querySelectorAll('[data-flip] > *').forEach(function (el, i) {
      el.style.order = wide && i === 0 ? '2' : '';
    });
    var links = doc.querySelector('[data-nav-links]');
    if (links) links.style.display = w >= 900 ? 'flex' : 'none';
    if (bar && w >= 768) bar.style.display = 'none';
  }
  applyResponsive();
  window.addEventListener('resize', applyResponsive);

  doc.querySelectorAll('[data-magnet]').forEach(function (el) {
    el.addEventListener('mouseenter', function () { el.style.transform = 'scale(1.03) translateY(-1px)'; });
    el.addEventListener('mouseleave', function () { el.style.transform = 'none'; });
  });

  var mq = doc.querySelector('[data-marquee]');
  if (mq) mq.style.animationDuration = MARQUEE_SECONDS + 's';
  var wrap = doc.querySelector('[data-marquee-wrap]');
  if (wrap && mq) {
    wrap.addEventListener('mouseenter', function () { mq.style.animationPlayState = 'paused'; });
    wrap.addEventListener('mouseleave', function () { mq.style.animationPlayState = 'running'; });
  }
})();
"""

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
