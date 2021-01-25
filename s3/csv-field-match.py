import boto3
import pandas as pd

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

# Script variables
bucket_name = ""
csv_separator = ";"
sub_folder = ""
column_name = ""
matching_value = ""
object_name_pattern = ""

my_bucket = s3.Bucket(bucket_name)

"""
    Receive Object metadada, read csv and match from any value.
    @param file
        s3 file
"""
def read_data(file):    
    result = None
    try:
        df = pd.read_csv(file, sep=csv_separator)
        for index, row in df.iterrows():
            if row[column_name] == matching_value:
                print("Do Something and return result")
    except pd.errors.EmptyDataError:
        # Catch exception if any file is Empty
        df = pd.DataFrame()

    return result

for file in my_bucket.objects.filter(Prefix=sub_folder):
    key = file.key
    # myBycket/subfilder/filename.csv
    file_name = (key.split("/"))[-1]
    name_file = (file_name.split("."))[0]
    object_name = (name_file.split("_"))[-1]
    if object_name_pattern in object_name:
        #Revisar Bucket
        obj = s3_client.get_object(Bucket=bucket_name, Key=key)
        result = read_data(obj['Body'])
        if result is not None:
            print(result)