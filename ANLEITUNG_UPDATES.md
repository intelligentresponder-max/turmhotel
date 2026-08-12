# Kleine Änderungen selbst veröffentlichen (ohne Entwickler)

Für Rezeption/Hausdame — kein Git, kein Terminal nötig. Alles läuft über die
GitHub-Webseite im Browser.

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
