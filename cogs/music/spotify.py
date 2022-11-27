#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools

from discord.ext import commands

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def splay(self, ctx):
        return await "hi"

def setup(bot):
    bot.add_cog(Spotify(bot))