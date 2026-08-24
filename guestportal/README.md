# guestportal/ — Platzhalter für ein späteres Projekt

Dieser Ordner ist bewusst leer (bis auf diese Datei) und **nicht live**.

## Warum es ihn gibt

Ein erster Entwurf für ein eigenständiges Gäste-Portal (Concierge-Chat mit
erfundener Person "Alexander", spekulative Gäste-Pakete, WhatsApp-Fluss ohne
bestätigte Nummer) wurde am 24.08.2026 verworfen — er widersprach dem in
`index.html` bereits etablierten Prinzip *"keine erfundenen Personen/Fakten"*
und duplizierte, was das bestehende Gäste-Fragen-Widget in `index.html`
schon leistet.

Der tatsächliche Bedarf (Sauna- und Umgebungs-Infos) wurde stattdessen direkt
als zwei neue Einträge in `GUEST_FAQ` (`index.html`) ergänzt — kein neues
Widget, keine Dopplung.

## Wofür der Ordner reserviert bleibt

Falls später ein **echter** KI-gestützter Chatbot für Gäste entstehen soll
(mit echtem Backend/Modell statt Klick-Simulation, mit abgestimmter
WhatsApp-Nummer, mit Nicole/Rezeption abgesprochen) — dann ist das ein
eigenständiges neues Projekt, kein Merge in `index.html`. Dieser Ordner ist
der vorgesehene Startpunkt dafür, wenn es soweit ist.

Bis dahin: nichts hier deployen, nichts hier verlinken.
