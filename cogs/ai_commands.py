# -*- coding: utf-8 -*-
"""
AI-related commands for the Discord bot using Google's Gemini API.
"""
import discord
from discord.ext import commands
import google.generativeai as genai
import traceback
import sys
import logging
from utils.error_handler import handle_command_error
import config

logger = logging.getLogger('discord_bot')

class AICommands(commands.Cog):
    """Commands that interact with AI services."""
    
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
    
    @commands.command(name='gemini', help="Gemini AIを使って質問に答えます。例: !gemini こんにちは")
    async def gemini_chat(self, ctx, *, message):
        """Send a message to Gemini AI and get a response."""
        try:
            # Send typing indicator while processing
            async with ctx.typing():
                # Send message to Gemini API
                response = self.model.generate_content(
                    [
                        {"role": "model", "parts": [config.SYSTEM_PROMPT]},
                        {"role": "user", "parts": [message]}
                    ],
                    generation_config={
                        "max_output_tokens": config.MAX_OUTPUT_TOKENS,
                        "temperature": config.TEMPERATURE
                    }
                )
                
                # Send response to Discord (handle character limit)
                reply = response.text
                if len(reply) > config.MAX_MESSAGE_LENGTH:
                    for i in range(0, len(reply), config.MAX_MESSAGE_LENGTH):
                        await ctx.send(reply[i:i+config.MAX_MESSAGE_LENGTH])
                else:
                    await ctx.send(reply)
        except Exception as e:
            await handle_command_error(ctx, e, "Gemini APIでエラーが発生しました")
    
    @gemini_chat.error
    async def gemini_chat_error(self, ctx, error):
        """Error handler for gemini command."""
        await handle_command_error(ctx, error, "Gemini AIでエラーが発生しました")

async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(AICommands(bot))
