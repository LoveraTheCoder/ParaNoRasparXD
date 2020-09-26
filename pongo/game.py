#Pong creado por John Lovera Schultz y Ángela Mendez Alvarado
import sys
import pygame
import random

if not pygame.font:
    print('Warning! PyGame fonts disabled!')
else:
    pygame.font.init()

# constantes
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 10
PAD_HEIGHT = 80
PAD_VELOCITY = 3.5
GAME_TITLE = "Pong"
WHITE_COLOR = (255, 255, 255)
DIR_RIGHT = True
DIR_LEFT = False
PLAYER_LEFT = 0
PLAYER_RIGHT = 1


def spawn_ball(direction):
    #spawnea la pelota
    global ball_pos, ball_vel

    ball_pos = [FRAME_WIDTH // 2, FRAME_HEIGHT // 2]

    x_vel = random.randrange(120, 240) / 60
    y_vel = random.randrange(60, 180) / 60

    if direction == DIR_RIGHT:
        x_vel *= -1

    ball_vel = [x_vel, -y_vel]


def new_game():
    #crea un nuevo juego
    global paddle_left_pos, paddle_right_pos, paddle_left_vel, paddle_right_vel
    global score_left, score_right

    # pone puntos
    score_left = 0
    score_right = 0

    # posicion de las paletas
    paddle_left_pos = (FRAME_HEIGHT / 2) - (PAD_HEIGHT / 2)
    paddle_right_pos = (FRAME_HEIGHT / 2) - (PAD_HEIGHT / 2)

    # velocidad de las paletas
    paddle_left_vel = 0
    paddle_right_vel = 0

    # crea la posición random que la pelota viajara
    if random.randrange(0, 2) == 1:
        _direction = DIR_RIGHT
    else:
        _direction = DIR_LEFT

    
    spawn_ball(_direction)


def draw_handler(surface):
    """Draws to the surface every iteration"""
    # Clear surface
    surface.fill((0, 0, 0))

    # Draw midline and gutters
    pygame.draw.line(surface, WHITE_COLOR, (FRAME_WIDTH / 2, 0), (FRAME_WIDTH / 2, FRAME_HEIGHT), 1)
    pygame.draw.line(surface, WHITE_COLOR, (PAD_WIDTH, 0), (PAD_WIDTH, FRAME_HEIGHT), 1)
    pygame.draw.line(surface, WHITE_COLOR, (FRAME_WIDTH - PAD_WIDTH, 0),
                     (FRAME_WIDTH - PAD_WIDTH, FRAME_HEIGHT), 1)

    # Dibuja pelota
    render_ball(surface)

    # Dibuja paletas
    render_paddles(surface)

    # Dibuja los puntos del jugador
    draw_text_helper(surface, score_left, (125, 50), 72, WHITE_COLOR)
    draw_text_helper(surface, score_right, (425, 50), 72, WHITE_COLOR)

    pygame.display.update()


def keydown_handler(event_key):
    
    global paddle_left_vel, paddle_right_vel

    #Paleta del jugador de la izquierda
    if event_key == 115:
        paddle_left_vel = PAD_VELOCITY
    elif event_key == 119:
        paddle_left_vel = -PAD_VELOCITY

    # Paleta del jugador de la derecha
    if event_key == 274:
        paddle_right_vel = PAD_VELOCITY
    elif event_key == 273:
        paddle_right_vel = -PAD_VELOCITY


def keyup_handler(event_key):
    
    global paddle_left_vel, paddle_right_vel

    # Paleta del jugador de la izquierda
    if event_key == 119 or event_key == 115:
        paddle_left_vel = 0

    # Paleta del jugador de la derecha
    if event_key == 273 or event_key == 274:
        paddle_right_vel = 0


def frame():
    
    new_game()

    # crea superficie
    _game_surface = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))

    # pone el titulo
    pygame.display.set_caption(GAME_TITLE)

    # establece el clock para los fps
    _fps_clock = pygame.time.Clock()

    # bucle del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keydown_handler(event.key)
            elif event.type == pygame.KEYUP:
                keyup_handler(event.key)

        draw_handler(_game_surface)

        #fps limitados a 60
        _fps_clock.tick(60)

# Helpers
def render_ball(surface):
    #dibuja la pelota en la superficie
    global ball_pos, ball_vel

    ball_pos[0] = int(ball_pos[0])
    ball_pos[1] = int(ball_pos[1])

    # crea pelota
    if ball_pos[0] + (BALL_RADIUS + PAD_WIDTH) >= FRAME_WIDTH:
        # esto tambien revisa si la pelota es oglpeada por paeltas
        if paddle_right_pos < ball_pos[1] < paddle_right_pos + PAD_HEIGHT:
            ball_vel[0] = (ball_vel[0] + 0.1) * -1
        else:
            player_score(PLAYER_LEFT)
            spawn_ball(DIR_RIGHT)

    if ball_pos[0] - (BALL_RADIUS + PAD_WIDTH) <= 0:
        # revisa si la pelota es golpeada por las paletas
        if paddle_left_pos < ball_pos[1] < paddle_left_pos + PAD_HEIGHT:
            ball_vel[0] = (ball_vel[0] - 0.1) * -1
        else:
            player_score(PLAYER_RIGHT)
            spawn_ball(DIR_LEFT)

    # si la pelota golpea 
    if ball_pos[1] - BALL_RADIUS == 0:
        ball_vel[1] *= -1

    if ball_pos[1] + BALL_RADIUS == FRAME_HEIGHT:
        ball_vel[1] *= -1

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    pygame.draw.circle(surface, WHITE_COLOR, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS, 0)


def render_paddles(surface):
   #dibuja las paletas y se asegura de que detecte cuando golpeen la pelota
    global paddle_left_vel, paddle_right_vel, paddle_left_pos, paddle_right_pos

    # velocidad
    if 0 <= paddle_left_vel + paddle_left_pos + paddle_left_vel <= FRAME_HEIGHT - PAD_HEIGHT:
        paddle_left_pos += paddle_left_vel

    if 0 <= paddle_right_vel + paddle_right_pos + paddle_right_vel <= FRAME_HEIGHT - PAD_HEIGHT:
        paddle_right_pos += paddle_right_vel

    # Dibujar las paletas
    pygame.draw.line(surface, WHITE_COLOR, (PAD_WIDTH / 2, paddle_left_pos),
                     (PAD_WIDTH / 2, paddle_left_pos + PAD_HEIGHT), PAD_WIDTH)
    pygame.draw.line(surface, WHITE_COLOR, (FRAME_WIDTH - PAD_WIDTH / 2, paddle_right_pos),
                     (FRAME_WIDTH - PAD_WIDTH / 2, paddle_right_pos + PAD_HEIGHT), PAD_WIDTH)


def draw_text_helper(surface, value, pos, size, color, font="sans-serif"):
    #Función para definir y renderizar el espacio y la fuente
    _font_object = pygame.font.Font(pygame.font.match_font(font), size)
    _font_draw = _font_object.render(str(value), True, color)
    surface.blit(_font_draw, pos)


def player_score(player):
    #Función que anota puntos
    global score_left, score_right

    if player == PLAYER_LEFT:
        score_left += 1
    elif player == PLAYER_RIGHT:
        score_right += 1


def main():
    frame()


if __name__ == '__main__':
    main()
