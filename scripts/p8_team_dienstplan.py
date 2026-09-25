import io,sys
f='housekeeping/housekeeping-v3.html'
s=io.open(f,encoding='utf-8').read()
if 'TEAM_DIENSTPLAN' in s: sys.exit('schon gepatcht')
R=[
# --- CSS fuer das Haekchen ---
(".mine-head{",
 """.pres-btn{border:1px solid var(--line);background:rgba(255,255,255,.04);color:var(--muted);
  border-radius:5px;padding:5px 11px;font-family:'Spline Sans Mono',monospace;font-size:.72rem;cursor:pointer;margin-right:8px;}
.pres-btn.da{background:rgba(42,122,75,.2);border-color:rgba(42,122,75,.6);color:#7fd6a2;}
.mine-head{"""),
# --- Team laden Button in der Personal-Karte ---
('''      <h3>Mitarbeiter hinzufügen</h3>''',
 '''      <button class="lang-btn" onclick="teamLaden()" style="margin-bottom:14px">Team aus Dienstplan laden</button>
      <h3>Mitarbeiter hinzufügen</h3>'''),
# --- Team + Funktionen ---
("function renderPersonal() {",
 """// Housekeeping laut Dienstplan (Stand 03.-09.08.2026), Reihenfolge wie auf dem Plan.
// Technik (El Houssaini) gehoert nicht in die Zimmerverteilung.
const TEAM_DIENSTPLAN = [
  { name: 'Kanczler',  abb: 'KAN', color: '#c9a227', rolle: 'Hausdame' },
  { name: 'Loi',       abb: 'LOI', color: '#d4a574', rolle: 'Hausdame' },
  { name: 'Boateng',   abb: 'BOA', color: '#2a7a4b', rolle: 'Reinigung' },
  { name: 'Ouattara',  abb: 'OUA', color: '#1a6fa8', rolle: 'Reinigung' },
  { name: 'Olah, Eva', abb: 'EVA', color: '#8e44ad', rolle: 'Reinigung' },
  { name: 'Tuhluk',    abb: 'TUH', color: '#e67e22', rolle: 'Reinigung' },
  { name: 'Mehari',    abb: 'MEH', color: '#c0392b', rolle: 'Reinigung' },
  { name: 'Kulwinder', abb: 'KUL', color: '#16a085', rolle: 'Reinigung' },
  { name: 'Haidari',   abb: 'HAI', color: '#5b8dee', rolle: 'Reinigung' },
  { name: 'da Silva',  abb: 'DAS', color: '#a0522d', rolle: 'Reinigung' },
  { name: 'Mia',       abb: 'MIA', color: '#7f8c8d', rolle: 'Aushilfe' },
];

function teamLaden() {
  if (!confirm('Das komplette Housekeeping aus dem Dienstplan übernehmen? Die bisherige Personalliste wird ersetzt, die Zimmerzuteilung bleibt.')) return;
  staff = TEAM_DIENSTPLAN.map(function(p){ return { name:p.name, abb:p.abb, color:p.color, rolle:p.rolle, da:false }; });
  saveStaffData(staff);
  renderPersonal(); renderOverview(); renderMine();
  alert('11 Personen übernommen. Jetzt antippen, wer heute da ist.');
}

function toggleDa(i) {
  staff[i].da = !staff[i].da;
  saveStaffData(staff);
  renderPersonal();
}

function renderPersonal() {"""),
# --- Haekchen in der Liste ---
('''    item.innerHTML = `<span class="staff-chip" style="background:${s.color}">${s.abb}</span><span class="pname">${s.name}</span><span class="pabb">${s.abb}</span><button class="del-btn" onclick="deleteStaff(${i})">×</button>`;''',
 '''    item.innerHTML = `<span class="staff-chip" style="background:${s.color}">${s.abb}</span><span class="pname">${s.name}</span>` +
      `<span class="pabb">${s.rolle || ''}</span>` +
      `<button class="pres-btn ${s.da ? 'da' : ''}" onclick="toggleDa(${i})">${s.da ? '✓ heute da' : 'heute nicht da'}</button>` +
      `<button class="del-btn" onclick="deleteStaff(${i})">×</button>`;'''),
# --- Verteilung nur auf Anwesende, ohne Hausdamen ---
("""function autoAssignStaff() {
  if (!staff.length) { alert('Erst Personal anlegen.'); return; }""",
 """function autoAssignStaff() {
  if (!staff.length) { alert('Erst Personal anlegen.'); return; }
  // Nur wer heute da ist und reinigt. Ist niemand markiert, gilt die alte Regel: alle.
  const markiert = staff.filter(function(s){ return s.da; });
  const team = markiert.length
    ? markiert.filter(function(s){ return s.rolle !== 'Hausdame' || markiert.every(function(x){ return x.rolle === 'Hausdame'; }); })
    : staff;
  if (!team.length) { alert('Niemand als anwesend markiert.'); return; }"""),
("""  function distribute(rooms) {
    rooms.forEach((id, i) => {
      const person = staff[i % staff.length].name;""",
 """  function distribute(rooms) {
    rooms.forEach((id, i) => {
      const person = team[i % team.length].name;"""),
("""  alert('Verteilt: ' + checkoutRooms.length + ' Abreise + ' + overnightRooms.length + ' Overnight auf ' + staff.length + ' Personen.');""",
 """  alert('Verteilt: ' + checkoutRooms.length + ' Abreise + ' + overnightRooms.length + ' Overnight auf ' + team.length + ' Personen (' + team.map(function(s){return s.name;}).join(', ') + ').');"""),
]
for a,b in R:
    if s.count(a)!=1: sys.exit('Anker nicht eindeutig: '+a[:45])
    s=s.replace(a,b,1)
io.open(f,'w',encoding='utf-8').write(s)
print('OK')
