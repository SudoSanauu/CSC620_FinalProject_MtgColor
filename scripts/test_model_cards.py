import sys
import json
import re


if len(sys.argv) != 3:
	print("Please put in src file and destination file.")
	quit()

def get_prob(token, model):
	# this is wrong and not real leplace smoothing
	if token in model['freq']:
		return model['freq'][token] / model['token_count']
	print("can't find token ", token, " in model.")
	raise error


model_path = sys.argv[1]
card_path = sys.argv[2]

print("reading model from ", model_path)
with open(model_path, 'r') as f: # , format="utf8"?
	model = json.load(f)


print("reading cards from ", card_path)
with open(card_path, 'r') as f: # , format="utf8"?
	cards = json.load(f)



no_reminder = re.compile("\([^)]*\)")
no_useless = re.compile("[\.,'\"!]")
no_newline = re.compile("\n")
space_colon = re.compile(":")
split_on_space = re.compile(' ')



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

	rules_prob = 1.0

	for t in rules_tokens:
		rules_prob *= get_prob(t, model['rules'])


	flavor_prob = 1.0

	if 'flavorText' in c:
		new_flavor = c['flavorText'].lower()

		# get rid of useless characters
		new_flavor = no_useless.sub("", new_flavor)

		# replace \n with ' '
		new_flavor = no_newline.sub(" ", new_flavor)

		# put into dict
		flavor_tokens = split_on_space.split(new_flavor)

		for t in flavor_tokens:
			flavor_prob *= get_prob(t, model['flavor'])	
	else:
		flavor_prob = get_prob('', model['flavor'])	

	print("For card ", c['name'],':')
	print("RP: ", rules_prob, " FP: ", flavor_prob, " TP: ", rules_prob * flavor_prob)

