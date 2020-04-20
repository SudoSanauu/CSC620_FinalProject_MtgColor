import sys
import json
import re


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


no_reminder = re.compile("\([^)]*\)")
no_useless = re.compile("[\.,'\"!]")
no_newline = re.compile("\n")
space_colon = re.compile(":")
split_on_space = re.compile(' ')


rules_token_count = 0
rules_freq_dict = {}
flavor_token_count = 0
flavor_freq_dict = {}

for c in cards:
	# replace cardname with @ and makes all lowercase
	new_rules = c['text'].replace(c['name'], "@").lower()

	# remove all reminder text in parens
	new_rules = no_reminder.sub("", new_rules)

	# get rid of useless characters
	new_rules = no_useless.sub("", new_rules)

	# replace \n with ' '
	new_rules = no_newline.sub(" ", new_rules)

	# edit : to be separated with spaces so it becomes its own token
	new_rules = space_colon.sub(' :', new_rules)

	# put into dict
	rules_tokens = split_on_space.split(new_rules)
	if rules_tokens == []:
		insert_incr_dict(rules_freq_dict, '')
		rules_token_count += 1
	# else:
	for t in rules_tokens:
		insert_incr_dict(rules_freq_dict, t)
		rules_token_count += 1


	if 'flavorText' in c:
		new_flavor = c['flavorText'].lower()

		# get rid of useless characters
		new_flavor = no_useless.sub("", new_flavor)

		# replace \n with ' '
		new_flavor = no_newline.sub(" ", new_flavor)

		# put into dict
		flavor_tokens = split_on_space.split(new_flavor)			
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
	json.dump(outData, f)




