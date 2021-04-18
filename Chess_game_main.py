#py -m pip install PyQt5

from MyClasses import *


board_size  = 800
top_lef_pos = 50
if __name__ == "__main__":
    chessGame = QApplication([])
    window = MainWindow(board_size, top_lef_pos)
    window.show()
    chessGame.exec()
    

        
