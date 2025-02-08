import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """The class which shows the score"""

    def __init__(self, ai_game):
        """Initialization of the attributes related to the score"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Setting the font to describe the score
        self.text_color = (200, 200, 200)
        self.font = pygame.font.SysFont(None, 48)

        self.heart_image = pygame.image.load('image/hart.jpg')
        self.heart_rect = self.heart_image.get_rect()

        # Prepare all score-related images
        self.prep_images()

    def prep_images(self):
        """Prepare all images related to score display"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Change the score to the picture"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Show the score on the right-top of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Show the score, level and ships on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Generate the record into the picture"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # Show the score on the center
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check whether new record is set up"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Change the string to the picture"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        # Set the level under the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships you still have"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = self.heart_image
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_starting_message(self):
        """Display 'Starting message' message with final score and replay prompt"""

        # Render  text as an image
        game_over_image = self.font.render("THIS IS THE ALIEN INVASION!", True, self.text_color, self.settings.bg_color)
        game_over_rect = game_over_image.get_rect(center=(self.screen_rect.centerx, 200))
        self.screen.blit(game_over_image, game_over_rect)

        # Render final score as an image
        score_text = f"Your total score is {self.stats.score}"
        score_image = self.font.render(score_text, True, self.text_color, self.settings.bg_color)
        score_rect = score_image.get_rect(center=(self.screen_rect.centerx, 280))
        self.screen.blit(score_image, score_rect)

        # Render 'Play Again' text as an image
        play_again_image = self.font.render("Do you want to play?", True, self.text_color, self.settings.bg_color)
        play_again_rect = play_again_image.get_rect(center=(self.screen_rect.centerx, 360))
        self.screen.blit(play_again_image, play_again_rect)

        pygame.display.flip()  # Update the screen
