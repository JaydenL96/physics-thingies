import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CENTER = np.array([WIDTH // 2, HEIGHT // 2])

class Cube:
    def __init__(self, size, center):
        half_size = size / 2
        self.vertices = np.array([
            [center[0] - half_size, center[1] - half_size, -half_size],
            [center[0] + half_size, center[1] - half_size, -half_size],
            [center[0] + half_size, center[1] + half_size, -half_size],
            [center[0] - half_size, center[1] + half_size, -half_size],
            [center[0] - half_size, center[1] - half_size, half_size],
            [center[0] + half_size, center[1] - half_size, half_size],
            [center[0] + half_size, center[1] + half_size, half_size],
            [center[0] - half_size, center[1] + half_size, half_size]
        ])
        self.edges = self._create_edges()

    def _create_edges(self):
        edges = []
        for i in range(4):
            edges.append((i, (i + 1) % 4))  # Base edges
            edges.append((i + 4, (i + 1) % 4 + 4))  # Top edges
            edges.append((i, i + 4))  # Vertical edges
        return edges

    def draw(self, screen, angle_x, angle_y, angle_z):
        rotated = rotate(self.vertices, angle_x, angle_y, angle_z)
        projected = rotated[:, :2] + CENTER
        draw_edges(screen, projected, self.edges)

class Sphere:
    def __init__(self, radius, center, num_latitude=10, num_longitude=20):
        self.vertices = self._create_vertices(radius, center, num_latitude, num_longitude)
        self.edges = self._create_edges(num_latitude, num_longitude)

    def _create_vertices(self, radius, center, num_latitude, num_longitude):
        vertices = []
        for i in range(num_latitude + 1):
            theta = math.pi * i / num_latitude  # polar angle
            for j in range(num_longitude):
                phi = 2 * math.pi * j / num_longitude  # azimuthal angle
                x = radius * math.sin(theta) * math.cos(phi) + center[0]
                y = radius * math.sin(theta) * math.sin(phi) + center[1]
                z = radius * math.cos(theta) + center[2]
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

    def draw(self, screen, angle_x, angle_y, angle_z):
        rotated = rotate(self.vertices, angle_x, angle_y, angle_z)
        projected = rotated[:, :2]  # Sphere is already 2D
        draw_edges(screen, projected, self.edges)

class Pyramid:
    def __init__(self, size, center):
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

    def draw(self, screen, angle_x, angle_y, angle_z):
        rotated = rotate(self.vertices, angle_x, angle_y, angle_z)
        projected = rotated[:, :2] + CENTER
        draw_edges(screen, projected, self.edges)

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
        pygame.draw.line(screen, (255, 255, 255), vertices[start], vertices[end])

# Main loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0
    cube_size = 200
    sphere_radius = 100
    pyramid_size = 200
    center = np.array([WIDTH // 2, HEIGHT // 2, 0])

    cube = Cube(cube_size, center)
    sphere = Sphere(sphere_radius, center, num_latitude=10, num_longitude=20)
    pyramid = Pyramid(pyramid_size, center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Clear screen
        screen.fill((0, 0, 0))

        # Rotate shapes
        angle_x += 0.01
        angle_y += 0.01
        angle_z += 0.01

        # Draw shapes
        cube.draw(screen, angle_x, angle_y, angle_z)
        sphere.draw(screen, angle_x, angle_y, angle_z)
        pyramid.draw(screen, angle_x, angle_y, angle_z)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
