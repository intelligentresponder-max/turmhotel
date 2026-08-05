f = "housekeeping/housekeeping-v3.html"
c = open(f, encoding="utf-8").read()

FIREBASE_URL = "https://turmhotel-hsk-default-rtdb.europe-west1.firebasedatabase.app"

# 1. saveState -> zusaetzlich an Firebase senden
old_savestate = "function saveState(s) { localStorage.setItem('hk_state3', JSON.stringify(s)); }"
new_savestate = ("function saveState(s) { localStorage.setItem('hk_state3', JSON.stringify(s)); "
                  "fetch('" + FIREBASE_URL + "/state.json', {method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(s)}).catch(function(e){console.warn('Sync state fehlgeschlagen', e);}); }")
assert c.count(old_savestate) == 1, "saveState-Anker nicht eindeutig"
c = c.replace(old_savestate, new_savestate, 1)

# 2. saveStaffData -> zusaetzlich an Firebase senden
old_savestaff = "function saveStaffData(s) { localStorage.setItem('hk_staff3', JSON.stringify(s)); }"
new_savestaff = ("function saveStaffData(s) { localStorage.setItem('hk_staff3', JSON.stringify(s)); "
                  "fetch('" + FIREBASE_URL + "/staff.json', {method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(s)}).catch(function(e){console.warn('Sync staff fehlgeschlagen', e);}); }")
assert c.count(old_savestaff) == 1, "saveStaffData-Anker nicht eindeutig"
c = c.replace(old_savestaff, new_savestaff, 1)

# 3. Test-Seed-Aufrufe entfernen + Cloud-Sync-Start einbauen
old_seed = "seedAllRoomsTestNote();\nforceFixNotes();\nassignTeamsAndInstructions();\nrenderRooms();\nrenderPersonal();\nupdateStats();"
new_seed = """renderRooms();
renderPersonal();
updateStats();

// == CLOUD-SYNC (Firebase) ==
const FIREBASE_URL = '""" + FIREBASE_URL + """';

async function syncFromCloud() {
  try {
    const stateRes = await fetch(FIREBASE_URL + '/state.json');
    const staffRes = await fetch(FIREBASE_URL + '/staff.json');
    const cloudState = await stateRes.json();
    const cloudStaff = await staffRes.json();
    if (cloudState && Object.keys(cloudState).length) {
      state = cloudState;
      localStorage.setItem('hk_state3', JSON.stringify(state));
    }
    if (cloudStaff && cloudStaff.length) {
      staff = cloudStaff;
      localStorage.setItem('hk_staff3', JSON.stringify(staff));
    }
    renderRooms(); renderPersonal(); renderOverview();
  } catch (e) {
    console.warn('Cloud-Sync fehlgeschlagen, nutze lokalen Stand', e);
  }
}
syncFromCloud();
setInterval(syncFromCloud, 8000);"""
assert c.count(old_seed) == 1, "Seed-Block-Anker nicht eindeutig"
c = c.replace(old_seed, new_seed, 1)

open(f, "w", encoding="utf-8").write(c)
print("OK: Cloud-Sync eingebaut, Test-Automatik entfernt")
