import discord
from .config import load_config, load_greet_embed
from .button import ButtonView
async def create_ticket(user, category, type):
	overwrites = {
		user.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
		user.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
		user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
	}
	user_name = user.name
	if len(user_name) > 26:
		user_name = user_name[:26]
	channel = await category.create_text_channel(name=f"ticket-{user_name}", topic=str(user.id))
	await channel.edit(overwrites=overwrites)
	data = await load_config("./config/panel.json")
	for val in data["options"]:
		if val["label"] == type:
			roles = val["role"]
			break
	if roles:
		msg = ""
		for role in roles:
			msg += f"<@&{role}>"
		await channel.send(msg)
	embed = await load_greet_embed()
	if embed:
		await channel.send(embed=embed, view = ButtonView())
	

	return channel