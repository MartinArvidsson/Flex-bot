#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import config

class BetterMember(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument as e:
            maybe_name = discord.utils.find(lambda x: x.name.lower() == argument.lower(), ctx.guild.members)
            if maybe_name is None:
                maybe_name = discord.utils.find(lambda x: x.display_name.lower() == argument.lower(), ctx.guild.members)
            if maybe_name:
                return maybe_name
            raise e