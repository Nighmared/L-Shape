import matplotlib.pyplot as plt
import matplotlib.animation as animation

CMAP = "viridis" #Color map used by matplotlib
# possible values include 'viridis', 'plasma', 'inferno', 'magma', 'cividis' 

toDisplay = [] #global variables #FIXME use OOP
im = None

def funcAnim(frame: int):
	'''provided to the animation, updates current state
	of the animation depending on the frame'''
	global im,toDisplay
	im.set_data(toDisplay[frame])
	return [im]

def printprog(currFr:int, totFr:int) -> None:
	print(f"{currFr}/{totFr} Frames saved",end="\r")

def animo(statelist: list, size: int, export=False):
	'''Visualize the matrix states contained in statelist (as lists of lists) by using matplotlib
	
	`export` argument defaults to False and decides if the animation is shown on-screen or saved as gif'''
	global toDisplay
	global im

	stateNum = len(statelist) #set delay between updates of figure depending on amount of states which is relative to the size
	if stateNum > 400:
		interval = 15
	elif stateNum>200:
		interval = 40
	elif stateNum >100:
		interval = 60
	else:
		interval = 80

	fig = plt.gcf() #maybe this and .figure both work but now that its running i aint touching it
	toDisplay = statelist # make global... dumb TODO use OOP
	im = plt.imshow(toDisplay[0],cmap=CMAP) # set initial frame, also initialize im
	anim = animation.FuncAnimation(fig,funcAnim,frames=len(toDisplay),interval = interval, repeat=False, blit=True)
	fig.suptitle(f"L-Shape Animation {size}x{size}")
	if(export):
		if(len(statelist)<100): #change speed of gif depending on amount of states ~ size of matrix
			fps = 3
		elif (len(statelist)<1000):
			fps = 7
		else:
			fps = 30
		writer = animation.ImageMagickFileWriter(fps=fps) #very important when using `writer='imagemagick'` shit doesn't work!!!!!
		anim.save('docs/img/recent.gif',writer=writer,progress_callback=printprog) #needs to have imagemagick installed :)
	else:
		plt.show() #display matplotlib animation
