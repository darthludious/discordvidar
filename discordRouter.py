import os
import discord
import requests
import random

# Environment variables
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
API_URL_VIDAR = os.environ["API_URL_VIDAR"]
API_URL_AVATAR = os.environ["API_URL_AVATAR"]
API_URL_CONTENT = os.environ["API_URL_CONTENT"]
API_URL_SCRIPT = os.environ["API_URL_SCRIPT"]

RESPONSES = [
    "Absolutely, {}! I shall deliver the wisdom you seek in a private message shortly.",
    "Understood, {}! I'll craft a masterful response and send it directly to you.",
    "Of course, {}! I'm conjuring my videography magic and will DM you the result.",
    "Fear not, {}! Vidar is on the task. Check your direct messages in a moment.",
    "Right away, {}! The essence of Vidar's knowledge will be in your DMs shortly."
]

class CustomBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = CustomBot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.tree.command(name="vidar", description="Vidar QnA")
async def vidar(interaction: discord.Interaction, question: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        output = requests.post(API_URL_VIDAR, json={"question": question}, timeout=30).json()
        await interaction.user.send(output)  # Send the response as a DM
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="avatar", description="Create a psychographic client avatar")
async def avatar(interaction: discord.Interaction, details: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        output = requests.post(API_URL_AVATAR, json={"details": details}, timeout=30).json()
        await interaction.user.send(output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="content", description="Find the latest newsworthy content for your client avatar")
async def content(interaction: discord.Interaction, details: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        output = requests.post(API_URL_CONTENT, json={"details": details}, timeout=30).json()
        await interaction.user.send(output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="script", description="Create a custom video script")
async def script(interaction: discord.Interaction, topic: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        output = requests.post(API_URL_SCRIPT, json={"topic": topic}, timeout=30).json()
        await interaction.user.send(output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
