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
        response_msg = random.choice(RESPONSES).format(message.author.mention)
        await message.author.send(response_msg)
        try:
            output = requests.post(API_URL_VIDAR, json={"question": message.content}, timeout=30).json()
            await message.author.send(output)  # Send the response as a DM
        except Exception as e:
            await message.author.send("Oops! Something went wrong. Please try again later.")

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
        payload_question = "Create a psychographic client avatar based on the following information " + details
        output = requests.post(API_URL_AVATAR, json={"question": payload_question}, timeout=30).json()
        await interaction.user.send(output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="script", description="Create a custom video script")
async def script(interaction: discord.Interaction, topic: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        predefined_text = "Based on the following information write a short voice over video script that brings your business, product of service into the narrative with the article, blog, YouTube video, regulatory change, or conversation happening online. Vidar For the video script, use the hook, story, actionable steps format -For the hook, depending on what makes the most sense, use one of these ( ) based on what makes most sense for the context of the article, blog, YouTube video, regulatory change, or conversation happening online. -For the story, take inspiration from the article, blog, YouTube video, regulatory change, or conversation happening online and bring the business into the narrative as a solution. -For the actionable steps, research and provide actionable steps the viewer can use to solve their problem or address their needs. Details: "
        payload_question = predefined_text + topic
        output = requests.post(API_URL_SCRIPT, json={"question": payload_question}, timeout=30).json()
        await interaction.user.send(output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="content", description="Find the latest newsworthy content for your client avatar")
async def content(interaction: discord.Interaction, details: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        payload_question = "Vidar using the client avatar and / or the following information and find 3 recent (within 72 hours) article, blog, YouTube video, regulatory change, or conversation happening online that relates to my company and client avatar and summarize what that content is about. " + details
        output = requests.post(API_URL_CONTENT, json={"question": payload_question}, timeout=30).json()
        await interaction.user.send(output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")


# Start the bot
bot.run(DISCORD_BOT_TOKEN)
