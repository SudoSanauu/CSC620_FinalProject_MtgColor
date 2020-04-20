import sys
import json
import re

if len(sys.argv) != 2:
	print("Please put in src file.")
	quit()

src_path = sys.argv[1]

with open(src_path, 'r') as f:
	cards = json.load(f)

# One problem with this rn is that since mtgjson has the cards nested in their
# sets and I just scooped them out of there, the json I got doesn't have their
# set or set abbreviation, so there is no way to tell reprints apart. This only
# matters if the flavor text changing changes matches and then we can't tell
# which set matches and which doesn't.`

# Pre-process the new cards
new_cards = []
for c in cards:
	# Get just the name and set for debugging purposes

	# try to get flavor text, if its not there return empty string, then remove
	# newlines
	flavorText = c.get("flavorText", "")
	flavorText = flavorText.replace("\n", " ")

	# remove newlines from rules text
	rulesText = c.get("text", "").replace("\n", " ")

	# I'm doing this additional logic on card type for if we add other types
	# which have to be handled differently (like including power/toughness)
	if c["types"] == ["Instant"]:
		text = " | ".join([c["type"], c["name"], rulesText, flavorText])
	elif c["types"] == ["Sorcery"]:
		text = " | ".join([c["type"], c["name"], rulesText, flavorText])
	else:
		print('Card :"', c.name,'" not of accepted types, please look over.')
		text = " | ".join([c["type"], c["name"], rulesText, flavorText])

	nc = { "name": c["name"], "text": text , "color": c["colors"] }
	new_cards.append(nc)

# compile REs
re_w_string = '(' \
	'soldier|valor|\slight\s|faith|[\s-]god-?' \
	'|destroy target tapped creature' \
	'|gain [0-9] life.*draw' \
	')'
w_re = re.compile(re_w_string, flags=re.IGNORECASE)

re_u_string = ('('
	'(gets|get) -\d/-\d until end of turn. Draw a card.'
	'|Look at the top three cards of your library'
	'|Counter target (creature|spell|noncreature)'
	'|Draw two cards.'
	'|(Put|Return) target (nonland permanent|creature)'
	'|can\'t be blocked this turn.'
	'|spell costs [0-9] less to cast'
	')')
u_re = re.compile(re_u_string, flags=re.IGNORECASE)

re_b_string = '(' \
	'murder|sacrifice|deathtouch|necromancer|lich' \
	'|deals? [0-9] damage.*gain [0-9] life' \
	'|loses [0-9] life.*gain [0-9] life' \
	'|target creature gets \-[34]/\-[34]' \
	'|(target|reveal).*discard' \
	'|return.*grave' \
	'|\sdie.*return' \
	')'
b_re = re.compile(re_b_string, flags=re.IGNORECASE)

re_r_string = ('('
	'to target (creature|player)'
	 '|deals [0-9] damage to any target'
	 '|gets +[0-9]/+[0-9] (until|and)'
	 '|Destroy target (artifact|land).'
	 '|Gain (control|trample)'
	 '|As an additional cost to cast this spell'
	 ''
	 ')')
r_re = re.compile(re_r_string, flags=re.IGNORECASE)

re_g_string = ('('
	'target creature gets \+[34]/\+[34]'
	'|deals damage equal to its power to target creature'
	'|destroy target creature with flying'
	'|natur.* destroy target artifact or enchantment'
	'|prevent all combat damage that would be dealt.* this turn.'
	')')
g_re = re.compile(re_g_string, flags=re.IGNORECASE)


# Run the cards through the REs to see their matches
correct = 0
incorrect = 0
for nc in new_cards:
	print("Working on ", nc["name"], " ...")
	# print(nc["text"])

	guess_color = []


	# ENABLE THIS FOR TESTING
	if w_re.search(nc["text"]): guess_color.append("W")
	if u_re.search(nc["text"]): guess_color.append("U")
	if b_re.search(nc["text"]): guess_color.append("B")
	if r_re.search(nc["text"]): guess_color.append("R")
	if g_re.search(nc["text"]): guess_color.append("G")

	if guess_color == nc["color"]:
		print("~~~ Correct for", nc["name"], "guessed", "".join(guess_color), "correctly ~~~\n")
		correct += 1
	# We'll need to figure out a better solution, since this doesn't work for
	# colorless cards at the moment
	elif guess_color == []:
		print("### Incorrect for", nc["name"], "couldn't guess any color, card was", "".join(nc["color"]), "###\n")
		incorrect +=1
	else:
		print("!!! Incorrect for", nc["name"], "guessed", "".join(guess_color), "not", "".join(nc["color"]), "!!!\n")
		incorrect +=1

print("\nFinished for all ", correct+incorrect, " cards:")
print("Correct = ", correct)
print("Incorrect = ", incorrect)
print("Accuracy = ", correct/(correct+incorrect))
