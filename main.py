from io import BytesIO
from MeowerBot.ext.help import Help as HelpExt
from os import environ as env
import requests
from MeowerBot import Bot, CallBackIds
from MeowerBot.context import Context, Post
from MeowerBot.cog import Cog
from MeowerBot.command import command
import platform
import psutil
import sys
import subprocess
import shlex
import base64
import os
import random
from PIL import Image, ImageFilter, ImageEnhance
import logging

from dotenv import load_dotenv  # type: ignore

load_dotenv()  # type: ignore


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("debug.log", encoding='utf8'),
        logging.StreamHandler()
    ]
)

logging.getLogger("websockets.client").setLevel(logging.INFO)
bot = Bot()

trusted_domains = [
    "https://meower.org/",
    "https://http.meower.org/",
    "https://assets.meower.org/",
    "https://forums.meower.org/",
    "https://hedgedoc.meower.org/",
    "https://docs.meower.org/",
    "https://uploads.meower.org/",
    "https://u.cubeupload.com/",
    "https://cubeupload.com/",
    "https://i.ibb.co/",
    "https://media.tenor.com/",
    "https://tenor.com/",
    "https://c.tenor.com/",
    "https://assets.scratch.mit.edu/",
    "https://cdn2.scratch.mit.edu/",
    "https://cdn.scratch.mit.edu/",
    "https://uploads.scratch.mit.edu/",
    "https://cdn.discordapp.com/",
    "https://media.discordapp.net/"
]


@bot.event
async def login(_token):
    print("Logged in!")

@bot.command(name="ask")
async def ask(ctx: Context, *question: str):
    question = " ".join(question)
    
    await ctx.reply("Asking Geminium...")

    # Make a GET request to the integrity validation endpoint
    integrity_response = requests.get("https://geminium.joshatticus.online/api/integrity/validate")

    if integrity_response.status_code == 200:
        integrity_result = integrity_response.json().get("result", False)
        if integrity_result:
            question += "\n\n{\"integrity\": \"true\"}"
        else:
            question += "\n\n{\"integrity\": \"false\"}"
    else:
        await ctx.reply("\nError: Failed to get a response from the Geminium App integrity validation API.")
        return

    question = shlex.quote(question)

    payload = {
        "question": question
    }

    response = requests.post(
        "https://geminium.joshatticus.online/api/geminium/ask", json=payload)

    if response.status_code == 200:
        await ctx.reply("\n\n" + response.text)
    else:
        await ctx.reply("\nError: Failed to get a response from the API.")



@bot.command(name="math")
async def ask(ctx: Context, *question: str):
    question = " ".join(question)
    question = shlex.quote(question)

    await ctx.reply("Asking Geminium Math...")

    payload = {
        "question": question
    }

    response = requests.post(
        "https://geminium.joshatticus.online/api/geminium/math", json=payload)

    if response.status_code == 200:
        await ctx.reply("\n\n" + response.text)
    else:
        await ctx.reply("\nError: Failed to get a response from the API.")

@bot.command(name="teachme")
async def ask(ctx: Context, *question: str):
    question = " ".join(question)
    question = shlex.quote(question)

    await ctx.reply("Asking Geminium Teachme...")

    payload = {
        "question": question
    }

    response = requests.post(
        "https://geminium.joshatticus.online/api/geminium/teachme", json=payload)

    if response.status_code == 200:
        await ctx.reply("\n\n" + response.text)
    else:
        await ctx.reply("\nError: Failed to get a response from the API.")


@bot.command(name="theme")
async def theme(ctx: Context, *question: str):
    question = " ".join(question)
    question = shlex.quote(question)

    await ctx.reply("Creating theme...")

    payload = {
        "style": question
    }

    response = requests.post(
        "https://geminium.joshatticus.online/api/themium/generate", json=payload)

    if response.status_code == 200:
        await ctx.reply("Here's your theme!\n\n`" + response.text + "`\n\n*P.S. want faster theme generation with instant previews? Try https://themium.joshatticus.online*")
    else:
        await ctx.reply("Error: Failed to get a response from the API.")

@bot.command(name="glass")
async def glass(ctx: Context, image_url: str):
    await ctx.reply("Checking image source...")

    if any(domain in image_url for domain in trusted_domains):
        await ctx.reply("Downloading and processing the image...")

        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Process the image (blur and reduce brightness)
            image = Image.open(BytesIO(response.content))

            # Convert image to RGB mode
            image = image.convert("RGB")

            # Blur the image
            blur_radius = 30  # Increase this value for stronger blur
            blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

            # Reduce brightness by 50%
            enhancer = ImageEnhance.Brightness(blurred_image)
            darkened_image = enhancer.enhance(0.5)

            # Save the processed image
            processed_image_path = "processed_image.png"
            darkened_image.save(processed_image_path)

            # Upload the processed image to ImgBB API
            with open(processed_image_path, "rb") as file:
                encoded_image = base64.b64encode(file.read()).decode("utf-8")

            imgbb_api_key = os.getenv("IMGBB_KEY")  # Replace with your ImgBB API key
            upload_url = f"https://api.imgbb.com/1/upload?key={imgbb_api_key}"
            response = requests.post(upload_url, data={"image": encoded_image})

            if response.status_code == 200:
                image_link = response.json()["data"]["image"]["url"]
                await ctx.reply(f"Here's your glass image!\n\n[Glass Image: {image_link}]")
            else:
                await ctx.reply("Error: Failed to upload the processed image.")
                
            # Clean up the processed image file
            os.remove(processed_image_path)
        else:
            await ctx.reply("Error: Failed to download the image.")
    else:
        await ctx.reply("Sorry, that image is not from a trusted domain.")


@bot.command(name="atticus")
async def atticus(ctx: Context, argument: str = None):
    image_directory = "atticuspics"

    if argument == "list":
        image_files = [f for f in os.listdir(image_directory) if f.endswith('.png')]
        await ctx.reply(f"I have **{len(image_files)}** Atticus pictures available.\n\nRun @Geminium atticus (number) to see a specific Atticus picture.")
    else:
        image_number = int(argument) if argument else None

        if image_number is None:
            image_files = [f for f in os.listdir(image_directory) if f.endswith('.png')]
            image_file = random.choice(image_files)
            image_path = os.path.join(image_directory, image_file)
            image_number = image_file.split('.')[0]  # Get the number from the filename
        else:
            image_path = os.path.join(image_directory, f"{image_number}.png")

        if os.path.isfile(image_path):
            await ctx.reply("Uploading the image...")
            
            # Open the image
            with open(image_path, "rb") as file:
                encoded_image = base64.b64encode(file.read()).decode("utf-8")

            imgbb_api_key = os.getenv("IMGBB_KEY")  # Replace with your ImgBB API key
            upload_url = f"https://api.imgbb.com/1/upload?key={imgbb_api_key}"
            response = requests.post(upload_url, data={"image": encoded_image})

            if response.status_code == 200:
                image_link = response.json()["data"]["image"]["url"]
                await ctx.reply(f"Atticus Pic #{image_number}\n\n[Image: {image_link}]")
            else:
                await ctx.reply("Error: Failed to upload the image.")
        else:
            await ctx.reply("Sorry, that image was not found.")



@bot.command(name="help")
async def help_command(ctx: Context):
	help_message = """
Geminium | Created & Maintained by JoshAtticus | An Atticus AI Project

Geminium Commands
- @Geminium ask (question) | Ask Geminium AI a question
- @Geminium math (question) | Ask Geminium Math a question
- @Geminium teachme (question) | Ask Geminium Teachme a question

Themium Commands
- @Geminium theme (style) | Create a Meower theme with Themium

Bot Commands
- @Geminium sysinfo | Check system info

Image Commands
- @Geminium glass (image url) | Gives image glass effect
- @Geminium atticus (image number) | Sends an Atticus picture. A random one is sent if a number is not provided.
"""
	await ctx.reply(help_message)
        
@bot.command(name="sysinfo")
async def sysinfo_command(ctx):
    # System info
    system_info = f"-- System --\n"
    system_info += f"Running on: {platform.system()} {platform.release()}\n"
    system_info += f"Free Memory: {psutil.virtual_memory().available / 1024 / 1024:.2f} MB\n"
    system_info += f"Used Memory: {psutil.virtual_memory().used / 1024 / 1024:.2f} MB\n"
    system_info += f"Python version: {sys.version}\n"

    # Bot info
    bot_info = f"-- Bot --\n"
    build_type = ""
    update_status = ""

    if subprocess.call("ls /etc/systemd/system/geminiumbot.service", shell=True) == 0:
        build_type = "Stable (Deployed)"
    elif subprocess.call("ls .dev", shell=True) == 0:
        build_type = "Development"
    else:
        build_type = "Stable (Undeployed)"

    if subprocess.call("git pull --dry-run | grep -q -v 'Already up-to-date.' && changed=1", shell=True) == 0:
        update_status = "**Update Available**"
    else:
        update_status = "Up to date"

    bot_info += f"Build type: {build_type}\n"
    bot_info += f"Update Status: {update_status}\n"

    # Send the message
    message = f"Geminium for Meower\n\n{system_info}\n{bot_info}"
    await ctx.reply(message)


class Ping(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    @command()
    async def cog_ping(self, ctx: Context):
        await ctx.send_msg("Pong!\n My latency is: " + str(self.bot.latency))
        print(bot.api.headers.get("token"))

    @cog_ping.subcommand()
    async def ping(self, ctx: Context):
        await ctx.send_msg("Pong!\n My latency is: " + str(self.bot.latency))


bot.register_cog(Ping(bot))
bot.run(env["GBOT_USERNAME"], env["GBOT_PASSWORD"])
