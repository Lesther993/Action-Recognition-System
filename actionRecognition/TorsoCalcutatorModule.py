

def calculateTorso(hipCenterCoord,shoulderCenterCoord):
	x = (hipCenterCoord[0] + shoulderCenterCoord[0])/2
	y = (hipCenterCoord[1] + shoulderCenterCoord[1])/2
	return (x,y)
		