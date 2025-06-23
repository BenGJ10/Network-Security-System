import os

class S3Sync:
    """
    A class to handle synchronization of local folders with AWS S3 buckets.
    This class provides methods to sync a local folder to an S3 bucket and vice versa.
    """
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        command = f"aws s3 sync {folder} {aws_bucket_url}"
        os.system(command)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        command = f"aws s3 sync {aws_bucket_url} {folder}"
        os.system(command)