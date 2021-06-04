import json
import random

FILE = "game_data/quotes.json"


class QuoteGenerator:
    def __init__(self):
        self.file = FILE

    def get_random_quote(self):
        with open(self.file, "r") as quotes:
            data = json.load(quotes)

        quotes_list = data["quotes"]
        return random.choice(quotes_list)
