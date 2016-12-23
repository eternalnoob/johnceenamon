from johnceenabot.utils import bot
from IPython import embed
import discord
import logging
import asyncio


voice_logger = logging.getLogger('voice')

@bot.command(pass_context=True)
async def cena(ctx):
    print(ctx)
    #discord.opus.load_opus('opus')
    voice_logger.info('trying to join channel')

    if ctx.message.author.voice_channel is not None:
        print(bot)
        voicechn = await bot.join_voice_channel(ctx.message.author.voice_channel)
        player = voicechn.create_ffmpeg_player('johnceenabot/audio/invisible.mp3')
        player.start()
    else:
        voice_logger.warning('user is not in a channel!')
        print('shit')




