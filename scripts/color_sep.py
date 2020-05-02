import sys
import json

if len(sys.argv) != 3:
    print("Please put in src file and destination file.")
    quit()

card_path = sys.argv[1]
dest_path = sys.argv[2]


print("reading from ", card_path)
with open(card_path, 'r') as f: # , format="utf8"?
    cards = json.load(f)
    
allowed_types = ["Instant", "Sorcery"]
allowed_colors = ["B", "W", "U", "G", "R"]
color_long = {'R': 'Red', 'U': 'Blue', 'B': 'Black', 'W': 'White', 'G': 'Green'}

card_list = {
    'Red': [],
    'Black': [],
    'Blue': [],
    'White': [],
    'Green': []
}

for c in cards:
    if "common" not in c['rarity']:
        continue
    if len(c['colors']) > 1 or c['colors'][0] not in allowed_colors:
        continue
    if c['type'] not in allowed_types:
        continue
        
    color = c['colors'][0]
    card_list[color_long[color]].append(c)
    

with open(dest_path, 'w') as f:
    # print(json.dumps(card_list, ensure_ascii=False, sort_keys=True, indent=2))
    json.dump(card_list, f, ensure_ascii=False, sort_keys=True, indent=2)
