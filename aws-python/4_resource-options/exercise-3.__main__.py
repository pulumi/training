import pulumi
from pulumi_aws import s3

config = pulumi.Config()
base_name = config.require("base_name")

# Create an AWS resource (S3 Bucket)
my_old_bucket_name = f"{base_name}-bucket"
my_bucket_name = f"{base_name}-funky-bucket"

bucket = s3.Bucket(my_bucket_name,
  bucket=my_old_bucket_name,
  opts=<fill in here>
)

pulumi.export("bucket_name", bucket.id)