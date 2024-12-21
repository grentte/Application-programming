import random

def choose_word():
    # Список слов из пяти букв
    words = ["столб", "мячик", "книга", "носки", "палка"]
    return random.choice(words).lower()

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

    secret_word = choose_word()
    attempts = 6

    while attempts > 0:
        guess = input(f"\nОсталось {attempts} попыток. Введите слово из 5 букв: ").lower()

        if len(guess) != 5:
            print("Пожалуйста, введите слово из 5 букв.")
            continue

        if guess == secret_word:
            print("Поздравляем! Вы угадали слово!")
            break

        feedback = get_feedback(secret_word, guess)
        print(f"{feedback}")
        attempts -= 1

    if attempts == 0:
        print(f"Вы исчерпали все попытки. Загаданное слово: {secret_word}")

if __name__ == "__main__":
    game()