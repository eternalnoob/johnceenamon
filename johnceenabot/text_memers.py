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

@bot.command()
async def noneroe():

    await bot.say(markov.make_sentence())


