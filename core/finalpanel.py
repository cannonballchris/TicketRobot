import discord
from .config import load_config, load_greet_embed
import json
import chat_exporter
import io
class ClosingPanel(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		self.add_item(DeleteButton())
		self.add_item(TranscriptButton())
		with open("./config/config.json", "r", encoding="utf-8") as file:
			data = json.load(file)
		if data["allow-reopening"]:
			self.add_item(ReopenButton())

class DeleteButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style = discord.ButtonStyle.red, label = "Delete", custom_id = "delete", emoji="🗑️")
	
	async def callback(self, interaction:discord.Interaction):
		#Checks will be placed here
		config = await load_config("./config/config.json")
		if config["staff_roles"] != []:
			for role in config["staff_roles"]:
				if role in [r.id for r in interaction.user.roles]:
					break
			else:
				return await interaction.response.send_message("You are not allowed to delete this ticket.", ephemeral = True)
		await interaction.response.defer()
		if config["transcript-logs"] == True:
			transcript_channel_id = config["transcript-channel"]
			#Get the channel
			channel = interaction.guild.get_channel(transcript_channel_id)
			if channel != None:
				transcript = await chat_exporter.export(interaction.channel)
				if not transcript:
					return
				transcript_file = discord.File(io.BytesIO(transcript.encode()), filename="transcript.html")
				embed = discord.Embed(title = f"Transcript for {interaction.channel.name}", color = discord.Color.green())
				await channel.send(embed=embed, file=transcript_file)
				#Delete ticket 
		await interaction.channel.delete(reason="Deletion of ticket carried out by admin.")

class TranscriptButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style = discord.ButtonStyle.green, label = "Transcript", custom_id = "transcript", emoji="📝")
	
	async def callback(self, interaction:discord.Interaction):
		#Checks will be placed here
		config = await load_config("./config/config.json")
		if config["staff_roles"] != []:
			for role in config["staff_roles"]:
				if role in [r.id for r in interaction.user.roles]:
					break
			else:
				return await interaction.response.send_message("You are not allowed to generate transcript for this ticket.", ephemeral = True)
		#Send transcript
		await interaction.response.defer()
		transcript = await chat_exporter.export(interaction.channel)
		if not transcript:
			await interaction.followup.send(":x: No transcript could be generated. Try again.", ephemeral=True)
		else:
			transcript_file = discord.File(io.BytesIO(transcript.encode()), filename="transcript.html")
			await interaction.followup.send(":white_check_mark: Transcript created.", ephemeral=True)
			await interaction.channel.send("Here is the transcript of this ticket.", file=transcript_file)
			

class ReopenButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style=discord.ButtonStyle.green, label="Reopen", custom_id="reopen", emoji="🔓")
	
	async def callback(self, interaction: discord.Interaction):
		user = interaction.guild.get_member(int(interaction.message.channel.topic))
		if user is None:
			return await interaction.response.send_message("User not found.", ephemeral=True)
		#Checks will be placed here
		config = await load_config("./config/config.json")
		if config["staff_roles"] != []:
			for role in config["staff_roles"]:
				if role in [r.id for r in interaction.user.roles]:
					break
			else:
				return await interaction.response.send_message("You are not allowed to delete this ticket.", ephemeral = True)
		#Reopen ticket
		overwrites = {
			interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
			interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
			user: discord.PermissionOverwrite(read_messages=True)
		}
		await interaction.channel.edit(overwrites=overwrites, reason="Reopening of ticket carried out by admin.")
		await interaction.message.edit(view=None)
		await interaction.response.send_message("Ticket reopened.", ephemeral=True)
		from .button import ButtonView
		embed = await load_greet_embed()
		if embed:
			await interaction.channel.send(embed=embed, view = ButtonView())
