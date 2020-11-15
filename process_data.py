import os
os.environ['SPARK_HOME'] = '/opt/spark/spark-3.0.1-bin-hadoop2.7'
import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession, functions


spark = SparkSession.builder.master("local[*]") \
                    .appName('Topic Modelling') \
                    .getOrCreate()

path = '/home/giangvdq/data/docword.enron.txt.gz'
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
df.show()
df.select(df.docId).distinct().show()

#count = df.select(df.docId).distinct.show()
#print(count)
