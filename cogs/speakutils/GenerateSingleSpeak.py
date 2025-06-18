#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inspect import getmembers
from discord.ext import commands
from random import randrange
import discord
import config
import markovify
intents = discord.Intents.default()
# Uses the Messages gathered from GetMessages to generate a random sentence


class GenerateSpeak():
    def sync_speak(self, ctx, record, userId, repeats=None):
        #Use nickname if possible else use username
        if not ctx.guild.get_member(userId).nick.__eq__('None'):
            username = ctx.guild.get_member(userId).nick
        else:
            username = ctx.guild.get_member(userId).name
        speech = "**{}:**\n".format(username)

        #Generate text model
        text = '\n'.join([x[0] for x in record if len(x[0]) > 20])
        try:
            text_model = markovify.NewlineText(text,config.statesize)
        except Exception as e:
            return e

        #Generate sentences from model depending on how many repeats was provided
        if repeats is None:
            try:
                variablename = text_model.make_sentence(tries=100)
                speech += "{}\n\n".format(variablename)
            except Exception as e:
                return e
        else:
            for _ in range(repeats):
                try:
                    variablename = text_model.make_sentence(tries=100)
                    speech += "{}\n\n".format(variablename)
                except:
                    continue
        return speech
