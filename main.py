# -*- coding: utf-8 -*-
"""
Discord bot with Gemini AI integration and moderation capabilities.
This bot provides Japanese language assistance and voice channel management functions.
"""
import discord
from discord.ext import commands
import google.generativeai as genai
import asyncio
import traceback
import sys
import logging
import os
from config import get_api_key, BOT_PREFIX, COMMAND_DESCRIPTIONS
from keepalive import keep_alive

# Setup logging
logger = logging.getLogger('discord_bot')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get API keys
try:
    GEMINI_API_KEY = get_api_key("GEMINI_API_KEY", "Enter Gemini API Key (visible input): ")
    DISCORD_TOKEN = get_api_key("DISCORD_TOKEN", "Enter Discord Bot Token (visible input): ")

    # Configure Gemini API
    genai.configure(api_key=GEMINI_API_KEY)
except ValueError as e:
    logger.error(f"Configuration error: {str(e)}")
    sys.exit(1)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Enable voice state intents for mute
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    """Called when the bot has connected to Discord."""
    logger.info(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='help')
async def custom_help(ctx, command_name=None):
    """Display help information for commands."""
    embed = discord.Embed(
        title="ボットコマンド一覧",
        description="利用可能なコマンドの一覧です。`!<コマンド名>`で実行できます。",
        color=0x3498db
    )
    
    for name, description in COMMAND_DESCRIPTIONS.items():
        embed.add_field(name=f"!{name}", value=description, inline=False)
        
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for command errors."""
    if isinstance(error, commands.CommandNotFound):
        return  # Silently ignore command not found errors
        
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"引数が不足しています: {error.param.name}")
        return
        
    logger.error(f"Command error: {str(error)}")
    await ctx.send(f"エラーが発生しました: {str(error)}")

async def load_extensions():
    """Load all extensions (cogs)."""
    await bot.load_extension("cogs.ai_commands")
    await bot.load_extension("cogs.moderation_commands")
    await bot.load_extension("cogs.utility_commands")
    logger.info("Loaded all extensions")

async def main():
    """Main function to start the bot."""
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

# Run the bot
if __name__ == "__main__":
    try:
        # Start the keep alive web server
        keep_alive()
        print("Keep alive server started!")
        # Then start the bot
        asyncio.run(main())
    except discord.errors.LoginFailure as e:
        print("無効なDiscordトークンです。Developer Portalで新しいトークンを生成してください。")
        logger.error(f"Login failure: {str(e)}")
        traceback.print_exc(file=sys.stdout)
    except Exception as e:
        print("ボットの実行中に予期しないエラーが発生しました:")
        logger.error(f"Unexpected error: {str(e)}")
        traceback.print_exc(file=sys.stdout)
