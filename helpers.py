from math import sqrt

def distance(point, point2):
	x_sq = pow(point2[0] - point[0], 2)
	y_sq = pow(point2[1] - point[1], 2)

	distance = sqrt(abs(x_sq + y_sq))
	return distance