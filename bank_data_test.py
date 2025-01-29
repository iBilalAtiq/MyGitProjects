from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Initialize Spark session
spark = SparkSession.builder \
    .appName("siddiq_buc") \
    .getOrCreate()

# Path to the dataset in GCS
file_path = "gs://siddiq_buc/test.csv"

# Load the dataset into a DataFrame
df = spark.read.option("header", "true").csv(file_path)

# Data Preprocessing: Convert columns to appropriate data types
df = df.withColumn("Account_Balance", df["Account_Balance"].cast("float"))

# 1. Grouping by Country and calculating the average salary
avg_account_balance = df.agg(F.avg("Account_Balance").alias("Average_Account_Balance"))

# Write the result to a single CSV file in GCS
avg_account_balance.coalesce(1).write.mode("overwrite").option("header", "true").csv("gs://siddiq_buc/output_new")


# Stop the Spark session
spark.stop()
