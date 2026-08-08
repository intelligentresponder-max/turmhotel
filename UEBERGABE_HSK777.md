# TURMHOTEL HOUSEKEEPING — ÜBERGABE (Trigger: HSK777)

Stand: **08.08.2026, 03:30** · Letzter Commit: `f957979`
Diese Datei ist der Einstiegspunkt — egal ob am PC (Git Bash) oder am Handy (Termux).
Bei „HSK777": diese Datei lesen, dann bei Abschnitt 3 weitermachen.

## Wo alles liegt
- Repo: `github.com/intelligentresponder-max/turmhotel`
- Verteil-Tool: `https://bit.ly/turm7` → `housekeeping/housekeeping-v3.html`
- Scan-Tool: `https://bit.ly/turmhsk` → `housekeeping/alpha-scan.html`
- Cloud-Sync: Firebase RTDB, `state.json` / `staff.json`

## Hotel-Stammdaten
- Turmhotel Frankfurt, Eschersheimer Landstraße 20, 60322 Frankfurt
- Check-in 15:00 / Check-out 11:00 · Kontakt: rooms@turmhotel-fra.de
- PMS: Oracle Suite8 (End-of-Life, Ablösung durch Mews war Thema für Tanja)
- 73 vermietbare Zimmer: Vorderhaus 11–55 (zweistellig), Hinterhaus 102–510
  (101 = Massageraum, dazu zwei Tagungsräume)

---

## 1. Der tägliche Ablauf (so ist er gedacht)

1. Rezeption druckt am Ende der Spätschicht die **Alpha-Liste** („Gäste im Haus
   inkl. Anreisen"). Spätanreisen sind dann bereits erfasst.
2. Foto der Liste ins **Scan-Tool**. OCR liest Zimmer + Abreisedatum.
3. Doppelcheck: **Anz.-Summe** der Alpha-Liste und **Anreisen Zimmer** aus der
   Suite8-Verfügbarkeit eintragen. Beide Badges müssen grün sein.
4. Leerstehende Anreisezimmer in Karte 4 antippen (siehe 2.1).
5. CSV herunterladen → im Verteil-Tool: *Zimmerstatus zurücksetzen* → importieren
   → Personal prüfen → automatisch verteilen.
6. Zuteilung landet per Cloud-Sync auf den Handys der Zimmermädchen.

---

## 2. Vier Dinge, die man wissen muss

**2.1 Die Alpha-Liste kennt nur belegte Zimmer.**
Leerstehende Zimmer mit Anreise stehen dort strukturell nie drin. Sie ergeben
sich nur aus `Anreisen − Abreisen`. Dafür gibt es das Feld „Anreisen Zimmer
laut PMS" und die Auswahlliste in Karte 4.

**2.2 Zimmer aus dem Leerstand sind bereits sauber** — Ausnahme: Zimmer, die
auf **OOO** standen. Die kommen in den Verkauf zurück und sind *nicht*
automatisch sauber. Weder Alpha-Liste noch Scan-Tool kennen sie bisher.

**2.3 Doppelbuchungen kommen vor.** Zimmer 105 stand am 07.08. zweimal drin,
im PMS nicht löschbar, einmal mit `Anz. 0`. Suite8 zählt diese Zeile bei „Erw."
mit, bei „Anz." nicht — daher scheinbare Summenfehler. Das Scan-Tool
dedupliziert beim Einlesen.

**2.4 Der Dienstplan taugt nicht als Zahlenquelle.** Der vom 31.07. nannte für
Samstag 16 Abreisen und 32 Anreisen — tatsächlich 28 und 36. Für
Reinigungszahlen immer die **aktuelle Verfügbarkeit** heranziehen.
Notation im Plan: `K` = krank, `U` = Urlaub, `A` = frei.

---

## 3. Offene Punkte (Reihenfolge = Priorität)

**1. Feld „Housekeeping-Tag" — kritisch.**
Das Scan-Tool bestimmt „Abreise heute" über das Systemdatum des Geräts. Die
Alpha-Liste wird aber gegen **23:30 gedruckt und oft vor Mitternacht
gescannt**. Dann ist „heute" noch der Vortag, und alle Abreisen des Folgetages
werden als `Overnight` exportiert — die Verteilung wäre komplett verdreht.
Nach Mitternacht stimmt es zufällig, davor nicht.
Lösung: eigenes Datumsfeld, vorbelegt mit **morgen**, wenn es nach 18 Uhr ist.
Alles andere im Tool hängt an diesem Datum.

**2. Den Dateiweg abschaffen.**
CSV herunterladen und wieder auswählen ist ein PC-Ablauf. Am Handy findet der
Browser die Dateien nicht zuverlässig wieder. Beide Tools sind Webseiten — die
Datei ist eine Krücke.
- *Kurzfristig:* Button „Ergebnis kopieren" im Scan-Tool. Das Verteil-Tool hat
  unter „⚡ JSON-Funktion" bereits ein Einfügefeld samt Zwischenablage-Button.
- *Sauber:* Button „Direkt übernehmen", der das Ergebnis in dieselbe Firebase-DB
  schreibt, über die ohnehin synchronisiert wird. Das Verteil-Tool meldet dann
  „Neue Liste vom Scan-Tool — übernehmen?".
- *Langfristig:* beide Seiten zu einem Reiter zusammenlegen, dann entfällt die
  Übergabe ganz.

**3. Bettenzahl mitführen.**
Die Alpha-Liste hat die Spalte `Erw.` (1/2/3). Das Zimmermädchen muss wissen,
wie viele Betten zu beziehen sind. Der JSON-Weg im Verteil-Tool kann das
bereits (`type`: E/D/T), der CSV-Weg wirft die Information weg.

**4. Kinder erfassen.**
Spalte `Kin.` der Alpha-Liste — Zusatz- oder Kinderbett. Wird derzeit gar nicht
gelesen.

**5. OOO-Rückläufer sichtbar machen.**
Am 07.08. stand ein Zimmer auf OOO, am 08.08. nicht mehr. Solche Zimmer
brauchen eine Reinigung, tauchen aber nirgends auf.

**6. Personal schnell abwählen.**
Häkchen „heute nicht da" statt Löschen und Neuanlegen. Am 08.08. fielen zwei
Kräfte kurzfristig krank aus.

**7. Kleineres**
- Verfügbarkeitszahlen in den Übergabebericht des Tools ziehen, damit die
  Hausdame Spitzentage früh sieht (z. B. 48 Abreisen am 09.08.).
- Chips in Karte 4 nach Vorder-/Hinterhaus gruppieren — bei 23 freien Zimmern
  derzeit unübersichtlich.
- Handbuch-Kapitel „Vorbereitung" kennt die neuen Karten 4 und 5 noch nicht.
- Aus der alten Roadmap offen: Arbeitszeit-Tracking, Mängel-Report,
  Technik-Report für den Hausmeister.

### Worauf beim Import zu achten ist
- **Immer zuerst „Zimmerstatus zurücksetzen"**, sonst addiert sich der Vortag
  dazu (war ein echter Bug, behoben am 05.08. — der Reset ist seitdem Pflicht).
- **Anz.-Summe und Anreisenzahl gegenprüfen**, bevor verteilt wird. Beide
  Badges grün, dann erst verteilen.
- **Der JSON-Import setzt jedes Zimmer auf `checkout`.** Für die reine
  Abreiseliste richtig, aber Overnight-Zimmer kommen darüber nicht ins Tool.
  Solange das so ist, bleibt CSV der Weg für den vollständigen Tag.
- **Zimmernummern ohne führende Null.** Das Verteil-Tool kennt `24`, nicht
  `024`. Scan-Tool und `parseCsv()` schneiden sie inzwischen ab, fremde
  CSV-Dateien nicht unbedingt.

---

## 4. Was in der Nacht 07./08.08. gemacht wurde

| Commit | Inhalt |
|---|---|
| `d36486d` | Gebäude-Label `Vorderhaus (Nebenhaus)` → `(Haupthaus)` |
| `945fdb7` | Anreisen-Abgleich, Dubletten-Filter, Status-Spalte im CSV; CSV-Import in `housekeeping-v3.html` gegen führende Nullen gehärtet |
| `d0944e9` | Auswahlliste der freien Zimmer (73 Zimmer hinterlegt) |
| `f957979` | Leerstandszimmer als `Overnight` statt `Abreise` |

Erster Echttest des Scan-Tools mit zwei Fotos einer Alpha-Liste (07.08.2026)
plus Verfügbarkeits-Auszug. Kontrollsummen gingen auf: 80 Erwachsene,
2 Kinder, 50 Zimmer; 28 Abreisen — identisch mit der Zeile „Abreisen Zimmer"
in Suite8.

---

## 5. Arbeitsregeln

Vor **jedem** Push die Syntaxprüfung:

```bash
sed -n '/<script>/,/<\/script>/p' DATEI.html | grep -v '<script>\|</script>' > ~/hk.js
node --check ~/hk.js
```

Bei Desync **nicht blind** `git reset --hard origin/main`. Erst
`git log --oneline -3` und `git show HEAD` — in der Nacht zum 08.08. wäre so
beinahe der Label-Commit verlorengegangen. Erst prüfen, dann `git pull --rebase`.

Am Handy gibt es kein `~/downloads`; Downloads liegen unter
`~/storage/downloads` (= `/storage/emulated/0/Download`). Wenn eine Datei dort
nicht ankommt: Änderung stattdessen als Patch-Skript einfügen und ausführen.
Mehrere `cp`-Zeilen immer mit `&&` verketten, sonst läuft ein Commit auch
dann durch, wenn das Kopieren fehlgeschlagen ist.
