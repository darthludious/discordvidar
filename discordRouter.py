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
CHANNEL_ID = 1166731466676379729

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def api_call(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

async def send_discord_message(channel, message):
    while message:
        chunk = message[:2000]
        await channel.send(chunk)
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
    await send_discord_message(interaction.channel, response)

@bot.slash_command(name="vidar", description="Talk to Vidar")
async def vidar_slash_command(interaction: disnake.ApplicationCommandInteraction, message_content: str):
    await interaction.response.defer()
    await handle_vidar_request(interaction, message_content)

@bot.slash_command(name="avatar", description="Create a psychographic client avatar")
async def avatar(
    interaction: disnake.ApplicationCommandInteraction,
    details: str = commands.param(description="Provide details about your company, target market, or website."),
):
    await interaction.response.defer()
    avatar_output = await fetch_avatar(details)
    await send_discord_message(interaction.channel, avatar_output)
    await interaction.followup.send("Response sent!") 

@bot.slash_command(name="content", description="Find the latest newsworthy content")
async def content(
    interaction: disnake.ApplicationCommandInteraction,
    details: str = commands.param(description="Provide avatar, or target market"),
):
    await interaction.response.defer()
    content_output = await fetch_content(details)
    await send_discord_message(interaction.channel, content_output)
    await interaction.followup.send("Response sent!")

@bot.slash_command(name="script", description="Create a custom voice-over video script")
async def script(
    interaction: disnake.ApplicationCommandInteraction,
    topic: str = commands.param(description="Provide an article and your client avatar."),
):
    await interaction.response.defer()
    script_output = await fetch_script(topic)
    await send_discord_message(interaction.channel, script_output)
    await interaction.followup.send("Response sent!")

@bot.slash_command(name="full_process", description="Full process from avatar creation to video script")
async def full_process(
    interaction: disnake.ApplicationCommandInteraction,
    details: str = commands.param(description="Provide details about your company, target market, or website."),
):
    await interaction.response.defer()
    avatar_output = await fetch_avatar(details)
    content_output = await fetch_content(avatar_output)
    script_output = await fetch_script(content_output)
    await send_discord_message(interaction.channel, script_output)
    await interaction.followup.send("Response sent!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    send_message.start()  # Start the loop
    await send_message()  # Call the function immediately

@tasks.loop(hours=6)
async def send_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        details = (
            "Context: Here is the following client avatar to base your search on."
            "Sophia, the Strategic Marketer"
            "Demographics:"
            "Age: 35"
            "Gender: Female"
            "Location: Urban area, United States"
            "Occupation: Marketing Manager"
            "Income: Above average"
            "Psychographics:"
            "Values: Creativity, innovation, and efficiency."
            "Personality: Analytical, detail-oriented, and goal-driven."
            "Interests: Marketing trends, data analytics, storytelling, and professional development."
            "Buying Motivations:"
            "Seeks video production services that effectively communicate brand stories and engage target audiences."
            "Values high-quality videos that align with marketing objectives."
            "Willing to invest in videos that deliver value and drive business growth."
            "Buying Concerns:"
            "Skeptical of video production companies without a strong portfolio or case studies."
            "Worries about investing in videos that do not generate measurable results or ROI."
            "Media Consumption:"
            "Actively consumes industry blogs, follows marketing influencers on social media platforms."
            "Engages in webinars, conferences, and workshops to stay updated on the latest marketing strategies and trends."
            "Brand Interactions:"
            "Appreciates video production companies that offer a strategic approach and understand marketing goals."
            "Values clear communication, timely delivery, and professional collaboration."
            "Looks for post-production support, such as video optimization and analytics."
            "Objective: Find 3-5 recent trending media from different sources and topics that would engage Sophia, the Strategic Marketer."
            "Please provide the links and a short summary for each."
            "Constraints: ONLY RESPOND WITH THE LINKS & SUMMARY INFORMATION, DO NOT COMMENT, INTRODUCE, OR CONCLUDE."

        )

        # Make an API call to Vidar
        response = await api_call(API_URL_VIDAR, {"question": details})
        
        # Check if the response is valid and contains the expected data
        if response and "answer" in response and isinstance(response["answer"], str):
            # Send the response to the Discord channel
            await send_discord_message(channel, response["answer"])
        else:
            await channel.send("There was an issue processing the request. Please try again later.")
    else:
        print("Channel not found")

# Start the bot
bot.run(DISCORD_BOT_TOKEN)


