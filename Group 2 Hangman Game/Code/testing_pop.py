#Importing python libraries required for game
import pygame
import random
import sys
#from button import Button

#Initialising imported libraries
pygame.init()

#Screen size information
screen_size = screen_width, screen_height = 1280, 720


autodetect_screen_info = pygame.display.Info()
detected_width = autodetect_screen_info.current_w
detected_height = autodetect_screen_info.current_h

if detected_width <= detected_height:
	win = pygame.display.set_mode(screen_size, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(screen_size, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)


clock = pygame.time.Clock()
FPS = 60


#RGB colours variables for easy indentification
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0,255)
GOLD = (255, 215, 0)
GRAY = (168, 169, 169)

#Fonts alloted for respective works (importing)
Font_a = pygame.font.Font("Fonts/LakkiReddy-Regular.ttf", 32) #Used for main game words
Font_b = pygame.font.Font("Fonts/Poppins.ttf", 28 ) #Used for Hindi alphabet in hints
Font_c = pygame.font.Font("Fonts/Ubuntu.ttf", 28) #Used for on screen instusctions
Font_d = pygame.font.Font("Fonts/VanDoesburg.ttf", 28) #Used to display score and lives
Font_e = pygame.font.Font("Fonts/TitilliumWeb-SemiBold.ttf", 28) #Used for keyboard letters
Font_f = pygame.font.Font("Fonts/VanDoesburg.ttf", 52)
instruction_message = Font_c.render("GUESS THE WORD WITH THE HELP OF HINT", True, GREEN)
instruction_exit = Font_c.render("PRESS ESC TO QUIT",True,RED)
#Sound effects alloted at perticular situations (importing)
win_fx = pygame.mixer.Sound("Sounds/win.wav")
lose_fx = pygame.mixer.Sound("Sounds/lose.wav")
alert_fx = pygame.mixer.Sound("Sounds/alert.wav")
#Images used around the game (imporing)
hangman_character = []
for i in range(7):
	character = pygame.image.load(f"Assets/hangman{i}.png")
	character = pygame.transform.scale(character, (330, 330))
	hangman_character.append(character)

BG = pygame.image.load("Assets/Background.png")	
opening_animation = pygame.image.load("Images/opening_animation.png")
opening_animation = pygame.transform.scale(opening_animation, (screen_width, screen_height))
main_background = pygame.image.load("Images/main_background.png")
main_background = pygame.transform.scale(main_background, (screen_width, screen_height))
gameover_background = pygame.image.load("Images/main_background_old.png")
gameover_background = pygame.transform.scale(gameover_background, (screen_width, screen_height))
################################################################################################################
####################################################################################################################
#assigning text document for play words (importing)
word_dict = {}
word_list = []
with open("Vocabulary/words easy.txt",encoding='utf-8') as file:
	for line in file.readlines():
		w, m = line.strip().split(":")
		word_dict[w.strip()] = m.strip()

def getWord():
	word = random.choice(list(word_dict.keys()))
	
	
	if word in word_list:
		
		return getWord()
	
	else:
		meaning = word_dict[word]
		return word.upper(), meaning
	
		
word, meaning = getWord()


current_word = Font_c.render(word, True,GOLD)
word_list.append(word)
guessed = ['' for i in range(len(word))]

#opening animation (fading style)	
class FadeScreen:
	def __init__(self, w, h, colour):
		self.surface = pygame.Surface((w, h))
		self.surface.fill(colour)
		self.alpha = 255
		self.surface.set_alpha(self.alpha)
		
	def update(self):
		self.alpha -= 2
		self.surface.set_alpha(self.alpha)
		
	def draw(self, x, y):
		win.blit(self.surface, (x,y))

class Button(pygame.sprite.Sprite):
	def __init__(self, text, x, y):
		super(Button, self).__init__()
		
		self.text = text
		self.image = Font_e.render(self.text, True, WHITE)
		self.rect = pygame.Rect(x, y, 60, 60)
		self.clicked = False
		
	def collision(self, pos):
		if pos and not self.clicked:
			if self.rect.collidepoint(pos):
				self.image = Font_e.render(self.text, True, GREEN)
				self.clicked = True
				return True, self.text
		return False
		
	def update(self):
		pygame.draw.rect(win, WHITE, self.rect, 5)
		win.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))
		
	def reset(self):
		self.clicked = False
		self.image = Font_e.render(self.text, True, WHITE)
		
btns = []
for i in range(26):
	text = f"{chr(65+i)}"
	x = 590 + ( i % 9 ) * 72
	y = 440 + (i // 9) * 72
	btns.append(Button(text, x, y))
	
#Creation and alloting mouse_positiontion for restart and quit button	
restart_img = Font_c.render("RESTART", True, WHITE)
quit_img = Font_c.render("QUIT", True, WHITE)
restart_rect = restart_img.get_rect()
restart_rect.x = screen_width - 550
restart_rect.y = screen_height - 120

quit_rect = quit_img.get_rect()
quit_rect.x  = screen_width - 840
quit_rect.y = screen_height - 120

# GAME ************************************************************************

lives = 6
score = 0
gameover = False
homepage = True

fadeScreen = FadeScreen(screen_width, screen_height, BLACK)

score_img = Font_d.render(f"Score {score}", True, GOLD)
lives_img = Font_d.render(f"Lives {lives}", True, GOLD)


running = True
while running:
	pos = None
	win.fill((0,0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

				
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			
	if homepage:
		if fadeScreen.alpha >= 0:
			fadeScreen.update()
			fadeScreen.draw(0,0)
			
			opening_animation.set_alpha(fadeScreen.alpha)
			win.blit(opening_animation, (screen_width - opening_animation.get_width() , screen_height - opening_animation.get_height()))
			
		else:
			homepage = False
		
	else:
		win.fill((0,0,0))
		win.blit(main_background,(0,0))
		hangman_current = hangman_character[6-lives]
		win.blit(hangman_current, (110,150))
		win.blit(score_img, (1050, 40))
		win.blit(lives_img, (1050, 80))
	
		# render buttons
		for btn in btns:
			btn.update()
			collision = btn.collision(pos) 
			if collision and not gameover:
				if collision[1] in word:
					for i in range(len(word)):
						if word[i] == collision[1]:
							guessed[i] = collision[1]
							
					if guessed.count('') == 0:
						previous_word = Font_c.render(word, True,GOLD)
						word, meaning = getWord()
						current_word = Font_c.render(word, True,GOLD)
						
						
						guessed = ['' for i in range(len(word))]
						word_list.append(word)
						
						win_fx.play()
						score += 1
						lives = 6

						score_img = Font_d.render(f"Score {score}", True, GOLD)
						lives_img = Font_d.render(f"Lives {lives}", True, GOLD)
						
						for btn in btns:
							btn.reset()	
						break
					

				else:
					lives -= 1
					lives_img = Font_d.render(f"Lives {lives}", True, GOLD)
					if lives == 2 and not gameover:
						alert_fx.play()
						win.blit(BG,(0,0))
					if lives == 0:
						gameover = True
						lose_fx.play()			
		if score >= 1:
			previous_word_text = Font_c.render("YOUR PRIOR GUESS:", True, GREEN)
			win.blit(previous_word_text,(40,600))
			win.blit(previous_word,(310,600))
		if lives <=2 and lives !=0:
			
			hint = Font_b.render(meaning, True, WHITE)
			win.blit(hint, (850,230))
			win.blit(instruction_message, (630, 190))
		# Render Dash and Characters
		for i in range(len(word)):
			x = screen_width // 2 - ((20 * len(word))// 10)
			x1, y1 = (x + 75 * i, screen_height // 2)
			x2, y2 = (x + 75 * i + 50, screen_height // 2)
			pygame.draw.line(win, (255,255,255), (x1, y1), (x2, y2), 5)
			
			if not gameover:
				char = Font_a.render(guessed[i], True, WHITE)
			else:
				char = Font_a.render(word[i], True, RED)
			win.blit(char, (x1 + 20, y1 - 40))
					
		# Render Top message and Hints
		#hint = Font_b.render(meaning, True, WHITE)
		#win.blit(hint, (850,230))
		#win.blit(instruction_message, (630, 190))
		instruction_message2 = Font_b.render("USE THE KEYS BELOW TO GUESS THE WORD:",True,WHITE)
		win.blit(instruction_message2,(630,150))
		win.blit(instruction_exit,(40,670))

		if gameover:
			#pygame.draw.rect(win, 'BLUE', [0, 0, 1280,960],0, 10)
			win.blit(gameover_background,(0,0))
			gameover_text = Font_f.render('GAME OVER', True, 'GOLD')
			gameover_word = Font_c.render('The correct word was:', True,'WHITE')
			win.blit(gameover_text, (455, 70))
			win.blit(score_img,(555,150))
			win.blit(gameover_word,(395,540))
			win.blit(current_word,(700,540))
			gameover_character = pygame.image.load(f"Assets/hangman6.png")
			gameover_character = pygame.transform.scale(gameover_character, (330, 330))
			win.blit(gameover_character,(475,200))

			

			win.blit(restart_img, restart_rect)
			win.blit(quit_img, quit_rect)
			pygame.draw.rect(win, RED, (restart_rect.x - 4, restart_rect.y - 4, 127, 43), 3)
			pygame.draw.rect(win, RED, (quit_rect.x - 5, quit_rect.y - 5, 78, 43), 3)
			
			if pos and restart_rect.collidepoint(*pos):
				score = 0
				lives = 6
				gameover = False
				
				word, meaning = getWord()
				current_word=Font_c.render(word, True,GOLD)
				guessed = ['' for i in range(len(word))]
				word_list = []
				word_list.append(word)
				
				for btn in btns:
					btn.reset()		
				score_img = Font_d.render(f"Score {score}", True, GOLD)
				lives_img = Font_d.render(f"Lives {lives}", True, GOLD)
				
			if pos and quit_rect.collidepoint(*pos):
				running = False
	if lives == 2:			
		pygame.draw.rect(win, RED, (0,0,screen_width,screen_height), 5)
	else:
		pygame.draw.rect(win, GOLD, (0,0,screen_width,screen_height), 5)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()
sys.exit()