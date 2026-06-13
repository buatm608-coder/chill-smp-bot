import discord
from discord.ext import commands
from mcstatus import BedrockServer
import os
import asyncio

TOKEN = os.environ.get("TOKEN")
SERVER_IP = "bedrock-2.mcserver.my.id:59516"
CHANNEL_ID = 1515298297806458921

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def update_channel():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    print(f"Channel: {channel}")
    while not bot.is_closed():
        try:
            server = BedrockServer.lookup(SERVER_IP)
            status = server.status()
            print(f"Players: {status.players.online}/{status.players.max}")
            await channel.edit(name=f"🟢 Player: {status.players.online}/{status.players.max}")
        except Exception as e:
            print(f"Error: {e}")
            await channel.edit(name=f"🔴 Server Offline")
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Bot online sebagai {bot.user}")
    bot.loop.create_task(update_channel())

@bot.command()
async def mcstatus(ctx):
    try:
        server = BedrockServer.lookup(SERVER_IP)
        status = server.status()
        embed = discord.Embed(
            title="🎮 CHILL SMP Status",
            color=discord.Color.green()
        )
        embed.add_field(name="Status", value="🟢 Online", inline=False)
        embed.add_field(name="Player Online", value=f"{status.players.online}/{status.players.max}", inline=False)
        embed.add_field(name="Versi", value=str(status.version.name), inline=False)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(
            title="🎮 CHILL SMP Status",
            color=discord.Color.red()
        )
        embed.add_field(name="Status", value="🔴 Server Offline", inline=False)
        await ctx.send(embed=embed)
REPORT_CHANNEL_ID = 1515309188127916162

@bot.command()
async def report(ctx, member: discord.Member, *, alasan: str):
    channel = bot.get_channel(REPORT_CHANNEL_ID)
    embed = discord.Embed(
        title="🚨 Report Baru!",
        color=discord.Color.red()
    )
    embed.add_field(name="Reporter", value=ctx.author.mention, inline=False)
    embed.add_field(name="Dilaporkan", value=member.mention, inline=False)
    embed.add_field(name="Alasan", value=alasan, inline=False)
    embed.set_footer(text=f"Report dari #{ctx.channel.name}")
    await channel.send(embed=embed)
    await ctx.send(f"✅ Report kamu udah dikirim ke admin!")

import json

XP_FILE = "xp.json"

def load_xp():
    try:
        with open(XP_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f)

def get_level(xp):
    return int(xp ** 0.5) // 5

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    data = load_xp()
    user_id = str(message.author.id)
    if user_id not in data:
        data[user_id] = 0
    old_level = get_level(data[user_id])
    data[user_id] += 10
    new_level = get_level(data[user_id])
    save_xp(data)
    if new_level > old_level:
        await message.channel.send(f"🎉 {message.author.mention} naik ke **Level {new_level}**!")
    await bot.process_commands(message)

@bot.command()
async def rank(ctx):
    data = load_xp()
    user_id = str(ctx.author.id)
    xp = data.get(user_id, 0)
    level = get_level(xp)
    embed = discord.Embed(title=f"⭐ Rank {ctx.author.name}", color=discord.Color.gold())
    embed.add_field(name="Level", value=str(level), inline=True)
    embed.add_field(name="XP", value=str(xp), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def leaderboard(ctx):
    data = load_xp()
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
    embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())
    for i, (user_id, xp) in enumerate(sorted_data, 1):
        user = await bot.fetch_user(int(user_id))
        embed.add_field(name=f"{i}. {user.name}", value=f"Level {get_level(xp)} | {xp} XP", inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)