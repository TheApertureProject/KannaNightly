import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import json
import os

with open('./config.json', 'r') as cjson:
    config = json.load(cjson)

DB_USERNAME = os.environ["DBUSERNAME"]
DB_PASSWORD = os.environ["DBPASSWORD"]

client = MongoClient(f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@kanna-mgpcj.mongodb.net/test?retryWrites=true&w=majority")
db = client.profiles

class Datacom(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def register(self, ctx):
        z = discord.Embed(title = "<a:loading:684031670520643640> Creating your profile")
        y = await ctx.send(embed = z)

        playerid = ctx.author.id

        user1 = db.profiles.find_one({'ui' : playerid})

        if user1 is not None:
            a = discord.Embed(title="⚠️ You've already created a neko-profile.")
            await y.edit(embed=a)

        else:
            UNAME = ctx.author.name
            UDESC = "I'm a pretty chill person !"
            UMONEY = 1000
            ULEVEL = 1

            profile = {'ui' : playerid,
            'ud' : UDESC,
            'um' : UMONEY,
            'ul' : ULEVEL,
            }

            db.profiles.insert_one(profile)

            a = f"""`{UDESC}`
            Balance : {UMONEY} <:nekocoins:689129268135067648>
            Level : {ULEVEL}"""

            e = discord.Embed(title = "✅ Neko-profile created !", color = 0x16c60c)
            e.add_field(name = f"**{UNAME}**'s profile", value = a)
            e.set_footer(text = "Tip : edit your description by typing 'nya desc <Description>' !")

            await y.edit(embed = e)

    @commands.command()
    async def profile(self, ctx):
        z = discord.Embed(title = "<a:loading:684031670520643640> Loading your profile")
        y = await ctx.send(embed = z)

        playerid = ctx.author.id

        user1 = db.profiles.find_one({'ui' : playerid})

        if user1 is None:
            a = discord.Embed(title="❌ This profile doesn't exist.")
            await y.edit(embed=a)

        else:
            UNAME = ctx.author.name
            UDESC = user1["ud"]
            UMONEY = user1["um"]
            ULEVEL = user1["ul"]

            a = f"""`{UDESC}`
            Balance : {UMONEY} <:nekocoins:689129268135067648>
            Level : {ULEVEL}"""

            e = discord.Embed(title=f"{playerid}'s neko-profile", description=a)

            await y.edit(embed=e)


def setup(bot):
    bot.add_cog(Datacom(bot))
