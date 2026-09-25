f = "housekeeping/housekeeping-v3.html"
c = open(f, encoding="utf-8").read()

# 1. Button in der Nav neben Facility
old_nav = "\U0001F527 Facility</a>"
new_nav = "\U0001F527 Facility</a>\n    <button class=\"lang-btn\" onclick=\"printHandoverReport()\">\U0001F5A8\uFE0F \u00dcbergabebericht</button>"
assert c.count(old_nav) == 1, "Nav-Anker nicht eindeutig: " + str(c.count(old_nav))
c = c.replace(old_nav, new_nav, 1)

# 2. Funktion vor dem Cloud-Sync-Block einfuegen
anchor = "// == CLOUD-SYNC (Firebase) =="
report_fn = """function printHandoverReport() {
  var skip = ['Tagungsraum Mailand', 'Tagungsraum Barcelona', '101'];
  var rooms = ALL_ROOMS.filter(function(id){ return skip.indexOf(id) === -1; });
  var rows = rooms.map(function(id){
    var rs = getRoomState(id);
    return {
      id: id,
      type: ROOM_TYPES[id] || '',
      clean: !!rs.clean,
      occupied: !!rs.occupied,
      guestType: rs.guestType || '',
      staffName: rs.staff || '',
      note: (rs.note || '').trim()
    };
  });
  var totalRooms = rows.length;
  var cleanedCount = rows.filter(function(r){ return r.clean; }).length;
  var openCount = totalRooms - cleanedCount;
  var checkoutCount = rows.filter(function(r){ return r.guestType === 'checkout'; }).length;
  var overnightCount = rows.filter(function(r){ return r.guestType === 'overnight'; }).length;

  var byStaff = {};
  rows.forEach(function(r){
    var name = r.staffName || 'Nicht zugewiesen';
    if (!byStaff[name]) byStaff[name] = [];
    byStaff[name].push(r);
  });

  var realNotes = rows.filter(function(r){
    return r.note && r.note.indexOf('So meldest du fertig') !== 0;
  });

  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  var staffHtml = '';
  Object.keys(byStaff).sort().forEach(function(name){
    var list = byStaff[name];
    var done = list.filter(function(r){ return r.clean; }).length;
    var roomIds = list.map(function(r){
      return r.id + (r.clean ? ' (fertig)' : '') + (r.guestType === 'checkout' ? ' [Abreise]' : (r.guestType === 'overnight' ? ' [Overnight]' : ''));
    }).join(', ');
    staffHtml += '<tr><td>' + esc(name) + '</td><td>' + done + ' / ' + list.length + '</td><td>' + esc(roomIds) + '</td></tr>';
  });

  var notesHtml = '';
  if (realNotes.length) {
    realNotes.forEach(function(r){
      notesHtml += '<tr><td>' + esc(r.id) + '</td><td>' + esc(r.staffName || '-') + '</td><td>' + esc(r.note) + '</td></tr>';
    });
  } else {
    notesHtml = '<tr><td colspan="3">Keine offenen Maengel gemeldet.</td></tr>';
  }

  var openRooms = rows.filter(function(r){ return !r.clean; }).map(function(r){ return r.id; }).join(', ') || 'Keine';

  var now = new Date();
  var dateStr = now.toLocaleDateString('de-DE') + ' ' + now.toLocaleTimeString('de-DE', {hour:'2-digit', minute:'2-digit'});

  var html = '<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">' +
    '<title>Uebergabebericht - Turmhotel</title>' +
    '<style>' +
    'body{font-family:Arial,sans-serif;color:#111;padding:24px;font-size:13px;}' +
    'h1{font-size:20px;margin-bottom:4px;}' +
    'h2{font-size:15px;margin-top:28px;border-bottom:1px solid #999;padding-bottom:4px;}' +
    '.meta{color:#555;margin-bottom:18px;}' +
    'table{width:100%;border-collapse:collapse;margin-top:8px;}' +
    'th,td{border:1px solid #ccc;padding:6px 8px;text-align:left;vertical-align:top;}' +
    'th{background:#eee;}' +
    '.summary span{display:inline-block;margin-right:22px;}' +
    '@media print{ body{padding:0;} }' +
    '</style></head><body>' +
    '<h1>Turmhotel Frankfurt - Uebergabebericht</h1>' +
    '<div class="meta">Erstellt: ' + dateStr + '</div>' +
    '<div class="summary">' +
      '<span><strong>' + totalRooms + '</strong> Zimmer gesamt</span>' +
      '<span><strong>' + cleanedCount + '</strong> gereinigt</span>' +
      '<span><strong>' + openCount + '</strong> ausstehend</span>' +
      '<span><strong>' + checkoutCount + '</strong> Abreise</span>' +
      '<span><strong>' + overnightCount + '</strong> Overnight</span>' +
    '</div>' +
    '<h2>Zuteilung nach Personal</h2>' +
    '<table><thead><tr><th>Name</th><th>Fertig / Zugewiesen</th><th>Zimmer</th></tr></thead><tbody>' + staffHtml + '</tbody></table>' +
    '<h2>Offene Maengel / Notizen</h2>' +
    '<table><thead><tr><th>Zimmer</th><th>Gemeldet von</th><th>Notiz</th></tr></thead><tbody>' + notesHtml + '</tbody></table>' +
    '<h2>Noch nicht fertiggestellte Zimmer</h2>' +
    '<div>' + esc(openRooms) + '</div>' +
    '</body></html>';

  var win = window.open('', '_blank');
  if (!win) { alert('Popup wurde blockiert. Bitte Popups fuer diese Seite erlauben.'); return; }
  win.document.open();
  win.document.write(html);
  win.document.close();
  setTimeout(function(){ win.focus(); win.print(); }, 350);
}

""" + anchor
assert c.count(anchor) == 1, "Cloud-Sync-Anker nicht eindeutig: " + str(c.count(anchor))
c = c.replace(anchor, report_fn, 1)

open(f, "w", encoding="utf-8").write(c)
print("OK: Uebergabebericht eingebaut")
