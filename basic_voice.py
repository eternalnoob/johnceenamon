import asyncio
import json

import discord
import youtube_dl
import random

from discord.ext import commands
from johnceenabot.settings import Config
from johnceenabot.utils import bot
import translations
from translations import transforms_from_string, translate_chain
import markovify
import os.path

from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

ROOT_PATH=os.path.dirname(os.path.abspath(__file__))+'/'

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
The spaghetti's run out, time'sy up, over - blaow!
Snap back to spaghetti, oh! - there goes gravity""",
    """
  There was one who said unto me that the universe was going to cause me to tremble,
That I am not the sharpest cutting implement in the storehouse.
She had the appearance unto me as a stupid one,
With her finger and her thumb
In the frame of a Greek gamma upon her forehead.
Behold, the years begin coming, and do not cease from coming.
Fed unto the axioms, and I fell upon the earth and ran.
It was not acceptable if not to live for the sake of pleasurable things.
Your brain increases its wisdom, but your heart increases its stupidity.
A great amount to do, a great amount to see,
Therefore, there is no difficult problem if we take the streets of the backside.
You will not know if you do not go.
You will not shine if you do not glow.
Behold currently! You are entirely a star child! Begin your power! Go! Laugh!
Behold currently! You are a master of the music! Begin your singing! Acquire your wages!
All that sparkles is gold!
Comets alone shatter the frame!  """,
"""You cheated not only the game, but yourself. You didn't grow.
You didn't improve. You took a shortcut and gained nothing.
You experienced a hollow victory. Nothing was risked and nothing was gained.
It's sad you don't know the difference."""

]


description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

valid_lang = {}
with open('languages.json', 'r') as fin:
    valid_lang = json.load(fin)



ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}


with open('chains/munroe_chains.json', mode='r') as f:
    contents = f.read()
    markov = markovify.Text.from_json(contents)

with open('chains/chain_jerry.json', mode='r') as f:
    contents = f.read()
    jerry = markovify.Text.from_json(contents)

with open('chains/horror_chains.json', mode='r') as f:
    contents = f.read()
    horror_markov = markovify.Text.from_json(contents)

with open('chains/seinfeldia.json', mode='r') as f:
    contents = f.read()
    ree_bees = markovify.Text.from_json(contents)

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):

    SUPPORTED_GNDS = {
        'neutral': texttospeech.enums.SsmlVoiceGender.NEUTRAL,
        'female': texttospeech.enums.SsmlVoiceGender.FEMALE,
        'male': texttospeech.enums.SsmlVoiceGender.MALE,
    }
    def __init__(self, bot):
        self.bot = bot
        self.gnd = self.SUPPORTED_GNDS['neutral']
        self.lang_code = 'en-us'

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    async def play_help(self, ctx, query):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    async def mp3_pipe(self, ctx, content):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(content))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    async def saytext(self, ctx, text, lang=None, gnd=None):
        if not lang:
            lang = self.lang_code
        if not gnd:
            gnd = self.gnd

        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        voice = texttospeech.types.VoiceSelectionParams(
            language_code=lang,
            ssml_gender=gnd,
        )

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        fname = ROOT_PATH+'mp3/'+'out.mp3'
        file = open(fname, mode='wb')
        file.write(response.audio_content)
        await self.mp3_pipe(ctx, fname)

    @commands.command()
    async def changelang(self, ctx, lang: str):
        self.lang_code = lang

    @commands.command()
    async def changevoicegnd(self, ctx, gnd: str):
        assert gnd in self.SUPPORTED_GNDS

        self.gnd = self.SUPPORTED_GNDS[gnd]

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        await self.play_help(ctx, query)

    @commands.command()
    async def cena(self, ctx):
        """:trumpet::trumpet::trumpet::trumpet:"""
        await self.play_help(ctx, ROOT_PATH+'johnceenabot/audio/invisible.mp3')
        await ctx.send(":trumpet::trumpet::trumpet:")

    @commands.command()
    async def nash(self, ctx):
        await self.play_help(ctx, ROOT_PATH+"johnceenabot/audio/vape-nation.mp3")

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def pause(self, ctx:discord.ext.commands.Context):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.pause()

    @commands.command()
    async def stop(self, ctx:discord.ext.commands.Context):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.stop()

    @commands.command()
    async def desummon(self, ctx:discord.ext.commands.Context):
        """
        Stops and disconnects the bot from voice

        :param ctx:
        :return:
        """
        await ctx.voice_client.disconnect()

    """

    BEGIN TEXT STUFF
    """

    @commands.command()
    async def greyfacefromspace(self, ctx):
        sentence = horror_markov.make_sentence()
        await self.saytext(ctx, sentence)

    @commands.command()
    async def tellmeastory(self, ctx):

        try:
            sentence = horror_markov.make_sentence_with_start(' '.join(ctx.message.content.split(' ')[1:]))
            await self.saytext(ctx, sentence)
        except:
            await bot.say("lol I can't tho")

    @commands.command()
    async def noneroe(self, ctx):
        sentence = markov.make_sentence()
        await self.saytext(ctx, sentence)

    @commands.command()
    async def datbee(self, ctx):
        sentence = ree_bees.make_sentence()

    @commands.command()
    async def datbeestory(self, ctx):
        sentence = ree_bees.make_sentence_with_start(' '.join(ctx.message.clean_content.split(' ')[1:]),
                                                     tries=1000,test_output=False)
        print(sentence)
        await self.sayitall(ctx, sentence)

    @commands.command()
    async def standup(self, ctx):
        msg = ctx.message.clean_content.split(' ')
        sentence = jerry.make_short_sentence(int(msg[2]), int(msg[1]), tries=100, test_output=False)
        await self.sayitall(ctx, sentence)

    @commands.command()
    async def jerry(self, ctx):
        sentence = jerry.make_sentence_with_start(' '.join(ctx.message.clean_content.split(' ')[1:]),
                                                  test_output=False,
                                                  tries=1000)
        await self.sayitall(ctx, sentence)

    @commands.command()
    async def talkback(self,ctx):
        sentence = ' '.join(ctx.message.clean_content.split(' ')[1:])
        await self.saytext(ctx, sentence)

    @commands.command()
    async def language(self, ctx):
        msg = ctx.message.clean_content.split(' ')
        lang = msg[1]
        sentence = ' '.join(msg[2:])
        await self.saytext(ctx, sentence, lang=lang)

    @commands.command()
    async def summon(self, ctx: discord.ext.commands.context):
        chan = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(chan)

        await chan.connect()

    @commands.command()
    async def seinfeld(self, ctx: discord.ext.commands.context):
        msg = ctx.message.content.split(' ')
        try:
            char = msg[1]
            count = 1
            if len(msg) >= 3:
                count = int(msg[2])
            with open('chains/chain_%s.json' % char, mode='r') as f:
                contents = f.read()
                temp_markov = markovify.Text.from_json(contents)
                content = ""
                print(count)
                for _ in range(count):
                    try:
                        content += temp_markov.make_sentence()+'\n'
                    except:
                        pass
                await self.sayitall(ctx, content)
        except FileNotFoundError:
            await ctx.send("that character was not found")
            await ctx.send('use a different character')

    @commands.command()
    async def shittymemes(self, ctx):
        sentence = random.choice(shitty_memes)
        await self.saytext(ctx, sentence)

    async def sayitall(self, ctx, sentence):
        await self.saytext(ctx, sentence)
        await ctx.send(sentence)

    @commands.command()
    async def ttslang(self, ctx):
        await ctx.send("supported languages\n{}".format(valid_lang))

    @commands.command()
    async def speakilate(self, ctx):
        transforms, result = transforms_from_string(' '.join(ctx.message.content.split(' ')[1:]))
        x = translate_chain(transforms, result)
        final = transforms[-1].to_lang
        if final not in valid_lang:
            await ctx.send("language unsupported, results shoddy, see ?ttslang")

        await ctx.send(x)
        await self.saytext(ctx, x, lang=final)

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.resume()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    @noneroe.before_invoke
    @seinfeld.before_invoke
    @speakilate.before_invoke
    @jerry.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(Music(bot))
bot.add_cog(translations.Translator(bot))
bot.run(Config.BOT_USER_TOKEN)
