import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

numCircles = 50

circleCenters = [(random.uniform(-4, 4), random.uniform(-4, 4)) for _ in range(numCircles)]

draggingCircle = [False] * numCircles
lastMouseX = [0] * numCircles
lastMouseY = [0] * numCircles

movementInterval = 25
maxMovement = 0.05
boundaryX = 4.0
boundaryY = 4.0

def drawCircle(center, radius, color):
    numSegments = 100  

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*color)
    
    glVertex2f(center[0], center[1])

    for i in range(numSegments + 1):
        theta = 2.0 * pi * i / numSegments
        x = radius * cos(theta) + center[0]
        y = radius * sin(theta) + center[1]
        glVertex2f(x, y)

    glEnd()

def mouseButtonCallback(window, button, action, mods):
    global draggingCircle, lastMouseX, lastMouseY
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            x, y = glfw.getCursorPos(window)
            for i in range(numCircles):
                if distance(x, y, circleCenters[i]) < 1.0:
                    draggingCircle[i] = True
                lastMouseX[i], lastMouseY[i] = x, y
        elif action == glfw.RELEASE:
            for i in range(numCircles):
                draggingCircle[i] = False

def cursorPosCallback(window, x, y):
    global draggingCircle, lastMouseX, lastMouseY
    for i in range(numCircles):
        if draggingCircle[i]:
            deltaX = x - lastMouseX[i]
            deltaY = lastMouseY[i] - y
            circleCenters[i] = (circleCenters[i][0] + deltaX / 400, circleCenters[i][1] + deltaY / 400)
            lastMouseX[i], lastMouseY[i] = x, y

def distance(x, y, center):
    return ((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5

def updateCircles():
    for i in range(numCircles):
        x, y = circleCenters[i]
        x += random.uniform(-maxMovement, maxMovement)
        y += random.uniform(-maxMovement, maxMovement)

        if x < -boundaryX:
            x = boundaryX
        elif x > boundaryX:
            x = -boundaryX

        if y < -boundaryY:
            y = boundaryY
        elif y > boundaryY:
            y = -boundaryY

        circleCenters[i] = (x, y)

def drawCircles():
    for center in circleCenters:
        drawCircle(center, 0.1, (random.random(), random.random(), random.random()))

def main():
    if not glfw.init():
        return

    window = glfw.createWindow(800, 800, "Circle Drawing", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.makeContextCurrent(window)

    glOrtho(-5, 5, -5, 5, -1, 1)
    glClearColor(0.870, 0.905, 0.937, 1.0)

    glfw.setMouseButtonCallback(window, mouseButtonCallback)
    glfw.setCursorPosCallback(window, cursorPosCallback)

    lastTime = glfw.getTime()

    while not glfw.windowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT)

        current_time = glfw.getTime()
        if current_time - lastTime >= movementInterval / 1000:
            updateCircles()
            lastTime = current_time

        drawCircles()

        glfw.swapBuffers(window)
        glfw.pollEvents()

    glfw.terminate()

if __name__ == "__main__":
    main()
