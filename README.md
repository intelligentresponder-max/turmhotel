# Turmhotel Frankfurt — Digitale Werkzeuge

Eigenentwicklung für den Betrieb des Turmhotel Frankfurt (73 Zimmer).
Alle Werkzeuge laufen als reine Webseiten ohne Server-Backend, gehostet über
GitHub Pages. Entwicklung und Betrieb: André Schwarz, Rezeption.

| Werkzeug | Zweck | Link |
|---|---|---|
| Housekeeping Manager v3 | Zimmerverteilung, Fertigmeldung, Übergabebericht | `bit.ly/turm7` |
| Alpha-Scan | Gästeliste per Foto einlesen, prüfen, exportieren | `bit.ly/turmhsk` |
| Gästeportal / Handbücher | Gästeinformation, Personalanweisungen | im Repo |

Einstiegspunkt für die Weiterarbeit: **`UEBERGABE_HSK777.md`**

---

## Versionsverlauf

### v3.7 — 09.08.2026 · Ausrichtung, Lesemodus, Team
Nachbesserungen aus dem ersten Nachtbetrieb.
- **Automatische Ausrichtung:** Das Werkzeug ermittelt an einer verkleinerten
  Kopie der ersten Seite, ob das Blatt quer fotografiert wurde, und dreht alle
  Seiten entsprechend. Im Test lieferte dieselbe Aufnahme ungedreht 23, gedreht
  63 verwertbare Zeilen.
- **Lesemodus der Texterkennung** auf einen zusammenhängenden Textblock
  festgelegt. Zuvor zerlegte die Erkennung die Tabelle selbständig in Spalten,
  wodurch Zimmernummer und Abreisedatum nie in derselben Zeile standen — die
  Hauptursache für fehlerhafte Zuordnungen.
- **Jahresprüfung verschärft:** Nur das Jahr der Liste und das Folgejahr sind
  zulässig. `2028` und `2022` sind häufige Fehllesungen von `2026`.
- **Summenzeile** wird auch erkannt, wenn Zeichenreste dahinterstehen.
- **Team-Dienstplan** im Housekeeping Manager hinterlegt, mit Häkchen
  „heute anwesend" statt Löschen und Neuanlegen bei Krankmeldungen.

### v3.6 — 09.08.2026 · Meine Zimmer
Eigene Ansicht pro Arbeitskraft, auf Wunsch des Housekeeping-Teams.
- Neuer Reiter **„Meine Zimmer"**: einmal den eigenen Namen antippen, das Gerät
  merkt ihn sich
- Nur die eigenen Zimmer, groß dargestellt, getrennt nach Abreisen
  (Vollreinigung) und Bleibern (auffrischen)
- Fertigmeldung durch einen einzigen Tipp auf das Zimmer, kein Suchen mehr im
  73er-Raster
- Zähler „x von y fertig"; Fortschritt erscheint unmittelbar in der Übersicht
  der Hausdame

### v3.5 — 08.08.2026 · Prüfung und Ampel im Scan-Tool
Erster Echtbetrieb hatte gezeigt, dass fehlerhafte Erkennung unbemerkt
durchlief. Seitdem lehnt das Werkzeug schlechte Aufnahmen aktiv ab.
- Bild wird vor der Texterkennung verdoppelt und in Graustufen gewandelt
  (Trefferquote im Test von 9 auf 40 erkannte Zimmernummern je Seite)
- Zeilenweiser Parser als Hauptweg; die alte spaltenweise Logik nur noch als
  Rückfall und dann mit ausdrücklicher Warnung
- Tolerante Datumserkennung mit Jahresreparatur aus dem Listenkopf — fängt
  Erkennungsfehler wie `09.08,202€`, `0708202`, `05.08:2026`
- Erkannte Zimmernummern werden gegen den echten Bestand von 73 Zimmern geprüft
- Anz.-Summe wird aus der Fußzeile gelesen und gegen die Zahl erkannter Zimmer
  gehalten
- **Ampel** über dem Export: bei Rot ist der CSV-Download gesperrt und die
  Meldung nennt den Grund

### v3.4 — 08.08.2026 · Mehrseitige Aufnahme (`a1977ca`)
- Bis zu drei Seiten nacheinander aufnehmen, als Miniaturen sichtbar, einzeln
  wieder entfernbar
- Gemeinsame Auswertung mit Fortschritt je Seite
- **Housekeeping-Tag** als eigenes Feld, automatisch aus dem Kopf der Liste
  gesetzt (Listendatum + 1 Tag). Behebt einen ernsten Fehler: Vor Mitternacht
  gescannte Listen hatten Abreisen und Bleiber vertauscht.

### v3.3 — 08.08.2026 · Leerstand und Abgleich (`945fdb7`, `d0944e9`, `f957979`)
- Feld **„Anreisen Zimmer laut PMS"**; das Werkzeug rechnet aus, wie viele
  leerstehende Anreisezimmer fehlen
- Auswahlliste aller Zimmer, die nicht auf der Gästeliste stehen — antippbar,
  bis die Rechnung aufgeht
- Leerstandszimmer werden als *Overnight* geführt, nicht als Vollreinigung:
  sie sind bereits sauber, sofern sie nicht auf OOO standen
- Dubletten-Filter beim Einlesen (dasselbe Zimmer kann im PMS doppelt
  erscheinen)
- CSV mit Status-Spalte, dadurch unabhängig von der Uhrzeit des Geräts
- Import in v3 gegen führende Nullen gehärtet (`024` gegen `24`)

### v3.2 — 08.08.2026 · Gebäudebezeichnungen (`d36486d`)
- Vertauschte Beschriftung Vorderhaus/Hinterhaus berichtigt

### v3.1 — 06.08.2026 · Alpha-Scan
- Eigenständiges Werkzeug zum Einlesen der Gästeliste per Foto
  (Texterkennung lokal im Browser, keine Daten verlassen das Gerät)
- Korrigierbare Tabelle, Doppelcheck gegen die PMS-Summe, CSV-Export

### v3.0 — 06.08.2026 · Cloud-Sync
- Zimmerstatus und Personal werden zwischen allen Geräten abgeglichen;
  jede Kraft sieht ihre Zuteilung auf dem eigenen Handy
- Oberfläche aufgeräumt, Übersetzungsschaltflächen entfernt

### v2 — 05.08.2026 · Verteilung und Übergabe
- Automatische, paritätische Verteilung: Abreise- und Bleiber-Zimmer getrennt
  reihum, damit jede Person eine vergleichbare Mischung erhält
- Druckbarer Übergabebericht für den Schichtwechsel
- Fehler behoben: CSV-Import addierte die Zimmer des Vortags, statt sie zu
  ersetzen. Seitdem ist „Zimmerstatus zurücksetzen" fester Bestandteil des
  Ablaufs.

### v1 — Juni/Juli 2026 · Grundlage
- Zimmerraster mit Status, Personalverwaltung, Notizen
- Handbücher für Rezeption und Housekeeping, digitales Gästeportal

---

## Als Nächstes

1. Dateiweg abschaffen: Ergebnis direkt übergeben statt CSV herunterladen und
   wieder auswählen; auf Dauer beide Werkzeuge in einer Oberfläche
2. Bettenzahl (Spalte `Erw.`) und Kinder (Spalte `Kin.`) mitführen — das
   Housekeeping muss wissen, wie viele Betten zu beziehen sind
3. OOO-Rückläufer sichtbar machen
4. Ausnahmeliste für doppelte Zimmerzeilen, damit Zimmer-Sharing bei Messen
   nicht als Fehler gemeldet wird
5. Aus der älteren Planung offen: Arbeitszeit-Tracking, Mängel-Report,
   Technik-Report für den Hausmeister

---

## Arbeitsregeln

Vor jedem Push die Syntaxprüfung:

```bash
sed -n '/<script>/,/<\/script>/p' DATEI.html | grep -v '<script>\|</script>' > ~/hk.js
node --check ~/hk.js
```

Bei abweichenden Ständen zwischen den Geräten nicht blind zurücksetzen —
erst `git log --oneline -3` und `git show HEAD`, dann `git pull --rebase`.
