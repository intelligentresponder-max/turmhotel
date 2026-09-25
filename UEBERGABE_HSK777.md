# TURMHOTEL HOUSEKEEPING — ÜBERGABE (Trigger: HSK777)

Stand: **25.09.2026** · Letzter Commit: `53b6735` (25.09.2026, Branch `claude/scan-speicher-fix`)
Diese Datei ist der Einstiegspunkt — egal ob am PC (Git Bash) oder am Handy (Termux).
Bei „HSK777": diese Datei lesen, dann bei Abschnitt 3 weitermachen.

> **Pflicht:** Wer pusht, aktualisiert hier das Datum „Stand" und den letzten
> Commit. Zwischen 08.08. und 25.09. wurde das versäumt (siehe Abschnitt 5, F1).

## Wo alles liegt
- Repo: `github.com/intelligentresponder-max/turmhotel`
- Verteil-Tool (**Hauptwerkzeug**, enthält seit v3.9 auch den Foto-Scan):
  `https://bit.ly/turm7` → `housekeeping/housekeeping-v3.html`
- Scan-Tool (**abgeschaltet seit 25.09.2026**): `https://bit.ly/turmhsk` →
  `housekeeping/alpha-scan.html` leitet automatisch auf `housekeeping-v3.html`
  weiter (Link bleibt so gültig, OCR-Logik dort ist entfernt)
- Team-Anleitung: `Gebrauchsanweisung-Housekeeping-App.pdf` (DE/EN/HR/HU/AF)
- Vorführungs-/Demo-Seite: `vorfuehrung.html` — Klick-Anleitung, Neuerungen,
  Verlinkung der Unterlagen; verlinkt in `manager.html`
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

**Gegenprobe mit Suite8 „Verfügbarkeit" (Screenshot von Amir, 24.09. abends):**
Alpha-Liste und PMS stimmen exakt überein — `Reservierungen`/`Def. Reservierungen`
für Do 24.09. = **71** (= Anz.-Summe der Liste), `Erwachsene im Haus` = **80**
(= Erw.-Summe), `Kinder im Haus` = **0** (= Kin.-Summe), `Abreisen Zimmer` für
Fr 25.09. (HK-Tag) = **38** (= gezählte Abreise-Zeilen). Damit ist die neue
Erw./Kin.-Erkennung aus 3.1/2.5 unabhängig gegen echte PMS-Zahlen bestätigt.

**Suite8-Verfügbarkeit die ganze Woche (24.09.–30.09., zum Vorausplanen):**

| Tag | Verfügbarkeit | Abreisen Zi. | Anreisen Zi. | Belegung | Kinder im Haus |
|---|---|---|---|---|---|
| Do 24.09. | 2 | 23 | 26 | 97,26 % | 0 |
| Fr 25.09. (HK-Tag) | 5 | 38 | 35 | 93,15 % | 0 |
| Sa 26.09. | 8 | 45 | 42 | 89,04 % | 0 |
| So 27.09. | 25 | 56 | 39 | 65,75 % | 1 |
| Mo 28.09. | 18 | 29 | 36 | 75,34 % | 2 |
| Di 29.09. | 8 | 28 | 38 | 89,04 % | 1 |
| Mi 30.09. | 6 | 20 | 22 | 91,78 % | 1 |

Ruhigster Tag der Woche: **So 27.09. mit 65,75 % Belegung** (25 freie Zimmer) —
für Personalplanung relevant. OOO/OOS laut PMS aktuell durchgehend 0.
Für das Doppelcheck-Feld „Anreisen Zimmer laut PMS" gilt die Zeile des
**HK-Tages**, nicht die des Listendatums (heute also 35, nicht 26).

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
- Bettenzahl/Kinder werden nur bei der zeilenweisen OCR-Erkennung (≥5 Zimmer
  pro Aufnahme) mitgelesen, nicht im „spaltenweise gelesen"-Fallback-Pfad bei
  schlechten Aufnahmen — dort bleiben Erw./Kin. leer und müssen von Hand
  nachgetragen werden (Tabelle ist dafür editierbar).
- **Mit echten Kamera-Fotos getestet (25.09., nach der Vorführung, F10):**
  Zimmer- und Abreise-Erkennung 71/71 fehlerfrei, inkl. aller 38 Abreisen zum
  HK-Tag. Erw./Kin. bei ca. 4 von 71 Zeilen (≈ 6 %) nicht lesbar, weil die
  Kamera-Texterkennung eine einzelne Ziffer als anderes Zeichen liest (z. B.
  „0" als „)"). Kein Bug, sondern OCR-Grenze — betroffene Zeilen sind in der
  Tabelle klar als „—" sichtbar und in Sekunden von Hand ergänzbar.

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

### Erledigt seit 25.09. (diese Übergabe)
- ~~Foto-Scan-Upload auf PDF erweitern (v3.12)~~ → Alpha-Liste kann jetzt als
  Text-PDF (Suite8 → „Microsoft Print to PDF") ohne OCR gelesen werden, dazu
  weiterhin als Foto (JPG/PNG/WEBP/HEIC) mit automatischer Ausrichtung je Seite,
  Blattzuschnitt und Kontrastaufhellung; Kamerazwang am Datei-Input entfernt
  (Galerie/Dateiauswahl wieder möglich); neuer Export „Als PDF speichern".
  Getestet mit echtem Chromium-Browser (Playwright) gegen die anonymisierte
  Alpha-Liste vom 25.09.: 70 Zimmer, 47 Abreise, 23 Overnight, Anz. 70, Erw. 96,
  Kin. 3, HK-Tag 26.09.2026 — alle Werte stimmen. PDF-Export liefert eine
  gültige A4-PDF (595×842 pt). **Noch nicht getestet:** echte Handyfotos/HEIC
  im Browser (kein Testgerät in dieser Sitzung verfügbar, siehe F14–F16).
- ~~`alpha-scan.html` abschalten~~ → eigenständige OCR-Logik entfernt, Datei
  leitet automatisch auf `housekeeping-v3.html` weiter, `bit.ly/turmhsk` bleibt
  dadurch gültig. Kachel aus `manager.html` entfernt.
- ~~Sync-Fehler unsichtbar~~ → rotes Banner + Last-Writer-wins bei Einzelzimmern
  entschärft (F12, `4d5435b`). **Weiterhin offen:** Firebase-Regeln selbst
  erneuern + Anonymous Auth einbauen — dafür fehlt der Web-API-Key aus der
  Firebase-Konsole (Project Settings → General), ohne den kann diese Session
  kein Sign-in-Request bauen. Sobald der Key da ist, siehe `CHECKLIST_HSK.md`
  Punkt 1.

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
| 25.09. | `6c6118b` | Neue Seite `vorfuehrung.html` (Klick-Anleitung + PDF-Verlinkung + Testergebnis), in `manager.html` verlinkt, `housekeeping-anleitung.html` mit Hinweis-Banner, README aktualisiert |
| 25.09. | `0388e22` | `alpha-scan.html` abgeschaltet (Redirect-Stub statt eigenständiger OCR-Logik), Kachel aus `manager.html` entfernt |
| 25.09. | `6f3c12f` | Echte Suite8-Verfügbarkeit (Amir) als Gegenprobe + Wochenübersicht in Referenzwerte dokumentiert |
| 25.09. | `c27db12` | Suite8-Wochenübersicht zusätzlich sichtbar auf `vorfuehrung.html` ergänzt |
| 25.09. | `a271cef` | Erw./Kin.-Regex robuster gegen OCR-Fehlerkennungen (F10), mit echten Fotos von der Vorführung getestet |
| 25.09. | `53b6735` | Foto-Scan-Speicherverbrauch bei großen Fotos begrenzt — behebt Tab-Reload/Datenverlust nach dem Scan (F11) |
| 25.09. | `4d5435b` | Firebase-Sync-Fehler sichtbar gemacht (rotes Banner), stillen Datenverlust bei `Permission denied` behoben (F12), PATCH statt PUT für die vier Einzelzimmer-Aktionen (Last-Writer-wins entschärft) |

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
| F10 | Erw./Kin.-Regex (25.09.) hatte `\b` am Zeilenende — bei OCR-Fehlerkennung klebt die Anz.-Ziffer oft ohne Leerzeichen an der nächsten Fehlerkennung (z.B. „1 0 14." statt „1 0 1 LGS") | Bei ca. 10 % der Zeilen (7 von 71 im Echttest) blieb Erw. leer, obwohl die Ziffer im Text stand | `\b` entfernt (25.09., zweiter Fix) → nur noch 4 von 71 Zeilen betroffen, siehe 3.1. Getestet mit `tesseract-ocr-deu` (Ubuntu-Paket) gegen die echten Fotos vom 25.09., nicht nur mit sauberem Text |
| F11 | `scanBildAufbereiten` verdoppelte jedes Foto mit Breite < 2000px ungedeckelt — ein normales Handyfoto einer vollen A4-Seite (z.B. 1475×2048) wurde zu einem 2950×4096-Graustufen-Canvas (~12 MP) samt eigener ImageData-Kopie und Tesseract-WASM-Speicher fürs selbe Bild | Handy lief nach korrekt eingelesenen Zimmer-/Abreisedaten in ein Speicherlimit, Tab lud neu, komplette Auswertung (noch nicht übertragen) war weg | Lange Kante nach Verdoppelung auf max. 3000px gedeckelt (25.09.). Mit den echten Fotos erneut getestet: Zimmer/Abreise weiter 71/71 bzw. 38/38 korrekt, Erw.-Erkennung minimal schwächer (6 statt 4 von 71 offen) — vertretbarer Tausch gegen die Speicherersparnis (~12 MP → ~6,5 MP beim großen Foto) |
| F12 | Firebase-Testregeln vom 06.08. nach 30 Tagen abgelaufen (25.09.) → DB liefert `Permission denied`. `fetch()` lehnt ein Promise nur bei echten Netzwerkfehlern ab, nicht bei HTTP-Fehlerstatus (401/403) — das `.catch()` in `saveState`/`syncFromCloud` griff also gar nicht. Zusätzlich: `syncFromCloud` prüfte nur `Object.keys(cloudState).length`, und `{error:"Permission denied"}` hat genau 1 Key → wurde als gültiger Zustand übernommen | Sync zwischen Handys lief seit 25.09. komplett ohne Fehlermeldung ins Leere; bei jedem Poll (alle 8 s) wäre zusätzlich der komplette lokale Zimmerstand durch das Firebase-Fehlerobjekt überschrieben worden, sobald der GET-Request eine Antwort bekam | `res.ok` explizit prüfen (`checkFirebaseResponse`), Fehlerobjekt in `syncFromCloud` erkennen und verwerfen statt übernehmen, rotes Banner „Offline – …" bei jedem fehlgeschlagenen Sync. Zusätzlich: die vier Einzelzimmer-Aktionen schreiben jetzt per `PATCH` nur das eine Zimmer statt den ganzen Stand per `PUT` zu ersetzen (Last-Writer-wins entschärft). Verifiziert mit einem Mock-Fetch-Test (kein echter Firebase-Zugriff aus dieser Sandbox möglich, siehe unten) — **noch nicht mit echten Handys getestet**. Firebase-Regeln selbst + Anonymous Auth bleiben offen, dafür fehlt der Web-API-Key aus der Konsole (`4d5435b`) |
| F13 | Handys synchronisieren nicht (25.09., weiterhin offen) | Firebase-Regeln abgelaufen (401), App fängt Fehler still ab (siehe F12) | offen: Regeln + rotes Offline-Banner — **erst mit André abstimmen** (Konten-Umzug laut `KONTEN_UMZUG.md`), nicht in Eigenregie auf `true` zurücksetzen |
| F14 | Erste Zuschnitt-Version des Foto-Scan-Uploads (v3.12) hätte Kopfzeile und Zimmerspalte abgeschnitten | Schwelle trennte bei formatfüllenden Fotos nur Randschatten vom Papier, nicht den echten Blattrand | `scanPapierRahmen` schneidet nur noch bei echtem dunklem Hintergrund zu (Mittelwert dunkler Bereich < 80, Abstand hell/dunkel > 90) |
| F15 | v3.12-Patch wurde zunächst gegen den Stand vor v3.10/v3.11 vorbereitet | Anker hätten bei blindem Einspielen nicht mehr gepasst | Regel: vor jedem Patch `git pull`, alle Anker vor dem Einspielen per `grep -c` auf genau 1 Treffer prüfen |
| F16 | Ein Testfoto der Alpha-Liste enthielt zusätzlich die Safe-/Tür-PIN-Liste (zweites Blatt im Bild) | PINs wären im Klartext auf dem Handy/als Export gelandet | Hinweis direkt im Tool ergänzt („Nur die Gästeliste fotografieren — keine Schlüssel-/PIN-Listen im Bild"); betroffenes Foto löschen |

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
