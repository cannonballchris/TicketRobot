import json
import discord
from discord import ui 
import core
class TicketsPanel(ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	async def load_options(self) -> None:
		with open("./config/panel.json", "r", encoding="utf-8") as f:
			data = json.load(f)
			#Check if the file is empty
			if not data:
				return None
			#Check if the file has more than 25 options
			if len(data["options"]) > 25:
				return None
			#Check if the file has less than 1 option
			if len(data["options"]) < 1:
				return None
			
			option_list = []
			for placeholder in data["options"]:
				option_list.append(discord.SelectOption(label = placeholder["label"], description = placeholder["description"], emoji=placeholder["custom_emoji"]))
			return option_list
	
class SelectClass(ui.Select):
	def __init__(self, options:list):
		self.option = options
		super().__init__(placeholder = "Select a category", options = self.option, custom_id="ticket_panel")
	
	async def callback(self, interaction:discord.Interaction):
		await interaction.response.defer(ephemeral=True)
		data = await core.load_config("./config/panel.json")
		for placeholder in data["options"]:
			if placeholder["label"] == self.values[0]:
				category = placeholder["category"]
				break
		else:
			return await interaction.followup.send("There was an error while selecting the category.", ephemeral=True)
		#Check if category exists.
		category = discord.utils.get(interaction.guild.categories, id = category)
		if not category:
			return await interaction.followup.send("There was an error while selecting the category.", ephemeral=True)
		#Check if the user has a ticket already open.
		for channel in category.channels:
			if channel.topic == str(interaction.user.id):
				await interaction.followup.edit_message(message_id=interaction.message.id, view = self.view)
				return await interaction.followup.send("You already have a ticket open.", ephemeral=True)
			
		#Create the ticket channel.
		try:
			channel = await core.create_ticket(interaction.user, category, self.values[0])
			await interaction.followup.send(f"Created a ticket <#{channel.id}>", ephemeral=True)
			await interaction.followup.edit_message(message_id=interaction.message.id, view = self.view)
		except Exception as e:
			await interaction.followup.send(f"There was an error while creating the ticket. {e}", ephemeral=True)