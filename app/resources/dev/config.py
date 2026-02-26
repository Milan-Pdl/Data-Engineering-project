

key = "milan project"
iv = "milan encryption"
salt = "milan data encryption"

#AWS Access And Secret key
aws_access_key = "your access key"
aws_secret_key = "your secret key"
bucket_name = "you aws bucket name"
s3_customer_datamart_directory = "customer_data_mart"
s3_sales_datamart_directory = "sales_data_mart"
s3_source_directory = "sales_data/"
s3_error_directory = "sales_data_error/"
s3_processed_directory = "sales_data_processed/"
s3_sales_partition_datamart_directory = "sales-partioned-datamart/"


#Database credential
# MySQL database connection properties
database_name = "de_project"
url = f"jdbc:mysql://localhost:3306/{database_name}"

properties = {
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD"),
    "driver": "com.mysql.cj.jdbc.Driver"
}

# Table name
customer_table_name = "customer"
product_staging_table = "product_staging_table"
product_table = "product"
sales_team_table = "sales_team"
store_table = "store"

#Data Mart details
customer_data_mart_table = "customers_data_mart"
sales_team_data_mart_table = "sales_team_data_mart"

# Required columns
mandatory_columns = ["customer_id","store_id","product_name","sales_date","sales_person_id","price","quantity","total_cost"]


# File Download location
# local_directory = "/opt/spark-app/files/file_from_s3/"
# yesla talako dir ma point garxa
local_directory = "D:\\Milan\\DEproject\\files\\file_from_s3\\"
customer_data_mart_local_file = "D:\\Milan\\DEproject\\files\\customer_data_mart\\"
sales_team_data_mart_local_file = "D:\\Milan\\DEproject\\files\\sales_team_data_mart\\"
sales_team_data_mart_partitioned_local_file = "D:\\Milan\DEproject\\files\\sales_partition_data\\"

error_folder_path_local = "D:\\Milan\\DEproject\\files\\error_files\\"
#  docker la,,yesla talako dir ma point garxa
# local_directory = "D:\\Milan\\DEproject\\files\\file_from_s3\\"
# error_folder_path_local="/opt/spark-app/files/error_files/"