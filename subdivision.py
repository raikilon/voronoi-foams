import numpy as np


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
        for delta in np.ndindex(2, 2, 2):
            offset = np.array(delta, dtype=float)
            origin_subsquare = origin_square + offset * length_halfsquare
            SubdivideCell(rho, origin_subsquare, length_halfsquare, seeds)

    return seeds


def __sample_new_point(origin_square, length_halfsquare, subidx):
    dx, dy, dz = subidx % 2, subidx // 2, subidx // 2
    offset = length_halfsquare * np.array([dx, dy, dz], dtype=float)
    random_offset = np.array([np.random.random(), np.random.random(), np.random.random()])
    return origin_square + random_offset * length_halfsquare + offset
