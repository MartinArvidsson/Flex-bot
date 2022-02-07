#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools

from discord.ext import commands

from ..speakutils.GenerateSingleSpeak import GenerateSpeak
from ..speakutils.GetMessages import GetMessages
from ..utils.converters import BetterMember


class Singlespeak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_converter = BetterMember()
        self.getMessages = GetMessages()
        self.generateSpeak = GenerateSpeak()

    @commands.group(invoke_without_command=True, case_insensitive=True, name="speak1", aliases=["s1"])
    async def speak1(self, ctx):
        user = ctx.message.author
        record = await self.getMessages.getmessages(ctx, self.bot, user.id)
        thing = functools.partial(
            self.generateSpeak.sync_speak, ctx, record, user.id)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("not enough content")

        await ctx.send(speech)


def setup(bot):
    bot.add_cog(Singlespeak(bot))
