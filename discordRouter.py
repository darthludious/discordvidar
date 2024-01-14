import os
import aiohttp
import disnake
from disnake.ext import commands

# Environment variables
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
API_URL_VIDAR = os.environ["API_URL_VIDAR"]

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def api_call(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

async def send_discord_message(user, response):
    # Extract the message text from the response dictionary
    message = response.get('text', '')  # Fallback to an empty string if 'text' key is not found

    while message:
        chunk = message[:2000]
        await user.send(chunk)
        message = message[2000:]

# Handle /vidar, @vidar, and DMs to Vidar
async def handle_vidar_request(interaction, message_content):
    response = await api_call(API_URL_VIDAR, {"question": message_content}) 
    await send_discord_message(interaction.user, response)
    await interaction.followup.send("Response sent to your DMs!")

@bot.slash_command(name="vidar", description="Talk to Vidar")
async def vidar_slash_command(interaction: disnake.ApplicationCommandInteraction, message_content: str):
    await interaction.response.defer()
    await handle_vidar_request(interaction, message_content)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
