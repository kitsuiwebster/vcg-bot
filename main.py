import discord
import os
import random
from discord.ext import commands
from discord import FFmpegPCMAudio, ConnectionClosed, ClientException
import asyncio
from dotenv import load_dotenv
from pydub import AudioSegment
from variables import song_titles

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)


async def change_status():
    await bot.wait_until_ready()

    while not bot.is_closed():
        server_count = len(bot.guilds)
        total_member_count = sum(guild.member_count for guild in bot.guilds)
        statuses = [
            discord.Game(name=f"in {server_count} servers"),
            discord.Game(name=f"with {total_member_count} members"),
        ]

        for status in statuses:
            await bot.change_presence(activity=status)
            await asyncio.sleep(10)

audio_files = [file for file in os.listdir("songs") if file.endswith(".mp3")]
random.shuffle(audio_files)  
voice_client = None
playlist = []

song_titles = song_titles

@bot.event
async def on_ready():
    print(f'{bot.user.name} is damn connected !!')

    bot.loop.create_task(change_status())

    target_voice_channel_id = 1150149299028635731
    target_voice_channel = bot.get_channel(target_voice_channel_id)

    text_channel_id = 583667220861681664
    text_channel = bot.get_channel(text_channel_id)

    if target_voice_channel:
        global voice_client
        voice_client = await target_voice_channel.connect()
        print("Bot is connected to the voice channel and starting to play music.")

        while True:
            try:
                if not playlist:
                    audio_files = [file for file in os.listdir("songs") if file.endswith((".mp3", ".wav"))]

                    if not audio_files:
                        print("No more songs in the 'songs' directory.")
                        break

                    random.shuffle(audio_files)

                    random_audio_file = audio_files.pop(0)
                    audio_file_path = os.path.join("songs", random_audio_file)

                    audio = AudioSegment.from_mp3(audio_file_path)
                    audio_duration = len(audio) / 1000

                    audio_source = FFmpegPCMAudio(executable="ffmpeg", source=audio_file_path)
                    try:
                        if not voice_client.is_playing():
                            voice_client.play(audio_source)
                            song_title = song_titles.get(random_audio_file, 'Unknown')
                            await text_channel.send(f'Vous écoutez désormais: {song_title}')
                        else:
                            print("Bot is already playing.")
                    except (ConnectionClosed, ClientException) as e:
                        print(f"Error occurred: {e}")
                        break

                    await asyncio.sleep(audio_duration)

            except discord.errors.ConnectionClosed as e:
                print(f"Disconnected from voice with error: {e}")
                print("Attempting to reconnect...")
                voice_client = await target_voice_channel.connect()
                continue
            


bot_token = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
    try:
        bot.run(bot_token)
    except KeyboardInterrupt:
        if voice_client:
            voice_client.stop()
            voice_client.disconnect()
