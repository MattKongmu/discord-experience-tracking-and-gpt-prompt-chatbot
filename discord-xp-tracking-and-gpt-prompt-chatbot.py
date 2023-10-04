import discord
from discord.ext import commands
import openai
import asyncio

intents = discord.Intents.all()
intents.members = True

TOKEN = "YOUR TOKEN HERE"
openai.api_key = "YOUR API KEY HERE"

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store character experience
experience = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


experience_points = {}

# define a command to add experience points to a character
@bot.command()
async def addxp(ctx, member: discord.Member, xp: int):
    if member.id not in experience_points:
        experience_points[member.id] = xp
    else:
        experience_points[member.id] += xp
    await ctx.send(f"{member.mention} gained {xp} XP. Total XP: {experience_points[member.id]}")


# define a command to check a character's experience points
@bot.command()
async def checkxp(ctx, member: discord.Member):
    if member.id not in experience_points:
        await ctx.send(f"{member.mention} has no XP.")
    else:
        await ctx.send(f"{member.mention} has {experience_points[member.id]} XP.")


# define a command to send a prompt to ChatGPT and post its response
@bot.command()
async def gpt(ctx, *, prompt: str):
    response = await fetch_gpt_response(prompt)
    await ctx.send(f"{response}")
    
async def fetch_gpt_response(prompt: str):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Change the engine here
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        message = response.choices[0].text.strip()
        return message
    except Exception as e:
        print(f"Error fetching GPT response: {e}")
        return f"Error: Unable to fetch GPT response. Details: {e}"


bot.run(TOKEN)
