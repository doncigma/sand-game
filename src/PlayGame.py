from SandGameUI import SandGameUI
from PyQt6.QtWidgets import QApplication
import sys

def PlayGame():
    app = QApplication(sys.argv)
    window = SandGameUI((50, 50))
    window.show()
    window.start_game()
    sys.exit(app.exec())

if __name__ == "__main__":
    PlayGame()
    