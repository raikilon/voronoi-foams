import numpy as np

from subdivision import gather_seeds


def closest_point_on_a_line(q, bl):
    """Computes the closeet point between a line and a point in 3D

              Parameters
            ----------
            q : np.array([x,y,z])
                the point q in the paper
            bl: np.array([x,y,z])
                the line bl from the paper
              return : np.array([x,y,z])
                pl of the paper, closest point on the line to q
           """

    # based on https://math.stackexchange.com/questions/1905533/find-perpendicular-distance-from-point-to-line-in-3d

    b = bl[0]
    c = bl[1]

    vbc = c - b
    dbc = vbc / np.linalg.norm(vbc)

    vqb = q - b

    t = np.dot(vqb, dbc)

    pl = b + t * dbc

    return pl


def bisector_plane(N1, N2):
    """Finds bisector plane between two 3D points

              Parameters
            ----------
            N1 : np.array([x,y,z])
                first seed
            N2: np.array([x,y,z])
                second seed
              return : np.array([a,b,c,d])
                coefficients of the bisecting plane
           """

    # like we did in the 3D scanning homework

    normp = N1 - N2
    midp = np.mean([N1, N2], axis=0)

    a = normp[0]
    b = normp[1]
    c = normp[2]

    d = -(a * midp[0] + b * midp[1] + c * midp[2])

    return a, b, c, d


def bisector_line_equation(N0, Ni, Nj):
    """Finds bisector line between two planes

              Parameters
            ----------
            N0 : np.array([x,y,z])
                first seed
            Ni: np.array([x,y,z])
                second seed
            Nj: np.array([x,y,z])
                third seed
              return : np.array([a,b,c,d])
                two points on the line bl
           """

    bp1 = bisector_plane(N0, Ni)
    bp2 = bisector_plane(Ni, Nj)

    # based on   https://stackoverflow.com/questions/48126838/plane-plane-intersection-in-python

    np1 = bp1[:3]
    np2 = bp2[:3]

    cross = np.cross(np1, np2)

    # First edge case, this means the bisecting planes are parallel to each other, so there is no intersection between them
    # This happens when we test 3 seeds that next to each other in a row/col on a regular grid
    if (cross == np.array([0, 0, 0])).all():
        # print("weird case, Seeds: {}, {}, {}".format(N0, Ni, Nj))
        # print("bisecting planes: {}, {}".format(bp1, bp2))
        # print("bisecting line: {}".format(bl))
        return None

    A = np.array([np1, np2, cross])
    d = np.array([-bp1[3], -bp2[3], 0.]).reshape(3, 1)

    # could add np.linalg.det(A) == 0 test to prevent linalg.solve throwing error

    p_inter = np.linalg.solve(A, d).T

    # return unit vector
    cross = cross / np.linalg.norm(cross)

    return p_inter[0], (p_inter + cross)[0]


def eval_structure(rho, tau, q, seeds=None, bl_list=None):
    """Returns 1 if q is in a beam and 0 otherwise

            Parameters
            ----------
            rho: float
                seed density
            tau: float
                beam radius
            q: np.array([x,y,z])
                query point
            seeds, bl_list are used for debug

            returns : {0,1}
           """

    if seeds is None:
        seeds = gather_seeds(rho, q)

    N = len(seeds)
    for i in range(1, N):
        for j in range(i + 1, N):
            bl = bisector_line_equation(seeds[0], seeds[i], seeds[j])
            if bl is None:
                continue

            pl = closest_point_on_a_line(q, bl)
            # d = np.linalg.norm(pl - q)
            # print("distance d:{} from q:{} to pl:{} on line bl:{}".format(d, q, pl, bl))
            # print("For seeds: {}, {}, {}".format(seeds[0], seeds[i], seeds[j]))
            if np.linalg.norm(pl - q) <= tau:
                accept = True
                for k in range(1, N):
                    if np.linalg.norm(seeds[0] - pl) > np.linalg.norm(seeds[k] - pl):
                        accept = False
                        break

                if accept:
                    return 1

    return 0
