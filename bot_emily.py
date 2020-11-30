import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

dburl = open('db.txt', "r").read()
token = open("token.txt", "r").read()
client = discord.Client()

cluster = MongoClient(dburl)
db = cluster["bot_emily_db"]
collection = db["bot_emily_collection"]

@client.event
async def on_ready():
		print('We have logged in as {0.user}'.format(client))
		await client.change_presence(activity=discord.Game('I\'m a good bot'))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!hello'):
		await message.channel.send('Hello!')
		await message.delete()

	#Bruh XD Counter
	myquery = { "_id": message.author.id }
	if(collection.count_documents(myquery) == 0):
		if "bruh xd" in message.content.lower():
			post = {"_id": message.author.id, "score": 1}
			collection.insert_one(post)
			await message.channel.send('You now have a balance of 1 bRuH xD!')
	else:
		if "bruh xd" in message.content.lower():
			query = {"_id": message.author.id}
			user = collection.find(query)
			for result in user:
				score = result["score"]
			score = score + 1
			collection.update_one({"_id":message.author.id}, {"$set":{"score":score}})
			await message.channel.send("You now have a balance of %d bRuH xD's!" % (score))
	#Clear RSVP List
	if message.content.startswith("!rsvpclear") and message.author.id == 636041117028319233:
		await message.channel.send("Works lol :D")
		await message.delete()

	if message.content.lower().startswith("!rsvp"):
		
client.run(token)