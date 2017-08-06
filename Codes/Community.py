import pandas as pd

def community(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False) 
	KeyWords =  df.Keyword.unique()
	Dict = {}
	for i in KeyWords:
		if len(i) > 2:
			Dict[i] = []
	for i in range(0,len(df)):
		try:
		    Dict[df['Keyword'][i]].append([df['UserID1'][i],df['UserID2'][i]])
		except:
		    pass

	for key in Dict:
		print "==================================="
		print key
		print Dict[key]
		print "==================================="
	return Dict

if __name__ == '__main__':
	community('user_pair_common_keywords.csv')