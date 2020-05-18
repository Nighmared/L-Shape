import showit

dir = 0

def tileup(tileval=0):
	VALS = (5,10,15,20,25,30,35)
	if tileval==VALS[-1] or tileval==0:
		tileval=VALS[0]
	else:
		tileval=VALS[VALS.index(tileval)+1]
	return tileval
tileval = tileup()
def fillist(n,c=0):
		ret = []
		for x in range(0,n):
			if type(c)==list:ret.append(c.copy())
			else: ret.append(c)
		return ret

class matrix(list):
	def __init__(self,m,n=0,c=0,mother=0,motherkey=0):
		self.mother = self.motherkey = 0
		if n==0:n=m
		if c==0:c=fillist(n)
		if mother!=0:
			self.mother = mother
			self.motherkey = motherkey
		self.m = m
		self.n = n
		self.id = fillist(m,c)
	def __str__(self):
		ret = ""
		for x in self.id:
			ret+="|"
			for y in x:
				ret += " "+str(y)+" "
			ret+="|\n"
		return ret
	def __getitem__(self,key):
		try:return matrix(1,c=self.id[key],mother=self,motherkey=key)
		except IndexError:
			return self.id[0][key]
	def __setitem__(self,key,value):
		if self.mother !=0:
			self.mother.id[self.motherkey][key] = value
		else:
			self.id[key] = value
	def __len__(self):
		return self.m*self.n

def filldict(n,s,thedict={}):
	thedict[s] = []
	for i in range(0,n,s):
		for j in range(0,n,s):
			thedict[s].append((i,j))
	if s==2:
		return thedict
	else:
		return filldict(n,int(s/2),thedict)



def search(x,y,targets,s): #finds the s*s (sub)square that contains a point (x,y)
	needya = False #kinda blackbox... but does what it should
	breakit = False
	finishit = False

	for i in targets:
		gotchas = []
		for k in range(0,s):
			for j in range(0,s):
				gotchas.append((i[0]+j,i[1]+k))
		for k in gotchas:
			if (x,y)==k:
				finishit = True
		if finishit:needya = gotchas
		if needya:
			break
	return(needya)

def center(point,s): #gives the 4 center point coordinates of a s sized square that has its upper left edge at point
	manip = int(s/2)
	centerpoints = [
		(point[0]+manip-1,point[1]+manip-1),
		(point[0]+manip,point[1]+manip-1),
		(point[0]+manip-1,point[1]+manip),
		(point[0]+manip,point[1]+manip)		
		]
	return centerpoints

def colourize(points,mat):
	global dir
	cols = [1,25,50,75]
	changes = (
		(0,1),
		(0,-1),
		(1,0),
		(-1,0),
	)


	if(len(points)!= 3):
		raise ValueError("False len of input")
	surround = []
	for (x,y) in points:
		for (a,b) in changes:
			new = (x+a,y+b)
			if new not in surround: surround.append(new)
	for (x,y) in surround:
		try:
			colFound = mat.id[x][y]
			if colFound in cols: cols.remove(colFound)
		except IndexError:
			continue	
	toColor = cols[0+dir]
	dir = 0 if dir <0 else -1 #more change between the selected color 
	for (x,y) in points:
		mat[x][y] = toColor

 #TODO add method for coloring that takes coords of the three fields that should be colored
def fillit(squaredict,coords,mat,n,statelist): 
	global tileval
	if n==2:
		needya =search(coords[0],coords[1],squaredict[n],n)
		therest = needya.copy()
		therest.remove((coords[0],coords[1]))
		#for i in therest:
		#	mat[i[0]][i[1]] = tileval #FIXME coloring #therest contains coords of 3 fields :check
		colourize(therest,mat) #CHANGED
		statelist.addstate(mat.id)
		tileval=tileup(tileval)
	else:
		mat = (fillit(squaredict,coords,mat,int(n/2),statelist))
		thepoint = search(coords[0],coords[1],squaredict[n],n)
		ctp = center(thepoint[0],n)
		for i in ctp:
			if(mat[i[0]][i[1]]) !=0:ctp.remove(i)
		buoys = []
		if len(ctp)>3:
			raise ValueError
		for i in ctp: #ctp = centerpoints
			buoys.append(search(i[0],i[1],squaredict[int(n/2)],int(n/2)))
			#mat[i[0]][i[1]] = tileval #color the three centerpoints FIXME coloring #ctp contains coords of 3 fields :check
		colourize(ctp,mat)
		statelist.addstate(mat.id)
		tileval=tileup(tileval)
		therealG = []
		for i in buoys:
			for j in i:
				if(mat.id[j[0]][j[1]] !=0):
					therealG.append(j)
		for i in therealG:
			mat = fillit(squaredict,i,mat,int(n/2),statelist)
	return (mat)


def doit(n,y,x):
	global tileval
	coords = (x,y)
	mat = matrix(n) #generates empty (filled with 0) matrix, if only one var is give the matrix will be quadratic
	mat[x][y] = 200
	states = showit.statelist()
	states.addstate(mat.id)
	squaredict = filldict(n,n) #dict with beginning coords (upper left) for every possible 2^k with k<=n square that fits inside nxn field, keys are 2^k
	mat = fillit(squaredict,coords,mat,n,states)
	#print(mat)
	showit.animo(states.states)
n = int(input("give the dimensions (must be a power of 2): \n"))
x = int(input("give an x coordinate, must be an integer and positive: \n"))
y = int(input("give an y coordinate, must be an integer and positive: \n"))
doit(n,x,y)