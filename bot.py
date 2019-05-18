#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
from datetime import datetime
import discord
import config
import markovify
import functools
import asyncpg
import asyncio


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), **kwargs)
        for cog in config.cogs:
            try:
                print(cog)
                self.load_extension(cog)
            except Exception as exc:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(
                    cog, exc))

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))
        if config.now_playing:
            print("setting NP game", flush=True)
            activity = discord.Game(name=config.now_playing)
            await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_message(self, message):
        if(message.author.bot != True and not message.content.startswith(("!", "&", "https://"))):
            await self.pool.execute('INSERT INTO flexbot.messages VALUES($1, $2, $3, $4, $5, $6) ',
                                    message.created_at,
                                    message.content,
                                    message.id,
                                    message.author.id,
                                    message.channel.id,
                                    message.guild.id)
        await bot.process_commands(message)


bot = Bot()

# write general commands here
@bot.command()
async def ping(ctx):
    await ctx.send('pong :)')


@bot.command()
async def getchannelhistory(ctx):
    channel = ctx.message.channel
    async for ctx.message in channel.history(limit=50000):
        if(ctx.message.author.bot != True and not ctx.message.content.startswith(("!", "&", "https://"))):
            await bot.pool.execute('INSERT INTO flexbot.messages VALUES($1, $2, $3, $4, $5, $6) ',
                                   ctx.message.created_at,
                                   ctx.message.content,
                                   ctx.message.id,
                                   ctx.message.author.id,
                                   ctx.message.channel.id,
                                   ctx.message.guild.id)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(asyncpg.create_pool(
        f"postgresql://{config.db_user}:{config.db_password}@127.0.0.1:5432/flexbot", command_timeout=60, min_size=4, max_size=10))
    bot.pool = pool

bot.run(config.token)
