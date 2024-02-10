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
	fileName = "data_ids.json"
	with open(fileName,"r") as file:
		link = json.load(file)
		dictlist = link["channels"]
	if typeCD == "create":
		if cid not in dictlist : dictlist.append(cid)
		else : return 0
	if typeCD == "delete":
		if cid not in dictlist : return 0
		else : dictlist.remove(cid)
	with open(fileName, "w")as file2:
		json.dump(link,file2)
	return "OK"

def check_message(cid : int):
	with open("data_ids.json" , "r") as file:
		channel_ids = json.load(file)
		if cid in channel_ids["channels"] : return 1
		else: return 0

def AiChatbot(message):
	link = f"http://api.brainshop.ai/get?bid=180356&key=6DRvcrqFlApaokis&uid=1&msg={message}"
	response = requests.get(link)
	json_data = json.loads(response.text)
	chatbot = json_data["cnt"]
	return chatbot

@bot.event
async def on_ready():
	os.system('clear')
	print("Bot is on")
	await bot.change_presence(activity=discord.Streaming(name=  "Mirage", url='https://www.twitch.tv/shiv09ds'))
	print(bot.user.id)
	synced = await bot.tree.sync()
	print(f"Synced {len(synced)} command(s)")

@bot.tree.command(name="help",description="Get the information about bot")
async def say2(interaction : discord.Interaction):
	bot_owner = bot.get_user(owner)
	embed = discord.Embed(colour = discord.Colour.random())
	embed.set_author(name=f"{bot_owner.name}",icon_url=bot_owner.avatar,url = "https://discordapp.com/users/866868740942200833")
	embed.add_field(name = "Help message", value="Greetings! This is an AI ChatBot\nTo use this bot you can use [ ``el <Your Message>`` ]\nOr you can set up a particular channel for the bot by using [ ``/set`` ] command\n[ ``/remove`` ] to remove channel for chatbot reply\nIf getting any issue contact [Admin](https://discordapp.com/users/866868740942200833)" ,inline = False)
	await interaction.response.send_message(embed = embed)

@bot.tree.command(name="remove",description="Remove the channel for bot [only admins can use]")
async def remove_channel(interaction : discord.Interaction):
	uid = interaction.user.id
	cid = interaction.channel_id
	if uid == owner or uid == interaction.guild.owner_id:
		response = CreateDelete("delete",cid)
		if response == "OK":
			await interaction.response.send_message("Channel is removed for chatbot")
		else : await interaction.response.send_message("Channel is not set for chatbot")
	else:
		await interaction.response.send_message("You don't have access to the command for more info use ``/help``")

@bot.tree.command(name="set",description="Set the channel for bot[only admins can use]")
async def set_channel(interaction : discord.Interaction):
	uid = interaction.user.id
	cid = interaction.channel_id
	if uid == owner or uid == interaction.guild.owner_id:
		if CreateDelete("create",cid) == "OK":
			await interaction.response.send_message("Channel is set for chatbot")
		else : 
			await interaction.response.send_message("Channel is already set")
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
			
		elif "slap" in second[2:8].lower():
			embed = discord.Embed(colour = discord.Colour.random())
			embed.set_image(url="https://cdn.discordapp.com/attachments/1072752415792697376/1205884543954063432/yuruyuri-akari-kyoko-anime-slap-fcacgc0edqhci6eh-264118416.gif?ex=65d9fe7f&is=65c7897f&hm=2c4c8bed48b003fa146627918925a0de1569cbfa75a3e225bf32b91da435ec13&")
			embed.set_author(name="slap")
			await ctx.reply(embed= embed)
		else:
			await ctx.reply(AiChatbot(second[2:]))
		

	elif check_message(channel_id):
		chat = AiChatbot(ctx.content)
		await ctx.reply(chat)



bot.run(os.getenv("token"))
