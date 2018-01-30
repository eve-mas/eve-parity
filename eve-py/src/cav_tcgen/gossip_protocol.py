import sys,itertools

def main(argv=None):
	f = open('gossip_protocol','w')	
#	f.write(str(sys.argv[1]))
	n = int(sys.argv[1])+1
	for x in xrange (1,n):
		#f.write(str(sys.argv[1]))
		f.write('module RM'+str(x)+' controls s'+str(x)+'\n')
		f.write('init\n')
		f.write(":: true ~> s"+str(x)+"' := true;\n")
		f.write('update\n')
		f.write(":: s"+str(x)+" ~> s"+str(x)+"' := false;\n")
		f.write(":: s"+str(x)+" ~> s"+str(x)+"' := true;\n")
		f.write(":: !s"+str(x)+" and (")
		pl=range(1,n)
		pl.remove(x)
		for a,b in enumerate(pl):
			if a!=0:
				f.write(" or !s"+str(b))
			else:
				f.write(" !s"+str(b))
		f.write(") ~> s"+str(x)+"' := true;\n")
		f.write('goal\n')
		f.write(':: (G F !s'+str(x)+');') 
		
		#f.write(')));\n\n')
		f.write('\n\n')

if __name__ == '__main__':
    main()
