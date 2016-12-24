from johnceenabot.utils import bot
from IPython import embed
import discord
import logging
import asyncio


@bot.command()
async def cena():
    await bot.makemp3player('johnceenabot/audio/invisible.mp3')

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
async def play():
    await bot.start_loop()

@bot.command(pass_context=True)
async def addtube(ctx):
    try:
        URL = ctx.message.content.split(' ')[1]
        await bot.makeytplayer(URL)
    except Exception:
        await bot.say('u suck at URL, kid')
