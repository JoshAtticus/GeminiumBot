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


@bot.event
async def login(_token):
    print("Logged in!")


@bot.command(name="ask")
async def ask(ctx: Context, *question: str):
    question = " ".join(question)

    await ctx.reply("Asking Geminium...")

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
