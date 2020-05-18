import matplotlib.pyplot as plt
import matplotlib.animation as animation

CMAP = "viridis" # possible values include 'viridis', 'plasma', 'inferno', 'magma', 'cividis' 

toDisplay = []
im = None

def funcAnim(frame):
	global im,toDisplay
	im.set_data(toDisplay[frame])
	return [im]

def printprog(currFr:int,totFr:int):
	print(f"{currFr}/{totFr} Frames saved",end="\r")

def animo(statelist,export=False):
	global toDisplay
	global im

	stateNum = len(statelist)
	if stateNum > 400:
		interval = 15
	elif stateNum>200:
		interval = 40
	elif stateNum >100:
		interval = 60
	else:
		interval = 80

	fig = plt.gcf() #maybe this and .figure both work but now that its running i aint touching it
	toDisplay = statelist
	im = plt.imshow(toDisplay[0],cmap=CMAP)
	anim = animation.FuncAnimation(fig,funcAnim,frames=len(toDisplay),interval = interval, repeat=False, blit=True)
	if(export):
		if(len(statelist<100)):
			fps = 15
		else:
			fps = 40
		writer = animation.ImageMagickFileWriter(fps=fps) #very important !!!!!
		anim.save('docs/img/anim.gif',writer=writer,progress_callback=printprog) #needs to have imagemagick installed :)
	else:
		plt.show()
