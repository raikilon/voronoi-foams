import multiprocessing

import numpy as np
from joblib import Parallel, delayed

import data_generation as dgen
import debug_plot as dplot
import voronoi as voronoi
from subdivision import gather_seeds
from utils import save_list_cube
from utils import visualize_cell


def check_values(res, GT, func):
    if (res == GT).all():
        print("testing {} passed. res and GT are {}".format(func, res))
    else:
        print("testing {} failed. res is {}, GT is {}".format(func, res, GT))


def test_gen_data():
    rho = 1
    tau = 0.05

    size = 1
    resolution = 100

    seeds = dgen.create_honeycomb_3d(size, 5)

    dplot.plot_3d(seeds)


def test_eval_structure():
    rho = 1
    tau = 0.05

    beam_points = []
    size = 1
    resolution = 20

    seeds = dgen.generate_random(size, 3)
    qs = dgen.create_grid_3d(size, resolution)

    for i in range(len(qs)):
        q = qs[i]

        # re-arrange order, first is the nearest seed to q
        nearest_id = dgen.find_nearest_seed(seeds, q)
        nearest_seed = seeds.pop(nearest_id)
        seeds.insert(0, nearest_seed)

        bl_list = []
        isBeam = voronoi.eval_structure(rho, tau, q, seeds, bl_list)
        if isBeam:
            beam_points.append(q)
            print("beam point :  {}".format(q))
    # dplot.plot_bl(bl_list, seeds, q)

    dplot.plot_3d_all(seeds, beam_points)


def test_eval_structure_random_seed():
    rho = 8
    tau = 0.05
    voxel_centers = np.load("models/voxels.npy")
    seeds = gather_seeds(rho, np.array([0, 0, 0]))
    num_cores = multiprocessing.cpu_count()

    beam_points = Parallel(n_jobs=num_cores)(delayed(compute_q)(i, rho, tau) for i in voxel_centers)
    beam_points = list(filter(any, beam_points))

    save_list_cube(seeds, tau, "final_seeds")
    save_list_cube(beam_points, tau, "final_voxels")

    visualize_cell(seeds, beam_points)


def compute_q(q, rho, tau):
    is_beam = voronoi.eval_structure(rho, tau, q, None, [])
    if is_beam:
        # print("beam point :  {}".format(q))
        return q
    else:
        return [None, None, None]


def test_bisector_line_equation():
    p1 = np.array([2, 0, 0])
    p2 = np.array([0, 0, 0])
    GT1 = np.array([1, 0, 0, 0])

    bp1 = voronoi.bisector_plane(p1, p2)
    # CheckValues(bp1, GT1, "bisector_plane")

    p3 = np.array([0, 2, 0])
    GT2 = np.array([0, 1, 0, 0])

    bp2 = voronoi.bisector_plane(p2, p3)
    # CheckValues(bp2, GT2, "bisector_plane")

    # a, b, c
    GT3 = np.array([0, 0, 1])

    res = voronoi.bisector_line_equation(p1, p2, p3)

    check_values(res, GT3, "bisector_line_equation")


def test_bisector_plane():
    p1 = np.array([1, 1, 1])
    p2 = np.array([0, 0, 0])

    # a, b, c, d
    GT = np.array([1, 1, 1, 1.5])

    res = voronoi.bisector_plane(p1, p2)

    check_values(res, GT, "bisector_plane")


def test_closest_point_on_a_line():
    l = np.array([1, 0, 0])
    p = np.array([0.5, 0.5, 1])
    o = np.array([0., 0., 0])
    GT = np.array([0.5, 0.0, 0.0])

    res = voronoi.closest_point_on_a_line(p, [l, o])

    check_values(res, GT, "closest_point_on_a_line")


def main():
    # test_closest_point_on_a_line()
    # test_bisector_plane()
    # test_bisector_line_equation()
    # test_eval_structure()
    test_eval_structure_random_seed()


if __name__ == '__main__':
    main()
