if __name__ == '__build__':
    raise Exception

import sys
import math
from math import cos as cos
from math import sin as sin
from math import pi as PI
from math import sqrt as sqrt
import glfw 

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except BaseException:
    print('''
ERROR: PyOpenGL not installed properly.
        ''')
    sys.exit()


screen_dimx = 550
screen_dimy = 550
screen_leftx = -15
screen_rightx = 15
screen_topy = -15
screen_bottomy = 15
screen_world_width = screen_rightx-screen_leftx
screen_world_height = screen_bottomy-screen_topy

time_delta = 1 / 64.
particle_radii = 0.75
last_time=0.0
dragged_particle = None
is_dragging = False
particle_distance = particle_radii * 2.5



class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.px = x
        self.py = y
        self.r = particle_radii
        self.inv_mass = 1.0


class Constraint:
    def __init__(self, id1, id2, distance):
        self.id1 = id1
        self.id2 = id2
        self.distance = distance
        self.stiffness = 0.1


class PointConstraint:
    def __init__(self, id1, x, y):
        self.id1 = id1
        self.x = x
        self.y = y


particles = [Particle(0.0,0.0)] + [ Particle(-15 * particle_radii + i * particle_radii *
                      2.2, particle_radii * i) for i in range(10)]


point_constraints = [PointConstraint(0,
                                     0.0,
                                     0.0)]


def draw_circle_outline(r, x, y):
    i = 0.0
    glLineWidth(3)
    glBegin(GL_LINE_LOOP)
    while i <= 360.0:
        glVertex2f(r * cos(PI * i / 180.0) + x,
                   r * sin(PI * i / 180.0) + y)
        i += 360.0 / 18.0
    glEnd()


def draw_circle(r, x, y):
    i = 0.0
    glLineWidth(1)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    while i <= 360.0:
        glVertex2f(r * cos(PI * i / 180.0) + x,
                   r * sin(PI * i / 180.0) + y)
        i += 360.0 / 18.0
    glEnd()


def drawParticles():
    global dragged_particle
    global particles
    glColor3f(0.494, 0.616, 0.761)
    for particle in particles:
        draw_circle(particle_radii, particle.x, particle.y)
    if dragged_particle is not None:
        glColor3f(1.0, 0.059, 0.224)
        draw_circle_outline(
            particle_radii,
            dragged_particle.x,
            dragged_particle.y)


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


def point_constraint(particle1, x2, y2):
    correction_x1 = x2 - particle1.px
    correction_y1 = y2 - particle1.py
    return (correction_x1, correction_y1)


def pbd_main_loop():
    global particles
    gravity = 0.0
    for particle in particles:
        # apply external forces - line 5
        particle.vx += 0.0
        particle.vy += (gravity) * time_delta
        # damp velocities - line 6
        particle.vx *= 0.8
        particle.vy *= 0.8
        # get initial projected positions - line 7
        particle.px = particle.x + particle.vx * time_delta
        particle.py = particle.y + particle.vy * time_delta

    # line 9-10
    for constraint in point_constraints:
            delta_x1, delta_y1 = point_constraint(particles[constraint.id1], constraint.x, constraint.y)
            particles[constraint.id1].px += delta_x1
            particles[constraint.id1].py += delta_y1

    # line 12
    for particle in particles:
        # line 13
        particle.vx = (particle.px - particle.x) / time_delta
        particle.vy = (particle.py - particle.y) / time_delta
        # line 14
        particle.x = particle.px
        particle.y = particle.py
    glfw.post_empty_event()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    drawParticles()
    glFlush()


def particle_clicked(x, y):
    res = None
    for particle in particles:
        if distance(x, y, particle.x, particle.y) <= particle_radii:
            return particle
    return res



def translate_to_world_coords(screenx, screeny):
    x = (screenx-screen_dimx/2)/screen_dimx* screen_world_width  
    y=  (screeny-screen_dimy/2)/screen_dimy* screen_world_height
    return (x, y)

def mouse_button_callback(window, button, action, mods):
    global dragged_particle, is_dragging
    x, y = glfw.get_cursor_pos(window)
    worldx,worldy = translate_to_world_coords(x,y)
    particle = particle_clicked(worldx, worldy)
    dragged_particle = particle
    if button == 0 and dragged_particle is not None:
        is_dragging = not is_dragging
        dragged_particle.inv_mass = 1.0
    if button == 1 and not is_dragging:
        dragged_particle = None

def cursor_position_callback(window,x,y ):
    global dragged_particle, is_dragging
    if(x >=0 and x < screen_dimx and 
       y >=0 and y < screen_dimy):
        if is_dragging:
            if dragged_particle is not None:
                worldx, worldy = translate_to_world_coords(x,y)
                dragged_particle.x = worldx
                dragged_particle.y = worldy
                dragged_particle.inv_mass = 0



# Initialize the library
if not glfw.init():
    exit()

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(screen_dimx, screen_dimy, "White Square on Black Background", None, None)
if not window:
    glfw.terminate()
    exit()

# Make the window's context current
glfw.make_context_current(window)

# Set callbacks
glfw.set_mouse_button_callback(window, mouse_button_callback)
#glutPassiveMotionFunc(mousePassive)
glfw.set_cursor_pos_callback(window, cursor_position_callback);

gluOrtho2D(screen_leftx,
            screen_rightx,
            screen_bottomy,
            screen_topy)

# Main loop
while not glfw.window_should_close(window):
    # Clear the screen with black color
    pbd_main_loop()
    display()
    # Swap front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

# Terminate GLFW
glfw.terminate()