import discord
import datetime
import os
import sys

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game("情報開示請求に反応してチャットのログを開示します。"))
    if not os.path.isdir(os.path.dirname(__file__)+"/logs"):
        os.mkdir(os.path.dirname(__file__)+"/logs")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    filepath = os.path.dirname(__file__)+"/logs/"+str(message.channel.id)+".txt"
    with open(filepath, mode='a') as f:
        if message.author.avatar != None:
            f.write("{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+" "+message.author.name+"@"+message.author.avatar+":"+message.content+"\n")
        else:
            f.write("{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+" "+message.author.name+"@[bot]:"+message.content+"\n")
    
    if message.content.startswith("情報開示請求"):
        await message.channel.send(content="{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+"時点でのチャットログ",file=discord.File(filepath,filename=message.channel.name+".txt"),delete_after=300)


try:
    with open(os.path.dirname(__file__)+"/token","r") as token:
        client.run(token.read())
except:
    try:
        client.run(sys.argv[1])
    except:
        with open(os.path.dirname(__file__)+"/token","a") as token:
            token.write("")
        print("tokenがありません")