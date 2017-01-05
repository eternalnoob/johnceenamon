from johnceenabot.utils import bot
import markovify
import aiofiles
shitty_memes = [
    """It simply is not true? I know, butterflies, more important than 300 deaths which are based on the number of high school, I have peace.
Monkeys trained to fight, and I'm not a military sniper. You anything, but it was not. We wanted to determine the sex. I mean, I see the face of the earth.
If you think you can find something on the Internet? Evo cars. Be prepared for hidden spy network in the United States to attack the larvae of intellectual property rights, I must say better. The storm destroyed painful memories. Half of the children died. You can do it anywhere and I can already killed hundreds of hands. This is wrong, but smaller oil reserves, like an old man "that some phones Navy to play ugly." But now we can not pay ridiculous prices. I do not want to disrupt their wounds.
Half of the children died.""",
]

with open('munroe_chains.json', mode='r') as f:
    contents = f.read()
    markov = markovify.Text.from_json(contents)

with open('horror_chains.json', mode='r') as f:
    contents = f.read()
    horror_markov = markovify.Text.from_json(contents)

with open('seinfeldia.json', mode='r') as f:
    contents = f.read()
    ree_bees = markovify.Text.from_json(contents)

@bot.command()
async def greyfacefromspace():
    sentence = horror_markov.make_sentence()
    await sayitall(sentence)

@bot.command(pass_context=True)
async def tellmeastory(ctx):
    try:
        sentence = horror_markov.make_sentence_with_start(' '.join(ctx.message.content.split(' ')[1:]))
        await sayitall(sentence)
    except:
        await bot.say("lol I can't tho")

@bot.command()
async def noneroe():
    sentence = markov.make_sentence()
    await sayitall(sentence)

@bot.command()
async def datbee():
    sentence = ree_bees.make_sentence()
    await sayitall(sentence)

@bot.command(pass_context=True)
async def datbeestory(ctx):
    try:
        sentence = ree_bees.make_sentence_with_start(' '.join(ctx.message.content.split(' ')[1:]))
        await sayitall(sentence)
    except:
        await bot.say("lol I can't tho")

@bot.command(pass_context=True)
async def talkback(ctx):
    try:
        sentence = ' '.join(ctx.message.content.split(' ')[1:])
        await sayitall(sentence)
    except:
        await bot.say("lol I can't tho")

async def sayitall(sentence):
    await bot.saytext(sentence)
    await bot.say(sentence)



