import discord
from discord.ext import tasks, commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("token")
CHANNEL_ID = 1383909771702435933  # your channel ID as int

bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())

GOOGLE_SHEET_API = "https://script.google.com/macros/s/AKfycbySlKkQgbG6uSeLXE_ftU5U4DXFNsee50_jc6QCpozLKrXLVHtL3LFIGGSpXIdosaGB/exec"
                        

last_job = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    check_for_new_jobs.start()

@tasks.loop(seconds=10) #)minutes=1
async def check_for_new_jobs():
    global last_job

    print(last_job)
    try:
        response = requests.get(GOOGLE_SHEET_API)
        print("Raw job data:", response.text)

        job_data = response.json()
        current_job = f"{job_data['jobTitle']} - {job_data['company']}"

  
        if current_job != last_job:
            last_job = current_job
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"📢 New job posted!\n{current_job}\nLocation: {job_data['location']}\nLink: {job_data['jobLink']}")
            else:
                print(f"Channel with ID {CHANNEL_ID} not found")
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        

bot.run(DISCORD_TOKEN)
