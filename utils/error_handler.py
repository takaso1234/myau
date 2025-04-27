# -*- coding: utf-8 -*-
"""
Error handling utilities for the Discord bot.
"""
import traceback
import sys
import logging
from discord.ext import commands

logger = logging.getLogger('discord_bot')

async def handle_command_error(ctx, error, error_message="エラーが発生しました"):
    """Generic error handler for bot commands."""
    
    # Handle specific error types with custom messages
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("あなたにはこのコマンドを実行する権限がありません！")
        return
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("ボットに必要な権限がありません！サーバーの権限設定を確認してください。")
        return
    elif isinstance(error, commands.CommandNotFound):
        return  # Silently ignore command not found errors
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"引数が不足しています: {str(error)}")
        return
    
    # Generic error handling
    full_error = f"{error_message}: {str(error)}"
    await ctx.send(full_error)
    
    # Log the full traceback
    logger.error(f"Command error in {ctx.command}: {str(error)}")
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stdout)
