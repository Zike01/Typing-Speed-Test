from tkinter import *
from quotes_generator import QuoteGenerator
from scoreboard import Scoreboard

current_word = 0
input_text = []
timer = None
doTick = True

# Initialize the word generator
generator = QuoteGenerator()

# Initialize the scoreboard
scoreboard = Scoreboard()

# ---------------------------- CONSTANTS ------------------------------------------#
DODGERBLUE = "#1E90FF"
RED = "#FF0000"
DARK_RED = "#B53B07"
BLACK = "#000000"

FONT = ("Arial", 10, "bold")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def count_up(count):
    global timer

    if not doTick:
        return

    timer = window.after(1000, count_up, count+1)
    canvas.itemconfig(timer_text, text=f"Time Elapsed: {count}s")


# -------------------------- WORD CHECKER -------------------------------------#
def check_word(event, chosen_quote_list):
    global current_word

    word_input = entry.get()

    # Remove leading spaces from entry
    if "" in word_input:
        word_input = word_input.strip()

    # Add the word input to the input_text list
    input_text.append(word_input)

    entry.delete(0, END)

    current_word += 1
    if current_word == len(chosen_quote_list):
        # Reset the word count and end game
        current_word = 0
        end_game()
    else:
        # Prompt the user with the next word in the quote text
        prompt(chosen_quote_list)


# ------------------------------------------------------------------------------------------- #
def start_test():
    global doTick

    # Start the timer
    doTick = True
    count_up(0)

    # Clear input_text list
    input_text.clear()

    # Print the highest WPM and highest accuracy
    if scoreboard.highest_wpm > 0 and scoreboard.highest_accuracy > 0:
        canvas.itemconfig(high_scores, text=f"Highest WPM: {scoreboard.highest_wpm}\n"
                                            f"Highest Accuracy: {scoreboard.highest_accuracy}")

    # Generate a random quote from the quotes.json file
    chosen_quote = generator.get_random_quote()["quote"]
    canvas.itemconfig(main_text, text=chosen_quote)

    # Prompt the user with the first word of the quote text
    prompt(chosen_quote.split())

    # Bind the spacebar to the entry widget to check every word input
    entry.bind("<space>", lambda event: check_word(event, chosen_quote_list=chosen_quote.split()))

    # Bind all keys to the entry widget to increase the character count (used to calculate the words per minute)
    entry.bind("<Key>", scoreboard.add_typed_entries)

    entry.delete(0, END)
    entry.focus()

    # Remove the start_button widget
    start_button.pack_forget()


def prompt(quote_list):
    # Places the current word above the quote text
    word = quote_list[current_word]
    canvas.itemconfig(word_prompt, text=word, fill=RED)


def end_game():
    global doTick

    # Stop the timer and reset
    doTick = False
    entry.unbind("<space>")

    # Grab the quote and time taken from the canvas
    quote = canvas.itemcget(main_text, 'text').split()
    time_taken = int(canvas.itemcget(timer_text, 'text').split(':')[1].split('s')[0])

    # Calculate the WPM and Accuracy
    wpm, accuracy = scoreboard.calculate_score(time_taken, quote, input_text)

    # Display stats on the canvas
    canvas.itemconfig(main_text,
                      fill=DARK_RED,
                      text=f"RESULTS\nTime: {time_taken}s \nWPM: {wpm}\nAccuracy: {accuracy}%")

    # Make the word prompt and high_score label invisible
    canvas.itemconfig(word_prompt, text="")
    canvas.itemconfig(high_scores, text="")

    # Reset the score and make the start button visible
    scoreboard.reset_scores()
    start_button.config(text="Try again")
    start_button.pack()


# ------------------------------ UI SETUP -----------------------------------#
window = Tk()
window.title("Typing Speed Test")
window.config(padx=20, pady=20, bg=BLACK)

# LABELS
title_label = Label(text="TYPING SPEED TEST", font=FONT)
title_label.pack()

# CANVAS
canvas = Canvas(width=500, height=400, highlightthickness=0, bg=DODGERBLUE)
main_text = canvas.create_text(250, 200, width=400, text="", font=FONT)
word_prompt = canvas.create_text(250, 100, text="", font=FONT)
high_scores = canvas.create_text(100, 20, text="")
timer_text = canvas.create_text(400, 20, text="Time Elapsed: 0s")

canvas.pack()

# ENTRY
entry = Entry(width=55, justify="center")
entry.pack()

# BUTTONS
start_button = Button(text="Start", bg=DODGERBLUE, command=start_test)
start_button.pack()

window.mainloop()
