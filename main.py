version = "alpha v2.0.0"
##################
import time
import discord
from discord.ext import commands
from discord import app_commands
import random
import requests
import os
from dotenv import load_dotenv
from datetime import timedelta
import base64
from PIL import Image, ImageDraw

START_TIME = time.time()

# Fix for Python 3.8+ where time.clock() was removed
if not hasattr(time, 'clock'):
    time.clock = time.perf_counter

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

DEV_GUILD_ID = 1457996708293120086

@bot.event
async def on_ready():
    guild = discord.Object(id=DEV_GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync(guild=None)
    requests.post(
        os.getenv("WEBHOOK_URL"),
        json={"content": "# dev bot online! <@&1458303852712562984>"}
    )

@bot.tree.command(name="ping", description="check bot status & latency")
async def ping(interaction: discord.Interaction):
    # Latency
    ws_latency = round(bot.latency * 1000)

    # Uptime
    uptime_seconds = int(time.time() - START_TIME)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60 

    if ws_latency < 300:
        status = "🟢"
    elif ws_latency < 500:
        status = "🟡"
    else:
        status = "🔴"

    vibe = random.choice([
        "we up",
        "still alive!",
        "pinged and responded",
        "not dead yet",
        "bot go brrr"
    ])

    embed = discord.Embed(
        title="pong! result:",
        description=vibe,
        color=discord.Color.green()
    )

    embed.add_field(name="latency", value=f"{ws_latency} ms", inline=True)
    embed.add_field(name="uptime", value=f"{hours}h {minutes}m", inline=True)
    embed.add_field(name="status", value=f"{status}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="dice", description="random number 1–6")
async def randnum(interaction: discord.Interaction):
    num = random.randint(1,6)
    await interaction.response.send_message(f"**{num}**")

@bot.tree.command(name="choose",description="choose smth")
async def choose(interaction: discord.Interaction, choice1: str, choice2: str):
    result = random.choice([choice1, choice2])
    await interaction.response.send_message(f"between {choice1} and {choice2}, i choose {result}!")

@bot.tree.command(name="b64encode", description="text to base64")
async def b64(interaction: discord.Interaction, text: str):
    try:
        result = base64.b64encode(text.encode()).decode()
        await interaction.response.send_message(f"user input: ```{text}```\nresult: ```{result}```", ephemeral=True)

    except:
        await interaction.response.send_message("invalid base64", ephemeral=True)

@bot.tree.command(name="b64decode", description="base64 to text")
async def b64(interaction: discord.Interaction, text: str):
    try:
        result = base64.b64decode(text.encode()).decode()
        await interaction.response.send_message(f"user input: ```{text}```\nresult: ```{result}```", ephemeral=True)

    except:
        await interaction.response.send_message("invalid base64", ephemeral=True)

@bot.tree.command(name="meme", description="send a random meme")
async def meme(interaction: discord.Interaction):
    all_files = os.listdir("meme")
    random_file = random.choice(all_files)
    await interaction.response.send_message(file=discord.File(f"meme/{random_file}"))

@bot.tree.command(name="rate", description="rate user")
async def rate(interaction, member: discord.Member):
    await interaction.response.send_message(f"{member.mention} is **{random.randint(1,10)}/10**")

@bot.tree.command(name="about", description="about this bot")
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="about this bot",
        description="a bot made by susp3st0",
        color=discord.Color.green()
    )
    embed.add_field(name="creator", value="susp3st0", inline=False)
    embed.add_field(name="version", value=version, inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="say", description="say smth")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@bot.tree.command(name="randomdraw", description="random draw")
async def randomdraw(interaction: discord.Interaction, randomrange: int):
    img = Image.new("RGB", (400, 300), "white")
    draw = ImageDraw.Draw(img)
    for _ in range(randomrange):
        x1 = random.randint(0, 350)
        y1 = random.randint(0, 250)
        x2 = x1 + random.randint(10, 50)
        y2 = y1 + random.randint(10, 50)

        color = (
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )

        draw.rectangle([x1, y1, x2, y2], fill=color)

    for _ in range(randomrange):
        x1 = random.randint(0, 350)
        y1 = random.randint(0, 250)
        x2 = x1 + random.randint(10, 50)
        y2 = y1 + random.randint(10, 50)

        color = (
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )

        draw.ellipse([x1, y1, x2, y2], fill=color)

    for _ in range(randomrange):
        x1 = random.randint(0, 350)
        y1 = random.randint(0, 250)
        x2 = x1 + random.randint(10, 50)
        y2 = y1 + random.randint(10, 50)

        color = (
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )

        draw.line([x1, y1, x2, y2], fill=color)

    img.save("random.png")
    await interaction.response.send_message("result:",file=discord.File("random.png"))


@bot.tree.command(name="8ball",description="similer to /choose, but this thing is yes/no")
async def ball(interaction: discord.Interaction, question: str):
    answer = random.choice(["yes","no","maybe","i dont know","ok","later"])
    await interaction.response.send_message(f"**question**: {question}\n**response**: {answer}")

@bot.tree.command(name="kick", description="kick a user")
@app_commands.default_permissions(administrator=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"kicked {member.mention}")
@kick.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, (app_commands.MissingRole, app_commands.MissingAnyRole)):
        await interaction.response.send_message("You dont have permission", ephemeral=True)

@bot.tree.command(name="ban", description="ban a user")
@app_commands.default_permissions(administrator=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"banned {member.mention}")
@ban.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, (app_commands.MissingRole, app_commands.MissingAnyRole)):
        await interaction.response.send_message("You dont have permission", ephemeral=True)

@bot.tree.command(name="timeout", description="timeout a user")
@app_commands.checks.has_permissions(moderate_members=True)
@app_commands.choices(
    duration=[
        app_commands.Choice(name="1 Minute", value=60),
        app_commands.Choice(name="5 Minutes", value=300),
        app_commands.Choice(name="10 Minutes", value=600),
        app_commands.Choice(name="1 Hour", value=3600),
        app_commands.Choice(name="1 Day", value=86400),
        app_commands.Choice(name="1 Week", value=604800),
    ]
)
async def timeout(
    interaction: discord.Interaction,
    member: discord.Member,
    duration: app_commands.Choice[int],
    reason: str = None
):
    until = discord.utils.utcnow() + timedelta(seconds=duration.value)

    await member.timeout(until, reason=reason)

    await interaction.response.send_message(
        f"**{member.mention}** timed out for **{duration.name}**\n"
        f"reason: **{reason or 'no reason'}**"
    )
@timeout.error
async def timeout_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "No permission",
            ephemeral=True
        )

@bot.tree.command(name="shutdown", description="Shutdown the bot safely")
@app_commands.check(lambda i: i.user.id == 1113996666534641726)
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message("Shutting down bot...")
    
    requests.post(
    os.getenv("WEBHOOK_URL"),
    json={"content": "# dev bot shutting down due creator's request"}
)
    
    # Close the bot gracefully
    await bot.close()

TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)


requests.post(
    os.getenv("WEBHOOK_URL"),
    json={"content": "# dev bot offline"}
)
