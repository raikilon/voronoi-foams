import pymesh
import numpy as np
from pymesh import VoxelGrid

def voxelize_mesh():
    mesh = load_mesh("models/cube.obj")
    grid = pymesh.VoxelGrid(0.3, mesh.dim)
    grid.insert_mesh(mesh)
    grid.create_grid()
    out_mesh = grid.mesh
    pymesh.save_mesh("models/voxel.obj", out_mesh)


def load_mesh(path):
    mesh = pymesh.load_mesh(path)
    return mesh


def save_mesh(path, mesh):
    pymesh.save_mesh(path, mesh)


voxelize_mesh()
