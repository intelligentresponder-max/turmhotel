import io,sys
f='housekeeping/alpha-scan.html'
s=io.open(f,encoding='utf-8').read()
if 'ausrichtungPruefen' in s: sys.exit('schon gepatcht')
R=[
("function bildAufbereiten(file) {",
 """let drehung = 0;   // wird einmal je Scan ermittelt und auf alle Seiten angewandt

function alsBild(file) {
  return new Promise(function(res, rej){
    var img = new Image();
    img.onload = function(){ res(img); };
    img.onerror = rej;
    img.src = URL.createObjectURL(file);
  });
}

function aufCanvas(img, grad, faktor) {
  var w = Math.round(img.width * faktor), h = Math.round(img.height * faktor);
  var c = document.createElement('canvas');
  if (grad % 180 === 0) { c.width = w; c.height = h; } else { c.width = h; c.height = w; }
  var ctx = c.getContext('2d');
  ctx.translate(c.width/2, c.height/2);
  ctx.rotate(grad * Math.PI / 180);
  ctx.drawImage(img, -w/2, -h/2, w, h);
  var d = ctx.getImageData(0, 0, c.width, c.height);
  for (var i = 0; i < d.data.length; i += 4) {
    var g = 0.299*d.data[i] + 0.587*d.data[i+1] + 0.114*d.data[i+2];
    d.data[i] = d.data[i+1] = d.data[i+2] = g;
  }
  ctx.putImageData(d, 0, 0);
  return c;
}

// Probelauf an einer verkleinerten Kopie der ersten Seite: welche Drehung liefert
// die meisten Zeilen, die mit einer Zimmernummer beginnen? Quer fotografierte
// Blaetter brachten im Test 23 statt 63 Zeilen.
async function ausrichtungPruefen(file, melde) {
  var img = await alsBild(file);
  var klein = Math.min(1, 1100 / Math.max(img.width, img.height));
  var beste = 0, bestN = -1;
  var winkel = [0, 90, -90];
  for (var i = 0; i < winkel.length; i++) {
    melde('Ausrichtung wird geprueft ... ' + (i+1) + '/' + winkel.length);
    try {
      var r = await Tesseract.recognize(aufCanvas(img, winkel[i], klein), 'deu');
      var n = (r.data.text.match(/(?:^|\\n)\\s*\\d{3}\\b/g) || []).length;
      if (n > bestN) { bestN = n; beste = winkel[i]; }
      if (n >= 15) break;
    } catch (e) { }
  }
  drehung = beste;
  return beste;
}

function bildAufbereiten(file) {"""),
("""    var img = new Image();
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
    };""",
 """    var img = new Image();
    img.onload = function(){
      res(aufCanvas(img, drehung, img.width < 2000 ? 2 : 1));
    };"""),
("""  try {
    let alles = '';
    for (let p = 0; p < pages.length; p++) {""",
 """  try {
    const grad = await ausrichtungPruefen(pages[0], function(t){ progressLabel.textContent = t; });
    if (grad !== 0) progressLabel.textContent = 'Aufnahme wird gedreht';
    let alles = '';
    for (let p = 0; p < pages.length; p++) {"""),
("  if (!summe) hinweis.push('Anz.-Summe nicht gefunden — bitte von Hand eintragen');",
 """  if (!summe) hinweis.push('Anz.-Summe nicht gefunden — bitte von Hand eintragen');
  if (drehung !== 0) hinweis.push('Aufnahme war quer, automatisch gedreht');"""),
]
for a,b in R:
    if s.count(a)!=1: sys.exit('Anker nicht eindeutig: '+a[:45])
    s=s.replace(a,b,1)
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
