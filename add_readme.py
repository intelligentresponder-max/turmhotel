import os
f = "README.md"
roadmap = """
## Naechste Updates (Housekeeping Manager v3)

1. Uebergabebericht - druckbare Tagesuebersicht: Zimmerstatus, zustaendige Person, offene Maengel. Fuer den Schichtwechsel.
2. Arbeitszeit-Tracking - Start/Ende pro Zimmer oder Schicht, pro Mitarbeiter auswertbar.
3. Maengel-Report - strukturierte, druckbare Auswertung der Notiz-/Technik-Eintraege aus der Fertigmeldung.
4. Technik-Report fuer den Hausmeister - druckbare Fassung der Facility-Manager-Tickets, sortiert nach Prioritaet.
"""
if not os.path.exists(f):
    open(f, "w", encoding="utf-8").write("# Turmhotel - Digitalisierungsprojekt\n" + roadmap)
    print("README.md neu erstellt")
else:
    c = open(f, encoding="utf-8").read()
    if "Naechste Updates (Housekeeping Manager v3)" not in c:
        open(f, "w", encoding="utf-8").write(c + "\n" + roadmap)
        print("Roadmap angehaengt")
    else:
        print("Roadmap schon vorhanden")
