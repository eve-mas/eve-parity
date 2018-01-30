import sys,itertools,math

def main(argv=None):
	f = open('gifford','w')	
#	f.write(str(sys.argv[1]))
	n = int(sys.argv[1])+1
	maj = int(math.ceil(float(n)/2))
	print 'maj',maj
	for x in xrange (1,n):
		#f.write(str(sys.argv[1]))
		f.write('module RM'+str(x)+' controls v'+str(x))
		f.write('\ninit\n')
		f.write(":: true ~> v"+str(x)+"':= false;\n")
		f.write('update\n')
		f.write(":: s"+str(x)+" ~> v"+str(x)+"':= true;\n")
		f.write(":: !s"+str(x)+" ~> v"+str(x)+"':= true;\n")
		f.write(":: !s"+str(x)+" ~> v"+str(x)+"':= false;\n")
		f.write('goal\n')
		f.write(':: (G F (s'+str(x)+' and X s0));') 
		f.write('\n\n')

	f.write('module environment controls ')
	for x in range(1,n):
		f.write('s'+str(x)+',')
	f.write("s0\n")
	f.write('init\n')
	f.write(":: true ~> ")
	for x in range(1,n):
		f.write("s"+str(x)+"':=false,")
	f.write("s0':=true;\n")
	f.write('update\n')
	f.write(":: s0 ~> ")
	for x in range(1,n):
		if x==1:
			f.write("s"+str(x)+"':=true,")
		else:
			f.write("s"+str(x)+"':=false,")			
	f.write("s0':=false;\n")

	f.write(":: (")
	for x in range(1,n-1):
		if x!=1:
			f.write(" or s"+str(x))
		else:
			f.write(" s"+str(x))
	f.write(") and (")
	for idx,tup in enumerate(list(itertools.combinations(range(1,n),maj))):
		if idx!=0:
			f.write(") or ")
		for i in range(0,maj):
			if i!=0:
				f.write(" and v"+str(tup[i]))
			else:
				f.write("( v"+str(tup[i]))
	f.write(" )) ~> ")
	for x in range(1,n):
		f.write("s"+str(x)+"':=false,")			
	f.write("s0':=true;")

	for x in range(1,n):
		if x==n-1:
			f.write("\n:: s"+str(x))
		else:			
			f.write("\n:: s"+str(x)+" and !(")
			for idx,tup in enumerate(list(itertools.combinations(range(1,n),maj))):
				if idx!=0:
					f.write(") or ")
				for i in range(0,maj):
					if i!=0:
						f.write(" and v"+str(tup[i]))
					else:
						f.write("( v"+str(tup[i]))
			f.write(")) ")
		f.write("~> ")
		for y in range(1,n):
			if y==x+1:
				f.write("s"+str(y)+"':=true,")
			else:
				f.write("s"+str(y)+"':=false,")	
		if x==n-1:
			f.write("s0':=true;")
		else:		
			f.write("s0':=false;")	
	
	f.write("\nproperty\n")
	f.write(":: G F (s0);")
if __name__ == '__main__':
    main()
