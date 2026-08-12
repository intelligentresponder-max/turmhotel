# Konten-Umzug: von André's privaten Konten auf hoteleigene Konten

Ziel: GitHub-Repo, Firebase-Projekt und bit.ly-Links laufen künftig unter
Konten, auf die das Hotel selbst Zugriff hat — nicht mehr nur privat bei
André Schwarz. Die eigentliche Übertragung braucht Zugangsdaten, die nur ihr
bzw. André habt; dieses Dokument ist die Schritt-für-Schritt-Anleitung dafür.
Ich kann bei jedem Schritt helfen, wenn ihr mir sagt, wo ihr steht.

Reihenfolge einhalten — GitHub zuerst, dann Firebase, zuletzt bit.ly, weil
die späteren Schritte von den URLs der früheren abhängen.

---

## 0. Vorbereitung

- [ ] Ein **Hotel-E-Mail-Postfach** festlegen, das die neuen Konten trägt
      (nicht die private Adresse einer einzelnen Person) — z. B. eine
      Rezeptions- oder IT-Adresse des Hotels.
- [ ] Damit einen **neuen GitHub-Account** anlegen (falls nicht vorhanden).
- [ ] Damit ein **Google-Konto** anlegen bzw. ein bestehendes Hotel-Google-Konto
      nutzen (für Firebase).

## 1. GitHub-Repo übertragen

André (aktueller Owner) macht das:

1. Im Repo → **Settings** → ganz unten **„Danger Zone"** → **„Transfer
   ownership"**.
2. Neuen Kontonamen (Hotel-Account) eingeben, bestätigen.
3. Das Hotel-Konto bekommt eine Einladung per Mail/GitHub-Benachrichtigung —
   annehmen.

**Achtung:** Nach dem Transfer ändert sich die GitHub-Pages-URL, falls der
alte Owner-Name Teil der URL war
(`https://[alter-owner].github.io/turmhotel/...` →
`https://[neuer-owner].github.io/turmhotel/...`). Das bedeutet: **alle
bit.ly-Links müssen danach ihr Ziel neu bekommen** (siehe Schritt 3). Bis
dahin funktionieren die alten bit.ly-Links nicht mehr — am besten Umzug
außerhalb der Hauptbetriebszeit machen und vorher kurz das Team informieren.

Danach: Wer künftig Änderungen einstellen soll, unter **Settings → Collaborators**
eintragen (siehe auch `ANLEITUNG_UPDATES.md`).

## 2. Firebase-Projekt umziehen

Firebase-Projekte lassen sich nicht einfach übertragen — es braucht ein
**neues Projekt** unter dem Hotel-Google-Konto plus Datenübernahme.

1. [console.firebase.google.com](https://console.firebase.google.com) mit dem
   Hotel-Google-Konto öffnen → **„Projekt hinzufügen"**.
2. **Realtime Database** anlegen, Region **europe-west1** wählen (wie bisher,
   sonst leidet die Geschwindigkeit).
3. Die neue Datenbank-URL notieren, sieht aus wie
   `https://[neuer-projektname]-default-rtdb.europe-west1.firebasedatabase.app`.
4. **Daten übernehmen** — die alten Daten sind nicht geheim, einfach im
   Browser abrufen und wieder einspielen:
   - Alt: `https://turmhotel-hsk-default-rtdb.europe-west1.firebasedatabase.app/state.json`
     und `.../staff.json` aufrufen, Inhalt kopieren.
   - In der neuen Firebase-Konsole unter **Realtime Database → Daten** die
     beiden Knoten `state` und `staff` anlegen und den kopierten Inhalt
     einfügen (Konsole hat einen „JSON importieren"-Button pro Knoten).
5. **Regeln setzen.** Aktuell ist die Datenbank ohne Anmeldung les- und
   beschreibbar (jeder mit der URL kann Daten überschreiben) — das beim Umzug
   am besten nicht 1:1 übernehmen, sondern in der neuen Konsole unter
   **Realtime Database → Regeln** mindestens folgendes setzen, damit nicht
   irgendwer im Internet die Zimmerbelegung überschreiben kann:
   ```json
   { "rules": { ".read": true, ".write": true } }
   ```
   ist der aktuelle (offene) Stand. Eine echte Absicherung (z. B. Regeln, die
   einen Anmeldevorgang verlangen) bedeutet Code-Änderungen an der App
   (Firebase-Auth einbauen) — das ist ein eigenes, größeres Thema. Wenn
   gewünscht, machen wir das als nächsten Schritt separat.
6. **Code anpassen** — dank der Aufräumarbeit gibt es nur noch **eine**
   Stelle: in `housekeeping/housekeeping-v3.html` die Zeile
   ```js
   const FIREBASE_URL = 'https://turmhotel-hsk-default-rtdb.europe-west1.firebasedatabase.app';
   ```
   auf die neue URL ändern (das geht über `ANLEITUNG_UPDATES.md`, ist aber
   Code im `<script>`-Bereich — hier lieber einen Entwickler oder Claude
   direkt bitten, den einen Zeilen-Tausch zu machen und die Syntaxprüfung
   laufen zu lassen).
7. Testen: Auf zwei Geräten öffnen, auf einem einen Zimmerstatus ändern, prüfen
   ob es auf dem anderen ankommt.

## 3. bit.ly-Links umziehen

1. Mit dem Hotel-Konto bei [bit.ly](https://bitly.com) anmelden (neuer
   Account, falls die alten Links auf André's privatem Account liegen).
2. Zwei neue Kurzlinks anlegen, die auf die **neue** GitHub-Pages-URL zeigen:
   - `housekeeping/housekeeping-v3.html` (bisher `bit.ly/turm7`)
   - `housekeeping/alpha-scan.html` (bisher `bit.ly/turmhsk`)
3. Falls möglich dieselben Kurznamen (`turm7`, `turmhsk`) wählen, damit sich
   für das Team nichts merken muss — sonst neue Links an alle verteilen
   (Homescreen-Icons auf den Handys müssen dann neu angelegt werden).

## 4. Nacharbeiten

- [ ] `README.md` und `UEBERGABE_HSK777.md`: Zeile „Entwicklung und Betrieb:
      André Schwarz" durch die neue Zuständigkeit ersetzen, falls gewünscht.
- [ ] Alle Geräte im Housekeeping-Team einmal die App neu laden lassen
      (Homescreen-Verknüpfung zeigt sonst weiter auf den alten Link).
- [ ] Altes Firebase-Projekt und alte bit.ly-Links erst löschen/deaktivieren,
      wenn der neue Weg 1–2 Tage im echten Betrieb bestätigt ist.

---

**Wenn ihr an einem der Schritte hängt** (z. B. Firebase-Konsole, Regeln,
oder der Code-Zeile in Schritt 2.6): einfach melden, wo genau ihr steht —
ich kann von dort aus weiterhelfen.
