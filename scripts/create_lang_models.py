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
	card_json = json.load(f)

final_dict = {}

for color in card_json:
	cards = card_json[color]
	rules_token_count = 0
	rules_freq_dict = {}
	flavor_token_count = 0
	flavor_freq_dict = {}

	for c in cards:
		rules_tokens = tp.rules_tokenize(c)
		rules_bigrams = tp.token_to_bigram(rules_tokens)

		if rules_tokens == []:
			insert_incr_dict(rules_freq_dict, '')
			rules_token_count += 1
		else:
			for t in rules_tokens:
				insert_incr_dict(rules_freq_dict, t)
				rules_token_count += 1


		if 'flavorText' in c:
			flavor_tokens = tp.flavor_tokenize(c)
			flavor_bigrams = tp.token_to_bigram(flavor_tokens)

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

	color_dict = {
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

	final_dict[color] = color_dict

with open(dest_path, 'w') as f:
    json.dump(final_dict, f, ensure_ascii=False, sort_keys=True, indent=2)


