import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.environ["token"]
GUILD_ID = os.environ["guild_id"]

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


@tree.command(name="setmarks", description="Set BITSAT marks role", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(marks="Your BITSAT score (0–390)")
async def set_marks(interaction: discord.Interaction, marks: int):
    if marks < 0 or marks > 390:
        await interaction.response.send_message("Stop lying, chutiye", ephemeral=True)
        return

    role_name = str(marks)
    guild = interaction.guild
    member = interaction.user

    #adding marks to side and stuff
    current_nick = member.nick if member.nick else member.name
    if current_nick[0] == "[" and "]" in current_nick[1:5]:
        current_nick = current_nick[current_nick.index("]")+1:]

    new_nick = f"[{marks}] {current_nick}"
    if len(new_nick) > 32:  #name too long
        await interaction.response.send_message("Bhai tera naam bhot lamba hai, chota kr de", ephemeral=True)
        return

    try:
        await member.edit(nick=new_nick)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to change your nickname.", ephemeral=True)
        return

    await interaction.response.send_message(
        f"✅ Nickname updated to `{new_nick}`! Now take lite :)", ephemeral=True
    )
bot.run(TOKEN)

#well i hope it works now
