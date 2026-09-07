import time
import random
import sys
import supervisor
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.2
cp.pixels.auto_write = False # the lights are global and have different meanings.

#21 is typically played from [0,21] in this game we are limited so we are trying to get as close to
#5 as we can

PLAY = [0, 1, 2, 3, 4]      # bottom lights, keep track of hand.
SCORE = [5, 6, 7, 8, 9]     # top lights, keep track of chips.

# keeps track of assigned colors

OFF  = (0, 0, 0)
BLUE = (0, 0, 80) # keeps track of cards/hand
GRN  = (0, 80, 0) # keeps track of chips and global round celebration
RED  = (80, 0, 0) # Global round loss
GLD  = (80, 40, 0) # when you win +5 chips


# game needs to keep track of score using class
# needs a way to control the hardware I.E led, sound, and buttons
class Game:
    def __init__(self):
        # tracked game state
        self.score = 0      # chips
        self.hits = 0       # current lights on bottom
        self.target = 0     # secret number
        self.prev_a = False # detects whether A was hit
        self.prev_b = False # detects whether B was hit

        self.clear() # Turns off leds so the game starts with a clean board
        self.new_round()    # starts a new starting number and secret target

    # clear function which turns off all leds between rounds
    # at the start and end of the game
    def clear(self):
        for i in range(10):
            cp.pixels[i] = OFF
        cp.pixels.show()

    # function that uses the top 5 lights, shows score,
    def show_score(self):
        for i, p in enumerate(SCORE): # gives me the index and the led light
            cp.pixels[p] = GRN if i < self.score else OFF

    # Shows my (hand)
    # lights bottom led lights with random hand.
    def show_hits(self):
        for i, p in enumerate(PLAY):
            cp.pixels[p] = BLUE if i < self.hits else OFF

    # function that refreshes both score and hit lights
    # since auto write is off
    def draw(self):
        self.show_score()
        self.show_hits()
        cp.pixels.show()


    # flash function with color, sound and number of times of flash
    def flash(self, color, tone, n):
        for _ in range(n):
            cp.pixels.fill(color)
            cp.pixels.show()
            if tone:
                cp.play_tone(tone, 0.1)
            time.sleep(0.05)
            cp.pixels.fill(OFF) # turns led off again
            cp.pixels.show()
            time.sleep(0.05)

    # Start a new round.
    def new_round(self):
        self.hits = random.randint(1, len(PLAY)) # your hand starts between [1,5]
        self.target = random.randint(1, len(PLAY)) # the hand you are trying to beat [1,5]
        self.draw()

    # How the hit function work
    def hit(self):
        step = random.randint(1, 2) # value between [1,2] & simulates drawing a card
        self.hits += step
        cp.play_tone(400 + step * 80, 0.08) # +2  gives a higher

        # bust: lose a chip
        if self.hits > len(PLAY):
            if self.score > 0:
                self.score -= 1
            print("-1 chip")
            self.flash(RED, 300, 3)
            self.new_round()
        else:
            self.draw()

    # stand function checks the win condition hits>target and hits<len(play)
    def stand(self):
        # win if you are higher than the secret number but not over 5
        if self.hits > self.target and self.hits <= len(PLAY):
            if self.score < len(SCORE):
                self.score += 1 # counter
            print("+1 chip")
            self.flash(GRN, 800, 3)
        else:
            if self.score > 0:
                self.score -= 1
            print("-1 chip")
            self.flash(RED, 250, 3)

        self.new_round()

        # 5 chips = win the game
        if self.score == len(SCORE):
            print("You win!")
            self.flash(GLD, 1000, 5)
            self.score = 0
            self.new_round()

    # serial output resets the game by typing r in the serial output
    def serial_input(self):
        if supervisor.runtime.serial_bytes_available:
            ch = sys.stdin.read(1)
            if ch == "r":
                self.score = 0
                self.hits = 0
                self.target = 0
                print("reset")
                self.clear()
                self.new_round()

    # action buttons
    def run(self):
        while True:
            a = cp.button_a
            b = cp.button_b

            if a and not self.prev_a:
                self.hit()
            if b and not self.prev_b:
                self.stand()

            # handle optional serial input without blocking
            self.serial_input()

            self.prev_a = a
            self.prev_b = b
            time.sleep(0.02)


g = Game()
g.run() 
