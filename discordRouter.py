import os
import discord
import aiohttp
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

    async def api_call(self, url, payload):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return await response.json()

bot = CustomBot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        try:
            output = await bot.api_call(API_URL_VIDAR, {"question": message.content})
            await message.author.send(output)  # Send the response as a DM
        except Exception as e:
            await message.author.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="vidar", description="Vidar QnA")
async def vidar(interaction: discord.Interaction, question: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        output = await bot.api_call(API_URL_VIDAR, {"question": question})
        await interaction.user.send(output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="avatar", description="Create a psychographic client avatar")
async def avatar(interaction: discord.Interaction, details: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        avatar_payload = "Create a psychographic client avatar based on the following information " + details
        avatar_output = await bot.api_call(API_URL_AVATAR, {"question": avatar_payload})
        await interaction.user.send(avatar_output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="content", description="Find the latest newsworthy content for your client avatar")
async def content(interaction: discord.Interaction, details: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        content_payload = "Vidar using the client avatar and / or the following information and find 3 recent (within 72 hours) article, blog, YouTube video, regulatory change, or conversation happening online that relates to my company and client avatar and summarize what that content is about. " + details
        content_output = await bot.api_call(API_URL_CONTENT, {"question": content_payload})
        await interaction.user.send(content_output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")

@bot.tree.command(name="script", description="Create a custom video script")
async def script(interaction: discord.Interaction, topic: str):
    response_msg = random.choice(RESPONSES).format(interaction.user.mention)
    await interaction.response.send_message(response_msg)
    try:
        script_predefined_text = ("Based on the following information, write a short voice over video script that integrates your business, product, or service into the context of an article, blog, YouTube video, regulatory change, or online conversation. "
      "For the video script, use the hook, story, actionable steps format. In the hook, tailor it to the context of the content. "
      "For the story, draw inspiration from the content, positioning the business as a solution. "
      "For the actionable steps, provide guidance that the viewer can use to address their needs or solve their problem. Details: ")

        script_payload = script_predefined_text + topic
        script_output = await bot.api_call(API_URL_SCRIPT, {"question": script_payload})
        await interaction.user.send(script_output)
    except Exception as e:
        await interaction.user.send("Oops! Something went wrong. Please try again later.")


@bot.tree.command(name="full_process", description="Creates Avatar, Finds Content, Writes Script")
async def full_process(interaction: discord.Interaction, details: str):
    try:
        # Execute avatar logic
        avatar_payload = "Create a psychographic client avatar based on the following information " + details
        avatar_output = await bot.api_call(API_URL_AVATAR, {"question": avatar_payload})
        await interaction.user.send("Avatar: " + avatar_output)

        # Use avatar_output in content logic
        content_payload = "Vidar using the client avatar and / or the following information and find 3 recent (within 72 hours) article, blog, YouTube video, regulatory change, or conversation happening online that relates to my company and client avatar and summarize what that content is about. " + avatar_output
        content_output = await bot.api_call(API_URL_CONTENT, {"question": content_payload})
        await interaction.user.send("Content: " + content_output)

        # Use content_output in script logic
        script_predefined_text = ("Based on the following information, write a short voice over video script that brings your business, product or service into the narrative with the article, blog, YouTube video, regulatory change, or conversation happening online. "
                                  "Vidar For the video script, use the hook, story, actionable steps format. "
                                  "For the hook, depending on what makes the most sense, use one of these ( ) based on the context of the article, blog, YouTube video, regulatory change, or conversation happening online. "
                                  "For the story, take inspiration from the content and bring the business into the narrative as a solution. "
                                  "For the actionable steps, research and provide steps the viewer can use to solve their problem or address their needs. Details: ")
        script_payload = script_predefined_text + content_output
        script_output = await bot.api_call(API_URL_SCRIPT, {"question": script_payload})
        await interaction.user.send("Script: " + script_output)

    except Exception as e:
        await interaction.user.send("Oops! Something went wrong during the full process. Please try again later.")

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
