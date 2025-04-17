import pygame
from ChessEngine import *
from ChessAI import *
import sys  
from multiprocessing import Process, Queue
import ctypes
import os
from Const import *
from Config import *
from GameComponents import *
import math



class Game:
    def __init__(self):
        pygame.init()
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        self.config = Config()
        self.mainScreen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Chess AI')
        pygame.display.set_icon(pygame.image.load('./assets/images/logo/logo.png'))
        if os.name == 'nt':
            myappid = 'chess.ai.game.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.gameState = GameState()
        self.validMoves = self.gameState.getValidMoves()
        self.imageSmall = {}
        self.imageBig = {}
        self.loadImages()
        self.captured = False
        self.hoveredSquare = None
        self.dragger = Dragger()
        self.player_one = True
        self.player_two = False
        self.ai_thinking = False
        self.move_finder_process = None
        self.move_undone = False
        self.game_over = False

        try:
            self.config.castleSound = pygame.mixer.Sound('./assets/sounds/castle.wav')
        except:
            pass

    def mainLoop(self):
            while True:
                human_turn = True
                self.drawGameState()
                self.highlightChecks()

                if not self.dragger.dragging:
                    Animation.showHover(self)

                if self.dragger.dragging:
                    Animation.showMoves(self)
                    self.dragger.updateBlit(self.mainScreen, self.dragger.piece)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEMOTION:
                        motionRow = event.pos[1] // SQUARE_SIZE
                        motionCol = event.pos[0] // SQUARE_SIZE

                        self.setHover(motionRow, motionCol)
                        self.dragger.updateMouse(event.pos)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and human_turn and not self.game_over:
                            clickRow = event.pos[1] // SQUARE_SIZE
                            clickCol = event.pos[0] // SQUARE_SIZE

                            if 0 <= clickRow < ROWS and 0 <= clickCol < COLS:
                                piece = self.gameState.board[clickRow][clickCol]
                                if piece != "--" and (
                                        (piece[0] == "w" and self.gameState.white_to_move) or
                                        (piece[0] == "b" and not self.gameState.white_to_move)):
                                    self.dragger.saveInitial(event.pos)
                                    self.dragger.dragPiece(piece)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and self.dragger.dragging and human_turn and not self.game_over:
                            releaseRow = event.pos[1] // SQUARE_SIZE
                            releaseCol = event.pos[0] // SQUARE_SIZE

                            if 0 <= releaseRow < ROWS and 0 <= releaseCol < COLS:
                                move = Move((self.dragger.initialRow, self.dragger.initialCol),
                                            (releaseRow, releaseCol),
                                            self.gameState.board)
                                
                                
                                if move.piece_moved[1] == 'p' and abs(move.start_col - move.end_col) == 1 and abs(move.start_row - move.end_row) == 1:
                                    move.is_enpassant_move = True
                                
                                is_castle = False
                                if move.piece_moved[1] == 'K' and abs(move.start_col - move.end_col) == 2:
                                    is_castle = True
                                    move.is_castle_move = True
                                
                                self.validMoves = self.gameState.getValidMoves()
                                if move in self.validMoves:
                                    print(f"Move: {move.start_row, move.start_col} -> {move.end_row, move.end_col}")
                                    self.captured = self.gameState.board[releaseRow][releaseCol] != "--"
                                    promotion_piece = 'Q' 
                                    if move.is_pawn_promotion and human_turn:
                                        promotion_piece = Animation.showPromotionOptions(self,releaseRow, releaseCol, move.piece_moved[0])
                                        move.promotion_choice = promotion_piece
                                    
                                    self.gameState.makeMove(move, promotion_piece)
                                    
                                    if is_castle:
                                        Animation.handleCastlingDisplay(self, move)
                                        
                                    self.validMoves = self.gameState.getValidMoves()
                                    
                                    self.playSound()
                                    self.move_undone = False


                            self.dragger.undragPiece()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z:
                            self.gameState.undoMove()
                            self.validMoves = self.gameState.getValidMoves()
                            self.move_undone = True
                            self.game_over = False
                            if self.ai_thinking:
                                self.move_finder_process.terminate()
                                self.ai_thinking = False
                        if event.key == pygame.K_r:
                            self.gameState = GameState()
                            self.validMoves = self.gameState.getValidMoves()
                            self.dragger.undragPiece()
                            self.game_over = False
                            if self.ai_thinking:
                                self.move_finder_process.terminate()
                                self.ai_thinking = False
                            self.move_undone = True
                        if event.key == pygame.K_n:
                            self.changeTheme()
                    

                if self.gameState.checkmate:
                    self.game_over = True
                    if self.gameState.white_to_move:
                        Animation.drawEndGameText(self, "Black wins by checkmate")
                    else:
                        Animation.drawEndGameText(self, "White wins by checkmate")

                elif self.gameState.stalemate:
                    self.game_over = True
                    print("Stalemate")
                    Animation.drawEndGameText(self, "Game ended in stalemate")

                self.clock.tick(FPS)
                pygame.display.update()
    
    
            
    def highlightChecks(self):
        if self.gameState.inCheck():  
            king_row, king_col = self.gameState.white_king_location if self.gameState.white_to_move else self.gameState.black_king_location
            
            # Tính toán alpha (độ trong suốt) với hiệu ứng nhạt hơn
            flash_speed = 0.004  # Giảm tốc độ nhấp nháy
            alpha = int(80 + 60 * math.sin(pygame.time.get_ticks() * flash_speed))  # Giảm biên độ
            
            # Màu đỏ nhạt với alpha thay đổi
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((255, 100, 100, alpha))  # Màu đỏ nhạt hơn
            
            self.mainScreen.blit(s, (king_col * SQUARE_SIZE, king_row * SQUARE_SIZE))
            
            # Vẽ thêm viền mờ để nổi bật
            border_alpha = min(150, alpha + 50)  
            border_color = (255, 150, 150, border_alpha) 
            border_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, border_color, (0, 0, SQUARE_SIZE, SQUARE_SIZE), 2) 
            self.mainScreen.blit(border_surface, (king_col * SQUARE_SIZE, king_row * SQUARE_SIZE))
            
    def drawGameState(self):
        self.drawBoard()
        Animation.showLastMove(self)
        self.showPieces()
    
    def drawBoard(self):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg[0] if (row + col) % 2 == 0 else theme.bg[1]
                pygame.draw.rect(self.mainScreen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if col == 0:
                    color = theme.bg[1] if row % 2 == 0 else theme.bg[0]
                    text = self.config.font.render(str(8 - row), 1, color)
                    self.mainScreen.blit(text, (5, 5 + row * SQUARE_SIZE))
                if row == 7:
                    color = theme.bg[0] if col % 2 == 0 else theme.bg[1]
                    text = self.config.font.render(chr(97 + col), 1, color)
                    self.mainScreen.blit(text, (col * SQUARE_SIZE + SQUARE_SIZE - 18, HEIGHT - 18))
                    
    def showPieces(self):
        board = self.gameState.board
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != "--":
                    if not (self.dragger.dragging and row == self.dragger.initialRow and col == self.dragger.initialCol):
                        pieceImg = self.imageSmall[piece]
                        self.mainScreen.blit(pieceImg, (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))
    
    def loadImages(self):
        for piece in PIECES:
            self.imageSmall[piece] = pygame.image.load(f'./assets/images/imgs-80px/{piece}.png')
            self.imageBig[piece] = pygame.image.load(f'./assets/images/imgs-128px/{piece}.png')
            

    
    def playSound(self):
        if self.captured:
            self.config.captureSound.play()
            self.captured = False
        else:
            if len(self.gameState.move_log) > 0 and self.gameState.move_log[-1].is_castle_move:
                if hasattr(self.config, 'castleSound'):
                    self.config.castleSound.play()
                else:
                    self.config.moveSound.play()
            else:
                self.config.moveSound.play()
                
    def changeTheme(self):
        self.config.changeTheme()
        
    def setHover(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            self.hoveredSquare = (row, col)
        else:
            self.hoveredSquare = None
            

        
if __name__ == "__main__":
    g = Game()
    g.mainLoop()