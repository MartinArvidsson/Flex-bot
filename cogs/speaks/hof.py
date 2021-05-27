#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import random


class speak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def hof(self, ctx):

        query = "select * from flexbot.messages where channel_id = '492245343430508544' order by timestamp desc"
        try:
            record = await self.bot.pool.fetch(query, timeout=5.0)
        except AttributeError:
            return await ctx.send("Något gick fel i queryn..")
        except Exception:
            return await ctx.send("Timade ut, databasproblem?")
        hofmsg = random.choice(record)
        await ctx.send("\N{TROPHY}***Hall of fame***\N{TROPHY}\n" + hofmsg['content'])

def setup(bot):
    bot.add_cog(speak(bot))
