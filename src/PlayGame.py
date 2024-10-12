from SandGameUI import SandGameUI
from PyQt6.QtWidgets import QApplication
import sys

def PlayGame():
    app = QApplication(sys.argv)
    game = SandGameUI((100, 60))
    game.show()
    game.start_game()
    sys.exit(app.exec())

if __name__ == "__main__":
    PlayGame()
    