start_message = """Added this *chat_id* to list of getters ip change info. 
For more commands use /help"""

help_message = """All available commands:
- /help - get help.
- /start - start command, adds chat_id to list of getters ip change info
- /getip - gets current ip
- /getconfig - gets config [in progress]
"""


def send_ip(ip):
    return "Ip is " + ip


def send_ip_change(ip):
    return "Ip changed. New is: " + ip


def send_config(json):
    return """Config in JSON format: ``` 
""" + json + """```"""
