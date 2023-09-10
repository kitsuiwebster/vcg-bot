import discord
import os
import random
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

audio_files = [file for file in os.listdir("songs") if file.endswith(".mp3")]
voice_client = None
playlist = []

@bot.event
async def on_ready():
    print(f'{bot.user.name} is damn connected !!')

    target_voice_channel_id = 1150149299028635731
    target_voice_channel = bot.get_channel(target_voice_channel_id)

    if target_voice_channel:
        global voice_client
        voice_client = await target_voice_channel.connect()
        print("Bot is connected to the voice channel and starting to play music.")

        while True:
            if not playlist:
                random_audio_file = random.choice(audio_files)
                audio_file_path = os.path.join("songs", random_audio_file)

                audio = AudioSegment.from_mp3(audio_file_path)
                audio_duration = len(audio) / 1000

                audio_source = FFmpegPCMAudio(executable="ffmpeg", source=audio_file_path)
                voice_client.play(audio_source)
                
                await asyncio.sleep(audio_duration)

            if not voice_client.is_connected():
                break


bot_token = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
    try:
        bot.run(bot_token)
    except KeyboardInterrupt:
        if voice_client:
            voice_client.stop()
            voice_client.disconnect()
