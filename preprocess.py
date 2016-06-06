######################Split data into train set and test set########################
# user_id, url, Unix_time
# import csv
# import time
# import datetime

# reader = csv.reader(file('/Users/floliu/Codes/HttpPrediction/data/raw/visit.csv','rb'))
# writer1 = csv.writer(file('/Users/floliu/Codes/HttpPrediction/data/train.csv','wb'))
# writer2 = csv.writer(file('/Users/floliu/Codes/HttpPrediction/data/test.csv','wb'))

# for line in reader:
# 	t = int(time.mktime(datetime.datetime.strptime(line[2],"%Y-%m-%d %H:%M:%S").timetuple()))
# 	if reader.line_num > 247614:
# 		writer2.writerow([line[0],line[1],t])
# 	else :
# 		writer1.writerow([line[0],line[1],t])

#########################Split data into sessions ##################################
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import csv

threshold = 60

def time_diff(x):
	timestamps = x.tolist()
	x = []
	for i in range(0,len(timestamps)-1):
		x.append(timestamps[i+1]-timestamps[i])

	return ",".join(str(e) for e in x)

def to_record(x):
	return str(x['TIMESTAMP'])+";"+x["URL"]

def combine(x):
	records = x.tolist()
	if len(records) == 1:
		return [records]
		#return [1]

	result = []
	tmp = [records[0]]
	succ = int(records[0].split(';')[0])
	for i in range(1,len(records)-1):
		ts = int(records[i].split(';')[0])
		if (ts-succ < threshold):
			tmp.append(records[i])
			succ = ts
		else :
			result.append(tmp)
			tmp = [records[i]]
			succ = ts
	result.append(tmp)

	return result
	#return [len(x) for x in result]

def test(x):
	urls = x.tolist()
	return ";".join(urls)

def test2(x):
	return len(x['URL'].split(';'))

df = pd.read_csv('/Users/floliu/Codes/HttpPrediction/data/test.csv')

########################################################################
# result = df.groupby(df["ID"])["TIMESTAMP"].agg(time_diff)

# str = ""
# for i in result:
# 	if i:
# 		str = str + i + ","
# str = str[0:-1] # remove the last ","
# list = [int(x) for x in str.split(",")]

# df = pd.DataFrame(list,columns=['gap'])

# result = df.groupby([pd.cut(df['gap'],[-1,0,1,10,60,300,3600,7200])]).count()/df.count()
# result.plot(kind='bar')

# plt.show()
########################################################################
# df['RECORD'] = df.apply(to_record,axis = 1)

# df = df.drop("TIMESTAMP",1).drop("URL",1)

# df = df.groupby(df['ID'])["RECORD"].agg(combine)

# data = []
# for i in df:
# 	for x in i:
# 		data.append(x)
# df = pd.DataFrame(data,columns=['length'])

# result = df.groupby([pd.cut(df['length'],np.arange(0,210,10))]).count()/df.count()

# result.plot(kind = 'line')

# plt.title("Session length, split by %ds" % threshold)
# plt.show()
########################################################################
#writer = csv.writer(file('/Users/floliu/Codes/HttpPrediction/data/session/%d.csv' % threshold,'wb'))
f = open('/Users/floliu/Codes/HttpPrediction/data/test_session/%d.csv' % threshold, 'w')
#f = open('/Users/floliu/Codes/HttpPrediction/data/session/%d.csv' % threshold, 'w')
df['RECORD'] = df.apply(to_record,axis = 1)
df = df.drop("TIMESTAMP",1).drop("URL",1)
df = df.groupby(df['ID'])["RECORD"].agg(combine)

for i in df:
	for j in i :
		if len(j) > 1:
			f.write(",".join(j)+"\n")
########################################################################
# data = []
# for i in df:
# 	for x in i:
# 		data.append(x)
# df = pd.DataFrame(data,columns=['length'])

# result = df.groupby([pd.cut(df['length'],np.arange(0,200,10))]).count()/df.count()

# result.plot(kind = 'bar')

# plt.title("Session length, split by 60s")
# plt.show()
########################################################################

# result = df.groupby([df['ID'],df['TIMESTAMP']])['URL'].agg(test).to_frame()

# result['len'] = result.apply(test2,axis = 1)
# result = result[result['len']>1]

# counts = result.groupby('URL').size()

# df2 = pd.DataFrame(counts,columns = ['size'])
# df2 = df2[df2['size']>1]

# df2.to_csv('/Users/floliu/Codes/HttpPrediction/data/test.csv')

