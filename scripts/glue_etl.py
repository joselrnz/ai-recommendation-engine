import sys
import boto3
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions


bucket = "your-bucket"
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
spark = SparkSession.builder.appName("ETLJob").getOrCreate()
glueContext = GlueContext(spark)
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data from S3
input_path = f"s3://{bucket}/raw-data/user_interactions.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Data transformation (convert timestamp format)
df = df.withColumn("timestamp", df["timestamp"].cast("long"))

# Write transformed data back to S3
output_path = f"s3://{bucket}/processed-data/user_interactions/"
df.write.mode("overwrite").parquet(output_path)

job.commit()
