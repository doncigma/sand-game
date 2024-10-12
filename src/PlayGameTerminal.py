from SandGameUI import SandGameUI
from PyQt6.QtWidgets import QApplication
import sys

def PlayGame():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Incorrect invocation of script: check readme for details.")
        return
  
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    
    app = QApplication(sys.argv)
    if len(sys.argv) == 4:
        brownian = int(sys.argv[3])
        game = SandGameUI((width, height), brownian)
    else:
        game = SandGameUI((width, height))
    game.show()
    game.start_game()
    sys.exit(app.exec())

if __name__ == "__main__":
    PlayGame()
    