import pygame

class Sound:
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)
    
    def play(self):
        pygame.mixer.Sound.play(self.sound)
        
        
class Theme:
    def __init__(self, lightBG, darkBG, lightTrace, darkTrace, lightMove, darkMove):
        self.bg = (lightBG, darkBG)
        self.trace = (lightTrace, darkTrace)
        self.move = (lightMove, darkMove)
        
        
        
class Config:
    def __init__(self):
        self.themes =[]
        self.indexTheme = 3
        self.setThemes()
        self.theme = self.themes[self.indexTheme]
        self.font = pygame.font.SysFont('monospace', 18, bold = True)
        self.moveSound = Sound("./assets/sounds/move.wav")
        self.captureSound = Sound("./assets/sounds/capture.wav")
    
    def changeTheme(self):
        self.indexTheme = (self.indexTheme + 1) % len(self.themes)
        self.theme = self.themes[self.indexTheme]
        
    def setThemes(self):
        pastel_pink  = Theme((255, 245, 250), (240, 180, 210), (255, 220, 240), (245, 190, 230), '#C86464', '#C84646')
        classic = Theme((240, 240, 240), (60, 60, 60), (200, 200, 200), (100, 100, 100), '#C86464', '#C84646')
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#C86464', '#C84646')
        purple = Theme((240, 230, 250), (120, 80, 160), (190, 170, 220), (150, 100, 200), '#C86464', '#C84646')
        red = Theme((245, 225, 225), (180, 80, 80), (250, 180, 180), (210, 100, 100), '#C86464', '#C84646')
        teal = Theme((230, 245, 245), (60, 160, 160), (130, 220, 220), (80, 190, 190), '#C86464', '#C84646')
        amber = Theme((250, 240, 210), (210, 160, 70), (255, 215, 120), (230, 180, 60), '#C86464', '#C84646')
        olive = Theme((235, 240, 210), (110, 130, 70), (190, 210, 120), (140, 170, 80), '#C86464', '#C84646')
        self.themes = [pastel_pink, classic, green, brown, blue, gray, purple, red, teal, amber, olive]
        