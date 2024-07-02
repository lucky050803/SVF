import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
PACMAN_SPEED = 20
GHOST_SPEED = 20
FPS = 10
NEW_GHOST_INTERVAL = 5000  # Intervalle de temps pour créer un nouveau fantôme en millisecondes
NEW_OBJECT_INTERVAL = 3000  # Intervalle de temps pour créer un nouvel objet en millisecondes
NEW_MULT_INTERVAL = 5000  # Intervalle de temps pour créer un multiplicateur en millisecondes
NEW_BOMB_INTERVAL = 15000  # Intervalle de temps pour créer une bombe en millisecondes

# Couleurs
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

POL = "arial"
IMG = "mageB.png"
txt_pth = "score.txt"
# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BRIQUE')

# Classes
pacman_image = pygame.image.load('mage.png')
pacman_image = pygame.transform.scale(pacman_image, (CELL_SIZE, CELL_SIZE))

# Classes
class PacMan:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = 0
        self.dy = 0
        self.image = pacman_image
        self.angle = 0

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bordures
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - CELL_SIZE:
            self.x = SCREEN_WIDTH - CELL_SIZE
        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_HEIGHT - CELL_SIZE:
            self.y = SCREEN_HEIGHT - CELL_SIZE

        # Rotation de l'image en fonction de la direction
        if self.dx > 0:  # Vers la droite
            self.angle = 270
        elif self.dx < 0:  # Vers la gauche
            self.angle = 90
        elif self.dy > 0:  # Vers le bas
            self.angle = 180
        elif self.dy < 0:  # Vers le haut
            self.angle = 0

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        screen.blit(rotated_image, (self.x, self.y))
    

class Ghost:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        self.dx = GHOST_SPEED * random.choice([-1, 1])
        self.dy = GHOST_SPEED * random.choice([-1, 1])

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bordures
        if self.x < 0 or self.x > SCREEN_WIDTH - CELL_SIZE:
            self.dx = -self.dx
        if self.y < 0 or self.y > SCREEN_HEIGHT - CELL_SIZE:
            self.dy = -self.dy

    def draw(self):
        # Points du triangle
        points = [(self.x + CELL_SIZE // 2, self.y), 
                  (self.x, self.y + CELL_SIZE), 
                  (self.x + CELL_SIZE, self.y + CELL_SIZE)]
        pygame.draw.polygon(screen, RED, points)

class Object:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        self.creation_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, GREEN, pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))

class Multipl:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        self.creation_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, BLUE, pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))

class BOMB:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        self.creation_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))
        
# Fonctions
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def menu():
    menu_running = True
    while menu_running:
        bg = pygame.image.load(IMG)
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bg, (0, 0))
        font = pygame.font.SysFont(POL, 55)
        fontT = pygame.font.SysFont(POL, 74)
        
        Title_text = font.render('Sorcier vs Fantomes', True, WHITE)
        play_text = font.render('Jouer', True, WHITE)
        quit_text = fontT.render('Quitter', True, WHITE)

        Title_rect = Title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)
        screen.blit(Title_text, Title_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    menu_running = False
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def check_collision(pacman, ghosts):
    pacman_rect = pygame.Rect(pacman.x, pacman.y, CELL_SIZE, CELL_SIZE)
    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost.x, ghost.y, CELL_SIZE, CELL_SIZE)
        if pacman_rect.colliderect(ghost_rect):
            return True
    return False

def check_object_collision(pacman, objects):
    pacman_rect = pygame.Rect(pacman.x, pacman.y, CELL_SIZE, CELL_SIZE)
    for obj in objects:
        obj_rect = pygame.Rect(obj.x, obj.y, CELL_SIZE, CELL_SIZE)
        if pacman_rect.colliderect(obj_rect):
            objects.remove(obj)
            return True
    return False

def check_multipl_collision(pacman, multipl):
    pacman_rect = pygame.Rect(pacman.x, pacman.y, CELL_SIZE, CELL_SIZE)
    for mult in multipl:
        obj_rect = pygame.Rect(mult.x, mult.y, CELL_SIZE, CELL_SIZE)
        if pacman_rect.colliderect(obj_rect):
            multipl.remove(mult)
            return True
    return False

def save_score(score):
    with open(txt_pth, 'r') as f:
        number = int(f.readline().strip())
    if number < score:
        with open('score.txt', 'w') as f:
            f.write(str(score))
            
def game_over_animation():
    
    alpha = 0
    with open(txt_pth, 'r') as f:
        number = int(f.readline().strip())
        
    font = pygame.font.SysFont(POL, 74)
    game_over_text = font.render('DEAD', True, WHITE)
    game_over_text.set_alpha(alpha)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    fontB = pygame.font.SysFont(POL, 50)
    game_over_score = fontB.render("HIGH SCORE : " + str(number), True, WHITE)
    game_over_score.set_alpha(alpha)
    game_over_score_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 100))
    
    retry_txt = fontB.render("RETRY ?", True, WHITE)
    retry_txt.set_alpha(alpha)
    retry_rect = retry_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    
    while alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(BLACK)
        draw_grid()

        alpha += 5  # Increment transparency
        game_over_text.set_alpha(alpha)
        game_over_score.set_alpha(alpha)
        retry_txt.set_alpha(alpha)
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(game_over_score, game_over_score_rect)
        screen.blit(retry_txt, retry_rect)
        
        pygame.display.flip()
        pygame.time.delay(20)

    # Wait for user input
    game_over_running = True
    while game_over_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over_running = False
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    game_over_running = False
                    return True
    return False

# Initialisation
pacman = PacMan()
ghosts = [Ghost() for _ in range(4)]
objects = []
multipls = []
bombs = []
score = 0
last_ghost_time = pygame.time.get_ticks()  # Initialisation du temps pour créer des fantômes
last_object_time = pygame.time.get_ticks()  # Initialisation du temps pour créer des objets
start_time = pygame.time.get_ticks()  # Temps de début du jeu
last_multipl_time = pygame.time.get_ticks()
last_bomb_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
running = True
multiplicateur = 1

# Boucle principale
menu()
while running:
    
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000  # Temps écoulé en secondes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.dx = -PACMAN_SPEED
                pacman.dy = 0
            elif event.key == pygame.K_RIGHT:
                pacman.dx = PACMAN_SPEED
                pacman.dy = 0
            elif event.key == pygame.K_UP:
                pacman.dx = 0
                pacman.dy = -PACMAN_SPEED
            elif event.key == pygame.K_DOWN:
                pacman.dx = 0
                pacman.dy = PACMAN_SPEED

    pacman.move()
    for ghost in ghosts:
        ghost.move()

    # Vérification des collisions avec les fantômes
    if check_collision(pacman, ghosts):
        pygame.time.delay(20)
        last_score = score
        save_score(last_score)
        if game_over_animation():
            pacman = PacMan()
            ghosts = [Ghost() for _ in range(4)]
            objects = []
            multipls = []
            bombs = []
            multiplicateur = 1
            score = 0
            last_ghost_time = pygame.time.get_ticks()
            last_object_time = pygame.time.get_ticks()
            last_multipl_time = pygame.time.get_ticks()
            start_time = pygame.time.get_ticks()
        else:
            running = False

    # Vérification des collisions avec les objets
    if check_object_collision(pacman, objects):
        score = score + 15 * multiplicateur

    if check_multipl_collision(pacman, multipls):
        multiplicateur += 1
        
    if check_multipl_collision(pacman, bombs):
        i = 0
        while i < 2:
            ghosts.pop(len(ghosts) - 1)
            i += 1
            
    # Création d'un nouveau fantôme toutes les 5 secondes
    if current_time - last_ghost_time > NEW_GHOST_INTERVAL:
        ghosts.append(Ghost())
        last_ghost_time = current_time

    if current_time - last_object_time > NEW_OBJECT_INTERVAL:
        objects.append(Object())
        last_object_time = current_time
    
    if current_time - last_multipl_time > NEW_MULT_INTERVAL:
        multipls.append(Multipl())
        last_multipl_time = current_time
        
    if current_time - last_bomb_time > NEW_BOMB_INTERVAL:
        bombs.append(BOMB())
        last_bomb_time = current_time

    screen.fill(BLACK)
    draw_grid()
    pacman.draw()
    
    for ghost in ghosts:
        ghost.draw()
        
    for object in objects:
        object.draw()
        
    for multiplic in multipls:
        multiplic.draw()
    
    for bombi in bombs:
        bombi.draw()
        
    font = pygame.font.SysFont(POL, 30)
    score_text = font.render("SCORE : " + str(score), True, WHITE)
    multi_txt = font.render('X' + str(multiplicateur), True, WHITE)
    score_rect = score_text.get_rect(center=(530, 450))
    multi_rect = multi_txt.get_rect(center=(610, 430))
    screen.blit(score_text, score_rect)
    screen.blit(multi_txt, multi_rect)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
