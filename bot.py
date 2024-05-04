import discord
from discord.ext import commands
import os
import sqlite3

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

TOKEN =os.environ['DISCORD_BOT_TOKEN']

conn = sqlite3.connect('discord_bot.db')
cursor = conn.cursor()

@bot.event
async def on_ready():
    print('Bot is ready.')
    await create_users_table()
    await update_database()

@bot.event
async def on_member_join(member):
    role_name = "مفصول من إدارة | IQD"
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        print(f"Gave {member.name} the {role_name} role.")
        await add_user(member.name, member.discriminator)
    else:
        print(f"Role {role_name} not found.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def role_stats(ctx):
    role_name = "مفصول من إدارة | IQD"
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        members_with_role = [member.name for member in ctx.guild.members if role in member.roles]
        await ctx.send(f"The following members have been granted the {role_name} role: {', '.join(members_with_role)}")
    else:
        await ctx.send("Role not found.")

@bot.command()
async def test(ctx):
    await ctx.send("# hi ")

async def create_users_table():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT,
                            discriminator TEXT
                        )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

async def add_user(username, discriminator=None):
    try:
        if discriminator is None:
            discriminator = "0000"
        cursor.execute('''INSERT INTO users (username, discriminator) VALUES (?,?)''', (username, discriminator))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding user: {e}")

async def update_database():
    guild = bot.get_guild(1090472218619813988)
    role_name = "مفصول من إدارة | IQD"
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        for member in guild.members:
            if role in member.roles:
                await add_user(member.name, member.discriminator)

async def close_database():
    conn.close()

bot.run(TOKEN)