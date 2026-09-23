/**
 * Warteliste fuer das Social Selling Coaching.
 * Nimmt eine E-Mail Adresse entgegen und haengt sie an die Tabelle an.
 * Bereitgestellt als Web-App, Zugriff anonym, Ausfuehrung als Eigentuemer.
 */
var SHEET_ID = '1CKrI0nWwBuQxLFpq7YwitnLmOS_2QTYuNfqyeblB13A';
var TAB = 'Warteliste';

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); } catch (err) { data = e.parameter || {}; }
    } else {
      data = (e && e.parameter) || {};
    }
    var mail = String(data.email || '').trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$/.test(mail) || mail.length > 160) {
      return out({ ok: false, error: 'mail' });
    }
    var sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB);
    var last = sheet.getLastRow();
    var known = [];
    if (last > 1) {
      known = sheet.getRange(2, 2, last - 1, 1).getValues().map(function (r) {
        return String(r[0]).trim().toLowerCase();
      });
    }
    if (known.indexOf(mail) === -1) {
      sheet.appendRow([
        new Date(),
        mail,
        String(data.source || 'warteliste').slice(0, 60),
        String(data.page || '').slice(0, 160),
        ''
      ]);
    }
    return out({ ok: true });
  } catch (err) {
    return out({ ok: false, error: String(err).slice(0, 200) });
  }
}

function doGet() {
  return out({ ok: true, hint: 'Warteliste laeuft' });
}

function out(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
