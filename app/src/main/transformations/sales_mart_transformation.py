
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from src.main.write.database_write import DatabaseWriter
from resources.dev import config


def sales_team_mart_calculation_table_write(final_sales_team_data_mart_df):
    window = Window.partitionBy("sales_person_id", "sales_month")
    
    final_sales_team_data_mart = final_sales_team_data_mart_df.withColumn("sales_date_month", 
                                            substring(col("sales_date"), 1, 7))\
        .withColumn("total_sales_every_month_by_each_sales_person",
                    sum("total_cost").over(window))\
        .select("sales_person_id", concat(col("sales_person_first_name"), lit(" "), col("sales_person_last_name")).alias("full_name"),
                 "sales_person_address", 
                "sales_month", col("total_sales_every_month_by_each_sales_person").alias("total_sales"))\
        .distinct()
    window_max_sales_in_months = Window.partitionBy("sales_month")
    final_sales_team_data_mart_incetive = final_sales_team_data_mart.withColumn("max_sales_in_month",
                                                                                max("total_sales").over(window_max_sales_in_months)
                                                                )
    final_sales_team_data_mart_incetive = final_sales_team_data_mart_incetive.withColumn("incentive",
                                          when(col("total_sales") == col("max_sales_in_month"), col("total_sales") * 0.1).otherwise(0))
    
    final_sales_team_data_mart_incetive.show(10)

    db_writer = DatabaseWriter(config.url, config.properties)
    db_writer.write_dataframe(final_sales_team_data_mart_incetive, config.sales_team_data_mart_table)