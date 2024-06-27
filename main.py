import pygame
import math
import os
import random

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

pygame.init()
cls()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
vers = 1.2
pygame.display.set_caption(f"Falling balls simulation v{vers}")
try:
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
except:
    print("Missing window icon!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0), 
    (0, 255, 0),  
    (0, 0, 255),    
    (255, 255, 0),  
    (255, 0, 255),  
    (0, 255, 255),  
    (255, 165, 0),  
    (128, 0, 128),  
    (0, 128, 128), 
    (128, 128, 0)   
]

circle_center = (WIDTH // 2, HEIGHT // 2)
circle_radius = 250

ball_radius = 10
gravity = 0.1 

def create_ball():
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(1, 3)
    color = random.choice(COLORS)
    return {
        'pos': [circle_center[0], circle_center[1] - circle_radius + ball_radius],
        'vel': [speed * math.cos(angle), speed * math.sin(angle)],
        'color': color,
        'trail': []
    }

def reset_balls(balls):
    for ball in balls:
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        ball['pos'] = [circle_center[0], circle_center[1] - circle_radius + ball_radius]
        ball['vel'] = [speed * math.cos(angle), speed * math.sin(angle)]
        ball['trail'] = []

balls = [create_ball() for _ in range(1)]

button_font = pygame.font.Font(None, 36)
plus_button_rect = pygame.Rect(WIDTH - 210, 10, 30, 30)
minus_button_rect = pygame.Rect(WIDTH - 175, 10, 30, 30)
pause_button_rect = pygame.Rect(WIDTH - 140, 10, 30, 30)
reset_button_rect = pygame.Rect(WIDTH - 105, 10, 30, 30)
speed_up_button_rect = pygame.Rect(WIDTH - 70, 10, 30, 30)
slow_down_button_rect = pygame.Rect(WIDTH - 35, 10, 30, 30)

clock = pygame.time.Clock()
paused = False
simulation_speed = 1

speed_up_pressed = False
slow_down_pressed = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if plus_button_rect.collidepoint(event.pos):
                balls.append(create_ball())
            elif minus_button_rect.collidepoint(event.pos):
                if balls:
                    balls.pop()
            elif pause_button_rect.collidepoint(event.pos):
                paused = not paused
            elif reset_button_rect.collidepoint(event.pos):
                reset_balls(balls)


    if not paused:
        for ball in balls:
            ball['vel'][1] += gravity
            ball['pos'][0] += ball['vel'][0]
            ball['pos'][1] += ball['vel'][1]

            dist_to_center = math.sqrt((ball['pos'][0] - circle_center[0]) ** 2 + (ball['pos'][1] - circle_center[1]) ** 2)
            if dist_to_center >= circle_radius - ball_radius:
                normal = [(ball['pos'][0] - circle_center[0]) / dist_to_center, (ball['pos'][1] - circle_center[1]) / dist_to_center]
                dot_product = ball['vel'][0] * normal[0] + ball['vel'][1] * normal[1]
                ball['vel'][0] -= 2 * dot_product * normal[0]
                ball['vel'][1] -= 2 * dot_product * normal[1]

                overlap = (circle_radius - ball_radius) - dist_to_center
                ball['pos'][0] += normal[0] * overlap
                ball['pos'][1] += normal[1] * overlap

            ball['trail'].append((int(ball['pos'][0]), int(ball['pos'][1])))
            if len(ball['trail']) > 50:
                ball['trail'].pop(0)

    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, circle_center, circle_radius, 1)

    for ball in balls:
        if len(ball['trail']) > 1:
            pygame.draw.lines(screen, ball['color'], False, ball['trail'], 2)
        pygame.draw.circle(screen, ball['color'], [int(ball['pos'][0]), int(ball['pos'][1])], ball_radius)

    pygame.draw.rect(screen, WHITE, plus_button_rect)
    pygame.draw.rect(screen, WHITE, minus_button_rect)
    pygame.draw.rect(screen, WHITE, pause_button_rect)
    pygame.draw.rect(screen, WHITE, reset_button_rect)

    plus_text = button_font.render("+", True, BLACK)
    minus_text = button_font.render("-", True, BLACK)
    pause_text = button_font.render("||" if not paused else ">", True, BLACK)
    reset_text = button_font.render("R", True, BLACK)

    screen.blit(plus_text, (plus_button_rect.x + 5, plus_button_rect.y))
    screen.blit(minus_text, (minus_button_rect.x + 5, minus_button_rect.y))
    screen.blit(pause_text, (pause_button_rect.x + 5, pause_button_rect.y))
    screen.blit(reset_text, (reset_button_rect.x + 5, reset_button_rect.y))

    counter_text = button_font.render(f"Balls: {len(balls)}", True, WHITE)
    screen.blit(counter_text, (10, 10))

    fps_text = button_font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (10, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(75)
pygame.quit()
