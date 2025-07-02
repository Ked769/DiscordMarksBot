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

d = dict()
users = dict()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} commands to guild.")
        global d
        f = open("seniors.txt")
        for line in f:
            uid, nick = line.split()
            d[uid] = nick
        f.close()
        f = open("users.txt")
        for line in f:
            uid, nick = line.split()
            users[uid] = nick
        f.close()
    except Exception as e:
        print(e)    # oops, fucked up

@tree.command(name="setmarks", description="Set BITSAT marks role", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(marks="Your BITSAT score (0–390)")
async def set_marks(interaction: discord.Interaction, marks: int):
    if marks < 0 or marks > 390:
        await interaction.response.send_message("Stop lying, chutiye 🤬", ephemeral=True)
        return

    role_name = str(marks)
    guild = interaction.guild
    member = interaction.user

    # Save original nickname to users.txt if this is their first time using setmarks
    current_nick = member.nick if member.nick else member.name
    if member.name not in users:
        # Save to users.txt
        with open("users.txt", "w") as f:
            for mem in users:
                f.write(f"{mem} {users[mem]}\n")
        users[member.name] = current_nick
        print(f"added {member.nick} to users.txt")
        print(open("users.txt").read())

    if member.name in users and member.nick != users[member.name]:
        users[member.name] = member.nick
        with open("users.txt", "w") as f:
            for mem in users:
                f.write(f"{mem} {user[mem]}\n")
        print(f"added {member.nick} to users.txt")

    if member.name in d:
        await member.edit(nick=d[member.name])
        await interaction.response.send_message(
            f"✅ Senior nick alloted! Hope ya like it :)", ephemeral=True
        )
        return
    elif member.name == "floatingreeds":
        await interaction.response.send_message("sorry, I don't think you'd like any nickname I give you.", ephemeral=True)
        return

    #adding marks to side and stuff
    if current_nick[0] == "[" and "]" in current_nick[1:5]:
        current_nick = current_nick[current_nick.index("]")+1:]

    new_nick = f"[{marks}]{current_nick}"
    if len(new_nick) > 32:  #name too long
        await interaction.response.send_message("Bhai tera naam bhot lamba hai, chota kr de 😅", ephemeral=True)
        return
    
    try:
        await member.edit(nick=new_nick)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to change your nickname 😕 contact ked769#9886", ephemeral=True)
        return

    await interaction.response.send_message(
        f"✅ Nickname updated to `{new_nick}`! Now take lite :)", ephemeral=True
    )

@tree.command(name="resetnick", description="Reset to your original nickname", guild=discord.Object(id=GUILD_ID))
async def reset_nick(interaction: discord.Interaction):
    member = interaction.user
    
    if member.name not in users:
        await interaction.response.send_message("You don't have an original nickname saved!", ephemeral=True)
        print(open("users.txt").read())
        return
        
    try:
        await member.edit(nick=users[member.name])
        await interaction.response.send_message(
            f"✅ Nickname reset to your original: `{users[member.name]}`", ephemeral=True
        )
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to change your nickname 😕 contact ked769#9886", ephemeral=True)

bot.run(TOKEN)

#well i hope it works now
