#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inspect import getmembers
from discord.ext import commands
from random import randrange
import discord
import config
import markovify
import functools
intents = discord.Intents.default()

# Uses the Messages gathered from GetMessages to generate a random sentence


class GeneratePairspeak():
    def sync_speak(self, ctx, firstRecord, secondRecord, userId, UserTwoId, repeats):
        firstText = '\n'.join([x[0] for x in firstRecord if len(x[0]) > 100])
        secondText = '\n'.join([x[0] for x in secondRecord if len(x[0]) > 100])
        try:
            text_model_one = markovify.NewlineText(firstText, state_size=2)
            text_model_two = markovify.NewlineText(secondText, state_size=2)
            combined_models = markovify.combine([text_model_one,text_model_two])
        except Exception as e:
            print(e)
            return -1
        speech = "**{} & {}:**\n".format(ctx.guild.get_member(userId).nick, ctx.guild.get_member(UserTwoId).nick)
        repeats = min(repeats, 20)
        for _ in range(repeats):
            try:
                variablename = combined_models.make_short_sentence(randrange(60,130),tries=50)
                speech += "{}\n\n".format(variablename)
            except:
                continue
        return speech
