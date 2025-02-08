import sys
import pygame
import random
import time
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
	"""General class that manages the game's resources and behavior."""

	def __init__(self):
		"""Initialize the game, create game resources."""
		pygame.init()
		pygame.mixer.init()  # Initialize the mixer for sound

		self.settings = Settings()
		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		# Load and play background music
		pygame.mixer.music.load("background_music1.mp3")  # Replace with your music file
		pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
		pygame.mixer.music.play(-1)  # -1 makes it loop indefinitely

		# Adjust the number of stars
		self.stars = [(random.randint(0, self.settings.screen_width),
		               random.randint(0, self.settings.screen_height))
		              for _ in range(150)]

		# Create an instance to save the game statistic and the scoreboard oon the screen
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()
		self.music_paused = False  # Track music state
		# 	Create the Play button
		self.play_button = Button(self, "Play")

	def run_game(self):
		"""Start the main game loop."""
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			else:
				self.sb.show_starting_message()  # Show the starting message
				self.play_button.draw_button()

			self._update_screen()

	def _check_events(self):
		"""Monitor/check mouse and keyboard events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start the new game when the player hits the Play button"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked:
			# Cancel the statistic of the game
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			# Rid of surplus of aliens and bullets.
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			self.aliens.empty()
			self.bullets.empty()
			# Create a new fleet and set the ship to the center
			self._create_fleet()
			self.ship.center_ship()
			# 		Hide the mouse on the screen
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		"""React on pressing a key."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_m:
			self._toggle_music()  # Toggle music on/off

	def _check_keyup_events(self, event):
		"""React when the key is released."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _toggle_music(self):
		"""Pause or unpause the music when 'M' is pressed."""
		if self.music_paused:
			pygame.mixer.music.unpause()
		else:
			pygame.mixer.music.pause()
		self.music_paused = not self.music_paused  # Toggle the state

	def _fire_bullet(self):
		"""Create a new bullet and add it to the group of bullets."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update bullet positions and remove bullets that disappear."""
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""Checks if a bullet collides with aliens and changes their image to an explosion"""
		for bullet in self.bullets.sprites():  # Checking all the bullets
			# If there are any collision between bullet and any alien
			alien_hit = pygame.sprite.spritecollideany(bullet, self.aliens)
			if alien_hit and not alien_hit.hit:  # Add the checking whether the alien was hit
				self._handle_alien_hit(alien_hit, bullet)

		if not self.aliens:
			self.start_new_level()

	def _handle_alien_hit(self, alien, bullet):
		"""Handles logic when an alien is hit."""
		alien.hit = True  # Check whether the alien receive the hit
		self.stats.score += self.settings.alien_points
		self.sb.prep_score()
		self.sb.check_high_score() # Checking the picture of the alien to explosion picture
		alien.explode()   # Calling a method to change an image to an explosion
		self.bullets.remove(bullet)  # Delete the bullet after collision
		alien.explode_time = time.time()   # Start the explosion timer

	def start_new_level(self):
		"""Starts a new level when all aliens are destroyed."""
		self.bullets.empty()
		self._create_fleet()
		self.settings.increase_speed()
		self.stats.level += 1
		self.sb.prep_level()

	def _update_aliens(self):
		"""Check whether the fleet is on the edge and update alien positions."""
		self._check_fleet_edges()
		self.aliens.update()
		# Search for the collisions between bullets and aliens
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		# Search whether any alien reach the bottom of the screen
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""React on collision between alien and ship"""
		if self.stats.ships_left > 0:
			# 	Decrease the ships_left. (initially the limit is 3)
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			# 	Decrease the surplus of the aliens and bullets
			self.ship.explode()
			self.aliens.empty()
			self.bullets.empty()
			# 	Create the new fleet and put the new ship to the center
			self._create_fleet()
			self.ship.center_ship()
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)
			self.sb.show_starting_message()
			self.play_button.draw_button()

	def _check_aliens_bottom(self):
		"""Check whether the alien reach the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# 			React the same way the ship was hit
				self._ship_hit()
				break

	def _create_fleet(self):
		"""Create a fleet of aliens."""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
		number_rows = available_space_y // (2 * alien_height)

		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and set its position."""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""React if an alien reaches the edge of the screen."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._check_fleet_direction()
				break

	def _check_fleet_direction(self):
		"""Drop all aliens down and change direction."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):
		"""Update the image on the screen and switch to a new screen."""
		self.screen.fill(self.settings.bg_color)
		for star in self.stars:
			pygame.draw.circle(self.screen, (255, 255, 255), star, 1.5)  # White stars with radius 2

		if self.stats.game_active:
			self.ship.blitme()  # Draw the ship
			for bullet in self.bullets.sprites():
				bullet.draw_bullet()  # Draw bullets
			self.aliens.draw(self.screen)  # Draw aliens

			# Draw the scoreboard
			self.sb.show_score()
		else:
			# Draw the "name of the game" message or button when the game is inactive
			self.sb.show_starting_message()  # Show Starting message
			self.play_button.draw_button()

		pygame.display.flip()  # Update the screen with the new drawings


if __name__ == '__main__':
	# Create the instance and start the game.
	ai = AlienInvasion()
	ai.run_game()
