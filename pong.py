import pygame
import random
import cv2
import mediapipe as mp
import time

# Set up webcam capture
global cap
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("SRI Pong")

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game variables
ball_x = width / 2
ball_y = height / 2
ball_radius = 12
ball_speed_x = 12 * random.choice([-1, 1])
ball_speed_y = 12 * random.choice([-1, 1])
# hit_counter = 0

paddle_width = 10
paddle_height = 100
paddle_speed = 10

player_x = 25
player_y = (height - paddle_height) / 2
computer_x = width - paddle_width - 25
computer_y = (height - paddle_height) / 2

player_score = 0
computer_score = 0
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 100)
font3 = pygame.font.Font(None, 180)


# ============================= Define the game functions =============================
def get_players_y():
    global cap

    # Read frames from webcam
    success, image = cap.read()
    if not success:
        return -1, -1

    # Convert image to RGB format for Mediapipe
    image = cv2.flip(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), 1)

    # Use Mediapipe Hand Tracker to find hand landmarks
    with mp_hands.Hands(max_num_hands=2) as hands:
        HandResults = hands.process(image)

    if HandResults.multi_hand_landmarks:

        if len(HandResults.multi_hand_landmarks) == 1:
            middle_tip_x = HandResults.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
            middle_tip_y = HandResults.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            # print("Uma mão")
            if middle_tip_x < 0.5:
                return middle_tip_y, -1
            else:
                return -1, middle_tip_y

        elif len(HandResults.multi_hand_landmarks) == 2:
            middle_tip_x = HandResults.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
            middle_tip_y = HandResults.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            middle_tip2_y = HandResults.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            # print(middle_tip[1])
            # print("Duas mãos")
            if middle_tip_x < 0.5:
                return middle_tip_y, middle_tip2_y
            else:
                return middle_tip2_y, middle_tip_y

        else:
            return -1, -1

    else:
        return -1, -1

# Update ball
def update_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, player_score, computer_score, ball_radius
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    if ball_y < 0 or ball_y > height:
        ball_speed_y *= -1
    if ball_x <= 0:
        computer_score += 1
        ball_radius -= 1
        # hit_counter = 0
        reset_ball()
    if ball_x >= width:
        player_score += 1
        ball_radius -= 1
        # hit_counter = 0
        reset_ball()
    if computer_score + player_score == 7:
        return False
    if (
        ball_x - ball_radius <= player_x + paddle_width and ball_x - ball_radius > player_x
        and ball_y + ball_radius > player_y and ball_y - ball_radius < player_y + paddle_height
    ):
        # hit_counter = hit_counter + 1
        # ball_speed_x = ball_speed_x + hit_counter * ball_speed_x / abs(ball_speed_x)
        ball_speed_x *= -1
    if (
        ball_x + ball_radius >= computer_x and ball_x + ball_radius< computer_x + paddle_width
        and ball_y + ball_radius > computer_y and ball_y - ball_radius < computer_y + paddle_height
    ):
        # hit_counter = hit_counter + 1
        # ball_speed_x = ball_speed_x + hit_counter * ball_speed_x / abs(ball_speed_x)
        ball_speed_x *= -1
    return True


# Reset Ball
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = width / 2
    ball_y = height / 2
    ball_speed_x = 12 * random.choice([-1, 1])
    ball_speed_y = 12 * random.choice([-1, 1])


# Update Player
def update_players():
    global player_y, computer_y
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_UP] and player_y > 0:
    #     player_y -= paddle_speed
    # if keys[pygame.K_DOWN] and player_y < height - paddle_height:
    #     player_y += paddle_speed

    y, y2 = get_players_y()
    # if 0 < y < 0.4 and player_y > 0:
    #     player_y -= paddle_speed
    # elif y > 0.6 and player_y < height - paddle_height:
    #     player_y += paddle_speed
    # else:
    #     player_y = player_y

    if y != -1:
        player_y = y*height
    else:
        player_y = player_y

    # if 0 < y2 < 0.4 and computer_y > 0:
    #     computer_y -= paddle_speed
    # elif y2 > 0.6 and computer_y < height - paddle_height:
    #     computer_y += paddle_speed
    # else:
    #     computer_y = computer_y

    if y2 != -1:
        computer_y = y2*height
    else:
        computer_y = computer_y


# Update Computer
def update_computer(): # Not in use
    global computer_y
    if computer_y + paddle_height / 2 < ball_y:
        computer_y += paddle_speed
    if computer_y + paddle_height / 2 > ball_y:
        computer_y -= paddle_speed

global ball_red, ball_green, ball_blue
# Draw the game
def draw_game():
    # Clear the screen
    window.fill((0, 0, 0))
    # Draw the ball
    # ball_red = random.randint(0, 255)
    # ball_green = random.randint(0, 255)
    # ball_blue = random.randint(0, 255)
    ball_red = 119
    ball_green = 0
    ball_blue = 200
    pygame.draw.circle(window, (ball_red, ball_green, ball_blue), (int(ball_x), int(ball_y)), ball_radius)
    # Draw the paddles
    pygame.draw.rect(
        window, (16, 16, 255), (player_x, player_y, paddle_width, paddle_height)
    )
    pygame.draw.rect(
        window, (255, 16, 16), (computer_x, computer_y, paddle_width, paddle_height)
    )

    # Draw the scores
    player_score_text = font.render(
        "Player 1: " + str(player_score), True, (16, 16, 255)
    )
    computer_score_text = font.render(
        "Player 2: " + str(computer_score), True, (255, 16, 16)
    )
    window.blit(player_score_text, (50, 50))
    window.blit(computer_score_text, (width - computer_score_text.get_width() - 50, 50))

# ============================= Main =============================
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    # Update the screen
    pygame.display.update()
    # Update the game
    running = update_ball()

    update_players()
    # update_computer()
    # Draw the game
    draw_game()

    # Set the game clock
    clock.tick(60)

    if not running:
        winner = font2.render(
            "WINNER", True, (255, 255, 255)
        )
        if player_score > computer_score:
            winner_name = font3.render(
                "Player 1", True, (16, 16, 255)
            )
        else:
            winner_name = font3.render(
                "Player 2", True, (255, 16, 16)
            )
        window.blit(winner, (width / 2 - winner.get_width() / 2, 200))
        window.blit(winner_name, (width / 2 - winner_name.get_width() / 2, 300))
        pygame.display.update()
        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    flag = False

pygame.quit()
