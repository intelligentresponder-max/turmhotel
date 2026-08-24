import io,sys
f='housekeeping/alpha-scan.html'
s=io.open(f,encoding='utf-8').read()
if 'listenMonat' in s: sys.exit('schon gepatcht')
R=[
# Listendatum merken, damit das Jahr daraus abgeleitet werden kann
("""function datumAusKopf(text) {
  var m = text.match(/am\\s+(\\d{2})\\.(\\d{2})\\.(\\d{4})/);
  if (!m) return;""",
 """let listenMonat = 0, listenJahr = 0;   // aus dem Kopf der Liste

function datumAusKopf(text) {
  var m = text.match(/am\\s+(\\d{2})\\.(\\d{2})\\.(\\d{4})/);
  if (!m) return;
  listenMonat = +m[2]; listenJahr = +m[3];"""),
# Jahr nicht mehr aus dem Bild uebernehmen
("""function datumsTreffer(str, jahr) {
  // toleriert 09.08,202€ / 0708202 / 05.08:2026 — Jahr wird aus dem Listenkopf ergaenzt
  var re = /(\\d{2})[.,:\\s]?(\\d{2})[.,:\\s]?(\\d{4}|\\d{3}|\\d{2})(?!\\d)/g, out = [], m;
  while ((m = re.exec(str)) !== null) {
    // 2028 und 2022 sind haeufige Fehllesungen von 2026. Nur das Jahr der Liste
    // und das Folgejahr sind moeglich - alles andere wird ersetzt.
    var j = (m[3] === jahr || m[3] === String(Number(jahr) + 1)) ? m[3] : jahr;
    out.push(m[1] + '.' + m[2] + '.' + j);
  }
  return out;
}""",
 """function datumsTreffer(str, jahr) {
  // Das Jahr wird bewusst NICHT aus dem Bild uebernommen. Die Erkennung liest es
  // regelmaessig falsch (2028, 2022, 202€). Gelesen werden nur Tag und Monat;
  // das Jahr kommt aus dem Kopf der Liste. Eine Abreise kann nicht vor dem
  // Listendatum liegen — ein kleinerer Monat bedeutet also das Folgejahr.
  var basisM = listenMonat || 0;
  var basisJ = listenJahr || Number(jahr);
  var re = /(\\d{2})[.,:\\s]?(\\d{2})[.,:\\s]?(?:\\d{4}|\\d{3}|\\d{2})(?!\\d)/g, out = [], m;
  while ((m = re.exec(str)) !== null) {
    var mon = +m[2];
    if (mon < 1 || mon > 12) continue;          // offensichtlich falsch gelesen
    var j = (basisM && mon < basisM) ? basisJ + 1 : basisJ;
    out.push(m[1] + '.' + m[2] + '.' + j);
  }
  return out;
}"""),
]
for a,b in R:
    if s.count(a)!=1: sys.exit('Anker nicht eindeutig: '+a[:45])
    s=s.replace(a,b,1)
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
