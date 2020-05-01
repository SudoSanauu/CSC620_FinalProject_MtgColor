import sys
import json
import re
import text_processing as tp


def insert_incr_dict(inDict, token):
    if token in inDict:
        inDict[token] += 1
    else:
         inDict[token] = 1



if len(sys.argv) != 3:
    print("Please put in src file and destination file.")
    quit()

card_path = sys.argv[1]
dest_path = sys.argv[2]


print("reading from ", card_path)
with open(card_path, 'r') as f: # , format="utf8"?
    cards = json.load(f)

# rules_token_count = 0
# rules_freq_dict = {}
# flavor_token_count = 0
# flavor_freq_dict = {}

allowed_types = ["Instant", "Sorcery"]
token_freq = {
    'R': {'rules': {}, 'flavor': {}},
    'B': {'rules': {}, 'flavor': {}},
    'U': {'rules': {}, 'flavor': {}},
    'W': {'rules': {}, 'flavor': {}},
    'G': {'rules': {}, 'flavor': {}}
}

token_count = {
    'R': {'rules': 0, 'flavor': 0},
    'B': {'rules': 0, 'flavor': 0},
    'U': {'rules': 0, 'flavor': 0},
    'W': {'rules': 0, 'flavor': 0},
    'G': {'rules': 0, 'flavor': 0}
}

card_count = {
    'total': 0,
    'R': 0,
    'B': 0,
    'U': 0,
    'W': 0,
    'G': 0
}

card_list = {
    'R': [],
    'B': [],
    'U': [],
    'W': [],
    'G': []
}

for c in cards:
    if "common" not in c['rarity']:
        continue
    if len(c['colors']) > 1 or c['colors'][0] not in token_freq:
        continue
    if c['type'] not in allowed_types:
        continue
        
    rules_tokens = tp.rules_tokenize(c)
    color = c['colors'][0]
    
    card_count['total'] += 1
    card_count[color] += 1
    card_list[color].append(c)

    if rules_tokens == []:
		# insert_incr_dict(rules_freq_dict, '')
		# rules_token_count += 1
        insert_incr_dict(token_freq[color]['rules'], '')
        token_count[color]['rules'] +=1
    else:
        for t in rules_tokens:
			# insert_incr_dict(rules_freq_dict, t)
			# rules_token_count += 1
            insert_incr_dict(token_freq[color]['rules'], t)
            token_count[color]['rules'] +=1



    if 'flavorText' in c:
        flavor_tokens = tp.flavor_tokenize(c)
        if flavor_tokens == []:
			# insert_incr_dict(flavor_freq_dict, '')
			# flavor_token_count += 1
            insert_incr_dict(token_freq[color]['flavor'], '')
            token_count[color]['flavor'] +=1
        else:
            for t in flavor_tokens:
				# insert_incr_dict(flavor_freq_dict, t)
				# flavor_token_count += 1
                insert_incr_dict(token_freq[color]['flavor'], t)
                token_count[color]['flavor'] +=1
    else:
		# insert_incr_dict(flavor_freq_dict, '')
		# flavor_token_count += 1
        insert_incr_dict(token_freq[color]['flavor'], '')
        token_count[color]['flavor'] +=1

"""
outData = {
	'numCards': len(cards),
	'rules': {
		'token_count': rules_token_count,
		'freq': rules_freq_dict
	},
	'flavor': {
		'token_count': flavor_token_count,
		'freq': flavor_freq_dict
	}
}
"""

outData = {
    'numCards': card_count['total'],
    'black': {
        'numCards': card_count['B'],
        'rules': {
            'token_count': token_count['B']['rules'],
            'freq': token_freq['B']['rules']
        },
        'flavor': {
            'token_count': token_count['B']['flavor'],
            'freq': token_freq['B']['flavor']
        }
    },
    'white': {
        'numCards': card_count['W'],
        'rules': {
            'token_count': token_count['W']['rules'],
            'freq': token_freq['W']['rules']
        },
        'flavor': {
            'token_count': token_count['W']['flavor'],
            'freq': token_freq['W']['flavor']
        }
    },
    'blue': {
        'numCards': card_count['U'],
        'rules': {
            'token_count': token_count['U']['rules'],
            'freq': token_freq['U']['rules']
        },
        'flavor': {
            'token_count': token_count['U']['flavor'],
            'freq': token_freq['U']['flavor']
        }
    },
    'red': {
        'numCards': card_count['R'],
        'rules': {
            'token_count': token_count['R']['rules'],
            'freq': token_freq['R']['rules']
        },
        'flavor': {
            'token_count': token_count['R']['flavor'],
            'freq': token_freq['R']['flavor']
        }
    },
    'green': {
        'numCards': card_count['G'],
        'rules': {
            'token_count': token_count['G']['rules'],
            'freq': token_freq['G']['rules']
        },
        'flavor': {
            'token_count': token_count['G']['flavor'],
            'freq': token_freq['G']['flavor']
        }
    }
}

with open(dest_path, 'w') as f:
    json.dump(outData, f, ensure_ascii=False, sort_keys=True, indent=2)




