# Week 4 — Postgres and RDS

## Required Homework

### Provisioned RDS Instance & Temporarily stopped an RDS instance

First things first, I provisioned the RDS instance using code below since it takes a while to spin up. However, I stopped it temporarily in AWS console since this will not be used right away.

```
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username cruddurroot \
  --master-user-password <some password> \
  --allocated-storage 20 \
  --availability-zone us-east-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```

### Tested again Postgres locally

Postgres has already been provisioned in Week 1, so just testing it now if it still works using:

```
psql -U postgres -h localhost
```

### Created database

Using the command below:

```
CREATE database cruddur;
```

has error when running in my local machine:

```
postgres-# CREATE database cruddur;
ERROR:  syntax error at or near "create"
LINE 2: create database cruddur
```

So I researched a bit and found out that I need to enclose the database name with double quotes as:

```
CREATE database "cruddur";
```


### Created schema.py

[Schema.sql](../backend-flask/db/schema.sql) is used to contain all schemas to use to populate the database

### Added UUID Extension
UUIDs are used to obscure the IDs

Added line into the schema.sql:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

The `IF NOT EXISTS` ensures a check and not throw an error when a database/table has already exist and stops the command run with error.

In repo root directory, execute command:

```
psql cruddur < db/schema.sql -h localhost -U postgres
```

### Connection URL string
Connection URL string is a way of providing all the details that it needs to authenticate to the server.

Store as env var:

```
CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
```

### Created non-extension bash scripts to facilitate DB commands

In `bin` folder, create:

- [db-connect](../backend-flask/bin-local/db-connect): This is used to connect and login to the database to perform psql commands. It accepts `prod` parameter to connect to RDS postgres DB.
- [db-create](../backend-flask/bin/db-create): This creates the database.
- [db-drop](../backend-flask/bin/db-drop): This drops the database.
- [db-schema-load](../backend-flask/bin/db-schema-load): this updates the schema based on [schema.sql](../backend-flask/db/schema.sql)
- [db-seed](../backend-flask/bin-local/db-seed): This loads initial set of data to database.
- [db-sessions](../backend-flask/bin/db-sessions): This displays all running postgres processes
- [db-setup](../backend-flask/bin/db-setup): This runs `db-drop`, `db-create`, `db-schema-load` and `db-seed` in sequence to setup and reinitialize the database.
- [rds-update-sg-rule](../backend-flask/bin/rds-update-sg-rule): This updates the RDS database security group to grant access to GitPod at a certain IP address. This is needed because the IP address of GitPod container changes in every launch.

To execute, need to change file permissions and this can be achieved by running below code:

```
chmod u+x bin/<bash script file>
```

Furthermore, as my local machine's bash is in different directory, I created the same set as above but within `bin-local` folder, except `rds-update-sg-rule` as this is needed only for GitPod.

### Modified db-create and db-drop bash files to remove database in connection string

Use linux stream editor `sed` to easily manipulate texts inline. In this case, `/cruddur` needs to be removed as a table can only be dropped when not in use and not in the connection string.

```
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c 'DROP database "cruddur";'
```

Notes:
- `schema.sql` will be a working file adding in more scripts in the build up.
- In postgres, there is the concept of schemas.  It is basically like a namespace representing different domains. `Public` is the default schema if nothing is provided in the DDL statements.

Tables created:

![Alt text](assets/week4/week4-tables-created.png)

Tables seeded:

![Alt text](assets/week4/week4-seed-created.png)


Query activities table:

![Alt text](assets/week4/week4-postgres-query-activities.png)

`db-sessions` helps check which postgres connections are idle/active.

### Driver for Postgres
- Driver is used to connect to postgres (Postgres for python)

```
psycopg[binary]
psycopg[pool]
```

### Connection Pool
- Pooling is managing multiple connections.
- pgbouncer - used for connection pooling, especially useful when using Lambda connections. But this is not used in the Cruddur application.

Created the file [db.py](../backend-flask/lib/db.py). This file has all the methods to query data from RDS database.

Modify home_activities.py

```python
    from lib.db import pool, query_wrap_array
```

```python
      sql = query_wrap_array("""
        SELECT
          activities.uuid,
          users.display_name,
          users.handle,
          activities.message,
          activities.replies_count,
          activities.reposts_count,
          activities.likes_count,
          activities.reply_to_activity_uuid,
          activities.expires_at,
          activities.created_at
        FROM public.activities
        LEFT JOIN public.users ON users.uuid = activities.user_uuid
        ORDER BY activities.created_at DESC
      """)

      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchone()
      print(json[0])
      return json[0]     
```

I successfully setup query from the backend postgres db!

![Alt text](assets/week4/week4-first-query-from-psql.png)

### Connect to RDS

Get GITPOD ID
```
GITPOD_IP=$(curl ifconfig.me)
```

Get local IP
```
LOCAL_IP=$(curl ifconfig.me)
```

Configure RDS Security Group Inbound Rule

![Alt text](assets/week4/week4-RDS-security-group-inboundrule.png)

Successful connection from local machine:

![Alt text](assets/week4/week4-RDS-local-connect.png)


Successful connection from gitpod:

![Alt text](assets/week4/week4-RDS-gitpod-connect.png)


Note that GitPod IP address changes every time it is launched. Therefore, there is a need to automate updating the RDS security group inbound rule.

Get ready with the security group ID and security group rule ID:

```
export DB_SG_ID="sg-09bde62d6040ac6d1"
gp env DB_SG_ID="sg-09bde62d6040ac6d1"
export DB_SG_RULE_ID="sgr-03e6cc44e992a9e8d"
gp env DB_SG_RULE_ID="sgr-03e6cc44e992a9e8d"

```

Execute AWS command to update security group rule to check

```
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GITPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```

To automate the above when Gitpod is launched, update gitpod.yml adding a command:

```
    command: |  
      export GITPOD_IP=$(curl ifconfig.me)
      source "$THEIA_WORKSPACE_ROOT/backend-flask/bin/rds-update-sg-rule"      
```

Test connection to production database:

In bin folder;

```
./db-connect prod
```

Load schema to production database:

In bin folder:

```
./db-schema-load prod
```

### Implemented Custom Authorizer for Cognito
- Need to have user for activities
- Need to have the cognito user id

Create Lambda function in AWS console and insert the code [Lambda function](../aws/lambdas/cruddur-post-confirmation.py).

![Alt text](assets/week4/week4-lambda-function.png)

Set environment variable `PROD_CONNECTION_URL`, the url used to connect to the RDS database. In GitPod, this is achieved by:

```
export PROD_CONNECTION_URL=<url string>
gp env PROD_CONNECTION_URL=<url string>
```

In local, this is stored in an `.env` file at application level.

### Added Lambda Layer

I encountered a permission issue.

![Alt text](assets/week4/week4-lambda-addlayer-issue.png)


Solution found in [here](https://github.com/jetbridge/psycopg2-lambda-layer).

So choosing "arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2", I was able to verify that it is working:

![Alt text](assets/week4/week4-lambda-addlayer-validate.png)

I added Lambda trigger in user pool properties in AWS console:

![Alt text](assets/week4/week4-lambda-trigger.png)

Created new policy  `AWSLambdaVPCAccessExecutionRole`:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeInstances",
                "ec2:AttachNetworkInterface"
            ],
            "Resource": "*"
        }
    ]
}
```

Added new policy to Lambda IAM role (e.g. cruddur-post-confirmation-role-05cx9vyr).

![Alt text](assets/week4/week4-lambda-newpolicy.png)

Added VPC

![Alt text](assets/week4/week4-lambda-addvpc.png)

There were errors/issues found as what Andrew encountered in the instructional video such as:
1. Incorrect string for SQL
2. Schema not updated

After ensuring that the schema.sql is ok, executed it and the SQL syntax in the lambda function is ok, I was able to successfully register, with the user information stored in the PROD database user table.

![Alt text](assets/week4/week4-lambda-post-confirm-success.png)


### Created Activities

I modified the script [create_activity.py](../backend-flask/services/create_activity.py) so that existing data can be retrieved from RDS database using `query_object_activity`, and data inserted back to RDS database using `create_activity` function.  To achieve this, [db.py](../backend-flask/lib/db.py) has been setup to have helper methods which make use of SQL statements defined in [create.sql](../backend-flask/db/sql/activities/create.sql) and in [object.sql](../backend-flask/db/sql/activities/object.sql).


### Correctly sanitize parameters passed to SQL to execute

To avoid SQL inject, it is recommended to sanitize SQL parameters. This is done for [lambda function](../aws/lambdas/cruddur-post-confirmation.py) and for [label](../backend-flask/bin/db-create)


### Debugging

Along the way, there were techniques applied to debug issues properly:
- Formatted log texts with different colors to easily see where the configured 'flags' are
- Used print() functions to output messages in the logs
- For lambda function, checked the CloudWatch logs for syntax, runtime errors when executing this function

### Refactoring

A lot of refactoring was done:
- to ensure modularity of methods
- to maintain `sql` commands separately
- to maintain and split bash scripts accordingly for ease of executing common scripts easily
- to sanitize sql parameters


### After completing the above tasks with lots of refactoring and debugging following Andrew's video and some research, I was able to create activities and store in RDS postgres database tables through local and Gitpod.

![Alt text](assets/week4/week4-create-activities-success.png)