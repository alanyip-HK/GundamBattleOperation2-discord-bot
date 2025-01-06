import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button
from ms_list import ms_list
import pandas as pd
import json
import random

load_dotenv()
TOKEN = '<replace with your bot token>'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')



@bot.command(name='rotate', help='GBO2の機体ルーレット')
async def rotate_condition_class(ctx,ms_cost:int =commands.parameter(default=500,description="コストを入力してください 0は無制限と意味する　例:350"),contain_ms_level:list=commands.parameter(default=['LV1'],description="回したいレベルを入力してください  例:14"),number_of_player:int=commands.parameter(default=6,description="人数を入力してください　例:3"),ground_or_space:str=commands.parameter(default='G',description="出撃の地形を入力してください　G＝地上、S=宇宙"),ms_type:list=commands.parameter(default=['G','R','S'],description="タイプを入力してください  例:RS  G=汎用、R=強襲、S=支援")):

    player_number = 0
    using_list = []
    for types in ms_type:
        if types == 'G':
            using_list.extend(ms_list.unit['汎用'])
        if types == 'R':
            using_list.extend(ms_list.unit['強襲'])
        if types == 'S':
            using_list.extend(ms_list.unit['支援'])
    df = pd.DataFrame(using_list)
    if ms_cost != 0:
        df.drop(df[df['COST'] != ms_cost].index, inplace = True)
    level_list = []
    for level in contain_ms_level:
        level_list.append("LV"+level)
    df.drop(df[~df.LV.isin(level_list)].index, axis = 0, inplace = True)
    if ground_or_space == 'G':
        df.drop(df[df['GROUND'] != 'TRUE'].index, inplace = True)
    if ground_or_space == 'S':
        df.drop(df[df['SPACE'] != 'TRUE'].index, inplace = True)
    output_json = json.loads(df.to_json(orient='records'))
    #print(df)
    while number_of_player != player_number:
        player_number += 1
        final_choice = random.choice(output_json)
        return_message = f"""
-------------------------------------------------
プレイヤー番号:{player_number}
機体 : {final_choice['MS']}
レベル : {final_choice['LV']}
タイプ : {final_choice['TYPE']}
-------------------------------------------------
"""
        await ctx.send(return_message)



bot.run(TOKEN)
