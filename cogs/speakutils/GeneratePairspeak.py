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
        #Use nickname if possible, otherwise use username
        usernameOne = ''
        usernameTwo = ''
        if not ctx.guild.get_member(userId).nick.__eq__('None'):
            usernameOne = ctx.guild.get_member(userId).nick
        else:
            usernameOne = ctx.guild.get_member(userId).name

        if not ctx.guild.get_member(UserTwoId).nick.__eq__('None'):
            usernameTwo = ctx.guild.get_member(UserTwoId).nick
        else:
            usernameTwo = ctx.guild.get_member(UserTwoId).name

        #Generate textmodels for each user
        firstText = '\n'.join([x[0] for x in firstRecord if len(x[0]) > 20])
        secondText = '\n'.join([x[0] for x in secondRecord if len(x[0]) > 20])
        
        #Combine the two models according to markovify 
        try:
            text_model_one = markovify.NewlineText(firstText, state_size=2)
            text_model_two = markovify.NewlineText(secondText, state_size=2)
            combined_models = markovify.combine([text_model_one,text_model_two])
        except Exception as e:
            print(e)
            return -1
        
        #Print sentences from the combined textmodels https://github.com/jsvine/markovify#combining-models
        speech = "**{} & {}:**\n".format(usernameOne, usernameTwo)
        repeats = min(repeats, 20)
        for _ in range(repeats):
            try:
                variablename = combined_models.make_sentence(tries=100)
                speech += "{}\n\n".format(variablename)
            except:
                continue
        return speech
