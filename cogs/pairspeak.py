#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
from .utils.converters import BetterMember
import discord
import config
import markovify
import functools


class pairspeak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def pairspeak(self, ctx, *args):
        """
        Uses markov chains to come up with fake sentences that almost sound like something you would say, see subredditsimulator for something similar
        Unfortunately requires a fair bit of messages, about 1000 to make bad sentences and 3000 to make non-repetitive from my experience
        """
        member_converter = BetterMember()
        if not args:
             return await ctx.send("behöver minst en person som argument exempel 'Pairspeak Martin' ")
        elif len(args) == 1:
            # If the user only provided one argument, it will be the user to pairspeak with
            user = ctx.author
            try:
                userTwo = await member_converter.convert(ctx, args[0])
            except:
                return await ctx.send("Felstavat argument, skrev du rätt person du ville pairspeaka med?")
            repeats = 5
        
        elif len(args) == 2:
            # I)f the user provided two arguments, build a scentence from both users
            try:
                user = await member_converter.convert(ctx, args[0])
                userTwo = await member_converter.convert(ctx, args[1])
            except:
                return await ctx.send("Felstavat argument, skrev du rätt person du ville pairspeaka med?")
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
                    return await ctx.send("Något gick snett, för många argument?")
                user = await member_converter.convert(ctx, a)

        # user = ctx.message.author if member is None else member
        query = "SELECT content FROM flexbot.messages WHERE author_id=$1 AND guild_id=$2 AND channel_id =$3 ORDER BY timestamp DESC LIMIT 20000;"
        try:
            firstRecord = await self.bot.pool.fetch(query, user.id, ctx.guild.id, ctx.message.channel.id, timeout=5.0)
            secondRecord = await self.bot.pool.fetch(query, user.id, ctx.guild.id, ctx.message.channel.id, timeout=5.0)
        except AttributeError:
            return await ctx.send("Något gick fel i queryn..")
        except Exception:
            return await ctx.send("Timade ut, databasproblem?")
        thing = functools.partial(self.sync_speak, firstRecord, secondRecord, user, userTwo, repeats)
        speech = await self.bot.loop.run_in_executor(None, thing)
        if speech == -1:
            return await ctx.send("Skriv lite mer, för lite text att bygga meningar av")

        await ctx.send(speech)

    def sync_speak(self, firstRecord, secondRecord, user, userTwo, repeats):
        firstText = '\n'.join([x[0] for x in firstRecord if len(x[0]) > 20])
        secondText = '\n'.join([x[0] for x in secondRecord if len(x[0]) > 20])
        try:
            text_model_one = markovify.NewlineText(firstText)
            text_model_two = markovify.NewlineText(secondText)
            combined_models = markovify.combine([text_model_one,text_model_two])
        except Exception as e:
            print(e)
            return -1
        speech = "**{} & {}:**\n".format(user.name, userTwo.name)
        repeats = min(repeats, 20)
        for _ in range(repeats):
            try:
                variablename = combined_models.make_short_sentence(
                    140, state_size=2)
                speech += "{}\n\n".format(variablename)
            except:
                continue
        return speech


def setup(bot):
    bot.add_cog(pairspeak(bot))
