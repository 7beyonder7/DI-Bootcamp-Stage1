import random

Choice = ["rock", "paper", "scissors"]
Result = ["win", "draw", "loss"]


class Game:
    _CHOICES = ("rock", "paper", "scissors")
    _BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

    def _normalize(self, raw: str):
        s = raw.strip().lower()
        alias = {"r": "rock", "p": "paper", "s": "scissors"}
        s = alias.get(s, s)
        if s not in self._CHOICES:
            raise ValueError("Please choose rock, paper, or scissors (r/p/s).")
        return s

    def get_user_item(self):
        while True:
            raw = input("Choose [r]ock, [p]aper, or [s]cissors: ")
            try:
                return self._normalize(raw)
            except ValueError as e:
                print(f"Invalid choice: {e}")

    def get_computer_item(self):
        return random.choice(self._CHOICES)

    def get_game_result(self, user_item, computer_item):
        if user_item == computer_item:
            return "draw"
        return "win" if self._BEATS[user_item] == computer_item else "loss"

    def play(self):
        user_item = self.get_user_item()
        computer_item = self.get_computer_item()
        result = self.get_game_result(user_item, computer_item)
        print(f"\nYou chose: {user_item}")
        print(f"Computer chose: {computer_item}")
        print(f"Result: {result.upper()}\n")
        return result
