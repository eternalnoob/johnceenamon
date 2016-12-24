from johnceenabot.utils import bot
from IPython import embed
import discord
import logging
import asyncio


voice_logger = logging.getLogger('voice')



#honestly isn't this all we need?

class MusicBox(object):
    def __init__(self, avconv=False):
        self.player = None
        self.ended = asyncio.Event()

    def stop_player(self):
        if self.player and self.player.is_playing():
            voice_logger.info('Something playing, stopping it')
            self.player.stop()
            voice_logger.info('Player stopped')
        self.ended.set()


ourbox = MusicBox()



async def connect_voice(ctx, mp3_path):
    ourbox.ended = asyncio.Event()
    voice_logger.info('trying to join channel')
    try:
        if ctx.message.author.voice_channel is not None:
            voicechn = await bot.join_voice_channel(ctx.message.author.voice_channel)
            await playmp3(voicechn, mp3_path)
        else:
            voice_logger.warning('user is not in a channel!')
            await bot.say('Can\'t ceema to figure out what\'s wrong (not in voice channel)')
    except AttributeError:
        await bot.say('Can\'t Play!')

async def playmp3(voicechn, mp3_path):
    ourbox.ended = asyncio.Event()
    player = voicechn.create_ffmpeg_player(mp3_path,
                                           after=ourbox.stop_player)
    player.start()
    await ourbox.ended.wait()
    await voicechn.disconnect()

@bot.command(pass_context=True)
async def cena(ctx):
    await connect_voice(ctx, 'johnceenabot/audio/invisible.mp3')

@bot.command(pass_context=True)
async def nash(ctx):
    await connect_voice(ctx, 'johnceenabot/audio/vape-nation.mp3')

