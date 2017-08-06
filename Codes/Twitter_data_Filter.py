import pandas as pd
import re
df_1 = pd.read_csv('Input_1.csv',sep=';',error_bad_lines=False)
df_2 = pd.read_csv('Input_2.csv',error_bad_lines=False)
df_3 = pd.read_csv('Input_3.csv',error_bad_lines=False)

print("########################   INPUT TYPE 1    #######################")
print len(df_1.columns)
print df_1.head(10)

print("########################   INPUT TYPE 2    #######################")
print len(df_2.columns)
print df_2.head(10)


print("########################   INPUT TYPE 3    #######################")
print len(df_3.columns)
print df_3.head(10)


def formatter(st):
    new_str = ' '.join([w for w in st.split() if len(w)>3])
    non_ht = [ w for w in new_str.split() if not(w.startswith("#") or w.startswith('@') or ("RT" in w) or ("https" in w) or ("http" in w))]
    return non_ht

if(len(df_1.columns)==10 and 'mentions' in df_1.columns and 'hashtags' in df_1.columns):
    new_df_1 = pd.DataFrame()
    new_df_1['username'] = df_1['username']
    new_df_1['date'] = df_1['date']
    new_df_1['hashtag_keywords'] = df_1.text.apply(lambda x: re.findall('#(?=\w+)\w+',str(x)))
    new_df_1['nonhashtag'] = df_1.text.apply(lambda x: formatter(str(x)))
    new_df_1['mentions'] = df_1.text.apply(lambda x: re.findall('@(?=\w+)\w+',str(x)))
    new_df_1.to_csv('Filter_Input_1.csv', index=False)

if(len(df_2.columns)==18):
    new_df_1 = pd.DataFrame()
    new_df_1['username'] = df_2['userScreen']
    new_df_1['date'] = df_2['tweetCreated']
    new_df_1['hashtag_keywords'] = df_2.tweetText.apply(lambda x: re.findall('#(?=\w+)\w+',str(x)))
    new_df_1['nonhashtag'] = df_2.tweetText.apply(lambda x: formatter(str(x)))
    new_df_1['mentions'] = df_2.tweetText.apply(lambda x: re.findall('@(?=\w+)\w+',str(x)))
    new_df_1.to_csv('Filter_Input_2.csv', index=False)

if(len(df_3.columns)==14):
    new_df_1 = pd.DataFrame()
    new_df_1['username'] = df_3['ScreenName']
    new_df_1['date'] = df_3['Tweeted Datetime']
    new_df_1['hashtag_keywords'] = df_3.TweetText.apply(lambda x: re.findall('#(?=\w+)\w+',str(x)))
    new_df_1['nonhashtag'] = df_3.TweetText.apply(lambda x: formatter(str(x)))
    new_df_1['mentions'] = df_3.TweetText.apply(lambda x: re.findall('@(?=\w+)\w+',str(x)))
    new_df_1.to_csv('Filter_Input_3.csv', index=False)
