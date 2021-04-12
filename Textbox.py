import pygame


class Textbox:
	selected_textbox = None
	font = pygame.font.Font("time_text_font.ttf", 50)

	def __init__(self, x, y, width, height, type):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.rect = pygame.Rect(x, y, width, height)

		self.text = "0"
		self._text_surface = Textbox.font.render(self.text, True, (0, 0, 0))
		self.type = type
		self.selected = False

	def draw(self, surface, color1=(255, 255, 255), color2=(128, 128, 128)):
		pygame.draw.rect(surface, color1, self.rect)     # inner rectangle

		if(not self.selected):                           # outer rectangle
			pygame.draw.rect(surface, color2, self.rect, 5)
		else:
			pygame.draw.rect(surface, (255, 0, 0), self.rect, 5)

		self._display_text(surface)    # blitting the text

	def _display_text(self, surface):
		surface.blit(self._text_surface, (self.rect.centerx - self._text_surface.get_width() // 2, self.rect.centery - self._text_surface.get_height() // 2))

	def update_text(self, text, keyboard=False):
		if(not keyboard):
			self.text = text
			self._text_surface = Textbox.font.render(self.text, True, (0, 0, 0))
		else:
			if(len(self.text) < 2 and self.text != "0"):
				self.text += text
				if(int(self.text) > 60):
					self.text = "60"
				self._text_surface = Textbox.font.render(self.text, True, (0, 0, 0))
			else:
				self.update_text(text)

	def textbox_events(self):
		pass

	@classmethod
	def select_textbox(cls, textbox=None, textbox_list=None, reverse=False):
		if(not reverse):
			for tb in textbox_list:
				if(tb.type == textbox.type):
					tb.selected = True
				else:
					tb.selected = False
		else:
			for tb in textbox_list:
				tb.selected = False
