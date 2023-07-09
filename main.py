import pygame
import sys
import random
import math
import json
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Set up the window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Countdown: Press Tab to edit date")

# Set up fonts
font = pygame.font.SysFont("Inter", 100)

# Set up colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)

# Open json file and take the date
with open("preset.json", "r") as json_file:
    data = json.load(json_file)
    target_month, target_day = data["Month"], data["Day"]

# Take data and create the target date, if it's past the current date sets it to next year
target_date = datetime(datetime.now().year, target_month, target_day, 0, 0, 0)
if target_date < datetime.now():
    target_date = datetime(datetime.now().year + 1, target_month, target_day, 0, 0, 0)
temp_date = target_date
date_change = False

# Firework variables
fireworks = []
explosions = []
boom = False

# Birthday message duration
birthday_duration = timedelta(hours=24)
birthday_start_time = None
birthday_over = False

# Load and play the background music
countdown_music = pygame.mixer.Sound("Sound/countdown.wav")
birthday_music = pygame.mixer.Sound("Sound/song.mp3")
countdown_music.set_volume(0.5)
birthday_music.set_volume(0.4)
countdown_music.play(-1)


def draw_checkmark(surface, position):
    x, y = position
    length = 12
    pygame.draw.line(surface, green, (x, y), (x + length, y + length), 3)
    pygame.draw.line(surface, green, (x + length, y + length), (x + 30, y - 18), 3)


def month_day_menu():
    # Initialize variables
    selected_month = ""
    selected_day = ""
    max_day = 31
    menu_font = pygame.font.SysFont("Inter", 50)
    finalized_month = False
    finalized_day = False
    enter_pressed = False

    lock_month = menu_font.render(f"Month: {selected_month}", True, white)
    lock_month_rect = lock_month.get_rect(center=(window_width // 2, window_height // 2 + 50))

    lock_day = menu_font.render(f"Day: {selected_day}", True, white)
    lock_day_rect = lock_day.get_rect(center=(window_width // 2, window_height // 2 + 250))

    while not enter_pressed:
        # Render explaining
        window.fill(black)
        menu_text = menu_font.render("Enter a new Birthday!", True, white)
        menu_text_rect = menu_text.get_rect(center=(window_width // 2, window_height // 2 - 200))
        window.blit(menu_text, menu_text_rect)

        lock_text = menu_font.render("Press Enter to lock in your month and day:", True, white)
        window.blit(lock_text, lock_text.get_rect(center=(window_width // 2, window_height // 2 - 150)))

        # Render the month input text
        month_text = menu_font.render("Select Month (1-12):", True, white)
        window.blit(month_text, month_text.get_rect(center=(window_width // 2, window_height // 2 - 50)))

        # Render the selected month text
        if 0 < len(selected_month) <= 2:
            lock_month = menu_font.render(f"Month: {selected_month}", True, white)
            lock_month_rect = lock_month.get_rect(center=(window_width // 2, window_height // 2))
            window.blit(lock_month, lock_month_rect)

        # Render the day input text
        day_text = menu_font.render("Select Day (1 up to 31):", True, white)
        window.blit(day_text, day_text.get_rect(center=(window_width // 2, window_height // 2 + 100)))

        # Render the selected day text
        if 0 < len(selected_day) <= 2:
            lock_day = menu_font.render(f"Day: {selected_day}", True, white)
            lock_day_rect = lock_day.get_rect(center=(window_width // 2, window_height // 2 + 150))
            window.blit(lock_day, lock_day_rect)

        # Render checkmark for month or date
        if finalized_month:
            draw_checkmark(window, (lock_month_rect.centerx + 100, lock_month_rect.centery))
        if finalized_day:
            draw_checkmark(window, (lock_day_rect.centerx + 100, lock_day_rect.centery))
        pygame.display.update()

        # Handle events
        for case in pygame.event.get():
            if case.type == pygame.QUIT or (case.type == pygame.KEYDOWN and case.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if case.type == pygame.KEYDOWN:
                if not finalized_month:
                    if pygame.K_0 <= case.key <= pygame.K_9:
                        new_month = selected_month + pygame.key.name(case.key)
                        if 1 <= int(new_month) <= 12:
                            selected_month = new_month
                    elif case.key == pygame.K_BACKSPACE:
                        selected_month = selected_month[:-1]
                    # Press enter to finalize the month selection
                    if case.key == pygame.K_RETURN and len(selected_month) > 0 and 1 <= int(selected_month) <= 12:
                        finalized_month = True
                # day selection
                elif finalized_month and not finalized_day:
                    # Depending on the month limits the day selection
                    if 0 < len(selected_day) <= 2:
                        max_day = 31
                        if int(selected_month) in [4, 6, 9, 11]:
                            max_day = 30
                        elif int(selected_month) == 2:
                            leap_year = ((int(datetime.now().year) % 4 == 0 and int(datetime.now().year) % 100 != 0) or
                                         int(datetime.now().year) % 400 == 0)
                            max_day = 29 if leap_year else 28
                    # Type out the desired day
                    if pygame.K_0 <= case.key <= pygame.K_9:
                        new_day = selected_day + pygame.key.name(case.key)
                        if 1 <= int(new_day) <= max_day:
                            selected_day = new_day
                    elif case.key == pygame.K_BACKSPACE:
                        selected_day = selected_day[:-1]
                    # Press enter to finalize the day selection
                    if case.key == pygame.K_RETURN and len(selected_day) > 0 and 1 <= int(selected_day) <= max_day:
                        finalized_day = True

                # Final enter to check off both
                elif finalized_month and finalized_day:
                    if case.key == pygame.K_RETURN:
                        enter_pressed = True
                # Remove the secured month or day by pressing Backspace
                if event.key == pygame.K_BACKSPACE:
                    if finalized_day:
                        finalized_day = False
                    elif finalized_month:
                        finalized_month = False
                        max_day = 31
    return int(selected_month), int(selected_day)


# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_color = tuple(random.randint(0, 255) for _ in range(3))
        self.color = self.base_color
        self.speed = random.uniform(0.5, 2.0)
        self.angle = random.uniform(0, 2 * math.pi - 0.1)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.lifetime = random.randint(50, 100)
        self.alpha = random.uniform(250.0, 255.0)

    def update(self):
        gravity = 0.1
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self):
        light_factor = 0.3  # Adjust the light intensity as needed
        light_color = tuple(int(c + (255 - c) * light_factor) for c in self.base_color)
        self.color = light_color + (self.alpha,)
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), random.randint(1, 4))


def switch_track(stop_song, start_song):
    stop_song.stop()
    if not pygame.mixer.get_busy():
        start_song.play(-1)


# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                countdown_music.stop()
                birthday_music.stop()
                fireworks = []
                explosions = []
                # Open the menu for updating target date
                target_month, target_day = month_day_menu()
                target_date = datetime(datetime.now().year, target_month, target_day, 0, 0, 0)
                # If the date already passed makes it set to next year
                if target_date < datetime.now():
                    target_date = datetime(datetime.now().year + 1, target_month, target_day, 0, 0, 0)
                # Saves the selected month and date
                with open('preset.json', 'r+') as json_file:
                    data = json.load(json_file)
                    data["Month"] = target_month
                    data["Day"] = target_day
                    json_file.seek(0)
                    json_file.truncate()
                    json.dump(data, json_file)

                if not pygame.mixer.get_busy():
                    countdown_music.play(-1)
            # Debug
            elif event.key == pygame.K_EQUALS:
                if date_change:
                    temp_date = target_date
                    target_date = datetime.now()
                    date_change = False
                    switch_track(countdown_music, birthday_music)
                else:
                    target_date = temp_date
                    date_change = True
                    switch_track(birthday_music, countdown_music)
                    fireworks = []
                    explosions = []
                    birthday_start_time = None
    # Calculate the remaining time for countdown
    current_time = datetime.now()
    if current_time > target_date and birthday_over:
        target_date = datetime(target_date.year + 1, target_month, target_day, 0, 0, 0)
    remaining_time = target_date - current_time

    days = remaining_time.days
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    window.fill(black)

    # Update and draw fireworks
    for firework in fireworks:
        pygame.draw.circle(window, tuple(random.randint(0, 255) for _ in range(3)), firework[:2], firework[2])
        firework[1] -= 6  # Move fireworks

        if firework[1] <= 100 and random.randint(1, 20) == 1:
            boom = True
        # Check if firework explodes
        if firework[1] + firework[2] <= 0 or boom:
            # Create explosion particles
            for i in range(random.randint(60, 80)):
                particle = Particle(firework[0], firework[1])
                explosions.append(particle)
            fireworks.remove(firework)
            boom = False

    # Update and draw explosion particles
    for particle in explosions:
        particle.update()
        particle.draw()
        # Remove particles that have expired
        if particle.lifetime <= 0:
            explosions.remove(particle)

    # if countdown is at 0
    if remaining_time.total_seconds() <= 0:
        # Stop the countdown music and start the birthday music
        switch_track(countdown_music, birthday_music)
        birthday_over = False

        # Render the birthday message
        text = font.render("Happy Birthday!", True, white)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)

        # Create fireworks
        if len(fireworks) < 200 and pygame.time.get_ticks() % 20 == 0:
            fireworks.append([random.randint(0, window_width), window_height, random.randint(1, 4)])

        # Start the birthday message duration
        if birthday_start_time is None:
            birthday_start_time = datetime.now()

        # Restart timer for the next year
        if datetime.now() - birthday_start_time >= birthday_duration:
            # Stop birthday music and start countdown
            switch_track(birthday_music, countdown_music)
            birthday_over = True
            # Reset the fireworks and explosion particles
            fireworks = []
            explosions = []
            birthday_start_time = None
            # Check if it's past midnight to update the target date for the next year
            if datetime.now().date() >= target_date.date():
                target_date = datetime(target_date.year + 1, 7, 6, 0, 0, 0)
    else:
        # Render the remaining time on the window
        text = font.render(f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}", True, white)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)

    pygame.display.update()
    pygame.time.Clock().tick(60)
