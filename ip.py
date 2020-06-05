import requests
import json


def get_ip():
    req = requests.get("https://api.ipify.org?format=json")
    if req.status_code == 200:
        return req.json().ip
    else:
        print("Error in getting ip. Code: " + req.status_code)
        return None


def check_ip_change(save_file_name):
    ip = get_ip()
    if ip is not None:
        file = open(save_file_name, "+")
        saves = json.loads(file.read())
        if saves.last_ip != ip:
            saves.last_ip = ip
            if file.writable():
                file.write(json.dumps(saves))
                return ip
        file.close()
    return None
