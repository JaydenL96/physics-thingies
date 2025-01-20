import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CENTER = np.array([WIDTH // 2, HEIGHT // 2])

# Perspective scaling factor
PERSPECTIVE_SCALE = 500

class Cube:
    def __init__(self, size, center):
        self.center = np.array(center)
        half_size = size / 2
        self.vertices = np.array([
            [center[0] - half_size, center[1] - half_size, center[2] - half_size],
            [center[0] + half_size, center[1] - half_size, center[2] - half_size],
            [center[0] + half_size, center[1] + half_size, center[2] - half_size],
            [center[0] - half_size, center[1] + half_size, center[2] - half_size],
            [center[0] - half_size, center[1] - half_size, center[2] + half_size],
            [center[0] + half_size, center[1] - half_size, center[2] + half_size],
            [center[0] + half_size, center[1] + half_size, center[2] + half_size],
            [center[0] - half_size, center[1] + half_size, center[2] + half_size]
        ])
        self.edges = self._create_edges()

    def _create_edges(self):
        edges = []
        for i in range(4):
            edges.append((i, (i + 1) % 4))  # Base edges
            edges.append((i + 4, (i + 1) % 4 + 4))  # Top edges
            edges.append((i, i + 4))  # Vertical edges
        return edges

    def draw(self, screen, angle_x, angle_y, angle_z, camera_pos):
        relative_vertices = self.vertices - self.center
        rotated = rotate(relative_vertices, angle_x, angle_y, angle_z)
        rotated += self.center  # Translate back
        relative_to_camera = rotated - camera_pos
        draw_edges(screen, relative_to_camera, self.edges)

class Sphere:
    def __init__(self, radius, center, num_latitude=10, num_longitude=20):
        self.center = np.array(center)
        self.vertices = self._create_vertices(radius, num_latitude, num_longitude)
        self.edges = self._create_edges(num_latitude, num_longitude)

    def _create_vertices(self, radius, num_latitude, num_longitude):
        vertices = []
        for i in range(num_latitude + 1):
            theta = math.pi * i / num_latitude  # polar angle
            for j in range(num_longitude):
                phi = 2 * math.pi * j / num_longitude  # azimuthal angle
                x = radius * math.sin(theta) * math.cos(phi)
                y = radius * math.sin(theta) * math.sin(phi)
                z = radius * math.cos(theta)
                vertices.append([x, y, z])
        return np.array(vertices)

    def _create_edges(self, num_latitude, num_longitude):
        edges = []
        for i in range(num_latitude):
            for j in range(num_longitude):
                next_j = (j + 1) % num_longitude
                edges.append((i * num_longitude + j, i * num_longitude + next_j))  # Horizontal edges
                edges.append((i * num_longitude + j, (i + 1) * num_longitude + j))  # Vertical edges
        return edges

    def draw(self, screen, angle_x, angle_y, angle_z, camera_pos):
        relative_vertices = self.vertices - self.center
        rotated = rotate(relative_vertices, angle_x, angle_y, angle_z)
        rotated += self.center  # Translate back
        relative_to_camera = rotated - camera_pos
        draw_edges(screen, relative_to_camera, self.edges)

class Pyramid:
    def __init__(self, size, center):
        self.center = np.array(center)
        half_size = size / 2
        self.vertices = np.array([
            [center[0], center[1], center[2] + half_size],  # Apex
            [center[0] - half_size, center[1] - half_size, center[2] - half_size],
            [center[0] + half_size, center[1] - half_size, center[2] - half_size],
            [center[0] + half_size, center[1] + half_size, center[2] - half_size],
            [center[0] - half_size, center[1] + half_size, center[2] - half_size]
        ])
        self.edges = self._create_edges()

    def _create_edges(self):
        edges = []
        for i in range(1, 5):
            edges.append((0, i))  # Apex to base
        for i in range(1, 5):
            edges.append((i, (i % 4) + 1))  # Base edges
        return edges

    def draw(self, screen, angle_x, angle_y, angle_z, camera_pos):
        relative_vertices = self.vertices - self.center
        rotated = rotate(relative_vertices, angle_x, angle_y, angle_z)
        rotated += self.center  # Translate back
        relative_to_camera = rotated - camera_pos
        draw_edges(screen, relative_to_camera, self.edges)

# Rotation matrices
def rotation_matrix_x(angle):
    return np.array([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])

def rotation_matrix_y(angle):
    return np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])

def rotation_matrix_z(angle):
    return np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

# Function to rotate points
def rotate(points, angle_x, angle_y, angle_z):
    rotated = points @ rotation_matrix_x(angle_x).T
    rotated = rotated @ rotation_matrix_y(angle_y).T
    rotated = rotated @ rotation_matrix_z(angle_z).T
    return rotated

# Function to draw edges
def draw_edges(screen, vertices, edges):
    for start, end in edges:
        z_start = max(1, vertices[start][2])  # Prevent division by zero
        z_end = max(1, vertices[end][2])      # Prevent division by zero

        # Perspective projection
        perspective_start = vertices[start][:2] / z_start * PERSPECTIVE_SCALE
        perspective_end = vertices[end][:2] / z_end * PERSPECTIVE_SCALE

        # Shift to the screen center
        start_pos = perspective_start + CENTER
        end_pos = perspective_end + CENTER

        pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos)

# Main loop
def main():
    global WIDTH, HEIGHT, CENTER
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    WIDTH, HEIGHT = screen.get_size()
    CENTER = np.array([WIDTH // 2, HEIGHT // 2])
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0
    cube_size = 200
    sphere_radius = 100
    pyramid_size = 200
    camera_pos = np.array([0, 0, -500])  # Camera starts far back
    center = np.array([0, 0, 0])

    cube = Cube(cube_size, center)
    sphere = Sphere(sphere_radius, center, num_latitude=10, num_longitude=20)
    pyramid = Pyramid(pyramid_size, center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Handle camera movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera_pos[2] += 5  # Move forward
        if keys[pygame.K_s]:
            camera_pos[2] -= 5  # Move backward
        if keys[pygame.K_a]:
            camera_pos[0] -= 5  # Move left
        if keys[pygame.K_d]:
            camera_pos[0] += 5  # Move right
        if keys[pygame.K_UP]:
            camera_pos[1] -= 5  # Move up
        if keys[pygame.K_DOWN]:
            camera_pos[1] += 5  # Move down

        # Clear screen
        screen.fill((0, 0, 0))

        # Rotate shapes
        angle_x += 0.01
        angle_y += 0.01
        angle_z += 0.01

        # Draw shapes
        cube.draw(screen, angle_x, angle_y, angle_z, camera_pos)
        sphere.draw(screen, angle_x, angle_y, angle_z, camera_pos)
        pyramid.draw(screen, angle_x, angle_y, angle_z, camera_pos)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
