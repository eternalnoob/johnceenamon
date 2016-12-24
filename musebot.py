from discord.ext.commands import Bot

import logging
import asyncio

from asyncio import Queue

voice_logger = logging.getLogger('voice')



class MusicBox(object):
    # basic loop is to go through the list after each play to grab
    # next song, then create appropriate player for initializing it


    def __init__(self):
        self.player = None
        self.ended = asyncio.Event()
        self.queue = Queue()



    # utilities for creating and setting up different player types
    # self.ended will be used as the await for trying to get the next song
    async def player_check(self):
        if self.ended.is_set():
            if not self.queue.empty():
                self.player = await self.queue.get()
                await self.say(self.player.)
                self.player.start()
                self.ended.clear()
            else:
                print('hmmmm')

    async def start_loop(self):
        await self.player_check()


    async def stop_player(self):
        """
        used to both stop player at end of player completion as well
        as on user command
        :return: None
        """
        if self.player and self.player.is_playing():
            voice_logger.info('Something playing, stopping it')
            self.player.stop()
            voice_logger.info('Player stopped')
        self.ended.set()
        self.check_quit()

    async def add_song(self, player):
        await self.queue.put(player)

    async def add_mp3(self, player):
         self.queue.put_nowait(player)



class MuseBot(Bot, MusicBox):

    def __init__(self, *args, **kwargs):
        Bot.__init__(self, *args, **kwargs)
        MusicBox.__init__(self)
        self.voice_channel = None
        self.inChannel = asyncio.Event()


    async def summon(self, ctx):
        if ctx.message.author.voice_channel is not None:
            self.voice_channel = await self.join_voice_channel(ctx.message.author.voice_channel)
            self.inChannel.set()
            await self.say('In there')
        else:
            voice_logger.warning('user is not in a channel!')
            await self.say('Can\'t ceema to figure out what\'s wrong (not in voice channel)')

    async def desummon(self, ctx):
        if self.inChannel.is_set():
            await self.voice_channel.disconnect()
            self.inChannel.clear()

    async def makemp3player(self, mp3_path):
        if self.inChannel.is_set():
            player = self.voice_channel.create_ffmpeg_player(mp3_path,
                                                                  after=self.stop_player)
            await self.add_mp3(player)
            await self.say('We ran it alright')
            await self.say(self.queue.qsize())

    async def makeytplayer(self, yt_path):
        if self.inChannel.is_set():
            await self.add_song(await self.voice_channel.create_ytdl_player(yt_path,
                                                                      after=self.stop_player))

