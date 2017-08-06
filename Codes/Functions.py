#!/usr/bin/python
# -*- coding: latin-1 -*-

import pandas as pd
import re
from urlparse import urlparse
from tld import get_tld
import time
from datetime import datetime, date, timedelta
import statistics

####################### To Get the Host name from the text ###############################
#Example:- "#2015 #2016 #Happyâ€¦ https://www.instagram.com/p/BAAt3Ncl1gD/
#Output:- instagram
##########################################################################################
def Get_Host_Name(text):
	try:
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(text))
		parsed_uri = urlparse(urls[0])
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		tld = get_tld(domain) # Top-Level domain
		plat_name = tld.split('.')
		return str(plat_name[0])
	except:
		return ''
####################### To check weather the input text is in datetime ###############################
previous = "12:00 AM - 01 Jan 2016"
def Check_DateTime(text):
	global previous
	try:
		dt = datetime.strptime(text, "%I:%M %p - %d %b %Y")
		previous = text
		return text
	except:
		return previous

def formatter(st):
    new_str = ' '.join([w for w in st.split() if len(w)>3])
    non_ht = [ w for w in new_str.split() if not(w.startswith("#") or w.startswith('@') or ("RT" in w) or ("https" in w) or ("http" in w))]
    return non_ht 

################## To Convert Human readable datetime to Unix format######################
previous = "12:00 AM - 01 Jan 2016"
def UnixFormat(text):
	global previous
	try:
		dt = datetime.strptime(text, "%I:%M %p - %d %b %Y")
		previous = text
	except:
		dt = datetime.strptime(previous, "%I:%M %p - %d %b %Y")
	#print dt
	unixtime = time.mktime(dt.timetuple())
	return int(unixtime)


previous = "59.93901"
def Check_Lat(text):
	global previous
	try:
		a = float(text)
		previous = text
		return text
	except:
		return previous
# it will increment the time by one hour and return start and end time
def increment_by_hour(dt):
	start = time.mktime(dt.timetuple())
	dt += timedelta(hours=1)
	end = time.mktime(dt.timetuple())
	return start,end

def increment_by_day(dt):
	start = time.mktime(dt.timetuple())
	dt += timedelta(days=1)
	end = time.mktime(dt.timetuple())
	return start,end

def increment_by_week(dt):
	start = time.mktime(dt.timetuple())
	dt += timedelta(days=7)
	end = time.mktime(dt.timetuple())
	return start,end

def count_per_day_hourly_tweets(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False) 
	start_list = []
	end_list = []
	value = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
	while True:
		start_time, end_time = increment_by_hour(dt)
		dt += timedelta(hours=1)
		#print start_time, stop
		if start_time >= stop:
			break 
		start_list.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
		end_list.append(datetime.fromtimestamp(int(end_time)).strftime("%I:%M %p - %d %b %Y"))
		tmp = len(df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)])
		value.append(tmp)
	Table = pd.DataFrame()
	Table['StartTime'] = start_list
	Table['EndTIme'] = end_list
	Table['Count'] = value
	print "Converting into CSV......."
	Table.to_csv('count_per_day_hourly_tweets.csv', index=False)
	print "Success!!! please see count_per_day_hourly_tweets.csv"

def count_per_day_tweets(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False) 
	start_list = []
	end_list = []
	value = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
	while True:
		start_time, end_time = increment_by_day(dt)
		dt += timedelta(days=1)
		#print start_time, stop
		if start_time > stop:
			break 
		start_list.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
		end_list.append(datetime.fromtimestamp(int(end_time)).strftime("%I:%M %p - %d %b %Y"))
		tmp = len(df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)])
		value.append(tmp)
	Table = pd.DataFrame()
	Table['StartTime'] = start_list
	Table['EndTIme'] = end_list
	Table['Count'] = value
	print "Converting into CSV......."
	Table.to_csv('count_per_day_tweets.csv', index=False)
	print "Success!!! please see count_per_day_tweets.csv"

def count_weekly_tweets(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False) 
	start_list = []
	end_list = []
	value = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
	while True:
		start_time, end_time = increment_by_week(dt)
		dt += timedelta(days=7)
		#print start_time, stop
		if start_time >= stop:
			break 
		start_list.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
		end_list.append(datetime.fromtimestamp(int(end_time)).strftime("%I:%M %p - %d %b %Y"))
		tmp = len(df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)])
		value.append(tmp)
	Table = pd.DataFrame()
	Table['StartTime'] = start_list
	Table['EndTIme'] = end_list
	Table['Count'] = value
	print "Converting into CSV......."
	Table.to_csv('count_weekly_tweets.csv', index=False)
	print "Success!!! please see count_weekly_tweets.csv"

def count_per_location(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	Table = pd.DataFrame()
	Table['Lat'] = df['Lat']
	Table['Long'] = df['Long']
	Table['Count'] = 0
	Table = pd.DataFrame(Table.groupby(['Lat','Long']).count(),columns=['Count'])
	print "Converting into CSV......."
	Table.reset_index().to_csv('count_per_location.csv', index=False,header=True,)
	print "Success!!! please see count_per_location.csv"

def count_per_day_hourly_per_location(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False) 
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
	Table = pd.DataFrame()
	while True:
		start_time, end_time = increment_by_hour(dt)
		dt += timedelta(hours=1)
		#print start_time, stop
		if start_time >= stop:
			break 
		tmp = df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)]
		intermediate_Table = pd.DataFrame()
		intermediate_Table['Lat'] = tmp['Lat']
		intermediate_Table['Long'] = tmp['Long']
		intermediate_Table['Count'] = 0
		intermediate_Table = pd.DataFrame(intermediate_Table.groupby(['Lat','Long']).count(),columns=['Count'])
		intermediate_Table = intermediate_Table.reset_index()
		intermediate_Table['StartTime'] = datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y")
		intermediate_Table['EndTime'] = datetime.fromtimestamp(int(end_time)).strftime("%I:%M %p - %d %b %Y")
		Table = pd.concat([Table,intermediate_Table],ignore_index=True)
	Table['Lat'],Table['Long'],Table['Count'],Table['StartTime'],Table['EndTime'] = Table['StartTime'],Table['EndTime'], Table['Lat'],Table['Long'],Table['Count']
	cols = list(Table)
	# Seting the header of the Table .i.e. line no: 174  will swap only the values not the header names.
	cols[0],cols[1],cols[2],cols[3],cols[4] = cols[3], cols[4], cols[0],cols[1],cols[2]
	Table.columns = cols
	print "Converting into CSV......."
	Table.reset_index().to_csv('count_per_day_hourly_per_location.csv', index=False,header=True,)
	print "Success!!! please see count_per_day_hourly_per_location.csv"

def count_per_hour(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False) 
	value = [0 for i in range(0,24)]
	l = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	for i in range(0,24):
		dt += timedelta(hours=1)
		l.append(dt.time())
	for i in df['ReadableDateTime']:
    		dt = datetime.strptime(i, "%I:%M %p - %d %b %Y")
    		tmp = dt.time()
    		for j in range(0,len(l)):
    	    		try:
    	        		if(l[j]<=tmp and l[j+1]>tmp):
    	            			value[j]+=1
    	    		except:
    	        		value[len(value)-1]+=1
    	Table = pd.DataFrame()
    	Table['Hours'] = l
    	Table['Count'] = value
	print "Converting into CSV......."
	Table.reset_index().to_csv('count_per_hour.csv', index=False,header=True,)
	print "Success!!! please see count_per_hour.csv"

def count_per_location_hourly(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	l = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	for i in range(0,24):
		dt += timedelta(hours=1)
		l.append(dt.time())

	Table_list = []

	for i in range(0,24):
	    	Table = pd.DataFrame(columns = list(df))
    		Table_list.append(Table)
	#print df
	for i in range(0,len(df)):                                                        
    		dt = datetime.strptime(df['ReadableDateTime'][i], "%I:%M %p - %d %b %Y")
    		tmp = dt.time()
    		for  j in range(0,len(l)):
    	    		try:
    	        		if(l[j]<=tmp and l[j+1]>tmp):
    	            			Table_list[j].loc[len(Table_list[j])]=df.loc[i]
    	    		except:
    	        		Table_list[len(l)-1].loc[len(Table_list[len(l)-1])]=df.loc[len(l)-1]
   	Table = pd.DataFrame()
   	for i in range(0,24):  
    		intermediate_Table = pd.DataFrame(Table_list[i].groupby(['Lat','Long']).count(),columns=['UserID'])
    		intermediate_Table = intermediate_Table.reset_index()
    		intermediate_Table['Hours'] = l[i]                                            
    		Table = pd.concat([Table,intermediate_Table],ignore_index=True)
    	print "Converting into CSV......."
	Table['Lat'],Table['Long'],Table['UserID'],Table['Hours'] = Table['Hours'],Table['Lat'],Table['Long'],Table['UserID']
	cols = list(Table)
    	cols[0],cols[1],cols[2],cols[3] = cols[3], cols[0],cols[1],cols[2]
	Table.columns = cols
	Table.reset_index().to_csv('count_per_location_hourly.csv', index=False,header=True,)
	
	print "Success!!! please see count_per_location_hourly.csv"

def count_platform_location(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	l = df['SourcePlatform'].unique()
	d = {}
	for i in l:
		Table = pd.DataFrame(columns = list(df))
    		d[i] = Table
    	for i in range(0,len(df)):       
    		d[df['SourcePlatform'][i]].loc[len(d[df['SourcePlatform'][i]])] = df.loc[i]
   		Table = pd.DataFrame()
    		for i in l:
    			intermediate_Table = pd.DataFrame(d[i].groupby(['Lat','Long']).count(),columns=['UserID'])
    			intermediate_Table = intermediate_Table.reset_index()
    			if pd.isnull(i):
    				intermediate_Table['SourcePlatform'] = "Twitter"
    			else:
    				intermediate_Table['SourcePlatform'] = i
    			Table = pd.concat([Table,intermediate_Table],ignore_index=True)
    	#print Table
    	Table['Lat'],Table['Long'],Table['UserID'], Table['SourcePlatform'] = Table['SourcePlatform'], Table['Lat'],Table['Long'],Table['UserID']
    	cols = list(Table)
    	cols[2] = 'Count'
    	cols[0],cols[1],cols[2],cols[3] = cols[3], cols[0],cols[1],cols[2]
    	Table.columns = cols
    	print "Converting into CSV......."
	Table.reset_index().to_csv('count_platform_location.csv', index=False,header=True,)
	print "Success!!! please see count_platform_location.csv"

def user_location_freq(input_file):
	df = pd.read_csv(input_file)
	df['Location'] = df['Lat'].map(str)+' '+df['Long'].map(str)
	Location_List = df['Location'].unique()
	UserName=[]
	UserID=[]
	Lat = []
	Long = []
	Freq = []
	Table = pd.DataFrame()
	for location in Location_List:
		intermediate_Table = df[df['Location'] == location]
    		user = list(intermediate_Table['UserID'])
    		users = set(user)
    		for j in users:
    			UserID.append(j)
    			Freq.append(user.count(j))
    			tmp_Lat,tmp_Long = map(float,location.split())
    			Lat.append(tmp_Lat)
    			Long.append(tmp_Long)
	
	Table['UserID'] = UserID
	Table['Lat'] = Lat
	Table['Long'] = Long
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_location_freq.csv', index=False,header=True,)
	print "Success!!! please see user_location_freq.csv"


def Count_User_Freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	Table = pd.DataFrame()
	Table['UserName'] = df['UserName']
	Table['UserID'] = df['UserID']
	Table['Frequency'] = 0
	Table = pd.DataFrame(Table.groupby(['UserID']).count(),columns=['Frequency'])
	print "Converting into CSV......."
	Table.reset_index().to_csv('Count_User_Freq.csv', index=False,header=True,)
	print "Success!!! please see Count_User_Freq.csv"	

def Count_user_date_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	Table = pd.DataFrame()
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
	while True:
		start_time, end_time = increment_by_day(dt)
		dt += timedelta(days=1)
		#print start_time, stop
		if start_time >= stop:
			break 
		intermediate_Table = df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)]
		intermediate_Table = pd.DataFrame(intermediate_Table.groupby(['UserID']).count(),columns=['Lat'])
		intermediate_Table = intermediate_Table.reset_index()
		intermediate_Table['DateTime'] = datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y")
		Table = pd.concat([Table,intermediate_Table],ignore_index=True)
	Table['DateTime'], Table['Lat'] = Table['Lat'], Table['DateTime']
	cols = list(Table)
	cols[1] = 'Count'
	cols[1],cols[2] = cols[2],cols[1]
	Table.columns = cols
	print "Converting into CSV......."
	Table.reset_index().to_csv('Count_user_date_freq.csv', index=False,header=True,)
	print "Success!!! please see Count_user_date_freq.csv"



def clean_keywords(KeyWords):
	KeyWords = KeyWords.replace('[','') 
	KeyWords = KeyWords.replace(']','') 
	KeyWords = KeyWords.replace('\'','')
	KeyWords = KeyWords.replace(' ','')
	KeyWords = KeyWords.split(',')
	return KeyWords 	

def user_pair_common_keywords(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	Table = pd.DataFrame()
	UserID1=[]
	UserID2=[]
	Common_Pair_Words = []
	Index = df.index
	for i in range(0,len(df)):
		for j in range(i+1, len(df)):
			l1 = df.loc[Index[i]]
			l2 = df.loc[Index[j]]
			headers = ['hashtag_keywords','nonhashtag']
			common_words = []
			for  header in headers:
				KeyWords1 = l1[header]
				KeyWords1 = clean_keywords(KeyWords1)
				KeyWords2 = l2[header]
				KeyWords2 = clean_keywords(KeyWords2)
				if (len(KeyWords1)==1 or len(KeyWords2) ==1 ) and (('' in KeyWords1) or ('' in KeyWords2)):
					pass
				else:
					for word in KeyWords1:
						if word in KeyWords2:
							common_words.append(word)
			if len(common_words):
				for word in common_words:
					UserID1.append(l1['UserID'])
					UserID2.append(l2['UserID'])
					Common_Pair_Words.append(word)
	Table['UserID1'] = UserID1
	Table['UserID2'] = UserID2
	Table['KeyWord'] = Common_Pair_Words
	print "Converting into CSV......."
	Table.to_csv('user_pair_common_keywords.csv', index=False,header=True,)
	print "Success!!! please see user_pair_common_keywords.csv"

def user_pair_common_keywords_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	Table = pd.DataFrame()
	UserID1=[]
	UserID2=[]
	Common_Pair_Words = []
	Freq = []
	Index = df.index
	for i in range(0,len(df)):
		for j in range(i+1, len(df)):
			l1 = df.loc[Index[i]]
			l2 = df.loc[Index[j]]
			headers = ['hashtag_keywords','nonhashtag']
			common_words = []
			for  header in headers:
				KeyWords1 = l1[header]
				KeyWords1 = clean_keywords(KeyWords1)
				KeyWords2 = l2[header]
				KeyWords2 = clean_keywords(KeyWords2)
				if (len(KeyWords1)==1 or len(KeyWords2) ==1 ) and (('' in KeyWords1) or ('' in KeyWords2)):
					pass
				else:
					for word in KeyWords1:
						if word in KeyWords2:
							common_words.append(word)
			if len(common_words):
				words = set(common_words)
				for word in words:
					UserID1.append(l1['UserID'])
					UserID2.append(l2['UserID'])
					Common_Pair_Words.append(word)
					Freq.append(common_words.count(word))
	Table['UserID1'] = UserID1
	Table['UserID2'] = UserID2
	Table['KeyWord'] = Common_Pair_Words
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_pair_common_keywords_freq.csv', index=False,header=True,)
	print "Success!!! please see user_pair_common_keywords_freq.csv"

def user_pair_common_keywords_time(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	Table = pd.DataFrame()
	UserID1=[]
	UserID2=[]
	Common_Pair_Words = []
	Time = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
	while True:
		start_time, end_time = increment_by_day(dt)
		dt += timedelta(days=1)
		#print start_time, stop
		if start_time >= stop:
			break 
		intermediate_Table = df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)]
		Index = intermediate_Table.index
		for i in range(0,len(intermediate_Table)):
			for j in range(i+1, len(intermediate_Table)):
				l1 = intermediate_Table.loc[Index[i]]
				l2 = intermediate_Table.loc[Index[j]]
				headers = ['hashtag_keywords','nonhashtag']
				common_words = []
				for  header in headers:
					KeyWords1 = l1[header]
					KeyWords1 = clean_keywords(KeyWords1)
					KeyWords2 = l2[header]
					KeyWords2 = clean_keywords(KeyWords2)
					if (len(KeyWords1)==1 or len(KeyWords2) ==1 ) and (('' in KeyWords1) or ('' in KeyWords2)):
						pass
					else:
						for word in KeyWords1:
							if word in KeyWords2:
								common_words.append(word)
				if len(common_words):
					for word in common_words:
						UserID1.append(l1['UserID'])
						UserID2.append(l2['UserID'])
						Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
						Common_Pair_Words.append(word)
	Table['UserID1'] = UserID1
	Table['UserID2'] = UserID2
	Table['KeyWord'] = Common_Pair_Words
	Table['DateTime'] = Time
	print "Converting into CSV......."
	Table.to_csv('user_pair_common_keywords_time.csv', index=False,header=True,)
	print "Success!!! please see user_pair_common_keywords_time.csv"


def user_pair_common_keywords_location(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	df['Location'] = df['Lat'].map(str)+' '+df['Long'].map(str)
	Location_List = df['Location'].unique()
	UserID1=[]
	UserID2=[]
	Common_Pair_Words = []
	Lat = []
	Long = []
	Table = pd.DataFrame()
	for location in Location_List:
		intermediate_Table = df[df['Location'] == location]
		Index = intermediate_Table.index
		for i in range(0,len(intermediate_Table)):
			for j in range(i+1, len(intermediate_Table)):
				l1 = intermediate_Table.loc[Index[i]]
				l2 = intermediate_Table.loc[Index[j]]
				headers = ['hashtag_keywords','nonhashtag']
				common_words = []
				for  header in headers:
					KeyWords1 = l1[header]
					KeyWords1 = clean_keywords(KeyWords1)
					KeyWords2 = l2[header]
					KeyWords2 = clean_keywords(KeyWords2)
					if (len(KeyWords1)==1 or len(KeyWords2) ==1 ) and (('' in KeyWords1) or ('' in KeyWords2)):
						pass
					else:
						for word in KeyWords1:
							if word in KeyWords2:
								common_words.append(word)
				if len(common_words):
					for word in common_words:
						UserID1.append(l1['UserID'])
						UserID2.append(l2['UserID'])
						Common_Pair_Words.append(word)
						tmp_Lat,tmp_Long = map(float,location.split())
						Lat.append(tmp_Lat)
						Long.append(tmp_Long)
	Table['UserID1'] = UserID1
	Table['UserID2'] = UserID2
	Table['KeyWord'] = Common_Pair_Words
	Table['Lat'] = Lat
	Table['Long'] = Long
	print "Converting into CSV......."
	Table.to_csv('user_pair_common_keywords_location.csv', index=False,header=True,)
	print "Success!!! please see user_pair_common_keywords_location.csv"	

def user_pair_common_keywords_same_datetime_location(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	df['Location'] = df['Lat'].map(str)+' '+df['Long'].map(str)
	Location_List = df['Location'].unique()
	UserID1=[]
	UserID2=[]
	Common_Pair_Words = []
	Lat = []
	Long = []
	Time = []
	Table = pd.DataFrame()
	for location in Location_List:
		intermediate_Table_With_Location = df[df['Location'] == location]
		df = df.sort('Datetime')
		dt = df['Datetime'].iloc[0]
		dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
		dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
		stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
		while True:
			start_time, end_time = increment_by_day(dt)
			dt += timedelta(days=1)
			#print start_time, stop
			if start_time >= stop:
				break 
			intermediate_Table = intermediate_Table_With_Location[(intermediate_Table_With_Location['Datetime'] >= start_time) & (intermediate_Table_With_Location['Datetime'] < end_time)]
			Index = intermediate_Table.index
			for i in range(0,len(intermediate_Table)):
				for j in range(i+1, len(intermediate_Table)):
					l1 = intermediate_Table.loc[Index[i]]
					l2 = intermediate_Table.loc[Index[j]]
					headers = ['hashtag_keywords','nonhashtag']
					common_words = []
					for  header in headers:
						KeyWords1 = l1[header]
						KeyWords1 = clean_keywords(KeyWords1)
						KeyWords2 = l2[header]
						KeyWords2 = clean_keywords(KeyWords2)
						if (len(KeyWords1)==1 or len(KeyWords2) ==1 ) and (('' in KeyWords1) or ('' in KeyWords2)):
							pass
						else:
							for word in KeyWords1:
								if word in KeyWords2:
									common_words.append(word)
					if len(common_words):
						for word in common_words:
							UserID1.append(l1['UserID'])
							UserID2.append(l2['UserID'])
							Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
							Common_Pair_Words.append(word)
							tmp_Lat,tmp_Long = map(float,location.split())
							Lat.append(tmp_Lat)
							Long.append(tmp_Long)
	Table['UserID1'] = UserID1
	Table['UserID2'] = UserID2
	Table['KeyWord'] = Common_Pair_Words
	Table['DateTime'] = Time
	Table['Lat'] = Lat
	Table['Long'] = Long
	print "Converting into CSV......."
	Table.to_csv('user_pair_common_keywords_same_datetime_location.csv', index=False,header=True,)
	print "Success!!! please see user_pair_common_keywords_same_datetime_location.csv"	

def user_pair_common_keywords_time_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	Table = pd.DataFrame()
	UserID1=[]
	UserID2=[]
	Common_Pair_Words = []
	Time = []
	Freq = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1))
	while True:
		start_time, end_time = increment_by_day(dt)
		dt += timedelta(days=7)
		#print start_time, stop
		if start_time >= stop:
			break 
		intermediate_Table = df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)]
		Index = intermediate_Table.index
		for i in range(0,len(intermediate_Table)):
			for j in range(i+1, len(intermediate_Table)):
				l1 = intermediate_Table.loc[Index[i]]
				l2 = intermediate_Table.loc[Index[j]]
				headers = ['hashtag_keywords','nonhashtag']
				common_words = []
				for  header in headers:
					KeyWords1 = l1[header]
					KeyWords1 = clean_keywords(KeyWords1)
					KeyWords2 = l2[header]
					KeyWords2 = clean_keywords(KeyWords2)
					if (len(KeyWords1)==1 or len(KeyWords2) ==1 ) and (('' in KeyWords1) or ('' in KeyWords2)):
						pass
					else:
						for word in KeyWords1:
							if word in KeyWords2:
								common_words.append(word)
				if len(common_words):
					words = set(common_words)
					for word in words:
						UserID1.append(l1['UserID'])
						UserID2.append(l2['UserID'])
						Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
						Common_Pair_Words.append(word)
						Freq.append(common_words.count(word))
	Table['UserID1'] = UserID1
	Table['UserID2'] = UserID2
	Table['KeyWord'] = Common_Pair_Words
	Table['DateTime'] = Time
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_pair_common_keywords_time_freq.csv', index=False,header=True,)
	print "Success!!! please see user_pair_common_keywords_time_freq.csv"

def user_pair_common_keywords_location_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	df['Location'] = df['Lat'].map(str)+' '+df['Long'].map(str)
	Location_List = df['Location'].unique()
	UserID1=[]
	UserID2=[]
	Common_Pair_Words = []
	Lat = []
	Long = []
	Freq = []
	Table = pd.DataFrame()
	for location in Location_List:
		intermediate_Table = df[df['Location'] == location]
		Index = intermediate_Table.index
		for i in range(0,len(intermediate_Table)):
			for j in range(i+1, len(intermediate_Table)):
				l1 = intermediate_Table.loc[Index[i]]
				l2 = intermediate_Table.loc[Index[j]]
				headers = ['hashtag_keywords','nonhashtag']
				common_words = []
				for  header in headers:
					KeyWords1 = l1[header]
					KeyWords1 = clean_keywords(KeyWords1)
					KeyWords2 = l2[header]
					KeyWords2 = clean_keywords(KeyWords2)
					if (len(KeyWords1)==1 or len(KeyWords2) ==1 ) and (('' in KeyWords1) or ('' in KeyWords2)):
						pass
					else:
						for word in KeyWords1:
							if word in KeyWords2:
								common_words.append(word)
				if len(common_words):
					words = set(common_words)
					for word in words:
						UserID1.append(l1['UserID'])
						UserID2.append(l2['UserID'])
						Common_Pair_Words.append(word)
						Freq.append(common_words.count(word))
						tmp_Lat,tmp_Long = map(float,location.split())
						Lat.append(tmp_Lat)
						Long.append(tmp_Long)
	Table['UserID1'] = UserID1
	Table['UserID2'] = UserID2
	Table['KeyWord'] = Common_Pair_Words
	Table['Lat'] = Lat
	Table['Long'] = Long
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_pair_common_keywords_location_freq.csv', index=False,header=True,)
	print "Success!!! please see user_pair_common_keywords_location_freq.csv"	

def user_pair_common_keywords_same_datetime_location_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	df['Location'] = df['Lat'].map(str)+' '+df['Long'].map(str)
	Location_List = df['Location'].unique()
	UserID1=[]
	UserID2=[]
	Common_Pair_Words = []
	Lat = []
	Long = []
	Time = []
	Freq = []
	Table = pd.DataFrame()
	for location in Location_List:
		intermediate_Table_With_Location = df[df['Location'] == location]
		df = df.sort('Datetime')
		dt = df['Datetime'].iloc[0]
		dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
		dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
		stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
		while True:
			start_time, end_time = increment_by_day(dt)
			dt += timedelta(days=1)
			#print start_time, stop
			if start_time >= stop:
				break 
			intermediate_Table = intermediate_Table_With_Location[(intermediate_Table_With_Location['Datetime'] >= start_time) & (intermediate_Table_With_Location['Datetime'] < end_time)]
			Index = intermediate_Table.index
			for i in range(0,len(intermediate_Table)):
				for j in range(i+1, len(intermediate_Table)):
					l1 = intermediate_Table.loc[Index[i]]
					l2 = intermediate_Table.loc[Index[j]]
					headers = ['hashtag_keywords','nonhashtag']
					common_words = []
					for  header in headers:
						KeyWords1 = l1[header]
						KeyWords1 = clean_keywords(KeyWords1)
						KeyWords2 = l2[header]
						KeyWords2 = clean_keywords(KeyWords2)
						if (len(KeyWords1)==1 or len(KeyWords2) ==1 ) and (('' in KeyWords1) or ('' in KeyWords2)):
							pass
						else:
							for word in KeyWords1:
								if word in KeyWords2:
									common_words.append(word)
					if len(common_words):
						words = set(common_words)
						for word in words:
							UserID1.append(l1['UserID'])
							UserID2.append(l2['UserID'])
							Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
							Common_Pair_Words.append(word)
							Freq.append(common_words.count(word))
							tmp_Lat,tmp_Long = map(float,location.split())
							Lat.append(tmp_Lat)
							Long.append(tmp_Long)
	Table['UserID1'] = UserID1
	Table['UserID2'] = UserID2
	Table['KeyWord'] = Common_Pair_Words
	Table['DateTime'] = Time
	Table['Lat'] = Lat
	Table['Long'] = Long
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_pair_common_keywords_same_datetime_location_freq.csv', index=False,header=True,)
	print "Success!!! please see user_pair_common_keywords_same_datetime_location_freq.csv"	

def user_mention_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	UserName = []
	UserID = []
	mention = []
	Freq = []
	for i in range(0,len(df)):
		tmp_mention = df['mentions'][i]
		tmp_mention = clean_keywords(tmp_mention)
		mentions = set(tmp_mention)
		if (len(mentions)==1) and (('' in mentions)):
			pass
		else:
			for j in mentions:
				UserName.append(df['UserName'][i])
				UserID.append(df['UserID'][i])
				mention.append(j)
				Freq.append(tmp_mention.count(j))
	Table = pd.DataFrame()
	Table['UserName'] = UserName
	Table['UserID'] = UserID
	Table['@mention'] = mention
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_mention_freq.csv', index=False,header=True,)
	print "Success!!! please see user_mention_freq.csv"	

def user_mention_date_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	UserName=[]
	UserID=[]
	Time = []
	Freq = []
	mention = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
	while True:
		start_time, end_time = increment_by_day(dt)
		dt += timedelta(days=1)
		if start_time >= stop:
			break 
		intermediate_Table = df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)]
		index = intermediate_Table.index
		for i in range(0,len(intermediate_Table)):
			tmp_mention = intermediate_Table['mentions'][index[i]]
			tmp_mention = clean_keywords(tmp_mention)
			mentions = set(tmp_mention)
			if (len(mentions)==1) and (('' in mentions)):
				pass
			else:
				for j in mentions:
					UserName.append(intermediate_Table['UserName'][index[i]])
					UserID.append(intermediate_Table['UserID'][index[i]])
					mention.append(j)
					Freq.append(tmp_mention.count(j))
					Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
	Table = pd.DataFrame()
	Table['UserName'] = UserName
	Table['UserID'] = UserID
	Table['@mention'] = mention
	Table['DateTime'] = Time
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_mention_date_freq.csv', index=False,header=True,)
	print "Success!!! please see user_mention_date_freq.csv"	

def user_mention_location_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	df['Location'] = df['Lat'].map(str)+' '+df['Long'].map(str)
	Location_List = df['Location'].unique()
	UserName=[]
	UserID=[]
	mention=[]
	Lat = []
	Long = []
	Freq = []
	Table = pd.DataFrame()
	for location in Location_List:
		intermediate_Table = df[df['Location'] == location]
		Index = intermediate_Table.index
		for i in range(0,len(intermediate_Table)):
			tmp_mention = intermediate_Table['mentions'][Index[i]]
			tmp_mention = clean_keywords(tmp_mention)
			mentions = set(tmp_mention)
			if (len(mentions)==1) and (('' in mentions)):
				pass
			else:
				for j in mentions:
					UserName.append(intermediate_Table['UserName'][Index[i]])
					UserID.append(intermediate_Table['UserID'][Index[i]])
					mention.append(j)
					Freq.append(tmp_mention.count(j))
					tmp_Lat,tmp_Long = map(float,location.split())
					Lat.append(tmp_Lat)
					Long.append(tmp_Long)		
	Table['UserName'] = UserName
	Table['UserID'] = UserID
	Table['@mention'] = mention
	Table['Lat'] = Lat
	Table['Long'] = Long
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_mention_location_freq.csv', index=False,header=True,)
	print "Success!!! please see user_mention_location_freq.csv"

def user_mention_date_location_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	df['Location'] = df['Lat'].map(str)+' '+df['Long'].map(str)
	Location_List = df['Location'].unique()
	UserName=[]
	UserID=[]
	mention=[]
	Lat = []
	Long = []
	Time = []
	Freq = []
	Table = pd.DataFrame()
	for location in Location_List:
		intermediate_Table_With_Location = df[df['Location'] == location]
		df = df.sort('Datetime')
		dt = df['Datetime'].iloc[0]
		dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
		dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
		stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
		while True:
			start_time, end_time = increment_by_day(dt)
			dt += timedelta(days=1)
			#print start_time, stop
			if start_time >= stop:
				break 
			intermediate_Table = intermediate_Table_With_Location[(intermediate_Table_With_Location['Datetime'] >= start_time) & (intermediate_Table_With_Location['Datetime'] < end_time)]
			Index = intermediate_Table.index
			for i in range(0,len(intermediate_Table)):
				tmp_mention = intermediate_Table['mentions'][Index[i]]
				tmp_mention = clean_keywords(tmp_mention)
				mentions = set(tmp_mention)
				if (len(mentions)==1) and (('' in mentions)):
					pass
				else:
					for j in mentions:
						UserName.append(intermediate_Table['UserName'][Index[i]])
						UserID.append(intermediate_Table['UserID'][Index[i]])
						mention.append(j)
						Freq.append(tmp_mention.count(j))
						Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
						tmp_Lat,tmp_Long = map(float,location.split())
						Lat.append(tmp_Lat)
						Long.append(tmp_Long)	
	Table['UserName'] = UserName
	Table['UserID'] = UserID
	Table['@mention'] = mention
	Table['DateTime'] = Time
	Table['Lat'] = Lat
	Table['Long'] = Long
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_mention_date_location_freq.csv', index=False,header=True,)
	print "Success!!! please see user_mention_date_location_freq.csv"	

def user_mention_keyword_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	UserName=[]
	UserID=[]
	Freq = []
	mention=[]
	Keyword = []
	Table = pd.DataFrame()
	Index = df.index
	for i in range(0,len(df)):
		tmp_mention = df['mentions'][Index[i]]
		tmp_mention = clean_keywords(tmp_mention)
		mentions = set(tmp_mention)
		l = df.loc[Index[i]]
		headers = ['hashtag_keywords','nonhashtag']
		common_words = []
		for  header in headers:
			KeyWords1 = l[header]
			KeyWords1 = clean_keywords(KeyWords1)
			if (len(KeyWords1)==1 ) and ('' in KeyWords1):
				pass
			else:
				if (len(mentions)==1) and (('' in mentions)):
					pass
				else:
					KeyWords1_unique = set(KeyWords1)
					for j in mentions:
						for word in KeyWords1_unique:
							UserName.append(df['UserName'][Index[i]])
							UserID.append(df['UserID'][Index[i]])
							Freq.append(KeyWords1.count(word))
							mention.append(j)
							Keyword.append(word)	
	Table['UserName'] = UserName
	Table['UserID'] = UserID
	Table['@mention'] = mention
	Table['KeyWord'] = Keyword
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_mention_keyword_freq.csv', index=False,header=True,)
	print "Success!!! please see user_mention_keyword_freq.csv"

def user_mention_keyword_freq_date(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	UserName=[]
	UserID=[]
	Freq = []
	mention=[]
	Keyword = []
	Time = []
	Table = pd.DataFrame()
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1))
	while True:
		start_time, end_time = increment_by_day(dt)
		dt += timedelta(days=7)
		if start_time >= stop:
			break 
		intermediate_Table = df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)]
		Index = intermediate_Table.index
		for i in range(0,len(intermediate_Table)):
			tmp_mention = intermediate_Table['mentions'][Index[i]]
			tmp_mention = clean_keywords(tmp_mention)
			mentions = set(tmp_mention)
			l = intermediate_Table.loc[Index[i]]
			headers = ['hashtag_keywords','nonhashtag']
			common_words = []
			for  header in headers:
				KeyWords1 = l[header]
				KeyWords1 = clean_keywords(KeyWords1)
				if (len(KeyWords1)==1 ) and ('' in KeyWords1):
					pass
				else:
					if (len(mentions)==1) and (('' in mentions)):
						pass
					else:
						KeyWords1_unique = set(KeyWords1)
						for j in mentions:
							for word in KeyWords1_unique:
								UserName.append(intermediate_Table['UserName'][Index[i]])
								UserID.append(intermediate_Table['UserID'][Index[i]])
								Freq.append(KeyWords1.count(word))
								mention.append(j)
								Keyword.append(word)	
								Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
	Table['UserName'] = UserName
	Table['UserID'] = UserID
	Table['@mention'] = mention
	Table['DateTime'] = Time
	Table['KeyWord'] = Keyword
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_mention_keyword_freq_date.csv', index=False,header=True,)
	print "Success!!! please see user_mention_keyword_freq_date.csv"		


def Group_Freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	UserID = []
	Freq = []
	Mentions = []
	Used = []
	for i in range(0,len(df)):
		tmp_mention = df['mentions'][i]
		if tmp_mention!='[]' and (tmp_mention not in Used):
			tmp = df[df['mentions']==tmp_mention]
			tmp_UserID_unique = tmp['UserID'].unique()
			tmp_UserID = list(tmp['UserID'])
			for i in tmp_UserID_unique:
				UserID.append(i)
				Mentions.append(tmp_mention)
				Freq.append(tmp_UserID.count(i))
			Used.append(tmp_mention)
	Table = pd.DataFrame()
	Table['UserID'] = UserID
	Table['@mention'] = Mentions
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('Group_Freq.csv', index=False,header=True,)
	print "Success!!! please see Group_Freq.csv"

def Group_mention_date_location_freq(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	df['Location'] = df['Lat'].map(str)+' '+df['Long'].map(str)
	Location_List = df['Location'].unique()
	UserName=[]
	UserID=[]
	mention=[]
	Lat = []
	Long = []
	Time = []
	Freq = []
	Used = []
	Table = pd.DataFrame()
	for location in Location_List:
		intermediate_Table_With_Location = df[df['Location'] == location]
		df = df.sort('Datetime')
		dt = df['Datetime'].iloc[0]
		dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
		dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
		stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
		while True:
			start_time, end_time = increment_by_day(dt)
			dt += timedelta(days=1)
			#print start_time, stop
			if start_time >= stop:
				break 
			intermediate_Table = intermediate_Table_With_Location[(intermediate_Table_With_Location['Datetime'] >= start_time) & (intermediate_Table_With_Location['Datetime'] < end_time)]
			Index = intermediate_Table.index
			for i in range(0,len(intermediate_Table)):
				tmp_mention = intermediate_Table['mentions'][Index[i]]
				if tmp_mention!='[]' and (tmp_mention not in Used):
					tmp = intermediate_Table[intermediate_Table['mentions']==tmp_mention]
					tmp_UserID_unique = tmp['UserID'].unique()
					tmp_UserID = list(tmp['UserID'])
					for ID in tmp_UserID_unique:
						UserID.append(ID)
						mention.append(tmp_mention)
						Freq.append(tmp_UserID.count(ID))
						Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
						tmp_Lat,tmp_Long = map(float,location.split())
						Lat.append(tmp_Lat)
						Long.append(tmp_Long)
					Used.append(tmp_mention)	
	Table['UserID'] = UserID
	Table['@mention'] = mention
	Table['DateTime'] = Time
	Table['Lat'] = Lat
	Table['Long'] = Long
	Table['Frequency'] = Freq
	print "Converting into CSV......."
	Table.to_csv('Group_mention_date_location_freq.csv', index=False,header=True,)
	print "Success!!! please see Group_mention_date_location_freq.csv"	 

def Slide_11(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	mention = ['user_mention_freq.csv','user_mention_keyword_freq.csv' ,'user_mention_location_freq.csv']
	user = ['user_pair_common_keywords_freq.csv','user_pair_common_keywords_location_freq.csv']
	mention_files = []
	user_files = []
	List = []
	UserID_1 = []
	UserID_2 = []
	Edge_Freq = []
	Keyword = []
	Key_Freq = []
	Lat = []
	Long = []
	Geo_Freq = []
	for i in mention:
		mention_files.append(pd.read_csv(i))
	for i in user:
		user_files.append(pd.read_csv(i))
	for j in range(0,len(mention)):
		for i in mention_files[j]['UserID'].apply(str) +' '+mention_files[j]['@mention'].apply(str):
			List.append(i)
	List = set(List) # Find all the unique pairs
	for j in range(0,len(mention)):
		mention_files[j]['List'] = mention_files[j]['UserID'].apply(str) +' '+mention_files[j]['@mention'].apply(str)

	for i in List:
		try:
			tmp_keywords = mention_files[1][mention_files[1]['List'] == i]
			Index = tmp_keywords.index
			

			for j in range(0,len(tmp_keywords)):
				tmp = i.split()
				UserID_1.append(tmp[0])
				UserID_2.append(tmp[1])
				Keyword.append(tmp_keywords['KeyWord'][Index[j]])
				Key_Freq.append(tmp_keywords['Frequency'][Index[j]])
				try:
					match = mention_files[2][mention_files[2]['List'] == i]
					Geo_Freq.append(match['Frequency'][match.index[0]])
					Lat.append(match['Lat'][match.index[0]])
					Long.append(match['Long'][match.index[0]])

				except:
					Geo_Freq.append(0)	
					Lat.append(match['Lat'][match.index[0]])
					Long.append(match['Long'][match.index[0]])

				try:
					match = mention_files[0][mention_files[0]['List'] == i]
					Edge_Freq.append(match['Frequency'][match.index[0]])
				except:
					Edge_Freq.append(0)
		except:
				tmp = i.split()
				UserID_1.append(tmp[0])
				UserID_2.append(tmp[1])
				
				Keyword.append('0')
				Key_Freq.append(0)			
				try:
					match = mention_files[2][mention_files[2]['List'] == i]
					Geo_Freq.append(match['Frequency'][match.index[0]])
					Lat.append(match['Lat'][match.index[0]])
					Long.append(match['Long'][match.index[0]])

				except:
					Geo_Freq.append(0)	
					Lat.append(match['Lat'][match.index[0]])
					Long.append(match['Long'][match.index[0]])

				try:
					match = mention_files[0][mention_files[0]['List'] == i]
					Edge_Freq.append(match['Frequency'][match.index[0]])
				except:
					Edge_Freq.append(0)

	"""For UserID1 + UserID2"""
	List = []
	for j in range(0,len(user)):
		for i in user_files[j]['UserID1'].apply(str) +' '+user_files[j]['UserID2'].apply(str):
			List.append(i)
	List = set(List)
	for j in range(0,len(user)):
		user_files[j]['List'] = user_files[j]['UserID1'].apply(str) +' '+user_files[j]['UserID2'].apply(str)
	
	Table = pd.DataFrame()	
	for i in List:
		try:
			tmp_keywords = user_files[0][user_files[0]['List'] == i]
			Index = tmp_keywords.index
			for j in range(0,len(tmp_keywords)):
				Keyword.append(tmp_keywords['KeyWord'][Index[j]])
				Key_Freq.append(tmp_keywords['Frequency'][Index[j]])
				tmp = i.split()
				UserID_1.append(tmp[0])
				UserID_2.append(tmp[1])
				try:
					match = user_files[1][user_files[1]['List'] == i]
					Geo_Freq.append(match['Frequency'][match.index[0]])
					Lat.append(match['Lat'][match.index[0]])
					Long.append(match['Long'][match.index[0]])
				except:
					Geo_Freq.append(0)
					Lat.append(0)
					Long.append(0)	
				try:
					Edge_Freq.append(len(tmp_keywords))
				except:
					Edge_Freq.append(0)
		except:
				tmp = i.split()
				UserID_1.append(tmp[0])
				UserID_2.append(tmp[1])
				
				Keyword.append('0')
				Key_Freq.append(0)			
				Edge_Freq.append(0)
				try:
					Geo_Freq.append(user_files[2][user_files[2]['List'] == i]['Frequency'])
					Lat.append(match['Lat'][match.index[0]])
					Long.append(match['Long'][match.index[0]])
				except:
					Geo_Freq.append(0)
					Lat.append(0)
					Long.append(0)	

	print len(UserID_1)
	print len(UserID_2)
	print len(Edge_Freq)
	print len(Keyword)
	print len(Key_Freq)
	print len(Lat)
	print len(Long)

	Table['UserID_1'] = UserID_1
	Table['UserID_2'] = UserID_2
	Table['Edge_Freq'] = Edge_Freq
	Table['Keyword'] = Keyword
	Table['Key_Freq'] = Key_Freq
	Table['Lat'] = Lat
	Table['Long'] = Long
	Table['Geo_Freq'] = Geo_Freq
	print "Converting into CSV......."
	Table.to_csv('Slide_11.csv', index=False,header=True,)
	print "Success!!! please see Slide_11.csv"

def Slide_10(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	mention = ['Slide_11.csv','user_mention_date_freq.csv','user_mention_keyword_freq_date.csv']                                      
	user = ['Slide_11.csv','user_pair_common_keywords_time_freq.csv']                                    
	mention_files = []
	user_files = []
	List = []
	UserID_1 = []
	UserID_2 = []
	Edge_Freq = []
	mention_frequency = []
	Keyword = []
	Key_Freq = []
	Week = []
	Num_Weeks = 1
	intermediate_Table = []
	for i in mention:
		mention_files.append(pd.read_csv(i))
	mention_files[0] = mention_files[0][ mention_files[0]['UserID_2'].apply(lambda x: '@' in x)]

	for i in user:
		user_files.append(pd.read_csv(i))

	for j in range(0,len(mention)):
		try:
			for i in mention_files[j]['UserID'].apply(str) +' '+mention_files[j]['@mention'].apply(str):
				List.append(i)
		except:
			for i in mention_files[j]['UserID_1'].apply(str) +' '+mention_files[j]['UserID_2'].apply(str):
				List.append(i)

	
	List = set(List)
	for j in range(0,len(mention)):
		try:
			mention_files[j]['List'] = mention_files[j]['UserID'].apply(str) +' '+mention_files[j]['@mention'].apply(str)
		except:
			mention_files[j]['List'] = mention_files[j]['UserID_1'].apply(str) +' '+mention_files[j]['UserID_2'].apply(str)			

	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1))
	while True:
		start_time, end_time = increment_by_week(dt)
		dt += timedelta(days=7)
		#print start_time, stop
		if start_time >= stop:
			break 
		tmp_Week = 'Week' + str(Num_Weeks)
		Num_Weeks += 1
		intermediate_Table.append(mention_files[1][mention_files[1]['DateTime']==datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y")])
		intermediate_Table.append(mention_files[2][mention_files[2]['DateTime']==datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y")])
		for i in List:
			list_keywords = intermediate_Table[1][intermediate_Table[1]['List']==i]
			for In in range(0,len(list_keywords)):
				Keyword.append(list_keywords['KeyWord'].iloc[In])
				Key_Freq.append(list_keywords['Frequency'].iloc[In])
				Week.append(tmp_Week)
				Edge_Freq.append(mention_files[0][mention_files[0]['List']==i].iloc[0]['Edge_Freq'])
				mention_frequency.append(intermediate_Table[0][intermediate_Table[0]['List']==i].iloc[0]['Frequency'])
				UserID_1.append(mention_files[0][mention_files[0]['List']==i].iloc[0]['UserID_1'])
				UserID_2.append(mention_files[0][mention_files[0]['List']==i].iloc[0]['UserID_2'])
		intermediate_Table = []
	Table1 = pd.DataFrame()	
	Table1['UserID_1'] = UserID_1
	Table1['UserID_2'] = UserID_2
	Table1['Week'] = Week
	Table1['Edge_Freq'] = Edge_Freq
	Table1['mention_frequency'] = mention_frequency	
	Table1['Keyword'] = Keyword
	Table1['Key_Freq'] = Key_Freq

	List = []

	for j in range(1,len(user)):
		try:
			for i in user_files[j]['UserID1'].apply(str) +' '+user_files[j]['UserID2'].apply(str):
				List.append(i)
		except:
			for i in user_files[0]['UserID_1'].apply(str) +' '+user_files[0]['UserID_2'].apply(str):
				List.append(i)

	List = set(List)

	for j in range(0,len(user)):
		try:
			user_files[j]['List'] = user_files[j]['UserID1'].apply(str) +' '+user_files[j]['UserID2'].apply(str)
		except:
			user_files[j]['List'] = user_files[j]['UserID_1'].apply(str) +' '+user_files[j]['UserID_2'].apply(str)			


	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1))
	intermediate_Table = []
	UserID_1 = []
	UserID_2 = []
	Edge_Freq = []
	mention_frequency = []
	Keyword = []
	Key_Freq = []
	Week = []
	Num_Weeks = 1

	Num_Weeks = 1
	Week = []
	while True:
		start_time, end_time = increment_by_week(dt)
		dt += timedelta(days=7)
		#print start_time, stop
		if start_time >= stop:
			break 
		tmp_Week = 'Week' + str(Num_Weeks)
		Num_Weeks += 1
		intermediate_Table.append(user_files[1][user_files[1]['DateTime']==datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y")])
		for i in List:
			list_keywords = intermediate_Table[0][intermediate_Table[0]['List']==i]
			for In in range(0,len(list_keywords)):
				Keyword.append(list_keywords['KeyWord'].iloc[In])
				Key_Freq.append(list_keywords['Frequency'].iloc[In])
				Week.append(tmp_Week)
				Edge_Freq.append(user_files[0][user_files[0]['List']==i].iloc[0]['Edge_Freq'])
				UserID_1.append(user_files[0][user_files[0]['List']==i].iloc[0]['UserID_1'])
				UserID_2.append(user_files[0][user_files[0]['List']==i].iloc[0]['UserID_2'])
		intermediate_Table = []
	Table2 = pd.DataFrame()	

	Table2['UserID_1'] = UserID_1
	Table2['UserID_2'] = UserID_2
	Table2['Week'] = Week
	Table2['Edge_Freq'] = Edge_Freq
	Table2['Keyword'] = Keyword
	Table2['Key_Freq'] = Key_Freq

	List = []
	Table = pd.DataFrame()
	for i in Table1['UserID_1']:
		List.append(i)
	for i in Table2['UserID_1']:
		List.append(i)	
	List = set(List)
	UserID_1 = []
	Ratio_edge = []
	Avg_Keyword = []
	Week = set(Week)
	weeks = []
	for week in Week:
		for i in List:
			tmp = Table1[(Table1['Week']==week) & (Table1['UserID_1']==i)]
			Tmp = Table2[(Table2['Week']==week) & (Table2['UserID_1']==i)]
			try:
				tmp1 = statistics.median(tmp['Key_Freq'])
				tmp2 = statistics.median(Tmp['Key_Freq'])
				tmp1 = len(tmp)
				tmp2 = float(len(Tmp))
				Ratio_edge.append(tmp1/tmp2)
				UserID_1.append(i)
				Avg_Keyword.append(tmp1/tmp2)
				weeks.append(week)
			except:
				pass
	
	print len(UserID_1)
	print len(weeks)
	print len(Ratio_edge)
	print len(Avg_Keyword)

	Table['UserID'] = UserID_1
	Table['Week'] = weeks
	Table['Ratio Edge Frequency'] = Ratio_edge
	Table['Avg Keyword'] = Avg_Keyword
	
	Table.Ratio[(Table['Ratio Edge Frequency'] > 0.0) & (Table['Avg Keyword'] < 0.2)] = 'situational'
	Table.Ratio[(Table['Ratio Edge Frequency'] >= 0.2) & (Table['Avg Keyword'] < 0.4)] = 'event_based'
	Table.Ratio[(Table['Ratio Edge Frequency'] >= 0.4) & (Table['Avg Keyword'] < 0.6)] = 'active'
	Table.Ratio[(Table['Ratio Edge Frequency'] > 0.6) & (Table['Avg Keyword'] > 1.0)] = 'highly active'

	print "Converting into CSV......."
	Table.to_csv('Slide_10.csv', index=False,header=True,)
	print "Success!!! please see Slide_10.csv"


def user_source_freq(input_file):
	df = pd.read_csv(input_file)
	UserID = []
	Freq = []
	source = []
	Tmp = list(df['UserID'].unique())
	for i in Tmp:
    		intermediate_Table = df[df['UserID']==i]
    		tmp = pd.DataFrame(intermediate_Table.groupby(['SourcePlatform']).count(),columns=['UserID'])
    		tmp = tmp.reset_index()
    		for j in range(0,len(tmp)):
			UserID.append(i)
    	    		Freq.append(tmp['UserID'][j])
    	    		source.append(tmp['SourcePlatform'][j])
    	Table = pd.DataFrame()
    	Table['UserID'] = UserID
    	Table['Source'] = source
    	Table['Freq'] = Freq
	print "Converting into CSV......."
	Table.to_csv('user_source_freq.csv', index=False,header=True,)
	print "Success!!! please see user_source_freq.csv"   

def user_mention_keyword_freq_date(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	UserName=[]
	UserID=[]
	Freq = []
	mention=[]
	Keyword = []
	Table = pd.DataFrame()
	Time = []
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1)
	while True:
		start_time, end_time = increment_by_day(dt)
		dt += timedelta(days=1)
		#print start_time, stop
		if start_time >= stop:
			break 
		intermediate_Table = df[(df['Datetime'] >= start_time) & (df['Datetime'] < end_time)]
		for i in range(0,len(intermediate_Table)):
			tmp_mention = intermediate_Table['mentions'].iloc[i]
			tmp_mention = clean_keywords(tmp_mention)
			mentions = set(tmp_mention)
			l = intermediate_Table.iloc[i]
			headers = ['hashtag_keywords','nonhashtag']
			common_words = []
			for  header in headers:
				KeyWords1 = l[header]
				KeyWords1 = clean_keywords(KeyWords1)
				if (len(KeyWords1)==1 ) and ('' in KeyWords1):
					pass
				else:
					if (len(mentions)==1) and (('' in mentions)):
						pass
					else:
						KeyWords1_unique = set(KeyWords1)
						for j in mentions:
							for word in KeyWords1_unique:
								UserName.append(intermediate_Table['UserName'].iloc[i])
								UserID.append(intermediate_Table['UserID'].iloc[i])
								Freq.append(KeyWords1.count(word))
								mention.append(j)
								Keyword.append(word)
								Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
	Table['UserName'] = UserName
	Table['UserID'] = UserID
	Table['@mention'] = mention
	Table['KeyWord'] = Keyword
	Table['Frequency'] = Freq
	Table['Time'] = Time
	print "Converting into CSV......."
	Table.to_csv('user_mention_keyword_freq_date.csv', index=False,header=True,)
	print "Success!!! please see user_mention_keyword_freq_date.csv"

def slide_12(input_file):
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	user = ['user_source_freq.csv','user_pair_common_keywords_time_freq.csv']
	mention = ['user_mention_keyword_freq_date.csv']
	user_files =[]
	mention_files =[]
	UserID1=[]
	UserID2=[]
	Freq = []
	Keyword = []
	Key_Freq = []
	source = []
	source_freq = []
	Table = pd.DataFrame()
	Time = []
	for i in mention:
		mention_files.append(pd.read_csv(i))
	for i in user:
		user_files.append(pd.read_csv(i))
	df = df.sort('Datetime')
	dt = df['Datetime'].iloc[0]
	dt = datetime.fromtimestamp(int(dt)).strftime("%I:%M %p - %d %b %Y")
	dt = datetime.strptime(dt, "%I:%M %p - %d %b %Y")
	stop = df['Datetime'].iloc[len(df)-1] #+ timedelta(days=1))
	while True:
		start_time, end_time = increment_by_day(dt)
		dt += timedelta(days=1)
		#print start_time, stop
		if start_time >= stop:
			break 
		intermediate_Table = user_files[1][(user_files[1]['DateTime'] >= datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y")) & (user_files[1]['DateTime'] < datetime.fromtimestamp(int(end_time)).strftime("%I:%M %p - %d %b %Y"))]
		for i in range(0,len(intermediate_Table)):
			UserID1.append(intermediate_Table['UserID1'].iloc[i])			
			UserID2.append(intermediate_Table['UserID2'].iloc[i])
			Keyword.append(intermediate_Table['KeyWord'].iloc[i])
			Key_Freq.append(intermediate_Table['Frequency'].iloc[i])
			Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
			try:
				source.append(user_files[0][user_files[0]['UserID']==user_files[1]['UserID1'].iloc[i]]['Source'].iloc[0])
				source_freq.append(user_files[0][user_files[0]['UserID']==user_files[1]['UserID1'].iloc[i]]['Freq'].iloc[0])
			except:
				source.append(0)
				source_freq.append(0)	
		intermediate_Table = mention_files[0][(mention_files[0]['Time'] >= datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y")) & (mention_files[0]['Time'] < datetime.fromtimestamp(int(end_time)).strftime("%I:%M %p - %d %b %Y"))]
		for i in range(0,len(intermediate_Table)):
			UserID1.append(intermediate_Table['UserID'].iloc[i])			
			UserID2.append(intermediate_Table['@mention'].iloc[i])
			Keyword.append(intermediate_Table['KeyWord'].iloc[i])
			Key_Freq.append(intermediate_Table['Frequency'].iloc[i])
			Time.append(datetime.fromtimestamp(int(start_time)).strftime("%I:%M %p - %d %b %Y"))
			try:
				source.append(user_files[0][user_files[0]['UserID']==user_files[1]['UserID1'].iloc[i]]['Source'].iloc[0])
				source_freq.append(user_files[0][user_files[0]['UserID']==user_files[1]['UserID1'].iloc[i]]['Freq'].iloc[0])
			except:
				source.append(0)
				source_freq.append(0)	
	Table = pd.DataFrame()
	
	# print len(UserID1)
	# print len(UserID2)
	# print len(Time)
	# print len(Keyword)
	# print len(Key_Freq)
	# print len(source) 
	# print len(source_freq)
	
	Table['UserID1'] = UserID1
	Table['UserID2'] =  UserID2
	Table['Time'] = Time 
	Table['Keyword'] =  Keyword 
	Table['Key_Freq'] = Key_Freq 
	Table['source'] =  source 
	Table['source_freq'] = source_freq 

	print "Converting into CSV......."
	Table.to_csv('slide_12.csv', index=False,header=True,)
	print "Success!!! please see slide_12.csv"

def slide_13(input_file): #The input is slide 11.
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	l = []
	l.append(statistics.median(df['Key_Freq']))
	l.append(statistics.median(df['Edge_Freq']))
	l.append(statistics.median(df['Geo_Freq']))
	x = statistics.median(l)
	l=[]
	for i in range(0,len(df)):
		if df['Key_Freq'].iloc[i] >= x and df['Edge_Freq'].iloc[i] >= x and df['Geo_Freq'].iloc[i] >= x:
			l.append('Strong Trust')
		elif df['Key_Freq'].iloc[i] >= x and df['Edge_Freq'].iloc[i] >= x and x>df['Geo_Freq'].iloc[i]:
			l.append('Common Trust')
		elif x>df['Key_Freq'].iloc[i] and df['Edge_Freq'].iloc[i] >= x and df['Geo_Freq'].iloc[i] >= x:
			l.append('Geographical Trust')
	df['Classification'] = l
	print "Converting into CSV......."
	Table.to_csv('slide_13.csv', index=False,header=True,)
	print "Success!!! please see slide_13.csv"

def slide_14(input_file): # input file is Slide12's output.
	df = pd.read_csv(input_file,sep=',',error_bad_lines=False)
	l = []
	l.append(statistics.median(df['Key_Freq']))
	l.append(statistics.median(df['source_freq']))
	l.append(statistics.median(df['Geo_Freq']))
	x = statistics.median(l)
	l=[]
	for i in range(0,len(df)):
		if df['Key_Freq'].iloc[i] >= x and df['Edge_Freq'].iloc[i] >= x and df['Geo_Freq'].iloc[i] >= x:
			l.append('Strong Trust')
		elif df['Key_Freq'].iloc[i] >= x and df['Edge_Freq'].iloc[i] >= x and x>df['Geo_Freq'].iloc[i]:
			l.append('Common Trust')
		elif x>df['Key_Freq'].iloc[i] and df['Edge_Freq'].iloc[i] >= x and df['Geo_Freq'].iloc[i] >= x:
			l.append('Geographical Trust')
	df['Classification'] = l
	print "Converting into CSV......."
	Table.to_csv('slide_13.csv', index=False,header=True,)
	print "Success!!! please see slide_13.csv"
