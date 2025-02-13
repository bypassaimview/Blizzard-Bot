import discord
import os
import requests
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_current_roblox_version():
    API_URL = "https://clientsettings.roblox.com/v2/client-version/WindowsPlayer"
    return requests.get(API_URL).json().get("clientVersionUpload")

def get_current_blizzard_version():
    API_URL = "https://raw.githubusercontent.com/bypassaimview/Blizzard-Pub/refs/heads/main/version.json"
    return requests.get(API_URL).json().get("currentVersion")

bot = commands.Bot(command_prefix=".")

current_roblox_version = get_current_roblox_version()
current_blizzard_version = get_current_blizzard_version()

@bot.event
async def on_ready():
    print("Bot is ready")
    check_versions.start()

@tasks.loop(seconds=10)
async def check_versions():
    global current_roblox_version, current_blizzard_version

    new_roblox_version = get_current_roblox_version()
    new_blizzard_version = get_current_blizzard_version()
    guild = bot.get_guild(1339411035420889198)
    channel = guild.get_channel(1339425653388218409)

    if new_roblox_version != current_roblox_version:
        embed = discord.Embed(
            title="Roblox Version Update",
            description="Roblox has updated to a new version. Please wait for Blizzard to update.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Old Roblox Version", value=current_roblox_version, inline=True)
        embed.add_field(name="New Roblox Version", value=new_roblox_version, inline=True)
        embed.set_footer(text="Blizzard")
        await channel.send(embed=embed)
        current_roblox_version = new_roblox_version

    if new_blizzard_version != current_blizzard_version:
        embed = discord.Embed(
            title="Blizzard Version Update",
            description="Blizzard has updated to a new version. Please rerun the bootstrapper.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Old Blizzard Version", value=current_blizzard_version, inline=True)
        embed.add_field(name="New Blizzard Version", value=new_blizzard_version, inline=True)
        embed.set_footer(text="Blizzard")
        await channel.send(embed=embed)
        current_blizzard_version = new_blizzard_version

bot.run(os.getenv("TOKEN"))
