# 🏨 TURMHOTEL HOUSEKEEPING — ÜBERGABE (Trigger: HSK777)

Stand: 12.07.2026 · Zweck dieser Übergabe: Tool mit echten Daten füttern (Gästeliste, Zimmer, Personal)

## Wo das Tool liegt
Repo: `github.com/intelligentresponder-max/turmhotel`
Live: `https://intelligentresponder-max.github.io/turmhotel/housekeeping/housekeeping-v3.html`

## Was das Tool laut letztem Stand kann (aus früheren Sessions)
- **77-Zimmer-Grid** — Haupthaus + Nebenhaus
- **JSON-Import** der Gästeliste über ein Format namens `processGuestListScan`
- **Foto-Upload** via Claude Vision (Zimmer-Fotos direkt einlesbar)
- **Staff-System** — Mitarbeiter mit Avataren, Farben, VZ/TZ-Badges (Vollzeit/Teilzeit)
- **3-Klick-Completion-Flow** — Zimmer als fertig markieren
- **Zimmertyp-Badges** — SDH/SDS/STS/STH/LGH
- **Trilingual** — Deutsch/Englisch/Ungarisch
- **Facility Manager Board** — separater Bereich für Haustechnik
- **Staff-Handbuch** integriert

## Hotel-Stammdaten (zur Erinnerung)
- Turmhotel Frankfurt, Eschersheimer Landstraße 20, 60322 Frankfurt
- Check-in 15:00 / Check-out 11:00
- Kontakt: rooms@turmhotel-fra.de
- PMS: Oracle Suite8 (End-of-Life — Ablösung z.B. durch Mews war mal Thema für Owner Tanja)

## ⚠️ Wichtiger Hinweis für die nächste Session
Diese Übergabe basiert auf **Gedächtnis aus früheren Chats**, nicht auf einem frischen Blick in den aktuellen Code. Bevor mit dem Daten-Füttern losgelegt wird:

1. André bitten, den aktuellen Stand zu zeigen: `cat housekeeping-v3.html` (oder zumindest die Struktur/relevante Teile) — **nicht blind draufschreiben**, aus Erfahrung mit dem Sneaks4Seek-Projekt heute: alte/kaputte Dateiversionen sind ein reales Risiko
2. Klären: welches konkrete Daten-Format soll importiert werden? (JSON-Gästeliste, Zimmerliste, Personalliste — eins nach dem anderen)
3. Klären: manueller Import (einmalig Daten reinkopieren) oder soll ein wiederkehrender Workflow gebaut werden?

## Nächster Schritt beim Trigger "HSK777"
1. Diese Datei zeigen lassen / zusammenfassen
2. Fragen: "Was für Daten willst du reinfüttern — Gästeliste, Zimmerplan, oder Personal?"
3. Erst dann `cat` der relevanten Datei anfordern, dann loslegen
