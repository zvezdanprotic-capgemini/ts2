# {
#     "Records": [
#       {
#         "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
#         "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
#         "body": "{\n     \"CaseId\":\"5001A00000aXyzQAB\",\n     \"Name\": \"Martha Rivera\"\n}",
#         "attributes": {
#           "ApproximateReceiveCount": "1",
#           "SentTimestamp": "1545082649183",
#           "SenderId": "AIDAIENQZJOLO23YVJ4VO",
#           "ApproximateFirstReceiveTimestamp": "1545082649185"
#         },
#         "messageAttributes": {},
#         "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
#         "eventSource": "aws:sqs",
#         "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:my-queue",
#         "awsRegion": "us-west-2"
#       }
#     ]
# }


# import sys
# import logging
# import pymysql
# import json
# import os

# # rds settings
# user_name = os.environ['USER_NAME']
# password = os.environ['PASSWORD']
# rds_proxy_host = os.environ['RDS_PROXY_HOST']
# db_name = os.environ['DB_NAME']

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# try:
#         conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
# except pymysql.MySQLError as e:
#     logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
#     logger.error(e)
#     sys.exit(1)

# logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

# def lambda_handler(event, context):

#     logger.info(event)

#     message = ''

#     try:
#         # Handle the first format where 'value' contains JSON
#         recordspart = event['node']['inputs'][0]['value']
#         try:
#             # Try to parse as JSON first
#             recordspartjson = json.loads(recordspart)
#             message = recordspartjson['Records'][0]['body']
#         except json.JSONDecodeError:
#             # If it's not JSON, check for the CaseId=XXXX format
#             if 'CaseId=' in recordspart:
#                 CaseId = recordspart.split('CaseId=')[1].strip()
#                 message = json.dumps({
#                     'CaseId': CaseId
#                 })
#             else:
#                 # New format handling: direct value assignment
#                 message = json.dumps({
#                     'CaseId': recordspart.strip()
#                 })
#     except Exception as e:
#         try:
#             # Handle the Records format
#             message = event['Records'][0]['body']
#         except Exception as e:
#             try:
#                 # Last attempt to extract CaseId
#                 if 'node' in event and 'inputs' in event['node'] and len(event['node']['inputs']) > 0:
#                     recordspart = event['node']['inputs'][0].get('value', '')
#                     if 'CaseId=' in recordspart:
#                         CaseId = recordspart.split('CaseId=')[1].strip()
#                         message = json.dumps({
#                             'CaseId': CaseId
#                         })
#                     else:
#                         message = json.dumps({
#                             'CaseId': recordspart.strip()
#                         })
#                 else:
#                     logger.error(f"Could not extract CaseId from event: {event}")
#                     return
#             except Exception as e:
#                 logger.error(f"Error processing input: {e}")
#                 return

#     try:
#         data = json.loads(message)
#         CaseId = data['CaseId']
#     except Exception as e:
#         logger.error(f"Error parsing message as JSON: {e}")
#         return

#     item_count = 0
#     with conn.cursor() as cur:
#         cur.execute("select * from SHCases where CaseId = %s", (CaseId))
#         for row in cur:
#             item_count += 1
#             #print(row)
#     conn.commit()

#     return f"CaseId: {row[0]}, CaseNumber: {row[1]}, Status: {row[2]}, Priority: {row[3]}, Subject: {row[4]}, Description: {row[5]}, AccountId: {row[6]}, ContactId: {row[7]}"

#     # return  {
#     #     'body': json.dumps({
#     #         'CaseId': row[0],
#     #         'CaseNumber': row[1],
#     #         'Status': row[2],
#     #         'Priority': row[3],
#     #         'Subject': row[4],
#     #         'Description': row[5],
#     #         'AccountId': row[6],
#     #         'ContactId': row[7]
#     #     })
#     # }

import sys
import logging
import pymysql
import json
import os

# rds settings
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
        conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(event, context):

    logger.info(event)

    message = ''

    try:
        # Handle the first format where 'value' contains JSON
        recordspart = event['node']['inputs'][0]['value']
        try:
            # Try to parse as JSON first
            recordspartjson = json.loads(recordspart)
            message = recordspartjson['Records'][0]['body']
        except json.JSONDecodeError:
            # If it's not JSON, check for the CaseId=XXXX format
            if 'CaseId=' in recordspart:
                CaseId = recordspart.split('CaseId=')[1].strip()
                message = json.dumps({
                    'CaseId': CaseId
                })
            else:
                # New format handling: direct value assignment
                message = json.dumps({
                    'CaseId': recordspart.strip()
                })
    except Exception as e:
        try:
            # Handle the Records format
            message = event['Records'][0]['body']
        except Exception as e:
            try:
                # Last attempt to extract CaseId
                if 'node' in event and 'inputs' in event['node'] and len(event['node']['inputs']) > 0:
                    recordspart = event['node']['inputs'][0].get('value', '')
                    if 'CaseId=' in recordspart:
                        CaseId = recordspart.split('CaseId=')[1].strip()
                        message = json.dumps({
                            'CaseId': CaseId
                        })
                    else:
                        message = json.dumps({
                            'CaseId': recordspart.strip()
                        })
                else:
                    # Log detailed error for debugging but return generic message to user
                    logger.error(f"Could not extract CaseId from event: {event}")
                    return "Error: Invalid event format. Missing required inputs."
            except Exception as e:
                # Log detailed error for debugging but return generic message to user
                logger.error(f"Error processing input: {e}")
                return "Error: Problem processing the request."

    try:
        data = json.loads(message)
        CaseId = data['CaseId']
    except Exception as e:
        # Improved error handling: Log detailed error for debugging but return generic message to user
        logger.error(f"Error parsing message as JSON: {e}")
        return "Error: Invalid message format. Please check your input."

    item_count = 0
    with conn.cursor() as cur:
        # Fixed SQL injection vulnerability - properly parameterized query
        cur.execute("select * from SHCases where CaseId = %s", (CaseId,))
        for row in cur:
            item_count += 1
            #print(row)
    conn.commit()

    # return  {
    #     'body': json.dumps({
    #         'CaseId': row[0],
    #         'CaseNumber': row[1],
    #         'Status': row[2],
    #         'Priority': row[3],
    #         'Subject': row[4],
    #         'Description': row[5],
    #         'AccountId': row[6],
    #         'ContactId': row[7]
    #     })
    # } 
    return f"CaseId: {row[0]}, CaseNumber: {row[1]}, Status: {row[2]}, Priority: {row[3]}, Subject: {row[4]}, Description: {row[5]}, AccountId: {row[6]}, ContactId: {row[7]}"