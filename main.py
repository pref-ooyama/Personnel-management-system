import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Flask (Render維持用)
app = Flask(__name__)
@app.route('/')
def home(): return "Personnel Management System is running!"

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # メンバー情報取得に必須！
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 機能1: チケット管理 ---
@bot.command()
async def ticket(ctx):
    allowed = ["幹部自衛官", "監察課【ID】--Inspector Division"]
    if not any(r.name in allowed for r in ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        return await ctx.send("権限がありません。")
    
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="チケット作成", style=discord.ButtonStyle.primary, custom_id="create_ticket"))
    await ctx.send("相談・申請用のチケットを作成します。", view=view)

# --- 機能2: 身分証照会 ---
@bot.command()
async def info(ctx, member: discord.Member = None):
    target = member or ctx.author
    ignore_list = ["---------------受講済み-------------------", "----------その他/Other---------", "----------所属/Affiliation---------"]
    
    # 有効なロール抽出
    valid_roles = [r.name for r in target.roles if r.name not in ignore_list and r.name != "@everyone"]
    
    rank, dept = "不明", "所属なし"
    for r in valid_roles:
        if "警" in r or "官" in r: rank = r
        elif r != rank: dept = r

    embed = discord.Embed(title=f"【身分証】{target.display_name}", color=0x2c3e50)
    embed.add_field(name="階級", value=rank, inline=True)
    embed.add_field(name="所属", value=dept, inline=True)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.run(os.environ["TOKEN"])
