import csv

N = 5

threshold = 60*10

def generatemodel(n):
	reader = csv.reader(file('/Users/floliu/Codes/HttpPrediction/data/session/%d.csv' % threshold,'rb'))
	
	TABLE = {}
	HASH  = {}
	MAX = {}

	for session in reader:
		urls = [t.split(";")[1] for t in session]
		for j in range(0,len(session)-1):
			if (len(session)-j) > n:
				P = ",".join(urls[j:j+n])
				C = urls[j+n]
				if TABLE.has_key((P,C)):
					TABLE[(P,C)] = TABLE[(P,C)] + 1
				else :
					TABLE[(P,C)] = 1
				if MAX.has_key(P):
					if TABLE[(P,C)] > MAX[P]:
						MAX[P] = TABLE[(P,C)]
						HASH[P] = C
				else:
					MAX[P] = TABLE[(P,C)]
					HASH[P] = C

	return HASH

def predict(seq,H,n):
	while (len(seq) >= n):
		key = ",".join(seq)
		if H[len(seq)].has_key(key):
			return(H[len(seq)][key])
		seq = seq[1:]
	return "NO PREDICTION"

H = {}
for i in range(1,N):
	H[i] = generatemodel(i)

T = 0
F = 0
reader = csv.reader(file('/Users/floliu/Codes/HttpPrediction/data/test_session/%d.csv' % threshold,'rb'))

for session in reader:
	urls = [t.split(";")[1] for t in session]
	if len(urls) > N:
		urls = urls[0:N]
	pred = predict(urls[:-1],H,1)
	if (predict(urls[:-1],H,1) == urls[-1]):
		T = T +1
	else :
		F = F + 1

print T,F,float(T)/(T+F)









