# Konten-Umzug: von André's privaten Konten auf hoteleigene Konten

Ziel: GitHub-Repo, Firebase-Projekt und bit.ly-Links laufen künftig unter
Konten, auf die das Hotel selbst Zugriff hat — nicht mehr nur privat bei
André Schwarz. Die eigentliche Übertragung braucht Zugangsdaten, die nur ihr
bzw. André habt; dieses Dokument ist die Schritt-für-Schritt-Anleitung dafür.
Ich kann bei jedem Schritt helfen, wenn ihr mir sagt, wo ihr steht.

Reihenfolge einhalten — GitHub zuerst, dann Firebase, zuletzt bit.ly, weil
die späteren Schritte von den URLs der früheren abhängen.

---

## 0. Vorbereitung

- [ ] Ein **Hotel-E-Mail-Postfach** festlegen, das die neuen Konten trägt
      (nicht die private Adresse einer einzelnen Person) — z. B. eine
      Rezeptions- oder IT-Adresse des Hotels.
- [ ] Damit einen **neuen GitHub-Account** anlegen (falls nicht vorhanden).
- [ ] Damit ein **Google-Konto** anlegen bzw. ein bestehendes Hotel-Google-Konto
      nutzen (für Firebase).

## 1. GitHub-Repo übertragen

André (aktueller Owner) macht das:

1. Im Repo → **Settings** → ganz unten **„Danger Zone"** → **„Transfer
   ownership"**.
2. Neuen Kontonamen (Hotel-Account) eingeben, bestätigen.
3. Das Hotel-Konto bekommt eine Einladung per Mail/GitHub-Benachrichtigung —
   annehmen.

**Achtung:** Nach dem Transfer ändert sich die GitHub-Pages-URL, falls der
alte Owner-Name Teil der URL war
(`https://[alter-owner].github.io/turmhotel/...` →
`https://[neuer-owner].github.io/turmhotel/...`) — **außer** ihr richtet
vorher/danach die eigene Subdomain ein (Schritt 1b), dann bleibt die URL für
alle dauerhaft gleich. Ohne Subdomain gilt: **alle bit.ly-Links müssen ihr
Ziel neu bekommen** (siehe Schritt 3). Bis dahin funktionieren die alten
bit.ly-Links nicht mehr — am besten Umzug außerhalb der Hauptbetriebszeit
machen und vorher kurz das Team informieren.

GitHub Pages selbst läuft nach dem Transfer automatisch unter dem neuen
Owner-Namen weiter (keine Neueinrichtung nötig), die komplette Commit-Historie
bleibt erhalten, und es kostet nichts — GitHub Pages ist für öffentliche Repos
immer kostenlos.

**Vorher unbedingt aktualisieren — 7 Dateien verweisen fest auf den alten
Kontonamen** (`intelligentresponder-max`), das muss nach dem Transfer als
Code-Änderung nachgezogen werden (sonst zeigen Canonical-Tags, die Sitemap,
ein Link in `vorfuehrung.html` und die Anleitung in
`housekeeping-anleitung.html` weiter auf die alte Adresse):
- `index.html` (canonical, og:url)
- `wegweiser.html` (canonical, og:url)
- `sitemap.xml` (`<loc>`-Eintrag)
- `vorfuehrung.html` (Text „github.com/intelligentresponder-max/turmhotel")
- `housekeeping/housekeeping-anleitung.html` (Link + sichtbarer Text auf
  `housekeeping-v3.html`)
- `UEBERGABE_HSK777.md` (Repo-Adresse in Zeile 11)
- diese Datei selbst (Platzhalter `[neuer-owner]` oben)

Geprüft (25.09.2026): alle internen Links im Repo sind relativ, keine
absoluten `/…`-Pfade — die Seiten laufen also unverändert sowohl unter der
GitHub-Pages-Subpath-URL als auch später unter der eigenen Subdomain-Root,
ohne dass an den Links selbst etwas geändert werden muss. Nur die 7 oben
genannten Dateien mit fest eingetragener absoluter Adresse betreffen den
Umzug.

Am besten in einem eigenen Commit direkt nach dem Transfer — Claude Code kann
das in einem Rutsch erledigen, sobald der neue Kontoname feststeht.

Danach: Wer künftig Änderungen einstellen soll, unter **Settings → Collaborators**
eintragen (siehe auch `ANLEITUNG_UPDATES.md`).

## 1b. Eigene Subdomain (empfohlen)

Damit weder `intelligentresponder-max` noch ein neuer, ebenso beliebiger
GitHub-Nutzername in der URL auftaucht, empfiehlt sich eine Subdomain der
ohnehin vorhandenen Hotel-Domain `turmhotel-frankfurt.de`, z. B.
**`tools.turmhotel-frankfurt.de`**. Kostet nichts zusätzlich (GitHub Pages
selbst bleibt gratis), nur die Domain gibt es schon.

1. **DNS-Eintrag setzen** — bei wem auch immer `turmhotel-frankfurt.de`
   verwaltet wird (Hoster der Hauptseite, i. d. R. nicht André/GitHub):
   ```
   Typ: CNAME
   Name: tools
   Ziel: [neuer-owner].github.io
   ```
   (Ein CNAME-Eintrag auf eine Subdomain — nicht auf die nackte Domain
   `turmhotel-frankfurt.de` selbst, das bräuchte stattdessen A-Records auf
   die GitHub-Pages-IPs.)
2. **Im Repo:** Datei `CNAME` (ohne Endung) im Root anlegen, Inhalt genau
   eine Zeile: `tools.turmhotel-frankfurt.de`. Bei jedem Push automatisch
   ausgeliefert, kein Build-Schritt nötig.
3. **GitHub Settings → Pages:** Custom domain einträgt sich meist automatisch
   aus der `CNAME`-Datei; dort zusätzlich **„Enforce HTTPS"** anhaken, sobald
   das Zertifikat ausgestellt ist (kann nach DNS-Änderung einige Minuten bis
   ~24 h dauern, GitHub stellt es automatisch aus, kein eigenes Zertifikat
   nötig).
4. **bit.ly-Links** (Schritt 3) dann direkt auf die neue Subdomain zeigen
   lassen, z. B. `tools.turmhotel-frankfurt.de/housekeeping/housekeeping-v3.html`
   — kürzer und stabil, auch falls der GitHub-Kontoname sich je wieder ändert.
5. Canonical-Tags/og:url in `index.html` und `wegweiser.html` zusätzlich zur
   Konto-Umstellung gleich auf die Subdomain setzen, dann nur eine Änderung
   statt zwei.

Laut Rückmeldung (25.09.2026) verwaltet ein **externer Hoster/eine Agentur**
die DNS-Einträge von `turmhotel-frankfurt.de` — nicht André direkt. Fertige
Anfrage zum Weiterleiten:

> Betreff: DNS-Eintrag für turmhotel-frankfurt.de — neue Subdomain
>
> Bitte legt für turmhotel-frankfurt.de folgenden Eintrag an:
>
> Typ: CNAME
> Name/Host: tools
> Ziel/Wert: [neuer-owner].github.io
> TTL: Standard
>
> Ergebnis: tools.turmhotel-frankfurt.de soll auf unsere GitHub-Pages-Seite
> zeigen (kein Webspace bei euch nötig, nur der DNS-Eintrag). Danke!

`[neuer-owner]` durch den tatsächlichen GitHub-Kontonamen ersetzen, sobald er
feststeht (Schritt 1) — bis dahin kann die Anfrage nicht ganz fertig
raus, der Rest der Anfrage lässt sich aber schon jetzt vorbereiten/ankündigen.

## 2. Firebase-Projekt umziehen

Firebase-Projekte lassen sich nicht einfach übertragen — es braucht ein
**neues Projekt** unter dem Hotel-Google-Konto plus Datenübernahme.

1. [console.firebase.google.com](https://console.firebase.google.com) mit dem
   Hotel-Google-Konto öffnen → **„Projekt hinzufügen"**.
2. **Realtime Database** anlegen, Region **europe-west1** wählen (wie bisher,
   sonst leidet die Geschwindigkeit).
3. Die neue Datenbank-URL notieren, sieht aus wie
   `https://[neuer-projektname]-default-rtdb.europe-west1.firebasedatabase.app`.
4. **Daten übernehmen** — die alten Daten sind nicht geheim, einfach im
   Browser abrufen und wieder einspielen:
   - Alt: `https://turmhotel-hsk-default-rtdb.europe-west1.firebasedatabase.app/state.json`
     und `.../staff.json` aufrufen, Inhalt kopieren.
   - In der neuen Firebase-Konsole unter **Realtime Database → Daten** die
     beiden Knoten `state` und `staff` anlegen und den kopierten Inhalt
     einfügen (Konsole hat einen „JSON importieren"-Button pro Knoten).
5. **Regeln setzen — bitte NICHT den alten offenen Stand übernehmen.**
   *Korrektur, Stand 25.09.2026:* Die alte Datenbank ist aktuell **nicht**
   mehr offen les-/schreibbar — die Testregeln vom 06.08. sind nach 30 Tagen
   abgelaufen, die DB liefert seither `401 Permission denied` (siehe
   `UEBERGABE_HSK777.md` F12/F13). Das heißt: kein Datenverlust-Risiko beim
   Umzug, aber auch kein Sync zwischen den Handys, bis Regeln neu gesetzt
   sind — umso mehr Grund, beim neuen Projekt gleich richtig anzufangen statt
   die alte Lücke zu wiederholen.

   **Empfohlene Regeln für das neue Projekt** (Anonymous Auth, kein offener
   Zugriff mehr):
   ```json
   {
     "rules": {
       ".read": "auth != null",
       ".write": "auth != null"
     }
   }
   ```
   Console-Weg: **Authentication → Sign-in method → Anonymous → aktivieren**,
   dann **Realtime Database → Regeln** obiges JSON eintragen und
   veröffentlichen.

   **Dazu nötige Code-Änderung** (vorbereitet, noch **nicht** in die Live-Datei
   eingespielt — braucht den Firebase **Web API Key** aus der neuen Konsole,
   Project Settings → General → „Web API Key", und eure Freigabe):
   - Vor jedem der 7 Firebase-Zugriffe in `housekeeping/housekeeping-v3.html`
     (`saveState`, `saveStaffData`, History-Speichern/-Laden, `syncFromCloud`)
     einmalig anonym anmelden über die REST-Identity-Toolkit-API
     (`identitytoolkit.googleapis.com/v1/accounts:signUp?key=WEB_API_KEY`),
     das zurückgegebene `idToken` cachen und an jede `.json`-URL als
     `?auth=TOKEN` (bzw. `&auth=TOKEN`) anhängen.
   - `idToken` läuft nach 1 h ab — braucht einen stillen Refresh über das
     mitgelieferte `refreshToken` (`securetoken.googleapis.com/v1/token`),
     sonst reißt der Sync nach einer Stunde geräuschlos wieder ab (derselbe
     Fehlertyp wie F12/F13).
   - Kein SDK nötig, bleibt bei den bestehenden reinen `fetch()`-Aufrufen —
     nur ein kleiner `dbUrl(pfad)`-Helfer, der den Token anhängt, plus die
     Sign-in/Refresh-Funktion.
   - Aufwand: klein (kein Architekturwechsel), aber echte Code-Änderung mit
     Syntaxcheck-Pflicht und Test auf zwei Geräten — **nicht** im selben Zug
     wie der reine Kontenumzug, sondern als eigener, separat committeter
     Schritt, sobald der Web API Key vorliegt.
6. **Code anpassen** — dank der Aufräumarbeit gibt es nur noch **eine**
   Stelle für die URL selbst: in `housekeeping/housekeeping-v3.html` die Zeile
   ```js
   const FIREBASE_URL = 'https://turmhotel-hsk-default-rtdb.europe-west1.firebasedatabase.app';
   ```
   auf die neue URL ändern (das geht über `ANLEITUNG_UPDATES.md`, ist aber
   Code im `<script>`-Bereich — hier lieber einen Entwickler oder Claude
   direkt bitten, den einen Zeilen-Tausch zu machen und die Syntaxprüfung
   laufen zu lassen). Wird sinnvollerweise im selben Commit wie Schritt 5
   (Auth-Code) erledigt, da beides dieselben Zeilen betrifft.
7. Testen: Auf zwei Geräten öffnen, auf einem einen Zimmerstatus ändern, prüfen
   ob es auf dem anderen ankommt.

## 3. bit.ly-Links umziehen

1. Mit dem Hotel-Konto bei [bit.ly](https://bitly.com) anmelden (neuer
   Account, falls die alten Links auf André's privatem Account liegen).
2. Zwei neue Kurzlinks anlegen, die auf die **neue** GitHub-Pages-URL zeigen:
   - `housekeeping/housekeeping-v3.html` (bisher `bit.ly/turm7`)
   - `housekeeping/alpha-scan.html` (bisher `bit.ly/turmhsk`)
3. Falls möglich dieselben Kurznamen (`turm7`, `turmhsk`) wählen, damit sich
   für das Team nichts merken muss — sonst neue Links an alle verteilen
   (Homescreen-Icons auf den Handys müssen dann neu angelegt werden).

## 4. Nacharbeiten

- [ ] `README.md` und `UEBERGABE_HSK777.md`: Zeile „Entwicklung und Betrieb:
      André Schwarz" durch die neue Zuständigkeit ersetzen, falls gewünscht.
- [ ] Alle Geräte im Housekeeping-Team einmal die App neu laden lassen
      (Homescreen-Verknüpfung zeigt sonst weiter auf den alten Link).
- [ ] Altes Firebase-Projekt und alte bit.ly-Links erst löschen/deaktivieren,
      wenn der neue Weg 1–2 Tage im echten Betrieb bestätigt ist.
- [ ] Die 7 Dateien mit fest verdrahtetem alten Kontonamen aktualisieren
      (Liste siehe Schritt 1 oben).

---

## 5. Inhalts-Inventar (Stand 25.09.2026 — für den Transfer, nichts vergessen)

Alles unten wandert automatisch mit dem Repo-Transfer mit (Git überträgt die
komplette Historie inkl. aller Dateien) — diese Liste ist zur Kontrolle, damit
danach nichts als „verschwunden" gemeldet wird, und um zu zeigen, was danach
wo weiterläuft.

**Live, öffentlich indexiert** (`sitemap.xml`):
- `index.html` — Haupt-Landingpage (Gästeportal-FAQ-Widget, Kontakt, Impressum)

**Live, nur per Link/QR-Code** (`noindex`, bewusst nicht in der Sitemap):
- `wegweiser.html` — Gäste-Wegweiser (Sprachwahl DE/EN)
- `facility.html`, `handbuch.html` — Personal-Handbuch
- `onboarding-checkliste.html` — Personal-Onboarding
- `housekeeping/housekeeping-v3.html` — **das Housekeeping-Tool** (`bit.ly/turm7`)
- `housekeeping/alpha-scan.html` — abgeschaltet seit 25.09., leitet automatisch
  auf `housekeeping-v3.html` weiter (`bit.ly/turmhsk` bleibt dadurch gültig)
- `housekeeping/housekeeping-anleitung.html` — Bedienanleitung zum Tool
- `manager.html` — Übersichtsseite/Kachel-Menü zu den Personal-Tools
- `vorfuehrung.html` — **Vorführungs-/Präsentationsseite** für
  Leitungs-Meetings (zuletzt genutzt 25.09.2026)

**Referenzierte, aber nicht mehr existente Seite:**
- `personal.html` — früher im Footer geplant, Datei nie angelegt; aktuell
  (Stand 25.09.) nirgends mehr verlinkt gefunden, also kein toter Link mehr
  offen — nur zur Kenntnis, falls beim Aufräumen wieder auftaucht.

**Reserviert, absichtlich nicht live:**
- `guestportal/` — nur ein `README.md` als Platzhalter; ein früherer Entwurf
  (erfundene Concierge-Person „Alexander") wurde am 24.08. bewusst verworfen,
  siehe Datei selbst. Reserviert für einen echten KI-Chatbot, falls später mit
  Nicole/Rezeption abgestimmt.

**Dokumentation (Betrieb, nicht öffentlich):**
- `README.md`, `UEBERGABE_HSK777.md`, `CHECKLIST_HSK.md`,
  `ANLEITUNG_UPDATES.md`, `KONTEN_UMZUG.md` (diese Datei)
- `Gebrauchsanweisung-Housekeeping-App.pdf` — Team-Anleitung als PDF

**Bilder/Assets:**
- `img/` — 3 Screenshots für Doku/Anleitungen

**Entwickler-Werkzeug, nicht live:**
- `scripts/` — 12 einmalige Python-Patch-Skripte aus der Entwicklungshistorie
  (`p5_…` bis `p12_…`, `fix_…`). Rein historisch, nichts davon wird zur
  Laufzeit ausgeführt. **Geprüft (25.09.2026): bewusst getrennt von `archiv/`**
  gehalten — laut Verlauf-Tabelle in `UEBERGABE_HSK777.md` war „Skripte →
  `scripts/`, Backup → `archiv/`" eine gezielte Aufräum-Entscheidung vom
  selben Tag (`5467ab9`), kein Versehen. Nicht zusammenlegen, unkritisch für
  den Transfer.
- `archiv/housekeeping-v3.backup.html` — bewusst hier statt in `housekeeping/`
  abgelegt (siehe Fehlerprotokoll F3 in `UEBERGABE_HSK777.md`).
- `.claude/agents/Robo Bro.agent.md` — Agenten-Konfiguration, nicht Teil der
  Website, wandert automatisch mit.

**Externe Abhängigkeiten, die vom Transfer NICHT betroffen sind, aber separat
in diesem Dokument behandelt werden:**
- Firebase Realtime Database (Schritt 2 — braucht neues Projekt, s. o.)
- bit.ly-Kurzlinks `turm7`/`turmhsk` (Schritt 3)
- Externe CDN-Bibliotheken (Tesseract.js, pdf.js, heic2any, jsPDF — alle über
  cdnjs, keine eigenen Zugangsdaten, laufen unter jedem Konto identisch weiter)

---

**Wenn ihr an einem der Schritte hängt** (z. B. Firebase-Konsole, Regeln,
oder der Code-Zeile in Schritt 2.6): einfach melden, wo genau ihr steht —
ich kann von dort aus weiterhelfen.
