SYMBOLLIST = ("-","+","*","%","=")
a = SYMBOLLIST[0]
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
	def __len__(self):
		return self.n*self.m
	def __getitem__(self,key):
		try:return matrix(1,c=self.id[key],mother=self,motherkey=key)
		except IndexError:
			return self.id[0][key]
	def __setitem__(self,key,value):
		if self.mother !=0:
			self.mother.id[self.motherkey][key] = value
		else:
			self.id[key] = value



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
	needya = False
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

def switchy(a):
	global SYMBOLLIST
	if SYMBOLLIST.index(a)>=len(SYMBOLLIST)-1:
		a = SYMBOLLIST[0]
	else:
		a = SYMBOLLIST[SYMBOLLIST.index(a)+1]
	return a

def fillit(squaredict,coords,mat,n): 
	global a
	switchy(a)
	if n==2:
		needya =search(coords[0],coords[1],squaredict[n],n)
		therest = needya.copy()
		therest.remove((coords[0],coords[1]))
		for i in therest:
			mat[i[0]][i[1]] = a
		a = switchy(a)
	else:
		mat = (fillit(squaredict,coords,mat,int(n/2)))
		thepoint = search(coords[0],coords[1],squaredict[n],n)
		ctp = center(thepoint[0],n)
		for i in ctp:
			if(mat[i[0]][i[1]]) !=0:ctp.remove(i)
		buoys = []
		if len(ctp)>3:
			raise ValueError
		for i in ctp:
			buoys.append(search(i[0],i[1],squaredict[int(n/2)],int(n/2)))
			mat[i[0]][i[1]] = a
		a = switchy(a)
		therealG = []
		for i in buoys:
			for j in i:
				if(mat.id[j[0]][j[1]] !=0):
					therealG.append(j)
		for i in therealG:
			mat = fillit(squaredict,i,mat,int(n/2))
	return (mat)


def doit(n,y,x):
	counter = 1
	coords = (x,y)
	mat = matrix(n) #generates empty (filled with 0) matrix, if only one var is give the matrix will be quadratic
	mat[x][y] = "X"
	squaredict = filldict(n,n) #dict with beginning coords (upper left) for every possible 2^k with k<=n square that fits inside nxn field, keys are 2^k
	mat = fillit(squaredict,coords,mat,n)
	print(mat)
n = int(input("give the dimensions (must be a power of 2): \n"))
x = int(input("give an x coordinate, must be an integer and positive: \n"))
y = int(input("give an y coordinate, must be an integer and positive: \n"))
doit(n,x,y)
