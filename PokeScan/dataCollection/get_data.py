import requests
import shutil, os
import json

cwd = os.getcwd()

def mkdir(path):
    "Creates a directory with the name `path` if it doesn't already exist."
    if not os.path.exists(path):
        os.makedirs(path)

def write_json_to_file(path, jsn):
    "Writes json to a file, creating it if it doesn't already exist."
    with open(path, 'w') as f:
        json.dump(jsn, f)

def read_json_from_file(path):
    "Returns a json object from path."
    with open(path, 'r') as f:
        return json.load(path)

def download_png(url, path):
    "Downloads a picture to path."
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def get_all_sets():
    "Gets all sets from https://api.pokemontcg.io/v1/sets"
    r = requests.get('https://api.pokemontcg.io/v1/sets')
    return r.json()['sets']

def get_set_by_id(id):
    "Gets a specific set by id"
    r = requests.get(f'https://api.pokemontcg.io/v1/sets/{id}')
    return r.json()['set']

def get_card_by_id(id):
    "Gets a card by id."
    r = requests.get(f'https://api.pokemontcg.io/v1/cards/{id}')
    return r.json()['card']

def get_cards_by_set(set):
    "Creates a json file for all the cards in a given set. Input set must be a json object."
    set_id = set['code']
    number_of_cards = set['totalCards']
    
    cards = list()
    
    for card_number in range(1, number_of_cards + 1):
        cards.append(get_card_by_id(f'{set_id}-{card_number}'))
    
    return cards



data_path = os.path.join(cwd, 'data')

mkdir(data_path)

all_sets = get_all_sets()

write_json_to_file(os.path.join(data_path, 'sets.json'), all_sets)

for each_set in all_sets:
    set_folder = os.path.join(data_path, each_set['code'])

    mkdir(set_folder)

    download_png(each_set['symbolUrl'], os.path.join(set_folder, 'symbol.png'))

    print(f"Now downloading cards for {each_set['series']} {each_set['name']}...")

    cards = get_cards_by_set(each_set)

    write_json_to_file(os.path.join(set_folder, 'cards.json'), cards)
