import pygame
from pygame.sprite import Sprite
import time


class Alien(Sprite):
    """The class which represents one alien from the flot"""
    def __init__(self, ai_game):
        """Initialize the alien and set his initial position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load("image/picture1.bmp")
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        self.explode_time = None  # Time when explosion starts
        self.hit = False

    def check_edges(self):
        """Return TRUE if the alien is on the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def explode(self):
        """Show explosion, then start a timer to remove the alien after 1 second"""
        self.image = pygame.image.load("image/boom2.jpg")
        self.explode_time = time.time()  # Record the time of the explosion

    def update(self):
        """Update the alien state (check if it needs to be removed after explosion)"""
        # If the alien has exploded and 1 second has passed, remove the alien
        if self.explode_time and time.time() - self.explode_time > 0.2:  # 0.2 second after explosion
            self.kill()  # Remove the alien from the screen
        else:
            # Regular update of the alien's movement (left or right)
            self.x += (self.settings.alien_speed * self.settings.fleet_direction)
            self.rect.x = self.x
