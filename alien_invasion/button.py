import pygame.font


class Button:

    def __init__(self, ai_game, msg):
        """Initialize attributes of the button"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
#         Set the sizes and the properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255,255)
        self.font = pygame.font.SysFont(None, 48)
#         Create object rect of the button and set it to center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
#         The message should appear only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn the text to the picture and set it to the center of the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        pygame.display.flip()  # Update the screen

    def draw_button(self):
#         Draw the empty button and then, the message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)




