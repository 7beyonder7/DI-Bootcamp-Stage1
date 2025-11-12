from pathlib import Path
from random import randint, choice
import json
import sys


def get_words_from_file(file_path: str) -> list[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            words = content.strip().split()
            if not words:
                raise ValueError('The file is empty.')
        return words
    except FileNotFoundError as e:
        print(f"Error: The file at {file_path} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def get_random_sentence(length: int, file_path: str) -> str:
    words = get_words_from_file(file_path)
    chosen_words = [choice(words) for _ in range(length)]
    new_sentence = ' '.join(chosen_words).lower()
    return new_sentence


def main():
    print('Welcome to the Random Sentence Generator')
    print('The program generates a random sentence of a specified length from a file\n')
    while True:
        try:
            base_dir = Path(__file__).resolve().parent
            file_path = base_dir / "words.txt"
            user_input_length = int(input(
                'Please enter a number between 2 and 20 to generate a sentence with provided length: '))
            if 2 <= user_input_length <= 20:
                print(f"Valid input: {user_input_length}")
                print(
                    f'The sentence is: {get_random_sentence(user_input_length, file_path)}')
                break
            else:
                print(
                    f"Invalid input. The number {user_input_length} is outside the range 2-20.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


main()

sampleJson = """{
   "company": {
      "employee": {
         "name": "emma",
         "payable": {
            "salary": 7000,
            "bonus": 800
        }
    }
   }
 }"""

data = json.loads(sampleJson)

print(data)
salary = data["company"]["employee"]["payable"]["salary"]
print("Salary:", salary)
data["company"]["employee"]["birth_date"] = "1991-12-31"
print(data)

try:
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "dump.json"
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
except Exception as e:
    print(e)
