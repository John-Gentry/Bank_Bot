import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
import json, requests
import time
import re
import os
import sys
import discord
import logging
from discord.ext import commands
import gspread

#Me, Cooldude, Kobe
authorized_users = ["229086359833280512","226439688330674186","426468000934264853"]

TOKEN = 'NTU2Njk4NjYzODU5MTI2Mjcy.D29hlw.iwZqFlvGM2mheZYoMkg2L4DklCQ'
logging.basicConfig(level=logging.WARNING)
description = '''Bot description here2'''
client = commands.Bot(command_prefix='>', description=description)
def bank_sheets(dis,type):
    from oauth2client.service_account import ServiceAccountCredentials
    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(THIS_FOLDER, 'client_secret.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    clientt = gspread.authorize(creds)
    sh = clientt.open("Bank of Malta")
    shares = sh.worksheet("Ownership")
    if type == "shares":
        disc = shares.find(dis)
        data = shares.row_values(disc.row)
        return data

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@client.event
async def on_ready():
    print('Bot is ready for use')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('>shares'):
        list = bank_sheets(str(message.author.id),"shares")
        msg = "```Discord: <@!"+list[1]+">\nShares: "+list[3]+"```".format(message)
        await message.channel.send(msg)
    if message.content.startswith('>restart'):
        msg = 'Restarting...'.format(message)
        await message.channel.send(msg)
        restart_program()

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

if __name__ == '__main__':
    client.loop.create_task(list_servers())
    client.run(TOKEN)