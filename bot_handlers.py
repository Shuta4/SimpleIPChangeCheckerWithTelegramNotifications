import saving
import ip


def check_chat_id(config, chat_id):
    if config["interact_with"]:
        if str(chat_id) not in config["interact_with"]:
            return False
    return True


def text_message_handler(config, bot, message):
    if check_chat_id(config, message.chat.id):
        if message.content_type != "text":
            return False
        if message.text == "/start":
            saving.add_chat_id_to_info_getters_list(config["save_file_path"], message.chat.id)
            bot.reply_to(message, """Added this chat_id to list of getters ip change info. 
For more commands use /help""")
        elif message.text == "/getip":
            bot.reply_to(message, "IP is " + ip.get_ip())
