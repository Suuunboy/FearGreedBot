import re
import typing
import discord
from discord.ext import commands
import asyncio
from feargreed_scraper import scrap
import functools
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import asyncio
from discord.ext import tasks

fmt = "%H:%M"
fmt2 = "%m-%d"

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

# CN_CHANNEL = 1141286627117899916
# LOG_CHANNEL = 1161018317025329204

CN_CHANNEL = 1152910423134306304
LOG_CHANNEL = 1152910423134306304


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    func = functools.partial(blocking_func, *args,
                             **kwargs)  # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)


@client.event
async def on_ready():
    print('Ready!')
    print('------------------')


@tasks.loop(minutes=20)
async def send_news():
    print('started')
    res = int(await run_blocking(scrap))
    chanel = client.get_channel(CN_CHANNEL)
    if res >= 70:
        emb = discord.Embed(title='Warning: greed on market!', colour=0x00ff1e)
        emb.add_field(name="Index:", value=res, inline=True)
        await chanel.send(embed=emb)
    elif res <= 30:
        emb = discord.Embed(title='Warning: fear on market!', colour=0xff0000)
        emb.add_field(name="Index:", value=res, inline=True)
        await chanel.send(embed=emb)
    print('done!')


@commands.has_permissions(administrator=True)
@client.command()
async def startFG(ctx):
    if ctx.channel.id != CN_CHANNEL:
        return
    chanel = client.get_channel(LOG_CHANNEL)
    await chanel.send('Started!')
    send_news.start()


@commands.has_permissions(administrator=True)
@client.command()
async def stopFG(ctx):
    if ctx.channel.id != CN_CHANNEL:
        return
    print('Stopped')
    chanel = client.get_channel(LOG_CHANNEL)
    await chanel.send('Stopped!')
    send_news.stop()


@commands.has_permissions(administrator=True)
@client.command()
async def infFG(ctx):
    if ctx.channel.id != CN_CHANNEL:
        return
    await ctx.send('!start - start bot, users will be notified abot fear or greed')
    await ctx.send('!stop - stop bot')

client.run('MTE2NjMxMDQyNDQ4NTA0NDIyNA.Gb5WL2.3SJY12CianRVpjYf0w0gODmStp1Lv7Zj6mPj6k')
