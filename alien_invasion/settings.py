class Settings:
	# The class for saving all the game's settings
	def __init__(self):
		"""Initialize the constant settings"""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (18, 18, 51)
		# Setting up the ship
		self.ship_limit = 3
		# Setting the bullet
		self.bullet_width = 2.0
		self.bullet_height = 15
		self.bullet_color = (255, 255, 255)
		# Settings for aliens

# 		If the game should be speed up
		self.speedup_scale = 1.05
		self.initialize_dynamic_settings()
	# The increasing value for aliens
		self.score_scale = 1.5
	def initialize_dynamic_settings(self):
		"""Initialization of the changeable settings"""
		self.ship_speed = 1.5
		self.bullet_speed = 1.5
		self.alien_speed = 1.0
		self.bullets_allowed = 3
		self.alien_points = 10
		self.fleet_drop_speed = 10
		# fleet_direction 1 means turn on the right side on the screen by 1 and -1 -- turn left
		self.fleet_direction = 1

	def increase_speed(self):
		"""Increasing the speed limit and price for the aliens"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.bullets_allowed += 0.5
		self.fleet_drop_speed += 0.2

		self.alien_points = int(self.alien_points * self.score_scale)