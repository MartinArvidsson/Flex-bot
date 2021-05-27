#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
from inspect import getmembers
from random import randrange

import config
import discord
import markovify
from discord.ext import commands

from ..speakutils.GetMessages import GetMessages
from ..speakutils.GenerateSpeak import GenerateSpeak
from ..utils.converters import BetterMember


class speak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_converter = BetterMember()
        self.getMessages = GetMessages()
        self.generateSpeak = GenerateSpeak()

    @commands.group(invoke_without_command=True, case_insensitive=True, name="speak", aliases=["sp"])
    async def speak(self, ctx, *args):
        """
        Uses markov chains to come up with fake sentences that almost sound like something you would say, see subredditsimulator for something similar
        Unfortunately requires a fair bit of messages, about 1000 to make bad sentences and 3000 to make non-repetitive from my experience
        """
        if not args:
            user = ctx.message.author
            repeats = 5
        elif len(args) == 1:
            # If the user only provided one argument, we need to check if
            # The argument is repeats or a member to generate sentences from
            if args[0].isdigit() and int(args[0]) < 1000:
                user = ctx.author
                repeats = int(args[0])
            else:
                user = await self.member_converter.convert(ctx, args[0])
                repeats = 5
        else:
            a, b, *_ = args
            if a.isdigit() and int(a) < 1000:
                # A is probably repeats
                repeats = int(a)
                user = await self.member_converter.convert(ctx, b)
            else:
                try:
                    repeats = int(b)
                except ValueError:
                    return await ctx.send("Not sure what to make of what you said, please supply a member and or number of repeats (or nothing).")
                user = await self.member_converter.convert(ctx, a)

        
        record = await self.getMessages.getmessages(ctx, self.bot, user.id)
        thing = functools.partial(self.generateSpeak.sync_speak, record, user, repeats)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("not enough content")
        


        await ctx.send(speech)

    # def sync_speak(self, record, user, repeats):
    #     text = '\n'.join([x[0] for x in record if len(x[0]) > 100])
    #     try:
    #         text_model = markovify.NewlineText(text, state_size=2)
    #     except Exception as e:
    #         return e
    #     speech = "**{}:**\n".format(user.name)
    #     repeats = min(repeats, 20)
    #     for _ in range(repeats):
    #         try:
    #             variablename = text_model.make_short_sentence(randrange(60,130),tries=50)
    #             speech += "{}\n\n".format(variablename)
    #         except:
    #             continue
    #     return speech


def setup(bot):
    bot.add_cog(speak(bot))

