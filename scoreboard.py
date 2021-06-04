import json


class Scoreboard:
    def __init__(self):
        self.correct_words = 0
        self.typed_entries = 0

        self.wpm = 0
        self.accuracy = 0

        # Read and display the high score from game_data.txt
        with open("game_data/scores.json") as scores:
            data = json.load(scores)
        self.highest_wpm = int(data["WPM"])
        self.highest_accuracy = int(data["Accuracy"])

    def add_typed_entries(self, event):
        self.typed_entries += 1

    def calculate_score(self, time_taken, quote, input_text):
        # Calculate Percentage Accuracy
        for i, c in enumerate(quote):
            try:
                if input_text[i] == c:
                    self.correct_words += 1
            except IndexError:
                pass

        self.accuracy = round((self.correct_words / len(quote)) * 100)

        # Calculate WPM
        self.wpm = round((self.typed_entries/5) / (time_taken/60))
        return self.wpm, self.accuracy

    def reset_scores(self):
        self.correct_words = 0
        self.typed_entries = 0

        # Store the high score in game_data.txt
        if self.wpm > self.highest_wpm and self.accuracy >= self.highest_accuracy:
            data = {
                "WPM": self.wpm,
                "Accuracy": self.accuracy
            }
            with open("game_data/scores.json", mode="w") as scores:
                json.dump(data, scores)
