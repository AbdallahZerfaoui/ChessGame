import chess
import chess.svg
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

class MainWindow(QWidget):
    def __init__(self, board_size, top_lef_pos):
        super().__init__()
        
        self.setWindowTitle("Play with me!!")
        # 2 times the border size plus the board size we get the windwo size
        window_size = board_size + 2*top_lef_pos
        
        self.setGeometry(0, 0, window_size, window_size) #(x, y, width, height)

        self.widgetSvg = QSvgWidget(parent=self)
        self.svgX = top_lef_pos                          # top left x-pos of chessboard
        self.svgY = top_lef_pos                          # top left y-pos of chessboard
        self.cbSize = board_size                         # size of chessboard
        self.widgetSvg.setGeometry(self.svgX,self.svgY, self.cbSize, self.cbSize) # we set the board position
        self.coordinates = True
        # see chess.svg.py line 129
        self.margin = 0.05*self.cbSize if self.coordinates == True else 0
        self.squareSize  = (self.cbSize - 2 * self.margin) / 8.0 # square size computing
        self.chessboard = chess.Board() # the board is generated
        self.pieceToMove = [None, None]
        self.halfmove_number = 0
        """
        self.halfmove_number counts the number of half moves,
        it allows us to know who has to play
        """
    def IsRightPiece(self):
        """
        This method with check if it's our turn.
        IsRightPiece --> True if it's our turn
        we get the answer by comparing "turn" from the board with the color of the piece we are trying to move.
        """
        if (self.chessboard.turn != self.pieceToMove[0].color):
            return False
        else:
            return True
        
    @pyqtSlot(QWidget)
    def mousePressEvent(self, event):
        if self.pieceToMove[0] is not None:
            print(self.pieceToMove[0].color, chess.WHITE)
        if self.svgX < event.x() <= self.svgX + self.cbSize and self.svgY < event.y() <= self.svgY + self.cbSize:   # mouse on chessboard
            if event.buttons() == Qt.LeftButton:
                # if the click is on chessBoard only
                if self.svgX + self.margin < event.x() < self.svgX + self.cbSize - self.margin and self.svgY + self.margin < event.y() < self.svgY + self.cbSize - self.margin:
                    file = int((event.x() - (self.svgX + self.margin))/self.squareSize)             
                    rank = 7 - int((event.y() - (self.svgY + self.margin))/self.squareSize) 
                    square = chess.square(file, rank)                       # chess.sqare.mirror() if white is on top
                    piece = self.chessboard.piece_at(square)
                    coordinates = '{}{}'.format(chr(file + 97), str(rank +1))
               
                    if self.pieceToMove[0] is not None:
                        move = chess.Move.from_uci('{}{}'.format(self.pieceToMove[1], coordinates))
                        #we push the piece to move only if the move is legal 
                        if (move in self.chessboard.legal_moves):
                            self.chessboard.push(move)
                            self.halfmove_number += 1
                            print(self.chessboard.fen())
                            
                        elif(not self.IsRightPiece()):
                            print("It's not your turn")
                            #piece = None
                            #coordinates= None
                            print(chess.WHITE, self.pieceToMove[0].color)
                        else:
                            print("Sorry, you can execute this move")
                        piece = None
                        coordinates= None
                    self.pieceToMove = [piece, coordinates]                                           
                else:
                    print('coordinates clicked')
                # Envoke the paint event.
                self.update()
        else:
            QWidget.mousePressEvent(self, event)

    @pyqtSlot(QWidget)
    def paintEvent(self, event):
        self.chessboardSvg = chess.svg.board(self.chessboard, size = self.cbSize, coordinates = self.coordinates).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)
