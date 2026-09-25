# TURMHOTEL HOUSEKEEPING — ÜBERGABE (Trigger: HSK777)

Stand: **25.09.2026** · Letzter Commit: `5467ab9` (25.09.2026, Branch `claude/hsk777-aufraeumen-features`)
Diese Datei ist der Einstiegspunkt — egal ob am PC (Git Bash) oder am Handy (Termux).
Bei „HSK777": diese Datei lesen, dann bei Abschnitt 3 weitermachen.

> **Pflicht:** Wer pusht, aktualisiert hier das Datum „Stand" und den letzten
> Commit. Zwischen 08.08. und 25.09. wurde das versäumt (siehe Abschnitt 5, F1).

## Wo alles liegt
- Repo: `github.com/intelligentresponder-max/turmhotel`
- Verteil-Tool (**Hauptwerkzeug**, enthält seit v3.9 auch den Foto-Scan):
  `https://bit.ly/turm7` → `housekeeping/housekeeping-v3.html`
- Scan-Tool (nur noch **Fallback**): `https://bit.ly/turmhsk` → `housekeeping/alpha-scan.html`
- Team-Anleitung: `Gebrauchsanweisung-Housekeeping-App.pdf` (DE/EN/HR/HU/AF)
- Cloud-Sync: Firebase RTDB, `state.json` / `staff.json`, Archiv unter `/history/<Datum>.json`
- Konto-Umzug und Updates: `KONTEN_UMZUG.md`, `ANLEITUNG_UPDATES.md`
- Alte Patch-Skripte: `scripts/` · alte Backups: `archiv/`

## Hotel-Stammdaten
- Turmhotel Frankfurt, Eschersheimer Landstraße 20, 60322 Frankfurt
- Check-in 15:00 / Check-out 11:00 · Kontakt: rooms@turmhotel-frankfurt.de
- PMS: Oracle Suite8 (End-of-Life, Ablösung durch Mews war Thema für Tanja)
- 73 vermietbare Zimmer: Vorderhaus 11–55 (zweistellig), Hinterhaus 102–510
  (101 = Massageraum, dazu zwei Tagungsräume)

## Status Einführung
Tool inkl. Scan ist mit dem Team getestet und einsatzbereit. Die **offizielle
Einführung steht aus**, bis Tanja wieder ansprechbar ist.

---

## 1. Der tägliche Ablauf (Stand v3.9)

1. Rezeption druckt am Ende der Spätschicht die **Alpha-Liste** („Gäste im Haus
   inkl. Anreisen"). Spätanreisen sind dann bereits erfasst.
2. `bit.ly/turm7` öffnen → **Zimmerstatus zurücksetzen** (archiviert den
   Vortag automatisch in den Verlauf).
3. Reiter „Gästeliste" → **Foto-Scan**: bis zu 3 Seiten fotografieren.
   Der **Housekeeping-Tag** wird aus dem Listenkopf gesetzt (Listendatum + 1),
   manuell überschreibbar.
4. Doppelcheck: **Anz.-Summe** der Alpha-Liste und **Anreisen Zimmer** aus der
   Suite8-Verfügbarkeit eintragen. Beide Badges müssen grün sein.
5. Leerstehende Anreisezimmer über die Chips antippen (siehe 2.1), jetzt nach
   Vorder-/Hinterhaus gruppiert. Ex-OOO-Rückläufer stehen separat, rot markiert
   (siehe 2.2).
6. **Auf Zimmer übertragen** → Vorschau prüfen → übertragen. Kein CSV mehr nötig.
7. Personal prüfen (**„heute nicht da"** statt löschen) → automatisch verteilen.
8. Zuteilung landet per Cloud-Sync auf den Handys („Meine Zimmer").

### Referenzwerte letzte geprüfte Liste (24.09. → HK-Tag 25.09.)
71 Zimmer · 80 Erwachsene · 0 Kinder · 38 Abreisen · 33 Overnight.
Summenzeile der Liste = Zeilenzahl → Scan-Grundlage stimmt.

---

## 2. Was man wissen muss

**2.1 Die Alpha-Liste kennt nur belegte Zimmer.**
Leerstehende Zimmer mit Anreise stehen dort strukturell nie drin. Sie ergeben
sich nur aus der Suite8-Zahl „Anreisen Zimmer". Dafür gibt es das Feld
„Anreisen Zimmer laut PMS" und die Leerstand-Chips.

**2.2 Zimmer aus dem Leerstand sind bereits sauber** — Ausnahme: Zimmer, die
auf **OOO** standen. Die kommen in den Verkauf zurück und sind *nicht*
automatisch sauber. **Seit `5467ab9` kennt das Tool sie:** Zimmer-Modal hat
einen Betriebsstatus-Toggle (Im Verkauf / Außer Betrieb), im Foto-Scan gibt
es eine eigene, rot markierte Chip-Gruppe „Ex-OOO-Rückläufer" unterhalb der
normalen Leerstand-Chips. Auswahl dort erzwingt beim Übertragen `checkout`
(= braucht Reinigung) statt `overnight` (= gilt als sauber) und löscht das
OOO-Flag automatisch.

**2.3 Doppelte Zimmerzeilen — zwei verschiedene Fälle.**
*Fall 1 (Datenfehler):* Zimmer im PMS über das Kontextmenü zusätzlich angelegt
und darauf gebucht — Gast doppelt gezählt (07.08., Zimmer 105).
*Fall 2 (Sharing):* Messe-/Geschäftskunden teilen sich ein Zimmer als
gleichwertige Mieter — korrekt.
Fürs Housekeeping beides: ein Zimmer, einmal reinigen (Tool dedupliziert).
**Seit `5467ab9` meldet der Doppelcheck das nicht mehr als Fehler:** die
Anz.-Summe wird gegen `erkannte Zimmer + entfernte Dubletten` geprüft statt
gegen `erkannte Zimmer` allein. Bewusst **keine statische Ausnahmeliste** mit
Zimmernummern gebaut — Sharing-Partner wechseln laufend, eine feste Liste
wäre in ein paar Wochen veraltet und müsste manuell gepflegt werden.

**2.4 Der Dienstplan ist ein Planungsstand, keine Ist-Zahl.**
Für Reinigungszahlen immer die **aktuelle Verfügbarkeit** heranziehen.
Notation im Plan: `K` = krank, `U` = Urlaub, `A` = frei.

**2.5 `occupied` und `guestType` gehören zusammen.**
Bug vom 12.08. (243d5d5): JSON- und manueller Import setzten nur `guestType`,
die Statusleiste zeigte „0 belegt". Behoben auf Schreib- *und* Leseseite.
Neue Importwege müssen beide Felder setzen.

---

## 3. Offene Punkte (Reihenfolge = Priorität)

Alle fünf Punkte aus der letzten Übergabe sind mit `5467ab9` erledigt (Details
siehe 2.2/2.3 und Verlauf-Tabelle). Aktuell keine neuen offenen Punkte aus
dieser Runde — folgendes bleibt aus der alten Roadmap liegen:

- Alte Roadmap: Arbeitszeit-Tracking, Mängel-Report, Technik-Report Hausmeister.
- `alpha-scan.html` ist jetzt klar als Fallback gekennzeichnet (Banner) —
  langfristiges Abschalten steht weiter aus, bis niemand mehr darauf angewiesen ist.
- Bettenzahl/Kinder werden nur bei der zeilenweisen OCR-Erkennung (≥5 Zimmer
  pro Aufnahme) mitgelesen, nicht im „spaltenweise gelesen"-Fallback-Pfad bei
  schlechten Aufnahmen — dort bleiben Erw./Kin. leer und müssen von Hand
  nachgetragen werden (Tabelle ist dafür editierbar).

### Erledigt seit 08.08. (aus der alten Liste)
- ~~Housekeeping-Tag-Feld~~ → v3.8 / v3.9 (Datum aus Listenkopf, überschreibbar)
- ~~Dateiweg abschaffen~~ → v3.9, Scan direkt im Manager
- ~~Personal „heute nicht da"~~ → v3.7 Team-Dienstplan
- ~~Vergangene Tage weg nach Reset~~ → Verlauf-Tab mit Firebase-Archiv

### Erledigt seit 07.09. (diese Übergabe, `5467ab9`)
- ~~Bettenzahl mitführen~~ → Erw.-Spalte wird im Foto-Scan gelesen, Zimmertyp-
  Badge E/D/T wie beim JSON-Import, editierbar in der Zeilen-Tabelle.
- ~~Kinder erfassen~~ → Kin.-Spalte wird gelesen, „+Kind"-Badge am Zimmer.
- ~~OOO-Rückläufer sichtbar machen~~ → Betriebsstatus-Toggle im Zimmer-Modal +
  eigene „Ex-OOO"-Chip-Gruppe im Foto-Scan, erzwingt Reinigung.
- ~~Ausnahmeliste Sharing~~ → Doppelcheck rechnet entfernte Dubletten automatisch
  mit ein statt eine Ausnahmeliste zu pflegen (siehe 2.3).
- ~~Kleineres~~ → Verfügbarkeitszahlen im Übergabebericht, Leerstand-Chips nach
  Vorder-/Hinterhaus gruppiert, Handbuch Kapitel 1 umgeschrieben, `alpha-scan.html`
  als Fallback gekennzeichnet.

### Worauf beim Import zu achten ist
- **Immer zuerst „Zimmerstatus zurücksetzen"**, sonst addiert sich der Vortag.
- **Beide Badges grün**, dann erst verteilen.
- **Der JSON-Import setzt jedes Zimmer auf `checkout`** — Overnight kommt darüber
  nicht ins Tool. Für den vollständigen Tag: Foto-Scan oder CSV.
- **Zimmernummern ohne führende Null.** `24`, nicht `024`. Scan und `parseCsv()`
  schneiden sie ab, fremde CSV-Dateien nicht unbedingt.

---

## 4. Verlauf der Arbeiten

| Datum | Commit | Inhalt |
|---|---|---|
| 08.08. | `d36486d`–`f957979` | Anreisen-Abgleich, Dubletten-Filter, Leerstand-Chips, Leerstand = Overnight |
| 08.08. | `a1977ca` | Kamera: bis zu 3 Seiten, Datum aus Listenkopf |
| 09.08. | `4eaf153` | v3.5 Prüfung + Ampel, v3.6 „Meine Zimmer" |
| 09.08. | `d6a8641` | v3.7 Ausrichtung, Seitenmodus, Team-Dienstplan |
| 09.08. | `75b0985` | v3.8 Jahr aus Listenkopf, Zeilenanfang repariert |
| 12.08. | `6871e33` | Update- und Konten-Umzugsanleitung, Firebase-URL konsolidiert |
| 12.08. | `babfcd2`, `f420595` | Scan: Anreisen/Abreisen-Formel, OCR-Trennzeichen-Toleranz |
| 12.08. | `243d5d5` | Fix „0 belegt" (occupied/guestType) |
| 12.08. | `f11d75a` | Verlauf-Tab, Archiv beim Reset |
| 12.08. | `526d1f8` | **v3.9** Foto-Scan direkt im Manager |
| 12.08. | `d614e01` | Team-Gebrauchsanweisung DE/EN/HR/HU/AF |
| 26.08. | `7120c6e`, `bfe730e`, `59b1cea` | Gästeportal: Revert WLAN-Leak, Late Check-in, Impressum |
| 07.09. | `1c9466c` | Merge PR #1 (Gebrauchsanweisung-PDF) |
| 25.09. | `5467ab9` | Aufräumen (Skripte → `scripts/`, Backup → `archiv/`, `main` gelöscht) + Bettenzahl/Kinder im Foto-Scan + OOO-Rückläufer-Chips + Doppelcheck-Fix für Sharing + Verfügbarkeit im Übergabebericht + Vorder-/Hinterhaus-Gruppierung + Handbuch v3.9 |

---

## 5. Fehlerprotokoll (einmal gemachte Fehler — nicht wiederholen)

| # | Fehler | Folge | Gegenmaßnahme |
|---|---|---|---|
| F1 | UEBERGABE nach Sessions vom 09.08./12.08. nicht aktualisiert | HSK777 zeigte 6 Wochen alten Stand, erledigte Punkte als offen | Datum/Commit hier vor dem letzten Push prüfen (Pflicht, auch in DEPLOY-ROUTINE) |
| F2 | Escaped Backticks (`\``, `\${`) im Script | ganzes Script stirbt lautlos | Syntaxcheck vor jedem Push; Fix: `sed -i 's/\\`/`/g; s/\\${/${/g'` |
| F3 | `housekeeping-v3.backup.html` enthielt F2 | irreführende tote Kopie im Live-Ordner | Backups nie in `housekeeping/`, sondern `archiv/`; besser: Git-Historie statt Backup-Datei |
| F4 | CSV-Import addierte statt zu ersetzen (05.08.) | Vortagszimmer doppelt | Reset ist Pflichtschritt, Reset archiviert jetzt |
| F5 | `occupied`/`guestType` getrennt gesetzt (12.08.) | „0 belegt" trotz Zuteilung | siehe 2.5 |
| F6 | WLAN-Passwort öffentlich im Gästeportal (26.08.) | Sicherheitsleck | Revert; vor Push `grep -i "passw\|wlan" *.html` |
| F7 | Blindes `git reset --hard` (08.08.) | Label-Commit fast verloren | erst `git log`/`git show`, dann `pull --rebase` |
| F9 | Leere Datei `main` im Repo-Root (seit 12.07., vermutlich Tippfehler bei `git push … main` mit `>`) | Ballast, verwirrt | gelöscht 25.09.; vor `git add -A` immer `git status` lesen |
| F8 | Scan vor Mitternacht mit Gerätedatum | Abreise/Overnight vertauscht | HK-Tag aus Listenkopf (v3.8) |

---

## 6. Arbeitsregeln

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
