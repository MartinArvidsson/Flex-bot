#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import config

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), **kwargs)
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(cog, exc))

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))
        if config.now_playing:
            print("setting NP game", flush=True)
            activity = discord.Game(name=config.now_playing)
            await self.change_presence(status=discord.Status.idle, activity=activity)


bot = Bot()

# write general commands here
@bot.command()
async def ping(ctx):
    await ctx.send('pong :)')



bot.run(config.token)
