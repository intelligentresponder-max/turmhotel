# AUFTRAG FÜR CLAUDE CODE — HSK777 · 09.10.2026

Ablage: `turmhotel/AUFTRAG_CLAUDE_CODE_2026-10-09.md` (neben `UEBERGABE_HSK777.md`).
Wer fertig ist, trägt Ergebnisse in `UEBERGABE_HSK777.md` ein (Stand, Commit, F-Nummern).

## 0. Zuerst (Pflicht, wegen F21)
```bash
git fetch origin && git log --oneline HEAD..origin/main
cat UEBERGABE_HSK777.md        # F-Nummer aus dieser Datei ableiten (letzte war F23)
git status                     # vor jedem git add -A (F9)
```
Vor jedem Push: Syntaxcheck (F2) und `grep -i "passw\|wlan" *.html` (F6).
Das Repo ist **öffentlich**: keine Gästenamen, Preise, PINs, Fotos oder Testlisten mit Namen einchecken (F16).

## 1. Was André heute (09.10., 02:22–02:31) gemeldet hat
1. Tool wirkt „zurückgesetzt": 0 belegt, 73 frei, Personal da, aber alle „heute nicht da".
2. Personal bleibt browserübergreifend erhalten — **die noch nicht zugeordnete Liste (Foto-Scan-Ergebnis) war weg**.
3. Meldung „Erst Gästeliste importieren." beim Verteilen (Folge von 1/2).
4. Screenshot 1 läuft auf `sponder-max.github.io`, Screenshot 2 auf `intelligentresponder-max.github.io` — **zwei Herkunftsadressen**.

## 2. Befunde aus meiner Code-Durchsicht (Stand origin/main, nicht live getestet)
| # | Befund | Beleg |
|---|---|---|
| B1 | **Scan-Ergebnis liegt nur im Arbeitsspeicher.** `scanRows`, `scanPages`, `scanLastVerfuegbarkeit` sind reine `let`-Variablen, nirgends in localStorage/IndexedDB/Firebase gesichert. Tab-Reload, Speicherlimit (siehe F11), Browserwechsel = Liste weg. | `let scanRows = []` (Zeile ~1809), keine Speicherung |
| B2 | **Zwei Deployments.** localStorage ist pro Herkunftsadresse getrennt. Falls unter `sponder-max.github.io` eine ältere Kopie läuft, hängt sie evtl. an derselben Firebase-DB und hat noch `seedNotes()` (F23) — das würde den Cloud-Stand mit drei Notizen überschreiben. | URL in Screenshot 1; `KONTEN_UMZUG.md` existiert |
| B3 | **Schreiben vor erstem Sync.** Massenaktionen (`saveState` ohne `changedRoom`) machen `PUT` des lokalen Stands. Ein frischer Browser mit leerem Stand ersetzt die Cloud, wenn er schreibt, bevor `syncFromCloud()` fertig ist. | `saveState`, `resetAll`, `syncFromCloud` |
| B4 | `resetAll()` löscht Zimmer + Personal + Gästeliste **für alle Handys** (PUT), Rückfrage erwähnt das nicht (in F23 schon als offen vermerkt). | `resetAll()` |
| B5 | Nach „Reset" sind alle Personen „heute nicht da" (Feld `da`) — Verteilen schlägt dann leise fehl. | Screenshot 1, `toggleDa` |
| B6 | `alpha-scan.html` ist nur noch Redirect (OK, in Übergabe dokumentiert). | Datei 2,3 KB |

**Aufgaben dazu**
1. Klären, **welche Adresse die richtige ist** und ob `sponder-max.github.io/...` eine eigene Kopie ist. Wenn ja: Kopie auf denselben Stand bringen oder abschalten (Redirect auf die kanonische URL). Prüfen, ob dort `seedNotes()` noch aktiv ist. Ergebnis in `KONTEN_UMZUG.md` eintragen.
2. Cloud prüfen (`/state.json?shallow=true`, `/staff.json`, `/history?shallow=true`): Wie viele Zimmer stehen drin, wann wurde zuletzt geschrieben? Das beantwortet, ob die Cloud selbst geleert wurde oder nur ein Browser.
3. **Sync-Gate:** keine Schreibaktion (PUT/PATCH) bevor der erste `syncFromCloud()` erfolgreich war; Schaltflächen bis dahin sperren, kleiner Hinweis „lädt …".
4. **Sicherung vor Massenschreiben:** vor jedem `PUT` des ganzen Stands den bisherigen Cloud-Stand nach `/backup/state-letzter.json` kopieren (eine Ebene reicht). Dazu ein Knopf „Letzten Stand wiederherstellen" nur im Fehlerfall (Banner), nicht als Dauerfunktion.
5. **Scan-Entwurf persistieren (löst B1):** Zustand des Foto-Scans (nur `zimmer, abreise, leer, exOOO, reserve, betten/erw, kinder`, Listendatum, HK-Tag, PMS-Zahlen) lokal in IndexedDB **und** per Firebase unter `/scanEntwurf.json` ablegen; beim Laden wiederherstellen; nach „Auf Zimmer übertragen" löschen. **Keine Namen, keine Preise.** Alle Handys sehen denselben Entwurf.
6. Reset-Rückfrage ehrlich formulieren („gilt für ALLE Handys") — oder Reset ganz entfernen (siehe 3).
7. Nach „Reset"/„Neuer Tag": Personal behalten **und** `da` auf den Dienstplan-Stand lassen statt alles auf „nicht da" zu setzen — oder bewusst fragen. Verhalten festlegen, dokumentieren.

## 3. Funktions-Inventur — unnötige Admin-Funktionen entfernen
André: „Nicht notwendige administrative Funktionen sollen verschwinden!!!"

**Vorgehen:** Erst eine Tabelle aller 115 Funktionen + Buttons/Tabs erzeugen (Name · wo erreichbar · wer braucht sie · Entscheidung). Dann entfernen. Entfernen heißt: UI **und** toten Code löschen; Git-Historie ist das Backup (F3: keine Backup-Dateien im Live-Ordner). Nach jedem Entfernen Syntaxcheck + Klicktest bei 390 px.

**Kernfunktionen — bleiben:** Zimmer-Grid, „Meine Zimmer" mit „Fertig", Foto-Scan/PDF-Import inkl. Doppelcheck, „Auf Zimmer übertragen", Personal anlegen + „heute da/nicht da", automatisch verteilen (paritätisch), Übergabebericht, Sync-Banner.

**Kandidaten zum Entfernen (Vorschlag, bitte jeweils prüfen, ob etwas daran hängt):**
| Kandidat | Vorschlag | Grund |
|---|---|---|
| Button „Reset" (alles) | **entfernen** | zerstört Stand auf allen Handys (B4, F23) |
| „⬇ Stand exportieren" / JSON-Import | entfernen | Cloud-Sync ersetzt es; JSON-Import setzt alles auf `checkout` (Übergabe 3.) |
| Link „FACILITY" im Kopf | entfernen oder auf Rolle beschränken | andere Anwendung (`facility.html`), nicht Teil des Verteilens |
| CSV-/Datei-Importwege, manuelles Gästelisten-Eintippen | entfernen, falls Foto/PDF-Import vollständig | Datei-Weg am Handy unbrauchbar (Übergabe 08.08.) |
| Rotes „X" zum Personal löschen | durch „heute nicht da" ersetzen / hinter Bestätigung | versehentliches Löschen |
| Farbwahl für Personal (`COLORS`) | prüfen — nur behalten, wenn Zuordnung ohne Farbe unklar wird | Kosmetik |
| Tab „Verlauf" (+ `/history`-Archiv) | **André fragen** | nützlich für Tanja? sonst Archiv nur im Hintergrund |
| Tab „Übersicht" | **André fragen** | Statistik; evtl. in Übergabebericht aufgehen lassen |
| `nachtdienst`-Handoff-Block „Späte Anreisen" | behalten | Teil des Ablaufs (F19/F20) |
| `vorfuehrung.html`, Demo-/Handbuch-Seiten | nicht anfassen | andere Aufgabe |

Ergebnis: kurze Liste „entfernt / behalten / offen" in die Übergabe, eigener Commit je Themenblock.

## 4. Foto-Scan: Erw./Kin. sicher lesen (spart das Nachtragen der Belegung)
**Die Spalten in der Alpha-Liste:** `Z.Nr · Name · Status · Anreise · Abreise · Erw. · Kin. · Anz. · Kat. · Preis · Preiscode`. `Anz.` = Zimmeranzahl der Zeile (normal 1), `Erw./Kin.` = Personen. Die **letzte Zeile der letzten Seite** enthält die Summen: bei der Liste vom 08.10.2026 `81 · 0 · 63` = Σ Erw. · Σ Kin. · Σ Anz. (63 belegte Zimmer, 10 von 73 leer).
Stand heute laut Übergabe: Zimmer/Abreise 71/71 korrekt, Erw./Kin. bei ≈ 6 % der Zeilen nicht lesbar („0" als „)"). Zeilenweise Regex auf dem OCR-Text ist die Schwachstelle.

**Verbesserungen, in dieser Reihenfolge prüfen:**
1. **Summenzeile als Prüfsumme.** Fußzeile (Erw./Kin./Anz.) mitlesen, mit Σ der erkannten Zeilen vergleichen. Fehlt in genau einer Zeile ein Wert, ist er rechnerisch bekannt (Fußzeile − Σ übrige) → vorbefüllen und **gelb markieren** („errechnet"). Bei mehreren Lücken nur Warnung. Prüfen, ob die Erw.-Summe schon gelesen wird (Anz.-Summe wird es).
2. **Spaltenbasiert statt Regex:** Tesseract-Wortpositionen (TSV/`words` mit Bounding-Box) nehmen, die Spaltenköpfe `Erw.`, `Kin.`, `Anz.` suchen und Ziffern anhand der x-Position zuordnen. Das behebt „Ziffern kleben an Fehlzeichen" (F10) und gilt auch im bisherigen „spaltenweise"-Fallback.
3. **Nur Zahlenspalten an OCR geben:** Bild auf Z.Nr + Anreise/Abreise + Erw./Kin./Anz. zuschneiden und mit Ziffern-Whitelist lesen. Vorteil: bessere Trefferquote **und** Namen/Preise werden gar nicht erst verarbeitet (Datenschutz).
4. **Kategorie (`Kat.`)** nicht aus dem Foto, sondern aus dem Zimmerbestand ableiten (feste Zuordnung); Kat. nur als Plausibilitätsprüfung (z. B. Suite mit 3 Erw. ist plausibel).
5. **Plausibilitätsmarker** in der Tabelle: `Erw. = 0` (kommt echt vor, s. Zi. 34 unten — **nicht als Lesefehler behandeln, aber markieren**), `Erw. ≥ 3` (Zusatzbett), `Kin. > 0` (Kinderbett/Extras), Abreise vor Anreise.
6. **PDF vor Foto empfehlen:** Der Text-PDF-Weg (v3.12) ist exakt, ohne OCR. In der Oberfläche klar als bevorzugt zeigen, Foto als Fallback.
7. Anzeige am Zimmer: Personenzahl groß/lesbar („2 Erw." / „+1 Kind"), damit niemand die Belegung nachtragen muss; manuelles Nachtragen nur noch als Korrektur.

**Testfall (anonymisiert, Foto André 08.10.2026, Seite 2 von 2, Druck 22:02) → HK-Tag 09.10.2026**
| Zi. | Status | Anreise | Abreise | Erw. | Kin. | → HK |
|---|---|---|---|---|---|---|
| 303 | im Haus | 06.10. | 09.10. | 1 | 0 | Abreise |
| 110 | Eingecheckt | 08.10. | 09.10. | 1 | 0 | Abreise |
| 022 | Eingecheckt | 08.10. | 10.10. | 2 | 0 | Overnight |
| 103 | Eingecheckt | 08.10. | 10.10. | 1 | 0 | Overnight |
| 053 | Eingecheckt | 08.10. | 10.10. | 2 | 0 | Overnight |
| 405 | im Haus | 05.10. | 09.10. | 1 | 0 | Abreise |
| 034 | im Haus | 07.10. | 11.10. | **0** | 0 | Overnight (Erw. 0 markieren) |
| 044 | Eingecheckt | 08.10. | 09.10. | **3** | 0 | Abreise (Suite, 3 Pers.) |
| 108 | Eingecheckt | 08.10. | 10.10. | 1 | 0 | Overnight |
| 035 | im Haus | 07.10. | 10.10. | 2 | 0 | Overnight |
| 407 | Eingecheckt | 08.10. | 11.10. | 2 | 0 | Overnight |
| 308 | im Haus | 06.10. | 09.10. | 1 | 0 | Abreise |
| 102 | im Haus | 06.10. | 10.10. | 1 | 0 | Overnight |
| 033 | Eingecheckt | 08.10. | 11.10. | 2 | 0 | Overnight |
| 309 | Eingecheckt | 08.10. | 10.10. | 1 | 0 | Overnight |
| 209 | im Haus | 07.10. | 09.10. | 1 | 0 | Abreise |
| 207 | im Haus | 07.10. | 10.10. | 1 | 0 | Overnight |

Seite 2: 17 Zeilen · Σ Erw. = 23 · Σ Kin. = 0 · 6 Abreisen / 11 Overnight. Ganze Liste laut Fußzeile: 81 / 0 / 63. (Seite 1 fehlt mir — nicht erfunden.) Auffällig: Fußzeile ist nur auf der **letzten** Seite; bei „Seite x von y" prüfen, dass alle Seiten vorliegen, bevor die Prüfsumme gilt.
Als Testdatei nur **anonymisierte** Fassung (nur diese Spalten) ablegen, Original-Foto nie ins öffentliche Repo.

## 5. Alternativen — geprüft auf Nutzen / Sicherheit / neue Wege
| Frage | Option | Bewertung |
|---|---|---|
| Scan-Entwurf sichern | nur localStorage | bleibt im Browser, kein Wechsel zwischen Handys — **nicht genug** |
| | IndexedDB lokal | übersteht Reload, größere Daten — **ja, als lokale Schicht** |
| | Firebase `/scanEntwurf` | existiert bereits, Anonymous Auth + Regeln stehen (F13) — **ja, als geteilte Schicht**, nur Zimmerdaten |
| | Firestore/Supabase | mehr Funktionen, aber Umzug ohne Not — **nein** |
| OCR | Tesseract lokal (bleibt) | Fotos verlassen das Gerät nicht — **behalten** |
| | Cloud-Vision/LLM-API | genauer bei Tabellen, aber Gästenamen/Preise würden an Dritte gehen, API-Schlüssel im öffentlichen Seitencode — **nicht ohne DSGVO-Klärung/Server** |
| Eingabeweg | PDF (Text) statt Foto | exakt, kein OCR — **bevorzugen** |
| Sync-Schutz | Client-Gate + Backup-Kopie | wenig Aufwand, sofort wirksam — **ja** |
| | Firebase-Regeln mit `.validate` (z. B. kein Ersetzen von >10 Zimmern durch <5) | stärker, aber leicht falsch gesetzt → Aussperrung — **später, zuerst im Test** |
| Aufbewahrung | `/history` und `/backup` ohne Ablauf | Daten bleiben unnötig lange — **Aufbewahrung festlegen (z. B. 14 Tage, nur Zimmerdaten)** |

## 6. Fehlerprotokoll — Entwürfe (nach Verifikation in `UEBERGABE_HSK777.md` Abschnitt 5 eintragen, Nummern aus Datei ableiten)
- **F24** Scan-Ergebnis wurde nie gespeichert (reine JS-Variablen). Folge: Reload/Browserwechsel/Speicherlimit = Liste weg, während Personal (synchronisiert) blieb. Gegenmaßnahme: Entwurf in IndexedDB + `/scanEntwurf`, nach Übertragen löschen. *(Befund aus Code; Verhalten live noch nicht reproduziert.)*
- **F25** Zwei Herkunftsadressen für dasselbe Tool (`sponder-max.github.io` vs. `intelligentresponder-max.github.io`): localStorage getrennt, ältere Kopie kann denselben Cloud-Stand überschreiben. Gegenmaßnahme: eine kanonische URL, Kopie als Redirect. *(Hypothese, zu prüfen.)*
- **F26** Schreibzugriff vor dem ersten erfolgreichen Sync kann Cloud-Stand durch leeren Browser-Stand ersetzen. Gegenmaßnahme: Sync-Gate + Backup vor `PUT`. *(Hypothese, zu prüfen.)*
- **F27** (Übergabe-Disziplin) Handy-Screenshots zeigten „zurückgesetzt", obwohl F23 schon behoben war — Ursache offen. Bei jeder Rückmeldung „wieder weg" zuerst klären: welche URL, welcher Browser, Uhrzeit, Cloud-Inhalt prüfen — dann erst Code ändern.

## 7. Abnahme (Checkliste)
- [ ] Zwei Browser + zwei Handys: Personal anlegen, Scan machen, Reload → Entwurf und Personal bleiben.
- [ ] Frischer Browser (Inkognito) öffnet die Seite: Cloud-Stand unverändert (nach 30 s prüfen).
- [ ] Kein Schreiben vor erstem Sync; Banner bei Fehler sichtbar.
- [ ] Testfall aus Abschnitt 4: Erw./Kin. ohne Handarbeit korrekt, Prüfsumme grün.
- [ ] Entfernte Funktionen weg, Rest bei 390 px bedienbar, keine toten Handler (`node --check`, Konsole ohne Fehler).
- [ ] `grep` auf Namen/PINs/Passwörter im Repo leer.
- [ ] `UEBERGABE_HSK777.md` aktualisiert (Stand-Datum, Commit, F-Nummern, Liste „entfernt/behalten/offen").
