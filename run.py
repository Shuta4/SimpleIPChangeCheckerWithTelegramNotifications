import requests
import telebot
import json


"""
Config must be in json format!
Structure:
{
    "save_file_path": "<Path to file where program will save its info>",
    "bot_token": "<Token of your bot>",
    "interact_with": [
        "<chat_id>", "chat_id" <Massive of chat ids with which bot will interact,
        leave it empty if you want your bot to interact with any (!!! be careful, because every user,
        that knows name of your bot, can get your public IP and other information from it!!!)>
    ],
    "proxy": "<SOCKS4/5 proxy in format: "<http/https>:<socks4/socks5>:<proxy_ip>:<proxy_port>" 
        Leave this field empty if you don't want to use proxy>"
}
Config file format may be changed because of additional functionality of bot.
For new info visit: https://github.com/Shuta4/SimpleIPChangeCheckerWithTelegramNotifications
"""

config_file = open(input("Enter path to config file >> "), "r")
config = json.loads(config_file.read())
config_file.close()

if config["save_file_path"] == "":
    print("No save file specified! Stopping...")
    exit(1)

if config["proxy"] != "":
    proxy_string = config["proxy"].lower().split(":", 4)
    telebot.apihelper.proxy = {proxy_string[0]: proxy_string[1] + "://" + proxy_string[2] + ":" + proxy_string[3]}
    print(telebot.apihelper.proxy)
    print("Proxy setup complete!")
else:
    print("No proxy specified!")

if config["bot_token"] != "":
    bot = telebot.TeleBot(config["bot_token"])
else:
    print("No bot token! Stopping...")
    exit(1)


def check_chat_id(chat_id):
    if config["interact_with"]:
        if chat_id not in config["interact_with"]:
            return False
    return True


@bot.message_handler(commands=["start"])
def start_message(message):
    if check_chat_id(message.chat.id):
        bot.send_message(message.chat.id, "Hello, World!")


bot.polling()
