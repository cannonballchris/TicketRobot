import datetime
import discord
from discord.ext import commands
from views.panel import TicketsPanel, SelectClass
import core
class Ticket(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.views_added = False
	
	@commands.Cog.listener()
	async def on_ready(self):
		if not self.views_added:
			panel_view = TicketsPanel()
			options = await panel_view.load_options()
			if options:
				panel_view.add_item(SelectClass(options))
			self.bot.add_view(panel_view)
			self.bot.add_view(core.ButtonView())
			self.views_added = True


	
	@commands.command(name = "panel", description = "Creates a ticket panel")
	@commands.has_permissions(manage_channels = True)
	async def panel(self, ctx):
		embed = await core.load_panel_embed()
		#embed = discord.Embed(title = "Tickets", description="Please select a category to open ticket.", color = discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
		panel_view = TicketsPanel()
		options = await panel_view.load_options()
		if not options:
			return await ctx.send("There are no options in the panel.json file.")
		panel_view.add_item(SelectClass(options))
		await ctx.send(embed = embed, view = panel_view)

async def setup(bot):
	await bot.add_cog(Ticket(bot))