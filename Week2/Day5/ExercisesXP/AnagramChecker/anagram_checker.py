from pathlib import Path
import sys
from collections import Counter


def get_words_from_file(file_name: str) -> list[str]:
    try:
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / file_name
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            words = file_content.strip().lower().split()
            if not words:
                raise ValueError('The file is empty. Cannot proceed.')
            return words
    except FileNotFoundError as e:
        print(f'Error: The file at {file_path} was not found. Cannot proceed.')
        sys.exit(1)
    except Exception as e:
        print(f'An error occured: {e}')
        sys.exit(1)


class AnagramChecker:
    def __init__(self):
        self.list = get_words_from_file('sowpods.txt')

    def is_valid_word(self, word: str) -> bool:
        if word in self.list:
            return True
        else:
            return False

    def is_anagram(self, w1: str, w2: str) -> bool:
        if not (w1 and w2 and w1.isalpha() and w2.isalpha()):
            return False
        return Counter(w1.lower()) == Counter(w2.lower())

    def get_anagrams(self, word_to_check: str) -> list[str]:
        anagrams_list = []
        for word in self.list:
            anagram_word = self.is_anagram(word, word_to_check)
            if anagram_word:
                anagrams_list.append(word)
        return anagrams_list


def main():
    anagram_checker = AnagramChecker()
    print(anagram_checker.is_valid_word('aahing'))
    print(anagram_checker.is_valid_word('Witcher'))
    print(anagram_checker.get_anagrams('Witcher'))
    print(anagram_checker.get_anagrams('tutebr'))
    print(anagram_checker.get_anagrams('MEAT'))


if __name__ == "__main__":
    main()
