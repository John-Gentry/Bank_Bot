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
def bank_sheets(dis,type,amount,ppu):
    from oauth2client.service_account import ServiceAccountCredentials
    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(THIS_FOLDER, 'client_secret.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    clientt = gspread.authorize(creds)
    sh = clientt.open("Bank of Malta")
    if type == "shares":
        try: 
            shares = sh.worksheet("Ownership")
            disc = shares.find(dis)
            data = shares.row_values(disc.row)
            return data
        except:
            print("Not share holder")
    if type == "buy":
        buy = sh.worksheet("Market")
        next_line = len(buy.col_values(1))+1
        buy.update_cell(int(next_line),1, dis)
        buy.update_cell(int(next_line),2, amount)
        buy.update_cell(int(next_line),3, ppu)
    if type == "sell":
        sell = sh.worksheet("Market")
        next_line = len(sell.col_values(5))+1
        sell.update_cell(int(next_line),5, dis)
        sell.update_cell(int(next_line),6, amount)
        sell.update_cell(int(next_line),7, ppu)
    if type == "check":
        check = sh.worksheet("Ownership")
        try:
            disc = check.find(dis)
            data = check.row_values(disc.row)
            print(data[3])
            print(amount)
            if int(data[3]) > int(amount):
                return True
            else:
                return False
        except:
            return False
    if type == "buy_market":
        list = []
        x = ""
        market = sh.worksheet("Market")
        user = market.col_values(1)
        amount = market.col_values(2)
        amount = amount[2:]
        ppu = market.col_values(3)
        ppu = ppu[2:]
        user = user[2:]
        print(user)
        for i in range(0,len(user)):
            list.append("User: <@!"+str(user[i])+">"+"   Amount: "+str(amount[i])+"   PPU: "+str(ppu[i]))
        return list
    if type == "sell_market":
        list = []
        x = ""
        market = sh.worksheet("Market")
        user = market.col_values(5)
        amount = market.col_values(6)
        amount = amount[2:]
        ppu = market.col_values(7)
        ppu = ppu[2:]
        user = user[2:]
        print(user)
        for i in range(0,len(user)):
            list.append("User: <@!"+str(user[i])+">"+"   Amount: "+str(amount[i])+"   PPU: "+str(ppu[i]))
        return list
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
        list = bank_sheets(str(message.author.id),"shares",0,0)
        msg = "```Authorized User: <@!"+list[1]+">\nShares: "+list[3]+"\nOwnership %: "+list[5]+"```".format(message)
        await message.channel.send(msg)
    if message.content.startswith('>restart'):
        msg = 'Restarting...'.format(message)
        await message.channel.send(msg)
        restart_program()
    ##############Trading###############
    if message.content.startswith('>buy'):
        id = (message.content.format(message)[5:]).lower()
        id = id.split()
        print(id)
        bank_sheets(str(message.author.id),"buy",id[0],id[1])
        msg = "You have placed a buy order for "+id[0]+" shares at "+id[1]+" PPU.".format(message)
        await message.channel.send(msg)
    if message.content.startswith('>sell'):
        id = (message.content.format(message)[5:]).lower()
        id = id.split()
        print(id)
        if bank_sheets(str(message.author.id),"check",id[0],id[1]) == True:
            bank_sheets(str(message.author.id),"sell",id[0],id[1])
            msg = "You have placed a sell order for "+id[0]+" shares at "+id[1]+" PPU.".format(message)
            await message.channel.send(msg)
        else:
            msg = "You don't have enough shares.".format(message)
            await message.channel.send(msg)
    if message.content.startswith('>market'):
        list1 = bank_sheets(str(message.author.id),"buy_market",0,0)
        list2 = bank_sheets(str(message.author.id),"sell_market",0,0)
        #msg = str(bank_sheets(str(message.author.id),"buy_market",0,0)).format(message)
        #await message.channel.send(msg)
        embed = discord.Embed(title="Bank of Malta share market", description="For all your trading needs", color=0xFF0000)
        #embed.add_field(name="**Bids**", value="Buy orders on the market", inline=False)
        s = ""
        for i in range(0,len(list1)):
            s = s + list1[i]+"\n"
        embed.add_field(name="**Buy orders**", value=s, inline=False)
        s = ""
        for i in range(0,len(list2)):
            s = s + list2[i]+"\n"
        embed.add_field(name="**Sell orders**", value=s, inline=False)
        await message.channel.send(embed=embed)

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