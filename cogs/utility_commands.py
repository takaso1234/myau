# -*- coding: utf-8 -*-
"""
Utility commands for the Discord bot.
"""
import discord
from discord.ext import commands
import logging
import time
import datetime
import pytz
import asyncio

logger = logging.getLogger('discord_bot')

class UtilityCommands(commands.Cog):
    """Utility commands for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.japan_tz = pytz.timezone('Asia/Tokyo')
        # Flag to track if the status update task is running
        self.status_updating = False
        # Start the background task for updating status with current time
        self.start_status_task()
        
    def cog_unload(self):
        """Cleanup when cog is unloaded."""
        self.status_updating = False
        if hasattr(self, 'status_task') and not self.status_task.done():
            self.status_task.cancel()
            
    def start_status_task(self):
        """Create and start the status update task."""
        if not self.status_updating:
            self.status_updating = True
            # Create a new task for updating status
            self.status_task = self.bot.loop.create_task(self.update_status())
            logger.info("Started status update task")
        
    async def update_status(self):
        """Update the bot's status with the current time in Japan."""
        await self.bot.wait_until_ready()
        logger.info("Status update task is running")
        
        update_interval = 30  # Update every 30 seconds as requested
        last_minute = -1  # Track last minute to reduce logging
        
        while not self.bot.is_closed() and self.status_updating:
            try:
                # Get the current time in Japan
                now = datetime.datetime.now(self.japan_tz)
                current_minute = now.minute
                
                # Use a simple time format without seconds to avoid rate limits
                time_str = now.strftime('🕒 %H:%M JST')
                
                # Create and set the activity
                activity = discord.Activity(
                    type=discord.ActivityType.watching, 
                    name=time_str
                )
                await self.bot.change_presence(activity=activity)
                
                # Only log when minute changes to reduce console spam
                if current_minute != last_minute:
                    logger.info(f"Updated status to: {time_str}")
                    last_minute = current_minute
                
            except Exception as e:
                logger.error(f"Error updating status: {str(e)}")
            
            # Wait before updating again
            await asyncio.sleep(update_interval)
    
    @commands.command(name='ping', help="ボットの応答時間を確認します。")
    async def ping(self, ctx):
        """Check the bot's latency."""
        # Calculate the time it takes to send a message
        start_time = time.time()
        message = await ctx.send("計測中...")
        end_time = time.time()
        
        # Calculate the latency in milliseconds
        response_time = round((end_time - start_time) * 1000)
        
        # Get the WebSocket latency
        websocket_latency = round(self.bot.latency * 1000)
        
        # Create an embed with the latency information
        embed = discord.Embed(
            title="🏓 Pong!",
            description="ボットの応答時間情報",
            color=0x00ff00
        )
        embed.add_field(name="メッセージ応答時間", value=f"{response_time}ms", inline=True)
        embed.add_field(name="WebSocket接続時間", value=f"{websocket_latency}ms", inline=True)
        
        # Edit the original message with the embed
        await message.edit(content=None, embed=embed)
        
        logger.info(f"Ping command used. Response time: {response_time}ms, WebSocket latency: {websocket_latency}ms")
        
    @commands.command(name='time', aliases=['時間'], help="日本の現在時刻を表示します。")
    async def time_command(self, ctx):
        """Display the current time in Japan."""
        now = datetime.datetime.now(self.japan_tz)
        
        # Format time strings
        date_str = now.strftime('%Y年%m月%d日')
        time_str = now.strftime('%H:%M:%S')
        weekday = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日'][now.weekday()]
        
        # Create an embed with the time information
        embed = discord.Embed(
            title="🗾 日本の現在時刻",
            description=f"日本標準時（JST）",
            color=0x4285F4
        )
        embed.add_field(name="日付", value=f"{date_str} ({weekday})", inline=False)
        embed.add_field(name="時刻", value=f"🕒 {time_str}", inline=False)
        
        # Add footer with timezone information
        embed.set_footer(text="タイムゾーン: Asia/Tokyo (UTC+9)")
        
        await ctx.send(embed=embed)
        logger.info(f"Time command used. Current JST: {now.strftime('%Y-%m-%d %H:%M:%S')}")

async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(UtilityCommands(bot))