# ÜBERGABE — Optimierung HSK v3 + Facility

**Stand:** 30.10.2026 · **Repo:** `intelligentresponder-max/turmhotel` · **Branch:** `main`
**Geprüft gegen Commit:** `588b526` (09.10.2026) — vor Beginn `git pull` und Anker neu prüfen (F15, F21).
**Ablage im Repo:** Datei nach `UEBERGABE_OPTIMIERUNG.md` (Repo-Root) kopieren, `UEBERGABE_HSK777.md` am Ende der Session aktualisieren (F1).

**Ziel:** Ablauf bleibt wie bisher (Alpha-Liste fotografieren → Doppelcheck → übertragen → verteilen → „Meine Zimmer“). Neu: Freigabe durch die Hausdame, Facility in der Cloud, optionale Fotobestätigung überall.

---

## 0. Vor dem Start

```bash
cd ~/turmhotel && git status && git pull --rebase
git log -1 --format='%h %ci %s'
grep -c "function toggleFertig" housekeeping/housekeeping-v3.html      # erwartet: 1
grep -c "function createTechTicket" housekeeping/housekeeping-v3.html  # erwartet: 1
grep -c "Daten lokal im Browser" housekeeping/housekeeping-v3.html     # erwartet: 2
grep -c "facility_tasks" facility.html                                  # erwartet: 2
```

Weicht ein Wert ab: **stoppen**, Stand lesen, Anker anpassen. Nicht blind patchen.

---

## 1. Aufgaben (Reihenfolge = Priorität)

### A1 · Checklisten-Umgehung schließen — klein
- **Wo:** `housekeeping/housekeeping-v3.html`, `function toggleFertig(id)` (ca. Z. 1287)
- **Ist:** setzt `clean: !rs.clean` direkt, ohne Checkliste.
- **Soll:** Button in „Meine Zimmer“ ruft `openChecklist(id)` auf. Zurücksetzen auf „offen“ nur für Rolle Hausdame/Rezeption.
- [x] Umgesetzt (`11b74d3`) · [x] Test: Zimmer in „Meine Zimmer“ ohne Haken nicht fertig meldbar (Browser-Test mit simulierter Cloud, 30.10.)

### A2 · Ticket übernimmt Kategorie und Priorität — klein
- **Wo:** `function createTechTicket(roomId)` (ca. Z. 2874), `const TECH_CATS` (ca. Z. 2836)
- **Ist:** schreibt immer `cat: 'Elektro'`, `prio: 'mittel'`.
- **Soll:** `cat` aus `selectedTechCat` (ohne Emoji), `prio` aus Zuordnung: Sanitär, Steckdose, Schloss/Safe = `hoch`; TV, Möbel = `niedrig`; Rest = `mittel`.
- **Soll:** Ein gemeinsamer Kategorienkatalog für HSK und `facility.html` (heute 10 gegen 7 Kategorien).
- [x] Umgesetzt (`814536e`, neue Datei `kategorien.js`) · [x] Test: Ticket „Sanitär“ erscheint als Sanitär/hoch

### A3 · Kopfzeile korrigieren — klein
- **Wo:** Z. 483 (`#lbl-meta`) und Z. 2738 (`meta:` im Sprachobjekt `de`)
- **Ist:** „Daten lokal im Browser gespeichert“ — falsch seit Cloud-Sync.
- **Soll:** z. B. „Daten werden geschützt in der Cloud synchronisiert“. Beide Stellen ändern.
- [x] Umgesetzt (`f3f4394`, auch en/hu; Text: „Daten werden über die Cloud mit allen Geräten abgeglichen“ — bewusst ohne „geschützt“) · [ ] Beschriftung Vorder-/Hinterhaus mit dem Haus abgeglichen (André vor Ort)

### B1 · Freigabe durch die Hausdame — mittel
- **Ist:** nur `clean: true/false`.
- **Soll:** Zustände `offen → gereinigt → freigegeben`. Feld z. B. `approved: {by, at}` am Zimmerstatus.
  - Button „Freigeben“ nur für Rolle `Hausdame`, nicht dieselbe Person wie `staff` des Zimmers.
  - „Zurück an Reinigung“ setzt `clean:false`, Pflicht-Grund, gleiche Person bleibt zugeteilt.
  - Rezeption sieht „freigegeben“ getrennt; Zähler oben ergänzen.
  - Jede Statusänderung speichert Person + Uhrzeit (Verlauf).
- [x] Umgesetzt (`52a9b77`) · [x] Test: Zimmermädchen kann nicht selbst freigeben (simuliert; echter Test am Handy steht aus)

### B2 · Facility an die Cloud — mittel
- **Wo:** `facility.html`, `function load()` / `function save(d)` (Z. 286–287), `moveTask`, `deleteTask`
- **Ist:** nur `localStorage['facility_tasks']`.
- **Soll:** gleiche Firebase-DB und `fbEnsureAuth()` wie HSK v3 (Code übernehmen, nicht neu erfinden), Pfad z. B. `/facility/tasks`.
  - HSK v3 `createTechTicket()` schreibt ebenfalls dorthin.
  - `deleteTask` ersetzen durch Status „abgelehnt“ mit Grund.
  - Beim Laden **nie** den Cloud-Stand überschreiben (F23).
- [x] Umgesetzt (`73b3081`) · [x] Test: Ticket vom Handy A erscheint auf Gerät B (simuliert mit 3 Browsern inkl. Offline/Nachsenden; echter Test steht aus)

### C1 · Optionale Fotobestätigung überall — groß
- **Stellen:** Fertigmeldung (Checkliste), Freigabe/Rückgabe Hausdame, Ticket anlegen, Ticket erledigt (vorher/nachher).
- **Speicher:** Firebase Cloud Storage, in der DB nur Pfad/URL. **Vorher klären:** Storage braucht für neue Buckets vermutlich den Blaze-Tarif → André entscheidet, Budgetwarnung setzen.
- **Aufnahme:** `<input type="file" accept="image/*" capture="environment">`
- **Größe:** im Browser verkleinern, lange Kante ≈ 1280 px, JPEG ≈ 0,7, Ziel < 200 KB. Nie hochskalieren (F11).
- **Regeln:** nur mit Anmeldung, nur `image/*`, max. 1 MB.
- **Offline:** Foto puffern und nachsenden; Fertigmeldung darf nicht am Upload scheitern.
- **Datenschutz:** Hinweis am Button „Keine Personen, keine Gastsachen, keine Listen/PINs“ (F16). Automatische Löschung nach 30 Tagen.
- **Fehler:** HTTP-Status prüfen, Fehler sichtbar anzeigen (F12).
- [ ] Storage freigeschaltet · [ ] Umgesetzt · [ ] Test am Handy mit schlechtem Netz

**Umsetzungsplan C1 (30.10.2026, wartet auf Freigabe Storage durch André):**
1. *André, Firebase-Konsole:* Storage aktivieren (Tarif prüfen), Budgetwarnung z. B. 5 €/Monat, Bucket-Namen notieren (vermutlich `turmhotel-hsk.firebasestorage.app` — **ungeprüft**). Regeln: Lesen/Schreiben nur `request.auth != null`, nur `image/.*`, `< 1 MB`, nur unter `fotos/`. Löschregel 30 Tage (Lebenszyklus in der Google-Cloud-Konsole).
2. *Code:* neue gemeinsame Datei `foto.js` (wie `kategorien.js`) für HSK und Facility: Aufnahme (`capture="environment"`), Verkleinern (lange Kante ≤ 1280 px, nie hochskalieren, JPEG 0,7, notfalls Qualität senken bis < 200 KB), Upload per Storage-REST mit dem Token aus `fbEnsureAuth()`, `res.ok` prüfen, Fehler sichtbar (F12). In der DB nur der Pfad.
3. *Offline:* Foto in IndexedDB puffern, im 8-s-Sync nachsenden. Fertigmeldung/Ticket speichern sofort, Foto-Feld zunächst `{wartet:true}` — nie am Upload scheitern.
4. *Vier Stellen:* Checkliste (`confirmChecklist`), Freigabe/Rückgabe (`freigeben`/`zurueckAnReinigung`), Ticket anlegen (`createTechTicket`, Facility `addTask`), Ticket erledigt (`moveTask(…,'done')` = nachher-Foto).
5. *Hinweis am Knopf:* „Keine Personen, keine Gastsachen, keine Listen/PINs“ (F16).
6. *Test:* Browser-Test mit simuliertem Storage, danach echtes Handy mit schwachem Netz/Flugmodus.

---

## 2. Pflicht vor jedem Push

```bash
f=housekeeping/housekeeping-v3.html
sed -n '/<script>/,/<\/script>/p' $f | grep -v '<script>\|</script>' > ~/hk.js && node --check ~/hk.js && echo SAUBER
grep -n -i "passw\|wlan" *.html housekeeping/*.html     # muss leer sein (F6)
grep -n '\\`' $f                                          # muss leer sein (F2)
git status                                                # nur gewollte Dateien (F9)
```
Gleiches für `facility.html`.

---

## 3. Abnahme durch André

- [ ] Alpha-Liste scannen → übertragen → verteilen funktioniert wie vorher
- [ ] Fertigmeldung nur über Checkliste
- [ ] Hausdame gibt frei bzw. gibt mit Grund zurück
- [ ] Technik sieht Ticket auf eigenem Gerät, mit richtiger Kategorie
- [ ] Foto optional an allen vier Stellen, auch bei schwachem Netz
- [ ] `UEBERGABE_HSK777.md` aktualisiert (Datum, Commit, erledigt/offen)

---

## 4. Neuer Eintrag für das Fehlerprotokoll (in UEBERGABE_HSK777.md übernehmen)

| # | Fehler | Folge | Gegenmaßnahme |
|---|---|---|---|
| F24 | 30.10.2026: Übergabe- und Audit-Dokument teils aus altem Gedächtnisstand geschrieben („keine Anmeldung“, „Alpha-Scan als eigene Datei“, „CSV-Weg“) | Programmierer hätte erledigte Arbeit erneut geplant | Vor jedem Planungsdokument Repo pullen und Code lesen; Commit im Kopf angeben |
