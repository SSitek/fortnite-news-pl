
import discord
from discord.ext import tasks
import aiohttp
import os

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    if not news_loop.is_running():
        news_loop.start()

@tasks.loop(minutes=30)
async def news_loop():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        return

    url = "https://www.fortnite.com/news"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return
            text = await response.text()

    embed = discord.Embed(
        title="🎮 Fortnite News PL",
        description="Sprawdź najnowsze wiadomości Fortnite!",
        color=0x9B59B6,
        url=url
    )
    embed.add_field(
        name="📰 Oficjalne wiadomości",
        value="[Otwórz Fortnite News](https://www.fortnite.com/news)",
        inline=False
    )
    await channel.send(embed=embed)

bot.run(TOKEN)
