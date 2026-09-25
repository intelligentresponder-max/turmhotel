f = "housekeeping/housekeeping-v3.html"
c = open(f, encoding="utf-8").read()

# 1. BUGFIX: applyCsvImport() setzt jetzt ALLE Zimmer zurueck, bevor die neue Liste angewendet wird
old_fn = """function applyCsvImport() {
  if (!csvParsed.length) return;
  csvParsed.forEach(({ room, guestType }) => {"""
new_fn = """function applyCsvImport() {
  if (!csvParsed.length) return;
  ALL_ROOMS.forEach(id => {
    const old = getRoomState(id);
    state[id] = { ...old, guestType: '' };
  });
  csvParsed.forEach(({ room, guestType }) => {"""
assert c.count(old_fn) == 1, "applyCsvImport-Anker nicht eindeutig"
c = c.replace(old_fn, new_fn, 1)

# 2. RESET-BUTTON vor "Zimmer manuell markieren"
old_h3 = "<h3>Zimmer manuell markieren</h3>"
new_h3 = """<div style="margin:20px 0;padding:16px;border:1px solid rgba(230,126,34,.35);border-radius:4px;background:rgba(230,126,34,.06)">
  <div style="font-size:.78rem;color:var(--muted);margin-bottom:10px">Setzt Belegung, Reinigung und Zuweisung fuer ALLE Zimmer zurueck. Personal bleibt erhalten.</div>
  <button class="btn" style="background:var(--checkout-col);color:#fff" onclick="resetRoomStatus()">Zimmerstatus zuruecksetzen</button>
</div>
<h3>Zimmer manuell markieren</h3>"""
assert c.count(old_h3) == 1, "H3-Anker nicht eindeutig"
c = c.replace(old_h3, new_h3, 1)

# 3. Funktion resetRoomStatus() vor applyCsvImport einfuegen
anchor_fn2 = "function applyCsvImport() {"
new_reset_fn = """function resetRoomStatus() {
  if (!confirm('Alle Zimmerstatus zuruecksetzen (Belegung, Reinigung, Zuweisung)? Personal bleibt erhalten.')) return;
  state = {};
  saveState(state);
  csvParsed = [];
  const banner = document.getElementById('import-banner');
  if (banner) banner.classList.remove('show');
  renderRooms(); renderPersonal(); renderOverview();
  alert('Zimmerstatus wurde zurueckgesetzt.');
}

""" + anchor_fn2
assert c.count(anchor_fn2) == 1, "Anker2 nicht eindeutig"
c = c.replace(anchor_fn2, new_reset_fn, 1)

open(f, "w", encoding="utf-8").write(c)
print("OK: Bugfix + Reset-Button eingefuegt")
