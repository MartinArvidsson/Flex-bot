#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
from discord.ext import commands

from ..speakutils.GenerateSingleSpeak import GenerateSpeak
from ..speakutils.GetMessages import GetMessages
from ..speakutils.GetRandomMember import GetRandomMember
from ..utils.converters import BetterMember

#Adam den andre, Filip
blacklisted_users = [239052940290162689,109043103238762496]

class Randomspeak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_converter = BetterMember()
        self.getMessages = GetMessages()
        self.generateSpeak = GenerateSpeak()
        self.getRandomMember = GetRandomMember()


    @commands.group(invoke_without_command=True, case_insensitive=True, name="rspeak", aliases=["rs"])
    async def rspeak(self, ctx):
        userId = await self.get_valid_member_id()
        record = await self.getMessages.getmessages(ctx, self.bot, userId)
        thing = functools.partial(
            self.generateSpeak.sync_speak, ctx, record, userId)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("not enough content")

        await ctx.send(speech)

    async def get_valid_member_id(self):
        userId = await self.getRandomMember.getMemberId(self.bot)
        while userId in blacklisted_users:
            userId = await self.getRandomMember.getMemberId(self.bot)
        return userId

async def setup(bot):
    await bot.add_cog(Randomspeak(bot))
