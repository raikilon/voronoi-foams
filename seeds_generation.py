import numpy
import matplotlib.pyplot as plt


def sample_new_point(origin_square, length_halfsquare, subidx):
    dx, dy, dz = subidx % 2, subidx // 2, subidx // 2
    offset = length_halfsquare * numpy.array([dx, dy, dz], dtype=float)
    random_offset = numpy.array([numpy.random.random(), numpy.random.random(), numpy.random.random()])
    return origin_square + random_offset * length_halfsquare + offset


def subdivide_square(origin_square, length_square, seeds, density_func):
    length_halfsquare = 0.5 * length_square
    rho = density_func(origin_square + length_halfsquare)
    target_seeds = (length_square ** 3) * rho
    if target_seeds <= 8:
        # 1st case: the cell is a leaf
        shuffled_idx = numpy.random.permutation(8)
        min_samples = int(numpy.floor(target_seeds))
        proba_last = target_seeds - min_samples
        for i in range(min_samples):
            seeds.append(sample_new_point(origin_square, length_halfsquare, shuffled_idx[i]))
        if numpy.random.random() <= proba_last and min_samples < 8:
            seeds.append(sample_new_point(origin_square, length_halfsquare, shuffled_idx[min_samples]))
    else:
        # 2nd case: recursive call
        for delta in numpy.ndindex(2, 2, 2):
            offset = numpy.array(delta, dtype=float)
            origin_subsquare = origin_square + offset * length_halfsquare
            subdivide_square(origin_subsquare, length_halfsquare, seeds, density_func)


def plot_seeds(seeds, extent):
    seeds_x = [s[0] for s in seeds]
    seeds_y = [s[1] for s in seeds]
    seeds_z = [s[2] for s in seeds]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(seeds_x, seeds_y, seeds_z)
    ax.set_xlim([0, extent[0]])
    ax.set_ylim([0, extent[1]])
    ax.set_zlim([0, extent[2]])
    fig.show()


def generate_seeds(coarse_level_length, extent):
    def density_func(point):
        # grading in x direction
        seed_density_factor = 1000
        return (point[2] / extent[2]) * seed_density_factor  # seeds / mm^2

    numpy.random.seed(1)
    seeds = []
    for origin_x in numpy.arange(0.0, extent[0], coarse_level_length):
        for origin_y in numpy.arange(0.0, extent[1], coarse_level_length):
            for origin_z in numpy.arange(0.0, extent[2], coarse_level_length):
                origin_square_coarse = numpy.array([origin_x, origin_y, origin_z], dtype=float)
                subdivide_square(origin_square_coarse, coarse_level_length, seeds, density_func)

    return seeds


if __name__ == "__main__":
    coarse_level_length = 2.0  # (mm)
    extent = numpy.array([8.0, 2.0, 2.0], dtype=float)  # (mm)
    seeds = generate_seeds(coarse_level_length, extent)
    plot_seeds(seeds, extent)
