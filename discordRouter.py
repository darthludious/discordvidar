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

@bot.event
async def on_message(message: discord.Message):
    # Check if the message is a DM and not sent by the bot
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        try:
            output = requests.post(API_URL_VIDAR, json={"question": message.content}, timeout=30).json()
            await message.author.send(output["question"])  # Send the response as a DM
        except Exception as e:
            await message.author.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="vidar", description="Vidar QnA")
async def vidar(interaction: discord.Interaction, question: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        output = requests.post(API_URL_VIDAR, json={"question": question}, timeout=30).json()
        await interaction.user.send(output["question"])  # Send the response as a DM
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="avatar", description="Create a psychographic client avatar")
async def avatar(interaction: discord.Interaction, details: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        payload_question = "Create a psychographic client avatar based on the following information " + details
        output = requests.post(API_URL_AVATAR, json={"question": payload_question}, timeout=30).json()
        await interaction.user.send(output["question"])
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="script", description="Create a custom video script")
async def script(interaction: discord.Interaction, topic: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        predefined_text = "... predefined text ... Details: "
        payload_question = predefined_text + topic
        output = requests.post(API_URL_SCRIPT, json={"question": payload_question}, timeout=30).json()
        await interaction.user.send(output["question"])
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="content", description="Find the latest newsworthy content for your client avatar")
async def content(interaction: discord.Interaction, details: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        payload_question = "Vidar using the client avatar and / or the following information ... " + details
        output = requests.post(API_URL_CONTENT, json={"question": payload_question}, timeout=30).json()
        await interaction.user.send(output["question"])
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="full_process", description="Creates Avatar, Finds Content, Writes Script")
async def full_process(interaction: discord.Interaction, details: str):
    try:
        # Execute avatar logic
        avatar_payload = {
            "question": "Create a psychographic client avatar based on the following information " + details
        }
        avatar_output = requests.post(API_URL_AVATAR, json=avatar_payload, timeout=30).json()
        await interaction.user.send(avatar_output["question"])  # Send avatar response to user

        # Use avatar_output in content logic
        content_payload = {
            "question": "Vidar using the client avatar and / or the following information ... " + avatar_output["question"]
        }
        content_output = requests.post(API_URL_CONTENT, json=content_payload, timeout=30).json()
        await interaction.user.send(content_output["question"])  # Send content response to user

        # Use content_output in script logic
        script_predefined_text = "... predefined text ... Details: "
        script_payload = {
            "question": script_predefined_text + content_output["question"]
        }
        script_output = requests.post(API_URL_SCRIPT, json=script_payload, timeout=30).json()
        await interaction.user.send(script_output["question"])  # Send script response to user

    except Exception as e:
        await interaction.user.send("Oops! Something went wrong during the full process. Please try again later.")

# Start the bot
bot.run(DISCORD_BOT_TOKEN)

