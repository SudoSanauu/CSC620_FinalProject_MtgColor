import re

# declare constants & compile res
no_reminder = re.compile("\([^)]*\)")
no_useless = re.compile("[\.,'\"!—]")
no_newline = re.compile("\n")
space_colon = re.compile(":")
split_pattern = re.compile(' ')

rules_stoplist = ['the', 'of', '', 'with']
r_slist_fun = lambda f: not f in rules_stoplist

flavor_stoplist = ['the', '', 'a', 'to', 'an', 'it', 'its']
f_slist_fun = lambda f: not f in flavor_stoplist



def rules_tokenize(card):
	# replace cardname with @ and makes all lowercase
	new_rules = card['text'].replace(card['name'], "@").lower()

	# remove all reminder text in parens
	new_rules = no_reminder.sub("", new_rules)

	# get rid of useless characters
	new_rules = no_useless.sub("", new_rules)

	# replace \n with ' '
	new_rules = no_newline.sub(" ", new_rules)

	# edit : to be separated with spaces so it becomes its own token
	new_rules = space_colon.sub(' :', new_rules)

	# split tokens and remove stop words
	return list(filter(r_slist_fun, split_pattern.split(new_rules)))

def flavor_tokenize(card):
	# all lowercase
	new_flavor = card['flavorText'].lower()

	# get rid of useless characters
	new_flavor = no_useless.sub("", new_flavor)

	# replace \n with ' '
	new_flavor = no_newline.sub(" ", new_flavor)

	# split tokens and remove stop words
	return list(filter(f_slist_fun, split_pattern.split(new_flavor)))

def token_to_bigram(tokens):
	# S & E are start and end tokens
	new_tok = ['S'] + tokens + ['E']
	outlist = ['']*(len(new_tok)-1)
	
	for i in range(0, len(new_tok)-1):
		outlist[i] = '(' + new_tok[i] + ',' +  new_tok[i+1] + ')'

	return outlist
