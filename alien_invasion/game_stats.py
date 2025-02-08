class GameStats:
	"""Tracing the stats of the game"""

	def __init__(self, ai_game):
		"""Initialization of the statistic"""
		self.settings = ai_game.settings
		self.reset_stats()
		# Start game in inactive state.
		self.game_active = False
		self.high_score = 0

	def reset_stats(self):
		"""Initialize the statistic which can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1
