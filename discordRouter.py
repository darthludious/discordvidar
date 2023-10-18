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
            if response.headers.get('Content-Type') != 'application/json':
                raise ValueError(f"Unexpected response content type: {response.headers.get('Content-Type')}")
            return await response.json()

async def send_discord_message(interaction, message):
    # Split message if it's longer than 2000 characters
    while message:
        chunk = message[:2000]
        await interaction.user.send(chunk)
        message = message[2000:]

@bot.slash_command(name="vidar", description="Vidar QnA")
async def vidar(interaction: disnake.ApplicationCommandInteraction, question: str):
    try:
        response_msg = random.choice(RESPONSES).format(interaction.user.mention)
        await interaction.response.send_message(response_msg, ephemeral=True)
        output = await api_call(API_URL_VIDAR, {"question": question})
        await send_discord_message(interaction, output)
    except Exception as e:
        print(f"Error in vidar command: {e}")
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.slash_command(name="avatar", description="Create a psychographic client avatar")
async def avatar(interaction: disnake.ApplicationCommandInteraction, details: str):
    try:
        response_msg = random.choice(RESPONSES).format(interaction.user.mention)
        await interaction.response.send_message(response_msg, ephemeral=True)
        avatar_payload = "If your response will be over 1500 characters, send your response in multiple messages. Create a psychographic client avatar based on the following information.  " + details
        avatar_output = await api_call(API_URL_AVATAR, {"question": avatar_payload})
        await send_discord_message(interaction, avatar_output)
    except Exception as e:
        print(f"Error in avatar command: {e}")
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.slash_command(name="content", description="Find the latest newsworthy content for your client avatar")
async def content(interaction: disnake.ApplicationCommandInteraction, details: str):
    try:
        response_msg = random.choice(RESPONSES).format(interaction.user.mention)
        await interaction.response.send_message(response_msg, ephemeral=True)
        content_payload = ("Vidar using the client avatar and / or the following information and find 3 recent (within 72 hours) article, blog, YouTube video, regulatory change, or conversation happening online that relates to my company and client avatar and summarize what that content is about. " + details)
        content_output = await api_call(API_URL_CONTENT, {"question": content_payload})
        await send_discord_message(interaction, content_output)
    except Exception as e:
        print(f"Error in content command: {e}")
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.slash_command(name="script", description="Create a custom video script")
async def script(interaction: disnake.ApplicationCommandInteraction, topic: str):
    try:
        response_msg = random.choice(RESPONSES).format(interaction.user.mention)
        await interaction.response.send_message(response_msg, ephemeral=True)
        script_predefined_text = ("Based on the following information, write a short voice over video script that integrates your business, product, or service into the context of an article, blog, YouTube video, regulatory change, or conversation happening online that relates to your company and client avatar. " + topic)
        script_output = await api_call(API_URL_SCRIPT, {"question": script_predefined_text})
        await send_discord_message(interaction, script_output)
    except Exception as e:
        print(f"Error in script command: {e}")
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.slash_command(name="full_process", description="Full process from avatar creation to video script")
async def full_process(interaction: disnake.ApplicationCommandInteraction, details: str):
    try:
        response_msg = random.choice(RESPONSES).format(interaction.user.mention)
        await interaction.response.send_message(response_msg, ephemeral=True)
        full_process_payload = ("Vidar, I need you to take the following information and create a psychographic client avatar. Then, using that client avatar, find 3 recent (within 72 hours) article, blog, YouTube video, regulatory change, or conversation happening online that relates to my company and client avatar and summarize what that content is about. Finally, write a short voice over video script that integrates your business, product, or service into the context of one of those pieces of content. " + details)
        full_process_output = await api_call(API_URL_CONTENT, {"question": full_process_payload})
        await send_discord_message(interaction, full_process_output)
    except Exception as e:
        print(f"Error in full_process command: {e}")
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
