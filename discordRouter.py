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
            return await response.json()

async def send_discord_message(interaction, message):
    # Split message if it's longer than 2000 characters
    while message:
        chunk = message[:2000]
        await interaction.user.send(chunk)
        message = message[2000:]

# This function fetches the avatar based on the provided details
async def fetch_avatar(details: str):
    return await api_call(API_URL_AVATAR, {"question": details})

# This function fetches the content based on the avatar
async def fetch_content(avatar_output: str):
    return await api_call(API_URL_CONTENT, {"question": avatar_output})

# This function fetches the script based on the content
async def fetch_script(content_output: str):
    predefined_text = (
        "If multiple articles are shared, pick one you think would make the best video script. "
        "Based on the following information, write a short voice over video script that brings your business, product or service into the narrative with the article, blog, YouTube video, regulatory change, or conversation happening online. "
        "Vidar For the video script, use the hook, story, actionable steps format. "
        "For the hook, depending on what makes the most sense, use one of these ( ) based on the context of the article, blog, YouTube video, regulatory change, or conversation happening online. "
        "For the story, take inspiration from the content and bring the business into the narrative as a solution. "
        "For the actionable steps, research and provide steps the viewer can use to solve their problem or address their needs. Details: " + content_output
    )
    return await api_call(API_URL_SCRIPT, {"question": predefined_text})

@bot.slash_command(name="avatar", description="Create a psychographic client avatar")
async def avatar(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    avatar_output = await fetch_avatar(details)
    await send_discord_message(interaction, avatar_output)
    await interaction.followup.send("Response sent via DM!") 

@bot.slash_command(name="content", description="Find the latest newsworthy content for your client avatar")
async def content(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    content_output = await fetch_content(details)
    await send_discord_message(interaction, content_output)
    await interaction.followup.send("Response sent via DM!")

@bot.slash_command(name="script", description="Create a custom video script")
async def script(interaction: disnake.ApplicationCommandInteraction, topic: str):
    await interaction.response.defer()
    script_output = await fetch_script(topic)
    await send_discord_message(interaction, script_output)
    await interaction.followup.send("Response sent via DM!")

@bot.slash_command(name="full_process", description="Full process from avatar creation to video script")
async def full_process(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    
    avatar_output = await fetch_avatar(details)
    content_output = await fetch_content(avatar_output)
    script_output = await fetch_script(content_output)
    
    await send_discord_message(interaction, script_output)
    await interaction.followup.send("Response sent via DM!")

# ... (rest of your events and bot.run())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
