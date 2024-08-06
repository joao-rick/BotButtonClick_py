import sys
import pyautogui
import time
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel, QGridLayout #não tenho certeza se tem componentes melhores dessa lib pra usar
from PyQt5.QtCore import QThread, pyqtSignal

button_image = 'button.png'

class BotThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        while self.running:
            self.click_button()
            time.sleep(10)

    def click_button(self):
        try:
            button_location = pyautogui.locateCenterOnScreen(button_image, confidence=0.8)
            if button_location:
                pyautogui.click(button_location)
                self.log_signal.emit('Botão clicado!')
            else:
                self.log_signal.emit('Botão não encontrado.')
        except Exception as e:
            self.log_signal.emit(f'Erro ao tentar clicar no botão: {e}')

    def start_bot(self):
        self.running = True
        self.start()

    def stop_bot(self):
        self.running = False
        self.wait()

class BotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Bot Impressora - BRAJAN')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.start_button = QPushButton('Iniciar Bot')
        self.start_button.clicked.connect(self.start_bot)

        self.stop_button = QPushButton('Parar Bot')
        self.stop_button.clicked.connect(self.stop_bot)
        self.stop_button.setEnabled(False)

        self.layout.addWidget(QLabel('Logs:'))
        self.layout.addWidget(self.log_text)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)

        self.bot_thread = BotThread()
        self.bot_thread.log_signal.connect(self.log_message)

    def log_message(self, message):
        self.log_text.append(message)

    def start_bot(self):
        self.bot_thread.start_bot()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.log_message('Bot iniciado.')

    def stop_bot(self):
        self.bot_thread.stop_bot()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.log_message('Bot parado.')

def main():
    app = QApplication(sys.argv)
    ex = BotApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
