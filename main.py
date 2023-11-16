import discord
import os
import logging
import random
from discord.ext import commands
from discord import FFmpegPCMAudio, ConnectionClosed, ClientException
import asyncio
from dotenv import load_dotenv
from pydub import AudioSegment
from song_titles import song_titles

load_dotenv()
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.typing = False
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)





class NextCog(commands.Cog):
    def __init__(self, bot, voice_client):
        self.bot = bot
        self.voice_client = voice_client

    @commands.command()
    async def next(self, ctx):
        print("Next command triggered")
        voice_client = None
        print(f"dans next dans commands.command: {voice_client}")
        for vc in self.bot.voice_clients:
            if vc.guild == ctx.guild:
                voice_client = vc
                break

        if voice_client is None:
            print("Bot is not connected to a voice channel.")
            return

        try:

            voice_client.stop()
            print(f"dans next dans le try catch: {voice_client}")
            print("Next song will play")
            await play_random_song()
            
        except Exception as e:
            print(f"Error occurred tg: {e}")

async def setup(bot, voice_client):
    cog = NextCog(bot, voice_client)
    bot.add_cog(cog)
    return cog





async def change_status():
    await bot.wait_until_ready()

    while not bot.is_closed():
        statuses = [
            discord.Game(name="VCG!"),
            discord.Game(name="Kitsui!"),
            discord.Game(name="Koni!"),
            discord.Game(name="Kitsui Koni!"),
        ]

        for status in statuses:
            await bot.change_presence(activity=status)
            await asyncio.sleep(10)

audio_files = [file for file in os.listdir("songs") if file.endswith(".mp3")]
random.shuffle(audio_files)  
voice_client = None
print(f"DEHORS: {voice_client}")

playlist = []

song_titles = song_titles

@bot.event
async def on_ready():
    print(f'{bot.user.name} is damn connected !!')

    global voice_client

    target_voice_channel_id = 1150149299028635731
    target_voice_channel = bot.get_channel(target_voice_channel_id)

    bot.loop.create_task(change_status())
    if target_voice_channel:
        if voice_client is None:
            voice_client = await target_voice_channel.connect()
        print(f"le global dans bot.loop: {voice_client}")
        print("Bot is connected to the voice channel and starting to play music.")
        await play_random_song()

@bot.event   
async def play_random_song():
    global voice_client
    print(f"dans play_random_song: {voice_client}")
    target_voice_channel_id = 1150149299028635731
    target_voice_channel = bot.get_channel(target_voice_channel_id)
    print(f"le bot tg: {target_voice_channel}")
    bot.loop.create_task(change_status())
    if target_voice_channel:
        if voice_client is None:
            voice_client = await target_voice_channel.connect()
        print(f"dans play_random_song2: {voice_client}")
    text_channel_id = 583667220861681664
    text_channel = bot.get_channel(text_channel_id)
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
                target_voice_channel_id = 1150149299028635731
                target_voice_channel = bot.get_channel(target_voice_channel_id)
                print(f"Disconnected from voice with error: {e}")
                print("Attempting to reconnect...")
                voice_client = await target_voice_channel.connect()
                continue

bot_token = os.getenv("DISCORD_BOT_TOKEN")

async def run_bot():
    try:
        print("oui")

    except Exception as e:
        print(f"Error loading extension: {e}")




if __name__ == "__main__":
    try:
        print(f"en bas la: {voice_client}")
        bot.loop.run_until_complete(setup(bot, voice_client))
        bot.run(bot_token)
    except KeyboardInterrupt:
        if voice_client:
            voice_client.stop()
            voice_client.disconnect()
