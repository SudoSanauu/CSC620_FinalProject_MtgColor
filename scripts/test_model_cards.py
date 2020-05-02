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
		return log2(model['freq'][token] / (model['token_count'] + 1))
	return log2(1 / (model['token_count'] + 1))



model_path = sys.argv[1]
card_path = sys.argv[2]

print("reading model from ", model_path)
with open(model_path, 'r') as f: # , format="utf8"?
	model = json.load(f)

print("reading cards from ", card_path)
with open(card_path, 'r') as f: # , format="utf8"?
	cards = json.load(f)

for c in cards:
	rules_tokens = tp.rules_tokenize(c)
	card_probs = []

	for color in model:
		m = model[color]

		# scale by prob of card in model
		rules_prob = log2(m['numCards'])

		if rules_tokens == []:
			rules_prob += get_prob('', m['rules'])
		for t in rules_tokens:
			rules_prob += get_prob(t, m['rules'])

		flavor_prob = log2(m['numCards'])

		if 'flavorText' in c:
			flavor_tokens = tp.flavor_tokenize(c)

			if flavor_tokens == []:
				flavor_prob += get_prob('', m['flavor'])	
			else:
				for t in flavor_tokens:
					flavor_prob += get_prob(t, m['flavor'])	
		else:
			flavor_prob = get_prob('', m['flavor'])	
		card_probs.append({
			'rules_prob': rules_prob,
			'flavor_prob': flavor_prob,
			'color': color
		})

	print("For card ", c['name'],':')
	
	for d in card_probs:
		s = "{0} RP: {1:f} FP: {2:f} TP: {3:f}"
		print(s.format(d['color'], d['rules_prob'], d['flavor_prob'], (d['rules_prob'] + d['flavor_prob'])))
