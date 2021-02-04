import json
from card_parsing.parse_card_player import parse_player

def parse_cards():
    # Read cards
    f = open('data/cards/Cards.txt', 'r')
    cards_data_string = f.readline()
    f.close()

    # Load it as json data
    cards_data = json.loads(cards_data_string)

    player_db = []
    for player in cards_data:
        # Parse each player
        player_db.append(parse_player(player))

    # TODO match player ratings for -sp/-rp

    return player_db