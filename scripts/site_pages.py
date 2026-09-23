# -*- coding: utf-8 -*-
"""Inhalte der Unterseiten und der Einwilligungsleiste.

Getrennt von build-site.py, damit der Generator lesbar bleibt.
Rechtstexte: Stand 23.09.2026, Angaben aus dem Impressum von fatmir.de.
"""

SITE = "https://fatmir.de"
MAIL = "team@fatmir.de"
TEL = "02331 3442428"
NAME = "Fatmir Adzaj"
STREET = "Tronjestraße 14"
CITY = "44319 Dortmund"
USTID = "DE815728781"

# Leer lassen, solange keine Messung laeuft. Sobald hier eine GA4 Kennung steht,
# erscheint die Kategorie Statistik in der Leiste und wird nur nach Einwilligung geladen.
GA4_ID = ""

H2 = 'style="margin:38px 0 14px; font-size:clamp(1.25rem,2.4vw,1.6rem); line-height:1.2; letter-spacing:-.02em;"'
H3 = 'style="margin:26px 0 10px; font-size:1.08rem; line-height:1.3; letter-spacing:-.01em;"'
P = 'style="margin:0 0 14px; font-size:1.02rem; line-height:1.7; color:#3A413D;"'
UL = 'style="margin:0 0 14px; padding-left:20px; font-size:1.02rem; line-height:1.7; color:#3A413D;"'

# --------------------------------------------------------------------- Kontakt

KONTAKT_MAIN = f'''  <main id="termin" style="flex:1; padding:clamp(122px,14vw,160px) 22px clamp(56px,7vw,96px);">
    <div style="max-width:960px; margin:0 auto;">
      <h1 style="margin:0; font-size:clamp(2.1rem,5.4vw,3.4rem); line-height:1.12; letter-spacing:-.02em; color:#14181A;">Termin mit Fatmir buchen</h1>
      <p style="margin:18px 0 0; max-width:52ch; font-size:clamp(1.05rem,1.5vw,1.2rem); line-height:1.65; color:#4B534F;">Such dir einen freien Platz im Kalender aus. Im Gespräch klären wir, wo du gerade stehst und welcher Hebel bei dir am schnellsten Sichtbarkeit bringt.</p>
      <div style="margin-top:18px; display:flex; flex-wrap:wrap; gap:8px 20px; font-size:.98rem; font-weight:600; color:#4B534F;">
        <span>30 Minuten</span><span style="color:rgba(20,24,26,.3);">·</span>
        <span>kostenlos</span><span style="color:rgba(20,24,26,.3);">·</span>
        <span>persönlich mit Fatmir</span>
      </div>

      <div data-calendly style="margin-top:clamp(30px,4vw,48px); border-radius:22px; border:1px solid rgba(20,24,26,.1); background:#FDFBF6; box-shadow:0 18px 48px rgba(20,24,26,.06); overflow:hidden;">
        <div data-calendly-gate style="min-height:420px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:18px; padding:clamp(28px,5vw,56px); text-align:center;">
          <p style="margin:0; max-width:46ch; font-size:1.05rem; line-height:1.65; color:#3A413D;">Der Kalender kommt von Calendly. Beim Laden erfährt Calendly deine IP Adresse und setzt eigene Cookies. Deshalb fragen wir vorher.</p>
          <button type="button" data-calendly-load style="min-height:54px; padding:16px 30px; border-radius:999px; border:none; background:#C32828; color:#F5F2EC; font-family:inherit; font-size:1.02rem; font-weight:600; cursor:pointer;">Kalender laden und Termin wählen</button>
          <p style="margin:0; font-size:.9rem; line-height:1.6; color:#767D78;">Kein Kalender nötig? Schreib einfach an <a href="mailto:{MAIL}" style="color:#A02121; font-weight:600;">{MAIL}</a> oder ruf an: <a href="tel:+4923313442428" style="color:#A02121; font-weight:600;">{TEL}</a></p>
        </div>
        <div data-calendly-mount style="display:none;"></div>
      </div>
    </div>
  </main>
'''

# -------------------------------------------------------------------- Impressum

IMPRESSUM_MAIN = f'''  <main style="flex:1; padding:clamp(122px,14vw,150px) 22px clamp(56px,7vw,96px);">
    <div style="max-width:760px; margin:0 auto;">
      <h1 style="margin:0 0 28px; font-size:clamp(2rem,5vw,3rem); line-height:1.12; letter-spacing:-.02em; color:#14181A;">Impressum</h1>

      <h2 {H2}>Angaben gemäß § 5 TMG</h2>
      <p {P}>{NAME}<br>{STREET}<br>{CITY}<br>Deutschland</p>

      <h2 {H2}>Kontakt</h2>
      <p {P}>Telefon: <a href="tel:+4923313442428" style="color:#A02121;">{TEL}</a><br>
      E-Mail: <a href="mailto:{MAIL}" style="color:#A02121;">{MAIL}</a></p>

      <h2 {H2}>Vertreten durch</h2>
      <p {P}>{NAME}</p>

      <h2 {H2}>Umsatzsteuer-Identifikationsnummer</h2>
      <p {P}>Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz: {USTID}</p>

      <h2 {H2}>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
      <p {P}>{NAME}<br>{STREET}<br>{CITY}</p>

      <h2 {H2}>Streitbeilegung</h2>
      <p {P}>Die Europäische Kommission stellt eine Plattform zur Online Streitbeilegung bereit: <a href="https://ec.europa.eu/consumers/odr" rel="noopener" target="_blank" style="color:#A02121;">ec.europa.eu/consumers/odr</a>. Unsere E-Mail Adresse steht oben. Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>

      <h2 {H2}>Haftung für Inhalte</h2>
      <p {P}>Als Diensteanbieter sind wir für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Wir sind jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen. Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den allgemeinen Gesetzen bleiben davon unberührt. Eine diesbezügliche Haftung ist erst ab dem Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden entsprechender Rechtsverletzungen entfernen wir diese Inhalte umgehend.</p>

      <h2 {H2}>Haftung für Links</h2>
      <p {P}>Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft, rechtswidrige Inhalte waren nicht erkennbar. Eine permanente inhaltliche Kontrolle ohne konkrete Anhaltspunkte einer Rechtsverletzung ist nicht zumutbar. Bei Bekanntwerden von Rechtsverletzungen entfernen wir solche Links umgehend.</p>

      <h2 {H2}>Urheberrecht</h2>
      <p {P}>Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung des jeweiligen Autors. Downloads und Kopien dieser Seite sind nur für den privaten, nicht kommerziellen Gebrauch gestattet. Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die Urheberrechte Dritter beachtet und als solche gekennzeichnet. Sollte Ihnen dennoch eine Urheberrechtsverletzung auffallen, bitten wir um einen Hinweis. Bei Bekanntwerden von Rechtsverletzungen entfernen wir solche Inhalte umgehend.</p>

      <p style="margin:32px 0 0; font-size:.92rem; color:#767D78;">Alle genannten Marken und Logos gehören den jeweiligen Rechteinhabern.</p>
    </div>
  </main>
'''

# ------------------------------------------------------------------ Datenschutz

DATENSCHUTZ_MAIN = f'''  <main style="flex:1; padding:clamp(122px,14vw,150px) 22px clamp(56px,7vw,96px);">
    <div style="max-width:760px; margin:0 auto;">
      <h1 style="margin:0 0 12px; font-size:clamp(2rem,5vw,3rem); line-height:1.12; letter-spacing:-.02em; color:#14181A;">Datenschutzerklärung</h1>
      <p style="margin:0 0 26px; font-size:.95rem; color:#767D78;">Stand: 23. September 2026</p>

      <h2 {H2}>1. Verantwortlicher</h2>
      <p {P}>{NAME}<br>{STREET}<br>{CITY}<br>Deutschland<br>
      Telefon: <a href="tel:+4923313442428" style="color:#A02121;">{TEL}</a><br>
      E-Mail: <a href="mailto:{MAIL}" style="color:#A02121;">{MAIL}</a></p>
      <p {P}>Ein Datenschutzbeauftragter ist nicht bestellt, da die gesetzlichen Voraussetzungen dafür nicht vorliegen.</p>

      <h2 {H2}>2. Überblick in einem Satz</h2>
      <p {P}>Diese Seite kommt ohne Werbe Cookies und ohne Messtechnik aus. Nur wenn du den Terminkalender lädst oder dich in die Warteliste einträgst, verlassen Daten diese Seite, und das jeweils erst nach deiner ausdrücklichen Handlung.</p>

      <h2 {H2}>3. Hosting und Server Logfiles</h2>
      <p {P}>Die Seite wird bei GitHub Pages gehostet, einem Dienst der GitHub, Inc., 88 Colin P Kelly Jr Street, San Francisco, CA 94107, USA. Beim Aufruf der Seite verarbeitet GitHub technisch notwendige Verbindungsdaten, darunter die IP Adresse, Datum und Uhrzeit des Zugriffs, die aufgerufene Datei, den Browsertyp und das Betriebssystem. Ohne diese Verarbeitung lässt sich die Seite technisch nicht ausliefern.</p>
      <p {P}>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO, unser berechtigtes Interesse an einer sicheren und stabilen Auslieferung der Seite. Die Übermittlung in die USA stützt sich auf die Standardvertragsklauseln der EU Kommission und die Zertifizierung von GitHub unter dem EU US Data Privacy Framework. Weitere Angaben: <a href="https://docs.github.com/site-policy/privacy-policies/github-privacy-statement" rel="noopener" target="_blank" style="color:#A02121;">GitHub Privacy Statement</a>.</p>

      <h2 {H2}>4. Schriften und eingebundene Inhalte</h2>
      <p {P}>Die verwendeten Schriften werden von unserem eigenen Server ausgeliefert. Es entsteht keine Verbindung zu Google Fonts und es wird keine IP Adresse an Google übertragen. Bilder, Icons und Skripte liegen ebenfalls auf unserem Server.</p>

      <h2 {H2}>5. Einwilligungsbanner und lokale Speicherung</h2>
      <p {P}>Damit wir dich nicht bei jedem Aufruf erneut fragen, speichern wir deine Entscheidung im lokalen Speicher deines Browsers unter dem Schlüssel <code style="font-size:.95em;">fa-consent</code>. Das ist kein Cookie, die Angabe verlässt deinen Browser nicht und enthält nur deine Auswahl und den Zeitpunkt. Rechtsgrundlage ist § 25 Abs. 2 Nr. 2 TDDDG, weil die Speicherung für die von dir gewünschte Einstellung unbedingt erforderlich ist. Deine Entscheidung kannst du jederzeit unten im Fußbereich unter „Cookie Einstellungen" ändern. Die Einwilligung gilt für zwölf Monate, danach fragen wir erneut.</p>

      <h2 {H2}>6. Terminbuchung über Calendly</h2>
      <p {P}>Auf der Seite <a href="/kontakt/" style="color:#A02121;">Kontakt</a> bieten wir eine Terminbuchung über Calendly an, einen Dienst der Calendly LLC, 271 17th St NW, Atlanta, GA 30363, USA. Der Kalender wird erst geladen, wenn du auf die Schaltfläche klickst und damit einwilligst. Vorher wird keine Verbindung zu Calendly aufgebaut.</p>
      <p {P}>Nach dem Laden verarbeitet Calendly deine IP Adresse, technische Browserdaten und setzt Cookies. Wenn du einen Termin buchst, verarbeitet Calendly zusätzlich die von dir angegebenen Daten, in der Regel Name, E-Mail Adresse und die von dir gewählte Zeit, sowie deine Antworten auf etwaige Fragen im Buchungsformular. Diese Daten erreichen uns, damit wir den Termin wahrnehmen können.</p>
      <p {P}>Rechtsgrundlage für das Laden des Kalenders und die damit verbundene Speicherung auf deinem Endgerät ist deine Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO und § 25 Abs. 1 TDDDG. Rechtsgrundlage für die Verarbeitung der Buchungsdaten ist Art. 6 Abs. 1 lit. b DSGVO, da sie der Durchführung vorvertraglicher Maßnahmen dient. Die Übermittlung in die USA stützt sich auf die Standardvertragsklauseln und das EU US Data Privacy Framework. Du kannst deine Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen, indem du im Fußbereich die Cookie Einstellungen öffnest. Weitere Angaben: <a href="https://calendly.com/de/privacy" rel="noopener" target="_blank" style="color:#A02121;">Datenschutzerklärung von Calendly</a>.</p>

      <h2 {H2}>7. Warteliste für das Social Selling Coaching</h2>
      <p {P}>Wenn du dich für die Warteliste einträgst, verarbeiten wir die von dir angegebene E-Mail Adresse sowie den Zeitpunkt des Eintrags. Wir nutzen sie ausschließlich, um dich einmalig zu informieren, sobald das Coaching startet. Es folgt kein weiterer Newsletter.</p>
      <p {P}>Die Eintragung wird in einer Tabelle bei Google Sheets gespeichert, einem Dienst der Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland. Eine Verarbeitung durch die Google LLC in den USA ist dabei nicht ausgeschlossen, sie stützt sich auf die Standardvertragsklauseln und das EU US Data Privacy Framework. Rechtsgrundlage ist deine Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO, die du mit dem Absenden erteilst. Du kannst sie jederzeit formlos an <a href="mailto:{MAIL}" style="color:#A02121;">{MAIL}</a> widerrufen, dann löschen wir deinen Eintrag. Spätestens sechs Monate nach dem Start des Coachings löschen wir die Liste vollständig.</p>

      <h2 {H2}>8. Kontaktaufnahme per E-Mail oder Telefon</h2>
      <p {P}>Wenn du uns schreibst oder anrufst, verarbeiten wir deine Angaben, um die Anfrage zu bearbeiten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO bei vertraglichem Bezug, sonst Art. 6 Abs. 1 lit. f DSGVO, unser berechtigtes Interesse an der Beantwortung. Wir löschen die Daten, sobald der Vorgang abgeschlossen ist und keine gesetzlichen Aufbewahrungsfristen entgegenstehen.</p>

      <h2 {H2}>9. Keine Reichweitenmessung</h2>
      <p {P}>Zum genannten Stand setzen wir keine Analyse oder Tracking Werkzeuge ein. Es findet kein Profiling und keine automatisierte Entscheidungsfindung statt. Sobald sich das ändert, ergänzen wir diese Erklärung und fragen vorher über das Einwilligungsbanner.</p>

      <h2 {H2}>10. Verschlüsselung</h2>
      <p {P}>Die Seite wird ausschließlich über HTTPS ausgeliefert. Damit sind die Inhalte, die du überträgst, auf dem Transportweg verschlüsselt.</p>

      <h2 {H2}>11. Deine Rechte</h2>
      <p {P}>Du hast nach der DSGVO jederzeit das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen (Art. 21). Eine erteilte Einwilligung kannst du jederzeit mit Wirkung für die Zukunft widerrufen (Art. 7 Abs. 3). Wende dich dafür formlos an <a href="mailto:{MAIL}" style="color:#A02121;">{MAIL}</a>.</p>
      <p {P}>Außerdem steht dir ein Beschwerderecht bei einer Aufsichtsbehörde zu. Zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen, Kavalleriestraße 2 bis 4, 40213 Düsseldorf.</p>

      <h2 {H2}>12. Änderungen</h2>
      <p {P}>Wir passen diese Erklärung an, wenn sich die Seite ändert, etwa wenn eine Reichweitenmessung hinzukommt. Es gilt jeweils die hier veröffentlichte Fassung.</p>
    </div>
  </main>
'''
