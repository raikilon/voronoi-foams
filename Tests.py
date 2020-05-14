import numpy as np
import Voronoi as voronoi
import DebugPlot as dplot
import DataGeneration as dgen


def CheckValues(res, GT, func):

	if (res==GT).all():
		print("testing {} passed. res and GT are {}".format(func, res))
	else:	
		print("testing {} failed. res is {}, GT is {}".format(func, res, GT))




def TestEvalStructure():

	rho = 1
	tau = 0.05

	beam_points = []
	size = 1
	resolution = 100

	seeds = dgen.CreateHoneycomd2D(size, 4)
	qs = dgen.CreateGrid2D(size, resolution)

	# ideal input - 2 layers  of seeds

	for i in range(resolution**2):
		q = qs[i]

		#re-arrange order, first is the nearest seed to q
		# nearest_id = dgen.FindNearestSeed(seeds, q)
		# nearest_seed = seeds.pop(nearest_id)
		# seeds.insert(0, nearest_seed)

		isBeam = voronoi.EvalStructure(rho, tau, q)
		if isBeam:
			beam_points.append(q)
			print("beam point :  {}".format(q))


	dplot.PlotSeedsAndBeamPoints(beam_points, seeds)


def TestBisectorLineEquation():

	p1 = np.array([2,0,0])
	p2 = np.array([0,0,0])
	GT1 = np.array([1,0,0,0])

	bp1 = voronoi.BisectorPlane(p1,p2)
	#CheckValues(bp1, GT1, "BisectorPlane")

	p3 = np.array([0,2,0])
	GT2 = np.array([0,1,0,0])

	bp2 = voronoi.BisectorPlane(p2,p3)
	#CheckValues(bp2, GT2, "BisectorPlane")

	# a, b, c
	GT3 = np.array([0,0,1])

	res = voronoi.BisectorLineEquation(p1, p2, p3)

	CheckValues(res, GT3, "BisectorLineEquation")


def TestBisectorPlane():
	p1 = np.array([1,1,1])
	p2 = np.array([0,0,0])
	
	# a, b, c, d
	GT = np.array([1,1,1, 1.5])

	res = voronoi.BisectorPlane(p1,p2)

	CheckValues(res, GT, "BisectorPlane")


def TestClosestPointOnALine():
	
	l = np.array([1,0,0])
	p = np.array([0.5,0.5,1])
	o = np.array([0. ,0., 0])
	GT =  np.array([0.5,0.0,0.0])

	res = voronoi.ClosestPointOnALine(p, [l, o])
	
	CheckValues(res, GT, "ClosestPointOnALine")
	

def main():

	#TestClosestPointOnALine()
	#TestBisectorPlane()
	#TestBisectorLineEquation()
	TestEvalStructure()





if __name__ == '__main__':
    main()