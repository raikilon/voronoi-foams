import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
from subdivision import __sample_new_point


def subdivide_square(origin_square, length_square, seeds, density_func):
    length_halfsquare = 0.5 * length_square
    rho = density_func(origin_square + length_halfsquare)
    target_seeds = (length_square ** 3) * rho
    if target_seeds <= 8:
        np.random.seed(int(origin_square[0] * 7873 + origin_square[1] * 6269 + origin_square[2] * 2531 + 10000000))
        # 1st case: the cell is a leaf
        shuffled_idx = np.random.permutation(8)
        min_samples = int(np.floor(target_seeds))
        proba_last = target_seeds - min_samples
        for i in range(min_samples):
            seeds.append(__sample_new_point(origin_square, length_halfsquare, shuffled_idx[i]))
        if np.random.random() <= proba_last and min_samples < 8:
            seeds.append(__sample_new_point(origin_square, length_halfsquare, shuffled_idx[min_samples]))
    else:
        # 2nd case: recursive call
        for offx in [-1, 1]:
            for offy in [-1, 1]:
                for offz in [-1, 1]:
                    offset = np.array([offx, offy, offz], dtype=float)
                    origin_subsquare = origin_square + offset * (length_halfsquare / 2)
                    subdivide_square(origin_subsquare, length_halfsquare, seeds, density_func)

    return seeds


def generate_seeds(coarse_level_length, extent):
    def density_func(point):
        # grading in x direction
        seed_density_factor = 10
        return (point[2] / extent[2]) * seed_density_factor  # seeds / mm^2

    seeds = []
    for origin_x in np.arange(0.0, extent[0], coarse_level_length):
        for origin_y in np.arange(0.0, extent[1], coarse_level_length):
            for origin_z in np.arange(0.0, extent[2], coarse_level_length):
                origin_square_coarse = np.array([origin_x, origin_y, origin_z], dtype=float)
                subdivide_square(origin_square_coarse, coarse_level_length, seeds, density_func)

    return seeds


if __name__ == "__main__":
    coarse_level_length = 2.0  # (mm)
    extent = np.array([4.0, 4.0, 16.0], dtype=float)  # (mm)
    seeds = generate_seeds(coarse_level_length, extent)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(seeds)
    pcd.paint_uniform_color([0, 0, 1])
    o3d.visualization.draw_geometries([pcd])
    # plot_seeds(seeds, extent)
