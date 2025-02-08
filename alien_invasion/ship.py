import time
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
	"""Class for ship management"""

	def __init__(self, ai_game):
		"""Initialize ship and set the starting point"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		# Download the image of the ship and get his RECT
		self.image = pygame.image.load('image/ship1.bmp')
		self.rect = self.image.get_rect()

		# Create each new ship at the bottom of the screen (in the center)
		self.rect.midbottom = self.screen_rect.midbottom

		# Save a decimal value for the horizontal position of the ship
		self.x = float(self.rect.x)

		# Moving indicator
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Update the current position of the ship based on the moving indicator"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed
		# Update the object RECT with SELF.X
		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship in his current location"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Center the ship on the screen"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
		# self.image = pygame.image.load('image/ship1.bmp')

	def explode(self):
		"""Show explosion, then start a timer to remove the alien after 1 second"""
		self.image = pygame.image.load("image/boom2.jpg")  # Set explosion image
		self.screen.blit(self.image, self.rect)  # Force update
		pygame.display.flip()  # Update display to show explosion
		time.sleep(0.5)  # Wait for 1 second (non-blocking in main loop)

		self.image = pygame.image.load('image/ship1.bmp')  # Reset to normal image
