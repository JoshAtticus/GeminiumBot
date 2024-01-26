import requests
from MeowerBot import Bot, CallBackIds
from MeowerBot.context import Context, Post
from MeowerBot.cog import Cog
from MeowerBot.command import command

import logging

from dotenv import load_dotenv # type: ignore

load_dotenv() # type: ignore

from os import environ as env
from MeowerBot.ext.help import Help as HelpExt

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
	
	await ctx.send_msg("Asking Geminium...")
	
	payload = {
		"question": question
	}
	
	response = requests.post("https://geminium.joshatticus.online/api/geminium/ask", json=payload)
	
	if response.status_code == 200:
		await ctx.send_msg(response.text)
	else:
		await ctx.send_msg("Error: Failed to get a response from the API.")
		
@bot.command(name="math")
async def ask(ctx: Context, *question: str):
	question = " ".join(question)
	
	await ctx.send_msg("Asking Geminium Math...")
	
	payload = {
		"question": question
	}
	
	response = requests.post("https://geminium.joshatticus.online/api/geminium/math", json=payload)
	
	if response.status_code == 200:
		await ctx.send_msg(response.text)
	else:
		await ctx.send_msg("Error: Failed to get a response from the API.")


# noinspection PyIncorrectDocstring
@bot.command(name="logs")
async def get_logs(ctx: Context, *args):
	"""
	Arguments:
		start: Optional[int]
		end: Optional[int]

	Formated like this:
		start=...

	@prefix get_logs start=-200 end=-1
	"""
	# start=...
	# end=...
	start = -10
	end = -1
	arg: str
	for arg in args:
		if arg.startswith("start"):
			start = int(arg.split("=")[1])
		elif arg.startswith("end"):
			end = int(arg.split("=")[1])

	with open("debug.log") as logfile:
		logs = logfile.readlines()

	message = await ctx.send_msg("".join(logs[start: end]))
	if not message:
		await ctx.reply("Error: Logs to big for current env")


@bot.command(name="bots")
async def get_bots(ctx: Context):
	await ctx.reply(f"\n {' '.join(list(bot.cache.bots.keys()))}")


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
bot.register_cog(HelpExt(bot, disable_command_newlines=True))
bot.run(env["GBOT_USERNAME"], env["GBOT_PASSWORD"])
