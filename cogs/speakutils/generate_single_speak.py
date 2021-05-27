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


class GenerateSpeak():
    def sync_speak(self, ctx, record, userId, repeats=None):
        text = '\n'.join([x[0] for x in record if len(x[0]) > 100])
        try:
            text_model = markovify.NewlineText(text, state_size=2)
        except Exception as e:
            return e
        speech = "**{}:**\n".format(ctx.guild.get_member(userId).nick)
        if repeats is None:
            try:
                text_model = markovify.NewlineText(text, state_size=2)
            except Exception as e:
                return e
        else:
            repeats = min(repeats, 20)

        if repeats is None:
            try:
                variablename = text_model.make_short_sentence(
                    randrange(60, 130), tries=50)
                speech += "{}\n\n".format(variablename)
            except Exception as e:
                return e
        else:
            for _ in range(repeats):
                try:
                    variablename = text_model.make_short_sentence(
                        randrange(60, 130), tries=50)
                    speech += "{}\n\n".format(variablename)
                except:
                    continue
        return speech
