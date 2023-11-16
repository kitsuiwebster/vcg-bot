from discord.ext import commands
from main import play_random_song



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
