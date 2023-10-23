import re
import typing
import discord
from discord.ext import commands
import asyncio
from cryptocurrency_scraper import scrap
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

CN_CHANNEL = 1141286627117899916
LOG_CHANNEL = 1161018317025329204


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    func = functools.partial(blocking_func, *args,
                             **kwargs)  # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)


@client.event
async def on_ready():
    print('Ready!')
    print('------------------')


@tasks.loop(hours=1)
async def send_news():
    print('started')

    print('done!')


@commands.has_permissions(administrator=True)
@client.command()
async def startfg(ctx):
    if ctx.channel.id != CN_CHANNEL:
        return
    chanel = client.get_channel(LOG_CHANNEL)
    await chanel.send('Started!')
    send_news.start()


@commands.has_permissions(administrator=True)
@client.command()
async def stopfg(ctx):
    if ctx.channel.id != CN_CHANNEL:
        return
    print('Stopped')
    chanel = client.get_channel(LOG_CHANNEL)
    await chanel.send('Stopped!')
    send_news.stop()


@commands.has_permissions(administrator=True)
@client.command()
async def inffg(ctx):
    if ctx.channel.id != CN_CHANNEL:
        return
    await ctx.send('!start - start bot, users will be notified abot fear or greed')
    await ctx.send('!stop - stop bot')

client.run('')
