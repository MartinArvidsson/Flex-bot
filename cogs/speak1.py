#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
from .utils.converters import BetterMember
from random import randrange
import discord
intents = discord.Intents.default()
intents.members = True
import config
import markovify
import functools


class speak1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, name="speak1", aliases=["s1"])
    async def speak1(self, ctx):
        """
        Uses markov chains to come up with fake sentences that almost sound like something you would say, see subredditsimulator for something similar
        Unfortunately requires a fair bit of messages, about 1000 to make bad sentences and 3000 to make non-repetitive from my experience
        """
        user = ctx.message.author

        # user = ctx.message.author if member is None else member
        query = "SELECT content FROM flexbot.messages WHERE author_id=$1 AND guild_id=$2 AND channel_id=$3 ORDER BY random() LIMIT 20000;"
        try:
            record = await self.bot.pool.fetch(query, user.id, ctx.guild.id, ctx.message.channel.id, timeout=5.0)
        except AttributeError:
            return await ctx.send("Something went wrong in the DB query")
        except Exception:
            return await ctx.send("Timed out, DB error most likely")
        thing = functools.partial(self.sync_speak, record, user)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("not enough content")

        await ctx.send(speech)

    def sync_speak(self, record, user):
        text = '\n'.join([x[0] for x in record if len(x[0]) > 100])
        try:
            text_model = markovify.NewlineText(text, state_size=2)
        except Exception as e:
            return -1
        speech = "**{}:**\n".format(user.nick)
        variablename = text_model.make_short_sentence(randrange(60,130),tries=50)
        speech += "{}\n\n".format(variablename)
        return speech


def setup(bot):
    bot.add_cog(speak1(bot))

