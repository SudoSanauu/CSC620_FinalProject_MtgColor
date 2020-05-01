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



rules_token_count = 0
rules_freq_dict = {}
flavor_token_count = 0
flavor_freq_dict = {}

for c in cards:
	rules_tokens = tp.rules_tokenize(c)

	if rules_tokens == []:
		insert_incr_dict(rules_freq_dict, '')
		rules_token_count += 1
	else:
		for t in rules_tokens:
			insert_incr_dict(rules_freq_dict, t)
			rules_token_count += 1


	if 'flavorText' in c:
		flavor_tokens = tp.flavor_tokenize(c)
		if flavor_tokens == []:
			insert_incr_dict(flavor_freq_dict, '')
			flavor_token_count += 1
		else:
			for t in flavor_tokens:
				insert_incr_dict(flavor_freq_dict, t)
				flavor_token_count += 1
	else:
		insert_incr_dict(flavor_freq_dict, '')
		flavor_token_count += 1



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

with open(dest_path, 'w') as f:
    json.dump(outData, f, ensure_ascii=False, sort_keys=True, indent=2)




