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

# Define spatial hash parameters
CELL_SIZE = 0.1  
GRID_WIDTH = int(1 / CELL_SIZE)
GRID_HEIGHT = int(1 / CELL_SIZE)

# Create a spatial hash with cells
spatial_hash = {(x, y): [] for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}

# Function to map agent positions to grid cells and handle out-of-bounds
def map_to_grid(x, y):
    cell_x = min(max(int(x / CELL_SIZE), 0), GRID_WIDTH - 1)
    cell_y = min(max(int(y / CELL_SIZE), 0), GRID_HEIGHT - 1)
    return cell_x, cell_y        

# Update function to calculate new velocities for agents
def update_agents():
    for cell in spatial_hash:
        spatial_hash[cell] = []
    
    for agent in agents:
        total_force_x, total_force_y = 0, 0
        
        cell_x, cell_y = map_to_grid(agent.x, agent.y)
        spatial_hash[(cell_x, cell_y)].append(agent)
        
        for x in range(cell_x - 1, cell_x + 2):
            for y in range(cell_y - 1, cell_y + 2):
                if (x, y) in spatial_hash:
                    for other_agent in spatial_hash[(x, y)]:
                        if other_agent != agent:
                            force_x, force_y = avoidance_force(agent, other_agent)
                            total_force_x += force_x
                            total_force_y += force_y
        
        agent.vx += total_force_x * VELOCITY_SCALE
        agent.vy += total_force_y * VELOCITY_SCALE
        
        agent.x += agent.vx * TIME_STEP
        agent.y += agent.vy * TIME_STEP
        
        agent.x = agent.x % 1
        agent.y = agent.y % 1


# Variables for FPS calculation
frame_count = 0
start_time = time.time()

# Function to calculate and display FPS
def display_fps():
    global frame_count, start_time
    frame_count += 1
    current_time = time.t bime()
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