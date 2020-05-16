import numpy as np

g = np.mgrid[-2:3, -2:3, -2:3].T.reshape((125, 3))
coarse_level_length = 1


# Noli, your magic goes here
def SubdivideCell(rho, origin_square, length_square, seeds=[]):
    """Returns all seeds in the cell

        Parameters
        ----------
        rho: float
            seed density
        center: np.array([x,y,z])
            center of the cell
        length: float
            cell length
        returns : seed list
       """

    length_halfsquare = 0.5 * length_square
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
                    SubdivideCell(rho, origin_subsquare, length_halfsquare, seeds)
    return seeds


def __sample_new_point(origin_square, length_halfsquare, subidx):
    # np.random.seed(100)
    if subidx == 0:
        dx, dy, dz = [1, 1, 1]
    elif subidx == 1:
        dx, dy, dz = [1, 1, -1]
    elif subidx == 2:
        dx, dy, dz = [1, -1, 1]
    elif subidx == 3:
        dx, dy, dz = [-1, 1, 1]
    elif subidx == 4:
        dx, dy, dz = [-1, -1, 1]
    elif subidx == 5:
        dx, dy, dz = [-1, 1, -1]
    elif subidx == 6:
        dx, dy, dz = [1, -1, -1]
    elif subidx == 7:
        dx, dy, dz = [-1, -1, -1]
    offset = (length_halfsquare / 2) * np.array([dx, dy, dz], dtype=float)
    random_offset = np.array([np.random.random(), np.random.random(), np.random.random()])
    return origin_square + random_offset * (length_halfsquare / 2) + offset


def GridCellEnclosing(q):
    """Finds the coarse grid cell containing q. This grid refers the to seed grid not voxelization!!

        Parameters
        ----------
        q: np.array([x,y,z])
            query point
        coarse_level_length: size of the coarse cell
        returns : Cell
       """
    # center = ((q // coarse_level_length) * coarse_level_length) + coarse_level_length / 2
    center = np.round(q / coarse_level_length) * coarse_level_length

    return center


def TwoRingNeighborhood(cell):
    """Returns all the cells in 2-ring neighborhood of the cell. Possibly 3D shape - diamond

        Parameters
        ----------
        cell: Cell
            a cell in the seed grid
        returns : Cell list
       """
    neighborhood = cell + coarse_level_length * g
    return neighborhood.tolist()


def GatherSeeds(rho, q):
    """Returns all seeds that can influence q

        Parameters
        ----------
        rho: float
            seed density
        q: np.array([x,y,z])
            query point
        returns : seed list
       """
    # np.random.seed(100)
    N = []
    visited = []

    cq = GridCellEnclosing(q)
    closest = np.array([np.inf, np.inf, np.inf])

    neighborhood = TwoRingNeighborhood(cq)

    for cell in neighborhood:
        visited.append(cell)
        seeds = SubdivideCell(rho, cell, coarse_level_length, [])
        N.extend(seeds)
        for s in seeds:
            if (np.linalg.norm(closest - q) > np.linalg.norm(s - q)):
                closest = s

    cs = GridCellEnclosing(closest)
    neighborhood = TwoRingNeighborhood(cs)
    for cell in neighborhood:
        if cell not in visited:
            seeds = SubdivideCell(rho, cell, coarse_level_length, [])
            N.extend(seeds)
    index = [i for i, s in enumerate(N) if s[0] == closest[0] and s[1] == closest[1] and s[2] == closest[2]][0]
    N.insert(0, N.pop(index))
    return N
