import pygame
from Const import *
from Config import *
from Const import *
import sys
from ChessEngine_Local import *
import math

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initialRow = 0
        self.initialCol  = 0


    def updateBlit(self, surface, piece):
        img = pygame.image.load(f'./assets/images/imgs-128px/{piece}.png')
        img_center = (self.mouseX, self.mouseY)
        texture_rect = img.get_rect(center=img_center)
        surface.blit(img, texture_rect)


    def updateMouse(self, pos):
        self.mouseX, self.mouseY = pos 
        
        
    def saveInitial(self, pos):
        self.initialRow = pos[1] // SQUARE_SIZE
        self.initialCol  = pos[0] // SQUARE_SIZE

    def dragPiece(self, piece):
        self.piece = piece
        self.dragging = True

    def undragPiece(self):
        self.piece = None
        self.dragging = False
class Animation:
    def showPromotionOptions(game, row, col, color):
        boardSurface = game.mainScreen.copy()
        
        promotion_x = col * SQUARE_SIZE
        promotion_y = row * SQUARE_SIZE
        highlightAlpha = 0
        while highlightAlpha < 180:
            game.mainScreen.blit(boardSurface, (0, 0))
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill((255, 255, 100, highlightAlpha))  # Màu vàng nhạt
            game.mainScreen.blit(highlight, (promotion_x, promotion_y))
            pygame.draw.rect(game.mainScreen, (255, 215, 0), 
                            (promotion_x, promotion_y, SQUARE_SIZE, SQUARE_SIZE), 3)
            
            highlightAlpha += 10
            pygame.display.update()
            game.clock.tick(FPS)
        panelWidth  = 240
        panelHeight  = 100
        
        # Xác định vị trí panel 
        if row < 4: 
            panel_y = promotion_y + SQUARE_SIZE + 10
        else: 
            panel_y = promotion_y - panelHeight  - 10
        panel_y = max(10, min(HEIGHT - panelHeight  - 10, panel_y))

        panel_x = max(10, min(WIDTH - panelWidth  - 10, promotion_x - (panelWidth  - SQUARE_SIZE)/2))

        start_x = WIDTH + panelWidth 
        current_x = start_x
        target_x = panel_x
        
        while current_x > target_x:
            game.mainScreen.blit(boardSurface, (0, 0))
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill((255, 255, 100, 180))
            game.mainScreen.blit(highlight, (promotion_x, promotion_y))
            pygame.draw.rect(game.mainScreen, (255, 215, 0), 
                            (promotion_x, promotion_y, SQUARE_SIZE, SQUARE_SIZE), 3)
            
            panel = pygame.Surface((panelWidth , panelHeight ), pygame.SRCALPHA)
            panel.fill((240, 240, 240, 200)) 

            pygame.draw.rect(panel, (70, 70, 70, 230), (0, 0, panelWidth , panelHeight ), 2)
            
            current_x -= 20
            if current_x < target_x:
                current_x = target_x
                
            game.mainScreen.blit(panel, (current_x, panel_y))
            pygame.display.update()
            game.clock.tick(FPS)
        
        panel = pygame.Surface((panelWidth , panelHeight ), pygame.SRCALPHA)
        panel.fill((240, 240, 240, 200))
        pygame.draw.rect(panel, (70, 70, 70, 230), (0, 0, panelWidth , panelHeight ), 2)
        
        font = pygame.font.SysFont("monospace", 14, True)
        title = font.render("Chọn quân cờ phong cấp", True, (0, 0, 0))
        title_rect = title.get_rect(center=(panelWidth  // 2, 15))
        panel.blit(title, title_rect)
        
        pieceSize = 40
        piece_y = panelHeight  // 2 + 5
        spacing = 10
        pieces = ['Q', 'R', 'B', 'N']
        pieceRects = []
        total_width = 4 * pieceSize + 3 * spacing
        start_piece_x = (panelWidth  - total_width) // 2
        
        for i, piece in enumerate(pieces):
            piece_x = start_piece_x + i * (pieceSize + spacing)
            pieceRect = pygame.Rect(piece_x, piece_y - 15, pieceSize, pieceSize)
            pieceRects.append(pieceRect)

            pygame.draw.rect(panel, (200, 200, 200, 180), pieceRect)
            pygame.draw.rect(panel, (100, 100, 100, 230), pieceRect, 2)
            
            pieceImage  = game.imageSmall[f"{color}{piece}"]
            pieceImage  = pygame.transform.scale(pieceImage , (pieceSize - 10, pieceSize - 10))
            panel.blit(pieceImage , (piece_x + 5, piece_y - 15 + 5))
        

        game.mainScreen.blit(panel, (panel_x, panel_y))
        pygame.display.update()

        waiting  = True
        chosenPiece = 'Q' 
        hoveredPiece = -1
        
        while waiting :
            mousePosition = pygame.mouse.get_pos()
            positionRelative = (mousePosition[0] - panel_x, mousePosition[1] - panel_y)

            currentHover  = -1
            for i, rect in enumerate(pieceRects):
                if rect.collidepoint(positionRelative) and panel_x <= mousePosition[0] <= panel_x + panelWidth  and panel_y <= mousePosition[1] <= panel_y + panelHeight :
                    currentHover  = i
                    break

            if currentHover  != hoveredPiece:
                hoveredPiece = currentHover 

                game.mainScreen.blit(boardSurface, (0, 0))
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill((255, 255, 100, 180))
                game.mainScreen.blit(highlight, (promotion_x, promotion_y))
                pygame.draw.rect(game.mainScreen, (255, 215, 0), 
                                (promotion_x, promotion_y, SQUARE_SIZE, SQUARE_SIZE), 3)
 
                panel = pygame.Surface((panelWidth , panelHeight ), pygame.SRCALPHA)
                panel.fill((240, 240, 240, 200))
                pygame.draw.rect(panel, (70, 70, 70, 230), (0, 0, panelWidth , panelHeight ), 2)

                panel.blit(title, title_rect)

                for i, piece in enumerate(pieces):
                    piece_x = start_piece_x + i * (pieceSize + spacing)
                    pieceRect = pieceRects[i]
                    
                    if i == hoveredPiece:
                        pygame.draw.rect(panel, (180, 210, 255, 230), pieceRect)
                        pygame.draw.rect(panel, (0, 120, 215, 255), pieceRect, 2)
                        
                    else:
                        pygame.draw.rect(panel, (200, 200, 200, 180), pieceRect)
                        pygame.draw.rect(panel, (100, 100, 100, 230), pieceRect, 2)
                    
                    pieceImage  = game.imageSmall[f"{color}{piece}"]
                    pieceImage  = pygame.transform.scale(pieceImage , (pieceSize - 10, pieceSize - 10))
                    panel.blit(pieceImage , (piece_x + 5, piece_y - 15 + 5))
                    

                game.mainScreen.blit(panel, (panel_x, panel_y))
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        for i, rect in enumerate(pieceRects):
                            if rect.collidepoint(positionRelative) and panel_x <= mousePosition[0] <= panel_x + panelWidth  and panel_y <= mousePosition[1] <= panel_y + panelHeight :
                                chosenPiece = pieces[i]
                                pygame.draw.rect(panel, (160, 190, 255, 255), pieceRect)
                                pygame.draw.rect(panel, (0, 80, 185, 255), pieceRect, 2)
                                game.mainScreen.blit(panel, (panel_x, panel_y))
                                pygame.display.update()
                                pygame.time.delay(100)
                                
                                waiting  = False
                                break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        chosenPiece = 'Q'
                        waiting  = False
                    elif event.key == pygame.K_r:
                        chosenPiece = 'R'
                        waiting  = False
                    elif event.key == pygame.K_b:
                        chosenPiece = 'B'
                        waiting  = False
                    elif event.key == pygame.K_n:
                        chosenPiece = 'N'
                        waiting  = False
                    elif event.key == pygame.K_ESCAPE:
                        chosenPiece = 'Q'
                        waiting  = False
            
            game.clock.tick(FPS)
        
        for alpha in range(200, 0, -20):
            game.mainScreen.blit(boardSurface, (0, 0))
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill((255, 255, 100, alpha))
            game.mainScreen.blit(highlight, (promotion_x, promotion_y))

            pygame.draw.rect(game.mainScreen, (255, 215, 0, alpha), 
                            (promotion_x, promotion_y, SQUARE_SIZE, SQUARE_SIZE), 3)

            panel = pygame.Surface((panelWidth , panelHeight ), pygame.SRCALPHA)
            panel.fill((240, 240, 240, alpha))
            pygame.draw.rect(panel, (70, 70, 70, alpha), (0, 0, panelWidth , panelHeight ), 2)
            game.mainScreen.blit(panel, (panel_x, panel_y))
            
            pygame.display.update()
            game.clock.tick(FPS)

        game.drawGameState()
        pygame.display.update()
        
        return chosenPiece


    def handleCastlingDisplay(game, move):
            """
            Hiệu ứng nhập thành
            """
            kingRowIndex = move.end_row
            if move.end_col - move.start_col == 2: 
                rookOldCol = 7
                rookNewCol  = move.end_col - 1
            else:  
                rookOldCol = 0
                rookNewCol  = move.end_col + 1
            
            oldColor = game.config.theme.bg[0] if (kingRowIndex + rookOldCol) % 2 == 0 else game.config.theme.bg[1]
            pygame.draw.rect(game.mainScreen, oldColor, 
                            (rookOldCol * SQUARE_SIZE, kingRowIndex * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            pieceColor  = "w" if move.piece_moved[0] == "w" else "b"
            rookPiece  = f"{pieceColor }R"
            game.mainScreen.blit(game.imageSmall[rookPiece ], 
                                (rookNewCol  * SQUARE_SIZE + 5, kingRowIndex * SQUARE_SIZE + 5))
            
            pygame.display.update() 
            
    def showHover(game):
        if game.hoveredSquare:
            color = (200, 200, 100)
            row, col = game.hoveredSquare
            rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(game.mainScreen, color, rect, width=3)
    
    def showLastMove(game):
        theme = game.config.theme
        if len(game.gameState.move_log) > 0:
            lastMove = game.gameState.move_log[-1]
            initial = lastMove.start_row, lastMove.start_col
            final = lastMove.end_row, lastMove.end_col
            
            for position in [initial, final]:
                color = theme.trace[0] if (position[0] + position[1]) % 2 == 0 else theme.trace[1]
                pygame.draw.rect(game.mainScreen, color, (position[1] * SQUARE_SIZE, position[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            if lastMove.is_castle_move:
                if lastMove.end_col - lastMove.start_col == 2:  
                    rookInitial = (lastMove.end_row, 7)
                    rookFinal  = (lastMove.end_row, lastMove.end_col - 1)
                else:  
                    rookInitial = (lastMove.end_row, 0)
                    rookFinal  = (lastMove.end_row, lastMove.end_col + 1)
                
                for position in [rookInitial, rookFinal ]:
                    color = theme.trace[0] if (position[0] + position[1]) % 2 == 0 else theme.trace[1]
                    pygame.draw.rect(game.mainScreen, color, (position[1] * SQUARE_SIZE, position[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def showMoves(game):
        theme = game.config.theme
        
        if game.dragger.dragging:
            piece = game.dragger.piece
            initialRow = game.dragger.initialRow
            initialCol  = game.dragger.initialCol 
            
            for move in game.validMoves:
                if move.start_row == initialRow and move.start_col == initialCol :
                    color = theme.move[0] if (move.end_row + move.end_col) % 2 == 0 else theme.move[1]
                    
                    if piece[1] == 'K' and abs(move.start_col - move.end_col) == 2:
                        rect = (move.end_col * SQUARE_SIZE, 
                               move.end_row * SQUARE_SIZE, 
                               SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(game.mainScreen, color, rect, width=3)
                        
                        if move.end_col > move.start_col:  
                            rookCol  = move.end_col - 1
                        else:  
                            rookCol  = move.end_col + 1
                        
                        rookRect = (rookCol  * SQUARE_SIZE, 
                                    move.end_row * SQUARE_SIZE, 
                                    SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(game.mainScreen, color, rookRect, width=3)
                    else:
                        if game.gameState.board[move.end_row][move.end_col] != "--":
                            rect = (move.end_col * SQUARE_SIZE, 
                                   move.end_row * SQUARE_SIZE, 
                                   SQUARE_SIZE, SQUARE_SIZE)
                            pygame.draw.rect(game.mainScreen, color, rect, width=3)
                        else:
                            center = (move.end_col * SQUARE_SIZE + SQUARE_SIZE//2, 
                                    move.end_row * SQUARE_SIZE + SQUARE_SIZE//2)
                            radius = SQUARE_SIZE // 4
                            pygame.draw.circle(game.mainScreen, color, center, radius)
    
    
    def showEndGameScreen(game, result_text, winner=None):
        board_surface = game.mainScreen.copy()
        
        try:
            if winner == "w":
                victorySound  = pygame.mixer.Sound('./assets/sounds/lose.wav')
            elif winner == "b":
                victorySound  = pygame.mixer.Sound('./assets/sounds/victory.wav')
            victorySound .play()
        except:
            print("Not found victory sound @@")
        
        for alpha in range(0, 100, 5):
            game.mainScreen.blit(board_surface, (0, 0))

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            game.mainScreen.blit(overlay, (0, 0))
            
            pygame.display.update()
            game.clock.tick(FPS)

        
        resultSizeFont = 48
        resultFont = pygame.font.SysFont("monospace", resultSizeFont, True)

        if winner == "w":
            main_text = "YOU WIN"
            color = (255, 255, 255)  # Trắng
        elif winner == "b":
            main_text = "YOU LOSE"
            color = (50, 50, 50)  # Đen
        else:
            main_text = "STALEMENT"
            color = (200, 200, 100)  # Vàng

        for size in range(resultSizeFont + 40, resultSizeFont - 5, -2):
            game.mainScreen.blit(board_surface, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            game.mainScreen.blit(overlay, (0, 0))
            
            tmpFont = pygame.font.SysFont("monospace", size, True)
            
            for offset in range(5, 0, -1):
                glowSurface = tmpFont.render(main_text, True, (color[0]//2, color[1]//2, color[2]//2))
                glowRect = glowSurface.get_rect(center=(WIDTH//2 + offset, HEIGHT//3 + offset))
                game.mainScreen.blit(glowSurface, glowRect)

            textSurface = tmpFont.render(main_text, True, color)
            textRect = textSurface.get_rect(center=(WIDTH//2, HEIGHT//3))
            game.mainScreen.blit(textSurface, textRect)
            
            pygame.display.update()
            game.clock.tick(FPS)
        
        reason_font = pygame.font.SysFont("monospace", 24)
        reason_text = result_text

        for alpha in range(0, 255, 10):
            game.mainScreen.blit(board_surface, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            game.mainScreen.blit(overlay, (0, 0))
            
            textSurface = resultFont.render(main_text, True, color)
            textRect = textSurface.get_rect(center=(WIDTH//2, HEIGHT//3))
            game.mainScreen.blit(textSurface, textRect)
            
            reasonSurface = reason_font.render(reason_text, True, (*color, alpha))
            reasonRect = reasonSurface.get_rect(center=(WIDTH//2, HEIGHT//3 + 60))
            game.mainScreen.blit(reasonSurface, reasonRect)
            
            pygame.display.update()
            game.clock.tick(FPS)
        

        instruction_font = pygame.font.SysFont("monospace", 18)
        instructions = [
            "Press R to play again",
            "Press ESC to exit"
        ]

        instructionSurfaces = []
        instructionRects = []
        
        for i, instruction in enumerate(instructions):
            instSurface = instruction_font.render(instruction, True, (200, 200, 200))
            instRect  = instSurface.get_rect(center=(WIDTH//2, HEIGHT*3//4 + i*30))
            instructionSurfaces.append(instSurface)
            instructionRects.append(instRect )

        for alpha in range(0, 255, 10):
            game.mainScreen.blit(board_surface, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            game.mainScreen.blit(overlay, (0, 0))
            
            game.mainScreen.blit(textSurface, textRect)

            game.mainScreen.blit(reasonSurface, reasonRect)

            for i, (surface, rect) in enumerate(zip(instructionSurfaces, instructionRects)):
                temp_surface = instruction_font.render(instructions[i], True, (200, 200, 200, alpha))
                game.mainScreen.blit(temp_surface, rect)
            
            pygame.display.update()
            game.clock.tick(FPS)

        blink_time = 0
        blink_rate = 30
        blink_state = True

        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.gameState = GameState()
                        game.validMoves = game.gameState.getValidMoves()
                        game.game_over = False
                        waiting_for_key = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            blink_time += 1
            if blink_time >= blink_rate:
                blink_time = 0
                blink_state = not blink_state

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            game.mainScreen.blit(overlay, (0, 0))
            game.mainScreen.blit(textSurface, textRect)
            game.mainScreen.blit(reasonSurface, reasonRect)
            if blink_state:
                for surface, rect in zip(instructionSurfaces, instructionRects):
                    game.mainScreen.blit(surface, rect)
            
            pygame.display.update()
            game.clock.tick(FPS)
        
        for alpha in range(100, 0, -5):
            game.mainScreen.blit(board_surface, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            game.mainScreen.blit(overlay, (0, 0))
            
            pygame.display.update()
            game.clock.tick(FPS)

    def drawEndGameText(game, result_text):

        winner = None
        if "White wins" in result_text or "Trắng thắng" in result_text:
            winner = "w"
        elif "Black wins" in result_text or "Đen thắng" in result_text:
            winner = "b"
        Animation.showEndGameScreen(game, result_text, winner)
        
    def highlightChecks(game ):
        if game .gameState.inCheck():  
            king_row, king_col = game .gameState.white_king_location if game .gameState.white_to_move else game .gameState.black_king_location
            
            # Tính toán alpha (độ trong suốt) với hiệu ứng nhạt hơn
            flash_speed = 0.004  # Giảm tốc độ nhấp nháy
            alpha = int(80 + 60 * math.sin(pygame.time.get_ticks() * flash_speed))  # Giảm biên độ
            
            # Màu đỏ nhạt với alpha thay đổi
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((255, 100, 100, alpha))  # Màu đỏ nhạt hơn
            
            game .mainScreen.blit(s, (king_col * SQUARE_SIZE, king_row * SQUARE_SIZE))
            
            # Vẽ thêm viền mờ để nổi bật
            border_alpha = min(150, alpha + 50)  
            border_color = (255, 150, 150, border_alpha) 
            border_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, border_color, (0, 0, SQUARE_SIZE, SQUARE_SIZE), 2) 
            game .mainScreen.blit(border_surface, (king_col * SQUARE_SIZE, king_row * SQUARE_SIZE))    
