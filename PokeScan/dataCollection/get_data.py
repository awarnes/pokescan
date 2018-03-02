import requests
import shutil, os, sys
import json
from datetime import datetime

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
        return json.load(f)

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
    r = requests.get('https://api.pokemontcg.io/v1/sets/{}'.format(id))
    return r.json()['set']

def get_card_by_id(id):
    "Gets a card by id."
    r = requests.get('https://api.pokemontcg.io/v1/cards/{}'.format(id))
    try:
        return r.json()['card']
    except Exception as e:
        print(e)
        print(r.json())
        return r.json()

def get_cards_by_set(set):
    "Creates a json file for all the cards in a given set. Input set must be a json object."
    set_id = set['code']
    number_of_cards = set['totalCards']
    
    cards = list()
    
    for card_number in range(1, number_of_cards + 1):
        cards.append(get_card_by_id('{}-{}'.format(set_id, card_number)))
    
    return cards    

def update_change_log(path):
    "Creates and additional entry in change.log for update purposes in path."
    with open(os.path.join(path, 'change.log'), 'a') as f:
        f.write(datetime.now().strftime('%m/%d/%Y %X'))
        f.write('\n')


data_path = os.path.join(cwd, 'data')

mkdir(data_path)

all_sets = get_all_sets()

write_json_to_file(os.path.join(data_path, 'sets.json'), all_sets)

for each_set in all_sets:
    set_folder = os.path.join(data_path, each_set['code'])

    update = True
    try:
        last_updated = ''
        with open(os.path.join(set_folder, 'change.log'), 'r') as f:
            last_updated = f.readlines()[-1].strip()
            set_updated_at = datetime.strptime(each_set['updatedAt'], '%m/%d/%Y %X')
            system_updated = datetime.strptime(last_updated, '%m/%d/%Y %X')
            if (set_updated_at < system_updated):
                print("Already have latest information for {} {}!".format(each_set['series'], each_set['name']))
                update = False

    except (FileNotFoundError, IndexError):
        print('Set not found, downloading now...')
        pass

    if update:
        mkdir(set_folder)

        download_png(each_set['symbolUrl'], os.path.join(set_folder, 'symbol.png'))

        print("Now downloading cards for {} {}...".format(each_set['series'], each_set['name']))

        cards = get_cards_by_set(each_set)

        write_json_to_file(os.path.join(set_folder, 'cards.json'), cards)

        update_change_log(set_folder)


