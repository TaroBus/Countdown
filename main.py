import pygame
import sys
import random
from datetime import datetime

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Happy Birthday")

# Set up fonts
font = pygame.font.Font(None, 100)

# Set up colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
firework_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]

# Set up the target date and time
target_date = datetime(2023, 7, 17, 0, 0, 0)

# Firework variables
fireworks = []
firework_speed = 5
firework_interval = 15
explosions = []

# Particle variables
particle_speed = 2
particle_gravity = 0.1
num_particles = 100
particle_lifetime = 120


# Particle class
class Particle:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.color = c
        self.vx = random.uniform(-particle_speed, particle_speed)
        self.vy = random.uniform(-particle_speed, particle_speed)
        self.lifetime = particle_lifetime

    def update(self):
        self.vy += particle_gravity
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), 2)


# Load and play the background music
countdown_music = pygame.mixer.Sound("countdown.wav")
birthday_music = pygame.mixer.Sound("song.mp3")
countdown_music.play(-1)

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calculate the remaining time
    current_time = datetime.now()
    remaining_time = target_date - current_time
    days = remaining_time.days
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Clear the window
    window.fill(black)

    # Update and draw fireworks
    for firework in fireworks:
        color = random.choice(firework_colors)  # Randomly select a color from the list
        pygame.draw.circle(window, color, firework[:2], firework[2])
        # Move fireworks
        firework[1] -= firework_speed

        # Check if firework explodes
        if firework[1] + firework[2] <= 0:
            # Create explosion particles
            for i in range(num_particles):
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

    if remaining_time.total_seconds() <= 0:
        # Stop the countdown music
        countdown_music.stop()

        if not pygame.mixer.get_busy():
            birthday_music.play(-1)

        # Render the "Happy Birthday" message on the window
        text = font.render("Happy Birthday!", True, white)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)

        # Create fireworks periodically
        if len(fireworks) < 200 and pygame.time.get_ticks() % firework_interval == 0:
            fireworks.append([random.randint(0, window_width), window_height, random.randint(2, 8)])

    else:
        # Render the remaining time on the window
        text = font.render(f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}", True, white)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    pygame.time.Clock().tick(60)
