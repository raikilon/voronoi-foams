
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as lines
import open3d as o3d
from mpl_toolkits.mplot3d import Axes3D


def visualize_cloud(points):
    """

    :param points: np array of points [[x,y,z],[x,y,z]]
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.paint_uniform_color([0, 0, 1])
    o3d.visualization.draw_geometries([pcd])


def Plot3D(seeds):

	#bx, by = Convert3Dto2D(beam_points)
	sx, sy, sz = Convert3Dto3D(seeds)

	ax = plt.axes(projection='3d')

	ax.scatter3D(sx, sy, sz)
	plt.show()


def Plot3DAll(seeds, beam_points):

	bx, by, bz = Convert3Dto3D(beam_points)
	sx, sy, sz = Convert3Dto3D(seeds)

	ax = plt.axes(projection='3d')

	ax.scatter3D(sx, sy, sz, c='r')
	ax.scatter3D(bx, by, bz, c='k')
	plt.show()

def LinesToRange(bl_list):

	for i in range(len(bl_list)):
		l = bl_list[i][0]
		l2 = bl_list[i][1]


def PlotBL(bl_list, seeds, q):

	sx, sy, sz = Convert3Dto3D(seeds)
	#bx, by, bz = Convert3Dto3D(beam_points)

	ax = plt.axes(projection='3d')

	lx = []
	ly = []
	lz = []

	for i in range(len(bl_list)):
		l = bl_list[i][0]
		l2 = bl_list[i][1]
		lx.append(l[0])
		ly.append(l[1])
		lz.append(l[2])
		lx.append(l2[0])
		ly.append(l2[1])
		lz.append(l2[2])

	ax.plot3D(lx, ly, lz, c='b')
	ax.scatter3D(sx, sy, sz, c='r')
	ax.scatter3D(q[0], q[1], q[2], c='k')
	plt.show()



def Convert3Dto3D(points3D):

	points3Dx = []
	points3Dy = []
	points3Dz = []

	for i in range(len(points3D)):
		p = points3D[i]
		points3Dx.append(p[0])
		points3Dy.append(p[1])
		points3Dz.append(p[2])

	return points3Dx, points3Dy, points3Dz



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
	plt.savefig("debug.png")
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