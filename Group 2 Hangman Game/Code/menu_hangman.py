import pygame, sys
#from button import Button

pygame.init()
screen_size = screen_width, screen_height = 1280, 720

autodetect_screen_info = pygame.display.Info()
detected_width = autodetect_screen_info.current_w
detected_height = autodetect_screen_info.current_h

if detected_width <= detected_height:
	SCREEN = pygame.display.set_mode(screen_size, pygame.NOFRAME)
else:
	SCREEN = pygame.display.set_mode(screen_size, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
        
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

BG = pygame.image.load("Assets/Background.png")
BG = pygame.transform.scale(BG, (screen_width, screen_height))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Assets/font.ttf", size)

def play():
    while True:
        import testing_pop
        
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("PYTHON PROJECT GROUP 2:", True, "Black")
        ABHINAV = get_font(36).render("ABHINAV YADAV", True, "Blue")
        VARENYA = get_font(36).render("VARENYA GIRISH HEGDE", True, "Blue")
        YASH = get_font(36).render("YASHVARDHAN SHUKLA ", True, "Blue")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 150))
        ABHINAV_RECT = ABHINAV.get_rect(center=(640, 250))
        VARENYA_RECT = VARENYA.get_rect(center=(640, 300))
        YASH_RECT = YASH.get_rect(center=(640, 350))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(ABHINAV,ABHINAV_RECT)
        SCREEN.blit(VARENYA,VARENYA_RECT)
        SCREEN.blit(YASH,YASH_RECT)
        OPTIONS_BACK = Button(image=None, pos=(640, 660), 
                            text_input="BACK", font=get_font(36), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        pygame.draw.rect(SCREEN, (255,215,0), (0,0,screen_width,screen_height), 5)
        MENU_TEXT = get_font(100).render("HANGMAN GAME", True, "#ffd700")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Assets/Play Rect.png"), pos=(640, 250), 
                            text_input="START", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Assets/Options Rect.png"), pos=(640, 400), 
                            text_input="CREDITS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
pygame.quit()
sys.exit()