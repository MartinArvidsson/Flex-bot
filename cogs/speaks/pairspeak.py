#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
from ..utils.converters import BetterMember
from random import randrange
import discord
intents = discord.Intents.default()
intents.members = True
import config
import markovify
import functools


class pairspeak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, name="pairspeak", aliases=["ps"])
    async def pairspeak(self, ctx, *args):
        """
        Uses markov chains to come up with fake sentences that almost sound like something you would say, see subredditsimulator for something similar
        Unfortunately requires a fair bit of messages, about 1000 to make bad sentences and 3000 to make non-repetitive from my experience
        """
        member_converter = BetterMember()
        if not args:
             return await ctx.send("need a second arg for pairspeak")
        elif len(args) == 1:
            # If the user only provided one argument, it will be the user to pairspeak with
            user = ctx.author
            try:
                userTwo = await member_converter.convert(ctx, args[0])
            except:
                return await ctx.send("no person with that name, did you write it correctly?")
            repeats = 5
        
        elif len(args) == 2:
            # If the user provided two arguments, build a scentence from both users
            try:
                user = await member_converter.convert(ctx, args[0])
                userTwo = await member_converter.convert(ctx, args[1])
            except:
                return await ctx.send("no person with that name, did you write it correctly?")
            repeats = 5
        else:
            a, b, *_ = args
            if a.isdigit() and int(a) < 1000:
                # A is probably repeats
                repeats = int(a)
                user = await member_converter.convert(ctx, b)
            else:
                try:
                    repeats = int(b)
                except ValueError:
                    return await ctx.send("too many arguments?")
                user = await member_converter.convert(ctx, a)

        # user = ctx.message.author if member is None else member
        query = "SELECT content FROM flexbot.messages WHERE author_id=$1 AND guild_id=$2 AND channel_id =$3 ORDER BY random() LIMIT 20000;"
        try:
            firstRecord = await self.bot.pool.fetch(query, user.id, ctx.guild.id, ctx.message.channel.id, timeout=5.0)
            secondRecord = await self.bot.pool.fetch(query, userTwo.id, ctx.guild.id, ctx.message.channel.id, timeout=5.0)
        except AttributeError:
            return await ctx.send("Something went wrong in the DB query")
        except Exception:
            return await ctx.send("Timed out, DB error most likely")
        thing = functools.partial(self.sync_speak, firstRecord, secondRecord, user, userTwo, repeats)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("not enough content")

        await ctx.send(speech)

    def sync_speak(self, firstRecord, secondRecord, user, userTwo, repeats):
        firstText = '\n'.join([x[0] for x in firstRecord if len(x[0]) > 100])
        secondText = '\n'.join([x[0] for x in secondRecord if len(x[0]) > 100])
        try:
            text_model_one = markovify.NewlineText(firstText, state_size=2)
            text_model_two = markovify.NewlineText(secondText, state_size=2)
            combined_models = markovify.combine([text_model_one,text_model_two])
        except Exception as e:
            print(e)
            return -1
        speech = "**{} & {}:**\n".format(user.nick, userTwo.nick)
        repeats = min(repeats, 20)
        for _ in range(repeats):
            try:
                variablename = combined_models.make_short_sentence(randrange(60,130),tries=50)
                speech += "{}\n\n".format(variablename)
            except:
                continue
        return speech


def setup(bot):
    bot.add_cog(pairspeak(bot))
