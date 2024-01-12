import glfw
from OpenGL.GL import *
import time
import random

# Initialize player position
px, py = 400, 30

# Initialize bullet properties
bullet_x, bullet_y = None, None
bullet_speed = 5

# Initialize enemy properties
enemy_x, enemy_y = random.randint(50, 750), 500
enemy_speed = 2

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_player():
    glColor3f(0, 1, 0)  # Green color
    draw_rect(px, py, 40, 10)

def draw_enemy():
    glColor3f(1, 0, 0)  # Red color
    draw_rect(enemy_x, enemy_y, 20, 20)

def draw_bullet():
    if bullet_y is not None:
        glColor3f(1, 1, 1)  # White color
        draw_rect(bullet_x, bullet_y, 3, 10)

def collision(obj1, obj2):
    return (
        obj1[0] < obj2[0] + 20 and
        obj1[0] + 40 > obj2[0] and
        obj1[1] < obj2[1] + 20 and
        obj1[1] + 10 > obj2[1]
    )

def key_callback(window, key, scancode, action, mods):
    global px, py
    if action == glfw.PRESS:
        if key == glfw.KEY_A and px > 0:
            px -= 5
        elif key == glfw.KEY_D and px < 760:
            px += 5

def game_loop():
    global bullet_x, bullet_y, enemy_x, enemy_y

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_player()
        draw_enemy()
        draw_bullet()

        # Update bullet position
        if bullet_y is not None:
            bullet_y -= bullet_speed
            if bullet_y < 0:
                bullet_y = None

        # Update enemy position
        enemy_y -= enemy_speed
        if enemy_y < 0:
            enemy_x, enemy_y = random.randint(50, 750), 500

        # Check for collisions
        if collision([px, py], [enemy_x, enemy_y]) or \
                (bullet_y is not None and collision([bullet_x, bullet_y], [enemy_x, enemy_y])):
            print("Game Over!")
            glfw.set_window_should_close(window, True)

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.02)

# Initialize GLFW
if not glfw.init():
    print("Failed to initialize GLFW")
    glfw.terminate()
    exit()

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "Space Invaders", None, None)
if not window:
    print("Failed to create GLFW window")
    glfw.terminate()
    exit()

# Make the window's context current
glfw.make_context_current(window)

# Set the clear color
glClearColor(0.0, 0.0, 0.0, 0.0)

# Set the orthographic projection matrix
glOrtho(0, 800, 600, 0, -1, 1)

# Set the keyboard callback function
glfw.set_key_callback(window, key_callback)

# Run the game loop
game_loop()

# Terminate GLFW
glfw.terminate()
