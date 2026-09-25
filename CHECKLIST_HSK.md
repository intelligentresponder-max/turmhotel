# CHECKLIST_HSK — Optimierung Housekeeping Manager v3

Stand: 25.09.2026 · Datei: `housekeeping/housekeeping-v3.html`
Reihenfolge = Priorität. Erledigtes mit Commit-Hash abhaken.

---

## 1. Sync & Sicherheit (zuerst)

- [ ] **Firebase-Regeln erneuern.** Stand 25.09.: DB antwortet `Permission denied` (Testregeln vom 06.08. vermutlich nach 30 Tagen abgelaufen).
      Nicht wieder `".read": true` / `".write": true`, sondern Anonymous Auth + `auth != null`.
- [ ] **Sync-Fehler sichtbar machen.** Aktuell nur `console.warn` → rotes Banner „Offline – nicht synchron".
- [ ] **`PUT /state.json` → `PATCH` pro Zimmer.** Heute gewinnt der letzte Schreiber; Fertig-Meldungen anderer Handys können überschrieben werden.
- [ ] **Polling (8 s) → Firebase-Listener (`onValue`).** Sofort aktuell, weniger Akku.
- [ ] Nach Fix: Test mit 2 Handys gleichzeitig „Fertig" tippen → beide Meldungen bleiben erhalten.

## 2. Upload per Handy

- [ ] Prüfen: Foto-Scan-Reiter (v3.9) übernimmt komplett ohne Datei-Weg.
- [ ] **Reset vor Import automatisch** (nicht manuell). Grund: Doppel-Import-Bug 05.08.
- [ ] Zimmerzahl vs. PMS-Summe prüfen → bei Rot „Verteilen" sperren.
- [ ] Spalten `Erw.` / `Kin.` mitführen (Bettenzahl, Kinderbett).
- [ ] OOO-Rückläufer als eigener Status (brauchen Reinigung).
- [ ] Ausnahmeliste Zimmer-Sharing (Doppelzeile ≠ Fehler).

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
| 25.09. | Kein Sync zwischen Handys | Firebase-Regeln abgelaufen | offen | — |

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
