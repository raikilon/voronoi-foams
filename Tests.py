import numpy as np
import Voronoi as voronoi
import DebugPlot as dplot
import DataGeneration as dgen
from utils import visualize_cell
from subdivision import GatherSeeds
from joblib import Parallel, delayed
import multiprocessing
import pymesh
from utils import save_cube_union
from utils import save_list_cube


def CheckValues(res, GT, func):
    if (res == GT).all():
        print("testing {} passed. res and GT are {}".format(func, res))
    else:
        print("testing {} failed. res is {}, GT is {}".format(func, res, GT))


def TestGenData():
    rho = 1
    tau = 0.05

    size = 1
    resolution = 100

    seeds = dgen.CreateHoneycomd3D(size, 5)

    dplot.Plot3D(seeds)


def TestEvalStructure():
    rho = 1
    tau = 0.05

    beam_points = []
    size = 1
    resolution = 20

    seeds = dgen.GenerateRandom(size, 3)
    qs = dgen.CreateGrid3D(size, resolution)

    for i in range(len(qs)):
        q = qs[i]

        # re-arrange order, first is the nearest seed to q
        nearest_id = dgen.FindNearestSeed(seeds, q)
        nearest_seed = seeds.pop(nearest_id)
        seeds.insert(0, nearest_seed)

        bl_list = []
        isBeam = voronoi.EvalStructure(rho, tau, q, seeds, bl_list)
        if isBeam:
            beam_points.append(q)
            print("beam point :  {}".format(q))
    # dplot.PlotBL(bl_list, seeds, q)

    dplot.Plot3DAll(seeds, beam_points)


def TestEvalStructureRandomSeed():
    rho = 8
    tau = 0.05
    voxel_centers = np.load("models/cube_voxels.npy")
    # size = voxel_centers[0] - voxel_centers[1]
    seeds = GatherSeeds(rho, np.array([0, 0, 0]))
    # beam_points = []
    num_cores = multiprocessing.cpu_count()

    beam_points = Parallel(n_jobs=num_cores)(delayed(compute_q)(i, rho, tau) for i in voxel_centers)
    beam_points = list(filter(any, beam_points))

    save_list_cube(seeds, tau, "final_seeds")
    save_list_cube(beam_points, tau, "final_voxels")

    visualize_cell(seeds, beam_points)


def compute_q(q, rho, tau):
    isBeam = voronoi.EvalStructure(rho, tau, q, None, [])
    if isBeam:
        # print("beam point :  {}".format(q))
        return q
    else:
        return [None, None, None]


def TestBisectorLineEquation():
    p1 = np.array([2, 0, 0])
    p2 = np.array([0, 0, 0])
    GT1 = np.array([1, 0, 0, 0])

    bp1 = voronoi.BisectorPlane(p1, p2)
    # CheckValues(bp1, GT1, "BisectorPlane")

    p3 = np.array([0, 2, 0])
    GT2 = np.array([0, 1, 0, 0])

    bp2 = voronoi.BisectorPlane(p2, p3)
    # CheckValues(bp2, GT2, "BisectorPlane")

    # a, b, c
    GT3 = np.array([0, 0, 1])

    res = voronoi.BisectorLineEquation(p1, p2, p3)

    CheckValues(res, GT3, "BisectorLineEquation")


def TestBisectorPlane():
    p1 = np.array([1, 1, 1])
    p2 = np.array([0, 0, 0])

    # a, b, c, d
    GT = np.array([1, 1, 1, 1.5])

    res = voronoi.BisectorPlane(p1, p2)

    CheckValues(res, GT, "BisectorPlane")


def TestClosestPointOnALine():
    l = np.array([1, 0, 0])
    p = np.array([0.5, 0.5, 1])
    o = np.array([0., 0., 0])
    GT = np.array([0.5, 0.0, 0.0])

    res = voronoi.ClosestPointOnALine(p, [l, o])

    CheckValues(res, GT, "ClosestPointOnALine")


def main():
    # TestClosestPointOnALine()
    # TestBisectorPlane()
    # TestBisectorLineEquation()
    # TestEvalStructure()
    TestEvalStructureRandomSeed()


# estGenData()


if __name__ == '__main__':
    main()
