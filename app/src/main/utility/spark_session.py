import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from src.main.utility.logging_config import *
import os
import sys

import os
import sys
from pyspark.sql import SparkSession

def spark_session():
    # Force alignment between Java and Python
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    
    # Point directly to your Spark installation
    os.environ['SPARK_HOME'] = r'C:\spark\spark-4.1.1-bin-hadoop3'

    return SparkSession.builder \
        .appName("MyDEProject") \
        .master("local[*]") \
        .config("spark.driver.host", "localhost") \
        .config("spark.sql.execution.pyspark.udf.faulthandler.enabled", "true") \
        .getOrCreate()