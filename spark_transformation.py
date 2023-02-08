import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
import boto3
spark=SparkSession.builder.appName('Weather-api-transformation').getOrCreate()
spark.conf.set("spark.sql.shuffle.partitions",1)
s3=boto3.client('s3')
def get_files():
    buckets=s3.list_objects(Bucket='weather-api-raw-s3')
    return buckets['Contents']
def read_json():
    input_df=spark.read.json('s3a://weather-api-raw-s3/')
    return input_df
def transformation_udf(col):
    return (col**2)*0.00256 
#spark.udf.register('transform_udf', transformation_udf)
convertudf=udf(lambda x:transformation_udf(x))
def transform_wind_mph():
    transformed_df=read_json().withColumn('psf', convertudf('wind_mph'))
    return transformed_df
def write_to_s3():
    for key in get_files():
        split_key=key['Key'].split('.json')[0]
        try:
            write_file=transform_wind_mph().coalesce(1).write.csv(f's3a://weather-api-transformed-s3/{split_key}.csv')
        except Exception:
            pass
write_to_s3()