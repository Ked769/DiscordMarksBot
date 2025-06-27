import discord
from discord.ext import commands
from discord import app_commands

TOKEN = open("token.txt").read()
GUILD_ID = int(open("guildID.txt").read())

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # to do those cool /set commands


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} commands to guild.")
    except Exception as e:
        print(e)    # oops, fucked up


