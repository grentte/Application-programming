import random
import json

def load_words():
    # Загрузка списка слов из файла word_dictionary.json
    try:
        with open("word_dictionary.json", "r", encoding="utf-8") as file:
            words = json.load(file)
            return [word.lower() for word in words if len(word) == 5]
    except FileNotFoundError:
        print("Файл word_dictionary.json не найден. Убедитесь, что он находится в той же директории, что и main.py.")
        return []

def choose_word(word_list):
    # Случайный выбор слова из списка
    return random.choice(word_list)

def get_feedback(secret_word, guess):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            feedback.append("+")  # Буква на правильной позиции
        elif guess[i] in secret_word:
            feedback.append("?")  # Буква есть, но на другой позиции
        else:
            feedback.append("-")  # Буквы нет в слове
    return "".join(feedback)

def game():
    print("Добро пожаловать в игру '5 букв'!")
    print("Угадайте слово из 5 букв. После каждой попытки вы получите подсказки:")
    print("+ : Буква на правильной позиции.")
    print("? : Буква есть, но на другой позиции.")
    print("- : Буквы нет в слове.")

    word_list = load_words()
    if not word_list:
        print("Невозможно начать игру: список слов пуст или файл отсутствует.")
        return

    secret_word = choose_word(word_list)
    attempts = 6

    while attempts > 0:
        guess = input(f"\nОсталось {attempts} попыток. Введите слово из 5 букв: ").lower()

        if len(guess) != 5:
            print("Пожалуйста, введите слово из 5 букв.")
            continue

        if guess not in word_list:
            print("Это слово отсутствует в словаре. Попробуйте другое слово.")
            continue

        if guess == secret_word:
            print("Поздравляем! Вы угадали слово!")
            break

        feedback = get_feedback(secret_word, guess)
        print(f"Подсказка: {feedback}")
        attempts -= 1

    if attempts == 0:
        print(f"Вы исчерпали все попытки. Загаданное слово: {secret_word}")

if __name__ == "__main__":
    game()
