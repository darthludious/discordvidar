import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import requests
import random

# Environment variables
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
API_URL_VIDAR = os.environ["API_URL_VIDAR"]
API_URL_AVATAR = os.environ["API_URL_AVATAR"]
API_URL_CONTENT = os.environ["API_URL_CONTENT"]
API_URL_SCRIPT = os.environ["API_URL_SCRIPT"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)  # Initialize slash commands

# Different variations of the bot's response in channel
RESPONSES = [
    "Absolutely, {}! I shall deliver the wisdom you seek in a private message shortly.",
    "Understood, {}! I'll craft a masterful response and send it directly to you.",
    "Of course, {}! I'm conjuring my videography magic and will DM you the result.",
    "Fear not, {}! Vidar is on the task. Check your direct messages in a moment.",
    "Right away, {}! The essence of Vidar's knowledge will be in your DMs shortly."
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@slash.slash(name="vidar", description="Vidar QnA")
async def _vidar(ctx: SlashContext, question: str):
    response_msg = random.choice(RESPONSES).format(ctx.author.mention)
    await ctx.send(content=response_msg)
    try:
        output = requests.post(API_URL_VIDAR, json={"question": question}, timeout=30).json()
        await ctx.author.send(output)  # Send the response as a DM
    except requests.ConnectionError:
        await ctx.author.send("Sorry, I'm having trouble connecting to my knowledge source right now. Please try again later.")
    except requests.Timeout:
        await ctx.author.send("It's taking longer than expected to fetch the answer. Please wait a moment and try again.")
    except Exception as e:
        await ctx.author.send("Oops! Something went wrong. Please try again later.")
        print(f"Error: {e}")

@slash.slash(name="avatar", description="Create a psychographic client avatar")
async def _avatar(ctx: SlashContext, details: str):
    response_msg = random.choice(RESPONSES).format(ctx.author.mention)
    await ctx.send(content=response_msg)
    message = f"Create a client psychographic avatar for the following company. Only respond with the client avatar. You don't need to add any commentary. {details}"
    try:
        output = requests.post(API_URL_AVATAR, json={"details": message}, timeout=30).json()
        await ctx.author.send(output)
    except requests.ConnectionError:
        await ctx.author.send("Sorry, I'm having trouble connecting to my knowledge source right now. Please try again later.")
    except requests.Timeout:
        await ctx.author.send("It's taking longer than expected to fetch the answer. Please wait a moment and try again.")
    except Exception as e:
        await ctx.author.send("Oops! Something went wrong. Please try again later.")
        print(f"Error: {e}")

@slash.slash(name="content", description="Find the latest newsworthy content for your client avatar")
async def _content(ctx: SlashContext, details: str):
    response_msg = random.choice(RESPONSES).format(ctx.author.mention)
    await ctx.send(content=response_msg)
    message = f"Find me 5 recent newsworthy articles that would engage my psychographic client avatars and be related to what I do. If you don't remember my client avatar use the following information to help you find the articles. I only need the articles, and a short synopsis of each and how they would engage my audience. {details}"
    try:
        output = requests.post(API_URL_CONTENT, json={"details": message}, timeout=30).json()
        await ctx.author.send(output)
    except requests.ConnectionError:
        await ctx.author.send("Sorry, I'm having trouble connecting to my knowledge source right now. Please try again later.")
    except requests.Timeout:
        await ctx.author.send("It's taking longer than expected to fetch the answer. Please wait a moment and try again.")
    except Exception as e:
        await ctx.author.send("Oops! Something went wrong. Please try again later.")
        print(f"Error: {e}")

@slash.slash(name="script", description="Create a custom video script")
async def _script(ctx: SlashContext, topic: str):
    response_msg = random.choice(RESPONSES).format(ctx.author.mention)
    await ctx.send(content=response_msg)
    message = f"Using my client psychographic avatar create an engaging script for the following prompt. If you don't remember my avatar, use the information to create one before creating your script. We only need the script, you don't have to provide any other information or commentary. Prompt: {topic}"
    try:
        output = requests.post(API_URL_SCRIPT, json={"topic": message}, timeout=30).json()
        await ctx.author.send(output)
    except requests.ConnectionError:
        await ctx.author.send("Sorry, I'm having trouble connecting to my knowledge source right now. Please try again later.")
    except requests.Timeout:
        await ctx.author.send("It's taking longer than expected to fetch the answer. Please wait a moment and try again.")
    except Exception as e:
        await ctx.author.send("Oops! Something went wrong. Please try again later.")
        print(f"Error: {e}")

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
