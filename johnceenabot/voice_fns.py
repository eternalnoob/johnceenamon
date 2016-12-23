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

@bot.command(pass_context=True)
async def cena(ctx):
    print(ctx)
    ended = asyncio.Event()
    voice_logger.info('trying to join channel')
    if ctx.message.author.voice_channel is not None:
        voicechn = await bot.join_voice_channel(ctx.message.author.voice_channel)
        ourbox.ended = asyncio.Event()
        player = voicechn.create_ffmpeg_player('johnceenabot/audio/invisible.mp3',
                                               after=ourbox.stop_player)
        player.start()
        await ourbox.ended.wait()
        await voicechn.disconnect()
    else:
        voice_logger.warning('user is not in a channel!')
