# -*- coding: utf-8 -*-
"""
Configuration module for the Discord bot.
Contains environment variable handling and bot settings.
"""
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

# API Keys and tokens from environment variables with fallback to input
def get_api_key(name, prompt):
    """Get API key from environment variable with fallback to user input."""
    value = os.getenv(name)
    if not value:
        # Renderでは実行環境でインタラクティブな入力ができないため、
        # 環境変数RENDERが設定されている場合はそのまま例外を発生させる
        if os.getenv('RENDER') == 'true':
            raise ValueError(f"環境変数 {name} が設定されていません。Renderダッシュボードで環境変数を設定してください。")
        
        # ローカル環境の場合は入力を受け付ける
        logger.info(f"{prompt}")
        value = input().strip()
        if not value:
            raise ValueError(f"{name} is not provided")
    return value

# Bot configuration
BOT_PREFIX = '!'
GEMINI_MODEL = 'gemini-1.5-flash'
MAX_MESSAGE_LENGTH = 2000
MAX_OUTPUT_TOKENS = 1000
TEMPERATURE = 0.7

# Fixed channel and user IDs
VOICE_CHANNEL_ID = 1350092524127125538
TARGET_USER_ID = 860507172835033118

# Gemini system prompt
SYSTEM_PROMPT = "あなたは親しみやすい日本語アシスタントです。自然でフレンドリーに応答してください。"

# Command descriptions (for help messages)
COMMAND_DESCRIPTIONS = {
    "gemini": "Gemini AIを使って質問に答えます。例: !gemini こんにちは",
    "nuke": "チャンネル内のすべてのメッセージを削除します。管理者権限が必要です。",
    "言論統制": "特定のユーザーをボイスチャンネルでミュートします。",
    "暑くないわ": "ボイスチャンネル内のすべてのユーザーをミュートします。管理者権限が必要です。",
    "解除": "ボイスチャンネル内のすべてのユーザーのミュートを解除します。管理者権限が必要です。",
    "ping": "ボットの応答時間を確認します。",
    "time": "日本の現在時刻を表示します。(!時間でも利用可能)",
    "help": "利用可能なコマンドの一覧を表示します。"
}
