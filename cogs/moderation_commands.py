# -*- coding: utf-8 -*-
"""
Moderation commands for the Discord bot.
"""
import discord
from discord.ext import commands
import traceback
import sys
import logging
from utils.error_handler import handle_command_error
import config

logger = logging.getLogger('discord_bot')

class ModerationCommands(commands.Cog):
    """Commands for server moderation."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='nuke', help="チャンネル内のすべてのメッセージを削除します。管理者権限が必要です。")
    @commands.has_permissions(manage_messages=True)
    async def nuke(self, ctx):
        """Purge all messages in the current channel."""
        try:
            # Check if bot has manage_messages permission
            if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
                await ctx.send("ボットにメッセージ管理権限がありません！")
                return
                
            # Purge all messages in the channel
            deleted = await ctx.channel.purge(limit=None)
            await ctx.send(f"チャンネルをクリアしました！ {len(deleted)} 件のメッセージを削除。")
        except discord.errors.Forbidden:
            await ctx.send("ボットにメッセージを削除する権限がありません！")
        except Exception as e:
            await handle_command_error(ctx, e, "メッセージ削除でエラーが発生しました")
    
    @commands.command(name='言論統制', help="特定のユーザーをボイスチャンネルでミュートします。")
    async def speech_control(self, ctx):
        """Mute a specific user in voice channel."""
        try:
            # Check if bot has mute_members permission
            if not ctx.guild.me.guild_permissions.mute_members:
                await ctx.send("ボットにメンバーをミュートする権限がありません！サーバーの権限設定を確認してください。")
                return
                
            # Find the user by ID
            target_user = ctx.guild.get_member(config.TARGET_USER_ID)
            if not target_user:
                await ctx.send(f"指定されたユーザー（ID: {config.TARGET_USER_ID}）が見つかりません！サーバーに参加しているか確認してください。")
                return
                
            # Check if user is in a voice channel
            if not target_user.voice or not target_user.voice.channel:
                await ctx.send(f"ユーザー {target_user.name} はボイスチャンネルに接続していません！")
                return
                
            # Check role hierarchy
            if ctx.guild.me.top_role <= target_user.top_role:
                await ctx.send(f"ボットのロールが {target_user.name} のロール以下です！ボットのロールを上位に設定してください。")
                return
                
            # Mute the user
            await target_user.edit(mute=True)
            await ctx.send(f"ユーザー {target_user.name} をスピーカーミュートしました！")
        except Exception as e:
            await handle_command_error(ctx, e, "ミュート処理でエラーが発生しました")
    
    @commands.command(name='暑くないわ', help="ボイスチャンネル内のすべてのユーザーをミュートします。管理者権限が必要です。")
    @commands.has_permissions(administrator=True)
    async def mute_all(self, ctx):
        """Mute all users in a specific voice channel."""
        try:
            # Check if bot has mute_members permission
            if not ctx.guild.me.guild_permissions.mute_members:
                await ctx.send("ボットにメンバーをミュートする権限がありません！サーバーの権限設定を確認してください。")
                return
                
            # Get the voice channel by ID
            voice_channel = ctx.guild.get_channel(config.VOICE_CHANNEL_ID)
            if not voice_channel:
                await ctx.send(f"指定されたチャンネル（ID: {config.VOICE_CHANNEL_ID}）が見つかりません！")
                return
                
            if not isinstance(voice_channel, discord.VoiceChannel):
                await ctx.send(f"指定されたチャンネル（ID: {config.VOICE_CHANNEL_ID}）はボイスチャンネルではありません！")
                return
                
            # Check if there are members in the voice channel
            if not voice_channel.members:
                await ctx.send("ボイスチャンネルに誰も接続していません！")
                return
                
            # Mute all members in the voice channel
            for member in voice_channel.members:
                # Check role hierarchy
                if ctx.guild.me.top_role <= member.top_role:
                    await ctx.send(f"ボットのロールが {member.name} のロール以下です！ボットのロールを上位に設定してください。")
                    continue
                await member.edit(mute=True)
                
            await ctx.send(f"ボイスチャンネル {voice_channel.name} まかそ軍全員突撃！")
        except Exception as e:
            await handle_command_error(ctx, e, "一括ミュート処理でエラーが発生しました")
    
    @commands.command(name='解除', help="ボイスチャンネル内のすべてのユーザーのミュートを解除します。管理者権限が必要です。")
    @commands.has_permissions(administrator=True)
    async def unmute_all(self, ctx):
        """Unmute all users in a specific voice channel."""
        try:
            # Check if bot has mute_members permission
            if not ctx.guild.me.guild_permissions.mute_members:
                await ctx.send("ボットにメンバーをミュートする権限がありません！サーバーの権限設定を確認してください。")
                return
                
            # Get the voice channel by ID
            voice_channel = ctx.guild.get_channel(config.VOICE_CHANNEL_ID)
            if not voice_channel:
                await ctx.send(f"指定されたチャンネル（ID: {config.VOICE_CHANNEL_ID}）が見つかりません！")
                return
                
            if not isinstance(voice_channel, discord.VoiceChannel):
                await ctx.send(f"指定されたチャンネル（ID: {config.VOICE_CHANNEL_ID}）はボイスチャンネルではありません！")
                return
                
            # Check if there are members in the voice channel
            if not voice_channel.members:
                await ctx.send("ボイスチャンネルに誰も接続していません！")
                return
                
            # Unmute all members in the voice channel
            for member in voice_channel.members:
                await member.edit(mute=False)
                
            await ctx.send(f"ボイスチャンネル {voice_channel.name} まかそ軍全員撤退！")
        except Exception as e:
            await handle_command_error(ctx, e, "ミュート解除処理でエラーが発生しました")
    
    # Error handlers
    @nuke.error
    async def nuke_error(self, ctx, error):
        """Error handler for nuke command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("あなたにメッセージ管理権限がありません！")
        else:
            await handle_command_error(ctx, error)

    @speech_control.error
    async def speech_control_error(self, ctx, error):
        """Error handler for speech_control command."""
        await handle_command_error(ctx, error)

    @mute_all.error
    async def mute_all_error(self, ctx, error):
        """Error handler for mute_all command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("お前には無理じゃ！（笑）")
        else:
            await handle_command_error(ctx, error)

    @unmute_all.error
    async def unmute_all_error(self, ctx, error):
        """Error handler for unmute_all command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("あなたに管理者権限がありません！")
        else:
            await handle_command_error(ctx, error)

async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(ModerationCommands(bot))
