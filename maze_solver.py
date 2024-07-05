import heapq
import random
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def dijkstra(graph, start, goal):
    queue = [(0, start)]
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    came_from = {node: None for node in graph}
    visited = set()

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        visited.add(current_node)

        if current_node == goal:
            break

        for neighbor, weight in graph[current_node]:
            if neighbor in visited:
                continue
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                came_from[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return came_from, distances


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def create_grid_graph(size, obstacles):
    graph = {}
    for i in range(size):
        for j in range(size):
            if (i, j) in obstacles:
                continue
            graph[(i, j)] = []
            if i > 0 and (i - 1, j) not in obstacles:
                graph[(i, j)].append(((i - 1, j), 1))
            if i < size - 1 and (i + 1, j) not in obstacles:
                graph[(i, j)].append(((i + 1, j), 1))
            if j > 0 and (i, j - 1) not in obstacles:
                graph[(i, j)].append(((i, j - 1), 1))
            if j < size - 1 and (i, j + 1) not in obstacles:
                graph[(i, j)].append(((i, j + 1), 1))
    return graph


def generate_maze(size):
    maze = np.ones((size, size), dtype=bool)

    def carve_passages(cx, cy):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        stack = [(cx, cy)]

        while stack:
            x, y = stack[-1]
            maze[x, y] = False
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size and maze[nx, ny]:
                    if (nx >= 2 and not maze[nx - 2, ny]) or (nx < size - 2 and not maze[nx + 2, ny]) or \
                       (ny >= 2 and not maze[nx, ny - 2]) or (ny < size - 2 and not maze[nx, ny + 2]):
                        maze[nx, ny] = False
                        maze[x + dx // 2, y + dy // 2] = False
                        stack.append((nx, ny))
                        break
            else:
                stack.pop()

    maze[1, 1] = False
    carve_passages(1, 1)
    obstacles = [(i, j) for i in range(size) for j in range(size) if maze[i, j]]
    return obstacles


def animate_dijkstra(graph, start, goal, size, obstacles):
    came_from, distances = dijkstra(graph, start, goal)
    path = reconstruct_path(came_from, start, goal)

    fig, ax = plt.subplots()

    data = np.full((size, size), np.inf)
    for node in graph:
        data[node[0], node[1]] = distances[node]

    for obstacle in obstacles:
        data[obstacle[0], obstacle[1]] = -1

    cax = ax.matshow(data, cmap='viridis')
    mappable = ax.matshow(data, cmap='viridis')
    plt.colorbar(mappable)

    def update(frame):
        ax.clear()
        ax.matshow(data, cmap='viridis')
        for obstacle in obstacles:
            ax.plot(obstacle[1], obstacle[0])
        ax.plot(start[1], start[0], 'go')  # start point
        ax.plot(goal[1], goal[0], 'ro')  # end point

        # Draw the path up to the current frame
        if frame < len(path):
            for point in path[1:-1]:
                ax.scatter(point[1], point[0], color='b', s=1)  # blue points for path
        return []

    ani = animation.FuncAnimation(fig, update, frames=len(path) + 10, interval=200, blit=True, repeat=False)
    plt.show()


if __name__ == "__main__":
    size = 101  # Should be an odd number for maze generation
    start = (1, 1)
    goal = (size - 2, size - 2)
    start_time = time.time()
    print("maze maken")
    obstacles = generate_maze(size)
    end_time = time.time()
    print(f"maze algorithm completed in {end_time - start_time:.2f} seconds")
    graph = create_grid_graph(size, obstacles)
    start_time = time.time()
    print("oplossen maar")
    animate_dijkstra(graph, start, goal, size, obstacles)
    end_time = time.time()
    print(f"Dijkstra's algorithm completed in {end_time - start_time:.2f} seconds")
