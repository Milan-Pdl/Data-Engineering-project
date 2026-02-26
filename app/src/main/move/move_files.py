import traceback
from src.main.utility.logging_config import *
import os
# def move_s3_to_s3(s3_client, bucket_name, source_prefix, destination_prefix):
#     try:
#         response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=source_prefix)

#         for obj in response.get('Contents', []):
#             source_key = obj['Key']
#             destination_key = destination_prefix + source_key[len(source_prefix):]

#             s3_client.copy_object(Bucket=bucket_name,
#                                   CopySource={'Bucket': bucket_name,
#                                               'Key': source_key}, Key=destination_key)

#             s3_client.delete_object(Bucket=bucket_name, Key=source_key)
#         return f"Data Moved succesfully from {source_prefix} to {destination_prefix}"
#     except Exception as e:
#         logger.error(f"Error moving file : {str(e)}")
#         traceback_message = traceback.format_exc()
#         print(traceback_message)
#         raise e


def move_s3_to_s3(s3_client, bucket_name, source_prefix, destination_prefix,file_name=None):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=source_prefix)

        if file_name is None:
            for obj in response.get('Contents', []):
                # get la value linxa, yedi kai xaina vana error falnu ko satta empty string falxa
                source_key = obj['Key']
                destination_key = destination_prefix + source_key[len(source_prefix):]

                s3_client.copy_object(Bucket=bucket_name,
                                      CopySource={'Bucket': bucket_name,
                                                  'Key': source_key}, Key=destination_key)

                s3_client.delete_object(Bucket=bucket_name, Key=source_key)
            # return f"Data Moved succesfully from {source_prefix} to {destination_prefix}"
        else:
            for obj in response.get('Contents', []):
                source_key = obj['Key']
                logger.info(f"The source key is {source_key}***************************")
                # maila pachi add garako logic, yedi file name xa vane matra move garne, file name xaina vane sabai move garne
                for file_name in file_name:
                    prefix=os.path.basename(file_name)
                    logger.info(f"The prefix is {prefix}***************************")

                    if source_key.endswith(str(prefix)):
                        logger.info(f"Moving file: {source_key} to {destination_prefix}**************")
                        destination_key = destination_prefix + source_key[len(source_prefix):]

                        s3_client.copy_object(Bucket=bucket_name,
                                            CopySource={'Bucket': bucket_name,
                                                        'Key': source_key}, Key=destination_key)

                        s3_client.delete_object(Bucket=bucket_name, Key=source_key)
                        logger.info(f"Moved file: {source_key} to {destination_key}")
                    else:
                        logger.info(f"Skipped file: {source_key} as it does not match the specified file name: {file_name}")

            return f"Data Moved successfully from {source_prefix} to {destination_prefix}"
    except Exception as e:
        logger.error(f"Error moving file : {str(e)}")
        traceback_message = traceback.format_exc()
        print(traceback_message)
        raise e


def move_local_to_local():
    pass
