
import numpy as np


def FindNearestSeed(seeds, q):

    nearest_id = 0
    nearest_seed = seeds[nearest_id]

    for i in range(len(seeds)):

        if (np.linalg.norm(seeds[nearest_id] - q) > np.linalg.norm(seeds[i] - q)):
            nearest_id = i
            nearest_seed = seeds[i]


    return nearest_id


def CreateGrid2D(size, resolution):

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