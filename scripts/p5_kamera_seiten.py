import io,sys
f='housekeeping/alpha-scan.html'
s=io.open(f,encoding='utf-8').read()
if 'hsk-date' in s: sys.exit('schon gepatcht')
R=[
# --- CSS fuer Miniaturen ---
("  .progress-wrap{",
 """  .thumbs{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;}
  .thumb{position:relative;width:78px;height:104px;border-radius:4px;overflow:hidden;border:1px solid var(--line);}
  .thumb img{width:100%;height:100%;object-fit:cover;}
  .thumb .no{position:absolute;left:0;top:0;background:rgba(0,0,0,.65);color:#fff;font-size:.62rem;padding:1px 5px;}
  .thumb .x{position:absolute;right:0;top:0;background:rgba(0,0,0,.65);color:#fff;border:0;font-size:.7rem;padding:1px 5px;cursor:pointer;}
  .progress-wrap{"""),
# --- Upload-Karte: mehrere Aufnahmen ---
('''    <h2>1. Foto hochladen</h2>
    <div class="dropzone" id="dropzone">
      <input type="file" id="file-input" accept="image/*" capture="environment">
      <div class="dz-title">📷 Foto der Alpha-Liste hier ablegen</div>
      <div class="dz-sub">oder klicken zum Auswählen / Kamera öffnen</div>
    </div>
    <img id="preview-img">''',
 '''    <h2>1. Seiten aufnehmen</h2>
    <div class="dropzone" id="dropzone">
      <input type="file" id="file-input" accept="image/*" capture="environment">
      <div class="dz-title">📷 Seite der Alpha-Liste aufnehmen</div>
      <div class="dz-sub">bis zu 3 Seiten &middot; Kamera oder Datei &middot; ausgewertet werden nur Zimmernummer und Abreisedatum</div>
    </div>
    <img id="preview-img">
    <div class="thumbs" id="thumbs"></div>
    <div id="page-actions" style="display:none;margin-top:14px;">
      <button class="btn" id="ocr-btn">Seiten auswerten</button>
      <button class="btn secondary" id="more-btn" style="margin-left:8px;">Weitere Seite</button>
    </div>'''),
# --- Datumsfeld in die Doppelcheck-Karte ---
('''    <h2>3. Doppelcheck</h2>''',
 '''    <h2>3. Doppelcheck</h2>
    <div class="check-row" style="margin-bottom:8px;">
      <label for="hsk-date">Housekeeping-Tag:</label>
      <input type="date" id="hsk-date">
      <span class="check-badge wait" id="date-badge">Tag der Reinigung</span>
    </div>
    <div class="hint" style="margin-bottom:18px;">Wird aus dem Kopf der Liste gesetzt (Listendatum + 1 Tag). Nach 18 Uhr sonst automatisch auf morgen. Nur &auml;ndern, wenn du eine &auml;ltere Liste nachtr&auml;gst.</div>'''),
# --- Elemente + Datumsvorbelegung ---
("const resetBtn = document.getElementById('reset-btn');",
 '''const resetBtn = document.getElementById('reset-btn');
const thumbs = document.getElementById('thumbs');
const pageActions = document.getElementById('page-actions');
const ocrBtn = document.getElementById('ocr-btn');
const moreBtn = document.getElementById('more-btn');
const hskDate = document.getElementById('hsk-date');
const dateBadge = document.getElementById('date-badge');
let pages = [];

function setHskDate(d){
  hskDate.value = d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  dateBadge.textContent = 'Tag der Reinigung: '+heuteStr();
}
(function(){var d=new Date(); if(d.getHours()>=18) d.setDate(d.getDate()+1); setHskDate(d);})();'''),
# --- Upload-Logik: sammeln statt sofort auswerten ---
('''fileInput.addEventListener('change', e => { if (e.target.files[0]) handleFile(e.target.files[0]); });

function handleFile(file) {
  const url = URL.createObjectURL(file);
  previewImg.src = url;
  previewImg.style.display = 'block';
  runOCR(file);
}''',
 '''fileInput.addEventListener('change', e => {
  for (var i=0;i<e.target.files.length;i++) handleFile(e.target.files[i]);
  fileInput.value = '';
});
moreBtn.addEventListener('click', () => fileInput.click());
ocrBtn.addEventListener('click', () => runOCR());

function handleFile(file) {
  if (pages.length >= 3) { alert('Mehr als 3 Seiten sind nicht vorgesehen.'); return; }
  pages.push(file);
  renderThumbs();
}

function renderThumbs() {
  thumbs.innerHTML = '';
  pages.forEach(function(file, i){
    var d = document.createElement('div'); d.className = 'thumb';
    var img = document.createElement('img'); img.src = URL.createObjectURL(file);
    var no = document.createElement('span'); no.className = 'no'; no.textContent = 'S.'+(i+1);
    var x = document.createElement('button'); x.className = 'x'; x.textContent = '×';
    x.addEventListener('click', function(){ pages.splice(i,1); renderThumbs(); });
    d.appendChild(img); d.appendChild(no); d.appendChild(x); thumbs.appendChild(d);
  });
  pageActions.style.display = pages.length ? 'block' : 'none';
  ocrBtn.textContent = pages.length === 1 ? 'Seite auswerten' : pages.length + ' Seiten auswerten';
  moreBtn.style.display = pages.length >= 3 ? 'none' : 'inline-block';
}'''),
# --- OCR ueber alle Seiten ---
('''async function runOCR(file) {''',
 '''async function runOCR() {
  if (!pages.length) return;'''),
('''  try {
    const result = await Tesseract.recognize(file, 'deu', {
      logger: m => {
        if (m.status === 'recognizing text') {
          const pct = Math.round(m.progress * 100);
          progressFill.style.width = pct + '%';
          progressLabel.textContent = 'Wird gelesen … ' + pct + '%';
        } else {
          progressLabel.textContent = m.status;
        }
      }
    });
    progressWrap.style.display = 'none';
    parseText(result.data.text);''',
 '''  try {
    let alles = '';
    for (let p = 0; p < pages.length; p++) {
      const result = await Tesseract.recognize(pages[p], 'deu', {
        logger: m => {
          if (m.status === 'recognizing text') {
            const pct = Math.round(m.progress * 100);
            progressFill.style.width = pct + '%';
            progressLabel.textContent = 'Seite ' + (p+1) + ' von ' + pages.length + ' … ' + pct + '%';
          } else {
            progressLabel.textContent = 'Seite ' + (p+1) + ': ' + m.status;
          }
        }
      });
      alles += result.data.text + '\\n';
    }
    progressWrap.style.display = 'none';
    datumAusKopf(alles);
    parseText(alles);'''),
# --- Datum aus dem Listenkopf ---
("function normalizeRoom(raw) {",
 """function datumAusKopf(text) {
  var m = text.match(/am\\s+(\\d{2})\\.(\\d{2})\\.(\\d{4})/);
  if (!m) return;
  var d = new Date(+m[3], +m[2]-1, +m[1]);
  d.setDate(d.getDate() + 1);          // Liste vom Vorabend gilt fuer den Folgetag
  setHskDate(d);
}

function heuteStr() {
  if (hskDate && hskDate.value) {
    var p = hskDate.value.split('-');
    return p[2] + '.' + p[1] + '.' + p[0];
  }
  var n = new Date();
  return String(n.getDate()).padStart(2,'0') + '.' + String(n.getMonth()+1).padStart(2,'0') + '.' + n.getFullYear();
}

function normalizeRoom(raw) {"""),
# --- alte heuteStr entfernen ---
('''function heuteStr() {
  const d = new Date();
  return String(d.getDate()).padStart(2,'0') + '.' + String(d.getMonth()+1).padStart(2,'0') + '.' + d.getFullYear();
}

''', ''),
# --- Datumsaenderung wirkt sofort ---
("pmsArrivalsInput.addEventListener('input', updateCheck);",
 '''pmsArrivalsInput.addEventListener('input', updateCheck);
hskDate.addEventListener('change', function(){
  dateBadge.textContent = 'Tag der Reinigung: ' + heuteStr();
  renderRows(); updateCheck();
});'''),
# --- Reset ---
('''  rows = [];
  previewImg.style.display = 'none';''',
 '''  rows = [];
  pages = [];
  renderThumbs();
  previewImg.style.display = 'none';'''),
]
for a,b in R:
    if s.count(a)!=1: sys.exit('Anker nicht eindeutig: '+a[:45])
    s=s.replace(a,b,1)
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
