import googletrans
from discord.ext import commands
import discord
from typing import List, Tuple, NamedTuple, AnyStr

trans = googletrans.Translator(service_urls=['translate.google.com'])
class Transform(NamedTuple):
    """Represents an employee."""
    from_lang: str = 'auto'
    to_lang: str = 'en'

    def __repr__(self) -> str:
        return f'<Transform From:{self.from_lang}, To={self.to_lang}>'


def translate_chain(transforms: List[Transform], input):
    temp = input
    for transform in transforms:
        temp = trans.translate(temp, transform.to_lang, transform.from_lang).text
    return temp


def transforms_from_string(text: str) -> (List[Transform], str):
    pop = {']': '['}
    if text[0] != '[':
        raise Exception("Must be `[`")

    transforms = []

    stack = []

    src = ""
    dest = ""
    stack.append('[')
    insrc = True
    i = 0
    for char in text[1:]:
        i += 1
        if char == "[":
            stack.append('[')
        elif char == "]":
            assert stack.pop() == pop[char]
            if src != "" and dest != "":
                assert src in googletrans.LANGUAGES, 'src %s not present in languages' % src
                assert dest in googletrans.LANGUAGES, 'dest %s not present in languages' % dest
                transforms.append(Transform(src, dest))
                src = ""
                dest = ""
            insrc = not insrc
        elif char == ' ':
            continue
        elif char == ',':
            insrc = not insrc
        else:
            if insrc:
                src += char
            else:
                dest += char

        if len(stack) == 0:
            i += 1
            return transforms, text[i:]
    return transforms, text[i:]

class Translator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def langhelp(self, ctx: discord.ext.commands.Context):
        await ctx.send("{}".format(googletrans.LANGUAGES))

    @commands.command()
    async def translatecomp(self, ctx: discord.ext.commands.Context):
        transforms, result = transforms_from_string(' '.join(ctx.message.content.split(' ')[1:]))
        x = translate_chain(transforms, result)
        await ctx.send(translate_chain(transforms, x))

