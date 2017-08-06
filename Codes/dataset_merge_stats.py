import os
import math
from os import listdir
import pandas as pd
from dateutil.parser import parse
from dateutil import parser
import calendar
import re
from urllib.parse import urlparse
import numpy as np
import datetime
from tld import get_tld
import langid

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# This Dictionary stores language codes and their respective meanings
lang_dict = { 
	'ab': 'Abkhaz',
	'aa': 'Afar',
	'af': 'Afrikaans',
	'ak': 'Akan',
	'sq': 'Albanian',
	'am': 'Amharic',
	'ar': 'Arabic',
	'an': 'Aragonese',
	'hy': 'Armenian',
	'as': 'Assamese',
	'av': 'Avaric',
	'ae': 'Avestan',
	'ay': 'Aymara',
	'az': 'Azerbaijani',
	'bm': 'Bambara',
	'ba': 'Bashkir',
	'eu': 'Basque',
	'be': 'Belarusian',
	'bn': 'Bengali',
	'bh': 'Bihari',
	'bi': 'Bislama',
	'bs': 'Bosnian',
	'br': 'Breton',
	'bg': 'Bulgarian',
	'my': 'Burmese',
	'ca': 'Catalan; Valencian',
	'ch': 'Chamorro',
	'ce': 'Chechen',
	'ny': 'Chichewa; Chewa; Nyanja',
	'zh': 'Chinese',
	'cv': 'Chuvash',
	'kw': 'Cornish',
	'co': 'Corsican',
	'cr': 'Cree',
	'hr': 'Croatian',
	'cs': 'Czech',
	'da': 'Danish',
	'dv': 'Divehi; Maldivian;',
	'nl': 'Dutch',
	'dz': 'Dzongkha',
	'en': 'English',
	'eo': 'Esperanto',
	'et': 'Estonian',
	'ee': 'Ewe',
	'fo': 'Faroese',
	'fj': 'Fijian',
	'fi': 'Finnish',
	'fr': 'French',
	'ff': 'Fula',
	'gl': 'Galician',
	'ka': 'Georgian',
	'de': 'German',
	'el': 'Greek, Modern',
	'gn': 'Guaraní',
	'gu': 'Gujarati',
	'ht': 'Haitian',
	'ha': 'Hausa',
	'he': 'Hebrew (modern)',
	'hz': 'Herero',
	'hi': 'Hindi',
	'ho': 'Hiri Motu',
	'hu': 'Hungarian',
	'ia': 'Interlingua',
	'id': 'Indonesian',
	'ie': 'Interlingue',
	'ga': 'Irish',
	'ig': 'Igbo',
	'ik': 'Inupiaq',
	'io': 'Ido',
	'is': 'Icelandic',
	'it': 'Italian',
	'iu': 'Inuktitut',
	'ja': 'Japanese',
	'jv': 'Javanese',
	'kl': 'Kalaallisut',
	'kn': 'Kannada',
	'kr': 'Kanuri',
	'ks': 'Kashmiri',
	'kk': 'Kazakh',
	'km': 'Khmer',
	'ki': 'Kikuyu, Gikuyu',
	'rw': 'Kinyarwanda',
	'ky': 'Kirghiz, Kyrgyz',
	'kv': 'Komi',
	'kg': 'Kongo',
	'ko': 'Korean',
	'ku': 'Kurdish',
	'kj': 'Kwanyama, Kuanyama',
	'la': 'Latin',
	'lb': 'Luxembourgish',
	'lg': 'Luganda',
	'li': 'Limburgish',
	'ln': 'Lingala',
	'lo': 'Lao',
	'lt': 'Lithuanian',
	'lu': 'Luba-Katanga',
	'lv': 'Latvian',
	'gv': 'Manx',
	'mk': 'Macedonian',
	'mg': 'Malagasy',
	'ms': 'Malay',
	'ml': 'Malayalam',
	'mt': 'Maltese',
	'mi': 'Māori',
	'mr': 'Marathi (Marāṭhī)',
	'mh': 'Marshallese',
	'mn': 'Mongolian',
	'na': 'Nauru',
	'nv': 'Navajo, Navaho',
	'nb': 'Norwegian Bokmål',
	'nd': 'North Ndebele',
	'ne': 'Nepali',
	'ng': 'Ndonga',
	'nn': 'Norwegian Nynorsk',
	'no': 'Norwegian',
	'ii': 'Nuosu',
	'nr': 'South Ndebele',
	'oc': 'Occitan',
	'oj': 'Ojibwe, Ojibwa',
	'cu': 'Old Church Slavonic',
	'om': 'Oromo',
	'or': 'Oriya',
	'os': 'Ossetian, Ossetic',
	'pa': 'Panjabi, Punjabi',
	'pi': 'Pāli',
	'fa': 'Persian',
	'pl': 'Polish',
	'ps': 'Pashto, Pushto',
	'pt': 'Portuguese',
	'qu': 'Quechua',
	'rm': 'Romansh',
	'rn': 'Kirundi',
	'ro': 'Romanian, Moldavan',
	'ru': 'Russian',
	'sa': 'Sanskrit (Saṁskṛta)',
	'sc': 'Sardinian',
	'sd': 'Sindhi',
	'se': 'Northern Sami',
	'sm': 'Samoan',
	'sg': 'Sango',
	'sr': 'Serbian',
	'gd': 'Scottish Gaelic',
	'sn': 'Shona',
	'si': 'Sinhala, Sinhalese',
	'sk': 'Slovak',
	'sl': 'Slovene',
	'so': 'Somali',
	'st': 'Southern Sotho',
	'es': 'Spanish; Castilian',
	'su': 'Sundanese',
	'sw': 'Swahili',
	'ss': 'Swati',
	'sv': 'Swedish',
	'ta': 'Tamil',
	'te': 'Telugu',
	'tg': 'Tajik',
	'th': 'Thai',
	'ti': 'Tigrinya',
	'bo': 'Tibetan',
	'tk': 'Turkmen',
	'tl': 'Tagalog',
	'tn': 'Tswana',
	'to': 'Tonga',
	'tr': 'Turkish',
	'ts': 'Tsonga',
	'tt': 'Tatar',
	'tw': 'Twi',
	'ty': 'Tahitian',
	'ug': 'Uighur, Uyghur',
	'uk': 'Ukrainian',
	'ur': 'Urdu',
	'uz': 'Uzbek',
	've': 'Venda',
	'vi': 'Vietnamese',
	'vo': 'Volapük',
	'wa': 'Walloon',
	'cy': 'Welsh',
	'wo': 'Wolof',
	'fy': 'Western Frisian',
	'xh': 'Xhosa',
	'yi': 'Yiddish',
	'yo': 'Yoruba',
	'za': 'Zhuang, Chuang',
	'zu': 'Zulu',
}

# Checks if the date is valid
def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False
        
        
##########################################    Task 1    #########################################    
#################################################################################################
# This function makes appropriate directories for given files of different cities        
#################################################################################################

def make_directories(): # Splitting files into parent and child folders and distribute files in them
    
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Cities\\'))
    if not os.path.exists(os.path.join(APP_ROOT,'dataset_repo\\Cities\\')):
        os.mkdir(os.path.join(APP_ROOT,'dataset_repo\\Cities\\'))
        
    dataset_repo = os.path.join(APP_ROOT,'dataset_repo\\')    
    list_files = listdir(dataset_repo)
    list_files.remove('Cities')
    dir_list = []
    for f in list_files:
        filename = f.split('_')
        if filename[0] not in dir_list:
            dir_list.append(filename[0])
        if not os.path.exists(os.path.join(new_dir,filename[0])):
            os.mkdir(os.path.join(new_dir,filename[0]))
    for f in list_files:
        filename = f.split('_')
        os.rename(os.path.join(APP_ROOT,'dataset_repo\\',f), os.path.join(new_dir,filename[0],f))

        
#################################################################################################
#                 This function merges files from different directories       
#################################################################################################        
        
def merge_files():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Cities\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    folder_list = listdir(old_dir)    
#    for f1 in folder_list:
#        count = 0
#        fout=open(new_dir+"/merged_"+f1+".csv","a",encoding="ISO-8859-1")
#        curr_city_dir = os.path.dirname(os.path.join(old_dir,f1+'\\'))
#        list_curr_city_dir = listdir(curr_city_dir)
#        for fi in list_curr_city_dir:
#            if count == 0:
#                count = 1
#                for line in open(curr_city_dir+"/"+fi,'r',encoding="ISO-8859-1"):
#                    fout.write(line)
#            else:
#                f = open(curr_city_dir+"/"+fi,'r',encoding="ISO-8859-1")
#                next(f) # skip the header
#                for line in f:
#                    fout.write(line)
#                f.close()
#        fout.close() 
    fout=open(new_dir+"/merged_all_csv.csv","a",encoding="ISO-8859-1") 
    count = 0     
    for f1 in folder_list:
        
        curr_city_dir = os.path.dirname(os.path.join(old_dir,f1+'\\'))
        list_curr_city_dir = listdir(curr_city_dir)
        for fi in list_curr_city_dir:
            if count == 0:
                count = 1
                for line in open(curr_city_dir+"/"+fi,'r',encoding="ISO-8859-1"):
                    fout.write(line)
            else:
                f = open(curr_city_dir+"/"+fi,'r',encoding="ISO-8859-1")
                next(f) # skip the header
                for line in f:
                    fout.write(line)
                f.close()
    fout.close() 

    
#####################################    Task 2    ##############################################
#################################################################################################
#   This function counts number of unique latitudes and longitudes amongst different locations       
#################################################################################################
    
def lat_lon_count():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    file_list = listdir(old_dir)
    df = pd.DataFrame()
    df['Latitude'] = ''
    df['Longitude'] = ''
    df['Count'] = ''
    q = 0

    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
   
#    lat = list(df1.Lat.unique())
#    long = list(df1.Long.unique())
    lat_lon = {}

    for index, row in df1.iterrows():
        if not math.isnan(df1['Lat'][index]) and not df1['Lat'][index] == '':
            if (df1['Lat'][index],df1['Long'][index]) not in lat_lon:
                lat_lon[(df1['Lat'][index],df1['Long'][index])] = 1
            else:
                lat_lon[(df1['Lat'][index],df1['Long'][index])] = lat_lon[(df1['Lat'][index],df1['Long'][index])] + 1
    
    for k, v in lat_lon.items():
        df.set_value(q, 'Latitude', k[0])
        df.set_value(q, 'Longitude', k[1])
        df.set_value(q, 'Count', v)
        q = q + 1
    df = df.dropna()
    df.to_csv(new_dir+'\\lat_lon_count.csv', sep=',', index=False)

    
#################################################################################################
#      This function counts number of unique languages in which tweets have been written      
#################################################################################################
    
def detect_languages():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    file_list = listdir(old_dir)
    df = pd.DataFrame()
    df['Language'] = ''
    df['Count'] = ''
    lang = {}
    q = 0
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    tweetText = df1.TweetText
    for t in tweetText:
        x = langid.classify(str(t))
        if lang_dict[x[0]] not in lang:
            lang[lang_dict[x[0]]] = 1
        else:
            lang[lang_dict[x[0]]] = lang[lang_dict[x[0]]] + 1

    for k, v in lang.items():
        df.set_value(q, 'Language', k)
        df.set_value(q, 'Count', v)
        q = q + 1
    
    df.to_csv(new_dir+'\\Language_count.csv', sep=',', index=False)


#################################################################################################
#           This function counts number of tweets on different days of the year       
#################################################################################################    
    
def count_tweets_per_day():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1['Tweeted On']
    df = pd.DataFrame()
    df['Day(Number)'] = ''
    df['Sum count of Tweets'] = ''
    q = 0
    day_number = {}
    check = 0
    year = 0
    for date in df2:
        if is_date(str(date)):
            day = int(parser.parse(str(date)).strftime('%j'))
            if day not in day_number:
                day_number[day] = 1
                if check == 0:
                    check = 1
                    year = int(parser.parse(str(date)).strftime('%y'))
            else:
                day_number[day] = day_number[day] + 1
    
    if calendar.isleap(year):
        for x in range(1,367):
            if x not in day_number:
                day_number[x] = 0
    else:
        for x in range(1,366):
            if x not in day_number:
                day_number[x] = 0
        
    for k, v in day_number.items():
        df.set_value(q, 'Day(Number)', k)
        df.set_value(q, 'Sum count of Tweets', v)
        q = q + 1
    df.sort(['Day(Number)', 'Sum count of Tweets'], ascending=[True, False], inplace=True)  
    df.to_csv(new_dir+'\\day_number_count.csv', sep=',', index=False)


#################################################################################################
#          This function counts number of tweets in different weeks of the year       
#################################################################################################    
    
def count_tweets_per_week():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1['Tweeted On']
    df = pd.DataFrame()
    df['Week(Number)'] = ''
    df['Sum count of Tweets'] = ''
    q = 0
    week_number = {}

    for date in df2:
        if is_date(str(date)):
            week = int(parser.parse(str(date)).strftime('%V'))
            if week not in week_number:
                week_number[week] = 1
            else:
                week_number[week] = week_number[week] + 1

    for x in range(1,53):
            if x not in week_number:
                week_number[x] = 0

    for k, v in week_number.items():
        df.set_value(q, 'Week(Number)', k)
        df.set_value(q, 'Sum count of Tweets', v)
        q = q + 1
    df.sort(['Week(Number)', 'Sum count of Tweets'], ascending=[True, False], inplace=True)  
    df.to_csv(new_dir+'\\week_number_count.csv', sep=',', index=False)


#################################################################################################
#           This function counts number of tweets in different months of the year       
#################################################################################################     
    
def count_tweets_per_month():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1['Tweeted On']
    df = pd.DataFrame()
    df['Month(Name)'] = ''
    df['Sum count of Tweets'] = ''
    q = 0
    month_name = {}
    month_name_all = ['January','February','March','April','May','June','July','August','September','October','November','December']
    
    for x in month_name_all:
            if x not in month_name:
                month_name[x] = 0

    for date in df2:
        if is_date(str(date)):
            month = parser.parse(str(date)).strftime('%B')
            if month_name[month] == 0:
                month_name[month] = 1
            else:
                month_name[month] = month_name[month] + 1

    for m in month_name_all:
        df.set_value(q, 'Month(Name)', m)
        df.set_value(q, 'Sum count of Tweets', month_name[m])
        q = q + 1
    df.to_csv(new_dir+'\\month_name_count.csv', sep=',', index=False)


#################################################################################################
#    This function counts number of tweets on different days of the week throughout the year       
#################################################################################################     
    
def count_tweets_per_day_name():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1['Tweeted On']
    df = pd.DataFrame()
    df['Day of Week(Name)'] = ''
    df['Sum count of Tweets'] = ''
    q = 0
    day_name = {}
    day_name_all = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    for x in day_name_all:
            if x not in day_name:
                day_name[x] = 0

    for date in df2:
        if is_date(str(date)):
            day = parser.parse(str(date)).strftime('%A')
            if day_name[day] == 0:
                day_name[day] = 1
            else:
                day_name[day] = day_name[day] + 1

    for d in day_name_all:
        df.set_value(q, 'Day of Week(Name)', d)
        df.set_value(q, 'Sum count of Tweets', day_name[d])
        q = q + 1
    df.to_csv(new_dir+'\\day_of_week_count.csv', sep=',', index=False)


#################################################################################################
#        This function counts number of tweets with different platform URLs mentions       
#################################################################################################     
    
def find_platform_names():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1['TweetText']
    urls_dict = {}
    urls_list = []
    
    df = pd.DataFrame()
    df['Platform name'] = ''
    df['Sum count of Tweets'] = ''
    q = 0

    for text in df2:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(text))
        for url in urls:
            urls_list.append(url)
    
    for url in urls_list:
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        tld = get_tld(domain) # Top-Level domain
        plat_name = tld.split('.')
        if plat_name[0] not in urls_dict:
            urls_dict[plat_name[0]] = 1
        else:
            urls_dict[plat_name[0]] = urls_dict[plat_name[0]] + 1
                
    for k,v in urls_dict.items():
        df.set_value(q, 'Platform name', k)
        df.set_value(q, 'Sum count of Tweets', v)
        q = q + 1
    df.to_csv(new_dir+'\\platform_count.csv', sep=',', index=False)

    
#####################################    Task 3    ##############################################   
#################################################################################################
#   This function counts number of tweets at different hours of the day throughout the year       
#################################################################################################     
    
def count_hourly_tweets():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1['Tweeted Datetime']
    df = pd.DataFrame()
    df['Hours(24 hrs)'] = ''
    df['Count'] = ''
    q = 0
    
    hour_tweet_count = {}
    for x in range(0,24):
        if x not in hour_tweet_count:
            time_sec = x*60*60
            time_format = datetime.timedelta(seconds=time_sec)
            hour_tweet_count[time_format] = 0

    for x in df2:
        if x != '':
            date_time = str(x).split(' ')
            time = date_time[0].split(':')
            if not np.isnan(float(time[0])):
                time1 = int(float(time[0]))
                if len(date_time)>1:
                    if date_time[1] == 'PM':
                        if time1 == 12:
                            time1 = 0
                        else:
                            time1 = int(time[0]) + 12
                    time_sec = time1*60*60
                    time_format = datetime.timedelta(seconds=time_sec)
                    if hour_tweet_count[time_format] == 0:
                        hour_tweet_count[time_format] = 1
                    else:
                        hour_tweet_count[time_format] = hour_tweet_count[time_format] + 1

    for hr in range(0,24):
        time_sec = hr*60*60
        time_format = datetime.timedelta(seconds=time_sec)
        df.set_value(q, 'Hours(24 hrs)', time_format)
        df.set_value(q, 'Count', hour_tweet_count[time_format])
        q = q + 1    
    df.to_csv(new_dir+'\\hourly_tweet_count.csv', sep=',', index=False)


#################################################################################################
# This function counts number of tweets at different hours of different days throughout the year       
#################################################################################################     
    
def hourly_per_day_count():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)        
    df2 = df1[['Tweeted On','Tweeted Datetime']]

    df = pd.DataFrame()
    df['Hours'] = ''
    df['Day of the week'] = ''
    df['Count'] = ''
    
    q = 0
    day_and_hour = {}
    day_name_all = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    for x in range(0,24):
        for y in day_name_all:
            time_sec = x*60*60
            time_format = datetime.timedelta(seconds=time_sec)
            day_and_hour[(time_format,y)] = 0

    for index, row in df2.iterrows():
        date = row['Tweeted On']
        x = row['Tweeted Datetime']
        if is_date(str(date)):
            day = parser.parse(str(date)).strftime('%A')
            if x != '':
                date_time = str(x).split(' ')
                time = date_time[0].split(':')
                if not np.isnan(float(time[0])):
                    time1 = int(float(time[0]))
                    if len(date_time)>1:
                        if date_time[1] == 'PM':
                            if time1 == 12:
                                time1 = 0
                            else:
                                time1 = int(time[0]) + 12
                        time_sec = time1*60*60
                        time_format = datetime.timedelta(seconds=time_sec)
                        if day_and_hour[(time_format,day)] == 0:
                            day_and_hour[(time_format,day)] = 1
                        else:
                            day_and_hour[(time_format,day)] = day_and_hour[(time_format,day)] + 1
    
    for d in day_name_all:
        for hr in range(0,24):
            time_sec = hr*60*60
            time_format = datetime.timedelta(seconds=time_sec)
            df.set_value(q, 'Hours', time_format)
            df.set_value(q, 'Day of the week', d)
            df.set_value(q, 'Count', day_and_hour[(time_format,d)])
            q = q + 1
    df.to_csv(new_dir+'\\day_and_hour_count.csv', sep=',', index=False)


#################################################################################################
# This function counts number of tweets at different hours of the day throughout the year at different geolocations       
#################################################################################################     
    
def hour_and_geolocation_count():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)        
    df2 = df1[['Tweeted Datetime','Lat','Long']]

    df = pd.DataFrame()
    df['Hours'] = ''
    df['Latitude'] = ''
    df['Longitude'] = ''
    df['Count'] = ''
    
    q = 0
    hour_and_geo = {}

    for index, row in df2.iterrows():
        lat = row['Lat']
        long = row['Long']
        x = row['Tweeted Datetime']
        if x != '':
            date_time = str(x).split(' ')
            time = date_time[0].split(':')
            if not np.isnan(float(time[0])):
                time1 = int(float(time[0]))
                if len(date_time)>1:
                    if date_time[1] == 'PM':
                        if time1 == 12:
                            time1 = 0
                        else:
                            time1 = int(time[0]) + 12
                    time_sec = time1*60*60
                    time_format = datetime.timedelta(seconds=time_sec)
                    if (time_format,lat,long) not in hour_and_geo:
                        hour_and_geo[(time_format,lat,long)] = 1
                    else:
                        hour_and_geo[(time_format,lat,long)] = hour_and_geo[(time_format,lat,long)] + 1
    
    for k,v in hour_and_geo.items():
        df.set_value(q, 'Hours', k[0])
        df.set_value(q, 'Latitude', k[1])
        df.set_value(q, 'Longitude', k[2])
        df.set_value(q, 'Count', v)
        q = q + 1
        
    df.sort(['Latitude','Hours', 'Longitude', 'Count'], ascending=[True,True,False, False], inplace=True)      
    df.to_csv(new_dir+'\\hour_and_geolocation_count.csv', sep=',', index=False)


#################################################################################################
# This function counts number of tweets at different hours of different days throughout the year at different geolocations       
#################################################################################################     

def hour_day_and_geolocation_count():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)        
    df2 = df1[['Tweeted Datetime','Lat','Long','Tweeted On']]

    df = pd.DataFrame()
    df['Hours'] = ''
    df['Day of the Week'] = ''
    df['Latitude'] = ''
    df['Longitude'] = ''
    df['Count'] = ''
    
    q = 0
    hour_day_and_geo = {}

    for index, row in df2.iterrows():
        date = row['Tweeted On']
        lat = row['Lat']
        long = row['Long']
        x = row['Tweeted Datetime']
        if is_date(str(date)):
            day = parser.parse(str(date)).strftime('%A')
            if x != '':
                date_time = str(x).split(' ')
                time = date_time[0].split(':')
                if not np.isnan(float(time[0])):
                    time1 = int(float(time[0]))
                    
                    if len(date_time)>1:
                        if date_time[1] == 'PM':
                            if time1 == 12:
                                time1 = 0
                            else:
                                time1 = int(time[0]) + 12
                        time_sec = time1*60*60
                        time_format = datetime.timedelta(seconds=time_sec)
                        if (time_format,day,lat,long) not in hour_day_and_geo:
                            hour_day_and_geo[(time_format,day,lat,long)] = 1
                        else:
                            hour_day_and_geo[(time_format,day,lat,long)] = hour_day_and_geo[(time_format,day,lat,long)] + 1
    
    for k,v in hour_day_and_geo.items():
        df.set_value(q, 'Hours', k[0])
        df.set_value(q, 'Day of the Week',k[1])
        df.set_value(q, 'Latitude', k[2])
        df.set_value(q, 'Longitude', k[3])
        df.set_value(q, 'Count', v)
        q = q + 1
        
    df.sort(['Latitude','Hours','Day of the Week','Longitude', 'Count'], ascending=[True,True,False,False,False], inplace=True)      
    df.to_csv(new_dir+'\\hour_day_and_geolocation_count.csv', sep=',', index=False)    
    

##########################################    Task 4    ##########################################    

#################################################################################################
# This function finds different geolocations where particular platform has been mentioned in twitted text       
#################################################################################################
    
def platform_lat_long():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1[['TweetText','Lat','Long']]
    
    df = pd.DataFrame()
    df['Platform name'] = ''
    df['Latitude'] = ''
    df['Longitude'] = ''
    
    q = 0

    for index, row in df2.iterrows():
        text = row['TweetText']
        lat_curr = row['Lat']
        long_curr = row['Long']
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(text))
        for url in urls:
            parsed_uri = urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            tld = get_tld(domain) # Top-Level domain
            plat_name = tld.split('.')
            df.set_value(q, 'Platform name', plat_name[0])
            df.set_value(q, 'Latitude', lat_curr)
            df.set_value(q, 'Longitude', long_curr)
            q = q + 1

    df.to_csv(new_dir+'\\platform_lat_long.csv', sep=',', index=False)   

#################################################################################################
# This function finds count of no. of times platform names have been mentioned in twitted text at a particular geolocation       
#################################################################################################
    
def plat_lat_long_count():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1[['TweetText','Lat','Long']]
    
    df = pd.DataFrame()
    df['Platform name'] = ''
    df['Latitude'] = ''
    df['Longitude'] = ''
    df['Count'] = ''
    
    q = 0
    
    plat_lat_long_dict = {}
    
    for index, row in df2.iterrows():
        text = row['TweetText']
        lat_curr = row['Lat']
        long_curr = row['Long']
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(text))
        for url in urls:
            parsed_uri = urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            tld = get_tld(domain) # Top-Level domain
            plat_name = tld.split('.')
            if (plat_name[0],lat_curr,long_curr) not in plat_lat_long_dict:
                plat_lat_long_dict[(plat_name[0],lat_curr,long_curr)] = 1
            else:
                plat_lat_long_dict[(plat_name[0],lat_curr,long_curr)] = plat_lat_long_dict[(plat_name[0],lat_curr,long_curr)] + 1                  

    for k,v in plat_lat_long_dict.items():
        df.set_value(q, 'Platform name', k[0])
        df.set_value(q, 'Latitude', k[1])
        df.set_value(q, 'Longitude', k[2])
        df.set_value(q, 'Count', v)
        q = q + 1    
        
    df.to_csv(new_dir+'\\platform_lat_long_count.csv', sep=',', index=False)

#################################################################################################
# This function finds different geolocations where particular platform has been mentioned in twitted text at particular date-time      
#################################################################################################
    
def platform_date_lat_long():
    old_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\merged_files\\'))
    new_dir = os.path.dirname(os.path.join(APP_ROOT,'dataset_repo\\Outputs\\'))
    df1 = pd.read_csv(old_dir+"\\"+"merged_all_csv.csv", sep=',',encoding = "ISO-8859-1",error_bad_lines = False)
    
    df2 = df1[['TweetText','Lat','Long','Tweeted Datetime']]
    
    df = pd.DataFrame()
    df['Platform name'] = ''
    df['Latitude'] = ''
    df['Longitude'] = ''
    
    q = 0

    for index, row in df2.iterrows():
        text = row['TweetText']
        lat_curr = row['Lat']
        long_curr = row['Long']
        date_time = row['Tweeted Datetime']
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(text))
        for url in urls:
            parsed_uri = urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            tld = get_tld(domain) # Top-Level domain
            plat_name = tld.split('.')
            df.set_value(q, 'Platform name', plat_name[0])
            df.set_value(q, 'Date-Time', date_time)
            df.set_value(q, 'Latitude', lat_curr)
            df.set_value(q, 'Longitude', long_curr)
            q = q + 1

    df.to_csv(new_dir+'\\platform_date_lat_long.csv', sep=',', index=False) 

##########################    Function Calls    ################################
    
#make_directories()    
#merge_files()
#lat_lon_count()
#detect_languages()
#count_tweets_per_day()
#count_tweets_per_week()
#count_tweets_per_month()
#count_tweets_per_day_name()
#find_platform_names()
#count_hourly_tweets()
#hourly_per_day_count()
#hour_and_geolocation_count()
#hour_day_and_geolocation_count()
#platform_lat_long()
#plat_lat_long_count()
#platform_date_lat_long()    
UserID_1
UserID_2 = []
Edg_Freq = []
Keyword = []
Key_Freq = []
Lat = []
Lon = []
Geo_Freq = []