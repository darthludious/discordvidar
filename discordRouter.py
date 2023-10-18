import os
import random
import aiohttp
import disnake
from disnake.ext import commands

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

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def api_call(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            content_type = response.headers.get('Content-Type')
            if not content_type.startswith('application/json'):
                raise ValueError(f"Unexpected response content type: {content_type}")
            return await response.json()

async def send_discord_message(interaction, message):
    while message:
        chunk = message[:2000]
        await interaction.user.send(chunk)
        message = message[2000:]

@bot.slash_command(name="vidar", description="Vidar QnA")
async def vidar(interaction: disnake.ApplicationCommandInteraction, question: str):
    await interaction.response.defer()
    output = await api_call(API_URL_VIDAR, {"question": question})
    await send_discord_message(interaction, output)

@bot.slash_command(name="avatar", description="Create a psychographic client avatar")
async def avatar(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    avatar_payload = "Create a psychographic client avatar based on the following information. " + details
    avatar_output = await api_call(API_URL_AVATAR, {"question": avatar_payload})
    await send_discord_message(interaction, avatar_output)

@bot.slash_command(name="content", description="Find the latest newsworthy content for your client avatar")
async def content(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    content_payload = ("Find 3 recent (within 72 hours) articles, blogs, YouTube videos, regulatory changes, or conversations happening online that relate to my company and client avatar and summarize what that content is about. " + details)
    content_output = await api_call(API_URL_CONTENT, {"question": content_payload})
    await send_discord_message(interaction, content_output)

@bot.slash_command(name="script", description="Create a custom video script")
async def script(interaction: disnake.ApplicationCommandInteraction, topic: str):
    await interaction.response.defer()
    script_predefined_text = ("Write a short voice over video script that integrates your business, product, or service into the context of an article, blog, YouTube video, regulatory change, or conversation happening online that relates to your company and client avatar. " + topic)
    script_output = await api_call(API_URL_SCRIPT, {"question": script_predefined_text})
    await send_discord_message(interaction, script_output)

@bot.slash_command(name="full_process", description="Full process from avatar creation to video script")
async def full_process(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    full_process_payload = ("Create a psychographic client avatar, then find 3 recent articles or content related to the company and client avatar, and finally, write a video script integrating the business into the context of the content. " + details)
    full_process_output = await api_call(API_URL_CONTENT, {"question": full_process_payload})
    await send_discord_message(interaction, full_process_output)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
