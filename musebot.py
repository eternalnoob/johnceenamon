from discord.ext.commands import Bot
import discord.ext.commands

import logging
import asyncio
from gtts import gTTS
from strawpoll import StrawPoll
from discord import Client

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

    async def startvote(self, creator, question):
        self.strawpoll = StrawPoll(creator, question, superusers=set(['eternalnoob']))
        await self.saytext('Let\'s Rock the vote!:  ' + question)


    async def whowon(self, user):
        if self.strawpoll is not None and self.strawpoll.canend(user):
            results, winner = self.strawpoll.tally()
            await self.saytext(winner + ' Is the winning option for ' + self.strawpoll.question)
            await self.say(str(results))
            self.strawpoll = None

