import json
import os

def choose_level():
    while True:
        choice = int(input("Choose level: "))
        if choice >= 1 and choice <= 4:
            break
    
    with open(os.path.join(os.getcwd(), 'config.json'), 'r') as config_file:
        config = json.load(config_file)
        
        if choice >= 3:
            config["HIDER_CAN_MOVE"] = True
        else:
            config["HIDER_CAN_MOVE"] = False
    
    with open(os.path.join(os.getcwd(), 'config.json'), 'w') as config_file:
        json.dump(config, config_file, indent=4)
    
    return config, choose_map(choice)

def choose_map(level):
    folder = 'level' + str(level)
    map_list = os.listdir(os.path.join(os.getcwd(), folder))
    
    for i in range(0, len(map_list)):
        print(f"{i + 1} {map_list[i]}")
        
    while True:
        choice = int(input("Choose a map: "))
        if choice >= 1 and choice <= len(map_list):
            break
        
    path = map_list[choice - 1]
    
    return os.path.join(folder, path)