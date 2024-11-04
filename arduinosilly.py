import pygame
import math
import serial
import time

# Set up serial communication (adjust COM port as needed)
ser = serial.Serial('COM7', 9600)
time.sleep(2)

# Initialize pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Radar Visualization")

# Colors
BLACK = (0, 0, 0)
GREEN = (98, 245, 31)
RED = (255, 10, 10)

# Radar center and radius
center_x, center_y = width // 2, height - 50
radius = 250

def draw_radar():
    screen.fill(BLACK)
    pygame.draw.circle(screen, GREEN, (center_x, center_y), radius, 1)
    pygame.draw.circle(screen, GREEN, (center_x, center_y), radius // 2, 1)
    pygame.draw.line(screen, GREEN, (center_x, center_y), (center_x - radius, center_y), 1)
    pygame.draw.line(screen, GREEN, (center_x, center_y), (center_x + radius, center_y), 1)
    pygame.draw.line(screen, GREEN, (center_x, center_y), (center_x, center_y - radius), 1)

def draw_object(angle, distance):
    """Draws the detected object based on angle and distance."""
    angle_rad = math.radians(angle)
    dist_scaled = distance * radius / 40  # Scale distance to radar range

    # Calculate object's position
    obj_x = center_x + dist_scaled * math.cos(angle_rad)
    obj_y = center_y - dist_scaled * math.sin(angle_rad)

    # Draw line and circle for detected object
    pygame.draw.line(screen, RED, (center_x, center_y), (obj_x, obj_y), 5)
    pygame.draw.circle(screen, RED, (int(obj_x), int(obj_y)), 3)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_radar()

        if ser.in_waiting > 0:
            try:
                # Read and decode serial data
                data = ser.readline().decode().strip()
                
                # Split data by commas and parse
                angle_str, distance_str = data.split(",")
                angle = int(angle_str)
                distance = int(distance_str.split(".")[0])  # Remove trailing period if any

                # Debug output for parsed values
                print(f"Angle: {angle}, Distance: {distance}")

                # Draw object based on angle and distance
                draw_object(angle, distance)

            except ValueError as e:
                print(f"Error parsing data: {e}")

        pygame.display.flip()
        pygame.time.delay(30)

    pygame.quit()
    ser.close()

if __name__ == "__main__":
    main()
