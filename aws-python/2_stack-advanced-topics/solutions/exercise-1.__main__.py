import pulumi
from pulumi_aws import rds

config = pulumi.Config()
base_name = config.get("base_name") or f"{pulumi.get_organization()}-{pulumi.get_stack()}".lower()
db_username = config.get("db_username") or "dbadmin"
## Exercise 1 ##
db_password = config.require_secret("db_password")
pulumi.export("db_password", db_password)
## Exercise 1 ##

db = rds.Instance(f"{base_name}-rds", 
  instance_class="db.t3.micro",
  allocated_storage=20,
  engine="mariadb",
  engine_version="10.6",
  password=db_password,
  username=db_username,
  skip_final_snapshot=True
)

pulumi.export("db_admin", db_username)
