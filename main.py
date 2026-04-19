import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Flask (RenderでスリープさせないためのWebサーバー機能)
app = Flask(__name__)
@app.route('/')
def home(): return "Personnel Management System is Online."

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # メンバー情報の取得に必要
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} が起動しました。")

# 身分証照会機能
@bot.command()
async def info(ctx, member: discord.Member = None):
    target = member or ctx.author
    
    # 無視する仕切りロール
    ignore_list = [
        "---------------受講済み-------------------", 
        "----------その他/Other---------", 
        "----------所属/Affiliation---------"
    ]
    
    # ロール抽出
    valid_roles = [r.name for r in target.roles if r.name not in ignore_list and r.name != "@everyone"]
    
    rank, dept = "不明", "所属なし"
    for r in valid_roles:
        if "警" in r or "官" in r: rank = r
        elif r != rank: dept = r

    embed = discord.Embed(title=f"【身分証】{target.display_name}", color=0x2c3e50)
    embed.add_field(name="階級", value=rank, inline=True)
    embed.add_field(name="所属", value=dept, inline=True)
    await ctx.send(embed=embed)

# 実行
if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.run(os.environ["TOKEN"])
