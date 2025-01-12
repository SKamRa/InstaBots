from modules.config import BASE_DIR

def setBotId(self):
    with open(f"{BASE_DIR}/data/ids/ids_list.txt", 'r') as ids_list:
        max_id = ids_list.readlines.replace("\n", '')
        if max_id:
            bot_id = max_id + 1
        else:
            bot_id = 0
        
    with open(f"{BASE_DIR}/data/ids/ids_list.txt", 'a') as ids_list:
        ids_list.write(bot_id)