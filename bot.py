#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import config
import asyncpg
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True



class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), **kwargs, intents=intents)
        self.pool = None  # Will be set later

    async def setup_hook(self):
        for cog in config.cogs:
            try:
                print(f"Loading {cog}")
                await self.load_extension(cog)
            except Exception as exc:
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')
        if config.now_playing:
            print("Setting NP game", flush=True)
            activity = discord.Game(name=config.now_playing)
            await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_message(self, message):
        if (not message.author.bot and
            "https://" not in message.content and
            not message.content.startswith(("!", "&")) and
            len(message.clean_content) > 60):
            await self.pool.execute(
                'INSERT INTO flexbot.messages VALUES($1, $2, $3, $4, $5, $6)',
                message.created_at,
                message.clean_content,
                message.id,
                message.author.id,
                message.channel.id,
                message.guild.id
            )
        await self.process_commands(message)


bot = Bot()


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
@commands.has_role('memelord')
async def getchannelhistory(ctx):
    #await ctx.send('Fetching channel history...')
    channel = ctx.message.channel
    async for msg in channel.history(limit=600000):
        if (not msg.author.bot and
            not msg.content.startswith(("!", "&", "https://")) and
            len(msg.clean_content) > 5):
            try:
                await bot.pool.execute(
                    'INSERT INTO flexbot.messages VALUES($1, $2, $3, $4, $5, $6) ON CONFLICT DO NOTHING',
                    msg.created_at,
                    msg.clean_content,
                    msg.id,
                    msg.author.id,
                    msg.channel.id,
                    msg.guild.id
                )
            except Exception as e:
                print(f"Error inserting message: {e}")

async def setup_database_connection():
    pool = await asyncpg.create_pool(
        f"postgresql://{config.db_user}:{config.db_password}@127.0.0.1:5432/flexbot",
        command_timeout=60,
        min_size=4,
        max_size=10
    )
    async with pool.acquire() as conn:
        await conn.execute('CREATE EXTENSION IF NOT EXISTS tsm_system_rows')
    return pool


async def main():
    bot.pool = await setup_database_connection()
    await bot.start(config.token)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down cleanly (KeyboardInterrupt).")
    except asyncio.CancelledError:
        print("Shutting down cleanly (CancelledError).")
