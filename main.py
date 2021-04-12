import pygame
from sys import exit as EXIT
import themes
from themes import themes_list

pygame.init()
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)

from Textbox import Textbox
from Button import Button


def invoke_timer(hr, min, sec):
	global total_seconds, timer_status, timer_set_text, timer_running_text, starting_ticks
	timer_status = "running"
	starting_ticks = pygame.time.get_ticks()

	button_start.disabled = True
	button_cancel.disabled = False

	timer_set_text = Textbox.font.render(f"Timer Set for: {hr} : {min} : {sec}", True, selected_theme["timersetcolor"])
	timer_running_text = Textbox.font.render(f"{hr} : {min} : {sec}", True, selected_theme["timerrunningcolor"])

	seconds = hr * 3600 + min * 60 + sec
	total_seconds = seconds


def up_timer():
	global timer_status, timer_set_text
	timer_status = "up"

	timer_set_text = Textbox.render("TIME UP!", True, (255, 0, 0))


def stop_timer():
	global total_seconds, timer_status, timer_ringing, timer_set_text, timer_running_text, alarm_stopped

	timer_status = "stopped"
	timer_ringing = True
	total_seconds = 0

	# playing timer ringing sound
	pygame.mixer.music.play(-1)

	button_start.disabled = False
	button_cancel.disabled = True

	timer_set_text = Textbox.font.render("", True, selected_theme["timersetcolor"])
	timer_running_text = Textbox.font.render("", True, selected_theme["timerrunningcolor"])


def cancel_timer():
	global total_seconds, timer_status, timer_set_text, timer_running_text

	timer_status = "stopped"
	total_seconds = 0

	button_start.disabled = False
	button_cancel.disabled = True

	timer_set_text = Textbox.font.render("", True, selected_theme["timersetcolor"])
	timer_running_text = Textbox.font.render("", True, selected_theme["timerrunningcolor"])


def stop_timer_sound():
	global timer_ringing

	timer_ringing = False

	# stoping timer ringing sound
	pygame.mixer.music.stop()


def switch_theme():
	global selected_theme
	global title_text, switch_theme_text, hour_text, min_text, sec_text, timer_set_text, timer_running_text

	ind = themes_list.index(selected_theme)

	if(ind == len(themes_list) - 1):
		selected_theme = themes_list[0]
	else:
		selected_theme = themes_list[ind + 1]

	# rerendering text(s)
	title_text = title_font.render("Countdown Timer", True, selected_theme["titlecolor"])
	switch_theme_text = theme_font.render("T : Switch Theme", True, selected_theme["switchthemecolor"])
	hour_text = time_font.render("HOUR", True, selected_theme["hourcolor"])
	min_text = time_font.render("MIN", True, selected_theme["mincolor"])
	sec_text = time_font.render("SEC", True, selected_theme["seccolor"])
	timer_set_text = Textbox.font.render("", True, selected_theme["timersetcolor"])
	timer_running_text = Textbox.font.render("", True, selected_theme["timerrunningcolor"])

	# changing button(s) colors
	button_start.color1 = selected_theme["buttonstartcolor1"]
	button_start.color2 = selected_theme["buttonstartcolor2"]
	button_start.change_text_color(selected_theme["buttontextcolor"])
	button_cancel.color1 = selected_theme["buttoncancelcolor1"]
	button_cancel.color2 = selected_theme["buttoncancelcolor2"]
	button_cancel.textcolor = selected_theme["buttontextcolor"]
	button_cancel.change_text_color(selected_theme["buttontextcolor"])


def convert_time(seconds):
	minutes = seconds // 60
	final_seconds = seconds % 60

	hours = minutes // 60
	final_minutes = minutes % 60

	return hours, final_minutes, final_seconds


SCREENWIDTH, SCREENHEIGHT = 900, 600
FPS = 15

game_display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Countdown Timer")
CLOCK = pygame.time.Clock()

selected_theme = themes.DARK_THEME

timer_status = "stopped"
timer_ringing = False
total_seconds = 0
starting_ticks = None
alarm_stopped = True

# font(s)
title_font = pygame.font.Font("title_font.ttf", 50)
theme_font = pygame.font.Font("title_font.ttf", 30)
time_font = pygame.font.Font("title_font.ttf", 25)

# UI text(s)
title_text = title_font.render("Countdown Timer", True, selected_theme["titlecolor"])
title_text_width = title_text.get_width()
title_text_height = title_text.get_height()
switch_theme_text = theme_font.render("T : Switch Theme", True, selected_theme["switchthemecolor"])

hour_text = time_font.render("HOUR", True, selected_theme["hourcolor"])
min_text = time_font.render("MIN", True, selected_theme["mincolor"])
sec_text = time_font.render("SEC", True, selected_theme["seccolor"])

timer_set_text = Textbox.font.render("", True, selected_theme["timersetcolor"])
timer_running_text = Textbox.font.render("", True, selected_theme["timerrunningcolor"])

time_up_text = Textbox.font.render("TIME UP!", True, (255, 0, 0))

# loading asset(s)
# image(s)
alarm_clock_logo = pygame.transform.scale(pygame.image.load("alarm_clock.png").convert_alpha(), (350, 350))
alarm_clock_logo_width = alarm_clock_logo.get_width()

# sound(s) / music(s)
time_up_music = pygame.mixer.music.load("alarm_tone_1.wav")
button_sound = pygame.mixer.Sound("button_sound.wav")

# creating textbox(s)
textbox_hr = Textbox(x=0+150,
						y=300,
						width=75,
						height=75,
						type="hr")
textbox_min = Textbox(x=0 + 150 + 75 + 10,
						y=300,
						width=75,
						height=75,
						type="min")
textbox_sec = Textbox(x=0 + 150 + 75 * 2 + 10 * 2,
						y=300, 
						width=75,
						height=75,
						type="sec")

textbox_list = [textbox_hr, textbox_min, textbox_sec]

# creating button(s)
button_start = Button(
					name="StartTimer",
					x=textbox_min.x + textbox_min.width // 2 - 75,
					y=textbox_min.y + textbox_min.width + 50,
					width=150,
					height=40,
					text="Start Timer",
					color1=selected_theme["buttonstartcolor1"],
					color2=selected_theme["buttonstartcolor2"],
					text_color=selected_theme["buttontextcolor"]
					)
button_start.attach_command(invoke_timer)
button_cancel = Button(
					name="CancelTimer",
					x=SCREENWIDTH - 350 + alarm_clock_logo_width // 2 - 75,
					y=SCREENHEIGHT - 75,
					width=150,
					height=40,
					text="Cancel Timer",
					color1=selected_theme["buttoncancelcolor1"],
					color2=selected_theme["buttoncancelcolor2"],
					text_color=selected_theme["buttontextcolor"],
					)
button_cancel.disabled = True
button_cancel.attach_command(cancel_timer)

button_list = [button_start, button_cancel]

allowed_keys = [eval("pygame.K_" + str(i)) for i in range(0, 10)]

run = True
while run:
	# ticking the FPS
	CLOCK.tick(FPS)

	# event section start
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			pygame.quit()
			EXIT()
		if(event.type == pygame.MOUSEBUTTONUP):
			if(timer_ringing):
				stop_timer_sound()
			else:
				if(event.button == 4):          # mouse scroll up
					for textbox in textbox_list:
						if(textbox.rect.collidepoint(event.pos) and int(textbox.text) > 0):
							# play button sound
							button_sound.play()

							old_text = textbox.text
							new_text = str(int(textbox.text) - 1)
							textbox.update_text(new_text)
							break
				elif(event.button == 5):          # mouse scroll down
					for textbox in textbox_list:
						if(textbox.rect.collidepoint(event.pos) and int(textbox.text) < 60):
							# play button sound
							button_sound.play()

							old_text = textbox.text
							new_text = str(int(textbox.text) + 1)
							textbox.update_text(new_text)
							break
				elif(event.button == 1):         # mouse click 1
					collision = False
					for button in button_list:
						if(button.rect.collidepoint(event.pos)):
							# play button sound
							if(not button.disabled):
								button_sound.play()

							collision = True
							if(button.name == "StartTimer"):
								button.execute([int(textbox_hr.text), int(textbox_min.text), int(textbox_sec.text)])
							elif(button.name == "CancelTimer"):
								button.execute([])
							break

					if(not collision):
						for textbox in textbox_list:
							if(textbox.rect.collidepoint(event.pos)):
								collision = True
								Textbox.select_textbox(textbox=textbox, textbox_list=textbox_list)
								break
						else:
							textbox.select_textbox(textbox_list=textbox_list, reverse=True)
		if(event.type == pygame.KEYDOWN):
			if(timer_ringing):
				stop_timer_sound()
			else:
				if(timer_status == "stopped" and event.key == pygame.K_t):
					switch_theme()

			for textbox in textbox_list:
				if(textbox.selected and event.key in allowed_keys):
					textbox.update_text(str(event.key - 48), keyboard=True)

	# event section end

	# filling the display surface
	if(not timer_ringing):
		game_display.fill(selected_theme["bgcolor"])
	else:
		game_display.fill(selected_theme["timeupbgcolor"])


	# drawing the outline rectangle
	pygame.draw.rect(game_display, selected_theme["outlinecolor"], (0, 0, SCREENWIDTH, SCREENHEIGHT), 10)

	# displaying the time up text if required
	if(timer_ringing):
		game_display.blit(time_up_text, (textbox_min.x + textbox_min.width // 2 - time_up_text.get_width() // 2, 150))

	# displaying the alarm clock logo
	game_display.blit(alarm_clock_logo, (SCREENWIDTH - 350, 20 + title_text_height + 40))

	# displaying the title and other text(s)
	game_display.blit(title_text, (SCREENWIDTH // 2 - title_text_width // 2, 20))
	game_display.blit(hour_text, (textbox_hr.x + textbox_hr.width // 2 - hour_text.get_width() // 2, textbox_hr.y - 50))
	game_display.blit(min_text, (textbox_min.x + textbox_min.width // 2 - min_text.get_width() // 2, textbox_min.y - 50))
	game_display.blit(sec_text, (textbox_sec.x + textbox_sec.width // 2 - sec_text.get_width() // 2, textbox_sec.y - 50))

	# drawing the seperator line(s)
	pygame.draw.line(game_display, selected_theme["seperatorcolor"], (0 + 100, 20 + title_text_height + 20), (SCREENWIDTH - 100, 20 + title_text_height + 20), 2)
	pygame.draw.line(game_display, selected_theme["seperatorcolor"], (SCREENWIDTH - 350 - 20, 20 + title_text_height + 40), (SCREENWIDTH - 350 - 20, 20 + title_text_height + 40 + 350), 2)
	pygame.draw.line(game_display, selected_theme["seperatorcolor"], (0 + 100, 20 + title_text_height + 40 + 350 + 20), (SCREENWIDTH - 350 - 20, 20 + title_text_height + 40 + 350 + 20), 2)

	# displaying the switch theme information
	game_display.blit(switch_theme_text, (0 + 20, SCREENHEIGHT - switch_theme_text.get_height() - 20))

	# managing textboxes
	for textbox in textbox_list:
		textbox.draw(game_display, color1=selected_theme["textboxcolor1"], color2=selected_theme["textboxcolor2"])
		textbox.textbox_events()

	# managing buttons
	for button in button_list:
		button.draw(game_display)

	# displaying timer text(s) and message(s)
	if(timer_status == "running"):
		game_display.blit(timer_set_text, (textbox_min.x + textbox_min.width // 2 - timer_set_text.get_width() // 2, 150))
		game_display.blit(timer_running_text, (button_cancel.x + button_cancel.width // 2 - timer_running_text.get_width() // 2, button_cancel.y - 75))

		if(pygame.time.get_ticks() - starting_ticks >= 1000):
			starting_ticks = pygame.time.get_ticks()
			total_seconds -= 1
			h, m, s = convert_time(total_seconds)
			timer_running_text = Textbox.font.render(f"{h} : {m} : {s}", True, selected_theme["timerrunningcolor"])

			if(total_seconds <= 0):
				stop_timer()

	# updating the main display surface
	pygame.display.update()
