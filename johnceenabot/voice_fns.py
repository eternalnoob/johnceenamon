from johnceenabot.utils import bot
from IPython import embed
import discord
import logging
import asyncio


@bot.command()
async def cena():
    """:trumpet::trumpet::trumpet::trumpet:"""
    await bot.makemp3player('johnceenabot/audio/invisible.mp3')
    await bot.say(":trumpet::trumpet::trumpet:")

@bot.command()
async def reallycena():
    """:trumpet::trumpet::trumpet::trumpet:"""
    await bot.makeytplayer('https://www.youtube.com/watch?v=wjNtB5g70ic')
    await bot.say(":trumpet::trumpet::trumpet:")
    bot.player.start()

@bot.command()
async def nash():
    await bot.makemp3player('johnceenabot/audio/vape-nation.mp3')

@bot.command(pass_context=True)
async def desummon(ctx):
    await bot.desummon(ctx)

@bot.command(pass_context=True)
async def summon(ctx):
    await bot.summon(ctx)

@bot.command()
async def getit():
    await bot.makeytplayer('https://www.youtube.com/watch?v=PfYnvDL0Qcw')

@bot.command()
async def reallygetit():
    await bot.makeytplayer('https://www.youtube.com/watch?v=vkOJ9uNj9EY')

@bot.command()
async def mondaymitts():
    await bot.makeytplayer('https://www.youtube.com/watch?v=_ykAXB3JFy4')

@bot.command()
async def dmrainbow():
    await bot.makeytplayer('https://www.youtube.com/watch?v=OchyYnlHTdo')

@bot.command()
async def play():
    await bot.start_loop()

@bot.command()
async def stop():
    bot.stop_player()

@bot.command(pass_context=True)
async def addtube(ctx):
    try:
        URL = ctx.message.content.split(' ')[1]
        await bot.makeytplayer(URL)
    except:
        await bot.say('u suck at URL, kid')

@bot.command()
async def changevol( volume : float ):
    try:
        await bot.setvol(volume)
    except Exception:
        await bot.say('u suck at volumes, kid')

@bot.command()
async def vol( volume : float ):
    try:
        await bot.setvol(volume)
    except Exception:
        await bot.say('u suck at volumes, kid')

@bot.command()
async def areuok():
    await bot.say('I feel . . . pain')

