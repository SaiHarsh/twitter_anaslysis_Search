for _ in range (input()) :
	n = input()
	l = 2*n
	s = map(int,raw_input())
	s.sort()
	for i in range ((l/2)+1) :
		j += i + ' '
	for i in range ((l/2)+1,l) :
		j += i + ' '
	print j[len(j)/2]
	print j