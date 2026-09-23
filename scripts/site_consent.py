# -*- coding: utf-8 -*-
"""Einwilligungsleiste: Markup und Logik, auf jeder Seite gleich."""

BANNER = '''  <div data-consent hidden style="position:fixed; left:0; right:0; bottom:0; z-index:90; display:none; padding:14px; pointer-events:none;">
    <div style="pointer-events:auto; max-width:760px; margin:0 auto; padding:clamp(20px,3vw,28px); border-radius:24px; background:#FDFBF6; border:1px solid rgba(20,24,26,.12); box-shadow:0 24px 60px rgba(20,24,26,.22);">
      <p style="margin:0 0 8px; font-family:'Bricolage Grotesque','Karla',sans-serif; font-size:1.15rem; font-weight:700; letter-spacing:-.02em; color:#14181A;">Kurz gefragt, bevor es losgeht</p>
      <p style="margin:0 0 16px; font-size:.98rem; line-height:1.6; color:#3A413D;">Diese Seite läuft ohne Werbe Cookies. Nur der Terminkalender von Calendly lädt Inhalte von außen und setzt dabei eigene Cookies. Das entscheidest du.</p>
      <div data-consent-options style="display:none; flex-direction:column; gap:12px; margin:0 0 18px; padding:16px; border-radius:16px; background:#F5F2EC;">
        <label style="display:flex; align-items:flex-start; gap:12px; font-size:.95rem; line-height:1.55; color:#3A413D;">
          <input type="checkbox" checked disabled style="margin-top:3px; width:18px; height:18px; accent-color:#C32828;">
          <span><strong style="color:#14181A;">Notwendig.</strong> Hält die Seite am Laufen und merkt sich genau diese Entscheidung. Lässt sich nicht abwählen.</span>
        </label>
        <label style="display:flex; align-items:flex-start; gap:12px; font-size:.95rem; line-height:1.55; color:#3A413D; cursor:pointer;">
          <input type="checkbox" data-consent-cat="external" style="margin-top:3px; width:18px; height:18px; accent-color:#C32828; cursor:pointer;">
          <span><strong style="color:#14181A;">Externe Inhalte.</strong> Lädt den Terminkalender von Calendly. Dabei erfährt Calendly deine IP Adresse und setzt Cookies.</span>
        </label>
        <label data-consent-stats style="display:none; align-items:flex-start; gap:12px; font-size:.95rem; line-height:1.55; color:#3A413D; cursor:pointer;">
          <input type="checkbox" data-consent-cat="stats" style="margin-top:3px; width:18px; height:18px; accent-color:#C32828; cursor:pointer;">
          <span><strong style="color:#14181A;">Statistik.</strong> Zählt anonym, welche Seiten gelesen werden, damit wir wissen, was ankommt.</span>
        </label>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
        <button type="button" data-consent-all style="flex:1 1 200px; min-height:50px; padding:14px 24px; border:none; border-radius:999px; background:#C32828; color:#F5F2EC; font-family:inherit; font-size:1rem; font-weight:600; cursor:pointer;">Alles akzeptieren</button>
        <button type="button" data-consent-min style="flex:1 1 160px; min-height:50px; padding:14px 24px; border:1.5px solid rgba(20,24,26,.28); border-radius:999px; background:transparent; color:#14181A; font-family:inherit; font-size:1rem; font-weight:600; cursor:pointer;">Nur das Nötigste</button>
        <button type="button" data-consent-more style="min-height:50px; padding:14px 18px; border:none; border-radius:999px; background:transparent; color:#4B534F; font-family:inherit; font-size:.95rem; font-weight:600; text-decoration:underline; cursor:pointer;">Einstellungen</button>
        <button type="button" data-consent-save style="display:none; flex:1 1 200px; min-height:50px; padding:14px 24px; border:none; border-radius:999px; background:#14181A; color:#F5F2EC; font-family:inherit; font-size:1rem; font-weight:600; cursor:pointer;">Auswahl speichern</button>
      </div>
      <p style="margin:14px 0 0; font-size:.85rem; color:#767D78;"><a href="@ROOT@datenschutz/" style="color:#767D78; text-decoration:underline;">Datenschutz</a> · <a href="@ROOT@impressum/" style="color:#767D78; text-decoration:underline;">Impressum</a></p>
    </div>
  </div>
'''

JS = '''
/* Einwilligung: eine Entscheidung, im lokalen Speicher, zwoelf Monate gueltig. */
(function () {
  var KEY = 'fa-consent';
  var MAXAGE = 365 * 24 * 60 * 60 * 1000;
  var GA4 = '@GA4@';
  var root = document.querySelector('[data-consent]');

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var v = JSON.parse(raw);
      if (!v || v.v !== 1 || !v.ts || Date.now() - v.ts > MAXAGE) return null;
      return v;
    } catch (err) { return null; }
  }
  function write(state) {
    var v = { v: 1, ts: Date.now(), external: !!state.external, stats: !!state.stats };
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (err) { /* privates Fenster */ }
    api.state = v;
    apply(v);
    window.dispatchEvent(new CustomEvent('fa-consent', { detail: v }));
    hide();
  }
  function apply(v) {
    if (v && v.stats && GA4) loadStats();
  }
  var statsLoaded = false;
  function loadStats() {
    if (statsLoaded || !GA4) return;
    statsLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA4, { anonymize_ip: true });
  }
  function show() {
    if (!root) return;
    root.hidden = false;
    root.style.display = 'block';
  }
  function hide() {
    if (!root) return;
    root.style.display = 'none';
    root.hidden = true;
  }

  var api = {
    state: read(),
    has: function (cat) { return !!(api.state && api.state[cat]); },
    grant: function (cat) {
      var next = api.state || { external: false, stats: false };
      next[cat] = true;
      write(next);
    },
    open: function () {
      if (!root) return;
      var boxes = root.querySelectorAll('[data-consent-cat]');
      for (var i = 0; i < boxes.length; i++) {
        boxes[i].checked = api.has(boxes[i].getAttribute('data-consent-cat'));
      }
      root.querySelector('[data-consent-options]').style.display = 'flex';
      root.querySelector('[data-consent-save]').style.display = 'inline-flex';
      show();
    }
  };
  window.faConsent = api;

  if (root) {
    if (GA4) {
      var statsRow = root.querySelector('[data-consent-stats]');
      if (statsRow) statsRow.style.display = 'flex';
    }
    root.querySelector('[data-consent-all]').addEventListener('click', function () {
      write({ external: true, stats: !!GA4 });
    });
    root.querySelector('[data-consent-min]').addEventListener('click', function () {
      write({ external: false, stats: false });
    });
    root.querySelector('[data-consent-more]').addEventListener('click', function () {
      root.querySelector('[data-consent-options]').style.display = 'flex';
      root.querySelector('[data-consent-save]').style.display = 'inline-flex';
      this.style.display = 'none';
    });
    root.querySelector('[data-consent-save]').addEventListener('click', function () {
      var state = { external: false, stats: false };
      var boxes = root.querySelectorAll('[data-consent-cat]');
      for (var i = 0; i < boxes.length; i++) {
        state[boxes[i].getAttribute('data-consent-cat')] = boxes[i].checked;
      }
      write(state);
    });
    if (!api.state) { setTimeout(show, 900); } else { apply(api.state); }
  }

  document.querySelectorAll('[data-consent-open]').forEach(function (el) {
    el.addEventListener('click', function (e) { e.preventDefault(); api.open(); });
  });
})();
'''

CALENDLY_JS = '''
/* Calendly laedt erst nach Einwilligung, vorher steht dort nur der Hinweis. */
(function () {
  var gate = document.querySelector('[data-calendly-gate]');
  var mount = document.querySelector('[data-calendly-mount]');
  var button = document.querySelector('[data-calendly-load]');
  if (!gate || !mount) return;
  var loaded = false;

  function load() {
    if (loaded) return;
    loaded = true;
    gate.style.display = 'none';
    mount.style.display = 'block';
    var h = window.innerWidth < 720 ? 1320 : (window.innerWidth < 1000 ? 1150 : 1080);
    mount.innerHTML = '<div class="calendly-inline-widget" data-url="@CALENDLY@" data-resize="true" ' +
      'style="min-width:280px; width:100%; height:' + h + 'px;"></div>';
    var css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = 'https://assets.calendly.com/assets/external/widget.css';
    document.head.appendChild(css);
    var js = document.createElement('script');
    js.src = 'https://assets.calendly.com/assets/external/widget.js';
    js.async = true;
    document.body.appendChild(js);
  }

  if (window.faConsent && window.faConsent.has('external')) load();
  window.addEventListener('fa-consent', function (e) {
    if (e.detail && e.detail.external) load();
  });
  if (button) {
    button.addEventListener('click', function () {
      if (window.faConsent) window.faConsent.grant('external');
      load();
    });
  }
})();
'''
