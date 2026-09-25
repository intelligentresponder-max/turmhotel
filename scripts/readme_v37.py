import io,sys
f='README.md'
s=io.open(f,encoding='utf-8').read()
if 'v3.7' in s: sys.exit('schon eingetragen')

neu = """### v3.7 — 09.08.2026 · Ausrichtung, Lesemodus, Team
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

"""
s = s.replace('### v3.6', neu + '### v3.6', 1)

start = s.index('## Als N')
ende  = s.index('---', start)
liste = """## Als Nächstes

1. Dateiweg abschaffen: Ergebnis direkt übergeben statt CSV herunterladen und
   wieder auswählen; auf Dauer beide Werkzeuge in einer Oberfläche
2. Bettenzahl (Spalte `Erw.`) und Kinder (Spalte `Kin.`) mitführen — das
   Housekeeping muss wissen, wie viele Betten zu beziehen sind
3. OOO-Rückläufer sichtbar machen
4. Ausnahmeliste für doppelte Zimmerzeilen, damit Zimmer-Sharing bei Messen
   nicht als Fehler gemeldet wird
5. Aus der älteren Planung offen: Arbeitszeit-Tracking, Mängel-Report,
   Technik-Report für den Hausmeister

"""
s = s[:start] + liste + s[ende:]
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
