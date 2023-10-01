import discord
import os
import random
from discord.ext import commands
from discord import FFmpegPCMAudio, ConnectionClosed, ClientException
import asyncio
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

audio_files = [file for file in os.listdir("songs") if file.endswith(".mp3")]
random.shuffle(audio_files)  # Shuffle the songs
voice_client = None
playlist = []

song_titles = {
    '21h-21.mp3': 'Kitsui - 21h21',
    'jtaff.mp3': "Kitsui Koni - J'taff",
    'ailleurs.wav': 'Koni - Ailleurs https://open.spotify.com/track/1ej1MFyhok597ohCn24x0Q?si=0ca1b7aa452840ea',
    '1er-couplet.wav': 'Koni - 1er couplet https://open.spotify.com/track/3O4lGTA2UiUvYLZjIGRRTT?si=5956fecd92884c43',
    'a-travers-les-gens.mp3': 'Kitsui Koni - À travers les gens',
    'anakin.mp3': 'Kitsui Koni - Anakin',
    'besoin-daide.mp3': "Kitsui Koni - Besoin d'aide https://open.spotify.com/track/5lB8V03QVazVN3LDEd96nX?si=17200cf453e04cff",
    'bon-endroit.mp3': 'Kitsui Koni -Bon endroit https://open.spotify.com/track/476X6ywMJ0ouiG93OjJPR3?si=22cd02f95a33482f',
    'bro.mp3': 'Kitsui (feat. Biaco) - Bro https://open.spotify.com/track/42Wwxi75o3SUZPjDa7msAS?si=e4fca77399d94f4d',
    'cheat-code.mp3': 'Kitsui Koni - Cheat-code',
    'comme-dhab.mp3': "Kitsui Koni - Comme d'hab",
    'constats.wav': 'Kitsui Koni - Constats https://open.spotify.com/track/5IK4rnjQpUkA48Jywjkr2g?si=08b84097f3854ca8',
    'copier-coller.wav': 'Kitsui Koni - Copier coller https://open.spotify.com/track/427p3cWOLea7f8GwnOb3vW?si=119872a178124ae6',
    'dans-le-feu-les-flammes.wav': 'Kitsui Koni - Dans le feu les flammes https://open.spotify.com/track/421ENtpWZwzj3fNWbxnGCt?si=02e642092a0040b8',
    'dans-mon-coeur-ca-fait.wav': 'Koni - Dans mon coeur ça fait... https://open.spotify.com/track/6BRmfVcURIDULLJP2OZjXk?si=853f97686e0e4d16',
    'demain-la-veille.mp3': 'Kitsui Koni - Demain la veille',
    'demain.mp3': 'Kitsui Koni - Demain',
    'demi-coeur-mp3': 'Kitsui - Demi-coeur',
    'des-fois.mp3': 'Kitsui - Des fois https://open.spotify.com/track/6nV7AV65kfkPIEieOOCGyS?si=2090118b72894cb2    ',
    'drive-by.wav': 'Kitsui Koni - Drive-by https://open.spotify.com/track/0CzWpj3eUWFHcTf7OE7UK0?si=067bd7956c574200',
    'emprisonne.wav': 'Kitsui Koni - Emprisonné https://open.spotify.com/track/3K5Jky5CdH6OE7ApgLQWl8?si=df7a6277e5eb4738',
    'en-pleine-tempete.wav': 'Koni - En pleine tepête',
    'encore-seul.wav': 'Koni - Encore seul https://open.spotify.com/track/4Ynz0rfUU3kq2U1GGekMMI?si=2f62f53175804474',
    'est-ce-que-tes-triste.wav': "Koni - T'es triste ?? https://open.spotify.com/track/76ZEJo8NrrGmB79ieRP32Y?si=352727cabb5f41c7",
    'fais-le.mp3': 'Kitsui Koni - Fais-le',
    'flow.wav': 'Kitsui Koni - Flow https://open.spotify.com/track/0ioPInNuPoPlkOzC1Tt8De?si=3e87c9d3ffa6405e',
    'funk-vcg.wav': 'Kitsui Koni - Funk VCG https://open.spotify.com/track/1gufzDbekhBAqbeqxeWm6u?si=47b1454ed24a4da4',
    'heureux.wav': 'Koni - Heureux? https://open.spotify.com/track/5511qgse6acMXQwUo08lUV?si=2b3d4a0409f7483b',
    'italia.mp3': 'Kitsui Koni - Santa Catalina',
    'japprend-lequilibre.mp3': "Kitsui Koni - J'apprend l'équilibre",
    'jme-releve.mp3': "Kitsui (feat. Biaco) - J'me relève",
    'jsais-pas-tellement.wav': "Koni - J'sais pas tellement https://open.spotify.com/track/7MSItuUtov00jYAIsTNoDc?si=65ca2ea58dae480f",
    'koni-loupa.mp3': "Koni (feat. Loupa)",
    'late-night.mp3': "Kitsui Koni - Late night https://open.spotify.com/track/5YIe0g0bHfPXAWGZFhNn9u?si=64199a7f37384005",
    'maladie.wav': "Kitsui Koni - Maladie https://open.spotify.com/track/3ChaHH7yB4CTpP7EXZ0EhB?si=aa253720644e48a7",
    'mediator.mp3': "Kitsui Koni - Médiator",
    'meme-pas.wav': "Koni - Même pas https://open.spotify.com/track/5fKX7ejviSGKr8Qhn8uQe3?si=3bac51d16cae4083",
    'miss-moon.mp3': "Kitsui - Miss moon",
    'nul-part.wav': "Koni - Nul part https://open.spotify.com/track/3MKOmIIOVVcVcdiU808qe7?si=2e69c9946d34469c",
    'personne.mp3': "Kitsui - Personne https://open.spotify.com/track/7fWeGzgrbRmcA3y2WVg8vS?si=582577accfd74b25",
    'pleine-vitesse.wav': "Koni - Pleine vitesse https://open.spotify.com/track/52El1WmK5J1dt4w6M2e999?si=adfc85c0d2ef4984",
    'repondeur.wav': "Kitsui Koni - Répondeur https://open.spotify.com/track/15CdWoARhqSS5bOf4kPMPg?si=bb195f982203460d",
    'rose.wav': "Kitsui Koni - Rose https://open.spotify.com/track/2yLabHgDxev3SdRqOKhs0D?si=e6fedb9382a64f52",
    'sky.wav': "Kitsui Koni - Sky https://open.spotify.com/track/0fN9YHunlpnMmMfeKEL26w?si=66fd1557684c4494",
    'soleil.wav': "Kitsui Koni - Soleil https://open.spotify.com/track/5IFVfoKmDO2d4IimOzNDhf?si=57bf7db893f3433f",
    'tant-didees.mp3': "Kitsui Koni - Tant d'idées",
    'un-dces-4.wav': "Koni - Un d'ces 4 https://open.spotify.com/track/7LPVUZrs0gWoEkuPvqDPv9?si=8e67bea4c5de4436",
}

@bot.event
async def on_ready():
    print(f'{bot.user.name} is damn connected !!')

    target_voice_channel_id = 1150149299028635731
    target_voice_channel = bot.get_channel(target_voice_channel_id)

    text_channel_id = 583667220861681664
    text_channel = bot.get_channel(text_channel_id)

    if target_voice_channel:
        global voice_client
        voice_client = await target_voice_channel.connect()
        print("Bot is connected to the voice channel and starting to play music.")

        while True:
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
                voice_client.disconnect()


bot_token = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
    try:
        bot.run(bot_token)
    except KeyboardInterrupt:
        if voice_client:
            voice_client.stop()
            voice_client.disconnect()
