#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
from .utils.converters import BetterMember
import discord
import config
import markovify
import functools


class speak1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def speak1(self, ctx):
        """
        Uses markov chains to come up with fake sentences that almost sound like something you would say, see subredditsimulator for something similar
        Unfortunately requires a fair bit of messages, about 1000 to make bad sentences and 3000 to make non-repetitive from my experience
        """
        member_converter = BetterMember()
        user = ctx.message.author

        # user = ctx.message.author if member is None else member
        query = "SELECT content FROM flexbot.messages WHERE author_id=$1 AND guild_id=$2 ORDER BY timestamp DESC LIMIT 20000;"
        try:
            record = await self.bot.pool.fetch(query, user.id, ctx.guild.id, timeout=5.0)
        except AttributeError:
            return await ctx.send("Något gick fel i queryn..")
        except Exception:
            return await ctx.send("Timade ut, databasproblem?")
        thing = functools.partial(self.sync_speak, record, user)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("Skriv lite mer, för lite text att bygga meningar av")

        await ctx.send(speech)

    def sync_speak(self, record, user):
        text = '\n'.join([x[0] for x in record if len(x[0]) > 20])
        try:
            text_model = markovify.NewlineText(text)
        except Exception as e:
            return -1
        speech = "**{}:**\n".format(user.name)
        variablename = text_model.make_short_sentence(
            140, state_size=2)
        speech += "{}\n\n".format(variablename)
        return speech


def setup(bot):
    bot.add_cog(speak1(bot))
