from discord.ext.commands import Bot

import logging
import asyncio
from gtts import gTTS
from strawpoll import StrawPoll

from asyncio import Queue, QueueEmpty

voice_logger = logging.getLogger('voice')



class MusicBox(object):
    # basic loop is to go through the list after each play to grab
    # next song, then create appropriate player for initializing it


    def __init__(self):
        self.player = None
        self.ended = asyncio.Event()
        self.queue = Queue()
        self.ended.set()
        self.volume = .5
        self.interrupted = list()



    # utilities for creating and setting up different player types
    # self.ended will be used as the await for trying to get the next song
    async def player_check(self):
        print('x)')
        if self.ended.is_set():
            print('y')
            self.player = await self.queue.get()
            await self.say(str(self.player.volume))
            await self.say(str(self.player))
            self.player.volume = self.volume
            await self.say(str(self.player.volume))
            self.player.start()
            self.ended.clear()

    async def start_loop(self):
        await self.player_check()

    def stop_player(self):
        """
        used to both stop player at end of player completion as well
        as on user command
        :return: None
        """
        if self.player and self.player.is_playing():
            voice_logger.info('Something playing, stopping it')
            self.player.stop()
            voice_logger.info('Player stopped')

        try:
            check_next = self.queue.get_nowait()
            if check_next:
                self.player = check_next
                self.player.volume = self.volume
                self.player.start()
            else:
                self.ended.set()
        except:
            self.ended.set()


    async def add_song(self, player):
        await self.queue.put(player)

    async def add_mp3(self, player):
         await self.queue.put(player)

    async def setvol(self, vol):
        self.volume = vol
        if self.player is not None:
            self.player.volume = vol



class MuseBot(Bot, MusicBox):

    def __init__(self, *args, **kwargs):
        Bot.__init__(self, *args, **kwargs)
        MusicBox.__init__(self)
        self.voice_channel = None
        self.inChannel = asyncio.Event()
        self.strawpoll = None


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
            player = await self.voice_channel.create_ytdl_player(yt_path,
                                                                 after=self.stop_player)
            if 'pink' in player.description.lower() or 'pink' in player.title.lower():
                await self.say('NICE TRY, KID')
            else:
                await self.add_song(player)

    async def saytext(self, text):
        if self.voice_channel is not None:
            tts = gTTS(text=text,lang='en')
            filename = 'mp3/' + text.split(' ')[0] +'.mp3'
            file = tts.save(savefile=filename)
            if self.player is not None:
                self.interrupted.append(self.player)
                self.player.pause()
            self.player = self.voice_channel.create_ffmpeg_player(filename,
                                                                  after=self.stop_saytext)
            self.player.volume = self.volume
            self.player.start()

    def stop_saytext(self):
        if self.player:
            if len(self.interrupted) > 0:
                self.player = self.interrupted.pop(len(self.interrupted)-1)
                self.player.resume()

    async def startvote(self, creator, question):
        self.strawpoll = StrawPoll(creator, question, superusers=set(['eternalnoob']))
        await self.saytext('Let\'s Rock the vote!:  ' + question)


    async def whowon(self, user):
        if self.strawpoll is not None and self.strawpoll.canend(user):
            results, winner = self.strawpoll.tally()
            await self.saytext(winner + ' Is the winning option for ' + self.strawpoll.question)
            await self.say(str(results))
            self.strawpoll = None

