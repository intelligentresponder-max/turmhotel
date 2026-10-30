// Gemeinsamer Kategorienkatalog für Technik-Tickets (A2, 30.10.2026).
// Wird von housekeeping/housekeeping-v3.html (Checkliste) und facility.html
// (Board, Neue Aufgabe) geladen — Kategorien nur hier ändern.
//   name  = gespeicherter Wert im Ticket (ohne Emoji)
//   prio  = Standard-Priorität, wenn das Ticket aus dem Housekeeping kommt
//   css   = Farbklasse im Facility-Board (cat-…)
//   hsk   = in der Housekeeping-Checkliste als Knopf anbieten
var TECH_KATALOG = [
  { name: 'Beleuchtung',        icon: '💡', prio: 'mittel',  css: 'elektro',    hsk: true },
  { name: 'TV / Fernbedienung', icon: '📺', prio: 'niedrig', css: 'elektro',    hsk: true },
  { name: 'Sanitär',            icon: '🚿', prio: 'hoch',    css: 'sanitaer',   hsk: true },
  { name: 'Steckdose',          icon: '🔌', prio: 'hoch',    css: 'elektro',    hsk: true },
  { name: 'Fenster / Tür',      icon: '🪟', prio: 'mittel',  css: 'moebel',     hsk: true },
  { name: 'Möbel',              icon: '🛏', prio: 'niedrig', css: 'moebel',     hsk: true },
  { name: 'Klima / Heizung',    icon: '❄️', prio: 'mittel',  css: 'sanitaer',   hsk: true },
  { name: 'Schloss / Safe',     icon: '🔑', prio: 'hoch',    css: 'sicherheit', hsk: true },
  { name: 'WLAN',               icon: '📶', prio: 'mittel',  css: 'elektro',    hsk: true },
  // bisherige Facility-Kategorien, bleiben für alte und manuelle Tickets
  { name: 'Elektro',            icon: '⚡', prio: 'mittel',  css: 'elektro',    hsk: false },
  { name: 'Reinigung',          icon: '🧹', prio: 'mittel',  css: 'reinigung',  hsk: false },
  { name: 'Sicherheit',         icon: '🔒', prio: 'hoch',    css: 'sicherheit', hsk: false },
  { name: 'Sonstiges',          icon: '📋', prio: 'mittel',  css: 'sonstiges',  hsk: true },
];

function techKategorie(name) {
  for (var i = 0; i < TECH_KATALOG.length; i++) if (TECH_KATALOG[i].name === name) return TECH_KATALOG[i];
  return null;
}
