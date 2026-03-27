import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True  # REQUIRED

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs
GUILD_ID = 1486860608811962512
TARGET_USER_ID = 1476998781001007104
ROLE_ID = 1486881480301875271
CHANNEL_ID = 1486881632584601671

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        # Check server
        if member.guild.id != GUILD_ID:
            return

        # Check specific user
        if member.id != TARGET_USER_ID:
            return

        # Give role
        role = member.guild.get_role(ROLE_ID)
        if role:
            await member.add_roles(role)

        # Send message
        channel = member.guild.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"<@{member.id}> has been granted perms ✅")

    except Exception as e:
        print(e)

bot.run(os.getenv("TOKEN"))
