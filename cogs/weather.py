#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
from .utils.converters import BetterMember
from pyowm import OWM
import discord
import config
import functools


class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, name="weather", aliases=["temp"])
    async def weather(self, ctx, *args):
        if not args:
            return await ctx.send("please provide a city")
        elif len(args) == 1:
            # Check for a valid city
            if args[0].isalpha():
                city = args[0]

            owm = OWM(config.weathertoken)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(city)
            weather = observation.weather
        await ctx.send(weather.detailed_status)


def setup(bot):
    bot.add_cog(weather(bot))
