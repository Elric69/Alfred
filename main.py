import sys
sys.dont_write_bytecode = True
import requests
import os
import json
import discord
from discord.ext.commands import Bot
from keepAlive import keep_alive
keep_alive()
intent = discord.Intents.all()
bot = Bot(command_prefix="!",intents=intent)
owner = 866868740942200833

def CreateDelete(typeCD : str, cid : int):
	with open("channels.json","r") as file:
		link = json.load(file)
	if typeCD == "create":
		link["channels"].append(cid)
	if typeCD == "delete":
		link["channels"].remove(cid)
	with open("channels.json", "w")as file2:
		json.dump(link,file2)

def check(cid : int):
	with open("channels.json" , "r") as file:
		channel_ids = json.load(file)
		if cid in channel_ids["channels"]: return 1
		else: return 0

def AiChatbot(message):
	link = f"http://api.brainshop.ai/get?bid=180356&key=6DRvcrqFlApaokis&uid=1&msg={message}"
	response = requests.get(link)
	json_data = json.loads(response.text)
	chatbot = json_data["cnt"]
	return chatbot

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Streaming(name=  "Mirage", url='https://www.twitch.tv/shiv09ds'))
	print(bot.user.id)
	synced = await bot.tree.sync()
	print(f"Synced {len(synced)} command(s)")

@bot.tree.command(name="help",description="Get the information about bot")
async def say2(interaction : discord.Interaction):
	bot_owner = bot.get_user(owner)
	embed = discord.Embed(colour = discord.Colour.random())
	embed.set_author(name=f"{bot_owner.name}",icon_url=bot_owner.avatar,url = "https://discord.com/users/866868740942200833")
	embed.add_field(name = "Help message", value="Greetings! This is an AI ChatBot\nTo use this bot you can use [ ``el <Your Message>`` ]\nOr you can set up a particular channel for the bot by using [ ``/set`` ] command\n[ ``/remove`` ] to remove channel for chatbot reply\nIf getting any issue contact [Admin](https://discord.com/users/866868740942200833)" ,inline = False)
	await interaction.response.send_message(embed = embed)

@bot.tree.command(name="remove",description="Remove the channel for bot [only admins can use]")
async def remove_channel(interaction : discord.Interaction):
	uid = interaction.user.id
	cid = interaction.channel_id
	if uid == owner:
		CreateDelete("delete",cid)
		await interaction.response.send_message("Channel is removed for chatbot")
	elif uid == interaction.guild.owner_id:
		CreateDelete("delete",cid)
		await interaction.response.send_message("Channel is removed for chatbot")
	else:
		await interaction.response.send_message("You don't have access to the command for more info use ``/help``")

@bot.tree.command(name="set",description="Set the channel for bot[only admins can use]")
async def set_channel(interaction : discord.Interaction):
	uid = interaction.user.id
	cid = interaction.channel_id
	if uid == owner:
		CreateDelete("create",cid)
		await interaction.response.send_message("Channel is set for chatbot")
	elif uid == interaction.guild.owner_id:
		CreateDelete("create",cid)
		await interaction.response.send_message("Channel is set for chatbot")
	else:
		await interaction.response.send_message("You don't have access to the command for more info use ``/help``")


@bot.event
async def on_message(ctx):
	authId = ctx.author.id
	channel_id = ctx.channel.id
	if authId == bot.user.id : pass

	elif ctx.content.lower() == "hi" : await ctx.channel.send("Hello <:emoji_48:1115693431256272917> <:emoji_18:1115652337382465627> ")

	elif ctx.content.lower().startswith("el"):
		second = ctx.content
		if "help" in second[2:8].lower():
			await ctx.reply("Use ``/help`` for help")
		else:
			await ctx.reply(AiChatbot(second[2:]))

	elif check(channel_id):
		chat = AiChatbot(ctx.content)
		await ctx.reply(chat)



bot.run(os.getenv("token"))
