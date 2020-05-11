
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as lines


def Convert3Dto2D(points3D):

	points2Dx = []
	points2Dy = []

	for i in range(len(points3D)):
		p = points3D[i]
		points2Dx.append(p[0])
		points2Dy.append(p[1])

	return points2Dx, points2Dy

def PlotSeedsAndBeamPoints(beam_points, seeds):


	bx, by = Convert3Dto2D(beam_points)
	sx, sy = Convert3Dto2D(seeds)

	plt.scatter(bx, by, c='k')
	plt.scatter(sx, sy, c='r')
	plt.show()


def PlotBisectors(bl_list, tau):

	fig = plt.figure()

	ls = []

	for i in range(len(bl_list)):
		bl = bl_list[i]
		p1 = bl[0]
		p2 = bl[1]
		l = lines.Line2D(p1[:2], p2[:2], transform=fig.transFigure, figure=fig, linewidth=tau)
		ls.append(l)

	fig.lines.extend(ls)

	plt.show()