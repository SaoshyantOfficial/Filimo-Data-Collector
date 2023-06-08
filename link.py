"""saving movies and series links to gather their data"""

import json

links = ["https://www.filimo.com/m/vef58", "https://www.filimo.com/m/l1uef", "https://www.filimo.com/m/121775"]

with open("links.json", "w") as f:
    json.dump(links, f)
f.close()