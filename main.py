import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from urllib.request import urlopen
import json
import urllib.parse

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="--", case_insensitive=True, intents=intents)


class Person:

  def __init__(self, hashtag, count):
    self.hashtag = hashtag
    self.count = count




@bot.event
async def on_ready():
  print('Connected to bot: {}'.format(bot.user.name))
  print('Bot ID: {}'.format(bot.user.id))


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content.startswith('$title'):
    title = message.content[7:]
    url = "https://us-central1-sandtable-8d0f7.cloudfunctions.net/api/creations/" + title
    response = urlopen(url)
    data_json = json.loads(response.read())
    title = str(data_json['title'])
    await message.channel.send(title)
  if message.content.startswith('$search'):
    reduced_string = message.content[8:]
    search = urllib.parse.quote_plus(reduced_string)
    url = "https://us-central1-sandtable-8d0f7.cloudfunctions.net/api/creations?title=" + search
    response = urlopen(url)
    data_json = json.loads(response.read())
    try:
      entries = data_json[0]
      ttl = entries["data"]["title"]
      id = entries["data"]["id"]
      tid = entries["id"]  #trimmed id
      vts = str(entries["data"]["score"])
      pid = str(entries["data"]["parent_id"])
      chld = str(entries["data"]["children"])
      ts = entries["data"]["timestamp"]
      url = "https://sandspiel.club/#" + tid
      thmb = "https://firebasestorage.googleapis.com/v0/b/sandtable-8d0f7.appspot.com/o/creations%2F" + id + ".png?alt=media"
      embed = discord.Embed(title=ttl, url=url, description=ts)
      embed.set_author(name="Sandspiel Post")
      embed.set_thumbnail(url="https://firebasestorage.googleapis.com/v0/b/sandtable-8d0f7.appspot.com/o/creations%2F" + id + ".png?alt=media")
      embed.add_field(name="Title", value=ttl, inline=True)
      embed.add_field(name="ID", value=id, inline=True)
      embed.add_field(name="Trimmed ID", value=tid, inline=True)
      embed.add_field(name="Score", value=vts, inline=True)
      embed.add_field(name="Parent ID", value=pid, inline=True)
      embed.add_field(name="Child ID", value=chld, inline=True)
      await message.channel.send(embed=embed)
    except IndexError:
      await message.channel.send("No results!")
  if message.content.startswith('$trending'):
    final = ""
    print("test")
    url = "https://us-central1-sandtable-8d0f7.cloudfunctions.net/api/trending/"
    response = urlopen(url)
    data_json = json.loads(response.read())
    print(data_json)
    for i in range(len(data_json)):
      print()
      entries = data_json[i]
      trending = entries["hashtag"] + ": " + entries["htcount"] + " posts"+ "\n"
      final = final + trending
    await message.channel.send(final)
bot.run(TOKEN)
