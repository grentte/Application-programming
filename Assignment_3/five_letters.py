import sys
import random
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)

class WordleGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Игра 5 букв")
        self.setGeometry(100, 100, 400, 300)

        self.attempts = 6
        self.secret_word = ""
        self.word_list = self.load_words()
        if self.word_list:
            self.secret_word = self.choose_word()

        self.init_ui()

    def load_words(self):
        try:
            with open("word_dictionary.json", "r", encoding="utf-8") as file:
                words = json.load(file)
                return [word.lower() for word in words if len(word) == 5]
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл word_dictionary.json не найден.")
            return []

    def choose_word(self):
        return random.choice(self.word_list)

    def get_feedback(self, guess):
        feedback = []
        for i in range(len(guess)):
            if guess[i] == self.secret_word[i]:
                feedback.append("+")  # Буква на правильной позиции
            elif guess[i] in self.secret_word:
                feedback.append("?")  # Буква есть, но на другой позиции
            else:
                feedback.append("-")  # Буквы нет в слове
        return "".join(feedback)

    def init_ui(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("Угадайте слово из 5 букв. У вас есть 6 попыток.")
        layout.addWidget(self.info_label)

        self.attempts_label = QLabel(f"Осталось попыток: {self.attempts}")
        layout.addWidget(self.attempts_label)

        self.feedback_label = QLabel("Подсказка:")
        layout.addWidget(self.feedback_label)

        self.input_field = QLineEdit()
        self.input_field.setMaxLength(5)
        layout.addWidget(self.input_field)

        self.check_button = QPushButton("Проверить слово")
        self.check_button.clicked.connect(self.check_word)
        layout.addWidget(self.check_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_word(self):
        guess = self.input_field.text().lower()

        if len(guess) != 5:
            QMessageBox.warning(self, "Предупреждение", "Введите слово из 5 букв.")
            return

        if guess not in self.word_list:
            QMessageBox.warning(self, "Предупреждение", "Это слово отсутствует в словаре. Попробуйте другое слово.")
            return

        if guess == self.secret_word:
            QMessageBox.information(self, "Победа", "Поздравляем! Вы угадали слово!")
            self.reset_game()
            return

        feedback = self.get_feedback(guess)
        self.feedback_label.setText(f"Подсказка: {feedback}")

        self.attempts -= 1
        self.attempts_label.setText(f"Осталось попыток: {self.attempts}")

        if self.attempts == 0:
            QMessageBox.information(self, "Игра окончена", f"Вы исчерпали все попытки. Загаданное слово: {self.secret_word}")
            self.reset_game()

    def reset_game(self):
        self.attempts = 6
        self.secret_word = self.choose_word()
        self.feedback_label.setText("Подсказка:")
        self.attempts_label.setText(f"Осталось попыток: {self.attempts}")
        self.input_field.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    game = WordleGame()
    game.show()

    sys.exit(app.exec())
