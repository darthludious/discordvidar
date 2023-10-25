import os
import aiohttp
import disnake
from disnake.ext import commands, tasks

# Environment variables
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
API_URL_VIDAR = os.environ["API_URL_VIDAR"]
API_URL_AVATAR = os.environ["API_URL_AVATAR"]
API_URL_CONTENT = os.environ["API_URL_CONTENT"]
API_URL_SCRIPT = os.environ["API_URL_SCRIPT"]

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def api_call(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

async def send_discord_message(interaction, message):
    while message:
        chunk = message[:2000]
        await interaction.send(chunk)
        message = message[2000:]

# Fetch avatar based on the provided details
async def fetch_avatar(details: str):
    return await api_call(API_URL_AVATAR, {"question": details})

# Fetch content based on the avatar
async def fetch_content(avatar_output: str):
    return await api_call(API_URL_CONTENT, {"question": avatar_output})

# Fetch script based on the content
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

# Handle /vidar, @vidar, and DMs to Vidar
async def handle_vidar_request(interaction, message_content):
    response = await api_call(API_URL_VIDAR, {"question": message_content}) 
    await send_discord_message(interaction, response)

@bot.slash_command(name="vidar", description="Talk to Vidar")
async def vidar_slash_command(interaction: disnake.ApplicationCommandInteraction, message_content: str):
    await interaction.response.defer()
    await handle_vidar_request(interaction, message_content)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if bot.user.mentioned_in(message):
        content = message.content.replace(f"<@!{bot.user.id}>", "").strip()
        response_output = await api_call(API_URL_VIDAR, {"question": content})
        await message.channel.send(response_output)
    elif "/vidar" in message.content or isinstance(message.channel, disnake.DMChannel):
        content = message.content.replace("/vidar", "").strip()
        response_output = await api_call(API_URL_VIDAR, {"question": content})
        await message.author.send(response_output)

@bot.slash_command(name="avatar", description="Create a psychographic client avatar")
async def avatar(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    avatar_output = await fetch_avatar(details)
    await send_discord_message(interaction, avatar_output)
    await interaction.followup.send("Response sent!") 

@bot.slash_command(name="content", description="Find the latest newsworthy content for your client avatar")
async def content(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    content_output = await fetch_content(details)
    await send_discord_message(interaction, content_output)
    await interaction.followup.send("Response sent!")

@bot.slash_command(name="script", description="Create a custom video script")
async def script(interaction: disnake.ApplicationCommandInteraction, topic: str):
    await interaction.response.defer()
    script_output = await fetch_script(topic)
    await send_discord_message(interaction, script_output)
    await interaction.followup.send("Response sent!")

@bot.slash_command(name="full_process", description="Full process from avatar creation to video script")
async def full_process(interaction: disnake.ApplicationCommandInteraction, details: str):
    await interaction.response.defer()
    avatar_output = await fetch_avatar(details)
    content_output = await fetch_content(avatar_output)
    script_output = await fetch_script(content_output)
    await send_discord_message(interaction, script_output)
    await interaction.followup.send("Response sent!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    send_message.start()

CHANNEL_ID = 1166731466676379729

@tasks.loop(hours=6)
async def send_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = (
            f"<@!{bot.user.id}> Objective: find the latest trending media that would engage the following client psychographic avatar and provide a short summary of each trending media.\n\n"
            "Sophia, the Strategic Marketer\n\n"
            "Demographics:\n"
            "Age: 35\n"
            "Gender: Female\n"
            "Location: Urban area, United States\n"
            "Occupation: Marketing Manager\n"
            "Income: Above average\n\n"
            "Psychographics:\n"
            "Values: Creativity, innovation, and efficiency.\n"
            "Personality: Analytical, detail-oriented, and goal-driven.\n"
            "Interests: Marketing trends, data analytics, storytelling, and professional development.\n\n"
            "Buying Motivations:\n"
            "Seeks video production services that effectively communicate brand stories and engage target audiences.\n"
            "Values high-quality videos that align with marketing objectives.\n"
            "Willing to invest in videos that deliver value and drive business growth.\n\n"
            "Buying Concerns:\n"
            "Skeptical of video production companies without a strong portfolio or case studies.\n"
            "Worries about investing in videos that do not generate measurable results or ROI.\n\n"
            "Media Consumption:\n"
            "Actively consumes industry blogs, follows marketing influencers on social media platforms.\n"
            "Engages in webinars, conferences, and workshops to stay updated on the latest marketing strategies and trends.\n\n"
            "Brand Interactions:\n"
            "Appreciates video production companies that offer a strategic approach and understand marketing goals.\n"
            "Values clear communication, timely delivery, and professional collaboration.\n"
            "Looks for post-production support, such as video optimization and analytics."
            
            "Constraints: Never start with something like Here are some of the latest trending media that would engage Sophia, the Strategic Marketer. "
            "Never end your message with something like Please note that these are just a few examples of the trending media. Let me know if you would like more information on any specific topic."
            "IMPORTANT: ONLY RESPOND WITH THE INFORMATION, DO NOT COMMENT, INTRODUCE, OR FOLLOW UP"
        )
        await channel.send(message)
    else:
        print("Channel not found")

# Start the bot
bot.run(DISCORD_BOT_TOKEN)


