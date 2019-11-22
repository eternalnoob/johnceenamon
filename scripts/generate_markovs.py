import markovify

# Get raw text as string.
texts = []
with open("transcripts.txt") as f:
    texts.append((f.read(), "munroe_chains.json"))

with open("scury.txt") as f:
    texts.append((f.read(),"horror_chains.json"))

with open("aviation.txt") as f:
    texts.append((f.read(),"seinfeldia.json"))

# Build the model.
for text in texts:
    text_model = markovify.Text(text[0], state_size=2)

    # Print five randomly-generated sentences
    for i in range(5):
        print(text_model.make_sentence())

    # Print three randomly-generated sentences of no more than 140 characters
    for i in range(3):
        print(text_model.make_short_sentence(140))

    model_json = text_model.to_json()

    with open(text[1], 'w') as markout:
        markout.write(model_json)


