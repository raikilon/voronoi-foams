import numpy as np
import open3d as o3d
import pymesh


def visualize_cloud(points):
    """

    :param points: np array of points [[x,y,z],[x,y,z]]
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.paint_uniform_color([0, 0, 1])
    o3d.visualization.draw_geometries([pcd])


def visualize_cell(seeds, beam_points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(beam_points)
    pcd.paint_uniform_color([0, 0, 0])
    pcd1 = o3d.geometry.PointCloud()
    pcd1.points = o3d.utility.Vector3dVector(seeds)
    pcd1.paint_uniform_color([1, 0, 0])
    o3d.visualization.draw_geometries([pcd, pcd1])


def save_cube_union(centers, tau, name):
    meshes = []
    for s in centers:
        box = pymesh.generate_box_mesh(s - tau / 2, s + tau / 2)
        meshes.append({"mesh": box})
    csg = pymesh.CSGTree({"union": meshes})
    pymesh.save_mesh("models/{}.obj".format(name), csg.mesh)


def save_list_cube(centers, tau, name):
    vertices = []
    faces = []
    for s in centers:
        box = pymesh.generate_box_mesh(s - tau / 2, s + tau / 2)
        ver_s = len(vertices)
        vertices.extend(box.vertices)
        faces.extend(box.faces + ver_s)
    mesh = pymesh.form_mesh(np.array(vertices), np.array(faces))
    pymesh.save_mesh("models/{}.obj".format(name), mesh)
