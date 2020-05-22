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

# I know this isn't the most efficent way to do this, but I've already written 
# code and just want to finish up
# also using lists instead of objects or dicts is also bad, but I remain
# impatient and lazy
def get_best_prob(card_probs):
	max_rules = [card_probs[0]['rules_prob'], card_probs[0]['color']]
	max_flavor = [card_probs[0]['flavor_prob'], card_probs[0]['color']]
	max_both = [(max_rules[0] + max_flavor[0]), card_probs[0]['color']]

	for i in range(1,5):
		new_rules_prob = card_probs[i]['rules_prob']
		new_flavor_prob = card_probs[i]['flavor_prob']
		new_both_prob = new_rules_prob + new_flavor_prob

		if new_rules_prob > max_rules[0]:
			max_rules = [new_rules_prob, card_probs[i]['color']]

		if new_flavor_prob > max_flavor[0]:
			max_flavor = [new_flavor_prob, card_probs[i]['color']]

		if new_both_prob > max_both[0]:
			max_both = [
				new_both_prob,
				card_probs[i]['color'] ]
	
	return [max_rules[1], max_flavor[1], max_both[1]]





model_path = sys.argv[1]
card_path = sys.argv[2]

print("reading model from ", model_path)
with open(model_path, 'r') as f: # , format="utf8"?
	model = json.load(f)

print("reading cards from ", card_path)
with open(card_path, 'r') as f: # , format="utf8"?
	cards = json.load(f)

# This will be a 5/5 matrix where each row represents the actual color and each
# col represents the guessed color. All elements in [n,n] are correct, while any
# [a,b] where a /= b are incorrect
index_map = { 'W': 0, 'U': 1, 'B': 2, 'R': 3, 'G': 4 }
rules_result_mat = [[0] * 5, [0] * 5, [0] * 5, [0] * 5, [0] * 5]
flavor_result_mat = [[0] * 5, [0] * 5, [0] * 5, [0] * 5, [0] * 5]
both_result_mat = [[0] * 5, [0] * 5, [0] * 5, [0] * 5, [0] * 5]



for cur_color in cards.keys():
	for c in cards[cur_color]:
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


		# choose largest rules flavor and combined prob for each card and add it to the matrix
		[rule_guess_color, flavor_guess_color, both_guess_color] = get_best_prob(card_probs)

		[row, col] = [index_map[cur_color], index_map[rule_guess_color]]
		rules_result_mat[row][col] += 1

		[row, col] = [index_map[cur_color], index_map[flavor_guess_color]]
		flavor_result_mat[row][col] += 1

		[row, col] = [index_map[cur_color], index_map[both_guess_color]]
		both_result_mat[row][col] += 1

		print("For card ", c['name'],':')
		print("Actual color: ", cur_color)
		print("Rules guess: ", rule_guess_color,
			" Flavor Guess: ", flavor_guess_color,
			 " Both Guess: ", both_guess_color)
		# for d in card_probs:
		# 	s = "{0} RP: {1:f} FP: {2:f} TP: {3:f}"
		# 	print(s.format(d['color'], d['rules_prob'], d['flavor_prob'], (d['rules_prob'] + d['flavor_prob'])))

print('rules')
for r in rules_result_mat:
	print(r)

print('flavor')
for r in flavor_result_mat:
	print(r)

print('both')
for r in both_result_mat:
	print(r)


