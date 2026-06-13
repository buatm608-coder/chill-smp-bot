import discord
from discord.ext import commands
from mcstatus import BedrockServer
import os

TOKEN = os.envirion.get("TOKEN")
SERVER_IP = "https://bedrock-2.mcserver.my.id"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online sebagai {bot.user}")

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
        embed.add_field(name="Status", value="🔴 Offline", inline=False)
        await ctx.send(embed=embed)

bot.run(TOKEN)