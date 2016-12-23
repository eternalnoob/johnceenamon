import markovify

# Get raw text as string.
with open("transcripts.txt") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text, state_size=2)

# Print five randomly-generated sentences
for i in range(5):
    print(text_model.make_sentence())

# Print three randomly-generated sentences of no more than 140 characters
for i in range(3):
    print(text_model.make_short_sentence(140))

model_json = text_model.to_json()

with open("munroe_chains.json", 'w') as markout:
    markout.write(model_json)


