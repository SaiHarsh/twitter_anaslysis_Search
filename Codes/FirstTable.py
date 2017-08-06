from Functions import *          
import os
# direc = ''
# direc = '/home/saiharsh/Documents/twitter_anaslysis_Search/10_Oct_2016/' 
# ext = '.csv'
# input_files = [i for i in os.listdir(direc) if os.path.splitext(i)[1] == ext]
# #input_files = ['../01_Abu_Dubai_2016/1491174995_2016-02-23_tweets.csv','../02_Feb_2016/1490193480_2016-02-23_tweets.csv','../02_Feb_2016/1490194265_2016-02-24_tweets.csv']

# Master_Table = pd.DataFrame()
# for i in input_files:
# 	Tmp_Table = pd.DataFrame()
# 	address = direc + i
# 	df = pd.read_csv(address,sep=',',error_bad_lines=False)
# 	###### This will remove all the Rows in which atleast one column value is NAN ::: The Column Name's are defined ###################
# 	df = df.dropna(subset=['TweetId', 'UserName','UserID', 'Link','TweetText' ,'Tweeted Datetime', 'Lat','Long'])
	
# 	Tmp_Table['UserName'] = df['UserName']
# 	Tmp_Table['UserID'] = df['UserID']
# 	Tmp_Table['Datetime'] = df['Tweeted Datetime'].apply(lambda x: UnixFormat(str(x)))
# 	Tmp_Table['ReadableDateTime'] = df['Tweeted Datetime'].apply(lambda x: Check_DateTime(str(x)))
# 	Tmp_Table['hashtag_keywords'] = df.TweetText.apply(lambda x: re.findall('#(?=\w+)\w+',str(x)))
# 	Tmp_Table['nonhashtag'] = df.TweetText.apply(lambda x: formatter(str(x)))
# 	Tmp_Table['mentions'] = df.TweetText.apply(lambda x: re.findall('@(?=\w+)\w+',str(x)))
# 	Tmp_Table['Lat'] = df['Lat'].apply(lambda x: Check_Lat(str(x)))
# 	Tmp_Table['Long'] = df['Long'].apply(lambda x: Check_Lat(str(x)))
# 	Tmp_Table['SourcePlatform'] = df['TweetText'].apply(lambda x: Get_Host_Name(str(x)))
# 	Master_Table = Master_Table.append(Tmp_Table)
# 	Master_Table['nonhashtag'] = Master_Table.nonhashtag.apply(' '.join).str.replace('[^A-Za-z\s]+', '') \
# 	.str.split(expand=False)
# Master_Table.to_csv('Filter_Input_2.csv', index=False)
# count_per_day_hourly_tweets('Filter_Input_2.csv')
# count_per_day_tweets('Filter_Input_2.csv')
# count_weekly_tweets('Filter_Input_2.csv')
# count_per_location('Filter_Input_2.csv')
# count_per_day_hourly_per_location('Filter_Input_2.csv')
# count_per_hour('Filter_Input_2.csv')
# count_per_location_hourly('Filter_Input_2.csv')
# count_platform_location('Filter_Input_2.csv')
# Count_User_Freq('Filter_Input_2.csv')
# Count_user_date_freq('Filter_Input_2.csv')
# user_pair_common_keywords('Filter_Input_2.csv')
# user_pair_common_keywords_time('Filter_Input_2.csv')
# user_pair_common_keywords_location('Filter_Input_2.csv')
# user_pair_common_keywords_same_datetime_location('Filter_Input_2.csv')
# user_pair_common_keywords_freq('Filter_Input_2.csv')
# user_pair_common_keywords_time_freq('Filter_Input_2.csv')
# user_pair_common_keywords_location_freq('Filter_Input_2.csv')
# user_pair_common_keywords_same_datetime_location_freq('Filter_Input_2.csv')
# user_mention_freq('Filter_Input_2.csv')
# user_mention_date_freq('Filter_Input_2.csv')
# user_mention_location_freq('Filter_Input_2.csv')
# user_mention_date_location_freq('Filter_Input_2.csv')
# user_mention_keyword_freq('Filter_Input_2.csv')
# Group_Freq('Filter_Input_2.csv')
# Group_mention_date_location_freq('Filter_Input_2.csv')
# user_mention_keyword_freq_date('Filter_Input_2.csv')
# Slide_11('Filter_Input_2.csv')
# Slide_10('Filter_Input_2.csv')
# user_source_freq('Filter_Input_2.csv')
# user_mention_keyword_freq_date('Filter_Input_2.csv')
# user_source_freq('Filter_Input_2.csv')
# slide_12('Filter_Input_2.csv')
user_location_freq('Filter_Input_2.csv')
