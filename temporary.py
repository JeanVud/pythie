# [giangvdq@clientnode03-172-27-11-233 ~]$ cat /projects/fplay/sources/fplay-search/personalized_search/run_meta.sh
# echo "Run TV Channels"
# python tv_channels.py
# echo "Run create data channels"
# python create_data_channels.py
# echo "Run generate meta data"
# python generate_processed_meta_data.py -d $1
# echo "Run create meta data"
# python create_data_fplay.py -d $1
# echo "Run generate actors"
# python actors.py 
# echo "Run create data actors"
# python create_data_actors.py


#/projects/fplay/sources/fplay-search/personalized_search/tv_channels.py
from pymongo import MongoClient
client = MongoClient('127.0.0.1:27017')
db = client.fteluv
collection = db['tvchannels']
cursor = collection.find({})

import pandas as pd
data = pd.DataFrame(list(collection.find()))



data = data[['GEOIP_COUNTRY_CODE_availability', '_id','group_id','status', 'alias_name', 'imgPath','platforms', 'description']]


data[data.alias_name.str.find('Vĩnh Long') != -1]

data['alias_name'] = [x.lower() for x in data['alias_name']]

data.head()

data[data.alias_name.str.find('vĩnh') != -1]


#/projects/fplay/sources/fplay-search/personalized_search/create_data_channels.py

#/projects/fplay/sources/fplay-search/personalized_search/generate_processed_meta_data.py


#/projects/fplay/sources/fplay-search/personalized_search/create_data_fplay.py

#/projects/fplay/sources/fplay-search/personalized_search/actors.py


from pymongo import MongoClient

print("Reading from Mongo db")

db = client.fteluv
collection = db['people']
import pandas as pd
data = pd.DataFrame(list(collection.find()))
data['_id'] = [str(x) for x in data['_id']]
db = client.fteluv
collection = db['videos_ver2']
import pandas as pd
videos_info = pd.DataFrame(list(collection.find()))
videos_info.head()
videos_info['_id'] = [str(x) for x in videos_info['_id']]

def left_right_strip(text):
    text = text.rstrip()
    text = text.lstrip()
    return text
def strip_text(string):
    for i in range(len(string)):
        string[i] = left_right_strip(string[i])
    return string

videos_info['actors'] = videos_info.actors.apply(strip_text)

from bson.objectid import ObjectId

import math
import numpy as np

def return_list_items(row, potential_list, videos_info):
    full_name = row['full_name']
    origin_names = row['origin_names']
    origin_names.append(full_name)
    origin_names = list(set(origin_names))

    result = []

    for index_ in potential_list:
        row_video = videos_info[videos_info._id == index_]
        if len(row_video['actors'].values) == 0:
            continue
        list_actors = row_video['actors'].values[0]
        if isinstance(list_actors, list):
            for name in origin_names:
                if name in list_actors:
                    result.append(index_)
                    break
    return result


data['item'] = ''
list_ = ''
for index, row in data.iterrows():
    list_ = return_list_items(row, list_, videos_info)
    data.at[index, 'item'] = list_

data['_id'] = [str(x) for x in data['_id']]

#/projects/fplay/sources/fplay-search/personalized_search/create_data_actors.py
