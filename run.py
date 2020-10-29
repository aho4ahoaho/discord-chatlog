import discord
import datetime
import os
import sys

try:
    _ = sys.argv[1]
except:
    exit()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game("情報開示請求に反応してチャットのログを開示します。"))
    if not os.path.isdir("logs"):
        os.mkdir("logs")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    filepath = "logs/"+str(message.channel.id)+".txt"
    with open(filepath, mode='a') as f:
        f.write("{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+" "+message.author.name+"@"+message.author.avatar+":"+message.content+"\n")
    
    if message.content.startswith("情報開示請求"):
        await message.channel.send(content="{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+"時点でのチャットログ",file=discord.File(os.getcwd()+"/"+filepath,filename=message.channel.name+".txt"),delete_after=300)


client.run(sys.argv[1])