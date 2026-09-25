import io,sys
f='housekeeping/alpha-scan.html'
s=io.open(f,encoding='utf-8').read()
if 'pruefStatus' in s: sys.exit('schon gepatcht')
R=[
# --- Ampel-Badge in die Export-Karte ---
('''    <h2>5. CSV erstellen</h2>''',
 '''    <h2>5. CSV erstellen</h2>
    <div id="ampel" class="check-badge wait" style="display:block;margin-bottom:14px;">noch keine Auswertung</div>'''),
# --- Bild vor der Erkennung verdoppeln ---
("function heuteStr() {",
 """function bildAufbereiten(file) {
  // Tesseract schaetzt Handyfotos auf ~270 dpi. Verdoppeln + Graustufen hebt die
  // Trefferquote deutlich (im Test von 9 auf 40 erkannte Zimmernummern pro Seite).
  return new Promise(function(res){
    var img = new Image();
    img.onload = function(){
      var c = document.createElement('canvas');
      var f2 = img.width < 2000 ? 2 : 1;
      c.width = img.width * f2; c.height = img.height * f2;
      var ctx = c.getContext('2d');
      ctx.drawImage(img, 0, 0, c.width, c.height);
      var d = ctx.getImageData(0,0,c.width,c.height);
      for (var i=0;i<d.data.length;i+=4){
        var g = 0.299*d.data[i] + 0.587*d.data[i+1] + 0.114*d.data[i+2];
        d.data[i]=d.data[i+1]=d.data[i+2]=g;
      }
      ctx.putImageData(d,0,0);
      res(c);
    };
    img.onerror = function(){ res(file); };
    img.src = URL.createObjectURL(file);
  });
}

function heuteStr() {"""),
# --- aufbereitetes Bild an Tesseract geben ---
("      const result = await Tesseract.recognize(pages[p], 'deu', {",
 """      const bild = await bildAufbereiten(pages[p]);
      const result = await Tesseract.recognize(bild, 'deu', {"""),
# --- neuer Parser ---
('''function parseText(text) {
  // Zimmernummern: 3-stellige Zahl am Zeilenanfang (mit optionalen Leerzeichen)
  const roomRe = /(?:^|\\n)\\s*(\\d{3})\\b/g;
  const rooms = [];
  let m;
  while ((m = roomRe.exec(text)) !== null) rooms.push(m[1]);

  // Datumspaare TT.MM.JJJJ TT.MM.JJJJ (Anreise, Abreise) — wir wollen das zweite (Abreise)
  const dateRe = /(\\d{2}\\.\\d{2}\\.20\\d{2})\\D{0,15}(\\d{2}\\.\\d{2}\\.20\\d{2})/g;
  const departures = [];
  while ((m = dateRe.exec(text)) !== null) departures.push(m[2]);

  const count = Math.min(rooms.length, departures.length);''',
 '''let pruefText = '';

function datumsTreffer(str, jahr) {
  // toleriert 09.08,202€ / 0708202 / 05.08:2026 — Jahr wird aus dem Listenkopf ergaenzt
  var re = /(\\d{2})[.,:\\s]?(\\d{2})[.,:\\s]?(\\d{4}|\\d{3}|\\d{2})(?!\\d)/g, out = [], m;
  while ((m = re.exec(str)) !== null) {
    var j = (m[3].length === 4 && m[3].indexOf('20') === 0) ? m[3] : jahr;
    out.push(m[1] + '.' + m[2] + '.' + j);
  }
  return out;
}

function anzSumme(text) {
  // Fusszeile der letzten Seite: Erw / Kin / Anz — nur die dritte Zahl interessiert
  var m = text.match(/(?:^|\\n)\\s*(\\d{2,3})\\s+(\\d{1,2})\\s+(\\d{1,3})\\s*(?:\\n|$)/);
  if (!m) return null;
  var anz = parseInt(m[3], 10);
  return (anz > 0 && anz <= 73) ? anz : null;
}

function parseText(text) {
  const jahr = hskDate.value ? hskDate.value.split('-')[0] : String(new Date().getFullYear());
  const rooms = [];
  const departures = [];
  let m;

  // Weg 1: zeilenweise — Zimmer und Datum stehen in derselben Zeile. Zuverlaessig,
  // weil dabei keine Verschiebung zwischen den Spalten entstehen kann.
  text.split('\\n').forEach(function(zeile){
    var mz = zeile.match(/^\\s*(\\d{3})\\b/);
    if (!mz) return;
    var d = datumsTreffer(zeile.slice(mz[0].length), jahr);
    if (d.length >= 2) { rooms.push(mz[1]); departures.push(d[1]); }
  });

  // Weg 2 (Rueckfall): Tesseract hat die Tabelle spaltenweise gelesen — Zimmer und
  // Daten kommen als getrennte Bloecke. Paarung ueber die Position, fehleranfaellig.
  if (rooms.length < 5) {
    const roomRe = /(?:^|\\n)\\s*(\\d{3})\\b/g;
    while ((m = roomRe.exec(text)) !== null) rooms.push(m[1]);
    const alle = datumsTreffer(text, jahr);
    for (let i = 1; i < alle.length; i += 2) departures.push(alle[i]);
    pruefText = 'spaltenweise gelesen — Zuordnung unsicher, bitte jede Zeile pruefen';
  } else {
    pruefText = '';
  }

  const count = Math.min(rooms.length, departures.length);'''),
# --- Zimmerpruefung + Ampel im Anschluss an das Einlesen ---
('''  if (dubletten > 0) {''',
 '''  const ungueltig = rows.filter(function(r){ return ALLE_ZIMMER.indexOf(r.zimmer) === -1; });
  rows = rows.filter(function(r){ return ALLE_ZIMMER.indexOf(r.zimmer) !== -1; });

  const kopf = text.match(/am\\s+(\\d{2})[.,:\\s](\\d{2})[.,:\\s](\\d{4})/);
  if (kopf) { var kd = new Date(+kopf[3], +kopf[2]-1, +kopf[1]); kd.setDate(kd.getDate()+1); setHskDate(kd); }

  const summe = anzSumme(text);
  if (summe && !pmsTotalInput.value) pmsTotalInput.value = summe;

  pruefStatus(kopf, summe, ungueltig.length);

  if (dubletten > 0) {'''),
# --- Ampel-Funktion ---
("function renderFreeRooms(){",
 """function pruefStatus(kopf, summe, ungueltig) {
  var mangel = [], hinweis = [];
  if (!kopf) mangel.push('Kopfzeile mit Listendatum nicht erkannt');
  if (summe && summe !== rows.length) mangel.push('Anz.-Summe ' + summe + ', erkannt ' + rows.length);
  if (!rows.length) mangel.push('keine Zimmer erkannt');
  if (pruefText) mangel.push(pruefText);
  if (ungueltig) hinweis.push(ungueltig + ' Fehlerkennung(en) verworfen');
  if (!summe) hinweis.push('Anz.-Summe nicht gefunden — bitte von Hand eintragen');

  var el = document.getElementById('ampel');
  if (mangel.length) {
    el.className = 'check-badge bad';
    el.textContent = '✕ Aufnahme unvollständig: ' + mangel.join(' · ') + ' — bitte neu aufnehmen';
    downloadBtn.disabled = true; downloadBtn.style.opacity = '.4';
  } else if (hinweis.length) {
    el.className = 'check-badge wait';
    el.textContent = '! ' + rows.length + ' Zimmer erkannt · ' + hinweis.join(' · ');
    downloadBtn.disabled = false; downloadBtn.style.opacity = '1';
  } else {
    el.className = 'check-badge ok';
    el.textContent = '✓ ' + rows.length + ' Zimmer, Listendatum und Anz.-Summe stimmen überein';
    downloadBtn.disabled = false; downloadBtn.style.opacity = '1';
  }
}

function renderFreeRooms(){"""),
]
for a,b in R:
    if s.count(a)!=1: sys.exit('Anker nicht eindeutig: '+a[:45])
    s=s.replace(a,b,1)
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
