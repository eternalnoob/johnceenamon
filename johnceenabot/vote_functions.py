from johnceenabot.utils import bot

@bot.command(pass_context=True)
async def startvote(ctx):
    try:
        question = ' '.join(ctx.message.content.split(' ')[1:])
        user = ctx.message.author.name
        await bot.startvote(user, question)
    except:
        await bot.say('not this time')

@bot.command(pass_context=True)
async def votefor(ctx):
    if bot.strawpoll is not None:
        bot.strawpoll.vote(ctx.message.author.name, 'yes')

@bot.command(pass_context=True)
async def voteagainst(ctx):
    if bot.strawpoll is not None:
        bot.strawpoll.vote(ctx.message.author.name, 'no')

@bot.command(pass_context=True)
async def endvote(ctx):
    await bot.whowon(ctx.message.author.name)
