import logging
discordLogger = logging.getLogger('discord')
discordLogger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
discordLogger.addHandler(handler)
from discord.ext import commands
import musebot

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = musebot.MuseBot(command_prefix='?', description=description)


