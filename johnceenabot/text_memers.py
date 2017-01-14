from johnceenabot.utils import bot
import markovify
import aiofiles
import random
shitty_memes = [
    """It simply is not true? I know, butterflies, more important than 300 deaths which are based on the number of high school, I have peace.
Monkeys trained to fight, and I'm not a military sniper. You anything, but it was not. We wanted to determine the sex. I mean, I see the face of the earth.
If you think you can find something on the Internet? Evo cars. Be prepared for hidden spy network in the United States to attack the larvae of intellectual property rights, I must say better. The storm destroyed painful memories. Half of the children died. You can do it anywhere and I can already killed hundreds of hands. This is wrong, but smaller oil reserves, like an old man "that some phones Navy to play ugly." But now we can not pay ridiculous prices. I do not want to disrupt their wounds.
Half of the children died.""",

    """His palms are spaghetti, knees weak, arms spaghetti
There's vomit on his spaghetti already: mom's spaghetti
He's nervous, but on the surface he looks calm spaghetti
To drop spaghetti, but he keeps on spaghetti
What he wrote down, the whole crowd goes spaghetti
He opens his mouth but spaghetti won't come out
He's choking, how? Everybody's joking now
The spaghetti's run out, time's up, over - blaow!
Snap back to spaghetti, oh! - there goes gravity"""

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
    except: await bot.say("lol I can't tho")

@bot.command(pass_context=True)
async def shittymemes(ctx):
    try:
        sentence = random.choice(shitty_memes)
        await sayitall(sentence)
    except:
        await bot.say("lol I can't tho")

@bot.command(pass_context=True)
async def whatdidusay(ctx):
    try:
        sentence = """What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated top of my class in the Navy Seals, and I’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo."""
        await sayitall(sentence)
    except:
        await bot.say("lol I can't tho")

async def sayitall(sentence):
    await bot.saytext(sentence)
    await bot.say(sentence)




