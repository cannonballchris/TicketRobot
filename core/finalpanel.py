import discord
from .config import load_config
class ClosingPanel(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		self.add_item(DeleteButton())
		self.add_item(TranscriptButton())
	

class DeleteButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style = discord.ButtonStyle.red, label = "Delete", custom_id = "delete")
	
	async def callback(self, interaction:discord.Interaction):
		#Checks will be placed here
		config = await load_config("./config/config.json")
		if config["staff_roles"] != []:
			for role in config["staff_roles"]:
				if role in [r.id for r in interaction.user.roles]:
					break
			else:
				return await interaction.response.send_message("You are not allowed to delete this ticket.", ephemeral = True)
		#Delete ticket 
		await interaction.channel.delete(reason="Deletion of ticket carried out by admin.")

class TranscriptButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style = discord.ButtonStyle.green, label = "Transcript", custom_id = "transcript")
	
	async def callback(self, interaction:discord.Interaction):
		#Checks will be placed here
		config = await load_config("./config/config.json")
		if config["staff_roles"] != []:
			for role in config["staff_roles"]:
				if role in [r.id for r in interaction.user.roles]:
					break
			else:
				return await interaction.response.send_message("You are not allowed to delete this ticket.", ephemeral = True)
		#Send transcript
		await interaction.response.send_message("Transcript will be sent here.")

