import discord
import json
from discord.ext import commands
from discord import app_commands

# Load configuration from config.json
with open("config.json", "r") as file:
    config = json.load(file)

TOKEN = config["token"]
GUILD_ID = config["guild_id"]
CHANNEL_IDS = config["channel_ids"]
ALLOWED_ROLE_ID = int(config["allowed_role_id"])
SERVER_ICON_URL = config["icon_url"]

# Enable intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)  # Copy commands to the guild
        synced = await bot.tree.sync(guild=guild)  # Force sync slash commands
        print(f"✅ Synced {len(synced)} commands for {bot.user} in guild {GUILD_ID}")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.tree.command(name="announce", description="Send an announcement")
@app_commands.describe(message="The announcement message")
async def announce(interaction: discord.Interaction, message: str):
    """Send an announcement to specific channels if the user has the correct role"""
    
    # Check if the user has the allowed role
    if ALLOWED_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("⛔ You don't have permission to use this command.", ephemeral=True)
        return

    # Enhanced Dark Blue UI for Announcement Bot
    embed = discord.Embed(
        title="📢 ANNOUNCEMENT",
        description=message,  # Message directly in the description
        color=discord.Color.dark_blue(),  # Dark Blue Theme
        timestamp=discord.utils.utcnow()
    )
    embed.set_thumbnail(url=SERVER_ICON_URL)  # Server Logo as Thumbnail
    embed.set_footer(text="Stay updated with Quantum Roleplay")

    # Send message to all allowed channels
    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(int(channel_id))
        if channel:
            message_sent = await channel.send(embed=embed)
            await message_sent.add_reaction("✅")  # Auto react to the announcement

    await interaction.response.send_message("✅ Announcement sent successfully!", ephemeral=True)

bot.run(TOKEN)
