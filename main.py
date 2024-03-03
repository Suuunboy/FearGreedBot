import typing
import discord
from discord.ext import commands
from feargreed_scraper import scrap
import functools
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

FG_CHANNELS = []


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    func = functools.partial(blocking_func, *args,
                             **kwargs)  # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)


@client.event
async def on_ready():
    print('Ready!')
    print('------------------')


async def sender(embed, channels):
    for item in channels:
        chanel = client.get_channel(item)
        await chanel.send(embed=embed)
        print('sent')


@tasks.loop(minutes=30)
async def send_news():
    print('start sending...')
    res = int(await run_blocking(scrap))
    if res >= 70:
        emb = discord.Embed(title='Warning: greed on market!', colour=0x00ff1e)
        emb.add_field(name="Index:", value=res, inline=True)
        await sender(emb, FG_CHANNELS)
    elif res <= 30:
        emb = discord.Embed(title='Warning: fear on market!', colour=0xff0000)
        emb.add_field(name="Index:", value=res, inline=True)
        await sender(emb, FG_CHANNELS)
    print('done!')


@commands.has_permissions(administrator=True)
@client.command()
async def startFG(ctx):
    fg_channel = ctx.channel.id
    print(fg_channel)
    global FG_CHANNELS
    if FG_CHANNELS and fg_channel not in FG_CHANNELS:
        FG_CHANNELS.append(fg_channel)
        print('Started', fg_channel)
        chanel = client.get_channel(fg_channel)
        await chanel.send('Started!')
    elif not FG_CHANNELS:
        FG_CHANNELS.append(fg_channel)
        send_news.start()
        print('Started first', fg_channel)
        chanel = client.get_channel(fg_channel)
        await chanel.send('Started!')
    else:
        chanel = client.get_channel(fg_channel)
        await chanel.send('Bot is already running here')


@commands.has_permissions(administrator=True)
@client.command()
async def stopFG(ctx):
    fg_channel = ctx.channel.id
    global FG_CHANNELS
    if fg_channel in FG_CHANNELS:
        FG_CHANNELS.remove(fg_channel)
        print('Stopped', fg_channel)
        if len(FG_CHANNELS) == 0:
            send_news.cancel()
            print('Stopped all')
        chanel = client.get_channel(fg_channel)
        await chanel.send('Stopped!')
    else:
        chanel = client.get_channel(fg_channel)
        await chanel.send('Bot has already been stopped here')


@commands.has_permissions(administrator=True)
@client.command()
async def infFG(ctx):
    await ctx.send('!startFG - start bot, users will be notified abot fear or greed')
    await ctx.send('!stopFG - stop bot')


with open('token', 'r') as file:
    token = file.read()
client.run(token)
