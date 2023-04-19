import discord
from discord.ext import commands, tasks
import core

class AutoDelete(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		self.delete_inactive_tickets.start()
	
	@tasks.loop(minutes = 10)
	async def delete_inactive_tickets(self):
		config = await core.load_config("./config/config.json")
		panel = await core.load_config("./config/panel.json")
		if config["auto-close"] == True:
			panel_opt = panel["options"]
			for opt in panel_opt:
				category_id = opt["category"]
				#Get the category
				category = discord.utils.get(self.bot.get_all_channels(), id = int(category_id))
				#Get the channels in the category
				channels = category.text_channels
				for channel in channels:
					#Get the last message in the channel
					#Check if ticket has user id as it's description
					if channel.name.startswith("ticket-"):
						last_message = [message async for message in channel.history(limit = 1)]
						#Get the time difference between the last message and now
						time_difference = await core.get_time_difference(last_message[0].created_at)
						#If the time difference is greater than the time specified in the config file, delete the channel
						if time_difference > config["auto-close-interval"]:
							await channel.delete()

async def setup(bot):
	await bot.add_cog(AutoDelete(bot))


	
