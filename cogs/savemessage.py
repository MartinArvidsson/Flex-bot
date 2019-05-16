#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
from .utils.converters import BetterMember
import discord
import config
import functools
import asyncpg
import asyncio

class savemessage(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(savemessage(bot))