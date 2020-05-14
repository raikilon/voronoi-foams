import pymesh
import numpy as np
from utils import visualize_cloud


def voxelize_mesh():
    mesh = load_mesh("models/cube.obj")
    grid = pymesh.VoxelGrid(0.05, mesh.dim)
    grid.insert_mesh(mesh)
    grid.create_grid()
    out_mesh = grid.mesh
    centers = np.mean(out_mesh.vertices[out_mesh.elements], axis=1)
    np.save("models/cube_voxels.npy", centers)
    visualize_cloud(centers)
    # pymesh.save_mesh("models/voxel.obj", out_mesh)


def load_mesh(path):
    mesh = pymesh.load_mesh(path)
    return mesh


def save_mesh(path, mesh):
    pymesh.save_mesh(path, mesh)


voxelize_mesh()
