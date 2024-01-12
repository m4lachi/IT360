import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

circle1Center = (-1.0, 0.0)
circle2Center = (1.0, 0.0)

draggingCircle1 = False
draggingCircle2 = False
last_mouse_x, last_mouse_y = 0, 0

def drawCircle(center, radius, color):
    num_segments = 100  

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*color)
    
    glVertex2f(center[0], center[1])

    for i in range(num_segments + 1):
        theta = 2.0 * pi * i / num_segments
        x = radius * cos(theta) + center[0]
        y = radius * sin(theta) + center[1]
        glVertex2f(x, y)

    glEnd()

def mouse_button_callback(window, button, action, mods):
    global draggingCircle1, draggingCircle2, last_mouse_x, last_mouse_y
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            if distance(x, y, circle1Center) < 1.0:
                draggingCircle1 = True
            elif distance(x, y, circle2Center) < 1.0:
                draggingCircle2 = True
            last_mouse_x, last_mouse_y = x, y
        elif action == glfw.RELEASE:
            draggingCircle1 = False
            draggingCircle2 = False

def cursor_pos_callback(window, x, y):
    global draggingCircle1, draggingCircle2, last_mouse_x, last_mouse_y
    if draggingCircle1:
        delta_x = x - last_mouse_x
        delta_y = last_mouse_y - y
        circle1Center = (circle1Center[0] + delta_x / 400, circle1Center[1] + delta_y / 400)
        last_mouse_x, last_mouse_y = x, y
    elif draggingCircle2:
        delta_x = x - last_mouse_x
        delta_y = last_mouse_y - y
        circle2Center = (circle2Center[0] + delta_x / 400, circle2Center[1] + delta_y / 400)
        last_mouse_x, last_mouse_y = x, y

def distance(x, y, center):
    return ((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5

def drawCircles():
    drawCircle(circle1Center, 1.0, (0.807, 0.0, 0.0))
    drawCircle(circle2Center, 1.0, (0.807, 0.0, 0.0))

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Circle Drawing", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glOrtho(-2, 2, -2, 2, -1, 1)
    glClearColor(0.870, 0.905, 0.937, 1.0)  
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        drawCircles()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
