#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import random
import sys
from inspect import getmembers
from random import randrange

import markovify
from discord.ext import commands

from ..speakutils.generate_single_speak import GenerateSpeak
from ..speakutils.get_messages import GetMessages
from ..speakutils.GetRandomMember import GetRandomMember
from ..utils.converters import BetterMember


class Randomspeak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_converter = BetterMember()
        self.getMessages = GetMessages()
        self.generateSpeak = GenerateSpeak()
        self.getRandomMember = GetRandomMember()

    @commands.group(invoke_without_command=True, case_insensitive=True, name="rspeak", aliases=["rs"])
    async def rspeak(self, ctx):
        
        userId = await self.getRandomMember.getMemberId(self.bot)
        record = await self.getMessages.getmessages(ctx, self.bot, userId)
        thing = functools.partial(
            self.generateSpeak.sync_speak, ctx, record, userId)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("not enough content")

        await ctx.send(speech)

def setup(bot):
    bot.add_cog(Randomspeak(bot))
