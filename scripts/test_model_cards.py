import sys
import json
import re
import text_processing as tp
from math import log2


if len(sys.argv) != 3:
	print("Please put in src file and destination file.")
	quit()

def get_prob(token, model):
	# this is wrong and not real leplace smoothing
	if token in model['freq']:
		return log2(model['freq'][token] / model['token_count'])
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
	rules_tokens = tp.rules_tokenize(c)

	rules_prob = 0.0

	if rules_tokens == []:
		rules_prob += get_prob('', model['rules'])
	for t in rules_tokens:
		rules_prob += get_prob(t, model['rules'])


	flavor_prob = 0.0

	if 'flavorText' in c:
		flavor_tokens = tp.flavor_tokenize(c)

		if flavor_tokens == []:
			flavor_prob += get_prob('', model['flavor'])	
		else:
			for t in flavor_tokens:
				flavor_prob += get_prob(t, model['flavor'])	
	else:
		flavor_prob = get_prob('', model['flavor'])	

	print("For card ", c['name'],':')
	print("RP: ", 2 ** rules_prob, " FP: ", 2 ** flavor_prob, " TP: ", 2 ** (rules_prob + flavor_prob))
	# test 3 setups: just rules, just flavor, and rules * flavor, use f1



# 1) Make one data file
# 2) Make better pre-processing (stop list)
# 3) upgrade to bi/trigrams
