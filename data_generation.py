import numpy as np


def generate_random(size, resolution):
    points = []
    nx = (resolution + 1)
    x = np.random.uniform(low=0, high=size, size=(nx))
    y = np.random.uniform(low=0, high=size, size=(nx))
    z = np.random.uniform(low=0, high=size, size=(nx))

    for i in range(nx):
        points.append(np.array([x[i], y[i], z[i]]))

    return points


def find_nearest_seed(seeds, q):
    nearest_id = 0
    nearest_seed = seeds[nearest_id]

    for i in range(len(seeds)):

        if (np.linalg.norm(seeds[nearest_id] - q) > np.linalg.norm(seeds[i] - q)):
            nearest_id = i
            nearest_seed = seeds[i]

    return nearest_id


def create_grid_2d(size, resolution):
    points = []
    nx = (resolution + 1)
    ny = (resolution + 1)
    x = np.linspace(0, size, num=nx, endpoint=True)
    y = np.linspace(0, size, num=ny, endpoint=True)
    xv, yv = np.meshgrid(x, y)

    for i in range(nx):
        for j in range(ny):
            points.append(np.array([xv[i, j], yv[i, j], 0]))

    return points


def create_grid_3d(size, resolution):
    points = []
    nx = (resolution + 1)
    ny = (resolution + 1)
    nz = (resolution + 1)
    x = np.linspace(0, size, num=nx, endpoint=True)
    y = np.linspace(0, size, num=ny, endpoint=True)
    z = np.linspace(0, size, num=nz, endpoint=True)
    xv, yv = np.meshgrid(x, y)

    for k in range(nz):
        for i in range(nx):
            for j in range(ny):
                points.append(np.array([xv[i, j], yv[i, j], z[k]]))

    return points


def create_honeycomb_2d(size, resolution):
    points = []
    nx = (resolution + 1)
    ny = (resolution + 1)
    x = np.linspace(0, size, num=nx, endpoint=True)
    y = np.linspace(0, size, num=ny, endpoint=True)
    xv, yv = np.meshgrid(x, y)
    dist = size / resolution

    for i in range(nx):
        for j in range(ny):
            offset = 0.5 * dist * (i % 2)
            points.append(np.array([xv[i, j] + offset, yv[i, j], 0]))

    return points


def create_honeycomb_3d(size, resolution):
    points = []
    nx = (resolution + 1)
    ny = (resolution + 1)
    nz = (resolution + 1)
    x = np.linspace(0, size, num=nx, endpoint=True)
    y = np.linspace(0, size, num=ny, endpoint=True)
    z = np.linspace(0, size, num=nz, endpoint=True)
    xv, yv = np.meshgrid(x, y)
    dist = size / resolution

    for k in range(nz):
        for i in range(nx):
            for j in range(ny):
                if (k % 2):
                    offsetx = 0.5 * dist * (i % 2)
                    offsety = 0.5 * dist * ((j + 1) % 2)
                    offsetz = 0.5 * dist * ((k + 1) % 2)
                else:
                    offsetx = 0.5 * dist * ((i + 1) % 2)
                    offsety = 0.5 * dist * (j % 2)
                    offsetz = 0.5 * dist * ((k + 1) % 2)

                points.append(np.array([xv[i, j] + offsetx, yv[i, j] + offsety, z[k]]))

    return points
