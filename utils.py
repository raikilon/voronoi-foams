import open3d as o3d


def visualize_cloud(points):
    """

    :param points: np array of points [[x,y,z],[x,y,z]]
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.paint_uniform_color([0, 0, 1])
    o3d.visualization.draw_geometries([pcd])
