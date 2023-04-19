import os
import discord
from discord.ext import commands

# The error codes:
# 01 : Failed to load cog
class TicketBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="!", intents=discord.Intents.all(), case_insensitive=True)
	
	async def setup_hook(self) -> None:
		for filename in os.listdir("./cogs"):
			if filename.endswith(".py"):
				try:
					await self.load_extension(f"cogs.{filename[:-3]}")
				except Exception as e:
					print(f"ERROR 01 | {e}")
	
	async def on_ready(self):
		print(f"Logged in as {self.user} ({self.user.id})")
		#Set activity to watching support
		await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="support"))
