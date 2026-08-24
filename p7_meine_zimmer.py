import io,sys
f='housekeeping/housekeeping-v3.html'
s=io.open(f,encoding='utf-8').read()
if 'tab-meine' in s: sys.exit('schon gepatcht')
R=[
# --- CSS ---
(".room-card.clean::before{background:var(--clean);}",
 """.room-card.clean::before{background:var(--clean);}
.mine-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:18px;}
.mine-who{font-family:'Spline Sans Mono',monospace;font-size:.9rem;}
.mine-count{font-family:'Spline Sans Mono',monospace;font-size:1.15rem;}
.mine-group{margin-top:26px;}
.mine-group h3{font-size:1rem;margin:0 0 4px;}
.mine-sub{font-family:'Spline Sans Mono',monospace;font-size:.72rem;color:var(--muted);margin-bottom:10px;}
.mine-room{display:flex;align-items:center;justify-content:space-between;width:100%;
  padding:20px 18px;margin-bottom:10px;border-radius:8px;border:1px solid var(--line);
  background:rgba(255,255,255,.03);cursor:pointer;text-align:left;}
.mine-room .nr{font-family:'Spline Sans Mono',monospace;font-size:1.9rem;font-weight:600;}
.mine-room .st{font-family:'Spline Sans Mono',monospace;font-size:.8rem;color:var(--muted);}
.mine-room.done{background:rgba(42,122,75,.16);border-color:rgba(42,122,75,.55);}
.mine-room.done .nr{color:var(--clean);text-decoration:line-through;}
.mine-pick{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px;}
.mine-pick button{padding:16px 22px;border-radius:8px;border:1px solid var(--line);
  background:rgba(255,255,255,.04);font-family:'Spline Sans Mono',monospace;font-size:1rem;cursor:pointer;}"""),
# --- Tab-Button ---
('''  <button class="tab" id="tab-btn-uebersicht" onclick="showTab('uebersicht')">Übersicht</button>''',
 '''  <button class="tab" id="tab-btn-meine" onclick="showTab('meine')">Meine Zimmer</button>
  <button class="tab" id="tab-btn-uebersicht" onclick="showTab('uebersicht')">Übersicht</button>'''),
# --- Tab-Inhalt ---
('''<div id="tab-uebersicht" style="display:none">''',
 '''<div id="tab-meine" style="display:none">
  <div id="mine-body"></div>
</div>

<div id="tab-uebersicht" style="display:none">'''),
# --- showTab erweitern ---
("""function showTab(tab) {
  ['zimmer','uebersicht','gaeste','personal'].forEach(id => {""",
 """function showTab(tab) {
  ['zimmer','meine','uebersicht','gaeste','personal'].forEach(id => {"""),
("  if (tab === 'uebersicht') renderOverview();",
 "  if (tab === 'meine') renderMine();\n  if (tab === 'uebersicht') renderOverview();"),
# --- Logik ---
("function renderOverview() {",
 """// ══ MEINE ZIMMER ══
function meinName()      { return localStorage.getItem('hk_me') || ''; }
function setMeinName(n)  { localStorage.setItem('hk_me', n); renderMine(); }

function toggleFertig(id) {
  const rs = getRoomState(id);
  state[id] = { ...rs, clean: !rs.clean };
  saveState(state);
  renderMine(); renderRooms(); renderOverview();
}

function renderMine() {
  const box = document.getElementById('mine-body');
  const ich = meinName();

  if (!ich || !staff.some(s => s.name === ich)) {
    box.innerHTML = '<div class="building-label">Wer bist du?</div>' +
      '<p style="color:var(--muted);font-family:\\'Spline Sans Mono\\',monospace;font-size:.82rem">' +
      'Einmal antippen — das Handy merkt sich den Namen.</p><div class="mine-pick" id="mine-pick"></div>';
    const p = document.getElementById('mine-pick');
    if (!staff.length) { p.innerHTML = '<span style="color:var(--muted)">Noch kein Personal angelegt.</span>'; return; }
    staff.forEach(function(s){
      const b = document.createElement('button');
      b.textContent = s.name; b.style.borderColor = s.color;
      b.addEventListener('click', function(){ setMeinName(s.name); });
      p.appendChild(b);
    });
    return;
  }

  const meine     = ALL_ROOMS.filter(r => getRoomState(r).staff === ich);
  const abreise   = meine.filter(r => getRoomState(r).guestType === 'checkout');
  const bleiber   = meine.filter(r => getRoomState(r).guestType !== 'checkout');
  const fertig    = meine.filter(r => getRoomState(r).clean).length;

  function block(titel, unter, liste) {
    if (!liste.length) return '';
    return '<div class="mine-group"><h3>' + titel + '</h3><div class="mine-sub">' + unter + '</div>' +
      liste.map(function(r){
        const rs = getRoomState(r);
        return '<button class="mine-room' + (rs.clean ? ' done' : '') + '" onclick="toggleFertig(\\'' + r + '\\')">' +
               '<span class="nr">' + r + '</span>' +
               '<span class="st">' + (rs.clean ? '✓ fertig' : 'antippen wenn fertig') + '</span></button>';
      }).join('') + '</div>';
  }

  box.innerHTML =
    '<div class="mine-head"><span class="mine-who">' + ich +
    ' · <a href="#" onclick="localStorage.removeItem(\\'hk_me\\');renderMine();return false;" style="color:var(--muted)">wechseln</a></span>' +
    '<span class="mine-count">' + fertig + ' von ' + meine.length + ' fertig</span></div>' +
    (meine.length ? '' : '<p style="color:var(--muted);font-family:\\'Spline Sans Mono\\',monospace;font-size:.85rem">Heute sind dir noch keine Zimmer zugeteilt.</p>') +
    block('Abreisen', 'Vollreinigung — hier kommt heute ein neuer Gast', abreise) +
    block('Bleiber', 'Gast bleibt — nur auffrischen', bleiber);
}

function renderOverview() {"""),
]
for a,b in R:
    if s.count(a)!=1: sys.exit('Anker nicht eindeutig: '+a[:45])
    s=s.replace(a,b,1)
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
