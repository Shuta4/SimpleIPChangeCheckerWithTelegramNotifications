import requests
import json
import saving


def get_ip():
    req = requests.get("https://api.ipify.org?format=json")
    if req.status_code == 200:
        return req.json()["ip"]
    else:
        print("Error in getting ip. Code: " + str(req.status_code))
        return None


def check_ip_change(save_file_name):
    ip = get_ip()
    if ip is not None:
        saves = saving.read_saves(save_file_name)
        if saves["last_ip"] != ip:
            saves["last_ip"] = ip
            saving.write_saves(save_file_name, saves)
            return ip
    return None
