f = "housekeeping/housekeeping-v3.html"
c = open(f, encoding="utf-8").read()

old_langbtns = """    <button class="lang-btn active" onclick="setLang('de')">\U0001F1E9\U0001F1EA DE</button>
    <button class="lang-btn" onclick="setLang('en')">\U0001F1EC\U0001F1E7 EN</button>
    <button class="lang-btn" onclick="setLang('hu')">\U0001F1ED\U0001F1FA HU</button>
"""
assert c.count(old_langbtns) == 1, "Sprachbuttons-Anker nicht eindeutig: " + str(c.count(old_langbtns))
c = c.replace(old_langbtns, "", 1)

open(f, "w", encoding="utf-8").write(c)
print("OK: Sprachbuttons entfernt")
