from anagram_checker import AnagramChecker


def prompt_word() -> str:
    while True:
        user_input = input("Enter a word: ").strip()
        if " " in user_input:
            print("Error: Please enter exactly one word.")
            continue
        if not user_input.isalpha():
            print("Error: Only alphabetic characters are allowed.")
            continue
        return user_input


def main():
    print('Welcome to Anagram checker')
    anagram_checker = AnagramChecker()
    while True:
        print()
        print("1) Get anagrams for a word")
        print("2) Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            word = prompt_word()
            print("This is a valid English word.")
            result = anagram_checker.get_anagrams(word)
            if result:
                anagrams_str = ", ".join(result)
                print("\n" + "="*80)
                print(f"YOUR WORD: \"{word}\"")
                print(f"Anagrams for your word: {anagrams_str}.")
                print("="*80)
            else:
                print(f"No anagrams found for this word '{word}' in the list.")

        elif choice == "2":
            print("Goodbye!")
            return

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()
