import datetime
import discord

async def get_time_difference(time):
	now = discord.utils.utcnow()
	difference = now - time
	return difference.total_seconds() / 60