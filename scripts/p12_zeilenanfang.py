import io,sys
f='housekeeping/alpha-scan.html'
s=io.open(f,encoding='utf-8').read()
if 'zimmerAmZeilenanfang' in s: sys.exit('schon gepatcht')

alt = """  text.split('\\n').forEach(function(zeile){
    var mz = zeile.match(/^\\s*(\\d{3})\\b/);
    if (!mz) return;
    var d = datumsTreffer(zeile.slice(mz[0].length), jahr);
    if (d.length >= 2) { rooms.push(mz[1]); departures.push(d[1]); }
  });"""

neu = """  const belegt = {};
  text.split('\\n').forEach(function(zeile){
    var mz = zimmerAmZeilenanfang(zeile, belegt);
    if (!mz) return;
    var d = datumsTreffer(zeile.slice(mz.laenge), jahr);
    if (d.length >= 2) { rooms.push(mz.zimmer); departures.push(d[1]); belegt[mz.zimmer] = 1; }
  });"""

hilfe = """// Der Zeilenanfang ist die haeufigste Fehlerquelle: die Erkennung liefert dort
// S05 statt 505, §09 statt 509 oder haengt eine Ziffer davor (4102 statt 102).
// Ohne Zimmernummer faellt die ganze Zeile weg — daher hier reparieren.
function zimmerAmZeilenanfang(zeile, belegt) {
  var m = zeile.match(/^[\\s\\-–—.·:]*([0-9SsOoIlB§|]{3,4})\\b/);
  if (!m) return null;
  var roh = m[1]
    .replace(/[Ss§]/g, '5').replace(/[Oo]/g, '0')
    .replace(/[Il|]/g, '1').replace(/B/g, '8');
  if (!/^\\d{3,4}$/.test(roh)) return null;

  var kandidaten = roh.length === 3 ? [roh] : [roh.slice(1), roh.slice(0, 3)];
  var gueltig = kandidaten
    .map(function(k){ return String(parseInt(k, 10)); })
    .filter(function(k){ return ALLE_ZIMMER.indexOf(k) !== -1; });

  // Jedes Zimmer steht genau einmal auf der Liste. Ist ein Kandidat schon
  // vergeben, ist der andere gemeint. Bleibt es mehrdeutig, wird nicht geraten.
  var frei = gueltig.filter(function(k){ return !belegt[k]; });
  if (frei.length !== 1) return null;
  return { zimmer: frei[0], laenge: m[0].length };
}

"""

R=[
(alt, neu),
("function parseText(text) {", hilfe + "function parseText(text) {"),
]
for a,b in R:
    if s.count(a)!=1: sys.exit('Anker nicht eindeutig: '+a[:45])
    s=s.replace(a,b,1)
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
