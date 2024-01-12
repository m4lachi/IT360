import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

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

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)


        drawCircle((-1.0, 0.0), 1.0, (0.807, 0.0, 0.0))

       
        drawCircle((1.0, 0.0), 1.0, (0.807, 0.0, 0.0))

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
