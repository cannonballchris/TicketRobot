import asyncio
import json
import discord
from .config import load_config
from .finalpanel import ClosingPanel
class ButtonView(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		#Checks will be added here later
		self.add_item(CloseButton())
		self.add_item(AddUserButton())
		self.add_item(RemoveUser())
		with open("./config/config.json", "r", encoding="utf-8") as file:
			data = json.load(file)
		if data["claim"]:
			self.add_item(ClaimButton())

class CloseButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style = discord.ButtonStyle.red, label = "Close", custom_id = "close", emoji="🔒")
	
	async def callback(self, interaction:discord.Interaction):
		#Check for staff etc will be added here later.
		config = await load_config("./config/config.json")
		if config["allow-user-ticket-closing"] != True:
			if interaction.user.id == int(interaction.message.channel.topic):
				return await interaction.response.send_message("You are not allowed to close this ticket.", ephemeral = True)

			#lock the channel
		user = interaction.guild.get_member(int(interaction.message.channel.topic))
		overwrites = {
			interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
			interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
		}
		if user:
			overwrites[user] = discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False)
		await interaction.message.channel.edit(overwrites=overwrites)
		await interaction.response.send_message("This ticket has been closed.", ephemeral = True)
		await interaction.followup.edit_message(message_id = interaction.message.id, view = None)
		embed = discord.Embed(title = "This ticket is now closed.")
		embed.set_footer(text = f"Closed by {interaction.user}")
		await interaction.channel.send(embed = embed, view=ClosingPanel())

class AddUserButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style = discord.ButtonStyle.green, label = "Add User", custom_id = "adduser", emoji = "👤")
	
	async def callback(self, interaction:discord.Interaction):
		if interaction.user.id == int(interaction.message.channel.topic):
			return await interaction.response.send_message("You are not allowed to add members to this ticket. Ask a staff to do so.", ephemeral = True)
		#Send a message to the user asking for the user id.
		await interaction.response.send_message("Please send the user id or mention the user.")
		#Wait for the user to send a message.
		def check(m):
			return m.author == interaction.user and m.channel == interaction.channel
		try:
			msg = await interaction.client.wait_for("message", check=check, timeout=60)
		except asyncio.TimeoutError:
			await interaction.channel.send("You took too long to respond.", ephemeral = True)
		if msg.content.isdigit():
			user_id = int(msg.content)
		else:
			user_id = msg.mentions[0].id
		#Checks will be added here.
		#Add the user to the ticket.
		user = interaction.guild.get_member(user_id)
		ticket_owner = interaction.guild.get_member(int(interaction.message.channel.topic))
		if user:
			overwrites = {
				interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
				interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
				interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
				user : discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
			}
			if ticket_owner:
				overwrites[ticket_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
			await interaction.message.channel.edit(overwrites=overwrites)
			await interaction.followup.send(f"{user.mention} has been added to the ticket.", ephemeral = True)
		else:
			await interaction.followup.send("The user was not found.", ephemeral = True)

class ClaimButton(discord.ui.Button):
	def __init__(self):
		super().__init__(style = discord.ButtonStyle.green, label = "Claim", custom_id = "claim", emoji = "🔒")
	
	async def callback(self, interaction:discord.Interaction):
		#Checks for staff will be added later
		if interaction.user.id == int(interaction.message.channel.topic):
			return await interaction.response.send_message("You are not allowed to claim this ticket. Only a staff member can claim it.", ephemeral = True)
		#Claim the ticket
		overwrites = {
			interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
			interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
			interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
		}
		ticket_owner = interaction.guild.get_member(int(interaction.message.channel.topic))
		if ticket_owner:
			overwrites[ticket_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
		await interaction.message.channel.edit(overwrites=overwrites)
		await interaction.response.send_message("You have claimed this ticket.", ephemeral = True)
		embed = discord.Embed(title = f"{interaction.user.name} has claimed this ticket.")
		await interaction.channel.send(embed = embed)

class RemoveUser(discord.ui.Button):
	def __init__(self):
		super().__init__(style = discord.ButtonStyle.red, label = "Remove User", custom_id = "removeuser", emoji = "👤")
	
	async def callback(self, interaction:discord.Interaction):
		if interaction.user.id == int(interaction.message.channel.topic):
			return await interaction.response.send_message("You are not allowed to remove members from this ticket. Ask a staff to do so.", ephemeral = True)
		#Send a message to the user asking for the user id.
		await interaction.response.send_message("Please send the user id or mention the user.")
		#Wait for the user to send a message.
		def check(m):
			return m.author == interaction.user and m.channel == interaction.channel
		try:
			msg = await interaction.client.wait_for("message", check=check, timeout=60)
		except asyncio.TimeoutError:
			await interaction.channel.send("You took too long to respond.", ephemeral = True)
		if msg.content.isdigit():
			user_id = int(msg.content)
		else:
			user_id = msg.mentions[0].id
		#Checks will be added here.
		#Remove the user from the ticket.
		user = interaction.guild.get_member(user_id)
		ticket_owner = interaction.guild.get_member(int(interaction.message.channel.topic))
		if user:
			overwrites = {
				interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
				interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
				interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
				user : discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False)
			}
			if ticket_owner:
				overwrites[ticket_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
			await interaction.message.channel.edit(overwrites=overwrites)
			await interaction.followup.send(f"{user.mention} has been removed from the ticket.", ephemeral = True)
		else:
			await interaction.followup.send("The user was not found.", ephemeral = True)

