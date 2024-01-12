import glfw
from OpenGL.GL import *
import math
import random
import time

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 16900, 9000
AGENT_RADIUS = 0.0045
BORDER_THICKNESS = 0.03
NUM_AGENTS = 300
VELOCITY_SCALE = 0.045  
TIME_STEP = 0.0010  

# Agent class
class Agent:
    def __init__(self):
        self.x = random.uniform(0, 1)
        self.y = random.uniform(0, 1)
        self.vx = random.uniform(-0.01, 0.01)
        self.vy = random.uniform(-0.01, 0.01)

# List to store agents
agents = [Agent() for _ in range(NUM_AGENTS)]

# Avoidance force function
def avoidance_force(agent, other_agent, distance_threshold=0.15):
    dx = other_agent.x - agent.x
    dy = other_agent.y - agent.y
    distance = math.sqrt(dx * dx + dy * dy)
    
    if distance < distance_threshold:
        return (-dx / distance, -dy / distance)
    else:
        return (0, 0)

# Update function to calculate new velocities for agents
def update_agents():
    for agent in agents:
        total_force_x, total_force_y = 0, 0
        
        for other_agent in agents:
            if other_agent != agent:
                force_x, force_y = avoidance_force(agent, other_agent)
                total_force_x += force_x
                total_force_y += force_y
        
        # Update velocity 
        agent.vx += total_force_x * VELOCITY_SCALE
        agent.vy += total_force_y * VELOCITY_SCALE
        
        # Update agent position 
        agent.x += agent.vx * TIME_STEP
        agent.y += agent.vy * TIME_STEP
        
        # Wrap around to the other side of the border
        agent.x = agent.x % 1
        agent.y = agent.y % 1

# Variables for FPS calculation
frame_count = 0
start_time = time.time()

# Function to calculate and display FPS
def display_fps():
    global frame_count, start_time
    frame_count += 1
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time >= 1.0: 
        fps = frame_count / elapsed_time
        print(f"FPS: {fps:.2f}")
        frame_count = 0
        start_time = current_time

        glfw.set_window_title(window, f"Crowd Simulation - FPS: {fps:.2f}")

# Initialize the library
if not glfw.init():
    exit()

window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Crowd Simulation", None, None)
if not window:
    glfw.terminate()
    exit()

glfw.make_context_current(window)

# Main loop
while not glfw.window_should_close(window):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    update_agents()

    # Draw a border around the window
    glColor3f(1.0, 1.0, 1.0)  
    glBegin(GL_LINE_LOOP)
    glVertex2f(0, 0)
    glVertex2f(1, 0)
    glVertex2f(1, 1)
    glVertex2f(0, 1)
    glEnd()

    for agent in agents:
        # Draw agents as circles
        glColor3f(1.0, 1.0, 1.0)  
        glBegin(GL_POLYGON)
        for i in range(360):
            angle = math.radians(i)
            x = agent.x + AGENT_RADIUS * math.cos(angle)
            y = agent.y + AGENT_RADIUS * math.sin(angle)
            glVertex2f(x, y)
        glEnd()

     # Display FPS on the window
    display_fps()

    glfw.swap_buffers(window)
    glfw.poll_events()

# Terminate GLFW
glfw.terminate()