import json


def read_saves(file_path):
    f = open(file_path, "r")
    saves = json.loads(f.read())
    f.close()
    return saves


def write_saves(file_path, obj):
    f = open(file_path, "w")
    if f.writable():
        f.write(json.dumps(obj))
        f.close()
        return True
    else:
        f.close()
        return False


def get_offset(file_path):
    return read_saves(file_path)["offset"]


def set_offset(file_path, new_offset):
    saves = read_saves(file_path)
    saves["offset"] = new_offset
    write_saves(file_path, saves)


def init_save_file(file_path, last_offset):
    obj = {
        "save_file": True,
        "last_ip": "",
        "ip_info_getters": [],
        "offset": last_offset
    }
    write_saves(file_path, obj)


def add_chat_id_to_info_getters_list(file_path, chat_id):
    saves = read_saves(file_path)
    try:
        saves["ip_info_getters"].index(chat_id)
    except:
        saves["ip_info_getters"].append(chat_id)
        write_saves(file_path, saves)
