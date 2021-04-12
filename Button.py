import pygame


class Button():
	font = pygame.font.Font("title_font.ttf", 20)

	def __init__(self, name, x, y, width, height, text, color1=(128, 128, 128), color2=(100, 100, 100), text_color=(0, 0, 0), command=None):
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.text_color = text_color
		self._text_surface = Button.font.render(self.text, True, self.text_color)
		self.color1 = color1
		self.color2 = color2
		self.command = command

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.disabled = False

	def draw(self, surface):
		if(not self.disabled):
			mouse_pos = pygame.mouse.get_pos()

			if(not self.rect.collidepoint(mouse_pos)):
				pygame.draw.rect(surface, self.color1, self.rect)
			else:
				pygame.draw.rect(surface, self.color2, self.rect)

			surface.blit(self._text_surface, (self.x + self.width // 2 - self._text_surface.get_width() // 2, self.y + self.height // 2 - self._text_surface.get_height() // 2))

	def attach_command(self, command):
		self.command = command

	def execute(self, args):
		if(not self.disabled):
			if(self.command is not None):
				self.command(*args)

	def change_text_color(self, color):
		self.text_color = color

		# rerendering the button text
		self._text_surface = Button.font.render(self.text, True, self.text_color)
