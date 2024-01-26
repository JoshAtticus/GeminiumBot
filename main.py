from MeowerBot.ext.help import Help as HelpExt
from os import environ as env
import requests
from MeowerBot import Bot, CallBackIds
from MeowerBot.context import Context, Post
from MeowerBot.cog import Cog
from MeowerBot.command import command

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

Themium Commands
- @Geminium theme (style) | Create a Meower theme with Themium
"""
	await ctx.reply(help_message)


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
