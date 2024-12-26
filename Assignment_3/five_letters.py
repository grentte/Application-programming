import sys
import random
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QScrollArea, QMenuBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction


class WordleGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Игра 5 букв")
        self.setGeometry(100, 100, 600, 400)

        self.attempts = 6
        self.secret_word = ""
        self.word_list = self.load_words()
        if self.word_list:
            self.secret_word = self.choose_word()

        self.current_feedback = ["_ _ _ _ _" for _ in range(self.attempts)]
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

    def get_colored_feedback(self, guess):
        feedback = []
        for i, char in enumerate(guess):
            if char == self.secret_word[i]:
                feedback.append(f'<span style="color: green;">{char}</span>')  # Правильная буква и позиция
            elif char in self.secret_word:
                feedback.append(f'<span style="color: orange;">{char}</span>')  # Правильная буква, но неправильная позиция
            else:
                feedback.append(f'<span style="color: red;">{char}</span>')  # Буквы нет в слове
        return " ".join(feedback)

    def update_feedback_display(self):
        return "<br>".join(self.current_feedback)

    def init_ui(self):
        self.init_menu()

        layout = QVBoxLayout()

        self.info_label = QLabel("Угадайте слово из 5 букв за 6 попыток.")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_display = QLabel(self.update_feedback_display())
        self.feedback_display.setTextFormat(Qt.TextFormat.RichText)
        self.feedback_display.setWordWrap(True)

        self.input_field = QLineEdit()
        self.input_field.setMaxLength(5)
        self.input_field.returnPressed.connect(self.check_word)
        self.check_button = QPushButton("Проверить слово")
        self.check_button.clicked.connect(self.check_word)

        # Добавление элементов на экран
        layout.addWidget(self.info_label)
        layout.addWidget(self.feedback_display)
        layout.addWidget(self.input_field)
        layout.addWidget(self.check_button)

        container = QWidget()
        container.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        self.setCentralWidget(scroll_area)

    def init_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        game_menu = menu_bar.addMenu("Меню")

        reset_action = QAction("Начать заново", self)
        reset_action.triggered.connect(self.reset_game)
        game_menu.addAction(reset_action)

        rules_action = QAction("Правила", self)
        rules_action.triggered.connect(self.show_rules)
        game_menu.addAction(rules_action)

    def show_rules(self):
        rules = (
            "Принцип игры:\n"
            "1. Угадайте слово из 5 букв за 6 попыток.\n"
            "2. После каждой попытки буквы окрашиваются: зеленый - буква есть в слове и стоит на правильной позиции,\n"
            "жёлтый - буква есть в слове, но стоит на неправильной позиции, красный - буквы нет в слове.\n"
        )
        QMessageBox.information(self, "Правила игры", rules)

    def check_word(self):
        guess = self.input_field.text().lower()

        if len(guess) != 5:
            QMessageBox.warning(self, "Предупреждение", "Введите слово из 5 букв.")
            return

        if guess not in self.word_list:
            QMessageBox.warning(self, "Предупреждение", "Это слово отсутствует в словаре. Попробуйте другое слово.")
            return

        feedback = self.get_colored_feedback(guess)
        self.current_feedback[6 - self.attempts] = feedback
        self.feedback_display.setText(self.update_feedback_display())

        if guess == self.secret_word:
            QMessageBox.information(self, "Победа", "Поздравляем! Вы угадали слово!")
            self.reset_game()
            return

        self.attempts -= 1

        if self.attempts == 0:
            QMessageBox.information(self, "Игра окончена", f"Вы исчерпали все попытки. Загаданное слово: {self.secret_word}")
            self.reset_game()

        self.input_field.clear()

    def reset_game(self):
        self.attempts = 6
        self.secret_word = self.choose_word()
        self.current_feedback = ["_ _ _ _ _" for _ in range(self.attempts)]
        self.feedback_display.setText(self.update_feedback_display())
        self.input_field.clear()

    def resizeEvent(self, event):
        # Масштабирование шрифта в зависимости от размера окна
        width = self.width()
        height = self.height()

        font_size = max(min(width, height) // 30, 12)  # Вычисление шрифта в зависимости от размера окна
        font = QFont("Arial", font_size)

        self.info_label.setFont(font)
        self.feedback_display.setFont(font)
        self.input_field.setFont(font)
        self.check_button.setFont(font)

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    game = WordleGame()
    game.show()

    sys.exit(app.exec())
