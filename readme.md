🚀 Spark-Based ETL Pipeline with AWS S3 and MySQL

📌 Project Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline using:

PySpark for distributed data processing

AWS S3 for data ingestion and storage

MySQL for staging and metadata tracking

Parquet format for optimized analytics storage

The pipeline processes sales CSV files from S3, validates schema, manages staging status, joins dimension tables, and generates Customer and Sales Team Data Marts.

🏗 Architecture Overview
S3 (Raw Files)
      ↓
Download to Local
      ↓
Schema Validation
      ↓
Error Handling (Local + S3 Error Folder)
      ↓
Staging Table Update (MySQL)
      ↓
Spark Transformations
      ↓
Dimension Table Joins
      ↓
Customer Data Mart
Sales Team Data Mart
      ↓
Write Parquet (Local + S3)
      ↓
Move Files to Processed Folder
      ↓
Update Staging Status

🔄 ETL Workflow
1️⃣ Extract Phase

List files from S3 source directory

Download files to local directory

Identify:

Valid CSV files

Invalid (non-CSV) files → moved to error folder

2️⃣ Validation Phase

Validate schema against mandatory columns

Detect:

Missing columns

Extra columns

Extra columns are captured in additional_column

Invalid files are:

Moved to local error folder

Moved to S3 error directory

3️⃣ Staging Layer

Insert file metadata into product_staging_table

Track file lifecycle using:

A → Active (staged)

P → Processed


4️⃣ Transformation Phase (Spark)

Create Spark session

Load validated CSV files

Handle:

Missing columns

Extra columns

Union all corrected files

Join with dimension tables:

Customer

Store

Sales Team

Product

5️⃣ Data Mart Creation
🧍 Customer Data Mart

Contains:

Customer details

Sales date

Total cost

Output:

Local Parquet

Uploaded to S3

🏪 Sales Team Data Mart

Contains:

Store info

Sales person info

Monthly aggregation

Partitioned by:

sales_month

store_id

Output:

Local Parquet

S3 upload

Partitioned storage

6️⃣ Post-Processing

Move processed files to S3 processed directory

Delete local temporary files

Update staging table status to P

Stop Spark session

✅ Partitioned Data Strategy

Sales Team Data Mart is written using:

partitionBy("sales_month", "store_id")

This improves:

Query performance

Scalability

Analytical efficiency


Project STructure

DE_MILAN/
├── app/
│   ├── resources/
│   └── src/
│       └── main/
│           ├── delete/
│           │   ├── aws_delete.py
│           │   ├── database_delete.py
│           │   └── local_file_delete.py
│           ├── download/
│           │   └── aws_file_download.py
│           ├── move/
│           │   └── move_files.py
│           ├── read/
│           │   ├── aws_read.py
│           │   └── database_read.py
│           ├── transformations/
│           │   ├── jobs/
│           │   ├── __init__.py
│           │   ├── main.py
│           │   └── sales_mart_transformation.py
│           ├── upload/
│           │   └── upload_to_s3.py
│           └── utility/
│               ├── encrypt_decrypt.py
│               ├── logging_config.py
│               ├── my_sql_session.py
│               ├── s3_client_object.py
│               ├── spark_session.py
│               ├── write/
│               │   └── __init__.py
│               └── __init__.py
├── test/
│   ├── extra_column_csv_generate.py
│   ├── generate_csv_data.py
│   ├── generate_customer_table.py
│   ├── generate_datewise_sales_d.py
│   ├── less_column_csv_generated.py
│   ├── sales_data_upload_s3.py
│   └── __init__.py
├── __init__.py
└── requirements.txt



📈 Scalability Considerations

This pipeline can be scaled further by:

Using Apache Airflow for orchestration

Running on EMR / Databricks

Containerizing with Docker

Implementing batch partition pruning

Adding data quality validation rules

Using connection pooling for database operations

Using parameterized SQL queries for safe scaling

🔮 Future Improvements

Add Airflow DAG orchestration

Implement CI/CD pipeline

Add automated data quality checks

Introduce Delta Lake

Use IAM roles instead of static credentials

Add structured logging (CloudWatch / ELK)

Implement retry mechanisms


🎯 Learning Outcomes

This project demonstrates:

End-to-end ETL design

Cloud data ingestion

Spark-based transformation

Data warehouse concepts

File lifecycle management

Partitioned data lake strategy