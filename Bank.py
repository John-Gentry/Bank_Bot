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

@client.event
async def on_ready():
    print('Bot is ready for use')

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