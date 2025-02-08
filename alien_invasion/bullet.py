import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
	def __init__(self, ai_game):
		"""Creating the bullet object in the current position of the ship"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

# 		Create a rect of the bullet in (0, 0) and set the right position
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

# 		Save position of the ball as a float value
		self.y = float(self.rect.y)

	def update(self):
		"""Draw the bullet up to the top of the screen"""
		self.y -= self.settings.bullet_speed
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw the bullet on the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)
