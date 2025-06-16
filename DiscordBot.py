import discord
from discord.ext import tasks, commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("token")
CHANNEL_ID = 1383909771702435933  # your channel ID as int

bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())

GOOGLE_SHEET_API = "https://script.google.com/macros/s/AKfycbwoDvO04YAIWixvBIb1-rsTl_vG1_qhRLD4qUtLD8ilYB92Xr5jAiBEvFUdYXr3gPwf/exec"
                        

last_job = None
sent_jobs = set()
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    check_for_new_jobs.start()

@tasks.loop(seconds=10)
async def check_for_new_jobs():
    global last_job
    global sent_jobs
    try:
        response = requests.get(GOOGLE_SHEET_API)
        job_list = response.json()
        channel = bot.get_channel(CHANNEL_ID)
        for job_data in job_list:
            current_job = f"{job_data['jobTitle']} - {job_data['company']}"
            if current_job not in sent_jobs and job_data.get("jobLink"):
                sent_jobs.add(current_job)
                await channel.send(
                    f"📢 New job posted!\n{current_job}\nLocation: {job_data['location']}\nLink: {job_data['jobLink']}"
                )

    except Exception as e:
        print(f"Error fetching jobs: {e}")

        

bot.run(DISCORD_TOKEN)
