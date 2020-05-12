import pymesh


def voxelize_mesh():
    mesh = load_mesh("models/diamond.obj")
    grid = pymesh.VoxelGrid(1, mesh.dim)
    grid.insert_mesh(mesh)
    grid.create_grid()
    out_mesh = grid.mesh
    pymesh.save_mesh("models/diamondvoxel.obj", out_mesh)


def load_mesh(path):
    mesh = pymesh.load_mesh(path)
    return mesh


def save_mesh(path, mesh):
    pymesh.save_mesh(path, mesh)


voxelize_mesh()
