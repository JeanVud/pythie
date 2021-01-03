from pymongo import MongoClient

client = MongoClient('172.27.11.234:27017', username='developer', password=']ag+VB5E_samnsb~', authSource='fteluv')

print("Reading from Mongo db")

db = client.fteluv
collection = db['people']
import pandas as pd

data = pd.DataFrame(list(collection.find()))
data['_id'] = [str(x) for x in data['_id']]
from pymongo import MongoClient

client = MongoClient('172.27.11.234:27017', username='developer', password=']ag+VB5E_samnsb~', authSource='fteluv')

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

from thesis.configuration import search_config as sc


def return_list_items_ES(actor_name, sc, data):
    full_name = row['full_name']
    origin_names = row['origin_names']
    origin_names.append(full_name)
    origin_names = list(set(origin_names))

    from elasticsearch import Elasticsearch
    es = Elasticsearch([sc.ES_HOST])
    list_ = []
    for origin in origin_names:
        query = {
            "from": 0, "size": 100,
            "query": {
                "bool": {
                    "must": [
                        {
                            "function_score": {
                                "query": {
                                    "multi_match": {
                                        "query": origin,
                                        "type": "phrase",
                                        "fields": ["actors"]
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

        result = es.search(index=sc.INDEX_NAME, body=query)
        for i in range(len(result['hits']['hits'])):
            list_.append(str(result['hits']['hits'][i]['_id']))
        list_ = list(set(list_))
    return list_


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
for index, row in data.iterrows():
    list_ = return_list_items_ES(row, sc, data)
    list_ = return_list_items(row, list_, videos_info)
    data.at[index, 'item'] = list_

data['_id'] = [str(x) for x in data['_id']]

data.to_json(sc.ACTORS_OUTPUT + 'search_actors.json', orient="records", lines=True)
