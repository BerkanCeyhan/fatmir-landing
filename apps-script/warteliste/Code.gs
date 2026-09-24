/**
 * Warteliste fuer das Social Selling Coaching.
 * Nimmt eine E-Mail Adresse entgegen und haengt sie an die Tabelle an.
 * Bereitgestellt als Web-App, Zugriff anonym, Ausfuehrung als Eigentuemer.
 *
 * Abwehr gegen automatische Eintraege, in dieser Reihenfolge:
 *   1. Honigtopf   verstecktes Feld, das nur ein Skript ausfuellt
 *   2. Zeitfalle   ein Mensch braucht laenger als zweieinhalb Sekunden
 *   3. Signatur    Wert aus Adresse, Tagesdatum und Salz, im Browser gebildet
 *   4. Drossel     mehr als acht Eintraege in zehn Minuten sind kein Mensch
 *   5. Muster      Gmail Punkte-Trick und Wegwerfdomains
 * Abgewiesene Versuche landen im Blatt "Abgewiesen", die Antwort bleibt
 * aber immer freundlich, damit ein Bot nicht lernt, woran er scheitert.
 */
var SHEET_ID = '1CKrI0nWwBuQxLFpq7YwitnLmOS_2QTYuNfqyeblB13A';
var TAB = 'Warteliste';
var TAB_BLOCK = 'Abgewiesen';
var SALT = 'fatmir-warteliste-2026';
var MIN_MS = 2500;
var MAX_MS = 7200000;
var LIMIT_COUNT = 8;
var LIMIT_WINDOW = 10 * 60 * 1000;

function doPost(e) {
  var data = {};
  try {
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); } catch (err) { data = e.parameter || {}; }
    } else {
      data = (e && e.parameter) || {};
    }
  } catch (err) {
    return out({ ok: false, error: 'payload' });
  }

  var mail = String(data.email || '').trim().toLowerCase();
  if (!/^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$/.test(mail) || mail.length > 160) {
    return out({ ok: false, error: 'mail' });
  }

  var reason = check(data, mail);
  if (reason) {
    log(TAB_BLOCK, [new Date(), mail, String(data.source || '').slice(0, 60),
                    String(data.page || '').slice(0, 160), reason]);
    return out({ ok: true });
  }

  var sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB);
  var last = sheet.getLastRow();
  var known = [];
  if (last > 1) {
    known = sheet.getRange(2, 2, last - 1, 1).getValues().map(function (r) {
      return normalize(String(r[0]));
    });
  }
  if (known.indexOf(normalize(mail)) === -1) {
    sheet.appendRow([new Date(), mail, String(data.source || 'warteliste').slice(0, 60),
                     String(data.page || '').slice(0, 160), '']);
    remember();
  }
  return out({ ok: true });
}

/** Gibt den Ablehnungsgrund zurueck oder eine leere Zeichenkette. */
function check(data, mail) {
  if (String(data.hp || '').length > 0) return 'honigtopf';

  var dt = Number(data.dt || 0);
  if (!(dt >= MIN_MS && dt <= MAX_MS)) return 'zeitfalle ' + dt;

  if (String(data.k || '') !== '' && !signatureOk(mail, String(data.k))) return 'signatur';
  if (String(data.k || '') === '') return 'ohne signatur';

  var local = mail.split('@')[0];
  var domain = mail.split('@')[1];
  if ((local.match(/\./g) || []).length > 4) return 'punktmuster';
  if (/^(mailinator|guerrillamail|10minutemail|yopmail|trashmail|sharklasers)\./.test(domain)
      || /(mailinator|guerrillamail|10minutemail|yopmail|trashmail|sharklasers)\.[a-z]+$/.test(domain)) {
    return 'wegwerfadresse';
  }

  if (tooMany()) return 'drossel';
  return '';
}

/** Gmail ignoriert Punkte und alles hinter einem Plus. */
function normalize(mail) {
  mail = String(mail).trim().toLowerCase();
  var parts = mail.split('@');
  if (parts.length !== 2) return mail;
  var local = parts[0].split('+')[0];
  if (parts[1] === 'gmail.com' || parts[1] === 'googlemail.com') {
    local = local.replace(/\./g, '');
  }
  return local + '@' + parts[1];
}

/** Der Browser bildet denselben Wert, drei Tage werden zugelassen. */
function signatureOk(mail, given) {
  var now = new Date();
  for (var d = -1; d <= 1; d++) {
    var day = new Date(now.getTime() + d * 86400000);
    if (sign(mail, Utilities.formatDate(day, 'UTC', 'yyyyMMdd')) === given) return true;
  }
  return false;
}

function sign(mail, day) {
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,
                                      mail + '|' + day + '|' + SALT, Utilities.Charset.UTF_8);
  var hex = '';
  for (var i = 0; i < bytes.length; i++) {
    hex += ('0' + (bytes[i] & 255).toString(16)).slice(-2);
  }
  return hex.slice(0, 16);
}

function tooMany() {
  var props = PropertiesService.getScriptProperties();
  var raw = props.getProperty('stamps') || '[]';
  var stamps;
  try { stamps = JSON.parse(raw); } catch (err) { stamps = []; }
  var now = Date.now();
  var recent = stamps.filter(function (t) { return now - t < LIMIT_WINDOW; });
  return recent.length >= LIMIT_COUNT;
}

function remember() {
  var props = PropertiesService.getScriptProperties();
  var raw = props.getProperty('stamps') || '[]';
  var stamps;
  try { stamps = JSON.parse(raw); } catch (err) { stamps = []; }
  stamps.push(Date.now());
  props.setProperty('stamps', JSON.stringify(stamps.slice(-40)));
}

function log(tabName, row) {
  var book = SpreadsheetApp.openById(SHEET_ID);
  var sheet = book.getSheetByName(tabName);
  if (!sheet) {
    sheet = book.insertSheet(tabName);
    sheet.appendRow(['Zeitpunkt', 'E-Mail', 'Quelle', 'Seite', 'Grund']);
    sheet.setFrozenRows(1);
  }
  sheet.appendRow(row);
}

function doGet() {
  return out({ ok: true, hint: 'Warteliste laeuft' });
}

function out(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
