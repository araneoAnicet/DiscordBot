import discord
from discord.ext import commands
from config import *
import apiai
import json
from time import sleep, asctime, time
from random import randint


Client = discord.Client()
bot = commands.Bot(command_prefix='?', description=bot_description)


def gen_names():
    nicknames = []
    with open('nick_generator.txt', mode='r', encoding='utf-8') as rem:
        for line in rem:
            nicknames.append(line.split('\n'))
    nicknames = list(map(lambda i: nicknames[i][0], range(len(nicknames))))
    return nicknames  # returns a list with the nicknames from the .txt file


def msg_neural_gen(input_text):  # generates the message using NeuralNetwork
    df = apiai.ApiAI(apiai_token).text_request()
    df.lang = apiai_lang  # language
    df.session_id = apiai_session  # session id
    df.query = input_text
    response_json = json.loads(df.getresponse().read().decode('utf-8'))  # cover out the json file
    response = response_json['result']['fulfillment']['speech']  # response = the text of response message
    return response


def appeal_check(msg):
    splited_content = msg.content.split('>')
    if splited_content[0] == bot_appeal_prefix:
        return True
    return False




@bot.event
async def on_ready():
    print('>>> Bot has connected to the Discord')

@bot.event
async def on_member_join(member):
    '''Renames the new members'''
    booked_names = list(map(lambda j: j.display_name, [i for i in bot.get_all_members()]))
    new_name = gen_names()[randint(0, len(gen_names()))]  # takes a random name from the namelist
    iteration_start_time = time()
    while booked_names.count('Пидор ' + new_name) >= 1:  # if there's already a member with this name
        if time() - iteration_start_time >= 15:
            print('>>> ' + bot_rename_error)
            new_name = 'ERROR'
            break
        new_name = gen_names()[randint(0, len(gen_names()))]  # generate the name again
    await bot.change_nickname(member, 'Пидор ' + new_name)  # changes user's nickname on the server
    print('>>> ' + member.name + ' was renamed into the ' + new_name, ' congratulations!')


@bot.event
async def on_message(msg):
    '''Response by the DialogFlow neural network'''
    print(msg.author.display_name + ': ' + msg.content + ':  ' + asctime())
    global message_update
    message_update = ''
    if msg and message_update != msg.id and msg.author.id != '479359716095688708' and \
            reserved_messages.count(msg.content) == 0 and msg.content[0] != '@' and appeal_check(msg):
        response = msg_neural_gen(msg.content)
        if response:
            sleep(len(response) // 15)
            await bot.send_message(msg.channel, response)
            message_update = msg.id
            print('>>> Responsed!')


bot.run(bot_token)  # runs the bot
