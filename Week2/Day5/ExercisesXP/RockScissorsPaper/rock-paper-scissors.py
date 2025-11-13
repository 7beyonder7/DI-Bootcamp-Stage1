# from __future__ import annotations
from game import Game

MENU = {
    "1": "Play a new game",
    "2": "Show scores",
    "3": "Quit",
}


def get_user_menu_choice() -> str:
    while True:
        print("=== Rock Paper Scissors ===")
        for k, v in MENU.items():
            print(f"{k}) {v}")
        choice = input("Select an option (1-3): ").strip()
        if choice in MENU:
            return choice
        print("Invalid input. Please enter 1, 2, or 3.\n")


def print_results(results: dict[str, int]) -> None:
    wins = results.get("win", 0)
    losses = results.get("loss", 0)
    draws = results.get("draw", 0)
    total = wins + losses + draws
    print("\n=== Game Summary ===")
    print(f"Wins:   {wins}")
    print(f"Losses: {losses}")
    print(f"Draws:  {draws}")
    print(f"Total:  {total}")
    print("Thanks for playing!\n")


def main() -> None:
    results = {"win": 0, "loss": 0, "draw": 0}
    game = Game()

    while True:
        choice = get_user_menu_choice()

        if choice == "1":
            outcome = game.play()
            results[outcome] += 1
        elif choice == "2":
            print_results(results)
        elif choice == "3":
            print_results(results)
            break


if __name__ == "__main__":
    main()
