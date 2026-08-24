import io,sys
f='housekeeping/alpha-scan.html'
s=io.open(f,encoding='utf-8').read()
if 'tessedit_pageseg_mode' in s: sys.exit('schon gepatcht')
R=[
# 1) Tesseract zeilenweise lesen lassen statt Spalten zu erkennen
("      const result = await Tesseract.recognize(bild, 'deu', {",
 """      const result = await Tesseract.recognize(bild, 'deu', {
        tessedit_pageseg_mode: '6',   // ein zusammenhaengender Textblock:
                                      // erzwingt zeilenweises Lesen der Tabelle
"""),
# 2) Jahr muss plausibel sein - sonst aus dem Listenkopf ersetzen
("""    var j = (m[3].length === 4 && m[3].indexOf('20') === 0) ? m[3] : jahr;""",
 """    // 2028 und 2022 sind haeufige Fehllesungen von 2026. Nur das Jahr der Liste
    // und das Folgejahr sind moeglich - alles andere wird ersetzt.
    var j = (m[3] === jahr || m[3] === String(Number(jahr) + 1)) ? m[3] : jahr;"""),
# 3) Summenzeile darf Rest am Ende haben ("100 0 63 |")
("""  var m = text.match(/(?:^|\\n)\\s*(\\d{2,3})\\s+(\\d{1,2})\\s+(\\d{1,3})\\s*(?:\\n|$)/);""",
 """  var m = text.match(/(?:^|\\n)\\s*(\\d{2,3})\\s+(\\d{1,2})\\s+(\\d{1,3})\\s*[^\\d\\n]{0,4}(?:\\n|$)/);"""),
]
for a,b in R:
    if s.count(a)!=1: sys.exit('Anker nicht eindeutig: '+a[:45])
    s=s.replace(a,b,1)
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
