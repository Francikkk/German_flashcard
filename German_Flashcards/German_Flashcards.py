from tkinter import *
import pandas
import random

#---------------------------- DATA SETUP -------------------------------#
current_card = {}
to_learn = {}
flip_timer = None
BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("VS/German_Flashcards/data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("VS/German_Flashcards/data/1000_words_de_en.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

#---------------------------- FUNCTIONALITY -------------------------------#
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(card_title, text="German", fill="black")
    canvas.itemconfig(card_word, text=current_card["German"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("VS/German_Flashcards/data/words_to_learn.csv", index=False)
    next_card()

#---------------------------- UI SETUP -------------------------------#
# Create the window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# Create the card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="VS/German_Flashcards/images/card_front.png")
card_back = PhotoImage(file="VS/German_Flashcards/images/card_back.png")
card = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# Create the buttons
right_image = PhotoImage(file="VS/German_Flashcards/images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)
wrong_image = PhotoImage(file="VS/German_Flashcards/images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()


