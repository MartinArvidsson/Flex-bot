#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..speakutils.GetMessages import GetMessages
from ..speakutils.GeneratePairspeak import GeneratePairspeak
import markovify
import config
from random import randrange
from inspect import getmembers
import functools
import discord
from discord.ext import commands

from ..utils.converters import BetterMember

intents = discord.Intents.default()
intents.members = True


class Pairspeak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_converter = BetterMember()
        self.getMessages = GetMessages()
        self.GeneratePairspeak = GeneratePairspeak()

    @commands.group(invoke_without_command=True, case_insensitive=True, name="pairspeak", aliases=["ps"])
    async def pairspeak(self, ctx, *args):

        member_converter = BetterMember()
        if not args:
            return await ctx.send("need a second arg for pairspeak")
        elif len(args) == 1:
            # If the user only provided one argument, it will be the user to pairspeak with
            user = ctx.author
            try:
                userTwo = await member_converter.convert(ctx, args[0])
            except:
                return await ctx.send("no person with that name, did you write it correctly?")
            repeats = 5

        elif len(args) == 2:
            # If the user provided two arguments, build a scentence from both users
            try:
                user = await member_converter.convert(ctx, args[0])
                userTwo = await member_converter.convert(ctx, args[1])
            except:
                return await ctx.send("no person with that name, did you write it correctly?")
            repeats = 5
        else:
            a, b, *_ = args
            if a.isdigit() and int(a) < 1000:
                # A is probably repeats
                repeats = int(a)
                user = await member_converter.convert(ctx, b)
            else:
                try:
                    repeats = int(b)
                except ValueError:
                    return await ctx.send("too many arguments?")
                user = await member_converter.convert(ctx, a)

        firstRecord = await self.getMessages.getmessages(ctx, self.bot, user.id)

        secondRecord = await self.getMessages.getmessages(ctx, self.bot, userTwo.id)

        thing = functools.partial(self.GeneratePairspeak.sync_speak,
                                  ctx, firstRecord, secondRecord, user.id, userTwo.id, repeats)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("not enough content")

        await ctx.send(speech)


def setup(bot):
    bot.add_cog(Pairspeak(bot))
