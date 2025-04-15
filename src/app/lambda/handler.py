import json
import boto3
import pymysql
import os

# RDS connection info (use env vars or AWS Secrets Manager)
RDS_HOST = os.environ['RDS_HOST']
RDS_USER = os.environ['RDS_USER']
RDS_PASSWORD = os.environ['RDS_PASSWORD']
RDS_DB = os.environ['RDS_DB']

def connect_db():
    return pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

def insert_user(data):
    connection = connect_db()
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO users (customerId, firstName, lastName, age, city, email, accountBalance, creditLimit, creditCardBalance)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            data['customerId'],
            data['firstName'],
            data['lastName'],
            int(data['age']),
            data['city'],
            data['email'],
            int(data['accountBalance']),
            int(data['creditLimit']),
            int(data['creditCardBalance'])
        ))
        connection.commit()
    connection.close()

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    # Get file info from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Get the uploaded file
    obj = s3.get_object(Bucket=bucket, Key=key)
    raw_data = obj['Body'].read().decode('utf-8')
    user_data = json.loads(raw_data)

    # Insert to RDS
    try:
        insert_user(user_data)
        return {
            "statusCode": 200,
            "body": f"✅ User {user_data['customerId']} inserted into RDS"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"❌ Error inserting user: {str(e)}"
        }
