import boto3
from botocore import UNSIGNED
from botocore.config import Config

def _get_s3_client():
    """
    Create and return an S3 client using boto3.

    Returns:
        boto3.client: An S3 client object.
    """
    return boto3.client('s3', config=Config(signature_version=UNSIGNED))

def _get_s3_keys(bucket_name, prefix):
    """
    Retrieve all keys from an S3 bucket with a given prefix.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix to filter objects in the bucket.

    Returns:
        list: A list of keys in the specified S3 bucket and prefix.
    """
    s3_client = _get_s3_client()
    paginator = s3_client.get_paginator("list_objects_v2")
    all_s3_keys = []
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get("Contents", []):
            all_s3_keys.append(obj["Key"])
    return all_s3_keys

def _get_fort63_file_keys(bucket_name, prefix):
    """
    Retrieve keys for fort.63 files from an S3 bucket with a given prefix.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix to filter objects in the bucket.

    Returns:
        list: A list of fort.63 file keys in the specified S3 bucket and prefix.
    """
    all_s3_keys = _get_s3_keys(bucket_name, prefix)
    fort63_keys = [key for key in all_s3_keys if key.split("/")[-1].startswith("fort.63_") and key.endswith(".nc")]
    return fort63_keys

def main():
    """
    Main function to demonstrate the usage of the S3 client.
    """
    BUCKET_NAME = "noaa-nos-cora-pds"
    PREFIX = "cora_gec/native_grid/water_levels"
    all_fort63_keys = _get_fort63_file_keys(BUCKET_NAME, PREFIX)
    print(f"Found {len(all_fort63_keys)} fort.63 files in the bucket '{BUCKET_NAME}' with prefix '{PREFIX}'.")
    spark.createDataFrame([(k,) for k in all_fort63_keys], ["file_key"]).write.mode("overwrite").saveAsTable("db_sandbox.practice_data_area.fort63_file_keys_param")

if __name__ == "__main__":
    main()