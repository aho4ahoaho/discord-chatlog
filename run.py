import discord
import datetime
import os
import sys

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #Activityにbotの使い方を掲示
    await client.change_presence(activity=discord.Game("情報開示請求に反応してチャットのログを開示します。"))
    #logsフォルダがなければ生成
    if not os.path.isdir("logs"):
        os.mkdir("logs")

@client.event
async def on_message(message):
    #自分は無視
    if message.author == client.user:
        return

    #ログがなければ生成、あれば追記
    filepath = "logs/"+str(message.channel.id)+".txt"
    with open(filepath, mode='a') as f:
        #年-月-日 時:分:秒 ユーザーネーム@ユーザーのハッシュ値:メッセージ内容
        f.write("{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+" "+message.author.name+"@"+message.author.avatar+":"+message.content+"\n")
    
    #情報開示請求で始まる文章に反応
    if message.content.startswith("情報開示請求"):
        #日時付きでログファイルをチャンネル名.txtとしてアップロード、5分で自動削除
        await message.channel.send(content="{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+"時点でのチャットログ",file=discord.File(os.getcwd()+"/"+filepath,filename=message.channel.name+".txt"),delete_after=300)

#トークン読み込み、なければ引数、駄目なら警告を返して終了
try:
    with open("token","r") as token:
        client.run(token.read())
except:
    try:
        client.run(sys.argv[1])
    except:
        with open("token","a") as token:
            token.write("")
        print("tokenがありません")