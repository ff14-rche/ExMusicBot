import discord
from discord.ext import commands
import os
import shutil

# Token
token = 'MzQwNTM1OTMwMTYxMDcwMDkw.DFz8Tw.jjpyNZeBiP0k6kz_tIIyON6AfFU'
# デフォルトのフォルダ
config_folder_path = "config/"
# プレイリストのフォルダ
playlist_folder_path = "playlist/"
# デフォルトのファイル名
def_playlist_name = "autoplaylist.txt"
# デフォルトのフルパス
def_playlist_full_path = config_folder_path+def_playlist_name
# 現在のプレイリストのファイル名
current_playlist_file_name = "currentplaylist.txt"
# 上記のフルパス
current_play_list_full_path = config_folder_path+current_playlist_file_name


# Discord
bot = commands.Bot(command_prefix='!')

#@client.event
@bot.event
async def on_ready():
    print("on_ready")

# 現在のプレイリストへ追加
@bot.command()
async def add(str1):
    # フォルダ&ファイルチェック
    if os.path.exists(config_folder_path):
        if os.path.isfile(def_playlist_full_path):
            # プレイリストへ書き込む
            f = open(def_playlist_full_path, 'a')
            f.write(str1+"\n")
            f.close()
            # コピー元のプレイリストにも書き込む
            f = open(current_play_list_full_path, 'r')
            temp = str(f.read())
            f.close()
            f = open(playlist_folder_path+temp, 'a')
            f.write(str1+"\n")
            f.close()
            await bot.say("追加が完了しました。")
        else:
            await bot.say(def_playlist_name + " というファイルは存在しません。")
    else:
        await bot.say(config_folder_path + " というディレクトリは存在しません。")

# 特定のプレイリストへ追加
@bot.command()
async def addTo(str1, str2):
    # フォルダとファイルのチェック
    if os.path.exists(playlist_folder_path):
        path = playlist_folder_path+str1
        if os.path.isfile(path):
            # 指定されたファイルに書き込む
            f = open(path, 'a')
            f.write(str2+"\n")
            f.close()
            await bot.say("追加が完了しました。")
        else:
            await bot.say(str1 + " というファイルは存在しません。")
    else:
        await bot.say(playlist_folder_path + " というディレクトリは存在しません。")

# プレイリストから特定の曲を削除
@bot.command()
async def deleat(str1):
    if os.path.exists(def_playlist_full_path):
        if os.path.isfile(def_playlist_full_path):
            # 現在のプレイリストから削除
            f = open(def_playlist_full_path, 'r')
            temp = f.read()
            f.close()
            new = str(temp).replace(str1+"\n", "")
            f = open(def_playlist_full_path, 'w')
            f.write(new)
            f.close()
            # 上と同じプレイリストを探して削除
            path = config_folder_path+current_playlist_file_name
            f = open(path, 'r')
            current_name = f.read()
            f.close()
            f = open(playlist_folder_path+current_name, 'r')
            temp = f.read()
            f.close()
            new = str(temp).replace(str1+"\n", "")
            f = open(playlist_folder_path+current_name, 'w')
            f.write(new)
            f.close()
            await bot.say(str1 + " をプレイリストから削除しました。")
        else:
            await bot.say(str1 + " というファイルは存在しません。")
    else:
        await bot.say(playlist_folder_path + " というディレクトリは存在しません。")

# プレイリストの中身を表示
@bot.command()
async def show():
    # フォルダ&ファイルチェック
    if os.path.exists(config_folder_path):
        if os.path.isfile(def_playlist_full_path):
            # ファイルの中身を表示
            f = open(def_playlist_full_path)
            data = f.read()
            f.close()
            await bot.say(data)
        else:
            await bot.say(def_playlist_name + " というファイルは存在しません。")
    else:
        await bot.say(config_folder_path + " というディレクトリは存在しません。")

# 特定のプレイリストの中身を表示
@bot.command()
async def showTo(str1):
    # フォルダ&ファイルチェック
    if os.path.exists(playlist_folder_path):
        path = playlist_folder_path+str1
        if os.path.isfile(path):
            # ファイルの中身を表示
            f = open(path)
            data = f.read()
            f.close()
            await bot.say(data)
        else:
            await bot.say(def_playlist_name + " というファイルは存在しません。")
    else:
        await bot.say(config_folder_path + " というディレクトリは存在しません。")

# プレイリストのチェック
@bot.command()
async def check():
    # フォルダチェック
    if os.path.exists(playlist_folder_path):
        # フォルダの中身を表示
        data = os.listdir(playlist_folder_path)
        text = "\n".join(data)
        await bot.say(text)
    else:
        await bot.say(playlist_folder_path + " というディレクトリは存在しません。")

# プレイリストの切り替え
@bot.command()
async def switch(name):
    # フォルダチェック
    if os.path.exists(playlist_folder_path):
        # ファイルチェック
        path = playlist_folder_path+name
        if os.path.isfile(path):
            # 現在のプレイリストを設定
            if os.path.isfile(current_play_list_full_path):
                f = open(current_play_list_full_path, 'w')
                f.write(name)
                f.close()
                await bot.say("!restart")
            else:
                await bot.say(current_playlist_file_name + " というファイルが存在しません。")
            # ファイルをデフォルトの場所にコピー
            shutil.copyfile(path, def_playlist_full_path)
            await bot.say(name + " に切り替えました。")
        else:
            await bot.say(name + " というファイルは存在しません。")
    else:
        await bot.say(playlist_folder_path + " というディレクトリは存在しません。")

# Bot実行
bot.run(token)
