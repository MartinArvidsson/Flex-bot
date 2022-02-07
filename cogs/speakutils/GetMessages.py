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

# Picks messages from the respective user that's written in the same channel as the command was called.
class GetMessages():
    async def getmessages(self, ctx, bot, userId):
        query = "SELECT content FROM flexbot.messages WHERE author_id=$1 AND guild_id=$2 AND channel_id=$3 ORDER BY random() LIMIT 5000;"
        try:
            record = await bot.pool.fetch(query, userId, ctx.guild.id, 492236781253689348, timeout=5.0)
        except AttributeError:
            return await ctx.send("Something went wrong in the DB query")
        except Exception as e:
            return await ctx.send(e)
        return record
#ctx.message.channel.id        
