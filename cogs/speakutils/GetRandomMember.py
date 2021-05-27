#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randrange
import random
import discord
intents = discord.Intents.default()


class GetRandomMember():
    async def getMemberId(self,bot):
        userQuery = "select distinct author_id from flexbot.messages"
        try:
            userRecord = await bot.pool.fetch(userQuery, timeout=5.0)
            randomUser = random.choice(userRecord)
            userId = randomUser['author_id']
        except AttributeError:
            return await ctx.send("Something went wrong in the DB query")
        except Exception as e:
            return await ctx.send(print(e))
        return userId
