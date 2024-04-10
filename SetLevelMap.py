import json

def choose_level():
    while True:
        choice = int(input("Choose level: "))
        if choice >= 1 and choice <= 4:
            break
    
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        
        if choice >= 3:
            config["HIDER_CAN_MOVE"] = True
        else:
            config["HIDER_CAN_MOVE"] = False
    
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
        
    return config