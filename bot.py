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

bot.run(TOKEN)