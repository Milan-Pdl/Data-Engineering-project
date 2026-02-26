import traceback
from src.main.utility.logging_config import *
class Writer:
    def __init__(self,mode,data_format):
        self.mode = mode
        self.data_format = data_format

    def dataframe_writer(self, df, file_path):
        try:
            df.write.format(self.data_format) \
                .mode(self.mode) \
                .option("header", "true") \
                .option("path", file_path) \
                .save()  # Use .save() and pass the path here
                
            logger.info(f"Successfully wrote data to {file_path}")
            
        except Exception as e:
            logger.error(f"Error writing the data : {str(e)}")
            print(traceback.format_exc())
            raise e