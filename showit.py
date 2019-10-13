import matplotlib.pyplot as plt
import matplotlib.animation as anim
#import numpy as np
#a = np.random.random((16,16))
CMAP = "viridis"

class statelist():
	def __init__(self):
		self.states = []

	def addstate(self,state):
		global CMAP
		self.states.append([plt.imshow(state,cmap=CMAP,interpolation="nearest",animated=True)])

def animo(statelist):
	fig = plt.figure()
	an = anim.ArtistAnimation(fig,statelist,interval=200,blit=True,repeat=False)
	#ani.save('l-shape.mp4')
	plt.show()