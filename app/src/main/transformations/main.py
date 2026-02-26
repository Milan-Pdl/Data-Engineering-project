import os
import sys
from datetime import datetime
# 1. SETUP PROJECT PATHS
# current_dir is: .../app/src/main/transformations/
current_dir = os.path.dirname(os.path.abspath(__file__))
# app_root should point to the 'app' directory so 'src' and 'resources' are visible
# Moving up 3 levels from transformations/main.py gets you to the 'app' folder
app_root = os.path.abspath(os.path.join(current_dir, '../../..'))

if app_root not in sys.path:
    sys.path.insert(0, app_root)

# 2. SPARK & SYSTEM IMPORTS
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import shutil

# 3. PROJECT SPECIFIC IMPORTS (Now relative to app_root)
from app.src.main.upload.upload_to_s3 import UploadToS3
from app.src.main.write.parquet_writer import  Writer
from resources.dev import config 
from src.main.utility.encrypt_decrypt import *
from src.main.utility.s3_client_object import *
from src.main.utility.logging_config import * # Changed from app.src... to src...
from src.main.read import aws_read
from src.main.read.database_read import DatabaseReader
from src.main.utility import my_sql_session, spark_session
from src.main.download.aws_file_download import S3FileDownloader
from src.main.move.move_files import move_s3_to_s3
from src.main.transformations.jobs.dimension_tables_join import dimesions_table_join
from src.main.write.customer_mart_calculation_write import customer_mart_calculation_table_write
from src.main.transformations.sales_mart_transformation import sales_team_mart_calculation_table_write
from src.main.delete.local_file_delete import delete_local_file

####################### Get S3 client #######################
aws_access_key = config.aws_access_key
# aws_access_key = "BoDD3/AeLUlf6/nzioHdA5X/qL6piMZKOEZSw7+YowE="
aws_secret_key = config.aws_secret_key

s3_client_provider = S3ClientProvider((aws_access_key), (aws_secret_key))
s3_client = s3_client_provider.get_client()

# Now you can use s3_client for your S3 operations
response = s3_client.list_buckets()

logger.info("List of Buckets: %s", response['Buckets'] )

files_in_local=[files for files in os.listdir(config.local_directory) if files.endswith(".csv")]

database_conn=my_sql_session.get_mysql_connection()
cursor=database_conn.cursor()

if files_in_local:
    statement=f"""select distinct file_name from de_project.product_staging_table
                where file_name in ({str(files_in_local)[1:-1]}) and status='A' """
    
    cursor.execute(statement)
    data=cursor.fetchall()
    cursor.close()

    if data:
        logger.info("last run was failed")
    else:
        logger.info("NO record match")
else:
    logger.info("last run was successful")
    

# read data from s3
try:
    read_file=aws_read.S3Reader()
    # yo  foler path bata file read garna
    folder_path=config.s3_source_directory
    s3_absoute_file_path=read_file.list_files(
        s3_client,
        config.bucket_name,
        folder_path=folder_path
    )
    logger.info(f"The absolute file path on s3 bucketis {s3_absoute_file_path}")
except Exception as e:
    logger.error(f'{e}')

# aaba s3 ma vako data lai local ma load garna
bucket_name=config.bucket_name
directory_name=config.local_directory
prefix=f"s3://{bucket_name}/"
file_path=[url[len(prefix):] for url in s3_absoute_file_path]
logger.info(f"file available on s3 under {bucket_name} bucket and fllder name is {file_path}")

try:
    downloader=S3FileDownloader(s3_client,bucket_name,directory_name)
    downloader.download_files(file_path)
except Exception as e:
    logger.info(f"There is an error::{e}")

#file ta aaba hami la s3 bata local ma layim, aaba csv vanada aarru file aako xa vala teslai error files vanna dir ma rkhna
all_files=os.listdir(directory_name)
logger.info(f"The list of file after downloading from a s3 to local are {all_files}")
error_files=config.error_folder_path_local

if all_files:
    error_file=[]
    csv_file=[]
    for file in all_files:
        if not str(file).endswith('.csv'):
            error_file.append(os.path.abspath(os.path.join(directory_name,file)))
        else:
            csv_file.append(os.path.abspath(os.path.join(directory_name,file)))

    if error_file:
        logger.info(f"The error files are {error_file}")
    else:
        logger.info("There is no error files::")

else:
    logger.error(f"There is no data to process::")
    raise Exception("NO any csv data to process ")



logger.info(f"The csv file that is need to process are {csv_file}")

logger.info("**************creating spark session************")
spark=spark_session.spark_session()


# schema validation
corrected_file=[]
for data in csv_file:
    data_schema=spark.read.format("csv")\
                .option("header","true")\
                .load(data).columns
    logger.info(f"the schema for data {data} is {data_schema}")
    logger.info(f"The mandatory column are {config.mandatory_columns}")
    missing_column=set(config.mandatory_columns)-set(data_schema)

    if missing_column:
        error_file.append(data)
    else:
        logger.info(f"There is no any missing columm")
        corrected_file.append(data)

logger.info(f"The list of corrected file are {corrected_file}")
logger.info(f"The list of error file are {error_file}")

logger.info("moving error data to error directory::")

# move directory on error directory in local
erro_file_local_path=config.error_folder_path_local

if error_file:
    for error_files in error_file:
            if os.path.exists(error_files):
                file_name=os.path.basename(error_files)
                destination_path=os.path.join(erro_file_local_path,file_name)
                shutil.move(error_files, destination_path)
                logger.info(f"error file moved from {error_file,destination_path}")
            else:
                logger.info(f"no such path {error_file} exist")
            
            # moving in s3
            source_prefix=config.s3_source_directory
            destination_prefix=config.s3_error_directory
            meessage=move_s3_to_s3(s3_client,config.bucket_name,source_prefix,destination_prefix,file_name)
else:
    logger.info("NO any error files::")


# additional column should be taken care of 
# determine extra column

logger.info(f"******updatinf the satus of  product_staging_table****************")
insert_statement=[]
current_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if corrected_file:
    for file in corrected_file:
        file_name=os.path.basename(file)
        statement=f"""insert into de_project.product_staging_table (file_name,file_location,status,created_date) values ('{file_name}','{file}','A','{current_date}')"""
        insert_statement.append(statement)
    logger.info(f"The insert statement is {insert_statement}")

    logger.info("connecting to database and updating the status of product_staging_table")
    cursor=database_conn.cursor()
    logger.info("connected to database successfully")

    for statement in insert_statement:
        cursor.execute(statement)
        database_conn.commit()
        logger.info(f"The status of file {statement} is updated successfully in product_staging_table")
else:

    logger.info("There is no any corrected file to update the status in product_staging_table")
    raise Exception("NO any corrected file to update the status in product_staging_table")

logger.info("**************staging process completed successfully************")

logger.info("Fixing extra column issue")

schema=StructType([
    StructField("customer_id",StringType(),True),
    StructField("store_id",StringType(),True),
    StructField("product_name",StringType(),True),
    StructField("sales_date",StringType(),True),
    StructField("sales_person_id",StringType(),True),
    StructField("price",StringType(),True),
    StructField("quantity",StringType(),True),
    StructField("total_cost",StringType(),True)])

logger.info(f"Creating empty dataframe with required schema to handle extra column issue")

# empty_df=spark.createDataFrame([],schema)
# empty_df.show()


database_client=DatabaseReader(config.url,config.properties)
final_df_to_process=database_client.create_dataframe(spark,"empty_df")
final_df_to_process.show()


for data in corrected_file:
    data_df=spark.read.format("csv")\
                .option("header","true")\
                .load(data)
    logger.info(f"The data frame created for {data} is {data_df}")
    data_schema=data_df.columns
    extra_column=set(data_schema)-set(config.mandatory_columns)
    if extra_column:
        data_df=data_df.withColumn('additional_cloumn',concat_ws(',',*extra_column)) \
        .select("customer_id","store_id","product_name","sales_date","sales_person_id","price","quantity","total_cost","additional_cloumn")
        logger.info(f"processed {data} with extra column {extra_column} and added additional column with name additional_cloumn")
    else:
        data_df=data_df.withColumn('additional_cloumn',lit(None).cast(StringType())) \
        .select("customer_id","store_id","product_name","sales_date","sales_person_id","price","quantity","total_cost","additional_cloumn")
        logger.info(f"processed {data} with no extra column and added additional column with name additional_cloumn with null value")
        final_df_to_process=final_df_to_process.unionByName(data_df,allowMissingColumns=True)
        logger.info(f"The final dataframe to process is {final_df_to_process.show()}")


logger.info("***********starting for preparing data for data mart*************")

logger.info("creating dataframe for customer table from mysql database")
customer_table_df=database_client.create_dataframe(spark,config.customer_table_name)

logger.info("creating dataframe for product table from mysql database")
product_table_df=database_client.create_dataframe(spark,config.product_table)

logger.info("creating dataframe for sales team table from mysql database")
sales_team_table_df=database_client.create_dataframe(spark,config.sales_team_table)

logger.info("creating dataframe for store table from mysql database")
store_table_df=database_client.create_dataframe(spark,config.store_table)

logger.info("***********preparing data for product staging*************")
product_staging_table_df=database_client.create_dataframe(spark,config.product_staging_table)

s3_customer_store_sales_df_join=dimesions_table_join(final_df_to_process,customer_table_df,store_table_df,sales_team_table_df)

logger.info(f"The final dataframe after joining with dimension table is {s3_customer_store_sales_df_join.show()}")
# At the very end of your script
logger.info('writing  data into customer data mart')


final_customer_datamart_df = s3_customer_store_sales_df_join.select(
    col("ct.customer_id"),
    col("ct.first_name"),
    col("ct.last_name"),
    col("ct.address"),
    col("ct.pincode"),
    "phone_number",
    "sales_date",
    "total_cost"
)

logger.info(f"The final dataframe for customer datamart is {final_customer_datamart_df.show()}")

logger.info("writing data in local as parquet format")
parquet_writer=Writer(mode="overwrite",data_format="parquet")
parquet_writer.dataframe_writer(final_customer_datamart_df,config.customer_data_mart_local_file)

logger.info(f"The data is written in local directory {config.customer_data_mart_local_file} in parquet format successfully")

logger.info(f"writing data in s3 {config.s3_customer_datamart_directory} as parquet format")


s3_uploader=UploadToS3(s3_client)
message=s3_uploader.upload_to_s3(config.s3_customer_datamart_directory,config.bucket_name,config.customer_data_mart_local_file)

logger.info(message)

#sales_team Data Mart
logger.info("*********** write the data into sales team Data Mart **********")
final_sales_team_data_mart_df = s3_customer_store_sales_df_join\
    .select("store_id",
            "sales_person_id", "sales_person_first_name", "sales_person_last_name",
            "store_manager_name", "manager_id", "is_manager",
            "sales_person_address", "sales_person_pincode",
            "sales_date", "total_cost",
            expr("SUBSTRING(sales_date, 1, 7) as sales_month"))

logger.info("writing data in local as parquet format")

logger.info(f"The final dataframe for sales team datamart is {final_sales_team_data_mart_df.show()}")

logger.info("writing data in local as parquet format")
parquet_writer=Writer(mode="overwrite",data_format="parquet")
parquet_writer.dataframe_writer(final_sales_team_data_mart_df,config.sales_team_data_mart_local_file)

s3_uploader=UploadToS3(s3_client)
message=s3_uploader.upload_to_s3(config.s3_sales_datamart_directory,config.bucket_name,config.sales_team_data_mart_local_file)
logger.info(message)

logger.info("writing data in s3 in partitioned format for sales team datamart")
# also writing data into partitioned directory in s3 for sales team datamart
final_sales_team_data_mart_df.write.format("parquet").mode("overwrite")\
    .partitionBy("sales_month","store_id")\
    .save(config.sales_team_data_mart_partitioned_local_file)

logger.info(f"The data is written in local directory {config.sales_team_data_mart_partitioned_local_file} in parquet format successfully")

logger.info(f"writing data in s3 {config.s3_sales_partition_datamart_directory} as parquet format")
s3_uploader.upload_to_s3(config.s3_sales_partition_datamart_directory,
                         config.bucket_name,
                         config.sales_team_data_mart_partitioned_local_file)
logger.info(f"The data is written in s3 bucket {config.bucket_name} and directory {config.s3_sales_partition_datamart_directory} in parquet format successfully")

# calculation for customer datamart
customer_mart_calculation_table_write(final_customer_datamart_df)

# calculation for sales team datamart and giving incentive to sales person based on the sales in month

logger.info("calculation for sales team datamart")
sales_team_mart_calculation_table_write(final_sales_team_data_mart_df)

logger.info("***********moving the process data in processed folder in s3*************")

message=move_s3_to_s3(s3_client,config.bucket_name,config.s3_source_directory,config.s3_processed_directory,file_path)
logger.info(message)

logger.info("***********deleting sales data from local*************")
delete_local_file(config.local_directory)


logger.info("***********deleting customer datamart data from local*************")
delete_local_file(config.customer_data_mart_local_file)

logger.info("***********deleting sales team datamart data from local*************")
delete_local_file(config.sales_team_data_mart_local_file)

logger.info("***********deleting sales team partition datamart data from local*************")
delete_local_file(config.sales_team_data_mart_partitioned_local_file)

logger.info("All local files are deleted successfully")

# update the status of the file in product_staging_table to 'P' for processed
update_statement=[]
current_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
database_conn=my_sql_session.get_mysql_connection()
cursor=database_conn.cursor()
if corrected_file:
    for file in corrected_file:
        file_name=os.path.basename(file)
        statement=f"""update de_project.product_staging_table set status='P', updated_date='{current_date}' where file_name='{file_name}'"""
        update_statement.append(statement)
        logger.info(f"The update statement is {update_statement}")
    for statement in update_statement:
        cursor.execute(statement)
        database_conn.commit()
        logger.info(f"The status of file {statement} is updated successfully in product_staging_table")
else:
    logger.info("There is no any corrected file to update the status in product_staging_table")
    raise Exception("NO any corrected file to update the status in product_staging_table")

logger.info("**************ETL process completed successfully************")
input("Press Enter to stop the Spark Session and close the UI...")
spark.stop()
