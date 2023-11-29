import os
import json
import pyodbc
import boto3
import base64
from botocore.exceptions import ClientError
import pandas as pd 
from datetime import datetime 
from sqlalchemy import create_engine, text 
from urllib.parse import quote_plus


def get_secret(secret):

    secret_name = secret
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id='aws_access_key_id',
        aws_secret_access_key='aws_secret_access_key'
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret
            
def sqlConnector():
  server = json.loads(get_secret("prod/BancoSQLServer"))['host']
  database = json.loads(get_secret("prod/BancoSQLServer"))['dbname']
  username = json.loads(get_secret("prod/BancoSQLServer"))['username']
  password = json.loads(get_secret("prod/BancoSQLServer"))['password']    
  conn = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  quoted = quote_plus(conn)
  new_con = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)

  return create_engine(new_con,fast_executemany=True, use_insertmanyvalues=False)
    

def get_user_unit(user_email):
    conn_str = json.loads(get_secret("prod/BancoSQLServer"))
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={conn_str['host']};DATABASE={conn_str['dbname']};UID={conn_str['username']};PWD={conn_str['password']}"
    )
    cursor = connection.cursor()
    
    # Implement your SQL query to get the unit based on the user's email
    query_unit = f"SELECT org_unit_path FROM marketing.GoogleWorkspace WHERE primary_email = '{user_email}'"
    
    cursor.execute(query_unit)
    user_unit = cursor.fetchone()
    
    connection.close()
    
    if user_unit:
        return user_unit[0]
    else:
        return None
    