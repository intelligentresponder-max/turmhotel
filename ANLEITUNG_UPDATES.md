# Kleine Änderungen selbst veröffentlichen (ohne Entwickler)

Für Rezeption/Hausdame — kein Git, kein Terminal nötig.

## Weg A — Gäste-Info auf index.html: der Editor (empfohlen für Tanja)

FAQ-Antworten, Öffnungszeiten, Frühstückspreise, Kontakttexte, Chat-Fenster-Texte
(in allen 5 Sprachen) stehen **nicht mehr im Programmcode**, sondern in einer
eigenen Datei (`content/gaeste-info.json`). Dafür gibt es eine eigene Seite mit
Formularfeldern statt Rohtext — direkt vom Handy nutzbar:

**`content/editor.html`** öffnen (z. B. `[github-pages-url]/content/editor.html`) →

1. Einmalig einen **GitHub-Zugangs-Token** einrichten (Anleitung steht direkt auf
   der Editor-Seite) — nur einmal nötig, danach reicht der gespeicherte Token
   für die laufende Sitzung.
2. Konto, Repository (`turmhotel`) und Branch (`main`) eintragen, **Laden** tippen.
3. Gewünschten Punkt antippen (z. B. eine FAQ-Frage), Text ändern. Deutsch ist
   immer sichtbar, andere Sprachen nur auf Wunsch über „🌐 Alle Sprachen zeigen".
4. Unten kurz beschreiben, was geändert wurde, **Speichern & veröffentlichen**
   tippen. Die Seite zeigt die Änderung nach 1–2 Minuten.

**Warum eigens dafür eine Seite?** Diese Inhalte liegen technisch als JSON-Datei
vor (fürs Programm nötig, damit 5 Sprachen sauber zusammenspielen) — direkt in
GitHub bearbeitet müsste man auf Anführungszeichen und Kommas achten, ein
Tippfehler hätte die ganze Seite lahmgelegt. Der Editor übernimmt das im
Hintergrund; man tippt nur noch in normale Textfelder.

**Sicherheit:** Der Zugangs-Token wird nur im Browser-Tab gespeichert
(sessionStorage) — verschwindet beim Schließen, geht an niemanden außer GitHub
selbst. Bei der Token-Erstellung unbedingt **„Nur dieses Repository"** und
**„Contents: Read and write"** wählen, sonst nichts — dann kann der Token,
selbst wenn er irgendwie in falsche Hände geriete, nichts anderes als genau
diese eine Datei in diesem einen Repo ändern.

## Weg A2 — Spontanangebote (Rezeption, für die Schicht)

Gleiches Prinzip, eigene Seite: **`content/spontan-editor.html`**. Kurzfristig
frei gewordenes Zimmer eintragen (Zimmernummer, Preis, ab wann frei) →
**Speichern**, erscheint sofort auf `spontanangebote.html` — der öffentlichen
Seite, auf der Gäste direkt bei uns anfragen können (per `mailto:`-Link, kein
Formular, kein Spam-Risiko, da nichts an einen Server geht). Derselbe
Zugangs-Token wie bei Weg A funktioniert hier auch.

## Weg B — alles andere: direkt über die GitHub-Webseite

Für Änderungen außerhalb der Gäste-Info (z. B. Handbuch-Absätze, README) —
läuft weiterhin klassisch über den GitHub-Web-Editor im Browser.

**Wichtig — was hier NICHT geht:** Nur Text und Zahlen außerhalb der
Programmierung ändern (Kontaktdaten, Überschriften, Handbuch-Absätze,
Öffnungszeiten). Alles zwischen `<script>` und `</script>` ist Programmcode —
dort ändert bitte weiterhin ein Entwickler etwas, sonst kann die ganze Seite
lautlos kaputtgehen (siehe Warnung unten).

---

## 1. Voraussetzung

Ein **eigener GitHub-Account** mit Schreibrecht auf
`github.com/[hotel-konto]/turmhotel` (siehe `KONTEN_UMZUG.md`, falls das noch
nicht eingerichtet ist).

## 2. Datei bearbeiten

1. Auf `github.com` einloggen, zum Repo `turmhotel` navigieren.
2. Zur gewünschten Datei klicken (z. B. `README.md`, `handbuch.html`,
   `housekeeping/housekeeping-anleitung.html`).
3. Oben rechts auf das **Stift-Symbol** („Edit this file") klicken.
4. Änderung vornehmen — bei HTML-Dateien nur Text zwischen den spitzen
   Klammern `>...<` ändern, die Klammern selbst und alles ab `<script>`
   in Ruhe lassen.
5. Runterscrollen zu „Commit changes".
6. Kurze Beschreibung eintragen (z. B. „Telefonnummer aktualisiert").
7. **„Commit directly to the main branch"** auswählen, dann grünen Button
   klicken.

## 3. Kontrolle

Die Seite liegt auf GitHub Pages und aktualisiert sich automatisch, meist
innerhalb 1–2 Minuten. Danach die Live-Seite (bit.ly-Link) neu laden und
prüfen, ob die Änderung stimmt und die Seite noch normal aussieht.

## 4. Falls etwas kaputtgeht

Nicht in Panik verändern. Im Repo oben auf **„… commits"** bzw. den
Verlauf der Datei gehen, den eigenen Commit suchen, auf die drei Punkte
„…" bzw. „Revert" klicken — das macht die Änderung rückgängig, ohne dass
jemand Code lesen muss.

## 5. Was bewusst NICHT über diesen Weg geht

- Alles im Bereich `<script>…</script>` (Programmlogik von Housekeeping
  Manager und Alpha-Scan)
- Die Zimmerliste (`ROOMS` in `housekeeping-v3.html`) — ändert sich ohnehin
  praktisch nie, im Zweifel Entwickler fragen
- Die Firebase-Datenbank-URL (`FIREBASE_URL`) — nur beim Konten-Umzug
  ändern, siehe `KONTEN_UMZUG.md`

Personal (Zimmermädchen), Zimmerstatus und Tagesbetrieb laufen ohnehin **nicht**
über GitHub, sondern direkt in der App (Reiter „Personal" bzw. „Zimmer") —
dafür ist dieser Weg gar nicht nötig.
