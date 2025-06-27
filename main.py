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


@tree.command(name="setmarks", description="Set BITSAT marks role", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(marks="Your BITSAT score (0–390)")
async def set_marks(interaction: discord.Interaction, marks: int):
    if marks < 0 or marks > 390:
        await interaction.response.send_message("Stop lying, chutiye", ephemeral=True)
        return

    role_name = str(marks)
    guild = interaction.guild
    member = interaction.user

    # making role
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        try:
            role = await guild.create_role(name=role_name)
        except discord.Forbidden:
            await interaction.response.send_message("permission insufficient", ephemeral=True)
            return

    # in case you already got marks assigned
    for r in member.roles:
        if r.name.isdigit() and 0 <= int(r.name) <= 390:
            await member.remove_roles(r) # get unmarked

    # Assign the new role
    await member.add_roles(role)
    await interaction.response.send_message(f"You’ve been given `{marks}` flair! Now take lite", ephemeral=True)

bot.run(TOKEN)
