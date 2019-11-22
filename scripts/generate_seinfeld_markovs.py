import csv
import os.path
import markovify
import typing

DIA = 'Dialogue'
CHAR = 'Character'
with open('scripts.csv', 'r') as fin:
    reader = csv.DictReader(fin)
    chars = {} 
    for row in reader:
        dialogue = row[DIA]
        character = row[CHAR].lower()
        x = []
        if character in chars:
            x = chars[character]
        x.append(dialogue)
        chars[character] = x

    for char, text in chars.items():
        alltext = ' '.join(text)
        valid = True 
        try:
            markov = markovify.Text(alltext)
            sent = markov.make_sentence(tries=500)
            if not sent:
                valid = False
        except Exception:
            valid = False
            pass

        if valid:
            print(sent)
            print(char)
            as_json = markov.to_json()

            try:
                with open("../chains/chain_%s.json" % char.replace(' ',''), 'w') as fout:
                    fout.write(str(as_json))
            except Exception as e:
                pass


