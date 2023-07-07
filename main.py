import pygame
import sys
import random
import math
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
firework_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]

# Set up the target date and time
target_month = 7
target_day = 17
target_date = datetime(datetime.now().year, target_month, target_day, 0, 0, 0)

# Firework variables
fireworks = []
explosions = []

# Birthday message duration
birthday_duration = timedelta(hours=24)
birthday_start_time = None
birthday_over = False


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
                    if 0 < len(selected_day) <= 2:
                        max_day = 31
                        if int(selected_month) in [4, 6, 9, 11]:
                            max_day = 30
                        elif int(selected_month) == 2:
                            leap_year = ((int(datetime.now().year) % 4 == 0 and int(datetime.now().year) % 100 != 0) or
                                         int(datetime.now().year) % 400 == 0)
                            max_day = 29 if leap_year else 28

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

                # Remove the month or day by pressing Backspace
                if event.key == pygame.K_BACKSPACE:
                    if finalized_day:
                        finalized_day = False
                    elif finalized_month:
                        finalized_month = False
                        max_day = 31
    return int(selected_month), int(selected_day)


# Particle class
class Particle:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.color = c
        self.speed = random.uniform(0.5, 2.0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.lifetime = random.randint(80, 120)
        self.alpha = random.uniform(250.0, 255.0)
        self.color_with_alpha = self.color + (self.alpha,)

    def update(self):
        self.vy += 0.1
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.alpha = int((self.lifetime / 120) * 255)

    def draw(self):
        self.color_with_alpha = self.color + (self.alpha,)
        pygame.draw.circle(window, self.color_with_alpha, (int(self.x), int(self.y)), 2)


def switch_track(stop_song, start_song):
    stop_song.stop()
    if not pygame.mixer.get_busy():
        start_song.play(-1)


# Load and play the background music
countdown_music = pygame.mixer.Sound("Sound/countdown.wav")
birthday_music = pygame.mixer.Sound("Sound/song.mp3")
countdown_music.set_volume(0.5)
birthday_music.set_volume(0.4)
countdown_music.play(-1)

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_TAB:
                countdown_music.stop()
                birthday_music.stop()
                # Open the menu for updating target date
                target_month, target_day = month_day_menu()
                target_date = datetime(datetime.now().year, target_month, target_day, 0, 0, 0)
                if not pygame.mixer.get_busy():
                    countdown_music.play(-1)

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
        color = random.choice(firework_colors)  # Randomly select a color from the list
        pygame.draw.circle(window, color, firework[:2], firework[2])
        firework[1] -= 6  # Move fireworks

        # Check if firework explodes
        if firework[1] + firework[2] <= 0:
            # Create explosion particles
            for i in range(100):
                particle = Particle(firework[0], firework[1], random.choice(firework_colors))
                explosions.append(particle)
            fireworks.remove(firework)

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

        # Render the "Happy Birthday" message on the window
        text = font.render("Happy Birthday!", True, white)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)
        # Create fireworks periodically
        if len(fireworks) < 200 and pygame.time.get_ticks() % 15 == 0:
            fireworks.append([random.randint(0, window_width), window_height, random.randint(2, 8)])

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
