# CHECKLIST_HSK — Optimierung Housekeeping Manager v3

Stand: 25.09.2026 · Datei: `housekeeping/housekeeping-v3.html`
Reihenfolge = Priorität. Erledigtes mit Commit-Hash abhaken.

---

## 1. Sync & Sicherheit (zuerst)

- [ ] **Firebase-Regeln erneuern.** Stand 25.09.: DB antwortet `Permission denied` (Testregeln vom 06.08. vermutlich nach 30 Tagen abgelaufen).
      Nicht wieder `".read": true` / `".write": true`, sondern Anonymous Auth + `auth != null`.
      **Blockiert auf:** Firebase Web-API-Key aus der Konsole (Project Settings → General → „Web API Key") — ohne den kann das Anonymous-Sign-in nicht clientseitig eingebaut werden. Regeltext zum Einfügen liegt in `KONTEN_UMZUG.md` bereit, sobald der Key da ist.
- [x] **Sync-Fehler sichtbar machen.** `4d5435b` (25.09.): rotes Banner „Offline – …" bei jedem fehlgeschlagenen Sync (Netzwerk- **und** HTTP-Fehler, z.B. 401/403 bei abgelaufenen Regeln — `fetch()` lehnt bei HTTP-Fehlerstatus das Promise nicht ab, das musste extra geprüft werden).
- [x] **`PUT /state.json` → `PATCH` pro Zimmer.** `4d5435b` (25.09.): für die vier Einzelzimmer-Aktionen (`saveRoom`, `toggleFertig`, `applyManual`, `confirmChecklist`) umgestellt. Massenaktionen (Import, Reset, Verteilen) bleiben bewusst bei PUT, da dort ein vollständiges Ersetzen gewollt ist.
- [ ] **Polling (8 s) → Firebase-Listener (`onValue`).** Sofort aktuell, weniger Akku. Zurückgestellt: erfordert entweder das Firebase JS-SDK oder REST-Streaming (SSE) — beides ließ sich aus dieser Sandbox nicht gegen die echte DB testen (Netzwerk-Policy blockiert den Host), daher nicht blind in die Live-Datei gebaut.
- [ ] Nach Fix: Test mit 2 Handys gleichzeitig „Fertig" tippen → beide Meldungen bleiben erhalten. **Noch nicht mit echten Geräten getestet** (nur mit einem Mock-Fetch-Harness verifiziert, siehe Fehlerprotokoll F12 in `UEBERGABE_HSK777.md`).

## 2. Upload per Handy

- [ ] Prüfen: Foto-Scan-Reiter (v3.9) übernimmt komplett ohne Datei-Weg.
- [ ] **Reset vor Import automatisch** (nicht manuell). Grund: Doppel-Import-Bug 05.08.
- [ ] Zimmerzahl vs. PMS-Summe prüfen → bei Rot „Verteilen" sperren.
- [ ] Spalten `Erw.` / `Kin.` mitführen (Bettenzahl, Kinderbett).
- [ ] OOO-Rückläufer als eigener Status (brauchen Reinigung).
- [ ] Ausnahmeliste Zimmer-Sharing (Doppelzeile ≠ Fehler).
- [x] **Datei-Upload ohne Kamerazwang (v3.12).** `capture="environment"` entfernt —
      `<input>` erlaubt jetzt Galerie/Dateiauswahl + mehrere Dateien statt nur die
      Kamera. Zusätzlich: PDF-Weg (Suite8 → „Microsoft Print to PDF") wird ohne
      OCR exakt gelesen; Fotos (JPG/PNG/WEBP/HEIC) werden je Seite ausgerichtet,
      zugeschnitten und aufgehellt; neuer Export „Als PDF speichern". Getestet mit
      echtem Chromium-Browser (Playwright) gegen die anonymisierte Alpha-Liste vom
      25.09.: 70/47/23, Anz. 70, Erw. 96, Kin. 3 — stimmt. Siehe README v3.12.
      **Noch offen:** echte Handyfotos/HEIC im Browser (kein Testgerät verfügbar).

## 3. Paritätische Verteilung (`autoAssignStaff`)

- [ ] **Bug:** Abreise- und Overnight-Runde starten beide bei `team[0]` → bei Rest bekommt Person 1 doppelt mehr. Fix: Overnight-Runde beim Index weiterführen, wo Abreise endete.
- [ ] **Aufwand statt Anzahl:** Abreise ≈ 1,0 · Overnight ≈ 0,5 · + Bettenzahl.
- [ ] **Arbeitszeit anteilig:** TZ 6 h vs. VZ 8 h.
- [ ] **Laufwege:** nach Haus/Etage bündeln (Vorderhaus 11–55 / Hinterhaus 102–510) statt reihum 11, 14, 17 …
- [ ] Fertige Zimmer beim Neu-Verteilen nicht umhängen.
- [ ] Vorschau „Last pro Person" vor dem Bestätigen.
- [ ] Hausdame nur einplanen, wenn ausdrücklich gewählt (heute: nur wenn alle Hausdamen sind).

## 4. Bedienung (Feedback Team / Dario)

- [ ] „Meine Zimmer": größere Schrift, hoher Kontrast.
- [ ] „Rückgängig" bei versehentlichem Fertig.
- [ ] Chips nach Vorder-/Hinterhaus gruppieren.

## 5. Fehler-Log (Pflicht)

Jeder Fehler: **Datum · Symptom · Ursache · Fix · Commit**

| Datum | Symptom | Ursache | Fix | Commit |
|---|---|---|---|---|
| 05.08. | Vortag + neue Liste addiert | Import ersetzte nicht | Reset-Button | — |
| 08.08. | Abreise/Overnight vertauscht | Scan vor Mitternacht, Systemdatum | Feld Housekeeping-Tag | `a1977ca` |
| 08.08. | `024` ≠ `24` | führende Nullen | Import gehärtet | `945fdb7` |
| 25.09. | Kein Sync zwischen Handys | Firebase-Regeln abgelaufen | Regeln/Auth offen (Web-API-Key fehlt) | — |
| 25.09. | `syncFromCloud` hätte bei `Permission denied` die Fehlerantwort als gültigen Zustand übernommen und den kompletten lokalen Stand überschrieben | `fetch()` lehnt Promise nur bei Netzwerkfehlern ab, nicht bei HTTP 401/403; `Object.keys({error:'...'}).length` ist truthy | `res.ok` prüfen, Fehlerobjekt erkennen und verwerfen, Banner statt stillem Datenverlust | `4d5435b` |
| 25.09. | Erste Zuschnitt-Version des Foto-Scan-Uploads (v3.12) hätte Kopfzeile und Zimmerspalte abgeschnitten | Schwelle trennte bei formatfüllenden Fotos nur Randschatten vom Papier, nicht den echten Blattrand | Nur zuschneiden bei echtem dunklem Hintergrund (Mittelwert < 80, Abstand hell/dunkel > 90) | — |
| 25.09. | v3.12-Patch zunächst gegen älteren Stand vorbereitet | Repo war parallel auf v3.10/v3.11 gelaufen | Regel: vor jedem Patch `git pull`, Anker vorher per `grep -c` auf genau 1 Treffer prüfen | — |
| 25.09. | Testfoto der Alpha-Liste enthielt zusätzlich die Safe-/Tür-PIN-Liste | Zweites Blatt im Bild | Hinweis im Tool ergänzt; Foto löschen, nur die Gästeliste fotografieren | — |

Einträge zusätzlich in `UEBERGABE_HSK777.md` spiegeln.

## 6. Vor jedem Push

```bash
sed -n '/<script>/,/<\/script>/p' housekeeping/housekeeping-v3.html | grep -v '<script>\|</script>' > ~/hk.js && node --check ~/hk.js
```

## 7. Alternativen (doppelt geprüft)

| Option | Nutzen | Sicherheit | Urteil |
|---|---|---|---|
| Firebase + Auth + Regeln | bleibt, minimaler Umbau | gut mit Regeln | **jetzt** |
| Supabase | SQL, Row-Level-Security | gut | erst beim Konten-Umzug prüfen |
| Nur localStorage | kein Backend | lokal sicher | raus – kein Geräteabgleich |
