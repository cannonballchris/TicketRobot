import json
import discord

async def load_config(file):
	with open(file, "r", encoding="utf-8") as f:
		data = json.load(f)
	return data

async def load_greet_embed():
	with open("./config/embed.json", "r", encoding="utf-8") as f:
		data = json.load(f)
		try:
			embed_dict = data["greet_embed"]
			if embed_dict["color"]:
				embed_dict["color"] = int(embed_dict["color"][1:], 16)
			embed = discord.Embed.from_dict(embed_dict)
			return embed
		except Exception as e:
			print(e)
			return None

async def load_panel_embed():
	with open("./config/embed.json", "r", encoding="utf-8") as f:
		data = json.load(f)
		try:
			embed_dict = data["panel_embed"]
			if embed_dict["color"]:
				embed_dict["color"] = int(embed_dict["color"][1:], 16)
			embed = discord.Embed.from_dict(embed_dict)
			return embed
		except Exception as e:
			print(e)
			return None

