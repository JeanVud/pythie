import os
os.environ['SPARK_HOME'] = '/opt/spark/spark-3.0.1-bin-hadoop2.7'

import findspark
findspark.init()

import pyspark
from pyspark.mllib.linalg import Vector, Vectors
from pyspark.sql import SparkSession,SQLContext, Row, functions
from pyspark.sql.functions import asc, count, col, collect_list, monotonically_increasing_id
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.clustering import LDA

import numpy as np
import configuration

spark = SparkSession.builder.master("local[*]") \
                    .appName('Topic Modelling') \
                    .config("spark.driver.memory", "7g") \
                    .master("local[*]") \
                    .getOrCreate()
#VOCAB
path = configuration.PATHS["vocab"]["nytimes"]
vocab = spark.read.text(path)
vocab = vocab.withColumn("id", monotonically_increasing_id() + 1)
vocab = vocab.withColumnRenamed("value","word").select("id","word")

#DOCWORD
path = configuration.PATHS["docword"]["nytimes"]
df = spark.read.text(path)

metadata = df.head(3)
numDocs = int(metadata[0].value)
numWordsVocab = int(metadata[1].value)
numWordsCollection = int(metadata[2].value)

df = df.filter(df["value"].contains(" "))
split_col = pyspark.sql.functions.split(df['value'], ' ')

df = df.withColumn('docId', split_col.getItem(0)) \
        .withColumn('wordId', split_col.getItem(1)) \
        .withColumn('count', split_col.getItem(2)) \
        .drop(df['value'])

#JOIN THE DFs
joined = df.join(vocab, df.wordId == vocab.id, "left_outer")\
            .select("docId","word","count")
joined.write.parquet("/home/giangvdq/data/merged.nytimes.parquet")

def readDocWord():
    path = configuration.PATHS["merged"]["nytimes"]
    df = spark.read.parquet(path)

    metadata = df.head(3)
    numDocs = int(metadata[0].value)
    numWordsVocab = int(metadata[1].value)
    numWordsCollection = int(metadata[2].value)

    df = df.filter(df["value"].contains(" "))
    split_col = pyspark.sql.functions.split(df['value'], ' ')

    df = df.withColumn('docId', split_col.getItem(0)) \
        .withColumn('wordId', split_col.getItem(1)) \
        .withColumn('count', split_col.getItem(2)) \
        .drop(df['value'])

    df.show()