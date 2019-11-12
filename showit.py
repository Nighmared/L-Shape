import matplotlib.pyplot as plt
import matplotlib.animation as animation
import imageio
#import numpy as np
#a = np.random.random((16,16))
otherstates = []
CMAP = "viridis"
counter = 0
class statelist():
	def __init__(self):
		self.states = []
		self.otherstates =[]

	def addstate(self,state):
		global counter
		nexto = [plt.imshow(state,cmap=CMAP,interpolation="nearest",animated=True)]
		fname = f"{counter}"
		#plt.savefig(fname,nexto[0])
		counter+=1
		self.states.append(nexto)


def animo(statelist):
	fig = plt.figure()
	anim = animation.ArtistAnimation(fig,statelist,interval=200,blit=True,repeat=False)
	plt.show()	