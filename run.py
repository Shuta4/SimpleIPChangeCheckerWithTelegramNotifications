import requests
import telebot
import json
import time
import ip
import saving
import bot_handlers


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

if config["bot_token"] == "":
    print("No bot token! Stopping...")
    exit(1)

bot = telebot.TeleBot(config["bot_token"])

if config["save_file_path"] == "":
    print("No save file specified! Stopping...")
    exit(1)
else:
    try:
        saves = saving.read_saves(config["save_file_path"])
        if not saves["save_file"]:
            saving.init_save_file(config["save_file_path"], bot.last_update_id)
    except:
        saving.init_save_file(config["save_file_path"], bot.last_update_id)

if config["proxy"] != "":
    proxy_string = config["proxy"].lower().split(":", 4)
    telebot.apihelper.proxy = {proxy_string[0].lower(): proxy_string[1] + "://" + proxy_string[2] + ":" + proxy_string[3]}
    print(telebot.apihelper.proxy)
    print("Proxy setup complete!")
else:
    print("No proxy specified!")


# @bot.message_handler(commands=["start"])
# def start_message(message):
#     if check_chat_id(message.chat.id):
#         saving.add_chat_id_to_info_getters_list(config["save_file_path"], message.chat.id)
#         bot.reply_to(message, """Added this chat_id to list of getters ip change info.
#                                             For more commands use /help""")


print("Bot starting...")

# while True:
#     try:
#         bot.polling(none_stop=False)
#     except Exception as e:
#         print("Polling error: " + e)
#         time.sleep(300)

timer = 0
offset = saving.get_offset(config["save_file_path"])
while True:
    try:
        updates = bot.get_updates(offset=offset)
        # Do smthing with updates
        for update in updates:
            bot_handlers.text_message_handler(message=update.message, bot=bot, config=config)
            offset = update.update_id + 1
    except Exception as e:
        print("Get updates error: " + str(e))
        time.sleep(300)
        timer += 300
    # Check if its time to check ip - check it and send msg if it was changed
    if timer >= 600:
        ip = ip.check_ip_change(config["save_file_path"])
        if ip is not None:
            f = open(config["save_file_path"], "r")
            saves = json.loads(f.read())
            f.close()
            chat_ids = saves["ip_info_getters"]
            for chat_id in chat_ids:
                bot.send_message(chat_id, "Ip changed. New is: " + ip)
        timer = 0
    time.sleep(5)
    saving.set_offset(config["save_file_path"], offset)
    timer += 1
